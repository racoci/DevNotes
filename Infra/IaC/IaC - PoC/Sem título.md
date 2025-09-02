Awesome—let’s turn your local Docker Jenkins into an AWS-managed setup with Terraform, keeping your current repo layout. Below is a complete, production-ready (but cost-aware) ECS Fargate deployment of your Jenkins controller using your existing Dockerfile and JCasC config.

### What this Terraform does

- **ECR** repository for your custom Jenkins image (built from your `container/jenkins/Dockerfile`).
- **VPC** with 2 public subnets (keeps costs down—no NAT gateways).
- **ECS Fargate** cluster + service for Jenkins.
- **EFS** filesystem mounted into `/var/jenkins_home` to persist Jenkins data across task restarts.
- **ALB** (Application Load Balancer) with HTTP by default. HTTPS supported if you provide an ACM certificate.
- **CloudWatch Logs** for Jenkins container logs.
- **IAM** task roles so Jenkins can deploy to S3 and (optionally) invalidate CloudFront.

> ✅ You can later flip to private subnets + NAT if needed. This setup assigns a public IP to the ECS task to keep things simpler/cheaper.

---

## Directory layout (fits your repo)

Place these files under:  
`projects/static_web_site/cicd/infra/`

```
providers.tf
variables.tf
vpc.tf
security.tf
ecr.tf
efs.tf
logs.tf
iam.tf
ecs.tf
alb.tf
outputs.tf
```

---

## 1) `providers.tf`

```hcl
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }
}

provider "aws" {
  region  = var.region
  profile = var.aws_profile
}
```

---

## 2) `variables.tf`

```hcl
variable "project_name" {
  description = "Project name prefix for resources"
  type        = string
  default     = "static-website-cicd"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "sa-east-1"
}

variable "aws_profile" {
  description = "Local AWS CLI profile to use"
  type        = string
  default     = null
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.50.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "Two public subnets in different AZs"
  type        = list(string)
  default     = ["10.50.10.0/24", "10.50.20.0/24"]
}

variable "container_image_tag" {
  description = "Tag for the Jenkins ECR image"
  type        = string
  default     = "latest"
}

variable "cpu" {
  description = "Fargate CPU units"
  type        = number
  default     = 1024
}

variable "memory" {
  description = "Fargate memory (MB)"
  type        = number
  default     = 2048
}

variable "certificate_arn" {
  description = "ACM certificate ARN for HTTPS on ALB (optional). If empty, only HTTP is configured."
  type        = string
  default     = ""
}

variable "route53_zone_id" {
  description = "Route53 Hosted Zone ID for alias record (optional)"
  type        = string
  default     = ""
}

variable "domain_name" {
  description = "DNS name for ALB (optional, requires zone_id)"
  type        = string
  default     = ""
}

variable "site_bucket_name" {
  description = "S3 bucket Jenkins deploys the static site to (used for IAM permissions)"
  type        = string
  default     = ""
}

variable "cloudfront_distribution_id" {
  description = "CloudFront distribution ID to invalidate after deploys (optional)"
  type        = string
  default     = ""
}

variable "allow_jenkins_agent_port" {
  description = "Expose JNLP agent port 50000 (typically not needed if using in-container agents only)"
  type        = bool
  default     = false
}
```

---

## 3) `vpc.tf`

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${var.project_name}-vpc" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-igw" }
}

data "aws_availability_zones" "available" {}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = {
    Name = "${var.project_name}-public-${count.index + 1}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "${var.project_name}-public-rt" }
}

resource "aws_route" "public_inet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route_table_association" "public_assoc" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

---

## 4) `security.tf`

