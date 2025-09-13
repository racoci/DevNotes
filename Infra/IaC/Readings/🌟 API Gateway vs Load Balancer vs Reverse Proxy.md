# API Gateway vs Load Balancer vs Reverse Proxy 🌟

### #85: Break Into Edge Architecture (4 Minutes)

[](https://substack.com/@systemdesignone)

[Neo Kim](https://substack.com/@systemdesignone)

Aug 29, 2025

[](https://newsletter.systemdesign.one/p/api-gateway-load-balancer-reverse-proxy/comments)

Get my system design playbook for FREE on newsletter signup:

Subscribe

---

_This post outlines the differences between a load balancer, API gateway, and reverse proxy. You will find references at the bottom of this page if you want to go deeper._

- _[Share this post](https://newsletter.systemdesign.one/p/api-gateway-load-balancer-reverse-proxy/?action=share) & I'll send you some rewards for the referrals._
    

Once upon a time, a single server was enough to run an entire site.

The clients connected directly to it over the internet.


![API Gateway vs Load Balancer vs Reverse Proxy](https://substackcdn.com/image/fetch/$s_!SaFm!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3b7b30a-4ead-4213-aa97-7d7eb248543c_800x500.gif "API Gateway vs Load Balancer vs Reverse Proxy")



[Image Gif](https://substackcdn.com/image/fetch/$s_!SaFm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd3b7b30a-4ead-4213-aa97-7d7eb248543c_800x500.gif)

But as the internet became more popular, some sites exploded in traffic.

And it became extremely hard to scale those sites reliably.

So they added more servers and put a traffic management layer in front of those sites.

This includes components such as the load balancer, API gateway, and reverse proxy.

Yet it’s necessary to understand their differences to keep the site reliable.

Onward.

---

### **[Ship faster, with context-aware AI that speaks your language - Sponsor](https://refactoring.link/aug-sd)**

**[Augment Code](https://refactoring.link/aug-sd)** is the only AI coding agent built for real engineering teams.

It understands your codebase—across 10M+ lines, 10k+ files, and every repo in your stack—so it can actually help: writing functions, fixing CI issues, triaging incidents, and reviewing PRs.  
All from your IDE or terminal. No vibes. Just progress.

[Learn more about Augment](https://refactoring.link/aug-sd)

---

## Load Balancer

A load balancer distributes traffic evenly among servers.

Think of the **load balancer** as a restaurant manager who ensures each waitress handles a fair number of tables without overwhelming themselves.

[

![How Load Balancer Works](https://substackcdn.com/image/fetch/$s_!Zxev!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59b4201f-60c9-4b9f-8ede-ac4f619be384_948x672.png "How Load Balancer Works")



](https://substackcdn.com/image/fetch/$s_!Zxev!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F59b4201f-60c9-4b9f-8ede-ac4f619be384_948x672.png)

How Load Balancer Works

Here’s how it works:

1. The client sends a request to the load balancer
    
2. The load balancer finds servers that are ready to accept the request
    
3. It then forwards the request to the proper server
    

This technique ensures high availability.

Yet each service has a different workload and usage pattern. So it’s necessary to use different algorithms to route traffic.

Here are some of them:

- [Round-robin](https://www.vmware.com/topics/round-robin-load-balancing): routes traffic across servers in a sequential order.
    
- [Least-connections](https://www.f5.com/glossary/least-connection): routes traffic to the least busy servers.
    
- [IP-hashing](https://kemptechnologies.com/resources/glossary/source-ip-hash-load-balancing): routes a client’s traffic to the same server for sticky sessions.
    

And some popular examples of load balancers are [HAProxy](https://www.haproxy.org/), [AWS ELB](https://aws.amazon.com/elasticloadbalancing/), and [Nginx](https://nginx.org/).

Besides some load balancers work at [layer 4](https://osi-model.com/transport-layer/) (**transport level**). This means it checks the IP address and port number to route traffic. While others operate at [layer 7](https://osi-model.com/application-layer/) (**application level**). This means they check details such as URLs or HTTP headers to route traffic.

A load balancer prevents server overload and offers faster response time. But it adds operational costs and resource usage. Also it could become a single point of failure if configured incorrectly. So it’s important to design and monitor them for high availability.

Let’s keep going!

## API Gateway

The API Gateway acts as a single entry point to the site.

Imagine an **API Gateway** as the kitchen window of a busy restaurant. It’s where the orders get passed from a waitress to the kitchen. This avoids overwhelming the kitchen with many orders, similar to rate limiting.

[

![How API Gateway Works](https://substackcdn.com/image/fetch/$s_!jzIQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c20d45a-30bb-4ea3-94c1-5d8480e373b1_822x404.png "How API Gateway Works")



](https://substackcdn.com/image/fetch/$s_!jzIQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c20d45a-30bb-4ea3-94c1-5d8480e373b1_822x404.png)

How API Gateway Works

Here’s how it works:

1. The client sends a request to the API Gateway
    
2. The API Gateway throttles requests to avoid server overload and transforms data if necessary
    
3. It then routes the request to the correct microservices based on its URL path, HTTP headers, or query parameters
    
4. The API Gateway combines the responses from different microservices and responds to the client
    

Some popular ways to set up an API Gateway are using [Kong](https://konghq.com/), [AWS API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html), and [Google Cloud Apigee](https://cloud.google.com/apigee).

An API Gateway simplifies client interactions. Yet it slightly increases latency because of an extra network hop. Also it might become a performance bottleneck if set up incorrectly. So it’s important to install it properly.

Ready for the next part?

## Reverse Proxy

A reverse proxy protects the backend server. It decrypts incoming traffic for [TLS termination](https://en.wikipedia.org/wiki/TLS_termination_proxy) and caches the response to reduce server load.

Think of the **reverse proxy** as a kitchen host. They accept the orders on behalf of the kitchen chefs. This helps to group orders and reject orders if something is unavailable (**filter traffic**).

[

![How Reverse Proxy Works](https://substackcdn.com/image/fetch/$s_!AT1m!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5680c2e-60f6-4865-81e2-f0edbb1cc1e3_1404x710.png "How Reverse Proxy Works")



](https://substackcdn.com/image/fetch/$s_!AT1m!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa5680c2e-60f6-4865-81e2-f0edbb1cc1e3_1404x710.png)

How Reverse Proxy Works

Here’s how it works:

1. The client sends a request to the reverse proxy
    
2. It forwards the request to the server
    
3. The server responds to the reverse proxy
    
4. The reverse proxy then caches the response and returns it to the client
    

Some ways to set up a reverse proxy are using [Nginx](https://nginx.org/), [HTTP Server](https://httpd.apache.org/), or [Traefik](https://traefik.io/traefik).

A reverse proxy hides the backend server complexity and speeds up responses with caching. Yet it increases operational complexity and might become a single point of failure without redundancy. So it’s important to design it with failover and set up proper monitoring.

---

### TL;DR

Here’s how a typical edge architecture looks:

[

![High Level Overview of Edge Architecture](https://substackcdn.com/image/fetch/$s_!REc3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F114ff066-b879-4603-9f74-b28f2fe808a6_2020x339.png "High Level Overview of Edge Architecture")



](https://substackcdn.com/image/fetch/$s_!REc3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F114ff066-b879-4603-9f74-b28f2fe808a6_2020x339.png)

High-Level Overview of Edge Architecture

- Load balancer: distributes traffic evenly across servers
    
- API gateway: handles complex service calls
    
- Reverse proxy: handles security and caching
    

They manage traffic reliably and securely in large-scale systems. Yet this isn’t the only way to set them up together. So use them based on your scale and needs.