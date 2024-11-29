---
​---
title: Live Share
permalink: /MLM-IV/MLM-IV-EEDF-Analysis/
​---
---

# MLM-IV-EEDF-ANALYSIS

[**INDEX**](index.md)

The EEDF Analysis is based on the Druyvesteyn method as an alternative method to find the electron density **ne**, and the electron temperature **Te**, and it gives a better estimate compared to the methods in MLM-IV-Analysis. This is according to Handout for Plasma Physics: Plasma Probes, Jeremiah Williams, Physics Department, Wittenberg University, 2014. 

The EEDF can then be found from the second derivative of the electron current with respect to the
probe voltage using the Druyvesteyn method. Aprobe is the area of the probe, qe is the electron charge, me is the electron mass,  is the
electron energy ( = qe (Vp - Vprobe), Vprobe is the probe voltage and Ie is the electron current. 

![Handsouts Equation2](.\images\handsout-eq2-a.png)

The extracted EEDF, fe(ε) is seen below

![MLM-IV-Analysis output plot](.\images\MLM-IV-EEDF-Analysis.png)

The electron density and effective electron temperature can then be found by taking moments of the distribution function.

![Handsouts Equation2](.\images\handsout-eq3.png)

![Handsouts Equation2](.\images\handsout-eq4.png)
