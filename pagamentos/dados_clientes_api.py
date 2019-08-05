import pandas as pd

class DadosClientesApi:

    def __init__(self, config):        
        self.url = config.get('API_CLIENTES','url')

    def carregar_dados(self):
        clientes = pd.read_json(self.url)
        return clientes
