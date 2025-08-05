Aqui vai um esqueleto enxuto — em **apenas dois arquivos *.tf*** — que cobre todo o fluxo:

```
repo-root/
├── infra/                # executado LOCALMENTE, 1-vez, para subir o Jenkins
│   └── main.tf
├── jenkins-pipelines/    # lidos pelo próprio Jenkins
│   ├── deploy_bucket.Jenkinsfile
│   └── deploy_site.Jenkinsfile
└── bucket/               # código Terraform usado pelo 1º job
    └── main.tf
```

---

## 1. `infra/main.tf` — sobe o Jenkins (EC2 + Docker)

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers { aws = { source = "hashicorp/aws" ~> 5.0 } }
}

provider "aws" { region = var.region }

variable "region"       { default = "us-east-1" }
variable "key_name"     { description = "SSH key já existente" }
variable "instance_type"{ default = "t3.micro" }
variable "vpc_id"       {}
variable "subnet_id"    {}

resource "aws_security_group" "jenkins" {
  name        = "sg-jenkins"
  vpc_id      = var.vpc_id
  ingress { from_port = 8080 to_port = 8080 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  ingress { from_port = 22   to_port = 22   protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0    to_port = 0    protocol = "-1"  cidr_blocks = ["0.0.0.0/0"] }
}

data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["137112412989"] # Amazon
  filter { name = "name" values = ["al2023-ami-minimal-*x86_64*"] }
}

resource "aws_iam_role" "jenkins" {
  name               = "jenkins-role"
  assume_role_policy = data.aws_iam_policy_document.ec2.json
}

data "aws_iam_policy_document" "ec2" {
  statement {
    actions = ["sts:AssumeRole"]
    principals { type = "Service" identifiers = ["ec2.amazonaws.com"] }
  }
}

# Permissões mínimas: gerenciar S3 + Terraform state em S3 + DynamoDB lock
resource "aws_iam_role_policy_attachment" "s3full" {
  role       = aws_iam_role.jenkins.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_instance" "jenkins" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.jenkins.id]
  iam_instance_profile   = aws_iam_instance_profile.jenkins.name

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -a -G docker ec2-user

    docker run -d --name jenkins \
      -p 8080:8080 -p 50000:50000 \
      -v /var/jenkins_home:/var/jenkins_home \
      -e JAVA_OPTS="-Djenkins.install.runSetupWizard=false" \
      jenkins/jenkins:lts-jdk17
  EOF
}

resource "aws_iam_instance_profile" "jenkins" {
  name = "jenkins-profile"
  role = aws_iam_role.jenkins.name
}

output "jenkins_url" {
  value = "http://${aws_instance.jenkins.public_ip}:8080"
}
```

**O que esse único arquivo já faz**

1. Cria \[EC2] mínimo, instala \[Docker] e sobe o container oficial [`jenkins/jenkins:lts`](https://hub.docker.com/r/jenkins/jenkins)
2. Entrega a *public IP* via `terraform output`
3. Concede permissão total de \[S3] para os *jobs* (se quiser limitar, troque por política custom)
4. Mantém tudo em **um** `.tf`, atendendo ao pedido de “menor número de arquivos”.

---

## 2. `bucket/main.tf` — criado pelo job “Deploy Bucket”

```hcl
terraform {
  required_providers { aws = { source = "hashicorp/aws" } }

  backend "s3" {
    bucket = "tfstate-<SUA-CONTA>"
    key    = "bucket-prod.tfstate"
    region = "us-east-1"
    dynamodb_table = "tf-lock"
  }
}

provider "aws" { region = "us-east-1" }

variable "bucket_name" { description = "Nome do bucket para o site" }

