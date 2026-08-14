# Engineering Analysis Suite – Multi-page Streamlit App

A professional multi-module engineering calculator built with Streamlit, featuring:

- **Module A – Pipe Flow Analyser**: Complete Darcy-Weisbach calculator with fluid selection, friction factor (Haaland), pressure drop, interactive ΔP–Q plot and CSV export.
- **Module B – Heat Transfer Calculator**: Steady conduction (Fourier’s law) + Newton’s Law of Cooling with real-time interactive temperature history.
- **Module C – Rock & Fluid Data Dashboard**: CSV upload, summary statistics, interactive filtering, histogram + cross-plot, filtered CSV download.

## Live Demo

**Streamlit Community Cloud URL:**  
👉 *https://your-username-your-repo-name.streamlit.app*  
*(Replace with the actual URL after deployment)*

## Features & Code Quality

- **Object-oriented design**: `Fluid`, `Pipe` and `HeatTransfer` classes live in a separate `engineering.py` module.
- All public methods have clear docstrings.
- Input validation and graceful error handling prevent crashes.
- Professional UI: sidebar inputs, metric cards, interactive plots, expanders for verification notes.
- Ready for Streamlit Community Cloud deployment.

## Project Structure

```
pipe_flow_app/
├── streamlit_app.py          # Home / landing page
├── engineering.py            # OOP classes (Fluid, Pipe, HeatTransfer)
├── pages/
│   ├── 1_Pipe_Flow_Analyser.py
│   ├── 2_Heat_Transfer_Calculator.py
│   └── 3_Rock_Fluid_Dashboard.py
├── requirements.txt
├── README.md
└── AI_USAGE.md               # Documentation of AI assistance
```

## Local Installation & Run

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deployment on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select the repository.
4. Main file path: `streamlit_app.py`
5. Click **Deploy**.

## Calculation Verification

### Pipe Flow (Module A)
Hand-calculated example (Water @ 20 °C, D = 50 mm, L = 100 m, ε = 0.045 mm, Q = 0.01 m³/s):
- V ≈ 5.093 m/s
- Re ≈ 253 600 (turbulent)
- f (Haaland) ≈ 0.0203
- ΔP ≈ 524 kPa

### Newton’s Cooling (Module B)
Aluminium block example (m = 0.5 kg, cp = 900 J/kg·K, A = 0.05 m², h = 10 W/m²·K, T0 = 90 °C → 40 °C, T∞ = 25 °C):
- τ = 900 s
- t ≈ 1319 s ≈ 22.0 min

## AI Usage Documentation

See [AI_USAGE.md](AI_USAGE.md) for the list of prompts used, what was verified, and what was corrected.

## License

Educational / open use. Feel free to fork and extend.
