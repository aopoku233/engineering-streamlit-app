"""
Module C: Rock & Fluid Data Dashboard
Upload CSV, summary statistics, filtering, charts, download filtered data.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Rock & Fluid Data Dashboard", page_icon="🪨", layout="wide")

st.title("🪨 Module C – Rock & Fluid Data Dashboard")
st.markdown("""
Upload a CSV file containing rock or fluid sample data.  
Typical columns: `SampleID`, `Porosity`, `Permeability`, `Density`, `Lithology`, etc.

The app will:
- Show summary statistics
- Allow interactive filtering (e.g. porosity > X %)
- Display a porosity histogram and a porosity–permeability cross-plot
- Let you download the filtered dataset
""")

# ---------- Sample data generator (for first-time users) ----------
@st.cache_data
def generate_sample_data(n: int = 120) -> pd.DataFrame:
    """Generate a realistic synthetic rock-property dataset."""
    rng = np.random.default_rng(42)
    porosity = rng.normal(15, 5, n).clip(2, 35)  # %
    # Simple porosity-permeability relationship with noise (log-perm ~ a + b*phi)
    log_perm = -1.5 + 0.25 * porosity + rng.normal(0, 0.6, n)
    permeability = 10 ** log_perm  # mD
    density = 2.7 - 0.015 * porosity + rng.normal(0, 0.05, n)  # g/cm³
    lithologies = rng.choice(["Sandstone", "Limestone", "Shale", "Dolomite"], n, p=[0.4, 0.25, 0.2, 0.15])
    df = pd.DataFrame({
        "SampleID": [f"S-{i:03d}" for i in range(1, n+1)],
        "Porosity_%": np.round(porosity, 2),
        "Permeability_mD": np.round(permeability, 3),
        "Density_g_cm3": np.round(density, 3),
        "Lithology": lithologies
    })
    return df

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded **{len(df)}** rows × **{len(df.columns)}** columns")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()
else:
    st.info("No file uploaded – using built-in synthetic rock dataset for demonstration.")
    df = generate_sample_data()
    st.download_button(
        "Download sample dataset as CSV",
        data=df.to_csv(index=False),
        file_name="sample_rock_data.csv",
        mime="text/csv"
    )

# ---------- Display raw data ----------
with st.expander("Preview data (first 20 rows)", expanded=False):
    st.dataframe(df.head(20), use_container_width=True)

# ---------- Summary statistics ----------
st.subheader("Summary Statistics")
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if numeric_cols:
    st.dataframe(df[numeric_cols].describe().T.style.format("{:.3f}"), use_container_width=True)
else:
    st.warning("No numeric columns found for statistics.")

# ---------- Filtering ----------
st.subheader("Filter Data")
st.markdown("Apply simple numeric filters. Only rows satisfying **all** active filters are kept.")

filtered_df = df.copy()
filter_cols = st.multiselect(
    "Select numeric columns to filter on",
    options=numeric_cols,
    default=[c for c in ["Porosity_%", "Permeability_mD"] if c in numeric_cols][:1]
)

for col in filter_cols:
    col_min = float(df[col].min())
    col_max = float(df[col].max())
    # Sensible defaults
    if "porosity" in col.lower():
        default_low = max(col_min, 10.0)
    else:
        default_low = col_min
    low, high = st.slider(
        f"{col} range",
        min_value=col_min,
        max_value=col_max,
        value=(default_low, col_max),
        key=f"slider_{col}"
    )
    filtered_df = filtered_df[(filtered_df[col] >= low) & (filtered_df[col] <= high)]

st.markdown(f"**Filtered rows:** {len(filtered_df)} / {len(df)}")

# ---------- Charts ----------
st.subheader("Visualisations")

if len(filtered_df) == 0:
    st.warning("No data left after filtering – adjust the filters.")
else:
    col_left, col_right = st.columns(2)

    # Histogram of porosity (or first numeric column)
    with col_left:
        hist_col = "Porosity_%" if "Porosity_%" in filtered_df.columns else numeric_cols[0]
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.hist(filtered_df[hist_col].dropna(), bins=15, color="steelblue", edgecolor="white", alpha=0.85)
        ax1.set_xlabel(hist_col)
        ax1.set_ylabel("Count")
        ax1.set_title(f"Histogram of {hist_col}")
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)
        plt.close(fig1)

    # Cross-plot porosity vs permeability (or two numeric columns)
    with col_right:
        x_col = "Porosity_%" if "Porosity_%" in filtered_df.columns else numeric_cols[0]
        y_candidates = [c for c in numeric_cols if c != x_col]
        y_col = "Permeability_mD" if "Permeability_mD" in filtered_df.columns else (y_candidates[0] if y_candidates else x_col)

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        if y_col != x_col:
            # Log scale for permeability often useful
            use_log = "perm" in y_col.lower()
            ax2.scatter(filtered_df[x_col], filtered_df[y_col], alpha=0.7, c="darkorange", edgecolors="k", s=40)
            ax2.set_xlabel(x_col)
            ax2.set_ylabel(y_col)
            if use_log:
                ax2.set_yscale("log")
            ax2.set_title(f"{y_col} vs {x_col}")
            ax2.grid(True, alpha=0.3)
        else:
            ax2.text(0.5, 0.5, "Need at least two numeric columns", ha="center", va="center")
        st.pyplot(fig2)
        plt.close(fig2)

# ---------- Download filtered data ----------
st.subheader("Download Filtered Data")
if len(filtered_df) > 0:
    csv_buffer = io.StringIO()
    filtered_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Download filtered CSV",
        data=csv_buffer.getvalue(),
        file_name="filtered_rock_fluid_data.csv",
        mime="text/csv"
    )
else:
    st.button("Download filtered CSV", disabled=True)

st.caption("Tip: Column names containing 'Porosity' or 'Permeability' are automatically preferred for the charts.")
