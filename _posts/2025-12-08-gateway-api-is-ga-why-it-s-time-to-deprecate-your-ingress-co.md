---
layout: post
authors:
- devcrypted
pin: false
video_prefix: https://youtu.be/
playlist_prefix: https://youtube.com/playlist?list=
github_prefix: https://github.com/devcrypted/
published: true
title: "Gateway API is GA: Why It\u2019s Time to Deprecate Your Ingress Controller"
permalink: kubernetes-gateway-api-vs-ingress-migration
media_subpath: /assets/img
date: 2025-12-07 00:33:33 +0530
categories:
- Cloud Networking
tags:
- kubernetes
- gateway api
- networking
- ingress
- istio
image: 514d15bf328844a68a039afa71f39db6.webp
description: Comprehensive argument for migrating from Kubernetes Ingress to the Gateway
  API. Explain the technical limitations of Ingress (annotations hell) vs. the role-oriented
  design of Gat
video_id: ''
playlist_id: ''
github_repo: ''
---

# Gateway API is GA: Why It’s Time to Deprecate Your Ingress Controller

The Kubernetes Gateway API has reached a major milestone: key APIs like `Gateway`, `GatewayClass`, and `HTTPRoute` are now Generally Available (GA). This isn't just an incremental update; it's a fundamental reimagining of how traffic gets into your cluster. For years, Ingress has been the default, but its limitations have spawned a complex ecosystem of vendor-specific annotations and operational headaches.

The Gateway API provides a standardized, expressive, and role-oriented model for Kubernetes networking. If you're still managing a fleet of Ingress resources, now is the time to plan your migration. This article breaks down why the Gateway API is a superior model and provides a clear strategy for moving away from legacy Ingress controllers.

---

## The Pain of Ingress: A Look Back at "Annotations Hell"

The original Ingress API was a great start. It provided a simple, portable way to expose HTTP services. However, its simplicity became its greatest weakness. The specification was intentionally minimal, leaving advanced features up to individual implementations.

This led to the rise of "annotations hell." To configure anything beyond basic host and path routing, you had to rely on vendor-specific metadata.

Consider a typical Ingress managed by NGINX. Your resource would be littered with annotations for essential features:

*   URL rewrites: `nginx.ingress.kubernetes.io/rewrite-target: /`
*   CORS headers: `nginx.ingress.kubernetes.io/enable-cors: "true"`
*   Request timeouts: `nginx.ingress.kubernetes.io/proxy-read-timeout: "60s"`
*   Authentication: `nginx.ingress.kubernetes.io/auth-url: "http://auth-service/verify"`

This approach has several critical flaws:

1.  **No Portability:** Annotations are vendor-specific. If you decide to switch from NGINX to Traefik or HAProxy, you must learn a new set of annotations and rewrite all your Ingress resources.
2.  **Poor Validation:** Kubernetes doesn't validate the content of annotations. A simple typo (`proxy-read-timout` instead of `proxy-read-timeout`) will be silently ignored, leading to frustrating debugging sessions.
3.  **Lack of RBAC:** An Ingress resource bundles everything—the "what" (route `/app` to `app-service`) and the "how" (apply these timeouts, enable this auth). This makes it impossible to delegate permissions cleanly. You can't let a developer manage their application's routes without also giving them control over TLS certificates or gateway-level settings.

Ingress forced a choice: stay with the minimal, portable standard and have no features, or embrace a single vendor's annotations and lose all portability. The Gateway API was designed to solve this dilemma.

## The Gateway API Solution: Role-Oriented and Expressive

The Gateway API isn't just a better Ingress; it's a new paradigm. It deconstructs the monolithic Ingress resource into a set of specialized, interoperable resources that align with distinct operational roles.

### The Three Key Roles (and Resources)

The Gateway API's structure is built around a separation of concerns, mapping directly to how teams operate in the real world.

*   **Infrastructure Provider (Cluster Operator):** This role manages the underlying network infrastructure. They define a `GatewayClass`, which is a template for provisioning load balancers (e.g., `nginx-class`, `gke-l7-gxlb`). They also instantiate a `Gateway`, which represents a specific load balancer instance, requests an IP address, and defines which ports are open (e.g., `prod-web-gateway` on port 443).

*   **Application Operator (Platform Team):** This role manages how applications are exposed on the gateways. They can control which namespaces are allowed to attach routes to a specific `Gateway`, ensuring that a dev team can't accidentally hijack traffic meant for another team.

*   **Application Developer:** This role focuses solely on their application's routing logic. They create `HTTPRoute` resources (or `TCPRoute`, `GRPCRoute`, etc.) to map traffic from a parent `Gateway` to their `Service`. They don't need to know about certificates, IP addresses, or cloud provider specifics.

### Core Benefits Over Ingress

This role-oriented design delivers tangible benefits:

