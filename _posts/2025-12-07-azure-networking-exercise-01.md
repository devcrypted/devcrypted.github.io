---
layout: post
authors:
  - devcrypted
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: "The 'Kobayashi Maru' of Azure Networking: A 16-Hour Deep-Dive Complex Exercise for Networking Experts"
permalink: azure-networking-exercise-01
media_subpath: /assets/img
date: 2025-12-07 00:33:33 +0530
categories:
  - Cloud Networking
tags:
  - azure
  - azure-networking
  - networking
  - kobayashi-maru
  - multi-region-networking
  - exercises
image: azure-networking-exercise-01.webp
description: The modern cloud network is no longer a simple extension of the on-premises data center. It has evolved into a disjointed, highly abstract mesh of overlay networks, software-defined perimeters, and platform-native connectivity patterns that often defy traditional networking intuition. For a Senior Cloud Engineer, mastery is not demonstrated by the ability to deploy a Virtual Network (VNet); it is demonstrated by the ability to troubleshoot a dropped packet in a split-tunnel, asymmetric, multi-region architecture where the control plane is opaque and the data plane is encrypted.
video_id: ""
playlist_id: ""
github_repo: ""
---

# Module 0: The Philosophical Framework and Exercise

## Architecture

### 0.1 Introduction: The Challenge of Complexity

The modern cloud network is no longer a simple extension of the on-premises data center. It
has evolved into a disjointed, highly abstract mesh of overlay networks, software-defined
perimeters, and platform-native connectivity patterns that often defy traditional networking
intuition. For a Senior Cloud Engineer, mastery is not demonstrated by the ability to deploy a
Virtual Network (VNet); it is demonstrated by the ability to troubleshoot a dropped packet in a
split-tunnel, asymmetric, multi-region architecture where the control plane is opaque and the
data plane is encrypted.
This report outlines a comprehensive, 16-hour continuous simulation designed to push the
boundaries of Azure networking knowledge. Dubbed the "Kobayashi Maru" of connectivity
exercises, it is engineered to be unwinnable without a profound understanding of the
underlying mechanics of the Azure Software Defined Networking (SDN) stack. The exercise
operates at "Complexity Level 3000," moving beyond standard hub-and-spoke topologies
into a realm of overlapping IP spaces, fractured DNS horizons, zero-trust enforcement, and
competing routing protocols.

### 0.2 The Operational Mandate: Zero Trust and No Abstractions

The constraints for this exercise are absolute. To fully expose the "leaky abstractions" of
cloud resources, we reject the use of Terraform, Bicep, or ARM templates. While Infrastructure
as Code (IaC) is the standard for production, it often masks the granular API calls and
dependency chains that are critical for deep troubleshooting. Therefore, every component in
this laboratory will be constructed manually via the Azure CLI or the Azure Portal.

Furthermore, the architecture strictly adheres to a **Zero Trust** model.

- **No Public Ingress** : No Virtual Machine (VM) or Platform-as-a-Service (PaaS) resource
  (SQL, Storage, Function App) may have a public IP address.
- **Management via Bastion** : All administration occurs through a hardened jumpbox or
  Azure Bastion.
- **Private Link Mandate** : All PaaS services must be accessed exclusively via Private
  Endpoints.
- Encryption : All transit traffic must be encrypted.

### 0.3 The Architectural Topology

The simulation constructs a "Geopolitical" map of three distinct network zones, simulating a chaotic real-world enterprise environment formed through aggressive mergers and acquisitions.

Zone|Designation|Region|Characteristics|
Zone A|The Corporate Hub|East US 2|"The central transit point. Hosts the Azure Firewall Premium, VPN Gateway (Active-Active), Azure Route Server (ARS), and Private DNS Resolver. It represents the ""Greenfield"" modern standard."|
Zone B|The Legacy On-Premises,West US 2,"A simulated on-premises datacenter. Since physical hardware is unavailable, this is an isolated Azure VNet running Linux-based Network Virtual Appliances (NVAs) with FRRouting (FRR) to simulate physical Cisco/Juniper edge routers. It hosts legacy ""Mainframe"" simulations (SQL on VMs)."|
Zone C|The Acquisition Spokes|Central US|"A collection of fractured VNets hosting diverse workloads: Azure Container Apps (ACA), Serverless Functions, and Logic Apps. This zone introduces the ""Overlapping IP"" challenge, forcing the use of Network Address Translation (NAT) at the gateway level."|

