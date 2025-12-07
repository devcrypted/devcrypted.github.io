---
layout: post
authors:
  - devcrypted
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: "Kubernetes 1.35: Key Features and Upgrade Guide for Platform Engineers"
permalink: kubernetes-1-35-features-upgrade-guide
media_subpath: /assets/img
date: 2025-12-07 00:40:37 +0530
categories:
  - Kubernetes
tags:
  - kubernetes
  - k8s upgrade
  - platform engineering
  - cloud native
  - release notes
image: kubernetes-1-35-features-upgrade-guide.webp
description:
  "Detail the new features and deprecations in Kubernetes 1.35. Discuss
  the roadmap for 1.36 and the lifecycle management of clusters in 2025. Focus on
  stability improvements and the "
video_id: ""
playlist_id: ""
github_repo: ""
---

# Kubernetes 1.35: Key Features and Upgrade Guide for Platform Engineers

As Kubernetes continues its trajectory as the de facto standard for container orchestration, staying ahead of the release curve is paramount for platform engineers. The release of Kubernetes 1.35, while still on the horizon, represents a significant milestone in the project's focus on stability, security, and support for emerging workloads.

This article provides a forward-looking analysis of what to expect in Kubernetes 1.35, based on the project's current trajectory and long-term initiatives. We'll explore key themes, anticipated features and deprecations, and a practical guide to managing your cluster's lifecycle into 2025 and beyond.

**\*Note:** As of this writing, Kubernetes 1.35 is a future release, projected for late 2025 or early 2026 based on the current cadence of three releases per year. This guide is based on established trends, active Kubernetes Enhancement Proposals (KEPs), and the stated goals of various Special Interest Groups (SIGs).\*

## The Modern K8s Release: Stability is the Core Feature

Before diving into specific features, it's crucial to understand the philosophy driving modern Kubernetes development. The era of rapid, disruptive changes is over. The project now operates on a "production readiness" freeze cycle, emphasizing stability and predictability for enterprise users.

What this means for practitioners:

- **Longer Maturation Cycles:** Features often spend multiple releases in Alpha and Beta stages, undergoing rigorous testing and community feedback. By the time a feature reaches General Availability (GA), it is considered production-grade.
- **Predictable Deprecation Windows:** APIs are deprecated with ample warning (typically at least one year or three releases), giving teams time to migrate.
- **Focus on the Core:** The core Kubernetes API server, scheduler, and controller manager receive incremental, non-disruptive improvements. Major innovation is often pushed to ecosystem projects (e.g., service meshes, storage operators) that build on top of a stable foundation.

This shift ensures that upgrading a cluster is less about gambling on new features and more about a planned, methodical process of adopting battle-tested improvements.

## Projected Features and Themes in Kubernetes 1.35

Based on ongoing work in the community, we can project several key themes that will define the 1.35 release.

### H3: Graduating Advanced Security Primitives

Security remains a top priority. By the time 1.35 is released, we expect several powerful security features to have reached stable GA status, making them default tools in the platform engineer's arsenal.

- **ValidatingAdmissionPolicy (GA):** This feature, which uses the Common Expression Language (CEL), will be the standard for implementing complex, in-process admission control without requiring custom webhooks. This reduces operational overhead and improves cluster security posture.
- **CEL for CRD Validation (GA):** Extending CEL to Custom Resource Definitions allows for richer, more declarative validation rules directly within the CRD schema, improving the reliability of the entire operator ecosystem.

An example of a `ValidatingAdmissionPolicy` you might be using by then:

```
# A hypothetical policy to enforce that all Deployments have resource limits
# This logic lives directly in the API server, no webhook needed.

apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingAdmissionPolicy
metadata:
  name: "deployment-must-have-limits"
spec:
  failurePolicy: Fail
  matchConstraints:
    resourceRules:
    - apiGroups:   ["apps"]
      apiVersions: ["v1"]
      operations:  ["CREATE", "UPDATE"]
      resources:   ["deployments"]
  validations:
    - expression: "object.spec.template.spec.containers.all(c, has(c.resources.limits))"
      message: "All containers in a Deployment must have resource limits defined."
```

### H3: Enhanced Support for AI/ML and Batch Workloads

The rise of AI/ML has put new demands on Kubernetes. SIG-Node and SIG-Scheduling are actively working on features to better manage these stateful, resource-intensive workloads.

