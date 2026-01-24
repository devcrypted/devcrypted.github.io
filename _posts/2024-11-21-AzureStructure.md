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
title: "How Microsoft Azure is Structured? | Day 1 of Cloud Engineering"
permalink: introduction-to-azure-building-blocks
date: 2024-11-21 00:00 +0530
categories: ["Microsoft Azure"]
tags: ["Azure", "Management Groups (MG)", "Resource Groups (RG)", "Azure Resources", "Azure Subscription", "Azure Active Directory (AAD/Entra ID)"]
image: https://img.youtube.com/vi/cEg9INnN2p0/maxresdefault.jpg
description: In this blog, you'll understand Azure building blocks, like Management Groups, Subscriptions, Resource Groups, Azure Active Directory (Entra ID), etc.

# Variables
video_id: cEg9INnN2p0
playlist_id: PL2JBbPWIA_Tq6oI8hAkJVR6Uhg5wLx9AM
github_repo: ""
---

- [<i class="fa-brands fa-github"></i> &nbsp; GitHub Repository]({{page.github_prefix}}{{page.github_repo}})
- [<i class="fa-brands fa-youtube"></i> &nbsp; Watch on YouTube]({{page.video_prefix}}{{page.video_id}})
- [<i class="fa-solid fa-list"></i> &nbsp; YouTube Playlist]({{page.playlist_prefix}}{{page.playlist_id}})

---

{% include embed/youtube.html id=page.video_id %}

---

Microsoft Azure’s structure is designed to organize, manage, and secure resources effectively. This guide explains its key components, their hierarchy, and relationships, using real-world examples for clarity.

---

## 1. **Azure AD (Entra ID)**

Azure Active Directory (Azure AD), now part of **Azure Entra**, is Microsoft’s cloud-based identity and access management service. It is used to:

- Authenticate and authorize users, groups, and applications.
- Secure access to Azure resources and external services.

### Key Features

- **Users and Groups**: Manage identities and assign roles (e.g., Administrator, Contributor).
- **App Registrations**: Register applications for secure integration with Azure AD.
- **Enterprise Applications**: Enable Single Sign-On (SSO) and manage SaaS apps like Salesforce or ServiceNow.

### Example

A company "TechCorp" creates:

- **Users**: `john@techcorp.com` (Admin), `jane@techcorp.com` (Contributor).
- **Groups**: "Developers" group assigned access to specific Azure resources.
- **App Registration**: Registers an internal HR app for identity management.

---

## 2. **Azure Enterprise Account**

An **Azure Enterprise Account** is a billing and administrative boundary at the top level, often used by large organizations to manage costs and allocate resources.

### Example

"TechCorp" has an **Enterprise Agreement** with Microsoft and uses an Enterprise Account to:

- Allocate budgets to various departments (e.g., IT, Marketing).
- Generate usage and billing reports.

---

## 3. **Root Management Group**

The **Root Management Group** is the top-most level of management in Azure, and every Azure tenant has a single Root Management Group. All other management groups and subscriptions inherit policies from this group.

### Example

TechCorp’s Root Management Group enforces:

- **Policies**: Require all resources to have tags for cost tracking.
- **RBAC (Role-Based Access Control)**: Only global admins can modify the Root Management Group.

---

## 4. **Management Groups**

Management Groups provide a way to organize subscriptions into a hierarchy for applying policies and managing access at scale. A single Azure tenant can have up to **6 levels** of management groups.

### Example Hierarchy

1. **Root Management Group**
   - **IT Management Group**
     - "Development Subscriptions"
     - "Production Subscriptions"
   - **Finance Management Group**
     - "Financial Analysis Subscriptions"

---

## 5. **Subscriptions**

A **Subscription** acts as a billing unit and provides access to deploy and manage Azure resources. Each subscription is associated with one or more management groups.

### Example

TechCorp creates:

- **Subscription 1**: "Dev Environment" for developers to test code.
- **Subscription 2**: "Prod Environment" for live workloads.

---

## 6. **Resource Groups**

A **Resource Group (RG)** is a container that holds Azure resources, providing a logical grouping for easier management.

### Example

TechCorp creates:

- **Resource Group 1**: "WebAppRG" for hosting an application.
  - **Resources**:
    - Azure SQL Database
    - Virtual Machines (VMs)
    - Load Balancer (LB)

- **Resource Group 2**: "MonitoringRG" for storing log and metric data.

---

## 7. **Resources**

**Resources** are the actual services and objects deployed in Azure. They include VMs, databases, load balancers, virtual networks, and more.

### Examples of Resources

- **Compute**: Virtual Machines (VM), Virtual Machine Scale Sets (VMSS).
- **Networking**: Load Balancers (LB), Application Gateways.
- **Databases**: Azure SQL Database, Cosmos DB.

---

## Key Differences

| Component                  | Purpose                              | Example                              |
|----------------------------|--------------------------------------|--------------------------------------|
| **Azure AD (Entra)**       | Identity and Access Management      | Manage users, groups, and apps.     |
| **Enterprise Account**     | Billing and cost management         | Allocate budgets for departments.   |
| **Root Management Group**  | Top-level management group          | Enforce tenant-wide policies.       |
| **Management Groups**      | Organize subscriptions into hierarchies | Group subscriptions for IT/Finance. |
| **Subscriptions**          | Billing unit and resource boundary  | Dev/Prod subscriptions.             |
| **Resource Groups**        | Logical grouping for resources      | Group VMs, LBs, and databases.      |
| **Resources**              | Individual Azure services           | VM, SQL DB, App Services.           |

---

## Summary of Relationships

1. **Azure AD** manages identities that access Azure resources.
2. **Enterprise Account** provides billing at the organization level.
3. **Root Management Group** is the tenant-wide policy enforcer.
4. **Management Groups** organize subscriptions into logical hierarchies.
5. **Subscriptions** contain Resource Groups.
6. **Resource Groups** contain individual resources like VMs and databases.

### Visual Representation

![Visual Representation](mg-structure.png)
