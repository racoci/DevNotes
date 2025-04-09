**Lesson objective**

In this lesson, you will do the following:

- Explore an example that uses CloudFormation for an Amazon Connect instance deployment.

## Lesson introduction

The common uses of CloudFormation templates in the contact center space revolve around resource and integration deployment and updates. To test use case behaviors, organizations require rapid deployments of contact center environments when developing custom solutions. For example, a developer creates a solution that streams Amazon Connect contact records and agent events. To test, they need a minimal environment deployment to make calls and change states in the contact control panel. CloudFormation creates the resources required to deploy a ready-to-use environment. 

This lesson walks through a CloudFormation template sample deployment. At the end of the lesson, you will have the option to download the template and test it in your own environment.

## Designing your template

Depending on your specific scenario, consider deploying a main template that deploys other nested stacks. Advantages of using nested stacks are as follows:

- Stacks provide convenient downstream maintenance of your deployments. 
- Stacks are straightforward to document and understand by other members of your team. 
- Stacks provide the ability to test modifications without deploying the full infrastructure.
- With nested stacks, developers avoid reaching the CloudFormation service quota of 200 resources per file. For more information, navigate to [Understand CloudFormation Quotas(opens in a new tab)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-limits.html) in the _AWS CloudFormation User Guide_.

Consider a scenario where a small application deploys Lambda functions and two DynamoDB tables. You group the Lambda resources in one template and the tables in another. The main template contains an AWS::CloudFormation::Stack resource for each of the other stacks. If you need an additional Lambda function, by changing only one of the stacks, you reduce the risk of creating errors in the full stack deployment.

The following example illustrates a small application deployment with two stacks.

```
myprojectname_main_v1_0.yml  
myprojectname_functionality01_lambda_v1_0.yml  
myprojectname_functionality01_dynamodb_v1_0.yml
```

When dealing with complex projects, consider using a main template that deploys additional parent templates. Each parent template breaks down the organization of resources based on their functionality. The following example includes stacks for Lambda and DynamoDB nested under a parent stack for the specific functionality01. The parent is a nested stack of the main stack. 

The following code snippet depicts multiple nested stacks.

```
myprojectname_main_v1_0.yml  
myprojectname_functionality01_parent_v1_0.yml  
        myprojectname_functionality01_lambda_v1_0.yml  
        myprojectname_functionality01_dynamodb_v1_0.yml  
        myprojectname_functionality01_apigw_v1_0.yml  
myprojectname_functionality02_parent_v1_0.yml  
        myprojectname_functionality02_lambda_v1_0.yml  
        myprojectname_functionality02_queues_v1_0.yml
```

## Use case

The AnyCompany research and development team needs to deploy development environments for its contact center. To help AnyCompany deploy minimal infrastructure for its test environment, the team typically uses a CloudFormation template. The template must install an Amazon Connect instance and configure the initial parameters, such as call recording storage. It also must include an AWS Key Management Service (AWS KMS) key for encryption. The development team needs a phone number, a test queue, and a test routing profile to simulate agent interactions.
For convenience, the sample template for this course does not use nested stacks.  

### Defining the CloudFormation stack parameters

CloudFormation templates use parameters to refer to values you enter when creating a new stack. This means you have the option to create different stacks using the same CloudFormation template. For example, use the same template to deploy similar contact center resources in more than one AWS Region.  
  
In the following example, the instance alias is a parameter you specify at deployment time. The following syntax depicts how the CloudFormation template defines parameters. With this configuration, the CloudFormation stack displays a field where you specify an alias or unique name for the Amazon Connect instance.

```
Parameters:  
     InstanceAlias:  
          Type: String  
          Description: the alias of the Amazon Connect instance
```

### Creating the Amazon Connect instance

The attribute values specified in this script set the default values for select Amazon Connect settings. Attribute examples include the following:

- **AutoResolveBestVoices** **and** **UseCustomTTSVoices****:** These are configuration settings for the built-in Amazon Polly integration for text-to-speech. 
- **ContactflowLogs****:** This is a global setting that activates the flow log streaming to Amazon CloudWatch for observability.
- **ContactLens****:** This is a global setting that activates conversational analytics for the contact center instance.

The instance alias references the parameter previously defined by the parameters. CloudFormation provides this functionality by using the **!Ref** function in the example. 

The following script depicts the syntax for creating an instance.

```yaml
  
# Create Amazon Connect instance  
      AmazonConnectInstance:  
            Type: AWS::Connect::Instance  
            Properties:  
                  Attributes:  
                        AutoResolveBestVoices: true  
ContactflowLogs: true  
ContactLens: true  
EarlyMedia: true  
InboundCalls: true  
OutboundCalls: true  
UseCustomTTSVoices: false  
IdentityManagementType: CONNECT_MANAGED  
      InstanceAlias: !Ref InstanceAlias
```