### 0.4 Faculty Infrastructure and Prerequisites

Before the 16-hour clock begins, the "Faculty" infrastructure must be established. This is the
control plane for the simulation.

**Required Tooling:**

- Azure CLI (v2.40+)
- pspaping and curl for connectivity testing.
- bind9-utils for DNS digging.
- Python 3.9+ for custom validation scripts.

The Complexity of Cost:

A full Virtual WAN (vWAN) deployment, while desired, imposes significant cost constraints on
personal subscriptions. Standard vWAN Hubs incur hourly base unit costs regardless of
traffic.1 To balance realism with fiscal responsibility, this exercise utilizes a Simulated vWAN
architecture using peering meshes and NVAs for the first 12 hours, with an optional module to
deploy an actual vWAN hub for the final integration test if the subscription budget permits.

# 1️⃣ Module 1: The Identity and Connectivity Foundation

## (Hours 0-3)

The first phase establishes the cryptographic identity of the network and the central transit
hub. In a Zero Trust architecture, identity is the new perimeter. Before a single packet can flow,
the security principals governing that flow must be established.

### 1.1 The Identity Control Plane: Managed Identities and Key Vault

Azure networking components, particularly Azure Firewall Premium and Application Gateways,
increasingly rely on Managed Identities to access certificates for Transport Layer Security
(TLS) inspection.

**The "Chicken and Egg" Problem of Private Key Vaults:**

We require a Key Vault to store the certificates for the Firewall. However, the Key Vault itself
must be private.3 If the Key Vault is private, how does the Firewall (which is not yet deployed)
access the certificate during its own deployment?

**Architectural Insight:**

The solution lies in the specific order of operations regarding the Trusted Service bypass.
Azure Firewall is a trusted service. When we lock down the Key Vault, we must ensure that the
firewall's Managed Identity has pre-provisioned access.

**CLI Execution Strategy:**

```Bash

# Define Global Variables for Consistency

export RG_CORE="rg-kobayashi-core"
export LOC_HUB="eastus2"
export VNET_HUB="vnet-hub-core"
export KV_NAME="kv-kobayashi-secure-$RANDOM"

# Create Resource Group

az group create --name $RG_CORE --location $LOC_HUB

# Deploy Key Vault with RBAC Authorization (Modern Standard)

az keyvault create --name $KV_NAME --resource-group $RG_CORE --location $LOC_HUB --enable-rbac-authorization true

# Create User Assigned Managed Identity for Firewall

az identity create --name id-firewall-hub --resource-group $RG_CORE

# Assign Key Vault Secrets User Role to the Identity

export ID_PRINCIPAL=$(az identity show --name id-firewall-hub --resource-group $RG_CORE --query principalId -o tsv)
export KV_SCOPE=$(az keyvault show --name $KV_NAME --resource-group $RG_CORE --query id -o tsv)

az role assignment create --assignee $ID_PRINCIPAL --role "Key Vault Secrets User" --scope $KV_SCOPE
```

### 1.2 Certificate Authority Generation for TLS Inspection

To inspect encrypted traffic—a requirement for our "Complexity 3000" security posture—the
Azure Firewall must act as a Man-in-the-Middle (MitM). It decrypts outbound traffic, inspects
it, and re-encrypts it. This requires an Intermediate Certificate Authority (CA) certificate
stored in the Key Vault.

In a real scenario, this would be issued by an Enterprise Root CA. For this lab, we generate a
self-signed Root CA and an Intermediate CA using OpenSSL on the local shell, then upload it.

**Faculty Note on TLS Mechanics:**

