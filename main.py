import csv
import os
import requests
import logging

API_URL = "https://api.weather.com/v2/pws/observations/current?apiKey={key}&stationId={id}&numericPrecision=decimal&format=json&units=m"

try:
    API_KEY = os.environ["API_KEY"]
except KeyError:
    logging.error("Token nao encontrado")
    raise Exception

estacoes = []
logging.basicConfig(level=logging.INFO, filename="programa.log",
                    format="%(asctime)s - %(levelname)s - %(message)s")


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


setup()

for estacao in estacoes:
    verificar_status_estacao(estacao)
