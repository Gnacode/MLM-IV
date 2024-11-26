# MLM-IV-ANALYSIS

MLM-IV-Theory Plots, generates the theoretical plot by Merlino 2007, and overlays experimental artifacts as leakage current for ions and electrons, and a capacitive rounding of the "knee". We use the functions (3) and (6) from the Merlino 2007 paper. Merlino RL has made a Maple program doing the same, this here is an easier accessible Python version using Plotly as plotting engine, all based on open-source code and libraries and without any cost of use. 

Our use of the program is as a foundational algorithm used in our instrumentation where we have embedded the code for analysis of plasma generated in our devices.  The program can be used as a standalone program and run from e.g. VSCODE, PYCHARM, Jupyter Notebook or even from command line Python terminals. (see notes under [**Installation**](Installation.md)

Output plot by [**MLM-IV-ANALYSIS**](MLM-IV-Analysis.md) : Langmuir Probe Analysis with Fits and Intersections

![MLM-IV-Analysis output plot](.\images\MLM-IV-Analysis.png)

The programs outputs four plots using Plotly (for [**CODESPACE**](https://github.com/features/codespaces) use for pair programming [**Plotly**](https://plotly.com/) does not work that well and we therefore also provide a version using [**Dash by Plotly**](https://dash.plotly.com/) which is confirmed working with [**LiveShare using VSCODE and GITHUB CODESPACE**](Liveshare.md))