resource "aws_s3_bucket" "site" {
  bucket = var.bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "index.html"
  }

  object_lock_enabled = false
}
```

*(aqui basta um arquivo, pois só há 1 recurso)*

---

## 3. Jenkins Pipelines-as-Code

### `deploy_bucket.Jenkinsfile`

```groovy
pipeline {
  agent any
  environment {
    AWS_DEFAULT_REGION = 'us-east-1'
  }
  stages {
    stage('Init')  { steps { sh 'terraform -chdir=bucket init' } }
    stage('Apply') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                          credentialsId: 'jenkins-aws']]) {
          sh '''
             terraform -chdir=bucket apply \
               -auto-approve -var="bucket_name=meu-site-angular"
          '''
        }
      }
    }
  }
}
```

### `deploy_site.Jenkinsfile`

```groovy
pipeline {
  agent any
  environment {
    AWS_DEFAULT_REGION = 'us-east-1'
    BUCKET            = 'meu-site-angular'
  }
  stages {
    stage('Build Angular') {
      steps {
        sh 'npm ci'
        sh 'npm run build -- --prod'
      }
    }
    stage('Sync to S3') {
      steps {
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding',
                          credentialsId: 'jenkins-aws']]) {
          sh 'aws s3 sync ./dist/ s3://$BUCKET/ --delete'
        }
      }
    }
  }
  post {
    success {
      echo "Site publicado em: http://$BUCKET.s3-website-us-east-1.amazonaws.com"
    }
  }
}
```

*(Ambos os pipelines assumem que uma credencial AWS chamada **jenkins-aws** já foi cadastrada no Jenkins)*

---

## 4. Fluxo de uso

1. **Operador local**

   ```bash
   cd infra
   terraform init && terraform apply -auto-approve
   # ⬆️ cria a EC2 com Docker + Jenkins
   ```
2. Acesse o `jenkins_url` de *output* e cadastre a credencial **jenkins-aws** (Access Key + Secret ou IAM Role via Instance Profile já cobre).
3. **No Jenkins**, crie dois *Pipeline Jobs* apontando para o repositório Git e para os respectivos Jenkinsfiles.
4. **Executar “Deploy Bucket” →** cria o bucket via \[Terraform].
5. **Executar “Deploy Site” →** compila Angular (`npm run build`) e faz `aws s3 sync`.

---

## 5. Dicas finais

* Use um \[backend] S3/Dynamo diferente para `infra/` e `bucket/` para manter *states* independentes.
* Para evitar digitar variables hard-coded, exponha-as no **Jenkinsfile** ou use `terraform.workspace` para múltiplos ambientes.
* Se quiser **zero toil**: adicione um *job seed* com \[Job DSL] ou Groovy-init para criar os dois pipelines automaticamente na primeira execução.

---

Com esses **dois `.tf`** e dois **Jenkinsfiles**, você tem:

* \[IaC] completa para \[Jenkins] + \[S3]
* Build e deploy de site Angular
* Criação do bucket via \[Terraform] dentro do próprio Jenkins
* Estrutura mínima, fácil de copiar-colocar em qualquer Obsidian 😊

---

## 1 · `Dockerfile`   ( `jenkins/Dockerfile` )

```dockerfile
# Imagem base oficial LTS com JDK 17
FROM jenkins/jenkins:lts-jdk17