*   **Standardized Expressiveness:** Features like header-based routing, weighted backends (for canary releases), and URL rewrites are now first-class fields in the `HTTPRoute` spec. No more annotations.
*   **True Portability:** An `HTTPRoute` that performs a 5% canary split will work consistently across different Gateway API implementations like Istio, Kong, or NGINX Gateway Fabric.
*   **Granular RBAC:** Security becomes straightforward. Cluster operators can use Kubernetes RBAC to grant developers `create` permissions only for `HTTPRoute` in their own namespace, while restricting `Gateway` access to the platform team.
*   **Clean Extensibility:** For features not in the core API, the Gateway API provides a structured extension point called `PolicyAttachment`. This allows vendors to attach custom policies (like Web Application Firewall rules or rate-limiting) in a standardized way that is far superior to the free-for-all of annotations.

## Migration Strategy: From Ingress to Gateway

Migrating from Ingress is a planned process, not a sudden cut-over. The goal is to run both systems in parallel, validate functionality, and then shift traffic.

### General Migration Steps

1.  **Install a Gateway Controller:** Your cluster must have a controller that implements the Gateway API specifications. Popular options include Istio, NGINX Gateway Fabric, Kong, and cloud-provider-specific implementations.

2.  **Define a `GatewayClass` and `Gateway`:** A cluster administrator defines the `GatewayClass` provided by the controller and then creates a `Gateway` resource. This will provision a new load balancer with a distinct external IP address.
    ```shell
    # 1. Operator installs the controller (e.g., via Helm)

    # 2. Operator defines the Gateway resource, which will get a new IP
    kubectl apply -f my-gateway.yaml

    # 3. Check the status to get the new external IP address
    kubectl get gateway prod-web-gateway -o jsonpath='{.status.addresses[0].value}'
    ```

3.  **Translate and Shadow:** For each existing `Ingress` resource, create a corresponding `HTTPRoute` resource. The `HTTPRoute` will attach to the new `Gateway`. At this stage, your Ingress Controller and Gateway Controller are running side-by-side, serving traffic on different IP addresses.

4.  **Test and Validate:** Use internal host resolution or a staging DNS entry to send test traffic to the new Gateway's IP address. Verify that all routing rules, rewrites, and headers are working as expected.

5.  **Cut Over DNS:** Once you have confidence in the new setup, update your public DNS records to point from the old Ingress IP to the new Gateway IP. Monitor traffic closely.

6.  **Decommission:** After a safe observation period, you can delete the original `Ingress` resources and uninstall the legacy Ingress controller, freeing up resources.

---

## Practical Migration Paths

The specifics of translating annotations will depend on your current Ingress controller.

### For NGINX Ingress Users

NGINX offers two relevant projects: the legacy `ingress-nginx` controller and the new, purpose-built `nginx-gateway-fabric`. The migration path is to adopt the **NGINX Gateway Fabric**.

Your primary task will be to convert `nginx.ingress.kubernetes.io/` annotations into standard `HTTPRoute` fields.

*   **Rewrite Target:** An annotation like `nginx.ingress.kubernetes.io/rewrite-target: /some/path/$1` becomes a standard `URLRewrite` filter within the `HTTPRoute` rules.
*   **Traffic Splitting:** Canary deployments previously managed with complex, multi-Ingress annotation tricks are now handled by the standard `backendRefs` field, where you can assign a weight to each backend service (e.g., `service-v1` gets weight 95, `service-v2` gets weight 5).

The NGINX team provides detailed documentation and examples for this translation process.

### For Istio Ingress Gateway Users

Istio users have a unique advantage. Istio's own `Gateway` and `VirtualService` CRDs were a primary inspiration for the official Gateway API. As of Istio 1.16+, the `istio-ingressgateway` has native support for the Kubernetes Gateway API.

This means you can have Istio `VirtualServices` and Kubernetes `HTTPRoutes` coexist and attach to the same Istio gateway.

The migration path is to incrementally translate your `VirtualService` resources into `HTTPRoute` resources.

*   **Istio's `Gateway` vs. K8s `Gateway`:** You will configure Istio to recognize the standard `gateway.networking.k8s.io/v1` resource instead of its legacy `networking.istio.io/v1beta1` counterpart.
*   **`VirtualService` to `HTTPRoute`:** A `VirtualService`'s HTTP match conditions, rewrites, and delegate sections map cleanly to the `matches`, `filters`, and `backendRefs` in an `HTTPRoute`.

Istio provides a helpful tool to aid in this process:

```shell
# This command helps convert an Istio VirtualService to a Kubernetes HTTPRoute
istioctl experimental gtw-translate
```

This allows you to migrate your routes one application at a time without a "big bang" cut-over, leveraging the same underlying Istio data plane you already trust.

## Conclusion

The standardization of the Gateway API is a significant step forward for the Kubernetes ecosystem. It addresses the fundamental architectural flaws of the Ingress API by providing a portable, expressive, and secure model for traffic management. The "annotations hell" that plagued operations teams is replaced by a clean, role-oriented API that enhances both developer agility and platform stability.

The migration requires effort, but the long-term benefits are undeniable: a more portable, maintainable, and secure networking configuration for your clusters. Don't wait for your Ingress setup to become an unmanageable legacy system. Start exploring the Gateway API and planning your migration today.


## Further Reading

- https://blog.nginx.org/blog/kubernetes-networking-ingress-controller-to-gateway-api
- https://konghq.com/blog/engineering/gateway-api-vs-ingress
