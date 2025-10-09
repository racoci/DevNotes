# Question 1
A software company has a globally distributed team of developers, that requires secure and compliant access to AWS environments. The company manages multiple AWS accounts under AWS Organizations and uses an on-premises Microsoft Active Directory for user authentication. To simplify access control and identity governance across projects and accounts, the company wants a centrally managed solution that integrates with their existing infrastructure. The solution should require the least amount of ongoing operational management.

Which approach best meets the company’s requirements?

- Deploy AWS Directory Service for Microsoft Active Directory in AWS. Establish a trust relationship with the on-premises Active Directory. Use IAM roles linked to AD groups to control access to AWS resources.

- Use AWS Directory Service AD Connector to connect AWS to the on-premises Active Directory. Integrate AD Connector with AWS IAM Identity Center. Use permission sets to assign access to AWS accounts and resources based on Active Directory group membership.

- Deploy an open-source identity provider (IdP) on Amazon EC2. Synchronize it with the on-premises Active Directory and use SAML to federate access to AWS accounts. Assign IAM roles to federated users based on SAML assertions.

- Use AWS Control Tower to enable account access for developers. Create AWS IAM roles in each member account and manually assign permissions. Instruct developers to assume roles across accounts using the AWS CLI.

Answer: **Use AWS Directory Service AD Connector to connect AWS to the on-premises Active Directory.** **Integrate AD Connector with AWS IAM Identity Center.** **Use permission sets to assign access to AWS accounts and resources based on Active Directory group membership**

The problem describes a company that needs to integrate its on-premises Microsoft Active Directory with multiple AWS accounts, while also simplifying access management and minimizing operational overhead. The best solution is to use AWS Directory Service AD Connector with AWS IAM Identity Center.

- **AWS Directory Service AD Connector** allows AWS to connect to the existing on-premises Active Directory without syncing or replicating any user data to the cloud. This maintains the on-premises directory as the single source of truth for user identities.
- **AWS IAM Identity Center** (formerly AWS Single Sign-On) provides a centralized way to manage access to multiple AWS accounts and applications. It can be integrated with AD Connector to grant users access based on their existing Active Directory group memberships.
- **Permission sets** in IAM Identity Center define the permissions that users get when they access an AWS account. By assigning these permission sets to Active Directory groups, the company can centrally manage access for all developers, simplifying identity governance and reducing the need for manual configuration in each individual AWS account.

This approach meets all the company's requirements by providing a centrally managed, secure, and compliant solution with the least amount of ongoing operational management.
# Question 2
A major bank is using Amazon Simple Queue Service (Amazon SQS) to migrate several core banking applications to the cloud to ensure high availability and cost efficiency while simplifying administrative complexity and overhead. The development team at the bank expects a peak rate of about 1000 messages per second to be processed via SQS. It is important that the messages are processed in order.

Which of the following options can be used to implement this system?

- Use Amazon SQS FIFO (First-In-First-Out) queue in batch mode of 2 messages per operation to process the messages at the peak rate.
- Use Amazon SQS FIFO (First-In-First-Out) queue in batch mode of 4 messages per operation to process the messages at the peak rate.
- Use Amazon SQS FIFO (First-In-First-Out) queue to process the messages.
- Use Amazon SQS standard queue to process the messages.

Answer: **Use Amazon SQS FIFO (First-In-First-Out) queue in batch mode of 4 messages per operation to process the messages at the peak rate**

Explanation

The problem states that the messages must be processed in order, which requires an Amazon SQS FIFO (First-In-First-Out) queue. Standard queues do not guarantee the order of messages.

An Amazon SQS FIFO queue can process up to 300 messages per second. The problem requires processing a peak rate of 1000 messages per second. To achieve this, messages must be processed in batches. Each batch operation can process up to 10 messages.

To process 1000 messages per second, you can calculate the required batch size:

![](data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==)

1000 messages/sec300 messages/sec≈3.33 batchesthe fraction with numerator 1000 messages/sec and denominator 300 messages/sec end-fraction is approximately equal to 3.33 batches

1000 messages/sec300 messages/sec≈3.33 batches

Since you cannot have a fraction of a batch, you must round up to the next whole number, which is 4. Therefore, each batch must contain a minimum of 4 messages to process 1000 messages per second.
# Question 3:

A government agency is developing a online application to assist users in submitting permit requests through a web-based interface. The system architecture consists of a front-end web application tier and a background processing tier that handles the validation and submission of the forms. The application is expected to see high traffic and it must ensure that every submitted request is processed exactly once, with no loss of data.

Which design choice best satisfies these requirements?

