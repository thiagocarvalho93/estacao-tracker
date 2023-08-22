import csv
import requests

API_URL = "https://api.weather.com/v2/pws/observations/current?apiKey={key}&stationId={id}&numericPrecision=decimal&format=json&units=m"
API_KEY = "e1f10a1e78da46f5b10a1e78da96f525"

estacoes = []


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
            print(f"Estação {id_estacao} está online.")
        else:
            print(f"Estação {id_estacao} está offline! Enviando alerta...")
    except requests.ConnectionError as conn_error:
        print("Erro de conexão:", conn_error)
    except requests.Timeout as timeout_error:
        print("Tempo limite excedido:", timeout_error)
    except requests.HTTPError as http_error:
        print("Erro HTTP:", http_error)
    except requests.RequestException as ex:
        print("Erro não esperado:", ex)


setup()

for estacao in estacoes:
    verificar_status_estacao(estacao)
