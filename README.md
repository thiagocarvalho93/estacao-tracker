# Script de Monitoramento de Estações Meteorológicas

Este script em Python monitora o status de estações meteorológicas por meio de chamadas de API. Se uma estação ficar offline ou voltar pra online, ele envia alertas por e-mail.

## Recursos

- Monitora o status das estações meteorológicas definidas pelo usuário no arquivo "estacoes.csv" por meio de chamadas de API.
- Mantém um registro das estações que ficaram offline anteriormente no arquivo "estacoes_offline.csv".
- Compara o estado atual das estações offline com o estado anterior para determinar mudanças.
- Envia alertas por e-mail quando as estações ficam offline ou voltam para o status online.
- Fornece registro de atividades do script por meio de logs.

## Como Começar

### Pré-requisitos

- Python 3.x
- As bibliotecas Python necessárias estão listadas em `requirements.txt`.

### Instalação

1. Clone este repositório:

   ```sh
   git clone https://github.com//thiagocarvalho93/estacao-tracker.git
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure suas credenciais de e-mail e a configuração no script.
4. Modifique os nomes dos arquivos CSV e URLs de API conforme necessário.

## Configuração

Antes de executar o script, é necessário configurar algumas variáveis para que ele funcione corretamente. Aqui estão as configurações que você deve fazer:

1. **Chaves de API e Credenciais:**

   O script requer chaves de API e credenciais de e-mail para funcionar. Dependendo de onde você planeja executar o script, as configurações podem variar:

   - **Localmente:** Se você estiver executando o script localmente, você pode definir essas variáveis como variáveis de ambiente ou diretamente no script, substituindo o trecho de código em main.py:
   ```python
   API_KEY = os.environ["API_KEY"]
   SENDER_EMAIL = os.environ["SENDER_EMAIL"]
   SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
   RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
   ```
   Uma prática recomendada é definir as chaves de API e credenciais de e-mail como variáveis de ambiente. Isso ajuda a manter informações sensíveis fora do código-fonte. Certifique-se     de definir essas variáveis no ambiente em que o script será executado. Exemplo de como definir variáveis de ambiente no terminal:
   ```sh
   export API_KEY=sua_chave_de_api_aqui
   export SENDER_EMAIL=seu_email_de_envio
   export SENDER_PASSWORD=sua_senha_do_email
   export RECEIVER_EMAIL=email_de_receptor
   ```
   Lembre-se de substituir os valores das variáveis acima pelos seus próprios valores de chave de API e credenciais de e-mail.

   - **GitHub Actions:** Se estiver usando o GitHub Actions, você pode configurar essas variáveis como "Secrets" no GitHub. Configure as seguintes variáveis de ambiente no repositório:

     - `API_KEY`: Sua chave de API para acessar a API de estações meteorológicas.
     - `SENDER_EMAIL`: O endereço de e-mail do remetente para enviar alertas.
     - `SENDER_PASSWORD`: A senha do e-mail do remetente.
     - `RECEIVER_EMAIL`: O endereço de e-mail do destinatário para receber alertas.

1. **Configuração do Workflow (Opcional):**

   Se estiver usando o GitHub Actions, o fluxo de trabalho já está definido no arquivo `.github/workflows/actions.yml`. Ele será acionado automaticamente conforme agendado no arquivo.

2. **Configuração de Log (Opcional):**

   O script utiliza o módulo de logging para registrar atividades. Você pode configurar o nível de log e o arquivo de registro no início do script:

   ```python
   import logging
   
   logging.basicConfig(level=logging.INFO, filename="programa.log",
                       format="%(asctime)s - %(levelname)s - %(message)s")
   ```
## Uso

Aqui estão os passos básicos para executar o script:

1. **Localmente:**

   Se você estiver executando o script localmente, siga estas etapas:

   - Certifique-se de ter o Python 3.x instalado.
   - Clone o repositório:

     ```sh
     git clone https://github.com/seudigiteusuario/seurepo.git
     ```

   - Instale as dependências:

     ```sh
     pip install -r requirements.txt
     ```

   - Configure as variáveis de API e e-mail no script.
   - Execute o script:

     ```sh
     python main.py
     ```

2. **GitHub Actions:**

   Se você estiver usando o GitHub Actions, siga as etapas anteriores para configurar as variáveis de ambiente "Secrets" no repositório. O fluxo de trabalho já está definido no arquivo `.github/workflows/actions.yml`.

O script monitorará o status das estações meteorológicas e enviará alertas por e-mail quando necessário.

Lembre-se de substituir os valores das variáveis pelas suas próprias chaves de API e credenciais de e-mail.

## Contribuições

Contribuições são bem-vindas! Se encontrar problemas ou melhorias, por favor, envie uma solicitação de pull.
