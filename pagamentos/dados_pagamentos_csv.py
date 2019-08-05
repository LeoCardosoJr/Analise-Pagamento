import pandas as pd

class DadosPagamentosCsv:

    def __init__(self, config):
        self.caminho_csv = config.get('CSV','caminho_csv')
        self.separador = config.get('CSV','separator')

    def carregar_dados(self):
        pd.options.display.float_format = '{:,.2f}'.format
        colunas = ['ClienteID', 'DataPagamento', 'Valor', 'Plano']
        df = pd.read_csv(self.caminho_csv, sep=self.separador, header=None, names=colunas)
        return df
