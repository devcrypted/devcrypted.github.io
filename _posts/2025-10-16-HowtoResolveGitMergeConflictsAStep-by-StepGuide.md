---
layout: post
authors: ["devcrypted"]
media_subpath: /assets/img/
pin: false

# Should be changed according to post
published: true
title: "How to Resolve Git Merge Conflicts: A Step-by-Step Guide"
permalink: how-to-resolve-git-merge-conflicts-a-step-by-step-guide
date: 2025-10-16 00:39 
categories: ["Cloud Engineering"]
tags: ["Git", "GitHub Actions", "Tutorial"]
description: Step-by-step guide to mastering Git for effective version control.
---

<!-- This blog post was automatically generated using AI -->

---

Git essential workflow: track changes, share updates.

## Git Basic Workflow: Commit, Push, Pull

### 1. Repository Setup

-   **New project init:**
    ```bash
    git init
    ```
-   **Clone existing repo:**
    ```bash
    git clone <repository-url>
    ```

### 2. Local Changes (Stage & Commit)

-   **Check file status:**
    ```bash
    git status
    ```
-   **Add files to staging area:**
    ```bash
    git add <file-name>
    git add . # All changes
    ```
-   **Commit staged changes:**
    ```bash
    git commit -m "Descriptive commit message"
    ```
-   **Amend last commit:**
    ```bash
    git commit --amend --no-edit # Change message or add forgotten files
    ```

### 3. Remote Operations (Push & Pull)

-   **Push local commits to remote:**
    ```bash
    git push origin <branch-name>
    ```
-   **First push, set upstream:**
    ```bash
    git push -u origin main
    ```
-   **Pull remote changes to local:** (Fetch + Merge)
    ```bash
    git pull origin <branch-name>
    ```
-   **Fetch remote changes only:** (No merge)
    ```bash
    git fetch origin
    ```

### Basic Workflow Commands

```bash
# Start a new repo
git init

# Clone an existing repo
git clone <url>

# Check working directory status
git status

# Stage changes
git add .

# Commit changes
git commit -m "feat: initial commit"

# Push to remote
git push origin main

# Pull from remote
git pull origin main
```