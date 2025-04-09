## Lesson objective

In this lesson, you will do the following:

- Explore a sample use case that uses an AWS CDK application for an Amazon Connect contact center workload.
## Lesson introduction

Amazon Connect workload deployment can be part of an organization's CI/CD pipeline. Rapid deployment of complex infrastructure facilitates the research and development of new features and capabilities. Developers can build and test behaviors related to the use case they are solving. 

This lesson walks through an AWS CDK sample template built to deploy typical contact center workload resources. At the end of the lesson, you will have the option to download the template and test it in your own environment.

## Creating the AWS CDK project

Creating a new AWS CDK project requires the AWS CDK environment to be installed in your development environment. For instructions and prerequisites for installing the latest version of the AWS CDK, navigate to [Getting Started with the AWS CDK(opens in a new tab)](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html). After installation, you must confirm the version by running the following command in the AWS CDK Command Line Interface (CLI) command cdk.

```bash
cdk version
```

For a successfully installed AWS CDK, the command displays the version. It also informs you if newer versions are available. In the following example, the AWS CDK version is not the latest version that is available, and the system recommends an upgrade. 

The following snippet depicts the result after running the **cdk version** command.

```
2.130.0 (build bd6e5ee)  
**************************************************************  
*** Newer version of CDK is available [2.149.0] *********  
*** Upgrade recommended (npm install -g aws-cdk) ***  
**************************************************************
```

It is important to ensure that the installed version of the AWS CDK is current. New versions include new constructs that can only be used when the AWS CDK version is up to date. Release notes for the AWS CDK can be found in the Releases section of the AWS CDK GitHub repository.

After the AWS CDK is installed and up to date, you can create a new AWS CDK project in your environment by running the **cdk init app** command. Before running this command, you need to ensure that your command line runs from a new folder. This folder is where the files related to your AWS CDK project reside.

The AWS CDK supports various programming languages to accommodate developer preferences and existing technology stacks. For example, you can develop AWS CDK applications in plain JavaScript, TypeScript, or Go. When creating a new AWS CDK application, you need to specify the language to use by using the **--language** parameter. Run the **mkdir** command to create a new folder and the **cd** command to navigate to it. Then, create a new TypeScript AWS CDK project by using **cdk init app** command and specifying the language. 

The following code snippet depicts how to accomplish these three steps.

```bash
mkdir iac-fundamentals && cd iac-fundamentals  
cdk init app --language typescript
```
By running this command, the AWS CDK creates a new project from the application template, and your terminal provides feedback about the progress. In the feedback, review the **## Useful commands** section. This section provides a list of Node Package Manager (npm) commands that you will use at various stages of the development. 

When the project is initialized, the following message will display.

```
✅ All done!
```

The new AWS CDK application has the following folder structure.
```
iac-100  
├── README.md  
├── bin  
│ └── iac-100.ts  
├── cdk.json  
├── jest.config.js  
├── lib  
│ └── iac-100-stack.ts  
├── node_modules  
├── package-lock.json  
├── package.json  
├── test  
│ └── iac-100.test.ts  
└── tsconfig.json
```

An AWS CDK project contains multiple files and folders, which depend on the language selected. For a TypeScript project, the files controlling which AWS resources the application deploys are the .ts files in the bin folder and in the lib folder. At a high level, you will run the content of the bin folder to provision resources in the environment. The lib folder contains the definition for the resources.  
  
To add new resources, you must add them to the .ts file inside the lib folder. For convenience, this lesson covers a basic deployment without nested stacks. The TypeScript .ts file contains the necessary resources for this deployment.

Initializing a new AWS CDK application creates the following file in the lib folder. This template describes how to declare new resources.

```js
  
import * as cdk from 'aws-cdk-lib';  
import { Construct } from 'constructs';  
// import * as sqs from 'aws-cdk-lib/aws-sqs';  
  
export class Iac100Stack extends cdk.Stack {  
     constructor(scope: Construct, id: string, props?: cdk.StackProps) {  
          super(scope, id, props);  
  
          // The code that defines your stack goes here  
  
         // example resource  
         // const queue = new sqs.Queue(this, 'Iac100Queue', {  
         // visibilityTimeout: cdk.Duration.seconds(300)  
        // });  
     }  
}
```

You must update this file to include the Amazon Connect resources related to your contact center workload.  
  