### Creating the S3 bucket for Amazon Connect

At creation time, an Amazon Connect instance requires an S3 bucket to store call recordings, chat transcripts, and screen recordings. Properties for the bucket include access configuration settings. 

The following script depicts the declaration of the S3 bucket resource.

```yaml
# S3 Bucket for Amazon Connect call recordings  
      AmazonConnectS3Bucket:  
            Type: AWS::S3::Bucket  
            Properties:  
                  PublicAccessBlockConfiguration:  
                       BlockPublicAcls: true  
                       BlockPublicPolicy: true  
                       IgnorePublicAcls: true  
                       RestrictPublicBuckets: true
```

### Creating the KMS key for data encryption

For secure deployments, the data stored in the S3 bucket requires a KMS key. The Amazon Connect instance uses this key to encrypt data, such as events streamed with Amazon Kinesis or call recordings in Amazon S3. The **Statement** property specifies the AWS Identity and Access Management (IAM) permissions for AWS KMS service access. 

CloudFormation offers string manipulation functions and access to information about the underlying AWS account where the stack runs. The **!Sub** function is used to insert dynamic content within a static string. By using this reference, the stack inserts the ID of the underlying AWS account when creating this resource. 

The following code snippet depicts the property values for the KMS key.

```yaml
# KMS Key  
     AmazonConnectKey:  
         Type: AWS::KMS::Key  
         Properties:  
              Description: KMSKeyForConnect  
              Enabled: true  
              KeyPolicy:  
                    Version: '2012-10-17'  
                    Id: connectkey1  
                    Statement:  
                        - Sid: Enable IAM User Permissions  
                          Effect: Allow  
                          Principal:  
                               AWS: !Sub arn:aws:iam::${AWS::AccountId}:root  
                         Action:  
                              - kms:*  
                         Resource: '*'
```

### Creating associations for the recordings bucket

The following script creates an association between the call recordings resource type and storage configuration for the Amazon Connect instance created with this template. The **S3Config** property specifies the bucket prefix for recordings and the KMS key used for data encryption. Because the template contains the KMS key definition, by using the **!GetAtt** function, the template will access its value during the deployment cycle. 

The following code snippet depicts the syntax for associating recording storage with the instance.

```yaml
# Associate recordings storage for Amazon Connect  
   AmazonConnectStorage:  
         Type: AWS::Connect::InstanceStorageConfig  
         Properties:  
             InstanceArn: !GetAtt AmazonConnectInstance.Arn  
             ResourceType: CALL_RECORDINGS  
             S3Config:  
                  BucketName: !Ref AmazonConnectS3Bucket  
                  BucketPrefix: 'CallRecordings/'  
                  EncryptionConfig:  
                      EncryptionType: KMS  
                      KeyId: !GetAtt AmazonConnectKey.Arn  
             StorageType: S3
```

### Creating a routing profile for agents

The following script creates an agent's routing profile. This routing profile has one queue configured to deliver one voice and a maximum of two chat contacts. The queue has priority 1 and delay 0 for both voice and chat. 

The following code snippet depicts the syntax for this resource.

```yaml
# Create a routing profile for agents  
   AgentRoutingProfile:  
       Type: AWS::Connect::RoutingProfile  
       Properties:  
           AgentAvailabilityTimer: TIME_SINCE_LAST_INBOUND  
           DefaultOutboundQueueArn: !GetAtt Queue.QueueArn  
           Description: Routing profile for agents  
           InstanceArn: !Ref AmazonConnectInstance  
           MediaConcurrencies:  
                 - Channel: VOICE  
                    Concurrency: 1  
                 - Channel: CHAT  
                   Concurrency: 2  
            Name: Agent routing profile  
            QueueConfigs:  
                 - Delay: 0  
                   Priority: 1  
                   QueueReference:  
                        Channel: VOICE  
                        QueueArn: !GetAtt Queue.QueueArn  
                - Delay: 0  
                  Priority: 1  
                 QueueReference:  
                      Channel: CHAT  
                      QueueArn: !GetAtt Queue.QueueArn
```

### Creating hours of operation

The following script creates a resource for hours of operation from Monday to Friday between 8 a.m. and 4 p.m. in the America/New_York time zone. 

The following code snippet depicts the hours of operation configuration values.

