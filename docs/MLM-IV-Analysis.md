---
​---
title: Live Share
permalink: /MLM-IV/MLM-IV-Analysis/
​---
---

# MLM-IV-ANALYSIS

[**INDEX**](index.md)

MLM-IV-Analysis, loads a NPY data file from MLM-IV-SimPlot and performs following plots, fits, and analysis:

The analysis provides four sub-plots:

1. IV Curve
2. Derivative of IV Curve, and peak finding for estimation of the plasma potential $V_{p}$
3. Ion Saturation Fit, where we fit a linear curve to the ion saturation current
4. Subtraction of the Ion Saturation Current from the IV curve, and plotting the resulting data transformed by Ln(y), and fit the electron retardation zone and the electron saturation zone. The slope of the electron retardation zone gives the electron temperature $T_{e}$, in eV, the crossing point between the two fits is the plasma potential  $V_{p}$ which in most cases is a better estimated value compared to the value achieved by the peak of the derivative of the IV curve.



Output plot by [**MLM-IV-ANALYSIS**](MLM-IV-Analysis.md) : Langmuir Probe Analysis with Fits and Intersections

![MLM-IV-Analysis output plot](.\images\MLM-IV-Analysis.png)

The programs outputs four plots using Plotly (for [**CODESPACE**](https://github.com/features/codespaces) use for pair programming [**Plotly**](https://plotly.com/) does not work that well and we therefore also provide a version using [**Dash by Plotly**](https://dash.plotly.com/) which is confirmed working with [**LiveShare using VSCODE and GITHUB CODESPACE**](Liveshare.md))

4. 









