---
layout: post
authors: ["devcrypted"]
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: Windows 11 Setup - Clean & Minimal
permalink: desktop-setup
media_subpath: /assets/img
date: 2024-12-22 00:00 +0530
categories: ["Windows 11", "Desktop Setup", "WSL", "Cloud Engineering"]
tags: ["Windows 11", "Desktop Setup", "WSL"]
image: headers/desktop-setup.png
description: This blog will help you to configure your Windows 11 and WSL without having to manually do a lot of things. We have scripts for setting Windows 11 and WSL. Please follow the document.
video_id: randomVideoID
playlist_id: PL2JBbPWIA_Tq6oI8hAkJVR6Uhg5wLx9AM
github_repo: dotfiles
---

### **RESOURCES**

- [GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

{% include embed/youtube.html id=page.video_id %}

---

<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD013 -->

# **GETTING STARTED**

🧪 This is tested in Windows 10, 11, Ubuntu 20.04 and higher versions 🙌

## **1️⃣ INSTALL PREREQUISITES**

1. Install Windows updates
2. Install optional updates
3. [Install Powershell](ms-windows-store://pdp?hl=en-us&gl=in&ocid=pdpshare&referrer=storeforweb&productid=9mz1snwt0n5d&storecid=storeweb-pdp-open-cta&webid=08f4c27d-35ff-4c66-929a-5d34436bc137&websessionid=168a7aac-ba5c-4d8f-a3e1-7ef308adc84e) from Microsoft Store.

## **2️⃣ CONFIGURE WINDOWS 10/11**

🧑‍💻 _Step A & B will be installing everything for you needed in Windows. Just follow below 2 commands!_

### **🅰️ INSTALL WINDOWS APPS**

Launch Powershell Core as Administrator and run the below command:

```powershell
. { iwr -useb 'decr.in/pswinget' } | iex;
```

To see which applications are being installed, visit the [decr.in/pswinget](https://decr.in/pswinget) script.
If you want to install more apps, you can go to [winget.run](https://winget.run) and copy the command to install the application you want to install.

### **🅱️ INSTALL WINDOWS SUBSYSTEM FOR LINUX (WSL)**

Launch Windows Powershell as Administrator and run the below command:

```powershell
. { iwr -useb 'decr.in/pswsl' } | iex;
```

## **3️⃣ INSTALL AND CONFIGURE UBUNTU WSL**

1. Go to [My dotfiles repo](https://github.com/devcrypted/dotfiles.git) and fork it.
2. Change reference to my repo in below command with yours. Run the below commands:

```bash
sudo apt update && sudo apt upgrade -y && sudo apt install git -y
git clone https://github.com/devcrypted/dotfiles.git "$HOME/dotfiles"
cd "$HOME/dotfiles"
chmod +x installer.sh && /bin/bash installer.sh
```

## **CORE FEATURES THIS SETUP IS BRINGING**

- Preconfigured aliases for many commands like:
  - `ks` for `kubectl get pods`
  - `kl` for `kubectl get pods -o wide`
  - `ka` for `kubectl get pods --all-namespaces -o wide`
  - `p` for `poetry`
  - `v` for `nvim`
  - Read [.zshrc](https://github.com/devcrypted/dotfiles/blob/main/.zshrc) for more shortcuts.
- Auto completion for many of tools like `git`, `ansible`, `asdf`, `aws`, `azure`, `bun`, `cp`, `dnf`, `docker`, `docker-compose`, `gh`, `git`, `golang`, `helm`, `httpie`, `istioctl`, `kind`, `kubectl`, `kubectx`, `minikube`, `mongocli`, `npm`, `nvm`, `pep8`, `pip`, `pipenv`, `poetry`, `pyenv`, `ssh`, `tmux`, `ufw`, `vagrant`, `virtualenv`, `vscode`, and `yarn`.
- Manage test Kubernetes cluster by running `create-cluster`, `delete-cluster`, and `reset-cluster` command. Isn't it cool 🙌?
- Oh-my-zsh preinstalled.
- Windows 25 core developer and DevOps tools preinstalled.
- Linux 50+ core developer and DevOps tools preinstalled with Ansible. Checkout my [Ansible playbook file](https://github.com/devcrypted/dotfiles/blob/main/ansible/playbook.yaml).
- Stow preconfigured for managing your dotfiles using symlinks.
