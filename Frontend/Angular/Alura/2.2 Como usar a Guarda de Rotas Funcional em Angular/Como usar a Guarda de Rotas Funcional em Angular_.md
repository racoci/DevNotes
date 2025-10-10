## Introdução

Quando se trata de desenvolvimento de aplicações web com Angular, o controle de acesso às rotas é uma peça fundamental na construção de sistemas seguros e confiáveis. É claro que só conseguimos garantir a segurança de uma aplicação com tratamentos no back-end. No entanto, um front-end protegido é um passo essencial para que essa segurança exista.

Para isso, é comum que na rotina de desenvolvimento com Angular se use as famosas "guardas de rotas", que são os guardiões que determinam quem pode ou não adentrar os portões das diversas páginas da sua aplicação. Porém, o Angular, com suas atualizações constantes e evolução, também passou por transformações nesse aspecto.

Até a versão 14 do Angular, as guardas de rotas eram implementadas por meio de classes que incorporavam interfaces fornecidas pela própria estrutura. Essas classes tinham a responsabilidade de definir quem tinha permissão para acessar certas rotas com base em lógica interna e na injeção de dependências.

Neste artigo, exploraremos essa transição, analisando como as guardas de rotas funcionais em Angular, representadas por funções, simplificaram a maneira de controlar o acesso a rotas em suas aplicações. Vamos compreender como essa abordagem simplificada impacta o desenvolvimento e oferece uma nova perspectiva sobre como garantir a segurança das páginas em suas aplicações Angular.

