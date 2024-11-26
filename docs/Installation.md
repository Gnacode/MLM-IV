---
​---
title: Installation Guide
permalink: /MLM-IV/Installation/
​---
---

# Download and Installation Guide for the MLM-IV programs

[**INDEX**](index.md)

Code repository on Github: https://github.com/Gnacode/MLM-IV

Installation guide if you are using VSCODE

1. [**DOWNLOAD VSCODE AND INSTALL IT**](https://code.visualstudio.com/)
2. [DOWNLOAD PHYTON AND INSTALL IT](https://www.python.org/downloads/)
3. [**DOWNLOAD GIT AND INSTALL IT**](https://git-scm.com/downloads)
4. Reboot your computer
5. Create a directory where you want to have the code
6. Open a terminal window in that directory and run 

```
git clone https://github.com/Gnacode/MLM-IV.git
```

7.  Open VSCODE and click on the directory icon

![VSCODE](.\images\aVSCODE1.png)

8.  Click on the "Open Folder" button

![VSCODE](.\images\bVSCODE2.png)

9. when you open the folder where you cloned the repository it shold look like below

![VSCODE](.\images\cVSCODE3.png)

10. Install extensions for python

![VSCODE](.\images\dVSCODE4.png)

10.  Below is a list of useful extensions

```
bierner.github-markdown-preview
bierner.markdown-preview-github-styles
bierner.markdown-yaml-preamble
donjayamanne.githistory
eamodio.gitlens
github.codespaces
github.copilot
github.copilot-chat
github.remotehub
github.vscode-github-actions
github.vscode-pull-request-github
letmaik.git-tree-compare
mhutchie.git-graph
ms-python.debugpy
ms-python.python
ms-python.vscode-pylance
ms-vscode.powershell
ms-vsliveshare.vsliveshare
redhat.vscode-yaml
```

12. Open one of the Python scripts, and chose which python.exe to use and create an environment (.venv) and chose to install them from the requirements.txt file.

    1. This is done by first pressing keys CTRL+SHIFT+P which brings up the window where you type ">Python: Create" and which finds the option menu "Python: Create Environment", chose that and 
    2. when it asks if you want to use the "Requirements.txt" chose that. 
    3. chose the default Python interpreter
    4. Now your environment is created

    

    ![VSCODE](.\images\eVSCODE5.png)

    

    

    13. when this is done you should see **"Python 3.11.5  ('.venv':venv)"** in your bottom right side of the VSCODE interface as marked by red below. You can now run the MLM-IV-Programs.

        

![VSCODE](.\images\fVSCODE6.png)

14. You run a script by loading it by clicking on it in the explorer window, and then click on ► buttton marked below by the red circle. The program will load the output in a browser window so watch out for that, and the calculations will be output in the terminal window.

![VSCODE](.\images\gVSCODE7.png)





**Notes**: The MLM-IV-SimPlot generates data files that you have to copy manually into the MLM-IV-Analysis and MLM-IV-EEDF-Analysis programs. 

Please be aware of the path syntax, see below:

```
data = np.load('LMSIMData\\20241126-001559-LangmuirSIM_eV2_averaged_noisy.npy')
```

Notice the double \\\ which are required for the file to be read from the data directory correctly.

