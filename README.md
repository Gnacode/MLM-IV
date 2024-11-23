# GNACODE's MLM-IV Simulation and Analysis

We develop software for our microcontrollers for our instruments, and we develop tools for data analysis that is based on output from our devices, lab environment, and calibration systems. Some of these tools can be used as standalone programs, and we publish them here.

Hereto, we also publish our most interesting application in scientific journals and host the public repositories for those publications here as well




## Authors

- [@ltatgnacode](https://www.github.com/ltatgnacode)


MLM-IV-Theory Plots, generates the theoretial plot by Merlino 2007, and overlays experimental artifacts as leakage current for ions and electrons, and a capacitive rounding of the "knee". We use the functions (3) and (6) from the Merlino 2007 paper. Merlino RL has made a Maple program doing the same, this here is an easier accessible Python version using Plotly as plotting engine. 
![Logo](https://github.com/Gnacode/MLM-IV/blob/main/MLM-IV-TheoreticPlot.png?raw=true)

MLM-IV-SimPlot, generates a range of IV curves with different eV energies, based on the theoretical plot from MLM-IV-Theory Plots but incorporates the leakage currents for ions and electrons and adds the rounding of the "knee". The function is run a number of times with and sampled with gaussian noise from scipy. It outputs the different plots as files in the NPY plot format and they can be read by e.g. PlasmaPy. The plasma settings at the top of the Python file makes it easier to specify all relevant parameters for a Plasma like:
- electron concentration [ne], 
- ion concentration [ni], 
- electron temperature[Te], 
- ion temperature [Ti], 
- floating potential [Vf], 
- plasma potential [Vp] 
![Logo](https://github.com/Gnacode/MLM-IV/blob/95e54ab69f6cecf8586d679afa888b0414df2c8b/MLM-IV-Simplot.png?raw=true)

MLM-IV-Analysis, uses a straight forward IV curve analysis outlined in Handout for Plasma Physics: Plasma Probes, by Jeremiah Willams, Physics Department, Wittenberg University, 2014. We found that this fitting method gives better results than [PlasmaPy](https://github.com/PlasmaPy/PlasmaPy), which is easy to try because [PlasmaPy](https://github.com/PlasmaPy/PlasmaPy) can read the NPY files generated by MLV-IV-SimPlot 
![Logo](https://github.com/Gnacode/MLM-IV/blob/main/MLM-IV-Analysis.png?raw=true)
- Final Estimated Electron Temperature (Te) = 1.91 eV
- Final Estimated Plasma Potential (Vp) = 4.62 V (from derivative peak)
- Final Estimated Plasma Potential (Vp) = 5.45 V (from line crossing)
- Final Estimated Electron Saturation Current (Ie_sat) = 2.32e-03 A


MLM-IV-EEDF-Analysis, is a second method to fit for electron density [ne], and electron temperature [Te]. We found that an average of [Te]  we found in MLM-IV-Analysis and MLM-IV-EEDF-Analysis fits with the orignal [Te] provided for the simulation 
![Logo](https://github.com/Gnacode/MLM-IV/blob/main/MLM-IV-EEDF-Analysis.png?raw=true)
- Electron Density (n_e) [Simpson]: 1.0497957915644494e+16
- Electron Density (n_e) [Trapz]: 1.0497953882833564e+16
- Electron Temperature (T_e) [Simpson]: 2.2881789687780754 eV
- Electron Temperature (T_e) [Trapz]: 2.288175827279369 eV
- Electron Temperature (T_e) [Simpson]: 26542.876037825674 K
- Electron Temperature (T_e) [Trapz]: 26542.839596440677 K
---------------
Here we can see that (2.28 eV + 1.91 eV)/2 = 2.1 eV, where the original value set for the simulation was 2.0 eV
-------------



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)



## Feedback

If you have any feedback, please reach out to us at support@gnacode.com


## References

 - [American Journal of Physics, Vol 75, issue 12, pages 1078-1085](https://pubs.aip.org/aapt/ajp/article-abstract/75/12/1078/899100/Understanding-Langmuir-probe-current-voltage?redirectedFrom=fulltext)
 - Author: Merlino, Robert L.
 - Abstract:
  - I give several simple examples of model Langmuir probe current-voltage (I-V) characteristics that help students learn how to interpret real I-V characteristics obtained in a plasma. Students can also create their own Langmuir probe I-V characteristics using a program with the plasma density, plasma potential, electron temperature, ion temperature, and probe area as input parameters. Some examples of Langmuir probe I-V characteristics obtained in laboratory plasmas are presented and analyzed. A few comments are made advocating the inclusion of plasma experiments in the advanced undergraduate laboratory.

- [American Association of Physics Teachers, Handout for Plasma Physics: Plasma Probes, by Jermiah Williams, Wittenberg University 2014](https://advlabs.aapt.org/images/files/LangmuirProbe_handout_2014.pdf)