```hcl
# ALB security group: allow 80/443 from anywhere
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-alb-sg"
  description = "ALB SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  dynamic "ingress" {
    for_each = var.certificate_arn != "" ? [1] : []
    content {
      description = "HTTPS"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
  }

  egress {
    description = "All egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = { Name = "${var.project_name}-alb-sg" }
}

# ECS Tasks security group: only receive from ALB on 8080 (and optional 50000)
resource "aws_security_group" "ecs" {
  name        = "${var.project_name}-ecs-sg"
  description = "ECS tasks SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "From ALB to Jenkins 8080"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  dynamic "ingress" {
    for_each = var.allow_jenkins_agent_port ? [1] : []
    content {
      description     = "JNLP agent port 50000 from ALB (or adjust as needed)"
      from_port       = 50000
      to_port         = 50000
      protocol        = "tcp"
      security_groups = [aws_security_group.alb.id]
    }
  }

  egress {
    description = "All egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = { Name = "${var.project_name}-ecs-sg" }
}

# EFS security group: allow NFS from ECS tasks
resource "aws_security_group" "efs" {
  name        = "${var.project_name}-efs-sg"
  description = "EFS SG"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "NFS from ECS tasks"
    from_port       = 2049
    to_port         = 2049
    protocol        = "tcp"
    security_groups = [aws_security_group.ecs.id]
  }

  egress {
    description = "All egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = { Name = "${var.project_name}-efs-sg" }
}
```

---

## 5) `ecr.tf`

```hcl
resource "aws_ecr_repository" "jenkins" {
  name                 = "${var.project_name}-jenkins"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = { Name = "${var.project_name}-jenkins-ecr" }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.jenkins.repository_url
}
```

---

## 6) `efs.tf`

```hcl
resource "aws_efs_file_system" "jenkins" {
  creation_token = "${var.project_name}-jenkins-efs"
  encrypted      = true
  tags = { Name = "${var.project_name}-efs" }
}

# One mount target per subnet
resource "aws_efs_mount_target" "mt" {
  count           = length(aws_subnet.public)
  file_system_id  = aws_efs_file_system.jenkins.id
  subnet_id       = aws_subnet.public[count.index].id
  security_groups = [aws_security_group.efs.id]
}

# Access Point to enforce POSIX UID/GID 1000 (Jenkins user)
resource "aws_efs_access_point" "jenkins" {
  file_system_id = aws_efs_file_system.jenkins.id

  posix_user {
    uid = 1000
    gid = 1000
  }

  root_directory {
    path = "/jenkins"
    creation_info {
      owner_uid   = 1000
      owner_gid   = 1000
      permissions = "0755"
    }
  }

  tags = { Name = "${var.project_name}-efs-ap" }
}
```

---

## 7) `logs.tf`

```hcl
resource "aws_cloudwatch_log_group" "jenkins" {
  name              = "/ecs/${var.project_name}-jenkins"
  retention_in_days = 30
}
```

---

## 8) `iam.tf`

```hcl
# ECS task execution role (pull image, write logs)
resource "aws_iam_role" "ecs_execution" {
  name               = "${var.project_name}-ecs-exec"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume.json
}

data "aws_iam_policy_document" "ecs_tasks_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "ecs_exec_ecr" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Task role (what Jenkins can do in AWS)
resource "aws_iam_role" "ecs_task" {
  name               = "${var.project_name}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.ecs_tasks_assume.json
}

data "aws_iam_policy_document" "jenkins_permissions" {
  statement {
    sid     = "S3Deploy"
    actions = [
      "s3:PutObject", "s3:PutObjectAcl", "s3:DeleteObject",
      "s3:ListBucket", "s3:GetObject"
    ]
    resources = var.site_bucket_name != "" ? [
      "arn:aws:s3:::${var.site_bucket_name}",
      "arn:aws:s3:::${var.site_bucket_name}/*"
    ] : []
  }

  statement {
    sid     = "CloudFrontInvalidate"
    actions = ["cloudfront:CreateInvalidation"]
    resources = var.cloudfront_distribution_id != "" ? [
      "arn:aws:cloudfront::*:distribution/${var.cloudfront_distribution_id}"
    ] : []
  }

  # Optionally read Secrets Manager/SSM if you later store credentials
  # statement {
  #   actions   = ["secretsmanager:GetSecretValue", "ssm:GetParameter", "ssm:GetParameters"]
  #   resources = ["*"]
  # }
}

resource "aws_iam_policy" "jenkins_policy" {
  name   = "${var.project_name}-jenkins-policy"
  policy = data.aws_iam_policy_document.jenkins_permissions.json
}

# Attach only if there are statements with resources
resource "aws_iam_role_policy_attachment" "jenkins_attach" {
  count      = (var.site_bucket_name != "" || var.cloudfront_distribution_id != "") ? 1 : 0
  role       = aws_iam_role.ecs_task.name
  policy_arn = aws_iam_policy.jenkins_policy.arn
}
```

