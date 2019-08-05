import pytest
from pagamentos import DadosPagamentosCsv
import pandas as pd
import configparser

class TestDadosPagamentosCsv:    
    config = configparser.ConfigParser()
    config.read("pagamentos/config.cfg")

    def test_carregar_dados_csv_colunas(self):
        dados_pagamentos_csv = DadosPagamentosCsv(self.config)
        df = dados_pagamentos_csv.carregar_dados()
        assert (df.columns == ['ClienteID', 'DataPagamento', 'Valor', 'Plano']).all(), "As colunas não condizem com o teste"

    def test_carregar_dados_csv_e_data_frame(self):        
        dados_pagamentos_csv = DadosPagamentosCsv(self.config)
        df = dados_pagamentos_csv.carregar_dados()
        assert isinstance(df, pd.DataFrame), "carregar_dados_csv não retornou um data frame"
