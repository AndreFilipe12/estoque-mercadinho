🛒 CompraFácil — Controle de Estoque

Sistema web de controle de estoque desenvolvido com Python e Django, pensado para pequenos comércios, como mercadinhos de bairro.

O projeto foi construído com foco em uma operação simples de loja: cadastro de produtos, controle de entradas e saídas, acompanhamento do estoque, histórico de movimentações, filtros, alertas de estoque baixo e uma interface responsiva com identidade visual própria.

🔗 Repositório: https://github.com/AndreFilipe12/estoque-mercadinho

📌 Sobre o projeto

O CompraFácil nasceu como um projeto de estudo em Django e evoluiu para uma aplicação de estoque com fluxo próximo ao de um sistema comercial real.

A aplicação permite que o responsável pelo caixa/estoque faça o acompanhamento dos produtos de forma centralizada, reduzindo a necessidade de controles manuais.

Objetivos do projeto

Centralizar o cadastro e acompanhamento dos produtos.

Registrar entradas e saídas de estoque.

Identificar produtos próximos ou abaixo do estoque mínimo.

Consultar o histórico das movimentações.

Facilitar buscas e filtros.

Oferecer uma interface simples para a rotina de uma pequena loja.

✨ Funcionalidades

🔐 Autenticação

Tela de login personalizada.

Autenticação utilizando o sistema nativo do Django.

Proteção das páginas internas com login_required.

Logout com encerramento da sessão.

Redirecionamento automático para a tela de login quando o usuário não está autenticado.

Atualmente o projeto está configurado para uma operação simples com uma conta principal de acesso para o caixa/estoque. O Django permite evoluir posteriormente para múltiplos usuários e permissões.

📦 Produtos

Cadastro de produtos.

Edição de produtos.

Exclusão de produtos.

Código único para cada produto.

Categoria.

Quantidade atual em estoque.

Estoque mínimo.

Validação de dados do formulário.

Validação de código duplicado.

🔄 Movimentação de estoque

Registro de entradas.

Registro de saídas.

Atualização automática da quantidade em estoque.

Bloqueio de saída superior ao estoque disponível.

Campo para observação da movimentação.

Mensagem de confirmação após a operação.

📊 Dashboard

O dashboard apresenta:

Total de produtos.

Total de unidades em estoque.

Quantidade de produtos com estoque baixo.

Valor total estimado do estoque.

Produtos com estoque baixo posicionados primeiro na listagem.

Destaque visual para produtos que atingiram ou estão abaixo do estoque mínimo.

🔎 Busca e filtros

Busca por nome.

Busca por código.

Busca por categoria.

Filtro de categoria.

Paginação da lista de produtos.

🧾 Histórico de movimentações

Consulta de entradas e saídas.

Filtro por produto.

Filtro por tipo de movimentação.

Filtro por período.

Resumo das movimentações filtradas.

Total de movimentações.

Total de entradas.

Total de saídas.

Quantidade total movimentada.

🎨 Interface

Identidade visual do CompraFácil.

Tela de login com layout dividido e imagem de mercado.

Dashboard com cards e indicadores.

Formulários de cadastro, edição e movimentação padronizados.

Histórico com filtros e indicadores.

Notificações de sucesso em formato de toast.

Layout responsivo para telas menores.

🧰 Tecnologias utilizadas

Tecnologia

Utilização

Python

Linguagem principal

Django

Framework web

SQLite

Banco de dados local

HTML5

Estrutura das páginas

CSS3

Interface e responsividade

Django ORM

Acesso e consultas ao banco

Django Authentication

Login, sessão e autenticação

Git

Controle de versão

GitHub

Hospedagem do código

🗂️ Estrutura do projeto

estoque-mercadinho/
│
├── .gitignore
├── manage.py
│
├── controle_estoque/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   │
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_movimentacaoestoque.py
│   │   ├── 0003_alter_produto_preco.py
│   │   └── __init__.py
│   │
│   ├── static/
│   │   └── controle_estoque/
│   │       ├── style.css
│   │       └── img/
│   │           └── mercado.png
│   │
│   └── templates/
│       └── controle_estoque/
│           ├── editar_produto.html
│           ├── historico_movimentacoes.html
│           ├── home.html
│           ├── login.html
│           ├── movimentar_estoque.html
│           └── novo_produto.html
│
└── sistema_estoque/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

