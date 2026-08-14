"""
Multi-page Streamlit Engineering Calculator App
Home / Landing page.
"""

import streamlit as st

st.set_page_config(
    page_title="Engineering Calculators",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚙️ Engineering Analysis Suite")
st.markdown("""
Welcome to a multi-module engineering calculator built with **Streamlit**.

### Available Modules
| Module | Description |
|--------|-------------|
| **A – Pipe Flow Analyser** | Complete Darcy-Weisbach calculator with fluid selection, friction factor, pressure drop, interactive plots and CSV export. |
| **B – Heat Transfer Calculator** | Steady conduction (Fourier) + Newton's Law of Cooling with real-time temperature history plot. |
| **C – Rock & Fluid Data Dashboard** | Upload CSV, summary stats, filtering, histograms, cross-plots and download filtered data. |

Use the **sidebar** to navigate between pages.

---
**Code Quality Features**
- Object-oriented design (`Fluid`, `Pipe`, `HeatTransfer` classes in `engineering.py`)
- Full docstrings on all public methods
- Input validation and graceful error handling
- Ready for deployment on Streamlit Community Cloud
""")

st.info("Select a page from the sidebar to begin.")

st.sidebar.success("Select a module above.")
st.sidebar.markdown("---")
st.sidebar.caption("Built for engineering education & analysis")
