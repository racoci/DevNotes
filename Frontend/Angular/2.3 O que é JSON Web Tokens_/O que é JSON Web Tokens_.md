## Introdução

Você já foi em algum evento que precisou apresentar um **documento de identificação** para comprovar que você era realmente a pessoa que comprou o ingresso? O ato de solicitar o documento de identificação é uma forma de **autenticação** para que você receba a **autorização** para entrar. Na web, esse processo funciona de forma parecida. Para fazer requisições de alguns serviços ou acessar páginas específicas, você precisa se identificar de alguma forma, e essa identificação precisa ser segura e única.

Neste artigo você vai compreender o que é o padrão JWT (sigla para “JSON Web Tokens”) para autenticação, muito usado na web. Também veremos:

- O que é um token;
- Para que serve e quando usar um JWT;
- Como criar e verificar seu JWT token.

[![Banner promocional da Alura, com um design futurista em tons de azul, apresentando o texto](https://www.alura.com.br/artigos/assets/imersao-front-end-2/imersao-front-end-2-banner-corpo-mobile.png)](https://www.alura.com.br/imersao-front-end?utm_source=blog&utm_medium=banner&utm_campaign=imersao-front-end-2)

## O que é um token?

Atualmente, ouvimos muito a palavra token relacionada a NFTs (sigla para “Tokens não fundíveis” em português), metaverso, criptomoedas, etc. Porém, fora desse meio, um token é uma **assinatura digital**, **uma chave**.

Quando você abre uma conta em um banco, você precisa definir uma senha e seus dados pessoais. Esses dados são convertidos em uma assinatura digital que vai identificar você de **forma única** para aquele banco e, toda vez que você acessar seu banco e entrar com sua senha e um dado pessoal, o banco entenderá e **confirmará** que você é aquele usuário logado, semelhante a entrarmos no evento quando apresentamos nosso documento de identidade.

Existem vários algoritmos e padrões que transformam suas informações em um token, isto é, uma chave de autenticação única, que faz sentido para o serviço ou aplicação que esteja tentando acessar no momento. Um desses padrões é o JWT, que é seguro por permitir uma autenticação entre duas partes através de um **token assinado**.

## O que é JWT?

Um JWT é um padrão para autenticação e troca de informações definido pela [RFC7519](https://datatracker.ietf.org/doc/html/rfc7519). Nele é possível armazenar de forma segura e compacta [objetos JSON](https://www.alura.com.br/artigos/o-que-e-json). Este token é um código Base64 e pode ser assinado usando um segredo ou par de chaves privadas/públicas.

Tokens assinados podem verificar a integridade das informações contidas neles, diferente de tokens criptografados que ocultam essas informações. Se um JWT é assinado por um par de chaves pública/privada, a **assinatura** certifica que a parte que possui a chave privada é quem de fato assinou.

### Quando e onde eu posso usar um JWT?

Você pode usar, por exemplo, em um cenário de **autorização.** Depois que o usuário estiver conectado, é possível observar cada solicitação e verificar se esta inclui o JWT, permitindo que o usuário acesse rotas, serviços e outros recursos.

Outro cenário de utilização de JWTs são as **trocas de informações** pois, como eles são assinados, é possível ter certeza de que os remetentes são quem dizem ser quem são. Além disso, podemos identificar se o conteúdo da assinatura foi alterado ou não devido à composição de um JWT.

### Como surgiu o JWT?

Ele faz parte de uma família de especificações: a família JOSE.

JOSE significa JSON _Object Signing and Encryption_, em português **Assinatura e criptografia de objetos JSON**. O JWT faz parte dessa família de especificações e representa o token. Abaixo, você confere outras especificações desta família:

- JWT (JSON Web Tokens): representa o token propriamente dito;
- JWS (JSON Web Signature): representa a assinatura do token;
- JWE (JSON Web Encryption): representa a assinatura para criptografia do token;
- JWK (JSON Web Keys): representa as chaves para a assinatura;
- JWA (JSON Web Algorithms): representa os algoritmos para assinatura do token.

Agora que você já sabe o que é, para que serve e quando usar um JWT, vamos entender mais a fundo como funciona e quais os componentes de um JWT. Vem comigo!

## Componentes básicos de um JSON Web Token

Um JWT possui uma estrutura básica composta pelo _header_, _payload_ e a _signature_. Essas três partes são separadas por pontos ( `.` ). Dessa forma, seria algo do tipo: `header.payload.signature`. Vamos entender melhor cada uma dessas partes!

### Header

Headers é o cabeçalho do token onde passamos basicamente duas informações: o `alg` que informa qual algoritmo é usado para criar a assinatura e o `typ` que indica qual o tipo de token.

```
{
    "alg": "HS256",
    "typ": "JWT"
}
```

### Payload

É onde os dados são armazenados. Pode conter informações como o identificador do usuário, permissões, expiração do token, etc.

```
{
    "email": "nome@alura.com.br",
    "password": "HuEKW489!j445*"
}
```

Como forma de ilustrar o uso do payload, usamos as informações de email e senha do usuário, mas o ideal é que você evite utilizar informações sensíveis. Usar senhas no payload do JWT é inseguro, pois os JWTs são frequentemente decodificados e lidos por clientes. Senhas expostas podem comprometer a segurança, já que os JWTs são assinados, mas não criptografados, permitindo acesso não autorizado a informações sensíveis.

É mais seguro armazenar apenas identificadores no JWT e manter as senhas em um local seguro no servidor.

### Signature

A assinatura do token (_signature_) é composta pela codificação do header e do payload somada a uma chave secreta e é gerada pelo algoritmo especificado no cabeçalho.

```
HS256SHA256(
    base64UrlEncode(header) + "." + base64UrlEncode(payload), secret_key)
```

O resultado são três strings separadas por pontos que podem ser facilmente utilizadas em ambientes HTML e protocolos HTTP.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Agora que entendemos como é “por dentro” um JWT vamos criar nosso próprio JSON Web Token!

## Criando um jwt token

Para começar, vamos criar uma pasta chamada `jwt` no diretório que você desejar. Crie um arquivo [JavaScript](https://www.alura.com.br/artigos/javascript) com o nome que escolher, eu estou utilizando `index.js`. Faça a instalação da `lib jwt` que escolher. Existem diversas libs que ajudam na geração de JWTs. Irei utilizar a [jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken) que é uma das mais populares, mas você pode ficar à vontade para explorar outras opções.

O primeiro passo é importar a lib no nosso arquivo:

```
const jwt = require('jsonwebtoken');
```

Agora criamos a nossa chave secreta. A ideia é que só você saiba a sua chave secreta e que ela seja difícil a fim de dificultar a ação de ataques maliciosos. A minha ficou desse jeito:

```
const secretKey = 'skljaksdj9983498327453lsldkjf';
```

Feito isso, vamos criar nosso token utilizando o método `sign`. Este método aceita como parâmetros o payload, a chave secreta e o header, nesta ordem.

```
const nossoToken = jwt.sign(
  {
    email: 'nome@alura.com.br',
    password: 'HuEKW489!j445*',
  },
  secretKey,
  {
    expiresIn: '1y',
    subject: '1',
  }
);
```

Para este JWT, eu estou informando um email e senha no payload; minha chave secreta; e no header estou informando um **subject,** que na biblioteca deste exemplo funciona como um id. Além disso, estou dizendo que nosso token **expira** em 1 ano. Por padrão, o algoritmo de codificação é o HS256.

Para visualizar a saída em nosso terminal, utilizei a biblioteca **Nodemon** que você pode instalar e ver como funciona acessando [este link](https://www.npmjs.com/package/nodemon). O nodemon é uma ferramenta que ajuda a desenvolver aplicativos baseados em [Node.JS](https://www.alura.com.br/artigos/node-js), reiniciando automaticamente o aplicativo quando são detectadas alterações de arquivo no diretório.

Podemos ver nosso token gerado passando a variável `nossoToken` em um `console.log`:

```
console.log(nossoToken);
```

A saída deve ser:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5vbWVAYWx1cmEuY29tLmJyIiwicGFzc3dvcmQiOiJIdUVLVzQ4OSFqNDQ1KiIsImlhdCI6MTY1MTY4MzUxNywiZXhwIjoxNjgzMjQxMTE3LCJzdWIiOiIxIn0.t0UuIAxJ1NPXANtlBOKfHfLsePF4LRPu4RA2WMkJl6A
```

## Verificando nosso JWT

Para verificar nosso token podemos utilizar um método da própria biblioteca [jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken) chamado `decode` passando o token gerado.

```
const tokenGerado = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im5vbWVAYWx1cmEuY29tLmJyIiwicGFzc3dvcmQiOiJIdUVLVzQ4OSFqNDQ1KiIsImlhdCI6MTY1MTY4MzUxNywiZXhwIjoxNjgzMjQxMTE3LCJzdWIiOiIxIn0.t0UuIAxJ1NPXANtlBOKfHfLsePF4LRPu4RA2WMkJl6A';

console.log(jwt.decode(tokenGerado));
```

A saída deste código é:

```
{
  email: 'nome@alura.com.br',
  password: 'HuEKW489!j445*',
  iat: 1651683517,
  exp: 1683241117,
  sub: '1'
}
```

Onde os parâmetros `iat`, `exp` e `sub` são respectivamente, as datas de criação e expiração, no formato UTC, em que o token foi criado e em que expirará, e o `subject` que passamos no nosso código com valor 1. Outra alternativa para verificar nosso token é acessando o link: [https://jwt.io/](https://jwt.io/). Neste caso, só precisamos passar o token gerado e iremos visualizar as informações decodificadas.

Agora, você deve estar se perguntando: “Agora que eu sei o que é e como funciona um JSON Web Token, como usá-lo em minhas aplicações front-end?”

Vamos descobrir!

## Autenticação com tokens

Imagine que você é uma pessoa desenvolvedora e está criando o front-end de uma aplicação para um banco. Na página de login você pega os dados dos usuários e envia esses dados para uma API utilizando o fetch ou axios, por exemplo.

```
fetch(`${baseUrl}/auth/login`, {
method: ‘POST’
      headers: {
       ‘Content Type’: ‘Application/json’,
      },
body: usuário,
})
.then((resposta) => {
...alguma coisa
})
.catch((erro) => {
...alguma coisa
});
```

O servidor irá pegar esses dados e, por meio de uma lógica, irá retornar um token que vai identificar aquele usuário. Agora, toda vez que este usuário logar na plataforma, ele passará por uma **autenticação** e, se estiver tudo certo com os dados, será **autorizado** a acessar determinadas áreas da aplicação, como ver o saldo. Geralmente essa **codificação** e **geração** de tokens é realizada pelo back-end, mas você precisará garantir que este usuário logado possa continuar acessando outras áreas da aplicação.

Você também pode salvar o token na _session storage_ ou _local storage_ do seu navegador, para garantir que, enquanto o token não expirar, o usuário permaneça logado na aplicação. Além disso, é importante que, ao efetuar o login, o usuário seja redirecionado para uma página Home, onde ele poderá ver outras funcionalidades da aplicação.

Quando este usuário tentar acessar a página que mostra o seu saldo, por exemplo, você pode fazer uma requisição, usando axios ou fetch passando no headers um campo “Authorization” com o token gerado. Isso irá fazer com que o servidor verifique se o usuário tem permissão ou não de acessar aquela página específica.

```
fetch(`${baseUrl}/saldo`, {
      headers: {
       ‘Authorization’: Token,
      },
})
.then((resposta) => {
...alguma coisa
})
.catch((erro) => {
...alguma coisa
});
```

Quando o usuário fizer _logout_ na nossa aplicação, você pode redirecioná-lo para outra página, e quando o token expirar, você redireciona o usuário para a página de login novamente.

## Conclusão

Quanta coisa legal não é mesmo?

Neste artigo, você entendeu o que são JSON Web Tokens, para que servem, quais seus componentes e como utilizá-los em suas aplicações. Você também viu como utilizar tokens em uma aplicação front-end para autenticação de usuários.

Na Alura, temos a [formação de Next.js](https://cursos.alura.com.br/formacao-next-js) que está espetacular! Você pode aplicar todo esse conhecimento de JWT em uma aplicação real no curso de **[Next.js: autenticação e gerenciamento de Tokens](https://cursos.alura.com.br/course/nextjs-autenticacao-gerenciamento-tokens)**.

Se deseja mergulhar mais fundo em JSON Web Tokens, recomendo este [Alura+](https://cursos.alura.com.br/extra/alura-mais/o-que-e-json-web-token-jwt--c203) do Vinicius Dias e também este curso de [Node.js e JWT: autenticação com tokens](https://cursos.alura.com.br/course/node-jwt-autenticacao-tokens)!

Vejo você lá!