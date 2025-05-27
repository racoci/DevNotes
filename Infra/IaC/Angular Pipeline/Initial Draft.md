Para automatizar o deploy e os testes de uma aplicação web desenvolvida em AngularJS utilizando a AWS e o Terraform no paradigma de Infrastructure as Code (IaC), você pode seguir uma abordagem simples e eficaz. Abaixo, apresento um guia passo a passo que cobre desde a criação da infraestrutura até o deploy automatizado da aplicação.


---

🧰 Ferramentas Necessárias

AngularJS: Framework para desenvolvimento da aplicação web.

AWS S3: Armazenamento de arquivos estáticos (HTML, CSS, JS).

AWS CloudFront: CDN para distribuição global dos arquivos.

AWS Route 53: Gerenciamento de DNS (opcional).

Terraform: Ferramenta de IaC para provisionamento da infraestrutura.

AWS CodePipeline & CodeBuild: Serviços para CI/CD (opcional).

AWS CLI: Interface de linha de comando para interagir com os serviços da AWS.



---

🚀 Passo a Passo para Deploy Simples

1. Criar a Aplicação AngularJS

Se ainda não possui uma aplicação AngularJS, você pode criar uma estrutura básica:

npx @angular/cli new my-app
cd my-app
ng build --prod

O comando ng build --prod gerará os arquivos estáticos na pasta dist/my-app/.


---

2. Provisionar Infraestrutura com Terraform

Crie um arquivo main.tf com a seguinte configuração:

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "angular_app" {
  bucket = "meu-angular-app"
  website {
    index_document = "index.html"
    error_document = "index.html"
  }
}

resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.angular_app.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = "*",
      Action    = ["s3:GetObject"],
      Resource  = ["${aws_s3_bucket.angular_app.arn}/*"]
    }]
  })
}

output "website_url" {
  value = aws_s3_bucket.angular_app.website_endpoint
}

Execute os comandos Terraform:

terraform init
terraform apply

Após a execução, o Terraform criará um bucket S3 configurado para hospedagem de site estático e exibirá a URL do site.


---

3. Fazer o Upload da Aplicação para o S3

Utilize o AWS CLI para sincronizar os arquivos da aplicação com o bucket S3:

aws s3 sync dist/my-app/ s3://meu-angular-app/


---

4. (Opcional) Configurar CloudFront e Route 53

Para melhorar a performance e adicionar um domínio personalizado, você pode configurar o CloudFront e o Route 53. Um exemplo completo de configuração com Terraform está disponível no repositório mkryuk/terraform-angular-pipeline .


---

5. (Opcional) Automatizar com CodePipeline e CodeBuild

Para automatizar o processo de build e deploy, você pode utilizar o AWS CodePipeline e o CodeBuild. Isso permitirá que, a cada push no repositório, a aplicação seja automaticamente construída e implantada. Um exemplo de implementação está descrito no artigo Automated AngularJS & Bootstrap Deployment via AWS CodePipeline .


---

✅ Conclusão

Com os passos acima, você consegue automatizar o deploy de uma aplicação AngularJS na AWS utilizando o Terraform de forma simples e eficiente. Essa abordagem permite versionar a infraestrutura, facilitar o gerenciamento e escalar conforme necessário.

Se desejar, posso fornecer um exemplo completo de código Terraform para essa configuração. Gostaria que eu preparasse esse exemplo para você?

