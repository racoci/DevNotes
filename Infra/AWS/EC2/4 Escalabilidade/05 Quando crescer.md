Vimos nessa aula como definir um grupo de auto scaling que consegue criar (ou encerrar) instâncias automaticamente para nós.

Quando um grupo de auto scaling pode criar uma nova instância?

- Alternativa incorreta
	- Quando a aplicação em uma das instâncias estiver lenta.
	- “Estar lenta” é um critério subjetivo. Precisamos ter critérios objetivos para que uma instância seja considerada “não saudável”.
    
- Alternativa correta
	- Quando uma outra instância do grupo for desligada ou encerrada.
	- Se alguma instância do grupo for desligada, o grupo criará uma nova para manter a capacidade desejada.
    
- Alternativa correta
	- Quando a aplicação em uma das instâncias estiver inacessível.
	- Ao configurar o grupo de auto scaling nós habilitamos verificações de integridade. Se uma das instâncias não estiver mais acessível, o grupo pode criar outra. Isso foi habilitado quando na Etapa 3 (Configurar opções avançadas) nós marcamos a opção ELB em “Verificações de integridade”.