## Prompt

I'm trying to create a CI-CD pipeline to use for a project of Infrastructure as Code (IaC). In particular, my first task is to build a jenkins capable of deploying itself.

Initial definitions:
- I have to use Jenkins to deploy infrastructure using terraform.
- I have to use terraform for everything related to IaC
- I have to use aws.
- I have aws-cli/2.16.2 Python/3.11.8 Linux/5.15.0-139-generic exe/x86_64.ubuntu.20
- I don't have access to the aws web console.
- I'm using ubuntu 20.04
- I use python version 3.8.10
- I use Docker version 28.1.1, build 4eba377
- I want the jenkins to run inside a docker on aws so I can test it locally first
- I'm working on a shared bitbucket git repository so I need to track changes for deploy only inside a particular directory and only in some particular branches, but I want this to be configurable
- I want the jenkins docker infrastructure to be managed by job inside the same jenkins so I'll need one of the jobs to be a self-deploy
- I want a full plan and estimation of costs for the whole architecture before any code.
- Use plantuml to do any diagrams
- I need the jenkins to be accessible using a public URL, but I don't have permission to buy any dommain  so we'll have to use some AWS service that provides a public URL by default and I need this URL as one of the outputs of the terraform code
- Every resource created, deployed or updated by this jenkins must include a tag `GE-IaC-STS-CI-CD-Jenkins-2025` and key-value pairs showing the initial created date and last-updated date in the format `2025-09-13 14-03-57.123 UTC` 

Help me build a plan to accomplish all of this and ask me any necessary clarifications. Don't assume anything. I want you to clarify anything I didn't already say before any estimation or plan.

We can do this in steps, so initially, the minimum is to build a Jenkins docker that can be run locally on my configurations and can deploy itself.

The jenkins will also need to have some AWS credentials. I think it's not safe to use my own credentials to do this, but I don't have access to the web console so you'll need to show me just aws cli commands to create those credentials for Jenkins.

## Clarif