The Azure Firewall Premium dynamically generates server certificates for the sites users visit,
signed by this Intermediate CA. The client machines (Jumpboxes, Spoke VMs) must trust this
Intermediate CA. Failure to distribute this CA to the trusted root store of the client VMs will
result in certificate errors (x509: certificate signed by unknown authority) for all inspected
traffic.

### 1.3 The Hub Network Construction

The Hub VNet is the center of gravity. It does not host workloads; it hosts the **transit
mechanisms**.

**Subnet Architecture:**

- GatewaySubnet (/27): Reserved for VPN/ExpressRoute Gateways.
- AzureFirewallSubnet (/26): Reserved for Azure Firewall.
- RouteServerSubnet (/27): Reserved for Azure Route Server.
- InboundDnsSubnet (/28): For Private Resolver Inbound Endpoint.
- OutboundDnsSubnet (/28): For Private Resolver Outbound Endpoint.
- BastionSubnet (/26): For Azure Bastion.

**Deploying the Azure Route Server (ARS):**

The ARS is the most critical component for the hybrid routing complexity. It manages the BGP
peering with our simulated on-premises NVAs. Without ARS, we would be forced to manage
static User Defined Routes (UDRs) for every spoke, which is unmanageable at scale.

```bash

# Create Hub VNet

az network vnet create --resource-group $RG_CORE --name $VNET_HUB --address-prefixes

##### 10.0.0.0/

# Create Subnets

az network vnet subnet create --name GatewaySubnet --resource-group $RG_CORE --vnet-name $VNET_HUB --address-prefix 10.0.0.0/
az network vnet subnet create --name AzureFirewallSubnet --resource-group $RG_CORE --vnet-name $VNET_HUB --address-prefix 10.0.1.0/
az network vnet subnet create --name RouteServerSubnet --resource-group $RG_CORE --vnet-name $VNET_HUB --address-prefix 10.0.2.0/

# Deploy Route Server

az network public-ip create --name pip-ars --resource-group $RG_CORE --sku Standard
az network routeserver create --name rs-hub --resource-group $RG_CORE --hosted-subnet RouteServerSubnet --public-ip-address pip-ars
```

**Architectural Insight - Why ARS?**

ARS allows the Virtual Network Gateway to exchange routes with NVAs (Network Virtual
Appliances) inside the VNet. In our "Kobayashi Maru" scenario, we will eventually deploy a
Linux NVA inside the Azure Hub to act as a secondary BGP router, creating a conflict scenario.
ARS is the bridge that injects these NVA-learned routes into the SDN fabric.

# 2️⃣ Module 2: The Hybrid Core and BGP Mechanics (Hours 3-6)

This module focuses on the "On-Premises" simulation. Since we cannot physically run cables,
we simulate the on-premises datacenter using a separate VNet (vnet-onprem) in a different
region (West US 2). Connectivity will be established via a Site-to-Site (S2S) VPN, but with a
twist: we will use **FRRouting (FRR)** on Linux VMs to act as the on-premises Customer Edge
(CE) routers, speaking BGP to Azure.

### 2.1 The Simulated Datacenter (Zone B)

We deploy a Linux VM (nva-onprem) that will serve as the gateway for the simulated
172.16.0.0/12 corporate network.

**The NVA Build:**

- OS: Ubuntu 22.04 LTS.
- Networking: IP Forwarding Enabled on the NIC.
- Software: FRRouting (FRR) and StrongSwan (for IPsec).

**Deep Dive: The BGP State Machine in FRR**
FRR implements the BGP decision process. When it peers with the Azure VPN Gateway, it will receive routes for the Azure Hub (`10.0.0.0/16`). Conversely, it must advertise the corporate ranges.

**Configuration Complexity:**

We must configure FRR to support Active-Active peering. The Azure VPN Gateway (VpnGw2AZ
SKU) will provide two public IPs and two BGP peer IPs (APIPA or private IPs). Our FRR router
must establish two simultaneous BGP sessions to ensure redundancy.

**Sample `frr.conf` for the Simulation 7:**

