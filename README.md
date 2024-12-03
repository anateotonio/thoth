# Thoth

Aplicação gamificada que facilita o aprendizado e o estudo de estudantes do ensino fundamental e médio, aumentando o engajamento e a motivação através de quizzes interativos e sistemas de recompensas.

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes tecnologias instaladas:

- **Python** (versão recomendada: 3.x)
- **PostgreSQL**

## Configuração Inicial

### Configurar Conexão com o Banco de Dados

1. Edite o arquivo `/utils/db.py` para ajustar as configurações de conexão ao PostgreSQL.
2. Certifique-se de incluir o nome do banco, usuário, senha e host corretamente.

### Criar a Tabela no Banco de Dados

Utilize o script SQL fornecido no arquivo `bd_script.sql` para criar o banco de dados e as tabelas necessárias.

### Instalar Dependências

Instale todas as bibliotecas necessárias listadas em `requirements.txt` com o seguinte comando:

```bash
pip install -r requirements.txt
```

## Como Executar a Aplicação

1. Acesse a pasta do projeto via linha de comando:

```bash
cd /caminho/para/o/projeto/rp2-thoth
```

2. Execute a aplicação:

```bash
python main.py
```

## Estrutura do Projeto

```plaintext
RP2-THOTH/
├── models/                   # Definições das classes e modelos 
├── routes/                   # Rotas da aplicação (endpoints)
├── services/                 # Camada de lógica de negócio e integração
│   ├── auth_service.py       # Serviço de autenticação
│   ├── professor_service.py  # Serviço relacionado a professores
│   └── student_service.py    # Serviço relacionado a estudantes
├── static/                   # Arquivos estáticos (CSS, JS, imagens, etc.)
├── templates/                # Templates HTML para renderização
├── utils/                    # Funções utilitárias e configuração
│   ├── db.py                 # Configuração do banco de dados
├── app.py                    # Ponto de entrada principal da aplicação
├── bd_script.sql             # Script SQL para criação do banco de dados
├── config.py                 # Configurações gerais do projeto
├── docker-compose.yml        # Configuração para o Docker Compose
├── Dockerfile                # Arquivo Docker para criação da imagem
└── requirements.txt          # Dependências do projeto
```

## Dicas Adicionais

- Certifique-se de que o PostgreSQL esteja em execução antes de iniciar a aplicação.
- Utilize ambientes virtuais Python para evitar conflitos de dependências:

```bash
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate     # Windows
```
