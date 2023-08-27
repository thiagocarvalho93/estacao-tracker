import csv
import os
import logging
import smtplib
import email.message
import time
import requests

START_TIME = time.time()
API_URL = "https://api.weather.com/v2/pws/observations/current?apiKey={key}&stationId={id}&numericPrecision=decimal&format=json&units=m"
try:
    # Altere as variáveis abaixo com os valores correspondentes para rodar localmente
    API_KEY = os.environ["API_KEY"]
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
    RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
except KeyError as exc:
    logging.error("Token nao encontrado")
    raise KeyError from exc


def transformar_csv_para_lista(nome_arquivo: str):
    '''Transforma um arquivo csv em uma lista'''
    lista = []

    try:
        with open(nome_arquivo, "r", encoding='UTF-8') as csvfile:
            leitor = csv.reader(csvfile)
            for linha in leitor:
                lista.extend(linha)
    except FileNotFoundError:
        logging.error("O arquivo %s não foi encontrado.", nome_arquivo)
    return lista


def escrever_csv_da_lista(nome_arquivo: str, lista: list):
    '''Escreve um arquivo csv de uma lista'''

    with open(nome_arquivo, 'w', encoding="UTF-8") as arquivo:
        write = csv.writer(arquivo)
        write.writerow(lista)


def verificar_estacao_offline(id_estacao: str):
    '''Checa se a estação meteorológica está offline pelo seu id'''
    url = API_URL.format(key=API_KEY, id=id_estacao)
    status_offline = False

    try:
        response = requests.get(url, timeout=30000)
        if response.status_code == 200:
            mensagem = f"{id_estacao} online."
            logging.info(mensagem)
        else:
            mensagem = f"{id_estacao} offline! Enviando alerta..."
            status_offline = True
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
    return status_offline


def criar_corpo_email(lista_estacoes_offline: list, lista_estacoes_online: list):
    '''Cria o corpo do email baseado nas listas de estações que mudaram de status'''
    body = ""

    if len(lista_estacoes_offline) > 0:
        body += "<h3>🔴 As segunites estações agora estão offline:</h3>"
        body += "<ul>"
        for est in lista_estacoes_offline:
            body += f"<li>{est}</li>"
        body += "</ul>"

    if len(lista_estacoes_online) > 0:
        body += "<h3>🔵 As segunites estações agora estão online:</h3>"
        body += "<ul>"
        for est in lista_estacoes_online:
            body += f"<li>{est}</li>"
        body += "</ul>"

    return body


def enviar_email(corpo_email: str, assunto: str):
    '''Envia um email com o assunto e corpo especificados'''

    msg = email.message.Message()
    msg["Subject"] = assunto
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(corpo_email)
    msg_encoded = msg.as_string().encode("utf-8")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(msg["From"], SENDER_PASSWORD)
        server.sendmail(msg["From"], msg["To"], msg_encoded)
        server.quit()
        logging.info("Email enviado aos destinatários")
    except Exception as err:
        logging.error("Erro ao enviar o email: %s", err)


def main():
    '''Função principal a ser executada'''

    logging.info("Iniciando...")
    estacoes = transformar_csv_para_lista("estacoes.csv")
    offlines_antes = transformar_csv_para_lista("estacoes_offline.csv")

    offlines_atual = []
    for estacao in estacoes:
        is_offline = verificar_estacao_offline(estacao)
        if is_offline:
            offlines_atual.append(estacao)

    ficaram_off = list(set(offlines_atual).difference(offlines_antes))
    ficaram_on = list(set(offlines_antes).difference(offlines_atual))

    if len(ficaram_off) > 0 or len(ficaram_on) > 0:
        corpo_email = criar_corpo_email(ficaram_off, ficaram_on)
        assunto_email = "🚨 Alerta de estações"
        enviar_email(corpo_email, assunto_email)

    escrever_csv_da_lista("estacoes_offline.csv", offlines_atual)

    logging.info("Finalizando em %.2f s", (time.time() - START_TIME))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="programa.log",
                        format="%(asctime)s - %(levelname)s - %(message)s")
    main()