```conf
! /etc/frr/frr.conf
frr version 8.
frr defaults traditional
hostname onprem-edge-
!
router bgp 65001
bgp router-id 172.16.0.
! Peer with Azure Instance 0
neighbor 10.0.0.4 remote-as 65515
neighbor 10.0.0.4 description Azure-Gw-Inst
neighbor 10.0.0.4 ebgp-multihop 2
! Peer with Azure Instance 1
neighbor 10.0.0.5 remote-as 65515
neighbor 10.0.0.5 description Azure-Gw-Inst
neighbor 10.0.0.5 ebgp-multihop 2
!
address-family ipv4 unicast
network 172.16.0.0/
neighbor 10.0.0.4 route-map AZURE-MAP-IN in
neighbor 10.0.0.4 route-map AZURE-MAP-OUT out
neighbor 10.0.0.5 route-map AZURE-MAP-IN in
neighbor 10.0.0.5 route-map AZURE-MAP-OUT out
exit-address-family
!
route-map AZURE-MAP-IN permit 10
!
route-map AZURE-MAP-OUT permit 10
set metric 100
!
```

Analysis of the Config: Note the set metric 100. This sets the Multi-Exit Discriminator (MED). In
a later phase of the exercise, we will deploy a second NVA with set metric 200 to test Azure's
adherence to BGP best path selection (preferring lower MED).

### 2.2 The Azure VPN Gateway with NAT

In the Hub, we deploy the VPN Gateway. The "Complexity 3000" requirement introduces the **Overlapping IP Scenario**.

**The Scenario:**
A newly acquired branch office uses `10.0.1.0/24`. This range overlaps with our
AzureFirewallSubnet in the Hub. If we simply connect them, routing will break due to the
longest prefix match or simple conflict.

**The Solution: NAT Rules on the VPN Gateway.**

We must configure Ingress and Egress NAT rules on the Gateway.

- **Ingress SNAT** : Traffic coming _from_ the branch (10.0.1.0/24) is translated to 192.168.100.0/24 as it enters Azure.
- **Egress SNAT** : Traffic going _to_ the branch from Azure is translated to a non-conflicting range if necessary.

**CLI Implementation:**

````bash

# Create the Gateway (This takes ~45 mins - use this time to configure the Linux NVA)