- Leverage Amazon EventBridge to send events from the web application to the processing tier for asynchronous form handling
- Implement an Amazon SQS standard queue to reliably buffer and deliver form submissions from the web application layer to the processing tier
- Leverage Amazon API Gateway to pass the form submissions to AWS Lambda for processing in real time
- Implement an Amazon SQS FIFO queue to reliably buffer and deliver form submissions from the web application layer to the processing tier

Answer: **Implement an Amazon SQS FIFO queue to reliably buffer and deliver form submissions from the web application layer to the processing tier**

The problem states that the application must ensure "every submitted request is processed exactly once, with no loss of data." Amazon SQS FIFO (First-In, First-Out) queues are designed to handle this exact requirement. Unlike standard SQS queues, which offer "at least once" delivery and can sometimes deliver messages out of order, FIFO queues guarantee that messages are processed exactly once and in the same order they were sent. This makes them the ideal choice for scenarios where the order of operations and the prevention of duplicate processing are critical.
# Question 4:

A new DevOps engineer has just joined a development team and wants to understand the replication capabilities for Amazon RDS Multi-AZ deployment as well as Amazon RDS Read-replicas.

Which of the following correctly summarizes these capabilities for the given database?

A new DevOps engineer has just joined a development team and wants to understand the replication capabilities for Amazon RDS Multi-AZ deployment as well as Amazon RDS Read-replicas.
Which of the following correctly summarizes these capabilities for the given database?

- Multi-AZ follows synchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow asynchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans one Availability Zone (AZ) within a single region. Read replicas follow synchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow synchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow asynchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region

Answer: **Multi-AZ follows synchronous replication and spans at least two Availability Zones (AZs) within a single region.** **Read replicas follow asynchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region**

Amazon RDS Multi-AZ deployments provide high availability by synchronously replicating data to a standby instance in a different Availability Zone (AZ) within the same region. This ensures that in the event of an outage, a failover can occur with minimal data loss.

In contrast, Amazon RDS Read Replicas are used to increase read throughput and can be located in the same AZ, a different AZ, or even a different region. They use asynchronous replication, which means there can be a slight delay between the primary instance and the replica.
# Question 5:

One of the biggest football leagues in Europe has granted the distribution rights for live streaming its matches in the USA to a silicon valley based streaming services company. As per the terms of distribution, the company must make sure that only users from the USA are able to live stream the matches on their platform. Users from other countries in the world must be denied access to these live-streamed matches.

Which of the following options would allow the company to enforce these streaming restrictions? (Select two)

Question 5:
One of the biggest football leagues in Europe has granted the distribution rights for live streaming its matches in the USA to a silicon valley based streaming services company. As per the terms of distribution, the company must make sure that only users from the USA are able to live stream the matches on their platform. Users from other countries in the world must be denied access to these live-streamed matches.
Which of the following options would allow the company to enforce these streaming restrictions? (Select two)
Use georestriction to prevent users in specific geographic locations from accessing content that you're distributing through a Amazon CloudFront web distribution
Use Amazon Route 53 based failover routing policy to restrict distribution of content to only the locations in which you have distribution rights
Use Amazon Route 53 based latency-based routing policy to restrict distribution of content to only the locations in which you have distribution rights
Use Amazon Route 53 based weighted routing policy to restrict distribution of content to only the locations in which you have distribution rights
Use Amazon Route 53 based geolocation routing policy to restrict distribution of content to only the locations in which you have distribution rights

Answer: The correct options are:

- **Use georestriction to prevent users in specific geographic locations from accessing content that you're distributing through an Amazon CloudFront web distribution**
- **Use Amazon Route 53 based geolocation routing policy to restrict distribution of content to only the locations in which you have distribution rights**

Explanation

- **Georestriction with Amazon CloudFront:** Amazon CloudFront is a content delivery network (CDN). One of its features is georestriction, which allows you to restrict access to your content based on the geographic location of the user. This directly addresses the problem of allowing users in the USA while denying access to users from other countries.
- **Geolocation routing policy with Amazon Route 53:** Amazon Route 53 is a DNS web service. A geolocation routing policy allows you to route traffic to specific resources based on the geographic location of your users. This can be used to direct traffic from allowed locations (like the USA) to the streaming service's content, while directing traffic from other locations to a different resource or denying access.

# Question 6:
A healthcare analytics company centralizes clinical and operational datasets in an Amazon S3–based data lake. Incoming data is ingested in Apache Parquet format from multiple hospitals and wearable health devices. To ensure quality and standardization, the company applies several transformation steps: anomaly filtering, datetime normalization, and aggregation by patient cohort. The company needs a solution to support a code-free interface that enables data engineers and business analysts to collaborate on data preparation workflows. The company also requires data lineage tracking, data profiling capabilities, and an easy way to share transformation logic across teams without writing or managing code.