Constructs are the basic building blocks of AWS CDK applications. A construct is a component in an application that represents one or more CloudFormation resources and their configuration. You build your application, piece by piece, by importing and configuring constructs.

## Use case

[(opens in a new tab)](https://aws.amazon.com/compliance/shared-responsibility-model/)[(opens in a new tab)](https://docs.aws.amazon.com/connect/latest/adminguide/compliance-validation-best-practices-PII.html)The AnyCompany Bank development team wants to deploy a development environment to build a custom reporting and analytics solution for the company's contact center. The solution requires an Amazon Connect instance with minimal operational configuration and uses the data streaming capabilities of Amazon Connect. It captures contact records and agent events published on Amazon Kinesis Data Streams. It then processes the events using Lambda functions. The team uses a CI/CD pipeline to control the deployment. The team is exploring using the AWS CDK to facilitate the on-demand creation of the required base environment.

### Defining the deployment parameters

Amazon Connect instances require a unique alias at creation time. The effective way to define deployment parameters with AWS CDK is to use a CfnParameter resource. This resource helps define the parameters required when deploying the AWS CDK application. To declare a new CfnParameter resource, you must import the construct from the basic AWS CDK library. 

The following code snippet depicts how to perform this action.

```js
import * as cdk from 'aws-cdk-lib';
```

The creation of the AWS CDK application automatically imports the aws-cdk-lib library. 

The following snippet depicts how to create a new **CfnParameter** resource to define the **instanceAliasParameter**.

```js
// Create an input parameter for the instance alias  
const instanceAliasParameter = new cdk.CfnParameter(this, 'instanceAlias', {  
        type: 'String',  
        description: 'The alias for the Amazon Connect instance'  
});
```

### Defining the workload resources

[(opens in a new tab)](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege)Because the majority of the components that need deploying are Amazon Connect resources, you must import the **aws-connect** library. In TypeScript, you import new constructs by using the **import** statement. To reference this construct further, you will use the **connect** object. 

The following snippet depicts how to import the Amazon Connect construct.

```js
import * as connect from 'aws-cdk-lib/aws-connect';
```

Based on the project requirements, you will also need other types of resources, defined in different constructs. Examples include **aws-s3**, **aws-kms**, or **aws-kinesis**. 

The following snippet depicts statements to help define the required resources for the sample workload.

```js
import * as s3 from 'aws-cdk-lib/aws-s3';  
import * as kms from 'aws-cdk-lib/aws-kms';  
import * as kinesis from 'aws-cdk-lib/aws-kinesis';  
import * as lambda from 'aws-cdk-lib/aws-lambda';  
import { KinesisEventSource } from 'aws-cdk-lib/aws-lambda-event-sources';  
import { Construct } from 'constructs';
```

### Defining the Amazon Connect instance

The object specified in the last parameter of the constructor sets the initial values for the instance configuration. The stack uses the **instanceAlias** parameter value provided during deployment for the instance alias property.

The following snippet details the required syntax to define an Amazon Connect instance.

```js
// Create an Amazon Connect instance  
const connectInstance = new connect.CfnInstance(this, 'ConnectInstance', {  
        instanceAlias: instanceAliasParameter.valueAsString,  
        identityManagementType: 'CONNECT_MANAGED',  
        attributes: {  
              inboundCalls: true,  
              outboundCalls: true,  
  
             // the properties below are optional  
             autoResolveBestVoices: true,  
             contactflowLogs: true,  
             contactLens: true,  
             earlyMedia: true,  
             useCustomTtsVoices: false,  
        }  
});
```

### Defining the KMS key for data encryption

For secure deployments, the data stored in the S3 bucket requires a KMS key. The Amazon Connect instance uses this key to encrypt data, such as events streamed with Kinesis or call recordings in Amazon S3. 

The following snipped depicts how to create a KMS key.

```js
// Create a KMS key for encryption  
const encryptionKey = new kms.Key(this, 'ConnectEncryptionKey', {  
     description: 'KMS key for Amazon Connect instance and S3 bucket',  
     enableKeyRotation: true,  
});
```

### Defining the S3 bucket for Amazon Connect

An Amazon Connect instance requires an S3 bucket to store call recordings, chat transcripts, and screen recordings. The following script depicts the declaration of the S3 bucket resource. Properties for the bucket include access configuration settings. The **encryptionKey** property dynamically uses the previously defined KMS key resource.

```js
// Create an S3 bucket for Connect instance storage  
const connectStorageBucket = new s3.Bucket(this, 'ConnectStorageBucket', {  
      bucketName: instanceAliasParameter.valueAsString + '-storage-bucket',  
      encryption: s3.BucketEncryption.KMS,  
      encryptionKey: encryptionKey,  
      removalPolicy: cdk.RemovalPolicy.RETAIN,  
      autoDeleteObjects: false,  
});
```

### Defining associations for the call recordings bucket

The following definition establishes an association between the call recordings resource type and the storage configuration for the Amazon Connect instance created with this template. The **S3Config** property specifies the bucket prefix for recordings and the KMS key used for data encryption. The value for the S3 bucket name and the KMS key to use dynamic references to the resources defined previously, similar to previous steps.

```js
// create the storage configuration for call recordings  
const callRecordingsStorageConfig = new connect.CfnInstanceStorageConfig(this, 'CallRecordingsStorageConfig', {  
       instanceArn: connectInstance.attrArn,  
       resourceType: 'CALL_RECORDINGS',  
       storageType: 'S3',  
       s3Config: {  
       bucketName: connectStorageBucket.bucketName,  
       bucketPrefix: 'recordings/',  
       encryptionConfig: {  
               encryptionType: 'KMS',  
               keyId: encryptionKey.keyArn  
       },  
       },  
});
```

### Defining the Kinesis Data Streams and creating the Amazon Connect associations

Amazon Connect publishes agent and contact records events using Kinesis Data Streams. The AWS CDK stack defines streams and associates them with the Amazon Connect instance. 

The following snippet depicts how to define a contact records stream and an agent event stream with their respective storage configurations.

```js
const contactRecordsStream = new kinesis.Stream(this, 'ContactRecordsStream', {  
       streamName: 'connect-contact-records-stream',  
       encryption: kinesis.StreamEncryption.KMS,  
       encryptionKey: encryptionKey,  
});  
  
const agentEventsStream = new kinesis.Stream(this, 'AgentEventsStream', {  
       streamName: 'connect-agent-events-stream',  
       encryption: kinesis.StreamEncryption.KMS,  
       encryptionKey: encryptionKey,  
});  
  
// create the storage configuration for contact records  
const contactRecordsStorageConfig = new connect.CfnInstanceStorageConfig(this, 'ContactRecordsStorageConfig', {  
        instanceArn: connectInstance.attrArn,  
        resourceType: 'CONTACT_TRACE_RECORDS',  
        storageType: 'KINESIS_STREAM',  
        kinesisStreamConfig: {  
        streamArn: contactRecordsStream.streamArn  
        }  
});  
  
// create the storage configuration for agent events  
const agentEventsStorageConfig = new connect.CfnInstanceStorageConfig(this, 'AgentEventsStorageConfig', {  
         instanceArn: connectInstance.attrArn,  
        resourceType: 'AGENT_EVENTS',  
        storageType: 'KINESIS_STREAM',  
        kinesisStreamConfig: {  
        streamArn: agentEventsStream.streamArn  
        }  
});
```

### Defining the Lambda function resources

To define the Lambda functions required to process the contact records and the agent events, AWS CDK offers a Lambda construct called lambda.Code. Although the stack uses the construct, the Lambda functions code resides in a **lambdas** folder created as part of this application. 

The following snippet depicts an example of how to declare the two functions.

```js
// Create Lambda functions to process contact records and agent events  
const contactRecordProcessLambda = new lambda.Function(this, 'ContactRecordProcessLambda', {  
       functionName: this.stackName + '-connect-contact-record-process-lambda',  
       runtime: lambda.Runtime.NODEJS_20_X,  
       code: lambda.Code.fromAsset('lambdas'),  
       handler: 'contactRecordsProcess.handler',  
});  
  
const agentEventsProcessLambda = new lambda.Function(this, 'AgentEventsProcessLambda', {  
       functionName: this.stackName + '-connect-agent-events-process-lambda',  
       runtime: lambda.Runtime.NODEJS_20_X,  
       code: lambda.Code.fromAsset('lambdas'),  
       handler: 'agentEventsProcess.handler',  
});
```
### Defining the Kinesis activation of Lambda functions

Lambda functions run when Kinesis source events get published. AWS CDK uses the **addEventSource** method to associate the Kinesis event publication with the Lambda activated by that event. 

The following code snippet showcases the use of this method for both event streams: contact records and agent event processing.

```js
// Associate relevant Kinesis triggers to each Lambda function  
contactRecordProcessLambda.addEventSource(new KinesisEventSource(contactRecordsStream, {  
       batchSize: 1, // default  
       startingPosition: lambda.StartingPosition.TRIM_HORIZON  
}));  
  
agentEventsProcessLambda.addEventSource(new KinesisEventSource(agentEventsStream, {  
        batchSize: 1, // default  
        startingPosition: lambda.StartingPosition.TRIM_HORIZON  
}));
```

### Defining output information for the AWS CDK application

At the core, AWS CDK deploys a CloudFormation template. Using this functionality, developers have access to display output values when the stack deployment completes successfully. To display output values, the developers use the CfnOutput method. 

The following snippet depicts how to define three output values: the Amazon Connect instance Amazon Resource Name (ARN), the S3 bucket name, and the KMS key ARN.

```js
// Output the Connect instance ARN, S3 bucket name, and KMS key ARN  
new cdk.CfnOutput(this, 'ConnectInstanceArn', {  
        value: connectInstance.attrArn,  
        description: 'Amazon Connect Instance ARN',  
});  
  
new cdk.CfnOutput(this, 'ConnectStorageBucketName', {  
        value: connectStorageBucket.bucketName,  
        description: 'Amazon Connect Storage Bucket Name',  
});  
  
new cdk.CfnOutput(this, 'EncryptionKeyArn', {  
        value: encryptionKey.keyArn,  
        description: 'KMS Key ARN for encryption',  
});
```

For a complete list of AWS CDK constructs, navigate to [AWS CDK Reference Documentation(opens in a new tab)](https://docs.aws.amazon.com/cdk/api/v2/). This site contains the available Amazon Connect constructs and the constructs available for the AWS resources supported by the AWS CDK.

## Building and testing the sample solution

Test the deployment of the sample solution using the following four steps: 

1. Download and extract the sample application code.
2. Install and build the AWS CDK application.
3. Deploy the sample contact center.
4. Test the resources created by the application.

### Step 1: Download the sample application

To download the file attachment that contains the full sample for the application created in this lesson, choose anywhere inside the following box. Then, extract the contents of the archive file.
![[3 - iac-100.zip]]

### Step 2: Install and build the application code

Using a command line in your environment, install and build the code. The following snippet depicts the command to run.
```bash
npm install && npm run build
```

### Step 3: Deploy a sample contact center

Use the following command to deploy the application in your AWS environment. 

The **cdk** **deploy** command performs the following actions:

- Generates the corresponding CloudFormation template for this application
- Deploys the CloudFormation template

The following code snippet showcases the **cdk deploy** command.

```bash
cdk deploy --parameters instanceAlias=<enter an alias for the instance>
```

### Step 4: Test the resources

After the stack deployment is complete and successful, access your environment, and test the resources created by the application.

## Check your knowledge

The following section will check your understanding of the content covered in this lesson.

---
A developer wants to deploy an Amazon Connect contact center test environment using the AWS Cloud Development Kit (AWS CDK). The developer needs to define a unique alias for the Amazon Connect instance during deployment. 

  

Which AWS CDK construct provides this functionality? 
#### CfnResource
Correctly unselected
#### CfnParameter
**Correctly selected**

#### CfnMapping
Correctly unselected

#### CfnCondition
Correctly unselected

### Correct

The effective way to define deployment parameters with AWS CDK is to use create a CfnParameter resource.

---

A development team needs to create an AWS Lambda function to process the contact records events streamed from the Amazon Connect instance. Which AWS Cloud Development Kit (AWS CDK) construct must the team use to define the Lambda function? 

#### lambda.Function
Correctly unselected
#### lambda.Code 
**Correctly selected**

#### lambda.Runtime 
Correctly unselected

#### lambda.EventSource 
Correctly unselected

### Correct
To define a Lambda function, AWS CDK offers a Lambda construct that reads assets from the AWS CDK project. The construct is lambda.Code. Although the AWS CDK stack uses the construct, the Lambda function code is stored in a lambdas folder created as part of the AWS CDK application.

---

## What's next?

In this lesson, you learned the fundamentals of using AWS CDK to deploy and manage Amazon Connect workloads. Continue to the next lesson to review the course summary and prepare for the end-of-course assessment.
