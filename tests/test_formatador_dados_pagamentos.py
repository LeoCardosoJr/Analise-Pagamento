import pytest
from pagamentos import FormatadorDadosPagamentos
import pandas as pd

class TestFormatadorDadosPagamentos:
    def cria_data_frame_test(self):
        obj_pagamentos = {
            'ClienteID':        [3,             2,              1           ],
            'DataPagamento':    ['05/03/2017',  '12/08/2018',   '01/01/2017'],
            'Valor':            ['R$ 300,00',   'R$ 750,00',    'R$ 399,00'],
            'Plano':            ['Bronze/3',    'Ouro/3',       'Platina/1'] 
        }
        df = pd.DataFrame(data=obj_pagamentos)
        return df
        
    def test_formatar_valor_para_float_verifica_tipo(self):
        df = self.cria_data_frame_test()
        df = FormatadorDadosPagamentos.formatar_valor_para_float(df)
        
        assert df['Valor'].dtype == 'float64', "Valor deve ser formatado para 'Float'"
        
    def test_formatar_data_do_df_string_para_date_verifica_tipo(self):        
        df = self.cria_data_frame_test()
        df = FormatadorDadosPagamentos.formatar_data_do_df_string_para_date(df)
        
        assert df["DataPagamento"].dtype == 'datetime64[ns]', "DataPagamento deve ser formatado para 'datetime64[ns]'"

    def test_ordenar_df_data_verifica_se_ordenado(self):
        df = self.cria_data_frame_test()
        df = FormatadorDadosPagamentos.ordenar_df_data(df)
        result = df["ClienteID"].iloc[0] == 1 and df["ClienteID"].iloc[1] == 3 and df["ClienteID"].iloc[2] == 2
        
        assert result, "ordenar_df_data não ordenou corretamente"

    def test_separa_plano_meses_contrato(self):
        df = self.cria_data_frame_test()
        df = FormatadorDadosPagamentos.separa_plano_meses_contrato(df)
        
        erro = "separa_plano_meses_contrato não separou corretamente"
        
        assert df[df['ClienteID'] == 1]['Meses'].iloc[0] == 1, erro
        assert df[df['ClienteID'] == 1]['PlanoNormalizado'].iloc[0] == 'Platina', erro
        assert df[df['ClienteID'] == 2]['Meses'].iloc[0] == 3, erro
        assert df[df['ClienteID'] == 2]['PlanoNormalizado'].iloc[0] == 'Ouro', erro
        assert df[df['ClienteID'] == 3]['Meses'].iloc[0] == 3, erro
        assert df[df['ClienteID'] == 3]['PlanoNormalizado'].iloc[0] == 'Bronze', erro

    def test_criar_chave_concatenada(self):
        df = self.cria_data_frame_test()
        df.loc[:,"Meses"] = pd.Series([3, 3, 1], index=df.index)

        df = FormatadorDadosPagamentos.criar_chave_concatenada(df)
        erro = "criar_chave_concatenada não criou a chave corretamente"

        assert df[df['ClienteID'] == 1]['chave'].iloc[0] == '1-01/01/2017-1', erro
        assert df[df['ClienteID'] == 2]['chave'].iloc[0] == '2-12/08/2018-3', erro
        assert df[df['ClienteID'] == 3]['chave'].iloc[0] == '3-05/03/2017-3', erro