Which AWS solution best meets these requirements?

- Use AWS Glue Studio's visual canvas to design data transformation workflows on top of the Parquet files in Amazon S3. Configure Glue Studio jobs to run these transformations without writing code. Share the job definitions with team members for reuse. Use the visual job editor to track transformation progress and inspect profiling statistics for each dataset column
- Create Amazon Athena SQL queries to perform transformation steps directly on S3. Store queries in AWS Glue Data Catalog and share saved queries with other users through Amazon Athena's query editor
- Use AWS Glue DataBrew to visually build transformation workflows on top of the raw Parquet files in S3. Use DataBrew recipes to track, audit, and share the transformation steps with others. Enable data profiling to inspect column statistics, null values, and data types across datasets
- Use Amazon AppFlow to move and transform Parquet files in S3. Configure AppFlow transformations and mappings within the visual interface. Share flows with collaborators through AWS IAM policies and scheduled executions

Answer: **(c) Use AWS Glue DataBrew to visually build transformation workflows on top of the raw Parquet files in S3.** **Use DataBrew recipes to track, audit, and share the transformation steps with others.** **Enable data profiling to inspect column statistics, null values, and data types across datasets**

Explanation: The problem requires a solution that provides a code-free interface for data engineers and business analysts to collaborate on data preparation workflows. It also needs to support data lineage tracking, data profiling, and easy sharing of transformation logic.

- **AWS Glue Studio** provides a visual canvas, but the primary purpose is to create and run Glue jobs, which are typically for developers. While it has a visual editor, it is not as tailored for business analysts and data preparation as DataBrew.
- **Amazon Athena** uses SQL queries, which is not a code-free interface.
- **Amazon AppFlow** is designed to move and transform data between SaaS applications and AWS services, not for general-purpose data preparation and profiling within a data lake.
- **AWS Glue DataBrew** is a visual data preparation tool that allows users to clean and normalize data without writing code. It offers features like data profiling, lineage tracking through "recipes," and easy sharing of these recipes, which directly addresses all the requirements in the problem.

# Question 7:

A logistics company is building a multi-tier application to track the location of its trucks during peak operating hours. The company wants these data points to be accessible in real-time in its analytics platform via a REST API. The company has hired you as an AWS Certified Solutions Architect Associate to build a multi-tier solution to store and retrieve this location data for analysis.

Which of the following options addresses the given use case?

Leverage Amazon API Gateway with Amazon Kinesis Data Analytics
Leverage Amazon Athena with Amazon S3
Leverage Amazon QuickSight with Amazon Redshift
Leverage Amazon API Gateway with AWS Lambda

Answer: **Leverage Amazon API Gateway with AWS Lambda**

The problem describes a multi-tier application for tracking truck locations in real-time, with data accessible via a REST API. This is a classic serverless use case.

- **Amazon API Gateway** is a managed service that allows you to create, publish, maintain, monitor, and secure REST and WebSocket APIs at any scale. It acts as the "front door" for applications to access data, business logic, or functionality from your backend services.
- **AWS Lambda** is a serverless, event-driven compute service that lets you run code without provisioning or managing servers. It can be triggered by various AWS services, including API Gateway, to execute business logic.

Together, API Gateway and Lambda provide a scalable and cost-effective solution for building a real-time, multi-tier application that can handle the incoming location data and serve it via a REST API without the need to manage any servers.

# Question 8:
The IT department at a consulting firm is conducting a training workshop for new developers. As part of an evaluation exercise on Amazon S3, the new developers were asked to identify the invalid storage class lifecycle transitions for objects stored on Amazon S3.
Can you spot the INVALID lifecycle transitions from the options below? (Select two)
- Amazon S3 Standard-IA => Amazon S3 One Zone-IA
- Amazon S3 Standard => Amazon S3 Intelligent-Tiering
- Amazon S3 Intelligent-Tiering => Amazon S3 Standard
- Amazon S3 One Zone-IA => Amazon S3 Standard-IA
- Amazon S3 Standard-IA => Amazon S3 Intelligent-Tiering

The two invalid lifecycle transitions are:

- **Amazon S3 Standard-IA => Amazon S3 One Zone-IA**
- **Amazon S3 Standard-IA => Amazon S3 Intelligent-Tiering**

The Amazon S3 storage class lifecycle transitions have specific rules. Objects can be transitioned from a more frequently accessed storage class to a less frequently accessed one, but not the other way around. Additionally, some transitions between specific classes are not allowed.

