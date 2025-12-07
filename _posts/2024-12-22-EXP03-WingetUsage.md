---
layout: post
authors: ["devcrypted"]
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: "Unlock the Power of Winget: Master Windows Package Management"
permalink: everything-about-winget
media_subpath: /assets/img
date: 2025-01-23 00:00 +0530
categories: ["Desktop Configuration"]
tags: ["Windows 11", "Desktop Setup", "Winget"]
image: https://img.youtube.com/vi/CvcNiSRMSjk/maxresdefault.jpg
description: Welcome to our deep dive into Winget, the command-line package manager for Windows. Whether you're setting up a new machine, managing software updates, or simply curious about streamlining your digital environment, this video is for you!
video_id: CvcNiSRMSjk
playlist_id: PL2JBbPWIA_Tq_TNk0JGsnH_ate3QSIYoV
github_repo: ""
---

### **RESOURCES**

- [Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})
- [Download Winget](https://aka.ms/getwinget)
- [Winget Documentation](https://learn.microsoft.com/en-us/windows/package-manager/)
- [Winget.run](https://winget.run) for app search and commands

---

{% include embed/youtube.html id=page.video_id %}

---

<!-- markdownlint-disable MD025 -->
<!-- markdownlint-disable MD013 -->

# What is Winget?

Winget is a command-line tool for managing applications on Windows. Think of it as the Windows equivalent of Linux's APT or macOS's Homebrew. You can:

- **Install apps** in seconds.
- **Search for apps** without opening a browser.
- **Update, remove, and manage apps** with a few commands.
- **Share your setup** with others using JSON files.

---

# Installing Winget

## Pre-installed on Windows 11

1. Open the **Microsoft Store**.
2. Go to the **Library** section.
3. Click **Get updates** to ensure "App Installer" (which includes Winget) is up to date.

## Installing on Windows 10

- **From Microsoft Store**: Search for **App Installer** and install it.
- **Direct Download**: Visit [aka.ms/getwinget](https://aka.ms/getwinget) and download the latest App Installer package.

---

# Winget Basics

## Searching for Applications

```bash
winget search <app-name>
```

Example:

```bash
winget search firefox
```

> It will list all related apps. To narrow it down, use the **ID** provided in the results.

## Installing Applications

```bash
# Install with App Name
winget install <app-name>

# If multiple results show up, specify the app ID:
winget install <app-id>
```

Example:

```bash
winget install Mozilla.Firefox
```

## Listing Installed Applications

```bash
winget list
```

## Updating Applications

```bash
# Update a specific app:
winget upgrade <app-name>

# Update all apps at once:
winget upgrade --all
```

## Uninstalling Applications

Remove an app by name or ID:

```bash
winget uninstall <app-name>
```

**⚠️ Be careful with dependencies:** Removing shared libraries or tools might break other apps.

---

# Advanced Features

## Backup and Restore

Save your app setup and replicate it on another machine:

1. Export a list of installed apps:

   ```bash
   winget export --output apps.json
   ```

2. Import the list on another machine:

   ```bash
   winget import --input apps.json
   ```

> **Note**: This restores apps with their default configuration. Customizations aren’t included.

# Custom Sources

Add custom app repositories to expand your app library:

```bash
winget source add --name <source-name> <source-url>
```

List current sources:

```bash
winget source list
```

# Running Scripts with Winget

```bash
winget install vscode && winget install git
```

---

# Tips and Tricks

- **Use `--silent`**: Skip prompts during installation.

  ```bash
  winget install <app-name> --silent
  ```

- **Avoid Uninstalling Critical Dependencies**: Double-check dependencies before removing apps.

- **Winget.run**: Use [Winget.run](https://winget.run) to search apps and copy installation commands directly from your browser.

- **Shortcut Commands**:

  - View help: `winget --help`
  - View version: `winget --version`

- **Script Your Setup**: Watch a video on automating your Windows 11 setup - [Windows 11 Setup and WSL]({% post_url 2024-12-22-CE03-WindowsDesktopSetup %})

---

# Troubleshooting

- **App Not Found**: Ensure Winget is up to date by running updates in the Microsoft Store.
- **Errors During Installation**: Check app IDs or use `--force` for stubborn cases.
- **Permissions Issues**: Run the terminal as Administrator.

---

With Winget, managing apps is faster, simpler, and more efficient. Whether you’re setting up a new machine or maintaining your current one, Winget is your go-to tool. Try it out and make your Windows experience smoother!