---

## 9) `ecs.tf`

```hcl
locals {
  ecr_image = "${aws_ecr_repository.jenkins.repository_url}:${var.container_image_tag}"
}

resource "aws_ecs_cluster" "this" {
  name = "${var.project_name}-cluster"
}

resource "aws_ecs_task_definition" "jenkins" {
  family                   = "${var.project_name}-jenkins"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = tostring(var.cpu)
  memory                   = tostring(var.memory)
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  volume {
    name = "jenkins_home"
    efs_volume_configuration {
      file_system_id          = aws_efs_file_system.jenkins.id
      transit_encryption      = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.jenkins.id
        iam             = "ENABLED"
      }
      root_directory = "/jenkins"
    }
  }

  container_definitions = jsonencode([
    {
      name      = "jenkins"
      image     = local.ecr_image
      essential = true
      portMappings = [
        { containerPort = 8080, protocol = "tcp" }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.jenkins.name
          awslogs-region        = var.region
          awslogs-stream-prefix = "jenkins"
        }
      }
      mountPoints = [
        {
          sourceVolume  = "jenkins_home"
          containerPath = "/var/jenkins_home"
          readOnly      = false
        }
      ]
      # Environment variables (if your JCasC expects any)
      environment = [
        { name = "CASC_JENKINS_CONFIG", value = "/var/jenkins_home/casc_configs/jcasc.yaml" }
      ]
    }
  ])
}

resource "aws_ecs_service" "jenkins" {
  name            = "${var.project_name}-jenkins"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.jenkins.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets          = aws_subnet.public[*].id
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.jenkins.arn
    container_name   = "jenkins"
    container_port   = 8080
  }

  depends_on = [aws_lb_listener.http]
}
```

---

## 10) `alb.tf`

```hcl
resource "aws_lb" "this" {
  name               = replace("${var.project_name}-alb", "/[^a-zA-Z0-9-]/", "-")
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}

resource "aws_lb_target_group" "jenkins" {
  name        = replace("${var.project_name}-tg", "/[^a-zA-Z0-9-]/", "-")
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = "/login"
    matcher             = "200-399"
    interval            = 30
    unhealthy_threshold = 2
    healthy_threshold   = 2
    timeout             = 5
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type = var.certificate_arn != "" ? "redirect" : "forward"

    dynamic "redirect" {
      for_each = var.certificate_arn != "" ? [1] : []
      content {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }

    dynamic "forward" {
      for_each = var.certificate_arn == "" ? [1] : []
      content {
        target_group_arn = aws_lb_target_group.jenkins.arn
      }
    }
  }
}

resource "aws_lb_listener" "https" {
  count             = var.certificate_arn != "" ? 1 : 0
  load_balancer_arn = aws_lb.this.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = var.certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.jenkins.arn
  }
}

# Optional DNS record
resource "aws_route53_record" "alb" {
  count   = (var.route53_zone_id != "" && var.domain_name != "") ? 1 : 0
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_lb.this.dns_name
    zone_id                = aws_lb.this.zone_id
    evaluate_target_health = true
  }
}
```

---

## 11) `outputs.tf`