USER root
# Ferramentas que os pipelines vão precisar
RUN apt-get update && \
    apt-get install -y docker.io python3-pip && \
    pip3 install awscli && \
    rm -rf /var/lib/apt/lists/*

# Plugins essenciais: Bitbucket, Pipeline, Terraform, AWS CLI integration
RUN jenkins-plugin-cli --plugins \
    "bitbucket:227.vcc3d36b_80d2e" \
    "workflow-aggregator" \
    "hashicorp-terraform-plugin:1.0.15" \
    "cloudbees-folder"

# Evita o wizard interativo
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
USER jenkins
```

---

## 2 · `docker-compose.yml`  (uso local ou em CI para build da imagem)

```yaml
version: "3.9"
services:
  jenkins:
    build: ./jenkins
    image: jenkins-custom:latest
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
volumes:
  jenkins_home:
```

> **Como usar localmente**
>
> ```bash
> docker compose up -d          # sobe o Jenkins
> docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
> ```

---

## 3 · `infra/main.tf` — **todo o IaC em um único arquivo**

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers { aws = { source = "hashicorp/aws" ~> 5.0 } }

  backend "s3" {                # state remoto
    bucket = "tfstate-<sua-conta>"
    key    = "ecs-jenkins.tfstate"
    region = "us-east-1"
    dynamodb_table = "tf-lock"
  }
}

provider "aws" { region = "us-east-1" }

########################
# 1. Networking (mínimo)
########################
data "aws_availability_zones" "azs" {}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index)
  availability_zone       = data.aws_availability_zones.azs.names[count.index]
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" { vpc_id = aws_vpc.main.id }

resource "aws_route_table" "rt" {
  vpc_id = aws_vpc.main.id
  route  { cidr_block = "0.0.0.0/0" gateway_id = aws_internet_gateway.igw.id }
}
resource "aws_route_table_association" "assoc" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.rt.id
}

########################
# 2. ECS Fargate + ALB
########################
resource "aws_ecs_cluster" "jenkins" { name = "jenkins-cluster" }

resource "aws_iam_role" "task_exec" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = data.aws_iam_policy_document.task.json
}
data "aws_iam_policy_document" "task" {
  statement {
    actions   = ["sts:AssumeRole"]
    principals { type = "Service" identifiers = ["ecs-tasks.amazonaws.com"] }
  }
}
resource "aws_iam_role_policy_attachment" "exec_policy" {
  role       = aws_iam_role.task_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# Permissão de S3 (pipelines)
resource "aws_iam_role" "jenkins_job" {
  name               = "jenkins-job-role"
  assume_role_policy = data.aws_iam_policy_document.task.json
}
resource "aws_iam_role_policy_attachment" "s3_full" {
  role       = aws_iam_role.jenkins_job.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_security_group" "alb" {
  name   = "alb-sg"
  vpc_id = aws_vpc.main.id
  ingress { from_port = 80 to_port = 80 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0  to_port = 0  protocol = "-1" cidr_blocks = ["0.0.0.0/0"] }
}
resource "aws_security_group" "jenkins" {
  name   = "jenkins-sg"
  vpc_id = aws_vpc.main.id
  ingress { from_port = 8080 to_port = 8080 protocol = "tcp" security_groups = [aws_security_group.alb.id] }
  ingress { from_port = 50000 to_port = 50000 protocol = "tcp" security_groups = [aws_security_group.alb.id] }
  egress  { from_port = 0    to_port = 0    protocol = "-1" cidr_blocks      = ["0.0.0.0/0"] }
}

resource "aws_lb" "alb" {
  name               = "jenkins-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}
resource "aws_lb_target_group" "jenkins" {
  name     = "jenkins-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  health_check { path = "/" port = "8080" }
}
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.jenkins.arn
  }
}

# ECR para armazenar a imagem
resource "aws_ecr_repository" "jenkins" { name = "jenkins" }

# Task Definition usando a imagem do ECR
resource "aws_ecs_task_definition" "jenkins" {
  family                   = "jenkins"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.task_exec.arn
  task_role_arn            = aws_iam_role.jenkins_job.arn

  container_definitions = jsonencode([{
    name      = "jenkins"
    image     = "${aws_ecr_repository.jenkins.repository_url}:latest"
    essential = true
    portMappings = [
      { containerPort = 8080, hostPort = 8080, protocol = "tcp" },
      { containerPort = 50000, hostPort = 50000, protocol = "tcp" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-region        = "us-east-1"
        awslogs-group         = "/ecs/jenkins"
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/jenkins"
  retention_in_days = 14
}

resource "aws_ecs_service" "jenkins" {
  name            = "jenkins"
  cluster         = aws_ecs_cluster.jenkins.id
  task_definition = aws_ecs_task_definition.jenkins.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.public[*].id
    security_groups = [aws_security_group.jenkins.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.jenkins.arn
    container_name   = "jenkins"
    container_port   = 8080
  }
}

output "jenkins_url" {
  value = "http://${aws_lb.alb.dns_name}"
}
```

---

## 4 · Pipeline files (Jenkinsfiles) — idênticos ao exemplo anterior

Os dois Jenkinsfiles (`deploy_bucket.Jenkinsfile` e `deploy_site.Jenkinsfile`) permanecem válidos; o container já traz o AWS CLI e o plugin Terraform. Adapte o nome do bucket se necessário.

---

## 5 · Deploy **100 % via CLI**

```bash
# 1. Construir imagem e enviá-la ao ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <ID>.dkr.ecr.us-east-1.amazonaws.com

docker build -t jenkins-custom:latest ./jenkins
docker tag jenkins-custom:latest <ID>.dkr.ecr.us-east-1.amazonaws.com/jenkins:latest
docker push <ID>.dkr.ecr.us-east-1.amazonaws.com/jenkins:latest

# 2. Provisionar infraestrutura
cd infra
terraform init
terraform apply -auto-approve

# 3. Resultado
# jenkins_url = http://<alb-dns>
```

---

## 6 · Gatilho de build por push no **Bitbucket**

1. **Plugins já incluídos**: \[Bitbucket] e \[Pipeline].
2. **No Jenkins**

   * Crie um **Multibranch Pipeline**
   * Em *Branch Source* escolha *Bitbucket Cloud*.
   * Informe *Credentials* (token App Password) e o repositório.
   * Marque **“Build when a change is pushed to Bitbucket”**.
   * Salve; o job expõe automaticamente o endpoint

     ```
     http://<alb-dns>/bitbucket-hook/
     ```
3. **No Bitbucket** (`Repository → Settings → Webhooks`)

   * Add webhook → URL acima
   * Events → *Repository push*
   * Done.

> A cada `git push` no Bitbucket, o webhook dispara um scan e o Jenkins executa o pipeline correspondente.

---

### 🗒️ Resumo rápido

* **\[Dockerfile]** customizado para Jenkins + AWS CLI + plugins
* **\[docker-compose]** para rodar localmente ou compilar a imagem
* **IaC** em **1 arquivo `main.tf`** cria VPC, ALB, ECS Fargate, ECR e roles
* **CLI**: `docker build/push` → `terraform apply` → abrir URL
* **Bitbucket Webhook** ativa builds instantaneamente

Copie, ajuste nomes/IDs e você terá um pipeline completo, minimalista e conteinerizado em \[ECS] 🚀
