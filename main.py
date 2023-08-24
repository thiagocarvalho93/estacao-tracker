import csv
import os
import logging
import smtplib
import email.message
import time
import requests

START_TIME = time.time()
logging.basicConfig(level=logging.INFO, filename="programa.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")

API_URL = "https://api.weather.com/v2/pws/observations/current?apiKey={key}&stationId={id}&numericPrecision=decimal&format=json&units=m"

try:
    API_KEY = os.environ["API_KEY"]
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
    RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
except KeyError as exc:
    logging.error("Token nao encontrado")
    raise KeyError from exc

estacoes = []
estacoes_offline = []


def setup():
    '''Setup inicial da aplicação'''

    try:
        with open("estacoes.csv", "r", encoding='UTF-8') as csvfile:
            leitor = csv.reader(csvfile)
            for linha in leitor:
                estacoes.extend(linha)
    except FileNotFoundError:
        logging.error("O arquivo estacoes.csv não foi encontrado.")


def verificar_status_estacao(id_estacao):
    '''Checa o status da estação meteorológica pelo seu id'''

    url = API_URL.format(key=API_KEY, id=id_estacao)

    try:
        response = requests.get(url, timeout=30000)
        if response.status_code == 200:
            mensagem = f"{id_estacao} online."
            logging.info(mensagem)
        else:
            mensagem = f"{id_estacao} offline! Enviando alerta..."
            estacoes_offline.append(id_estacao)
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


def enviar_email(lista_estacoes):
    '''Envia um email de alerta com a lista de estações especificada'''

    subject = "🚨 Alerta de estação offline"
    body = "<h3>As segunites estações estão offline:</h3>"
    body += "<ul>"
    for est in lista_estacoes:
        body += f"<li>{est}</li>"
    body += "</ul>"

    msg = email.message.Message()
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg["From"], SENDER_PASSWORD)
        server.sendmail(msg["From"], msg["To"],
                        msg.as_string().encode("utf-8"))
        server.quit()
        logging.info("Email enviado aos destinatários %s", RECEIVER_EMAIL)
    except Exception as err:
        logging.error("Erro ao enviar o email: %s", err)


if __name__ == '__main__':
    logging.info("Iniciando...")

    setup()

    for estacao in estacoes:
        verificar_status_estacao(estacao)

    if len(estacoes_offline) > 0:
        enviar_email(estacoes_offline)

    logging.info("Finalizando em %.2f s", (time.time() - START_TIME))
