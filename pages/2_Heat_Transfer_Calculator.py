"""
Module B: Heat Transfer Calculator
1. Steady conduction through a flat wall (Fourier's law)
2. Newton's Law of Cooling – time to reach target temperature + interactive curve
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from engineering import HeatTransfer

st.set_page_config(page_title="Heat Transfer Calculator", page_icon="🔥", layout="wide")

st.title("🔥 Module B – Heat Transfer Calculator")
st.markdown("""
Two classical heat-transfer problems:

1. **Steady-state conduction** through a single-layer flat wall (Fourier’s law).
2. **Transient cooling / heating** of a lumped body following **Newton’s Law of Cooling**.
""")

tab1, tab2 = st.tabs(["🧱 Steady Conduction (Flat Wall)", "❄️ Newton’s Law of Cooling"])

# ==================== TAB 1: Conduction ====================
with tab1:
    st.header("Steady 1-D Conduction through a Flat Wall")
    st.markdown("""
    **Fourier’s law** for a plane wall:
    
    $$ Q = k \\, A \\, \\frac{T_{\\text{hot}} - T_{\\text{cold}}}{L} $$
    
    where  
    - \( k \) = thermal conductivity of the wall material (W/(m·K))  
    - \( A \) = area perpendicular to the heat flow (m²)  
    - \( L \) = wall thickness (m)  
    - \( T_{\\text{hot}}, T_{\\text{cold}} \) = surface temperatures (°C or K – difference is what matters)
    """)

    col_a, col_b = st.columns(2)
    with col_a:
        k = st.number_input(
            "Thermal conductivity k (W/(m·K))",
            min_value=0.01, value=15.0, step=0.1,
            help="Typical: concrete ~1.4, steel ~15–50, copper ~400, insulation ~0.04"
        )
        thickness = st.number_input(
            "Wall thickness L (m)",
            min_value=0.001, value=0.1, step=0.01,
            help="Distance between the two surfaces"
        )
    with col_b:
        area = st.number_input(
            "Cross-sectional area A (m²)",
            min_value=0.01, value=1.0, step=0.1,
            help="Area normal to the direction of heat flow"
        )
        t_hot = st.number_input("Hot-side temperature (°C)", value=80.0, step=1.0)
        t_cold = st.number_input("Cold-side temperature (°C)", value=20.0, step=1.0)

    try:
        q = HeatTransfer.conduction_flat_wall(k, area, thickness, t_hot, t_cold)
        st.success(f"**Heat transfer rate Q = {q:,.1f} W**  ({q/1000:.3f} kW)")
        st.metric("Heat flux q″ = Q/A", f"{q/area:,.1f} W/m²")
    except ValueError as e:
        st.error(str(e))

# ==================== TAB 2: Newton's Cooling ====================
with tab2:
    st.header("Newton’s Law of Cooling / Heating")
    st.markdown("""
    For a body with high thermal conductivity (lumped-capacitance approximation) the temperature evolves as:
    
    $$ T(t) = T_{\\infty} + (T_0 - T_{\\infty})\\, e^{-t/\\tau} $$
    
    where the time constant \(\\tau = \\dfrac{m\\, c_p}{h\\, A}\).
    
    Solving for the time to reach a target temperature \( T_{\\text{target}} \):
    
    $$ t = \\tau \\, \\ln\\left(\\frac{T_0 - T_{\\infty}}{T_{\\text{target}} - T_{\\infty}}\\right) $$
    """)

    st.subheader("Physical Inputs (all clearly described)")
    c1, c2, c3 = st.columns(3)
    with c1:
        t0 = st.number_input(
            "Initial temperature T₀ (°C)",
            value=90.0, step=1.0,
            help="Temperature of the object at time t = 0"
        )
        t_target = st.number_input(
            "Target temperature T_target (°C)",
            value=40.0, step=1.0,
            help="Temperature you want the object to reach"
        )
        t_inf = st.number_input(
            "Ambient temperature T∞ (°C)",
            value=25.0, step=1.0,
            help="Temperature of the surrounding fluid (air, water, …)"
        )
    with c2:
        h = st.number_input(
            "Heat transfer coefficient h (W/(m²·K))",
            min_value=0.1, value=10.0, step=0.5,
            help="Convection coefficient. Free air ~5–25, forced air ~20–200, water ~100–1000+"
        )
        area = st.number_input(
            "Surface area A (m²)",
            min_value=0.001, value=0.05, step=0.01,
            help="Area of the object exposed to the ambient fluid"
        )
    with c3:
        mass = st.number_input(
            "Mass of object m (kg)",
            min_value=0.001, value=0.5, step=0.1,
            help="Mass of the solid body being cooled/heated"
        )
        cp = st.number_input(
            "Specific heat capacity cp (J/(kg·K))",
            min_value=100.0, value=900.0, step=10.0,
            help="Typical: aluminium ~900, steel ~500, water ~4180, plastics ~1000–2000"
        )

    # Sliders for interactive exploration
    st.subheader("Interactive Controls (real-time plot update)")
    h_slider = st.slider("Adjust h (W/(m²·K))", 1.0, 200.0, float(h), 1.0)
    t_max_min = st.slider("Plot time horizon (minutes)", 1.0, 120.0, 30.0, 1.0)

    try:
        # Time to target
        t_sec = HeatTransfer.newtons_cooling_time(
            t0, t_target, t_inf, h_slider, area, mass, cp
        )
        t_min = t_sec / 60.0
        st.success(f"**Time to reach {t_target:.1f} °C = {t_sec:,.1f} s  ({t_min:.2f} minutes)**")

        # Temperature history
        t_max = t_max_min * 60.0
        times, temps = HeatTransfer.temperature_history(
            t0, t_inf, h_slider, area, mass, cp, t_max, n_points=300
        )

        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.plot(times / 60, temps, "b-", linewidth=2, label="T(t)")
        ax.axhline(t_inf, color="g", linestyle="--", label=f"T∞ = {t_inf} °C")
        ax.axhline(t_target, color="r", linestyle=":", label=f"Target = {t_target} °C")
        if 0 < t_min < t_max_min:
            ax.axvline(t_min, color="orange", linestyle="-.", label=f"t_target = {t_min:.1f} min")
        ax.set_xlabel("Time (minutes)")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Temperature Evolution – Newton’s Law of Cooling")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best")
        st.pyplot(fig)
        plt.close(fig)

        # Show time constant
        tau = (mass * cp) / (h_slider * area)
        st.caption(f"Time constant τ = m·cp / (h·A) = {tau:.1f} s ({tau/60:.2f} min)")

    except ValueError as e:
        st.error(str(e))
        st.info("Make sure the target temperature lies strictly between the initial temperature and the ambient temperature.")

with st.expander("Verification against analytical solution"):
    st.markdown("""
    **Example:** Aluminium block, m = 0.5 kg, cp = 900 J/(kg·K), A = 0.05 m²,  
    h = 10 W/(m²·K), T0 = 90 °C, T∞ = 25 °C, target = 40 °C.
    
    τ = 0.5 × 900 / (10 × 0.05) = 900 s  
    t = 900 × ln( (90-25)/(40-25) ) = 900 × ln(4.333) ≈ 900 × 1.466 = **1319 s ≈ 22.0 min**
    
    The app result should match this value exactly (within floating-point precision).
    """)