```bash
az network vnet-gateway create --name vpngw-hub --resource-group $RG_CORE --vnet $VNET_HUB --public-ip-addresses pip-gw-1 pip-gw-2 --sku VpnGw2AZ --gateway-type Vpn --vpn-type RouteBased --asn 65515 --enable-bgp true

# Apply NAT Rule (Ingress)

az network vnet-gateway nat-rule add --resource-group $RG_CORE --gateway-name vpngw-hub --name Nat-Branch-Ingress --type Static --mode IngressSnat --internal-mappings 192.168.100.0/24 --external-mappings 10.0.1.0/
````

_Implication_ : The On-Premises router will continue to send traffic sourced from 10.0.1.x, but
Azure NSGs and Firewalls will see packets sourced from 192.168.100.x. This translation is
opaque to the VNet. Debugging this requires looking at the "Effective Routes" on the Gateway,
where the NAT'd prefixes should appear.

# 3️⃣ Module 3: The PaaS Enclaves and Private Link DNS (Hours 6-10)

This module builds the workloads. We move away from simple IaaS networking into the more
opaque world of PaaS networking (Azure Container Apps, Logic Apps, and Storage).

### 3.1 Spoke 1: Azure Container Apps (ACA) and the "Wildcard"

ACA environments deployed into a custom VNet utilize an Internal Load Balancer (ILB). This
creates a specific DNS challenge.

**The Architecture:**

- VNet: vnet-spoke-aca (10.1.0.0/16).
- Subnet: snet-aca (Minimum /23 required for Consumption + Dedicated profiles, though
  /27 works for Consumption only, we use /23 to be safe).^11
- Resource: ACA Environment with internal ingress.

**The DNS Challenge 13:**

ACA requires a wildcard DNS record (\*.green-island.eastus2.azurecontainerapps.io) pointing
to the ILB IP. Since we cannot easily put a wildcard A-record in a standard Azure Private DNS
Zone linked to the hub without careful planning, we must create a dedicated Private DNS Zone
for the ACA domain.

**Validation Step:**
You must deploy a "Hello World" container and attempt to curl it from the Hub Bastion.
curl <https://my-app.green-island.eastus2.azurecontainerapps.io>
Failure Condition: If the DNS zone is not linked to the Hub VNet, or if the wildcard record is
missing, this fails.

### 3.2 Spoke 2: Serverless and the "Private Endpoint Loop"

We deploy a Logic App (Standard) that needs to read/write to a Storage Account. Both are
locked down.
The Setup 15 :

1. **Storage Account** : stlogicapp$RANDOM. Public access: **Disabled**.
2. **Private Endpoints** : We need PEs for blob, file, queue, and table sub-resources.
3. **Logic App** : logic-app-secure. VNet Integration enabled into snet-integration.

**The "Catch-22":**
A Standard Logic App stores its runtime state (workflow definitions, history) in the Storage
Account. If you disable public access to the Storage Account before the Logic App is fully
configured with VNet integration and Private DNS resolution, the Logic App deployment will
fail or the app will not start. The runtime cannot reach the storage to read its own
configuration code.

**The Fix:**

You must ensure the DNS resolution for the storage account is working from the VNet where
the Logic App is integrated.

- **App Setting** : WEBSITE_VNET_ROUTE_ALL=1.
- **App Setting** : WEBSITE_CONTENTOVERVNET=1.^15 This is the critical flag that tells the Logic App scaling controller to use the VNet integration to talk to its own storage.

**CLI for Private Endpoint Creation 17 :**

```bash
# Create Private Endpoint for Blob

az network private-endpoint create --name pe-blob --resource-group $RG_CORE --vnet-name $VNET_SPOKE_SERVERLESS --subnet snet-pe --private-connection-resource-id $STORAGE_ID --group-id blob --connection-name con-blob

# Create Private DNS Zone Group (The Magic Link)

az network private-endpoint dns-zone-group create --resource-group $RG_CORE --endpoint-name pe-blob --name zone-group-blob  -private-dns-zone "privatelink.blob.core.windows.net" --zone-name blob
```

### 3.3 Deep Dive: Private Link DNS Resolution Flow

Understanding the packet walk for the Logic App accessing Storage is essential for the
exercise.

1. **DNS Query** : Logic App runtime asks for stlogicapp.blob.core.windows.net.
2. **Azure DNS** : The query hits the Azure recursive resolver (168.63.129.16).^19
3. **CNAME Logic** : The public DNS returns a CNAME to
   stlogicapp.privatelink.blob.core.windows.net.
4. **Private Zone Lookup** : The resolver checks if a Private DNS Zone for
   privatelink.blob.core.windows.net is linked to the VNet.
5. **A-Record Return** : If linked, it returns the private IP (e.g., 10.2.1.4).
6. **Connection** : The Logic App connects to 10.2.1.4.

**Failure Scenario** : If the Private DNS Zone exists but is _not_ linked to the VNet, the resolver falls
back to public DNS, which resolves to the public IP. The connection attempts to go out to the
internet. If the Storage Account firewall is set to "Deny Public," the connection fails.

# 4️⃣ Module 4: The Advanced Routing and vWAN Simulation (Hours 10-12)

### 4.1 The Route Server vs. UDR Conflict

In a typical environment, engineers use UDRs to force traffic to a Firewall. In this "Complexity 3000" lab, we introduce a conflict.

**The Scenario:**

- We have a UDR on the GatewaySubnet pointing 0.0.0.0/0 to the Azure Firewall.
- We have BGP routes coming from ARS pointing specific prefixes to the NVA.

**The Question: Which route wins?**
The Answer: Longest Prefix Match (LPM) always wins. However, if prefixes are identical, UDRs
override learned BGP routes.

**The Exercise Task:**

1. Establish BGP peering between the Gateway and the On-Prem NVA. Advertise
   172.16.0.0/16.
2. Create a UDR on the Hub subnets pointing 172.16.0.0/16 to a "Blackhole" (Next Hop:
   None).^20
3. Observe that connectivity drops despite the BGP route being present in the Gateway.
4. **The Fix** : Modify the UDR to point to the Firewall, or remove the UDR to allow BGP
   propagation.

### 4.2 Integration of Azure Private DNS Resolver

To solve the fractured DNS landscape, we configure the **Azure Private DNS Resolver**.^21

**The Requirement:**

- On-Prem servers must resolve logicapp.privatelink.azurewebsites.net.
- Azure resources must resolve mainframe.corp.local.

Step 1: Inbound Endpoint. We provision an Inbound Endpoint in the Hub (10.0.4.4).

Step 2: On-Prem Configuration. On the Linux NVA (which also acts as a DNS server using Bind9), we configure a Conditional Forwarder. zone `"azure.com" { type forward; forwarders { 10.0.4.4; }; };`

Step 3: Outbound Endpoint & Ruleset We provision an Outbound Endpoint. We create a DNS Forwarding Ruleset linked to the Hub VNet.

- Rule: corp.local -> Target: 172.16.1.5 (On-Prem DNS IP). The "Transitive" DNS Problem: The Spoke VNets (ACA, Serverless) are peered to the Hub. Do they automatically use the Private Resolver? **No.** VNet Peering does not extend custom DNS settings.
  You must manually update the DNS Servers setting on every Spoke VNet to point to the Inbound Endpoint IP (10.0.4.4). CLI for Ruleset 27:

```bash
# Create Ruleset

