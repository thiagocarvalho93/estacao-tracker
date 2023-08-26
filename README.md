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

Antes de executar o script, você precisará configurar algumas variáveis para que ele funcione corretamente. Aqui estão as configurações que você deve fazer:

1. **Configuração de Log:**

   O script utiliza o módulo de logging para registrar atividades. Você pode configurar o nível de log e o arquivo de registro no início do script:

   ```python
   import logging

   logging.basicConfig(level=logging.INFO, filename="programa.log",
                       format="%(asctime)s - %(levelname)s - %(message)s")
   ```

2. **Chaves de API e credenciais:**
O script requer algumas chaves de API e credenciais de e-mail para funcionar. Você pode definir essas variáveis como variáveis de ambiente ou diretamente no script:
  ```python
  API_KEY = os.environ["API_KEY"]
  SENDER_EMAIL = os.environ["SENDER_EMAIL"]
  SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
  RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
  ```
3. **Variáveis de Ambiente:**
Uma prática recomendada é definir as chaves de API e credenciais de e-mail como variáveis de ambiente. Isso ajuda a manter informações sensíveis fora do código-fonte. Certifique-se de definir essas variáveis no ambiente em que o script será executado.
Exemplo de como definir variáveis de ambiente no terminal:
  ```sh
  export API_KEY=sua_chave_de_api_aqui
  export SENDER_EMAIL=seu_email_de_envio
  export SENDER_PASSWORD=sua_senha_do_email
  export RECEIVER_EMAIL=email_de_receptor
  ```
Lembre-se de substituir os valores das variáveis acima pelos seus próprios valores de chave de API e credenciais de e-mail.

## Uso

Execute o script:

```sh
python main.py
```