- **Amazon S3 Standard-IA => Amazon S3 One Zone-IA**: This is an invalid transition because you cannot transition from a storage class with high availability (Standard-IA) to a storage class with lower availability (One Zone-IA).
- **Amazon S3 Standard-IA => Amazon S3 Intelligent-Tiering**: This is an invalid transition because you cannot transition an object from a storage class that is already "infrequent access" to the Intelligent-Tiering class, which is designed to automatically move objects between frequent and infrequent access tiers.

# Question 9:
A gaming company is looking at improving the availability and performance of its global flagship application which utilizes User Datagram Protocol and needs to support fast regional failover in case an AWS Region goes down. The company wants to continue using its own custom Domain Name System (DNS) service.
Which of the following AWS services represents the best solution for this use-case?
AWS Global Accelerator
Amazon CloudFront
Amazon Route 53
AWS Elastic Load Balancing (ELB)

Answer: **(a) AWS Global Accelerator**

AWS Global Accelerator is a networking service that uses the AWS global network to improve the availability and performance of applications for global users. It routes traffic to the optimal healthy endpoint based on performance and user location. This service is particularly suitable for this use case because it supports User Datagram Protocol (UDP) traffic, which is mentioned in the problem description. It also provides instant failover to the next best endpoint if an application fails, which addresses the need for fast regional failover.


# Question 10:

A development team requires permissions to list an Amazon S3 bucket and delete objects from that bucket. A systems administrator has created the following IAM policy to provide access to the bucket and applied that policy to the group. The group is not able to delete objects in the bucket. The company follows the principle of least privilege.

```
    "Version": "2021-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket"
            ],
            "Effect": "Allow"
        }
    ]
```

Which statement should a solutions architect add to the policy to address this issue?
a)
```
{
    "Action": [
        "s3:*Object"
    ],
    "Resource": [
        "arn:aws:s3::: example-bucket/*"
    ],
    "Effect": "Allow"
}
```
b)
```
{
    "Action": [
        "s3:DeleteObject"
    ],
    "Resource": [
        "arn:aws:s3::: example-bucket/*"
    ],
    "Effect": "Allow"
}
```
c)

```
{
    "Action": [
        "s3:*"
    ],
    "Resource": [
        "arn:aws:s3::: example-bucket/*"
    ],
    "Effect": "Allow"
}
```
d)
```
{
    "Action": [
        "s3: DeleteObject"
    ],
    "Resource": [
        "arn:aws:s3::: example-bucket*"
    ],
    "Effect": "Allow"
}
```
The correct option is the second one.

The original policy allows the `s3:DeleteObject` action, but the `Resource` is specified as `arn:aws:s3:::example-bucket`. This resource ARN refers to the bucket itself, not the objects within it. To allow actions on objects inside a bucket, the resource ARN must include a wildcard (`/*`) at the end. The second option correctly specifies the resource as `arn:aws:s3:::example-bucket/*`, which allows the `s3:DeleteObject` action on all objects within the bucket. This also adheres to the principle of least privilege by only granting the necessary permission to delete objects, rather than all possible s3 actions.

Answer: **(b) The second option from the top**

# Question 11:

A retail company has developed a REST API which is deployed in an Auto Scaling group behind an Application Load Balancer. The REST API stores the user data in Amazon DynamoDB and any static content, such as images, are served via Amazon Simple Storage Service (Amazon S3). On analyzing the usage trends, it is found that 90% of the read requests are for commonly accessed data across all users.
As a Solutions Architect, which of the following would you suggest as the MOST efficient solution to improve the application performance?
- Enable ElastiCache Redis for DynamoDB and ElastiCache Memcached for Amazon S3
- Enable Amazon DynamoDB Accelerator (DAX) for Amazon DynamoDB and Amazon CloudFront for Amazon S3
- Enable ElastiCache Redis for DynamoDB and Amazon CloudFront for Amazon S3
- Enable Amazon DynamoDB Accelerator (DAX) for Amazon DynamoDB and ElastiCache Memcached for Amazon S3

Answer: **Enable Amazon DynamoDB Accelerator (DAX) for Amazon DynamoDB and Amazon CloudFront for Amazon S3**

The problem describes an application with two key components: user data stored in Amazon DynamoDB and static content (images) in Amazon S3. The primary performance bottleneck is identified as a high volume of read requests (90%) for commonly accessed data.

- **For Amazon DynamoDB:** Amazon DynamoDB Accelerator (DAX) is a caching service specifically designed for DynamoDB. It provides an in-memory cache that significantly reduces response times for read-heavy workloads, which is an ideal solution for the scenario described.
- **For Amazon S3:** Amazon CloudFront is a content delivery network (CDN) that caches static content, such as images, at edge locations around the world. This reduces latency and improves performance for users by serving content from a location closer to them.

Combining these two services directly addresses the performance issues for both the user data and the static content, making it the most efficient solution.