# Create Ruleset
az dns-resolver forwarding-ruleset create --name ruleset-hub --resource-group $RG_CORE --outbound-endpoints ""

# Create Rule for On-Prem
az dns-resolver forwarding-rule create --ruleset-name ruleset-hub --name rule-corp --domain-name "corp.local." --target-dns-servers "[{ip-address:172.16.1.5,port:53}]" --resource-group $RG_CORE
```

# 5️⃣ Module 5: The Security Perimeter and TLS Inspection (Hours 12-14)

### 5.1 Azure Firewall Premium and the TLS Handshake

We now activate the "God Mode" of the firewall: TLS Inspection.

**The Mechanics:**

1. Client (Spoke VM) sends HTTPS Hello to google.com.
2. UDR routes packet to Firewall.
3. Firewall intercepts Hello. It pauses the connection.
4. Firewall connects to google.com, validates the real cert.
5. Firewall generates a _new_ cert for google.com, signed by its internal CA (stored in KV).
6. Firewall presents this fake cert to the Client.
7. Client accepts it (because it trusts the Root CA).
8. Firewall decrypts payload, inspects for IDPS signatures, re-encrypts, and forwards.

**The Exercise Task:**

Configure an Application Rule to allow access to \*.google.com but deny [https://www.google.com/hidden-path.](https://www.google.com/hidden-path.) This URL-path filtering is only possible if
TLS inspection is working.29 If encryption is not broken, the firewall only sees the SNI (<www.google.com>), not the path (/hidden-path).

**Verification:**
From a Spoke VM, curl <https://www.google.com>. It should work. curl <https://www.google.com/hidden-path>. It should receive a 403 or Connection Reset from the Firewall.

### 5.2 Micro-Segmentation with NSGs

In the "Complexity 3000" spirit, we apply NSGs to the Private Endpoint subnets.
Historically, NSGs did not work on Private Endpoints. Now they do, but the feature must be
explicitly enabled.

**CLI Command:**

```bash
az network private-endpoint update --name pe-blob --resource-group $RG_CORE --set subnet.privateEndpointNetworkPolicies="Enabled"
```

**Task** : Create an NSG that allows port 443 from the Logic App subnet but **denies** it from the
Hub Bastion. Verify that the Bastion cannot access the Storage Account via the private IP,
while the Logic App can.

# Module 6: Chaos, Verification, and the "Final Boss"

## (Hours 14-16)

### 6.1 Automated Verification Suite

We cannot rely on manual checking. We write a Python script that runs on a "Probe VM" in the
Spoke. This script mimics an application health check.

**Faculty Resource: `validate_network.py`**

```python
import socket
import dns.resolver
import requests
import sys

