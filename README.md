# Divinópolis Transparency Monitor

Script em Python que consulta periodicamente informações salariais no Portal da Transparência de Divinópolis e envia os resultados automaticamente para o Telegram.

## Visão Geral

Este projeto utiliza Python e Playwright para acessar o Portal da Transparência de Divinópolis, pesquisar uma lista configurável de nomes e enviar as informações encontradas por meio de notificações no Telegram.

A execução é automatizada através do GitHub Actions.

## Funcionalidades

* Consulta automatizada ao Portal da Transparência de Divinópolis.
* Navegação em modo headless utilizando Playwright.
* Envio de notificações pelo Telegram.
* Execução automática com GitHub Actions.
* Configuração segura utilizando GitHub Secrets.
* Lista de nomes configurável.

## Tecnologias Utilizadas

* Python
* Playwright
* Requests
* Telegram Bot API
* GitHub Actions

## Estrutura do Projeto

```text
.
├── main.py
├── requirements.txt
└── .github
    └── workflows
        └── executar.yml
```

## Configuração

As informações sensíveis são armazenadas utilizando GitHub Secrets.

### Secrets necessários

| Secret               | Descrição                                         |
| -------------------- | ------------------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Token do bot do Telegram                          |
| `TELEGRAM_CHAT_ID`   | Chat ID para recebimento das notificações         |
| `NOMES_BUSCA`        | Lista de nomes a serem monitorados (um por linha) |

Exemplo:

```text
Fulano de Tal
Beltrano de Tal
Maria Silva
```

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/divinopolis-transparency-monitor.git
cd divinopolis-transparency-monitor
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Instale o Chromium do Playwright:

```bash
playwright install chromium
```

## Execução

Para executar manualmente:

```bash
python main.py
```

## Automação

O projeto foi desenvolvido para ser executado automaticamente pelo GitHub Actions.

A execução ocorre em horários pré-configurados e também pode ser iniciada manualmente através da aba **Actions** do GitHub.

## Segurança

Este projeto não armazena informações sensíveis no código-fonte.

As seguintes informações são protegidas por GitHub Secrets:

* Token do Telegram.
* Chat ID.
* Lista de nomes monitorados.

Nenhuma credencial, senha ou arquivo `.env` é enviado para o repositório.

## Aviso

As informações consultadas são provenientes do Portal da Transparência de Divinópolis e são de acesso público.

Este projeto tem finalidade educacional e de automação. O uso e a interpretação das informações obtidas são de responsabilidade do usuário.

## Licença

Este projeto está licenciado sob a licença MIT.
