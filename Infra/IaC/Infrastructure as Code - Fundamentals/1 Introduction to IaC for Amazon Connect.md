# Introduction to IaC for Amazon Connect
**Lesson objectives**

In this lesson, you will do the following:

- Explore the benefits of contact center deployments using Amazon Web Services (AWS) infrastructure as code (IaC) services.
- Explore the advantages and limitations of IaC tools on AWS.
- Identify the best use cases for AWS CloudFormation and the AWS Cloud Development Kit (AWS CDK).

## Lesson introduction

IaC is the practice of managing and provisioning cloud infrastructure resources through code artifacts and resource definitions instead of manual processes. By adopting an IaC approach, organizations can provision, configure, and manage AWS resources, including Amazon Connect resources, in a programmatic and repeatable manner. This approach mitigates deployment risks and streamlines operational processes. Additional benefits of using IaC include the ability to ensure version control, maintain consistency across environments, and scale resources efficiently with repeatable deployment patterns.  
  
The key advantage of using IaC with Amazon Connect is the ability to create and manage multiple environments with consistent, repeatable configuration settings. Examples include sandbox, development, testing, and production contact center environments. IT teams can effortlessly deploy staging environments for evaluating new capabilities, testing contact flows, and integrating with other AWS services.

## Benefits

Organizations use IaC to make the provisioning, configuration, and management of resources more efficient across their AWS environment, which can include Amazon Connect resources for contact center operations.

### Automated infrastructure provisioning

IaC activates the automated provisioning of contact center resources. These resources include third-party application servers, serverless compute applications, storage location, networking configuration, security, and governance resources. Using tools like CloudFormation, developers use code to define the contact center infrastructure. This allows for consistent and repeatable deployments across different contact center environments, such as development, test, or production environments.

### Configuration management

With IaC, organizations deploy resources, such as interactive voice response (IVR), call routing rules and strategy, agent application settings, and application integrations. This strategy ensures standardized deployments with version control that are convenient to reproduce. Contact center configuration managed as code reduces the risk of configuration drift and inconsistencies.

### Scalability and elasticity

Contact centers need scalable and elastic designs to provide business services to customers. For example, during peak call times, administrators must automatically scale up server capacity. Defining infrastructure scaling rules in code automatically adjusts resources based on demand. The dynamic scaling improves performance and cost efficiency.

### High availability and disaster recovery

IaC facilitates the implementation of high availability (HA) and disaster recovery (DR) strategies for contact center infrastructure. Redundant servers, failover mechanisms, backup storage, and recovery procedures are coded and tested in a controlled manner for HA and DR configurations. This ensures rapid recovery in case of failures and minimizes downtime.

### Integration with DevOps practices

IaC aligns with Development Operations (DevOps) practices by promoting collaboration between development and operations teams. Organizations manage infrastructure changes through version control systems, such as Git and Apache Subversion (SVN), allowing for code reviews, automated testing, and continuous integration and continuous deployment (CI/CD) pipelines.  This accelerates the delivery of infrastructure changes and improves overall agility.

### Cost optimization

By codifying infrastructure configurations and using AWS services, IaC helps optimize costs in contact center deployments. IaC dynamically provisions and deprovisions resources based on workload requirements. This approach avoids overprovisioning and minimizes idle or underused resources.

## Exploring IaC tools on AWS

AWS CDK and CloudFormation are IaC tools used to automate the creation of contact center resources. Both tools help achieve operational performance by removing manual provisioning methods like the AWS Management Console or AWS Command Line Interface (AWS CLI). By automating resource deployments, organizations can eliminate potential human errors and increase the speed of deployment.

### Evaluating CloudFormation

CloudFormation makes managing AWS resources more straightforward. With CloudFormation, developers use JSON or YAML templates to specify the AWS resources they want to create or update. They then create CloudFormation stacks from these templates. When the AWS architecture is no longer needed, developers remove the resources by deleting the stack that created them.  
  
CloudFormation templates provide the ability to create instances and other resources, such as users, quick connects, and contact flows. For more information, navigate to [Amazon Connect Resource Type Reference(opens in a new tab)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html) in the _AWS CloudFormation User Guide_. The following will outline the advantages and limitations of using CloudFormation templates.


#### Advantages
The following are advantages of using CloudFormation:

