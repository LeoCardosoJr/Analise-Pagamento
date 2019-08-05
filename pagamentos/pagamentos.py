import pandas_redshift as pr
import pandas as pd
import configparser
from pagamentos import DadosPagamentosCsv
from pagamentos import DadosClientesApi
from pagamentos import FormatadorDadosPagamentos as formata
from pagamentos import CalculoDadosPagamento
from pagamentos import Aws

class Pagamentos:
    
    def __init__ (self, arquivo_conf):
        self.config = configparser.ConfigParser()
        self.config.read(arquivo_conf)

        self.df_pagamentos = pd.DataFrame()
        self.df_clientes = pd.DataFrame()
        self.df_resultado = pd.DataFrame()

    def carregar_dados_pagamentos(self):
        dados_pagamentos_csv = DadosPagamentosCsv(self.config)
        self.df_pagamentos = dados_pagamentos_csv.carregar_dados()

    def carregar_dados_clientes(self):
        dados_clientes_api = DadosClientesApi(self.config)
        self.df_clientes = dados_clientes_api.carregar_dados()        

    def preparar_dados_pagamentos(self):
        self.df_pagamentos = formata.formatar_valor_para_float(self.df_pagamentos)
        self.df_pagamentos = formata.formatar_data_do_df_string_para_date(self.df_pagamentos)
        self.df_pagamentos = formata.ordenar_df_data(self.df_pagamentos)
        self.df_pagamentos = formata.separa_plano_meses_contrato(self.df_pagamentos)
        self.df_pagamentos = formata.criar_chave_concatenada(self.df_pagamentos)

    def calcular_dados_pagamentos(self):
        calculo = CalculoDadosPagamento()
        
        self.df_pagamentos = calculo.calcular_mrr(self.df_pagamentos)
        self.df_pagamentos = calculo.desagrupar_registros_em_pagamentos_mensais(self.df_pagamentos)
        
        self.df_pagamentos = formata.ordenar_df_data(self.df_pagamentos)
        self.df_pagamentos = formata.criar_chave_concatenada(self.df_pagamentos)        
        self.df_pagamentos = calculo.calcular_new_mrr(self.df_pagamentos)

        self.df_pagamentos = formata.ordenar_df_data(self.df_pagamentos)
        self.df_pagamentos = calculo.calcular_cancelled_mrr(self.df_pagamentos)
        
        self.df_pagamentos = formata.ordenar_df_data(self.df_pagamentos)
        self.df_pagamentos = calculo.calcular_contraction_expansion_e_resurrected_mrr(self.df_pagamentos)

    def mesclar_dados_pagamentos_e_clientes(self):
        self.df_resultado = pd.merge(self.df_pagamentos, self.df_clientes, 
            left_on='ClienteID', right_on='id', how='inner')

    def enviar_dados_processados_para_redshift(self):
        aws = Aws(self.config)
        aws.conectar_s3()
        aws.conectar_redshift()
        aws.enviar_df_para_redshift(self.df_resultado)
