# Angular: como funciona um componente?

## O que é componente?

Imagine que você aguardou por meses pelo show da sua banda favorita, e quando chega o grande dia, o show é cancelado, pois um dos membros não pode comparecer. Esse membro pode ser o vocalista, guitarrista ou baterista, importante para que a banda exista, pois só assim conseguem fazer os shows e produzir suas músicas. O mesmo acontece no Angular, pois todo o desenvolvimento de uma aplicação é baseado em componentes, e cada um é importante para uma aplicação.

Componente é uma parte da composição de um todo, algo que compõe ou ajuda na composição de algo, por exemplo um baterista de uma banda. Já no desenvolvimento de softwares, é descrito como uma unidade de uma aplicação que junta de outras unidades fazem parte de um sistema maior. E a construção de vários componentes é chamado de componentização.

A componentização é algo útil pois permite a reutilização de trechos de código, isolamento de contexto, diminuição de tags das páginas, melhor leitura do código e padronização do projeto. Frameworks como, [React](https://www.alura.com.br/artigos/react-js) e Vue utilizam esse método na construção de aplicações. Mas hoje você verá como isso se aplica no Angular.

Segundo a documentação do Angular, o componente é o principal bloco de construção para aplicativos, e é composto por um template, um estilo e uma classe. É no template que encontraremos toda a estrutura HTML, a árvore DOM do componente. Já o estilo é onde será feita a estilização, e a classe onde é definido o comportamento e a lógica feita em Typescript.

Para configurar um componente, no arquivo TS é passado o decorador `@Component`, importado da lib ‘@angular/core’. Esse decorador é um método que recebe um objeto com os metadados como parâmetro. É criado um seletor, que será usado como tag HTML em outro template, o template passando o caminho do arquivo HTML, mas pode ser passado inline, e o arquivo de folha de estilo ou, assim como o template, passado inline.

```
import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'sobre-componente';
}
```

Também temos a classe onde adicionamos propriedades e comportamentos ao componente.

Para ficar mais claro, crie uma nova aplicação com o Angular CLI, `ng new sobre-componente`. Não precisa de App Routing e o estilo fica à sua escolha. Com o projeto criado, serão gerados vários arquivos, dentre eles uma pasta chamada `app`. Nesta pasta estão os arquivos do AppComponent, principal componente da aplicação. É por meio do seletor deste componente que é passado para o `index.html` que toda aplicação vai poder ser vista pelo usuário.

```
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sobre Componente</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
</head>
<body>
  <!-- Tag AppComponent -->
  <app-root></app-root>
</body>
</html>
```

Com auxílio do Angular CLI, crie um novo componente usando o comando `ng generate component botao` ou usando abreviação `ng g c botao`, e veja o que acontece. Abaixo podemos ver o que o comando realizou. Os arquivos HTML, CSS e Typescript gerados e uma modificação no AppModule, no caso a declaração do novo componente.

```
$ ng g c components/botao
CREATE src/app/components/botao/botao.component.html (20 bytes)
CREATE src/app/components/botao/botao.component.spec.ts (619 bytes)
CREATE src/app/components/botao/botao.component.ts (271 bytes)     
CREATE src/app/components/botao/botao.component.css (0 bytes)      
UPDATE src/app/app.module.ts (553 bytes)
```

Após ser criado, o arquivo TS do BotaoComponent é bem parecido com a do AppComponent.

```
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-botao',
  templateUrl: './botao.component.html',
  styleUrls: ['./botao.component.css']
})
export class BotaoComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
```

Todo componente precisa ser declarado em um módulo para poder ser utilizado na aplicação.

```
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { BotaoComponent } from './botao/botao.component';

@NgModule({
  declarations: [
    AppComponent,
    BotaoComponent,
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
```

Para utilizar o componente botão que você criou, use o seletor `'app-botao'`, e insira no template do AppComponent.

```
<header >
  <div class="container">
   <h4>
     Component Botão - Alura
   </h4>
  </div>
</header>
<section class="container">
  <app-botao></app-botao>
</section>
```

E com um pouco de estilização o resultado é esse:

![Aplicação em Angular com uma barra azul na parte superior com o texto “Componentes com Angular”, e logo abaixo, em um fundo branco, um botão cinza com o texto “Botão” na cor branca.](https://www.alura.com.br/artigos/assets/angular-como-funciona-um-componente/imagem1.png)

E esse componente pode ser reutilizado várias vezes.

![Aplicação em Angular de cores azul e branca, no cabeçalho está escrito Componentes com Angular e no corpo da aplicação existem 3 botões cinza com a palavra Botão.](https://www.alura.com.br/artigos/assets/angular-como-funciona-um-componente/imagem2.png)

```
<header >
  <div class="container">
   <h4>
     Componentes com Angular
   </h4>
  </div>
</header>
<section class="container">
  <app-botao></app-botao>
  <app-botao></app-botao>
  <app-botao></app-botao>
  <app-botao></app-botao>
</section>
```

Quando criamos um componente, o objetivo é fazer com que ele possa ser reutilizado em outras partes do código, para isso é necessário deixar esse botão o mais flexível possível. Para isso, vamos usar o decorator `@Input()`, que permite a entrada de dados do componente pai.

```
export class BotaoComponent {
  @Input() btnConfigs: any;

  constructor() { }
}
```

Agora no componente pai, no caso o AppComponent, vamos criar objetos contendo um título para o botão e um estilo.

```
export class AppComponent {
  title = 'sobre-componente';

  primary = {
      titulo: 'Editar',
      styles: { backgroundColor: '#007bff' }
  };

  secondary = {
    titulo: 'Desabilitado',
    styles: { backgroundColor: '#6c757d' }
  };

  success = {
    titulo: 'Salvar',
    styles: { backgroundColor: '#28a745' },
  };

  danger = {
    titulo: 'Deletar',
    styles: { backgroundColor: '#dc3545' }
  };
}
```

Com as propriedades prontas, vamos até o template onde criamos os botões e criar um atributo property binding onde o `btnConfigs` vai receber o objeto que criamos no AppComponent.

```
<section class="container">
  <app-botao [btnConfigs]="primary"></app-botao>
  <app-botao [btnConfigs]="secondary"></app-botao>
  <app-botao [btnConfigs]="success"></app-botao>
  <app-botao [btnConfigs]="danger"></app-botao>
</section>
```

![Aplicação em Angular de cores azul e branca, no cabeçalho está escrito Componentes com Angular e no corpo da aplicação existem 4 botões de cores diferentes na posição vertical, o primeiro está é azul e está escrito Editar, o segundo é cinza e está escrito Desabilitar, o terceiro é verde e está escrito Salvar e o quarto é vermelho e está escrito Deletar.](https://www.alura.com.br/artigos/assets/angular-como-funciona-um-componente/imagem3.png)

Com as configurações chegando no BotaoComponent, podemos usá-las na estrutura do botão, colocando o estilo e o título. No HTML, vamos usar o property binding no ngStyle para receber o valor da propriedade que recebemos pelo `@Input()` e fazer uma interpolação para o título. E já vamos criar um evento de click para chamar o método alert.

```
<button
  class="button"
  [ngStyle]="btnConfigs.styles"
  (click)="alert()" >
  {{btnConfigs.titulo}}
</button>
```

O evento alert vai mostrar uma mensagem com o título do botão.

```
export class BotaoComponent {
  @Input() btnConfigs: any;

  constructor() { }
  alert() {
    alert(this.btnConfigs.titulo);
  }
}
```

E esse será o resultado.

![Imagem com os mesmos 4 botões, mas com um pop-up com o título do botão clicado, no caso Editar.](https://www.alura.com.br/artigos/assets/angular-como-funciona-um-componente/imagem4.png)

### Conclusão

O componente é uma das partes mais importantes de uma aplicação Angular, eles são os elementos que possibilitam criar funcionalidades da view. Conhecemos como criá-los e como são estruturados. Vimos também como utilizá-los, deixando a responsabilidade de estilização e título para o componente pai, e como adicionar um evento simples. Espero que a partir daqui você consiga explorar cada vez mais o universo Angular.

Quer utilizar esse código para explorar o que aprendeu? [Clica aqui](https://github.com/alura-cursos/sobre-componente/archive/refs/heads/main.zip) para baixar o projeto e mergulhar ainda mais no mundo do Angular!