O arquivo db.sqlite3 é utilizado localmente durante o desenvolvimento e está no .gitignore, portanto não faz parte do repositório.

💻 Requisitos

Para executar o projeto localmente, você precisa ter instalado:

Python 3.14 ou compatível com o projeto.

pip.

Git.

Você pode verificar as versões com:

python --version
pip --version
git --version

🚀 Instalação e execução

1. Clonar o repositório

git clone https://github.com/AndreFilipe12/estoque-mercadinho.git

Entrar na pasta:

cd estoque-mercadinho

2. Criar o ambiente virtual

No Windows:

python -m venv venv

Ativar:

.\venv\Scripts\Activate.ps1

Caso esteja usando outro shell, utilize o comando de ativação correspondente ao seu ambiente virtual.

3. Instalar o Django

pip install django

4. Aplicar as migrations

python manage.py migrate

5. Criar o usuário de acesso

O projeto utiliza a autenticação nativa do Django. Para criar uma conta:

python manage.py createsuperuser

Informe o usuário, email e senha durante o processo.

6. Iniciar o servidor

python manage.py runserver

Acesse no navegador:

http://127.0.0.1:8000/login/

Depois do login, o usuário será direcionado para o dashboard.

🔑 Fluxo de autenticação

O fluxo atual é:

/login/
   ↓
Autenticação Django
   ↓
Dashboard
   ↓
Produtos / Movimentações / Histórico

As principais páginas internas utilizam proteção de autenticação.

🧪 Fluxo de uso

Um fluxo típico do CompraFácil é:

1. Login
   ↓
2. Dashboard
   ↓
3. Cadastrar produto
   ↓
4. Consultar estoque
   ↓
5. Registrar entrada ou saída
   ↓
6. Atualizar estoque automaticamente
   ↓
7. Consultar histórico

📦 Exemplo de movimentação

Supondo um produto com:

Estoque atual: 8
Estoque mínimo: 10

Ao registrar uma entrada de 12 unidades:

8 + 12 = 20

O estoque passa a ser 20.

Ao registrar uma saída de 5 unidades:

20 - 5 = 15

O estoque passa a ser 15.

O sistema também impede uma saída superior ao estoque disponível.

⚠️ Estoque baixo

O sistema considera estoque baixo quando:

quantidade em estoque <= estoque mínimo

Esses produtos:

recebem destaque visual;

aparecem primeiro na lista do dashboard;

são contabilizados no indicador de estoque baixo.

🔍 Histórico de movimentações

O histórico pode ser filtrado por:

produto;

tipo de movimentação;

data inicial;

data final.

O resumo da tela acompanha os filtros utilizados.

Exemplo:

Produto: Arroz Tio João 5kg
Tipo: Saídas
Período: 01/09/2026 até 24/09/2026

🔒 Segurança e boas práticas

O projeto já utiliza algumas práticas importantes:

autenticação nativa do Django;

proteção das páginas internas;

CSRF nos formulários POST;

senha armazenada pelo sistema de autenticação do Django, sem implementação manual de hash;

banco local e arquivos sensíveis fora do Git por meio do .gitignore.

Antes de colocar em produção

Ainda seria necessário revisar a configuração para ambiente de produção, incluindo:

DEBUG = False;

SECRET_KEY armazenada de forma segura;

ALLOWED_HOSTS configurado corretamente;

banco de dados adequado ao ambiente de produção;

HTTPS;

arquivos estáticos e mídia;

criação de rotina de backup.

Este repositório representa o projeto de desenvolvimento/portfólio e não deve ser considerado uma configuração de produção pronta sem essa revisão.

👨‍💻 Autor

André Filipe Reis Santos

Projeto desenvolvido para estudo e prática de desenvolvimento web com Python e Django.

GitHub

https://github.com/AndreFilipe12

Projeto

https://github.com/AndreFilipe12/estoque-mercadinho
