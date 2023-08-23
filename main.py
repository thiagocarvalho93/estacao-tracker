import csv
import os
import requests
import logging
import smtplib
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, filename="programa.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

API_URL = "https://api.weather.com/v2/pws/observations/current?apiKey={key}&stationId={id}&numericPrecision=decimal&format=json&units=m"

try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    logging.error("Token nao encontrado")
    raise Exception("Token nao encontrado")

estacoes = []
estacoes_offline = []

# Email configuration
# TODO usar variáveis de ambiente
sender_email = "your_email@example.com"
sender_password = "your_email_password"
receiver_email = "receiver@example.com"


def setup():
    '''Setup inicial da aplicação'''

    try:
        with open("estacoes.csv", "r", encoding='UTF-8') as csvfile:
            leitor = csv.reader(csvfile)
            for linha in leitor:
                estacoes.extend(linha)
    except FileNotFoundError:
        print("O arquivo estacoes.csv não foi encontrado.")


def verificar_status_estacao(id_estacao):
    '''Checa o status da estação meteorológica pelo seu id'''

    url = API_URL.format(key=API_KEY, id=id_estacao)

    try:
        response = requests.get(url, timeout=30000)
        if response.status_code == 200:
            mensagem = f"{id_estacao} online."
            print(mensagem)
            logging.info(mensagem)
        else:
            mensagem = f"{id_estacao} offline! Enviando alerta..."
            estacoes_offline.append(id_estacao)
            print(mensagem)
            logging.warning(mensagem)
    except requests.ConnectionError as conn_error:
        mensagem = "Erro de conexão:" + conn_error
        logging.error(mensagem)
    except requests.Timeout as timeout_error:
        mensagem = "Tempo limite excedido:" + timeout_error
        logging.error(mensagem)
    except requests.HTTPError as http_error:
        mensagem = "Erro HTTP:" + http_error
        logging.error(mensagem)
    except requests.RequestException as ex:
        mensagem = "Erro não esperado:" + ex
        logging.error(mensagem)


def enviar_email(estacoes):
    subject = "Alerta de estação offline"
    body = f"As estações {estacoes} estão offline."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Alert email sent.")
    except Exception as e:
        print("Error sending email:", e)


logging.info("Iniciando...")
setup()

for estacao in estacoes:
    verificar_status_estacao(estacao)

# if (estacoes_offline.count > 0):
#     enviar_email(estacoes_offline)

logging.info("Finalizando...")