- **Dynamic Resource Allocation (GA):** This will provide a more flexible and extensible way to request and manage specialized hardware like GPUs, FPGAs, and NPUs, moving beyond the limitations of the current device plugin framework.
- **JobSet and Indexed Jobs Maturation:** Ecosystem projects like JobSet (for managing tightly coupled jobs) and core features like Indexed Jobs (for parallel processing) will be mature, providing robust, built-in patterns for complex batch and ML training scenarios.

### H3: Streamlined Cluster Lifecycle and Management

The work of SIG-Cluster-Lifecycle, particularly around Cluster API, will continue to simplify the management of Kubernetes clusters themselves. By 1.35, we can expect:

- **Declarative Control Plane Upgrades:** More sophisticated and automated strategies for rolling out control plane updates with minimal downtime.
- **Improved Node Health and Remediation:** More built-in intelligence for automatically detecting, draining, and replacing unhealthy nodes.

## Planning for Deprecations and Removals

A key part of any upgrade is managing deprecations. The Kubernetes API removal policy ensures you have time to adapt, but proactive monitoring is essential.

By 1.35, any Beta APIs introduced around the 1.28-1.30 timeframe will be candidates for removal. Your primary task is to continuously audit your clusters for usage of deprecated APIs.

### Actionable Steps: Staying Ahead of Deprecations

1.  **Read the Release Notes:** The "Deprecations and Removals" section of the official release notes is your single source of truth. Make reading it a non-negotiable part of your upgrade planning.
2.  **Use Static Analysis Tools:** Integrate tools that scan your manifests and Helm charts for deprecated API versions. A popular open-source tool is `pluto`.

    ```bash
    # Example: Running pluto to detect deprecated APIs in a directory of manifests
    pluto detect-files -d ./manifests
    ```

3.  **Audit Live Clusters:** For running clusters, use tools that query the API server to find controllers and users still accessing removed endpoints. `kubent` is an excellent choice for this.

    ```bash
    # Example: Running kubent (Kubernetes Expired Ticker)
    kubent
    ```

Regularly running these checks will prevent upgrade-time surprises.

## The 2025 Upgrade Guide: A Sustainable Strategy

Big-bang, infrequent upgrades are a recipe for failure. The goal is to make minor version upgrades a routine, low-risk operational task.

### H3: The N-2 Version Policy

For most organizations, a sound policy is to stay no more than two versions behind the latest stable release (N-2). For example, when 1.35 is released, you should be running at least 1.33.

This strategy provides a balance:

- **Security:** You receive timely security patches, as the Kubernetes project supports the three most recent minor releases.
- **Stability:** You avoid Day-1 bugs of a new release, letting the broader community surface them first.
- **Manageable Change:** The delta between two consecutive versions is small and easy to manage.

### H3: A Phased Upgrade Checklist

For every upgrade, follow a structured, phased approach.

1.  **Control Plane First:** Always upgrade the control plane components (`kube-apiserver`, `kube-scheduler`, `kube-controller-manager`, `etcd`) before touching the worker nodes. Managed Kubernetes services (EKS, GKE, AKS) handle this for you.
2.  **Update Core Add-ons:** Ensure your CNI, CSI, Ingress controller, and monitoring agents are compatible with the target Kubernetes version. This is the most common source of upgrade failures.
3.  **Create a Canary Node Pool:** Create a new node pool with the updated `kubelet` version. Migrate a few low-risk, stateless workloads to this pool.
4.  **Monitor and Validate:** Closely monitor application health, latency, and error rates on the canary pool. Check `kubelet` and application logs for any unusual activity.
5.  **Rollout to All Nodes:** Once confident, begin a rolling upgrade of your existing worker node pools, draining and replacing nodes gracefully to avoid application disruption.
6.  **Post-Upgrade Cleanup:** After all nodes are upgraded, perform a final health check and remove any tooling or feature flags related to the previous version.

## Conclusion: The Road to 1.36 and Beyond

Kubernetes 1.35 will not be a revolutionary release, and that is its greatest strength. It will represent the culmination of years of effort to make the platform more secure, stable, and capable of handling the next generation of cloud-native workloads. The roadmap toward 1.36 will likely continue these themes, with an even greater focus on operational simplicity and autonomous systems.

For platform engineers, the key to success is not in chasing the newest alpha feature, but in establishing a disciplined, continuous lifecycle management process. By understanding the project's direction, proactively managing API deprecations, and adopting a routine upgrade cadence, you can ensure your platform remains a stable, secure, and powerful foundation for your organization's innovation.

## Further Reading

- https://kubernetes.io/releases/
- https://www.kubernetes.dev/resources/release/
