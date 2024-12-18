# ArgoCD GitHub WebHook utility for monorepos with multiple Applications

### NOTE!!!
#### This is not meant to be used for production, this is only a personal weekend-project to learn about developing applications on Kubernetes, and interacting with the k8s API.
#### If you want a similar functionality, you should take a look into the "argocd.argoproj.io/manifest-generate-paths" annotation (https://argo-cd.readthedocs.io/en/release-2.5/operator-manual/high_availability/)


## Description

This projects aims to optimize monorepo setups with ArgoCD by only refreshing the Applications that need to be refreshed.
This is achieved by looking at the files changed in the last commit and determining to which Application they belong.
Currently, it only works with GitHub webhooks.
Working with monorepos is probably not the best idea, however it's quite comfortable for learning projects, such as
my homelab (k3s cluster).

## Getting Started

# THIS PROJECT IS UNDER HEAVY DEVELOPMENTS