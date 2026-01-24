---
layout: post
authors: ["kamal"]
media_subpath: /assets/img/
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
youtube_logo: <i class="fa-brands fa-youtube"></i>

# Should be changed according to post
published: true
title: "Introduction to Azure Networking"
permalink: introduction-to-azure-networking
date: 2024-11-18 00:00 +0530
categories: ["Microsoft Azure"]
tags: ["Azure", "Networking", "Virtual Network", "vNet Peering"]
image: https://img.youtube.com/vi/N3AV6OLahBM/maxresdefault.jpg
description: In this blog, you'll understand Azure Virtual Networks, vNet peering and demonstration on how to create and delete the virtual network in Azure portal.

# Variables
video_id: N3AV6OLahBM
playlist_id: PL2JBbPWIA_Tq6oI8hAkJVR6Uhg5wLx9AM
github_repo: ""
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

## What is Azure Virtual Network?

Azure Virtual Network (VNet) is the foundational building block for your private network in Azure. It enables Azure resources, such as virtual machines (VMs), to securely communicate with:

- Each other
- The internet
- On-premises networks

You can segment a virtual network into **subnets** for better organization and management.

**Pro Tip:** Use tools like [Visual Subnet Calculator](https://visualsubnetcalc.com) if you're new to subnetting.

### Example Scenario

- **Virtual Network CIDR**: `10.0.0.0/16`
- **Subnets**:
  - `10.0.0.0/18`
  - `10.0.64.0/18`
  - `10.0.128.0/18`
  - `10.0.192.0/18`

---

## Key Considerations

- **Within a VNet**:
  - VMs can communicate without additional configuration.
  - VMs in different subnets within the same VNet can also communicate by default.
  - **To block communication between subnets**, use **Network Security Groups (NSGs)**.

- **Between VNets**:
  - VNets **cannot communicate by default**.
  - To enable communication, use **VNet Peering**:
    - **Local VNet Peering**: For VNets in the same region.
    - **Global VNet Peering**: For VNets in different regions.

---

## How to Create a Virtual Network in Azure Portal

1. Go to the [Azure Portal](https://portal.azure.com).
2. Search for **Virtual Network** in the search bar.
3. Click on **Create**.
4. Fill in the **Basic Details**, including the VNet name.
5. Navigate to the **IP Addresses** tab:
   - Create subnets as needed (one default subnet is created automatically).
6. (Optional) Add **tags** in the Tags tab for better organization.
7. Click on **Review + Create**.
8. Verify the details and click **Create**.

---

## How to Delete a Virtual Network

### Using the Azure Portal

1. Navigate to the VNet you want to delete.
2. Click on the **Delete** button and confirm.

### Using Azure CLI

**To delete a VNet:**

```bash
az network vnet delete --name <vnet-name> --resource-group <resource-group-name>
```

**To list Virtual Networks:**

```bash
az network vnet list -o jsonc
```
