# Question 1
A software company has a globally distributed team of developers, that requires secure and compliant access to AWS environments. The company manages multiple AWS accounts under AWS Organizations and uses an on-premises Microsoft Active Directory for user authentication. To simplify access control and identity governance across projects and accounts, the company wants a centrally managed solution that integrates with their existing infrastructure. The solution should require the least amount of ongoing operational management.

Which approach best meets the company’s requirements?

- Deploy AWS Directory Service for Microsoft Active Directory in AWS. Establish a trust relationship with the on-premises Active Directory. Use IAM roles linked to AD groups to control access to AWS resources.

- Use AWS Directory Service AD Connector to connect AWS to the on-premises Active Directory. Integrate AD Connector with AWS IAM Identity Center. Use permission sets to assign access to AWS accounts and resources based on Active Directory group membership.

- Deploy an open-source identity provider (IdP) on Amazon EC2. Synchronize it with the on-premises Active Directory and use SAML to federate access to AWS accounts. Assign IAM roles to federated users based on SAML assertions.

- Use AWS Control Tower to enable account access for developers. Create AWS IAM roles in each member account and manually assign permissions. Instruct developers to assume roles across accounts using the AWS CLI.

# Question 2
A major bank is using Amazon Simple Queue Service (Amazon SQS) to migrate several core banking applications to the cloud to ensure high availability and cost efficiency while simplifying administrative complexity and overhead. The development team at the bank expects a peak rate of about 1000 messages per second to be processed via SQS. It is important that the messages are processed in order.

Which of the following options can be used to implement this system?

- Use Amazon SQS FIFO (First-In-First-Out) queue in batch mode of 2 messages per operation to process the messages at the peak rate.
- Use Amazon SQS FIFO (First-In-First-Out) queue in batch mode of 4 messages per operation to process the messages at the peak rate.
- Use Amazon SQS FIFO (First-In-First-Out) queue to process the messages.
- Use Amazon SQS standard queue to process the messages.


# Question 3:

A government agency is developing a online application to assist users in submitting permit requests through a web-based interface. The system architecture consists of a front-end web application tier and a background processing tier that handles the validation and submission of the forms. The application is expected to see high traffic and it must ensure that every submitted request is processed exactly once, with no loss of data.

Which design choice best satisfies these requirements?

- Leverage Amazon EventBridge to send events from the web application to the processing tier for asynchronous form handling
- Implement an Amazon SQS standard queue to reliably buffer and deliver form submissions from the web application layer to the processing tier
- Leverage Amazon API Gateway to pass the form submissions to AWS Lambda for processing in real time
- Implement an Amazon SQS FIFO queue to reliably buffer and deliver form submissions from the web application layer to the processing tier

# Question 4:

A new DevOps engineer has just joined a development team and wants to understand the replication capabilities for Amazon RDS Multi-AZ deployment as well as Amazon RDS Read-replicas.

Which of the following correctly summarizes these capabilities for the given database?

A new DevOps engineer has just joined a development team and wants to understand the replication capabilities for Amazon RDS Multi-AZ deployment as well as Amazon RDS Read-replicas.
Which of the following correctly summarizes these capabilities for the given database?

- Multi-AZ follows synchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow asynchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans one Availability Zone (AZ) within a single region. Read replicas follow synchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow synchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region
- Multi-AZ follows asynchronous replication and spans at least two Availability Zones (AZs) within a single region. Read replicas follow asynchronous replication and can be within an Availability Zone (AZ), Cross-AZ, or Cross-Region