```hcl
output "alb_dns_name" {
  description = "Public URL for Jenkins (use this if no custom domain)"
  value       = aws_lb.this.dns_name
}

output "service_name" {
  value = aws_ecs_service.jenkins.name
}

output "cluster_name" {
  value = aws_ecs_cluster.this.name
}
```

---

## Build & Push your Jenkins image to ECR

Use your existing Dockerfile at `projects/static_web_site/cicd/container/jenkins/Dockerfile` and `jcasc.yaml` in `container/`.

1) **Init/apply Terraform up to ECR** (so you get the repo URL):

```bash
cd projects/static_web_site/cicd/infra
terraform init
terraform apply -target=aws_ecr_repository.jenkins
```

2) **Authenticate to ECR & push image:**

```bash
# set your region/profile if needed
AWS_REGION="sa-east-1"   # or your chosen region
AWS_PROFILE=""           # e.g., default or your profile; leave empty if not using profiles

# Get ECR login (with profile if you use one)
aws ${AWS_PROFILE:+--profile $AWS_PROFILE} ecr get-login-password --region $AWS_REGION \
| docker login --username AWS --password-stdin $(terraform output -raw ecr_repository_url | cut -d'/' -f1)

# Build from your repo structure root
cd projects/static_web_site/cicd/container
docker build -t jenkins-controller:latest -f jenkins/Dockerfile .

# Tag & push
ECR_URL=$(cd ../infra && terraform output -raw ecr_repository_url)
docker tag jenkins-controller:latest ${ECR_URL}:latest
docker push ${ECR_URL}:latest
```

3) **Apply the rest of the infra:**

```bash
cd ../infra
terraform apply
```

> After a few minutes, grab `alb_dns_name` from outputs and open it in the browser. If you provided `certificate_arn` and domain, use your domain over HTTPS.

---

## Notes / Options

- **JCasC & Plugins**: Your Dockerfile already installs plugins and copies `jcasc.yaml` into `/var/jenkins_home/casc_configs/jcasc.yaml`. Because we mount EFS at `/var/jenkins_home`, that file persists after first run. If you want to keep the config baked into the image only, that’s fine; JCasC will load it at startup.
- **AWS CLI inside Jenkins**: Your Dockerfile installs `unzip`, `curl`, etc. If your pipelines call AWS CLI, add it to the image (e.g., install AWS CLI v2) or use Jenkins agents that have it. Quick addition:

```dockerfile
  RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
      && unzip awscliv2.zip && ./aws/install && rm -rf awscliv2.zip aws
```

- **Agent Port (50000)**: Disabled by default. If you run inbound agents, set `allow_jenkins_agent_port = true` and update ALB/SGs accordingly (also consider direct security group rules rather than via ALB).
- **HTTPS**: Provide `-var="certificate_arn=arn:aws:acm:..."` and optionally `route53_zone_id` + `domain_name` to get TLS on the ALB.
- **S3/CloudFront perms**: Set `site_bucket_name` and `cloudfront_distribution_id` vars to grant the task IAM role minimal deploy permissions used by your Jenkins pipelines.
- **State Backend**: You currently keep local state. If you want a remote backend (S3 + DynamoDB lock), I can add that.

---

## How this maps to your current repo

- Uses your existing `container/jenkins/Dockerfile` and `jcasc.yaml`.
- Keeps pipelines in `pipeline/` untouched. They’ll run on the ECS Jenkins.
- Replaces your local `docker-compose` runtime with ECS Fargate + ALB + EFS.

---

## Next steps / Questions

1. Which **AWS region** do you want to use? (I set `sa-east-1` by default.)
2. Do you have a **domain + ACM certificate** you want to use for HTTPS now?
3. What’s the **S3 bucket** and optional **CloudFront distribution** your pipeline deploys to? I can pre-fill those IAM permissions precisely.

If you share your `jcasc.yaml` highlights (admin user config, credentials sources), I can also wire Secrets Manager/SSM integration so credentials aren’t stored in the image or EFS.