# Configuration
TARGETS =

CUSTOM_DNS = "10.0.4.4" # Hub Private Resolver IP

def test_dns(target):
    res = dns.resolver.Resolver()
    res.nameservers =
    try:
        answers = res.resolve(target['host'], 'A')
        ip = answers.address
        print(f"[OK] DNS {target['name']}: Resolved {target['host']} to {ip}")
        return ip
    except Exception as e:
        print(f"[FAIL] DNS {target['name']}: {e}")
        return None

def test_tcp(ip, port, name):
    if not ip: return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"[OK] TCP {name}: Connection to {ip}:{port} successful")
        else:
            print(f"[FAIL] TCP {name}: Port {port} closed on {ip}")
    except Exception as e:
        print(f"[FAIL] TCP {name}: {e}")

print("--- STARTING COMPLEXITY 3000 VALIDATION ---")
for t in TARGETS:
    resolved_ip = test_dns(t)
    test_tcp(resolved_ip, t['port'], t['name'])
```

### 6.2 The Chaos Studio Experiment

To truly earn the "Senior" title, the network must survive failure. We utilize **Azure Chaos
Studio**.^31

**Experiment 1: The NVA Heart attack**
We will inject a "Network Disconnect" fault into the On-Prem NVA.

- **Expectation** : The BGP session with the VPN Gateway drops. Routes are withdrawn from
  the Route Server.
- **Observation** : How long does convergence take? Does traffic failover to the secondary
  NVA (if configured)?

**Experiment 2: The DNS Blackhole**
We stop the Private Resolver Inbound Endpoint (simulated by blocking port 53 via NSG).

- **Expectation** : All cross-premise name resolution fails.
- **Mitigation** : Does the application have caching? Is there a secondary DNS server
  configured in the VNet DNS settings?

### 6.3 The "Final Boss": Asymmetric Routing Debugging

The ultimate troubleshooting scenario involves the interaction between the VPN Gateway, the Firewall, and the Spoke.

**The Scenario**
Traffic flows from On-Prem (172.16.1.5) -> VPN Gateway -> Hub -> Spoke VM (10.1.0.5). The Return traffic flows Spoke VM -> Hub Firewall (10.0.1.4) -> VPN Gateway -> On-Prem.

**Why this happens:**
The Spoke VM has a UDR 0.0.0.0/0 -> Firewall.
The VPN Gateway routes traffic directly to the Spoke (bypassing Firewall) because it has a
system route for the peering.

**The Result:** Packet Drop. The Firewall sees a SYN-ACK (return traffic) without ever seeing the SYN (inbound traffic). It assumes this is a malformed or spoofed packet and drops it.

**The Solution:** You must force Inbound traffic through the Firewall as well.

- **Action** : Apply a UDR to the **GatewaySubnet**.
- Route: `10.1.0.0/16` (Spoke Range) -> Next Hop: Virtual Appliance (`10.0.1.4` - Firewall IP). This creates a symmetric path: Gateway -> Firewall -> Spoke -> Firewall -> Gateway.

## Conclusion: The State of the Art

Upon completing this 16-hour marathon, you will have built a network that rivals the
complexity of Fortune 100 infrastructures. You have navigated the intricacies of BGP route
reflection via Azure Route Server, implemented Zero Trust via Private Link and TLS Inspection,
and unified a fractured DNS landscape using Private Resolvers.

This exercise proves that in the cloud, "Networking" is no longer about cables and switches. It
is about **Identity** (Managed Identities for Firewalls), **DNS** (the glue of Private Link), and
**Routing Intent** (BGP and UDRs). You have looked into the abyss of the Azure SDN, and by scripting your own validation and chaos, you have ensured that the abyss does not stare back.