- **Accessibility:** JSON and YAML are user-friendly formats and markup languages. 
- **Standardization:** With the CloudFormation specification, developers can define resources in templates. They can then use templates to create or update stacks.
- **Reusability:** Developers reuse existing CloudFormation templates to create similar stacks and conveniently replicate AWS architectures. For example, they use the same template to create development, test, and production environments. CloudFormation increases the reusability of the templates with the use of parameters, mappings, and conditions.
- **Extensibility:** CloudFormation templates support custom resources. With custom resources, developers have the option to extend resource deployment and update deployment capabilities.
- **Error handling:** CloudFormation can automatically roll back the resources when errors occur. This approach provides a fast, secure, and reliable mechanism for handling failures.
- **Integration with AWS developer tools:** The integration with AWS CodePipeline offers access to CI/CD pipelines. 
- **Extensive documentation:** CloudFormation offers comprehensive documentation for AWS resources and property type references.

Now that you have reviewed the advantages, move on to the next tab to learn about the limitations.

#### Limitations
The following are limitations of CloudFormation templates:

- **No-code:** Although JSON or YAML are straightforward to learn, developers cannot use common programming languages to control the deployment flow. A deep understanding of specific CloudFormation concepts is necessary to achieve complex outcomes with custom resources.
- **No abstraction:** Object-oriented programming offers the advantage of setting standards for resources or groups of resources. Without this capability, resources require a detailed definition in a declarative manner.
- **Deep knowledge of AWS resources:** Developers writing CloudFormation templates need a deep understanding of each of the resources included in the template.

Now that you've explored advantages and limitations of using CloudFormation, move on to the next section of the lesson.


### Evaluating the AWS CDK

The AWS CDK is an open-source software development framework for defining cloud infrastructure as code and provisioning it through CloudFormation. With AWS CDK, developers write infrastructure code in common programming languages, like Python, JavaScript, TypeScript, C#, Go, or Java. The following will outline the advantages and limitations of using AWS CDK.

#### Advantages
The following are advantages of using the AWS CDK:

- **Provides reliability and security:** AWS CDK uses CloudFormation templates and stacks to deploy the code. This means organizations continue to benefit from the reliability and security CloudFormation provides.
- **Offers programming language support:** Instead of JSON and YAML, developers use AWS CDK libraries in the programming language of their choice. This provides control flow tools and efficient IaC code writing.
- **Provides abstraction:** Developers use object-oriented programming languages like Python in AWS CDK to define methods or classes to modularize code. AWS CDK provides classes for multiple AWS resource types.
- **Does not require deep **knowledge of** AWS resources:** The AWS CDK classes provide defaults based on common scenarios and security best practices. 
- **Handles complex deployments:** With AWS CDK, developers have the option to create multiple stacks in an AWS CDK app. They can then pass values between stacks by using input parameters and instance attributes.
- **Expands the CloudFormation capabilities:** The AWS Construct Library provides features to enhance the capabilities of CloudFormation. For example, developers using CloudFormation cannot delete an Amazon Simple Storage Service (Amazon S3) bucket that contains any objects. This action results in a stack deletion error when attempted with a CloudFormation template. With AWS CDK, by setting a Boolean property to _true_ on the S3 bucket resources, developers remove the S3 bucket with full content.

Now that you have reviewed the advantages, move on to the next tab to learn about the limitations.

#### Limitations
The following are limitations of the AWS CDK:

- **Dependency on CloudFormation quotas:** AWS CDK generates JSON CloudFormation templates from AWS CDK code and uses the templates to launch CloudFormation stacks to deploy AWS resources. Therefore, AWS CDK depends on the CloudFormation set limits.
- **Code sharing:** CloudFormation templates are reusable for new stacks. With AWS CDK, each stack has its own template. Developers share the code as packages or libraries for each specific programming language.

Now that you've explored advantages and limitations of AWS CDK, move on to the next section of the lesson.

## Selecting the right IaC tool for the right use case

Based on the advantages and limitations of the two IaC services on AWS, here are recommendations about how to decide on the right tool for deployments. Use only one tool or a combination of both tools to manage the deployment of the solution that solves for specific business use cases. The following will outline the recommendations of using the right IaC tool.

### Cloud Formation
Use CloudFormation for the following use cases:

- **Basic instance deployment:** This involves setting up the initial Amazon Connect instance with basic components like queues, prompts, and AWS Lambda functions. CloudFormation makes standing up a core contact center instance more efficient.
- **Updates to existing resources:** This involves changing existing resources, such as adding a new queue or Lambda function. The CloudFormation update workflows are reliable.
- **Light programming skill requirements:** If you prefer declarative YAML or JSON syntax over programming languages use CloudFormation to deploy basic architectures.  
    

Now that you have reviewed CloudFormation, move on to the next tab to learn about AWS CDK.

###   AWS CDK

Use AWS CDK for the following use cases:

