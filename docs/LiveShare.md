---
​---
title: Live Share
permalink: /MLM-IV/LiveShare/
​---
---

# LIVESHARE WITH  VSCODE AND GITHUB CODESPACES

## Pair Programming - Interactive Collaboration for Code Development

[**INDEX**](index.md)


Liveshare is an extension for VSCODE which can be activated in Github CODESPACES.

Codespaces are dedicated servers you can setup on your Github account on which you can try the software. It requires you have a /devcontainer/devcontainer.json file on your repository, which we have:

Devcontainer.json

```markdown
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/python
{
  "name": "Python 3",
  "image": "mcr.microsoft.com/devcontainers/python:0-3.11-bullseye",
  "features": {
    "ghcr.io/devcontainers-contrib/features/coverage-py:2": {}
  },
  "postCreateCommand": "pip3 install --user -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "streetsidesoftware.code-spell-checker"
      ]
    }
  }
}
```

with this in place you can create a CODESPACE from the repository

![MLM-IV-Analysis output plot](.\images\codespace-overview.png)



![MLM-IV-Analysis output plot](.\images\open-in-browser.png)

![MLM-IV-Analysis output plot](.\images\vscode-in-browser.png)

![MLM-IV-Analysis output plot](.\images\liveshare-starting.png)

Here you get the liveshare code, which looks like this, that you can send to your :



```
https://prod.liveshare.vsengsaas.visualstudio.com/join?692D41437EFED3E19A32DAA24E37E6C35729
```

On the remote machine the user should start the VSCODE with the LIVESHARE extension installed, and then click **liveshare** marked with red at the bottom of the screen. 

![MLM-IV-Analysis output plot](.\images\start-collaboration-session.png)



![MLM-IV-Analysis output plot](.\images\liveshare-following.png)

(tutorial for LIVESHARE WITH VSCODE AND CODESPACES WILL BE ADDED HERE)