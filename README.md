# Folding@Together

Democratizing folding@home (and potentially other networks like rosetta@home)

## Purpose

Though it isn't new, the Folding@Home project allows individuals to donate their computing resources to researchers searching for cures to diseases (like - and including - [COVID-19](https://foldingathome.org/covid19/)). These resources allow researchers to run computationally expensive simulations that illustrate how atoms in a protein move relative to each other, allowing for therapeutic discoveries.

However, there are two big issues preventing more people from helping:

1. Recognition. Many just don't know this software exists.
2. Fear. Downloading software can be daunting and scary. Downloading software that is "stealing" your computation resources is scarier.

### What Folding Together Does

In order to overcome the hurdles of (1) and (2), we democratize folding by allowing anyone to participate via micro-donations. These donations are then used to purchase computation resources on the cloud on the individuals' behalf. To incentivize future donations, we integrate with Facebook to allow the user to share their contribution.

## Technical

![architecture diagram](img/arch-diagram.png)

## High Level Tasks

1. Implementing the backing infrastructure into which computation resources will be provisioned
2. Scheduler to map user contributions to compute resource allocation
3. Registration and payments interface
4. Social recognition and feedback

## Running Deployments
### Deploying Frontend (Registration and Payments)
_Prerequisites_ - In order to deploy, make sure you have [helm](https://helm.sh/) installed and are set up in the AWS Auth configmap to authenticate with the cluster.
```
# upgrade the release
helm upgrade --install frontend-registration-payments -f helm/prod-values.yaml
```
