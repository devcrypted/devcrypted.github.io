---
layout: post
authors: ["devcrypted"]
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: 4 Ways To Create Azure Resources
permalink: 4-ways-to-create-azure-resource
media_subpath: /assets/img
date: 2024-12-22 00:00 +0530
categories: ["Microsoft Azure"]
tags: ["Terraform", "Azure CLI", "Cloud Engineering", "PowerShell"]
image: headers/CE03.png
description: "This blog will showcase four methods for creating resources in Azure: Azure Portal, Azure CLI, Azure PowerShell, and Terraform."
video_id: g3D0SJ8uBIg
playlist_id: PL2JBbPWIA_Tq6oI8hAkJVR6Uhg5wLx9AM
github_repo: ""
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

🧪 Let's quickly get started and create our first ever resource; a Resource Group.

## 1️⃣ CREATE USING AZURE PORTAL

1. Let's go to [portal.azure.com](https://portal.azure.com) and login using your Microsoft credentials.
2. Go to Global Search bar (G+/) and search for Resource Group.
3. Click on [+ Create](https://portal.azure.com/#create/Microsoft.ResourceGroup) button.
4. Now, you need to fill in 2 details:
   1. Resource Group Name - I'm naming it `TestRGUsingPortal`
   2. Location/Region - I'm using `CentralIndia`
5. You can now Click on Next. Feel free to add tags if you want.
6. Once done, click on `Create`

## 2️⃣ CREATE USING AZURE CLI

🚩 Skip 1st and 2nd step if you're using Azure Cloud Shell.

1. Download and install Azure CLI from [aka.ms/azcli](https://aka.ms/azcli)
2. Run command `az login` to login.
3. Run below command to create a new Resource Group using Azure CLI

    ```bash
    az group create --name 'TestRGUsingAzCLI'
    ```

## 3️⃣ CREATE USING AZURE POWERSHELL

🚩 Skip 1st and 2nd step if you're using Azure Cloud Shell.

1. Download and install Azure PowerShell module by running below command:

    ```powershell
    Install-Module -Name 'Az' -Scope CurrentUser
    ```

2. Login to Azure PowerShell using command: `Login-AzAccount`
3. Finally let's create a Resource group using below command:

    ```powershell
    New-AzResourceGroup -Name 'TestRGUsingAzPowerShell'
    ```

## 4️⃣ CREATE USING HASHICORP TERRAFORM

1. Let's create folder: `mkdir terraform-demo && cd terraform-demo`
2. Let's create a new terraform file `main.tf` and add below contents:

    ```terraform
    provider "azurerm" {
      features {}
      subscription_id = "0000-0000-0000000-00000000-0000000"
    }

    resource "azurerm_resource_group" "rg" {
      name     = "TestRGUsingTerraform"
      location = "JapanEest"

      tags = {
        environment = "sandbox"
        platform    = "app"
        department  = "finance"
      }
    }
    ```

3. To find the subscription ID, use command `az account show --query 'id'`
4. Use `terraform init` to initialize terraform.
5. Use `terraform apply` to create the resource group. Make sure you type `yes` and hit enter when asked to.

## 🧠 BONUS TIPS

1. Use `terraform destroy` to delete what you've created using Terraform.
2. Use `--auto-approve` flag with apply and destroy commands to skip confirmation. E.g.
   1. `terraform apply --auto-approve`
   2. `terraform destroy --auto-approve`
3. Use below PowerShell command to delete the resources that were created as part of this demo:

    ```powershell
    Get-AzResourceGroup -Name 'TestRGUsing*' | Remove-AzResourceGroup -Force
    ```
