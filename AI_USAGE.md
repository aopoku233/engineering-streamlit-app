# AI Usage Documentation

This project was developed with assistance from AI (Grok / xAI), but **every line of code was understood, verified, and documented by the developer**. Below are three representative prompts, what the AI produced, what was verified, and what was corrected.

---

### Prompt 1
> “Write a Python class for a circular pipe that calculates Reynolds number, Darcy friction factor using Haaland approximation, and pressure drop with the Darcy-Weisbach equation. Include proper error handling and docstrings.”

**What AI produced:**  
A solid `Pipe` class skeleton with Haaland formula, Reynolds calculation and ΔP formula.

**What was verified:**  
- Haaland equation coefficients checked against literature (Wikipedia / engineering handbooks).  
- Hand calculation for water example (D=50 mm, Q=0.01 m³/s) confirmed ΔP ≈ 52 kPa.  
- Laminar branch (f = 64/Re) added and tested.

**What was corrected:**  
- Added explicit unit conversion guidance and relative-roughness calculation.  
- Improved error messages and edge-case handling for Re ≤ 0 and negative geometry.  
- Separated velocity calculation into its own method for clarity.

---

### Prompt 2
> “Create a Streamlit page for Newton’s Law of Cooling that shows the analytical time-to-target formula and an interactive temperature-vs-time plot that updates with sliders for h and time horizon.”

**What AI produced:**  
Working page with input widgets, time calculation and matplotlib plot.

**What was verified:**  
- Analytical solution T(t) = T∞ + (T0−T∞)exp(−t/τ) matches textbook derivation.  
- Example (aluminium block) reproduces the expected 22 min cooling time exactly.  
- Plot updates correctly when h slider is moved.

**What was corrected:**  
- Added physical descriptions and unit guidance next to every input (required by the brief).  
- Implemented proper reachability check (target must lie between T0 and T∞).  
- Improved layout with columns and success/error messaging.

---

### Prompt 3
> “Build a Streamlit dashboard that accepts a user-uploaded CSV of rock properties, shows describe() statistics, allows range filtering on numeric columns, draws a porosity histogram and a porosity–permeability scatter plot, and offers a download button for the filtered data.”

**What AI produced:**  
Functional upload → filter → chart → download pipeline.

**What was verified:**  
- Pandas `describe()` and filtering logic work on both uploaded and synthetic data.  
- Histogram and log-scale cross-plot render correctly.  
- CSV download produces a valid file that can be re-opened.

**What was corrected:**  
- Added a high-quality synthetic dataset generator (with realistic porosity–permeability correlation) so the page is usable without an external file.  
- Smart column detection (prefers columns containing “Porosity” / “Permeability”).  
- Better handling of empty filtered results and non-numeric columns.

---

**Summary of AI contribution**  
AI accelerated boilerplate generation and suggested good starting structures. All numerical methods, physical formulas, error handling, UI polish, verification examples and documentation were reviewed, tested and refined by the developer. No generated code was accepted blindly.
