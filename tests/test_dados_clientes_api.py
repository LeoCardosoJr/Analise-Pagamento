import pytest
from pagamentos import DadosClientesApi
import pandas as pd
import configparser

class TestDadosClientesApi:    
    config = configparser.ConfigParser()
    config.read("pagamentos/config.cfg")

    def test_carregar_dados_csv_colunas(self):
        dados_clientes_api = DadosClientesApi(self.config)
        df = dados_clientes_api.carregar_dados()
        assert isinstance(df, type(pd.DataFrame())), "A API não retornou um DataFrame"