[![Banner promocional da Alura, com um design futurista em tons de azul, apresentando o texto](https://www.alura.com.br/artigos/assets/imersao-front-end-2/imersao-front-end-2-banner-corpo-mobile.png)](https://www.alura.com.br/imersao-front-end?utm_source=blog&utm_medium=banner&utm_campaign=imersao-front-end-2)

## Como usar a guarda de rotas funcional em Angular?

Ao trabalhar com Angular, as guardas de rotas são mecanismos que permitem controlar o acesso em uma aplicação, protegendo determinadas rotas, verificando se um usuário tem permissão para acessá-las. Até a versão 14 do Angular, as guardas de rotas eram implementadas por meio de classes que incorporavam interfaces fornecidas pela estrutura e habilitavam o controle do acesso com base nos métodos presentes na classe. Essa classe ficava parecida com o exemplo a seguir:

```

import { Injectable } from '@angular/core';
import { UserService } from "../services/user.service"
import { CanActivate, Router } from '@angular/router';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private router: Router, userService: UserService) {}

}
```

Nesse exemplo de guarda de rotas, há uma estrutura de classe com o decorator `@Injectable()`, que utilizava a interface `canActivate` para implementação. Essa classe possui um construtor que geralmente receberá a injeção de Router e de algum serviço que faça a verificação de acesso necessária para aquela rota determinada.

Nesse exemplo, estamos trabalhando com uma guarda de rotas para uma rota que só pode ser acessada após a pessoa usuária fazer login, portanto, tivemos que injetar um serviço que traz a informação de login da pessoa usuária nessa guarda de rotas.

Ainda, um método (nesse caso, `canActivate`) será chamado quando estivermos tentando acessar nossa página. Se o método retorna true, tudo está correto, e a pessoa usuária pode acessar a página. Se retornar falso, não conseguirá acessar a página, como podemos observar no exemplo a seguir:

```

import { Injectable } from '@angular/core';
import { UserService } from "../services/user.service"
import { CanActivate, Router } from '@angular/router';

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private router: Router, userService: UserService) {}

  canActivate(): boolean {
    if(userService.estaLogado()) {
        return true;
      } else {
        router.navigate(['/login']);
        return false;
      }
  }
}
```

No `app module`, adicionamos o `authGuard` aos providers e na constante que definimos com nossas rotas no arquivo `app-routing.module.ts`, adicionamos o `canActivate: [ authGuard ]` a rota que queremos proteger, logo após a definição do `path` e do `component`.

A partir do Angular 15, as classes como guardas de rotas se tornaram obsoletas, como podemos verificar na [documentação do Angular - DeprecatedGuard](https://angular.io/api/router/DeprecatedGuard).

> DeprecatedGuard(Guard obsoleta):
> 
> As classes **InjectionToken** e `@Injectable` para guardas e resolvedores foram descontinuadas em favor de funções JavaScript simples. A injeção de dependência ainda pode ser obtida usando a função inject de `@angular/core` e uma classe injetável pode ser usada como uma guarda funcional usando **inject**: `canActivate: [() => inject(myGuard).canActivate()]`.

Em outras palavras, nesse método, as funções desempenham o papel de guardas de rota, onde cada função retorna um valor booleano, o qual o **Angular emprega para decidir se uma rota é acessível ou não**.

Para observarmos como funciona essa nova abordagem, nós iremos refatorar a classe authGuard em uma guarda de rotas funcional.

Em um arquivo `authGuard.ts`, criamos uma função authGuard:

```
export const authGuard = () => {

}
```

Aqui não temos construtor, então usaremos `inject()` para realizar a injeção do serviço que captura o usuário logado e do Router:

```

import { inject } from "@angular/core"
import { UserService } from "../services/user.service"
import { Router } from "@angular/router"

export const authGuard = () => {
const userService = inject(UserService)
const router = inject(Router)
}
```

Em seguida inserimos a lógica de acesso à rota, conforme for necessário, retornando true ou false:

```
//imports ocultados

export const authGuard = () => {
const userService = inject(UserService)
const router = inject(Router)

  if(userService.estaLogado()) {
    return true;
  } else {
    router.navigate(['/login']);
    return false;
  }
}
```

Além disso, no arquivo `app.module.ts`, não é mais necessário inserir o serviço de guarda de rotas nos providers. Na constante que definimos com nossas rotas no arquivo `app-routing.module.ts`, adicionamos o `canActivate: [authGuard]` na rota que desejamos proteger, logo após a definição do `path` e do `component`:

```
// imports omitidos
import { authGuard } from './core/guards/auth.guard';

const routes: Routes = [
// rotas omitidas
  {
    path: 'perfil',
    component: PerfilComponent,
    canActivate: [authGuard]
  }
];
```

Essa mudança soa estranha para quem já tem o costume de trabalhar com Angular, já que aqui não há a injeção de dependências no construtor e essa guarda tem uma “carinha” de função que não estamos acostumados a encontrar no Angular.

Ou seja, a grande mudança é que, anteriormente, nós precisávamos de uma classe específica para implementar as guardas de rotas. Agora, uma simples função faz esse trabalho.

### E no que essa mudança implica?

A abordagem obsoleta, de criação de classes, oferece uma maior flexibilidade, uma vez que possibilita a utilização de Injeção de Dependência e oferece suporte a recursos mais avançados, incluindo o lazy loading. No entanto, como percebemos pela documentação, essa mudança foi realizada com intuito de promover o uso de funções JavaScript simples no Angular.

A abordagem funcional geralmente leva a um código mais simples e fácil de entender, pois é mais direta. Portanto, percebemos que aos poucos estamos vivenciando mudanças como essa abordagem funcional, que tornam a escrita mais amigável e consequentemente, atraem mais pessoas para o “lado Angular da força”.

![Gif do personagem Luke Skywalker, de Star Wars. O personagem aparece dos ombros para cima, virando o rosto em direção à câmera. Ao fundo há uma luz vermelha. No canto inferior direito há a frase escrita em letras brancas: “The force is with you, Young Skywalker”, que em português significa: “A força está com você, jovem Skywalker.”](https://www.alura.com.br/artigos/assets/guarda-de-rotas-funcional-angular/imagem1.gif)

## Conclusão

E se você gostou de conhecer essa nova abordagem de guardas de rotas no Angular, que tal dar uma olhada na nova formação [Desenvolva Aplicações Escaláveis com Angular](https://www.alura.com.br/formacao-aplicacoes-escalaveis-angular) para aprofundar seus conhecimentos e colocar em prática o uso das guardas de rotas funcionais e de outras ferramentas do Angular?

Além disso, não deixe de compartilhar suas experiências de aprendizado desse assunto marcando os perfis da Alura usando a #AprendiNaAlura nas suas redes sociais. Vamos mergulhar nesse conhecimento!