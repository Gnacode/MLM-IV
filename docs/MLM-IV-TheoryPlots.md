---
​---
title: MLM IV Theory Plots
permalink: /MLM-IV/MLM-TheoryPlots/
​---
---

# MLM-IV-THEORYPLOTS

[**INDEX**](index.md)

MLM-IV-Theory Plots, generates the theoretical plot by Merlino 2007, and overlays experimental artifacts as leakage current for ions and electrons, and a capacitive rounding of the "knee". We use the functions (3) and (6) from the Merlino 2007 paper. Merlino RL has made a Maple program doing the same, this here is an easier accessible Python version using Plotly as plotting engine, all based on open-source code and libraries and without any cost of use. 

Our use of the program is as a foundational algorithm used in our instrumentation where we have embedded the code for analysis of plasma generated in our devices.  The program can be used as a standalone program and run from e.g. VSCODE, PYCHARM, Jupyter Notebook or even from command line Python terminals. (see notes under [**Installation**](Installation.md)

The MLM-TheoryPlots generates four sub-plots:

1. Theoretical IV Curve with and simulated (dotted line) capacitive effect on measured current, and a simulated electron leakage current in the voltage bias range above 0 V.

2. Derivative of theoretical IV Curve, and peak finding for estimation of the plasma potential Vp

3. Ion Saturation current, with added overlay of simulated leakage currents (dotted lines)

4. IV curves where the capacitive effect, and leakage currents have been added.

   <a href="images\MLM-IV-TheoryPlot.png" onclick="window.open(this.href, 'popup', 'width=600,height=600'); return false;">Open image</a>

![MLM-IV-TheoryPlot](.\images\MLM-IV-TheoryPlot.png)

We use equation 3 and 6 from Merlino 2007 to generate theoretical plots. The MLM-IV-TheoryPlot is a translations of Merlino RL's Maple program to Python and with added features for showing capacitive artifacts and leakage currents, and compile a realistic experimental data set from the theoretical curves with added capacitance and leakage current. 

**Equation 3 from Merlino 2007**:

![Equation 3 - Merlino 2007](.\images\Merlino2007-Eq3.png)

**Equation 6 from Merlino 2007**:

![Equation 6 - Merlino 2007](.\images\Merlino2007-Eq6.png)