## Course summary

In this course, you learned about IaC tools on AWS and their use cases related to Amazon Connect deployments. Review these key concepts in the course summary before taking the course assessment.

### Introduction to IaC for Amazon Connect
    
IaC is the practice of managing and provisioning cloud infrastructure resources through code artifacts and resource definitions instead of manual processes. By adopting an IaC approach, organizations provision, configure, and manage AWS resources, including Amazon Connect resources, in a programmatic and repeatable manner. This approach mitigates deployment risks and streamlines operational processes.

  

The benefits of IaC deployments include the following:

- Capability to automate the creation and management of multiple environments
- Scalability and elasticity
- Version control management
- Cost optimization

### Using CloudFormation for Amazon Connect deployments

CloudFormation makes managing AWS resources more convenient. Users specify the resources they want to create in JSON or YAML templates.  
  
When designing a CloudFormation template, consider using nested stacks to make downstream maintenance more efficient. CloudFormation templates use Description, Parameters, Mappings, Conditions, Resources and Outputs to refer to values entered by the user when creating a new stack. 

  

To test a sample CloudFormation template for an Amazon Connect instance deployment, use a YAML file. Create a new stack using the CloudFormation console or Application Composer, and visualize the template in the Canvas and Template modes. 

  

After the stack deployment is successful, access the environment and test the created output resources.


### Using AWS CDK for Amazon Connect deployments

Amazon Connect workload deployments are part of an organization's CI/CD pipelines. To create an AWS CDK project, you must have the AWS CDK installed in the environment.

  

To create an AWS CDK project, you must do the following:

- Define deployment parameters using CfnParameter resources.
- Import the required constructs.
- Define the resources and associations between resources.

After the deployment is successful, access the new environment and test the created resources.


## Downloadable PDF of the summary

To download a PDF version of the summary section, choose anywhere inside the following box. For the best experience with screen readers, use NVDA or JAWS. If you are using VoiceOver, you might experience issues with the downloaded PDF.

![[4 Amazon Connect Infrastructure as Code Fundamentals Course Summary.pdf]]

## What's next?
In this section, you reviewed concepts related to how IaC tools on AWS help Amazon Connect workload deployments. In the next section, you will assess your knowledge of these concepts.