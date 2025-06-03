## Recapitulando o modelo 3 Camadas
- 1. Infra
- 2. Aplicações para construir: Bedrock e SageMaker
- 3. Serviços gerenciados pela própria AWS como reconhecimento de imagem, etc

Hoje falaremos da segunda camada

## Pipeline de IA
- Preparo de dados com conexão com outros serviços da AWS
- Feature Store: Guarda os datasets preparados para ser usado por diversos modelos 
- Construção do modelo
- Avaliação do modelo
- Treino ou fine-tuning
- Deploy em produção
- Monitoramento e gerenciamento

## Features do SageMaker Studio
- Permite usar em conjunto com outros desenvolvedores como um google docs
- Permitem outras pessoas verem os jobs de treinamento e manipularem como pausar, mudar algum hiper-parâmetros, mudar o dataset, etc.
- Processing jobs para manipulação de datasets

## IDEs
IDEs que funcionam no browser:
- JupyterLab
- Code Editor
- RStudio

Também é possível usar uma IDE local como o vs code e subir