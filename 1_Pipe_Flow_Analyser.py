"""
Module A: Pipe Flow Analyser
Complete pipe flow calculator using Darcy-Weisbach equation.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from engineering import Fluid, Pipe
import io

st.set_page_config(page_title="Pipe Flow Analyser", page_icon="💧", layout="wide")

st.title("💧 Module A – Pipe Flow Analyser")
st.markdown("""
Calculate velocity, Reynolds number, Darcy friction factor and pressure drop for steady incompressible flow in a circular pipe.
Uses the **Darcy-Weisbach** equation with the **Haaland explicit approximation** for turbulent friction factor.
""")

# ---------- Sidebar Inputs ----------
st.sidebar.header("Fluid Selection")
fluid_choice = st.sidebar.selectbox(
    "Select fluid",
    ["Water (20°C)", "Air (20°C)", "Crude Oil (typical)", "User-defined"]
)

if fluid_choice == "Water (20°C)":
    fluid = Fluid.water()
elif fluid_choice == "Air (20°C)":
    fluid = Fluid.air()
elif fluid_choice == "Crude Oil (typical)":
    fluid = Fluid.crude_oil()
else:
    st.sidebar.subheader("Custom Fluid Properties")
    name = st.sidebar.text_input("Fluid name", value="Custom Fluid")
    density = st.sidebar.number_input("Density ρ (kg/m³)", min_value=0.1, value=1000.0, step=1.0)
    viscosity = st.sidebar.number_input("Dynamic viscosity μ (Pa·s)", min_value=1e-6, value=0.001, format="%.6f")
    fluid = Fluid.custom(name, density, viscosity)

st.sidebar.markdown(f"**Current fluid:** {fluid.name}  
ρ = {fluid.density:.3f} kg/m³ | μ = {fluid.viscosity:.6f} Pa·s")

st.sidebar.header("Pipe Geometry")
diameter_mm = st.sidebar.number_input("Internal diameter D (mm)", min_value=1.0, value=50.0, step=1.0)
length_m = st.sidebar.number_input("Pipe length L (m)", min_value=0.1, value=100.0, step=1.0)
roughness_mm = st.sidebar.number_input("Absolute roughness ε (mm)", min_value=0.0, value=0.045, step=0.001, format="%.3f",
                                       help="Typical values: drawn tubing 0.0015 mm, commercial steel 0.045 mm, cast iron 0.26 mm")

st.sidebar.header("Flow Conditions")
flow_unit = st.sidebar.selectbox("Flow rate unit", ["m³/s", "L/s", "m³/h"])
q_input = st.sidebar.number_input("Volumetric flow rate", min_value=0.0, value=0.01 if flow_unit == "m³/s" else 10.0, step=0.001)

# Convert to SI
if flow_unit == "L/s":
    q = q_input / 1000.0
elif flow_unit == "m³/h":
    q = q_input / 3600.0
else:
    q = q_input

# ---------- Main Calculation ----------
try:
    pipe = Pipe(diameter=diameter_mm / 1000.0, length=length_m, roughness=roughness_mm / 1000.0)
    v, re, f, dp = pipe.pressure_drop(q, fluid)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Velocity V", f"{v:.3f} m/s")
    col2.metric("Reynolds number Re", f"{re:,.0f}")
    col3.metric("Friction factor f", f"{f:.5f}")
    col4.metric("Pressure drop ΔP", f"{dp/1000:.2f} kPa")

    # Regime
    if re < 2300:
        regime = "Laminar"
    elif re < 4000:
        regime = "Transitional"
    else:
        regime = "Turbulent"
    st.info(f"**Flow regime:** {regime}  |  Relative roughness ε/D = {pipe.roughness/pipe.diameter:.6f}")

    # ---------- Interactive Plot ----------
    st.subheader("Pressure Drop vs Flow Rate")
    st.markdown("Explore how ΔP changes with flow rate for the current pipe and fluid.")

    q_max_factor = st.slider("Maximum flow rate multiplier (relative to current Q)", 1.0, 10.0, 3.0, 0.5)
    q_max = max(q * q_max_factor, 1e-6)
    qs, dps = pipe.pressure_drop_vs_flowrate(0.0, q_max, fluid, n_points=80)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(qs * 1000, dps / 1000, "b-", linewidth=2, label="ΔP vs Q")
    ax.axvline(q * 1000, color="r", linestyle="--", label=f"Current Q = {q*1000:.2f} L/s")
    ax.axhline(dp / 1000, color="r", linestyle=":", alpha=0.7)
    ax.set_xlabel("Flow rate Q (L/s)")
    ax.set_ylabel("Pressure drop ΔP (kPa)")
    ax.set_title(f"Pressure Drop Characteristic – {fluid.name}")
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    # ---------- Export ----------
    st.subheader("Export Results")
    results = {
        "Fluid": [fluid.name],
        "Density (kg/m3)": [fluid.density],
        "Viscosity (Pa.s)": [fluid.viscosity],
        "Diameter (mm)": [diameter_mm],
        "Length (m)": [length_m],
        "Roughness (mm)": [roughness_mm],
        "Flow rate (m3/s)": [q],
        "Velocity (m/s)": [v],
        "Reynolds number": [re],
        "Friction factor": [f],
        "Pressure drop (Pa)": [dp],
        "Pressure drop (kPa)": [dp / 1000],
        "Flow regime": [regime]
    }
    df = pd.DataFrame(results)

    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download results as CSV",
        data=csv_buffer.getvalue(),
        file_name="pipe_flow_results.csv",
        mime="text/csv"
    )

    with st.expander("Show detailed results table"):
        st.dataframe(df.T, use_container_width=True)

except ValueError as e:
    st.error(f"Input error: {e}")
except Exception as e:
    st.error(f"Unexpected calculation error: {e}")

# ---------- Verification note ----------
with st.expander("Calculation verification notes"):
    st.markdown("""
    **Hand-calculation example (Water, D=50 mm, L=100 m, ε=0.045 mm, Q=0.01 m³/s):**
    - Area = π (0.025)² ≈ 0.0019635 m²
    - V = 0.01 / 0.0019635 ≈ 5.093 m/s
    - Re = 998 × 5.093 × 0.05 / 0.001002 ≈ 253 600 (turbulent)
    - ε/D = 0.0009
    - Haaland: f ≈ 0.02025
    - ΔP = 0.02025 × (100/0.05) × (998 × 5.093² / 2) ≈ 524 000 Pa ≈ **524 kPa**
    Values shown in the metrics above should match within ~1 % (Haaland approximation error).
    """)