- **Complex deployments:** This involves building complex contact flows and call logic with interdependent components. The AWS CDK abstraction capabilities make these deployments possible.
- **Frequent iteration and testing changes:** More efficient deployments in AWS CDK help with agile workflows, especially in development environments.
- **Amazon Connect integrations:** The flexibility of Amazon Connect to integrate with other AWS services, such as Lambda, Amazon DynamoDB, or AWS AppSync, renders complex architectural solutions.
- **Developer friendly tools:** Developers who are comfortable with TypeScript, Python, or Java use their preferred language to create AWS CDK constructs and applications.
- **Shared contact center components:** AWS CDK construct models make it more efficient to build reusable contact center components that are shared across multiple instances.
- **CI/CD pipeline facilitation:** AWS CDK projects are application code bases. This facilitates the integration of contact center deployments into existing CI/CD pipelines.

Now that you've explored use cases for CloudFormation and AWS CDK, move on to the next section of the lesson.


## Sample use cases

- ## Sample use case for CloudFormation
    
    A company wants to deploy a standardized infrastructure setup for Amazon Connect. This company needs multiple contact center instances and AWS resources dedicated to specific lines of business. Although they are identical in build, each business unit uses its own deployment. The business units require strict version control, auditability, and reproducibility in their specific deployments.

- ### Reasons for selecting CloudFormation
    
    CloudFormation provides the following benefits:
    
    - **Declarative template management:** Use the CloudFormation declarative approach for precise control over resource configurations. This approach is ideal for managing complex infrastructures.
    - **Version control and rollbacks:** Track changes, rollback versions, and collaboration using version-control CloudFormation templates with GitHub or GitLab. 
    - **Auditability and compliance:** CloudFormation provides an audit trail of infrastructure changes. Demonstrate compliance with regulations and policies.

- ## Sample use case for AWS CDK
    
    To implement a serverless application architecture, the AnyCompany Insurance development team needs to use Lambda, Amazon API Gateway, DynamoDB, and Amazon S3. These services are a part of an integration solution with Amazon Connect. The AWS resources require dynamic configurations, code reusability, and integration with existing development workflows.

- ### Reasons for selecting AWS CDK
    
    AWS CDK provides the following benefits:
    
    - **High-level abstraction:** With AWS CDK, developers define and efficiently manage serverless components using high-level constructs for AWS resources. This approach reduces the code complexity.
    - **Standardization:** AWS CDK provides the ability to create reusable constructs and libraries. This approach promotes code reusability, modularity, and consistency across projects.
    - **Integration with development tools:** AWS CDK seamlessly integrates with integrated development environments (IDEs), code editors, and development workflows. It uses features like code completion, error checking, and documentation for enhanced productivity.
    - **Dynamic configuration:** With AWS CDK, developers use programming constructs like loops, conditions, and functions for dynamic configurations.

## Check your knowledge

The following section will check your understanding of the content covered in this lesson.

An organization is evaluating the use of AWS CloudFormation for its contact center deployment. What is a limitation of using CloudFormation templates?  

#### Limited integration with AWS developer tools

Correctly unselected

#### Inability to handle failures during resource deployment

Correctly unselected

#### Lack of programming language support for writing templates

Correctly selected

#### Insufficient extensibility for custom resource deployment

Correctly unselected
 

### Correct

---
Developers must use JSON or YAML to define resources and cannot use common programming languages to control the deployment flow.


A contact center development team needs to implement a serverless application architecture involving AWS Lambda, Amazon API Gateway, Amazon DynamoDB, and Amazon S3 for integration with Amazon Connect. Which infrastructure as code (IaC) tool should the team use?

#### AWS CloudFormation because it provides standardization and reusability of templates

Correctly unselected

AWS Cloud Development Kit (AWS CDK) because it offers programming language support and high-level abstraction

Correctly selected

#### AWS CloudFormation because it has a deep knowledge of AWS resources

Correctly unselected

#### AWS Cloud Development Kit (AWS CDK) because it has no dependency on AWS CloudFormation quotas

Correctly unselected

### Correct

With AWS CDK, developers can define and efficiently manage serverless components using high-level constructs for AWS resources.

---

A company wants to automate the provisioning of multiple contact center environments across multiple lines of business. The deployments include third-party application servers, serverless compute applications, storage locations, and security resources. Which benefit of the infrastructure as code (IaC) approach is relevant in this scenario?

#### Configuration management

Correctly unselected

#### Automated infrastructure provisioning

Correctly selected

#### Scalability and elasticity

Correctly unselected

#### Integration with Development Operations (DevOps) practices

Correctly unselected


### Correct

In infrastructure provisioning, automatic provisioning streamlines the creation of required resources and their configuration.