```yaml
# Create hours of operation  
   OperatingHours:  
        Type: AWS::Connect::HoursOfOperation  
        Properties:  
            Name: WorkshopHoursOfOperation  
            Description: hours of operation for the development environment  
            InstanceArn: !Ref AmazonConnectInstance  
           TimeZone: America/New_York  
           Config:  
               - Day: MONDAY  
                 StartTime:  
                     Hours: 8  
                     Minutes: 0  
                EndTime:  
                     Hours: 16  
                     Minutes: 0  
              - Day: TUESDAY  
                 StartTime:  
                      Hours: 8  
                     Minutes: 0  
                EndTime:  
                     Hours: 16  
                     Minutes: 0  
             # Add more days as required
```

### Creating a queue

The following script creates a queue and maps the hours of operation configuration to the resource created by the previous statement.

```yaml
  
# Create a queue  
Queue:  
        Type: AWS::Connect::Queue  
        Properties:  
             Description: Queue for sample cfn template  
             HoursOfOperationArn: !GetAtt OperatingHours.HoursOfOperationArn  
             InstanceArn: !GetAtt AmazonConnectInstance.Arn  
             Name: SampleQueue
```

### Claiming a phone number

The following script claims a phone number for direct inward dialing (DID) or a local US phone number. The phone number is associated with the instance.

```yaml
# Claim a phone number  
   PhoneNumber:  
       Type: AWS::Connect::PhoneNumber  
       Properties:  
           CountryCode: US  
           TargetArn: !GetAtt AmazonConnectInstance.Arn  
           Type: DID
```

To find the complete list of Amazon Connect resources, navigate to the [Amazon Connect Resource Type Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html) in the _AWS CloudFormation User Guide_.

### Review the architecture for your stack

The following image represents the architecture deployed by the sample stack you walked through. For further details, select each of the following interactive markers.
![[Diagram of Connect architecture using CloudFormation, additional details located in numbered markers..png]]

### 1 Amazon Connect instance
The CloudFormation template creates an Amazon Connect instance using the alias entered as a parameter.
### 2 Call recordings S3 bucket
The stack deploys an S3 bucket where the Amazon Connect data stores recordings.
### 3 KMS key
To secure the data, the template creates a KMS key for the S3 bucket.
### 4 Amazon Connect queue
The template creates an Amazon Connect queue for contact routing.
### 5 Amazon Connect routing profile
The template creates a routing profile that defines the channels and the priority of the contacts handled by agents.
### 6 Amazon Connect hours of operation
The template creates the hours of operation for the queue.
### 7 Phone number
The template claims a phone number and associates it with the Amazon Connect instance.

## Building and testing the sample solution

To download the YAML file attachment that contains the template sections covered in this lesson, choose anywhere inside the following box.

### [sample.yaml (5.2 KB)](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1741021200/-0k50azYiJRTz-SNjgmvOA/tincan/e919c7c05d382d148757c40e7dcda74625e22a3f/assets/sample.yaml)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Sample Connect Instance Creation CFT
#
# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#=================================================================================================
# Resources created below
#=================================================================================================
Parameters:
  InstanceAlias:
    Type: String
    Description: the alias of the Amazon Connect instance
Resources:
  # Create Amazon Connect instance
  AmazonConnectInstance:
    Type: AWS::Connect::Instance
    Properties:
      Attributes:
        AutoResolveBestVoices: true
        ContactflowLogs: true
        ContactLens: true
        EarlyMedia: true
        InboundCalls: true
        OutboundCalls: true
        UseCustomTTSVoices: false
      IdentityManagementType: CONNECT_MANAGED
      InstanceAlias: !Ref InstanceAlias

  # S3 Bucket for Amazon Connect call recordings
  AmazonConnectS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # KMS Key
  AmazonConnectKey:
    Type: AWS::KMS::Key
    Properties:
      Description: KMSKeyForConnect
      Enabled: true
      KeyPolicy:
        Version: '2012-10-17'
        Id: connectkey1
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub arn:aws:iam::${AWS::AccountId}:root
            Action:
              - kms:*
            Resource: '*'

  # Associate recordings storage for Amazon Connect
  AmazonConnectStorage:
    Type: AWS::Connect::InstanceStorageConfig
    # DependsOn:
    #   - AmazonConnectInstance
    #   - AmazonConnectS3Bucket
    Properties:
      InstanceArn: !GetAtt AmazonConnectInstance.Arn
      ResourceType: CALL_RECORDINGS
      S3Config:
        BucketName: !Ref AmazonConnectS3Bucket
        BucketPrefix: recordings
        EncryptionConfig:
          EncryptionType: KMS
          KeyId: !GetAtt AmazonConnectKey.Arn
      StorageType: S3

  # Create a routing profile for agents
  AgentRoutingProfile:
    Type: AWS::Connect::RoutingProfile
    Properties:
      AgentAvailabilityTimer: TIME_SINCE_LAST_INBOUND
      DefaultOutboundQueueArn: !GetAtt Queue.QueueArn
      Description: Routing profile for agents
      InstanceArn: !Ref AmazonConnectInstance
      MediaConcurrencies:
        - Channel: VOICE
          Concurrency: 1
        - Channel: CHAT
          Concurrency: 2
      Name: Agent routing profile
      QueueConfigs:
        - Delay: 0
          Priority: 1
          QueueReference:
            Channel: VOICE
            QueueArn: !GetAtt Queue.QueueArn
        - Delay: 0
          Priority: 1
          QueueReference:
            Channel: CHAT
            QueueArn: !GetAtt Queue.QueueArn

  # Create hours of operation
  OperatingHours:
    Type: AWS::Connect::HoursOfOperation
    Properties:
      Name: WorkshopHoursOfOperation
      Description: hours of operation for workshop module 3
      InstanceArn: !Ref AmazonConnectInstance
      TimeZone: America/New_York
      Config:
        - Day: MONDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 16
            Minutes: 0
        - Day: TUESDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 16
            Minutes: 0
        - Day: WEDNESDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 16
            Minutes: 0
        - Day: THURSDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 16
            Minutes: 0
        - Day: FRIDAY
          StartTime:
            Hours: 8
            Minutes: 0
          EndTime:
            Hours: 16
            Minutes: 0

  # Claim a phone number
  PhoneNumber:
    Type: AWS::Connect::PhoneNumber
    Properties:
      CountryCode: US
      TargetArn: !GetAtt AmazonConnectInstance.Arn
      Type: DID

  # Create a queue
  Queue:
    Type: AWS::Connect::Queue
    Properties:
      Description: Queue for sample cfn template
      HoursOfOperationArn: !GetAtt OperatingHours.HoursOfOperationArn
      InstanceArn: !GetAtt AmazonConnectInstance.Arn
      Name: SampleQueue
```

---

Use the sample CloudFormation template to create and deploy a new stack. For more information about creating CloudFormation stacks, navigate to [Creating a Stack on the AWS CloudFormation Console(opens in a new tab)](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-console-create-stack.html) in the _AWS CloudFormation User Guide_. You can test and visualize the template by using the AWS Application Composer in the CloudFormation console. In the CloudFormation template, there are two options: _Canvas_ mode, and _Template_ mode. Select each tab to learn more about these modes.

## Canvas Mode
With Application Composer in CloudFormation console mode, you can drag, drop, configure, and connect a variety of resources, called cards, onto a visual canvas. This visual approach you design and edit your application architecture without having to work with templates directly. To access this mode from the CloudFormation console, select Application Composer from the left-side navigation menu. 

  ![[2 app-composer.jpg]]

Now that you have reviewed Canvas mode, move on to the next tab to learn about Template mode.

## Template Mode

By selecting Template mode, you get access to the template script. In this mode, you have access to make further script changes, as needed. Choose the _Validate_ button to confirm that your template is correct. The error details will display at the bottom of the script. In our example, there are no template validation errors.

![[2 app-composer-template.jpg]]After the stack deployment completes successfully, access your environment and test the resources created by the template.

## Check your knowledge

The following section will check your understanding of the content covered in this lesson.

---

AnyCompany has three different contact center environments for development, user acceptance testing, and production. The AnyCompany development team created an AWS CloudFormation template to deploy a custom streaming solution using data generated by Amazon Connect. The team will use this template to update all three environments. The template contains a parameter that identifies the specific deployment environment.  

  

Which statement justifies why the development team selected parameters for their solution deployment?

- CloudFormation templates use parameters to refer to values entered by the user when they create a new stack.

	Correctly selected

- Parameters are used to define the resources created by the CloudFormation template.

	Correctly unselected

- Parameters are used to specify the AWS Region where the resources are deployed.

	Correctly unselected

- Parameters are used to define the order in which CloudFormation template creates the resources.

	Correctly unselected

### Correct

CloudFormation templates use parameters to refer to values entered by the user when they create a new stack. This means that the development team has the option to create different stacks using the same CloudFormation template. For example, the streaming solution will be deployed in each of the three environments by specifying the Amazon Connect instance alias.

## What's next?

In this lesson, you discovered how to build and deploy a CloudFormation template that creates an Amazon Connect instance. Continue to the next lesson to learn how to use AWS CDK for deploying Amazon Connect resources.