import pytest
from pagamentos import CalculoDadosPagamento
from pagamentos import FormatadorDadosPagamentos as formata
import pandas as pd

class TestCalculoDadosPagamento:
    def cria_data_frame_test(self):
        obj_pagamentos = {
            'ClienteID':        [3,             2,              1,              1,              3,              2           ],
            'DataPagamento':    ['05/03/2017',  '12/08/2018',   '01/01/2017',   '01/02/2017',   '05/06/2017',   '01/02/2019'],
            'Valor':            ['R$ 300,00',   'R$ 750,00',    'R$ 399,00',    'R$ 300,00',    'R$ 750,00',    'R$ 750,00' ],
            'Plano':            ['Bronze/3',    'Ouro/3',       'Platina/1',    'Bronze/3',     'Ouro/3',       'Ouro/3'    ] 
        }
        df = pd.DataFrame(data=obj_pagamentos)
        df = formata.formatar_valor_para_float(df)
        df = formata.formatar_data_do_df_string_para_date(df)
        df = formata.separa_plano_meses_contrato(df)
        df = formata.criar_chave_concatenada(df)
        return df

    def test_calcular_mrr(self):
        erro = "calcular_mrr não calculou corretamente"

        df = self.cria_data_frame_test()
        df = CalculoDadosPagamento().calcular_mrr(df)
        
        assert df[df['ClienteID'] == 3]['MRR'].iloc[0] == 100, erro
        assert df[df['ClienteID'] == 1]['MRR'].iloc[0] == 399, erro
        assert df[df['ClienteID'] == 2]['MRR'].iloc[0] == 250, erro

    @pytest.mark.parametrize("mes, expected", [(0, 0), (1, 1), (3, 2), (599, 598), (-50, -50)])
    def test_subtrair_mes_se_maior_que_um(self, mes, expected):
        erro = "subtrair_mes_se_maior_que_um não calculou corretamente"

        result = CalculoDadosPagamento().subtrair_mes_se_maior_que_um(mes)
        
        assert result == expected, erro
       
    def test_calcular_new_mrr(self):      
        erro = "calcular_new_mrr não calculou corretamente"

        df = self.cria_data_frame_test()
        calculo = CalculoDadosPagamento()
        df = calculo.calcular_mrr(df)
        df = calculo.calcular_new_mrr(df)
        
        assert df[df['ClienteID'] == 3]['newMRR'].iloc[0] == 100, erro
        assert df[df['ClienteID'] == 1]['newMRR'].iloc[0] == 399, erro
        assert df[df['ClienteID'] == 2]['newMRR'].iloc[0] == 250, erro 

    def test_add_meses_registros_desagrupados_datas_mrr(self):
        erro = "add_meses_registros_desagrupados_datas_mrr não calculou corretamente"

        obj_pagamentos = {
            'DataPagamento':    ['01/03/2017',  '12/08/2018',   '01/01/2017'],
            'Meses':    [4,  2,   1],
        }
        df = pd.DataFrame(data=obj_pagamentos)

        calculo = CalculoDadosPagamento()
        df["DataPagamento"] = pd.to_datetime(df["DataPagamento"], format="%d/%m/%Y")
        df = calculo.add_meses_registros_desagrupados_datas_mrr(df)
        
        mes_validacao1 = df.loc[(df['Meses'] == 1), 'DataPagamento'].iloc[0]
        mes_validacao2 = df.loc[(df['Meses'] == 2), 'DataPagamento'].iloc[0]
        mes_validacao3 = df.loc[(df['Meses'] == 4), 'DataPagamento'].iloc[0]


        assert mes_validacao1 == pd.to_datetime('01/01/2017', format="%d/%m/%Y"), erro
        assert mes_validacao2 == pd.to_datetime('12/09/2018', format="%d/%m/%Y"), erro
        assert mes_validacao3 == pd.to_datetime('01/06/2017', format="%d/%m/%Y"), erro 

    def test_desagrupar_registros_em_pagamentos_mensais(self):
        erro = "desagrupar_registros_em_pagamentos_mensais não calculou corretamente"

        df = self.cria_data_frame_test()
        calculo = CalculoDadosPagamento()
        df = calculo.desagrupar_registros_em_pagamentos_mensais(df)
        df = formata.ordenar_df_data(df)
        
        mes_validacao1 = df.loc[(df['ClienteID'] == 3) & (df['Plano'] == 'Bronze/3'), 'DataPagamento'].iloc[0]
        mes_validacao2 = df.loc[(df['ClienteID'] == 3) & (df['Plano'] == 'Bronze/3'), 'DataPagamento'].iloc[1]
        mes_validacao3 = df.loc[(df['ClienteID'] == 3) & (df['Plano'] == 'Bronze/3'), 'DataPagamento'].iloc[2]

        assert mes_validacao1 == pd.to_datetime('05/03/2017', format="%d/%m/%Y"), erro
        assert mes_validacao2 == pd.to_datetime('05/04/2017', format="%d/%m/%Y"), erro
        assert mes_validacao3 == pd.to_datetime('05/05/2017', format="%d/%m/%Y"), erro 

    def test_calcular_cancelled_mrr(self):
        erro = "calcular_cancelled_mrr não calculou corretamente"    

        df = self.cria_data_frame_test()
        calculo = CalculoDadosPagamento()
        df = calculo.calcular_mrr(df)
        df = calculo.calcular_new_mrr(df)
        df = calculo.calcular_cancelled_mrr(df)
        df = formata.ordenar_df_data(df)
        print(df)

        mes_validacao1 = df.loc[(df['ClienteID'] == 1) & (df['MRR'] == 0), 'CancelledMRR'].iloc[0]
        mes_validacao2 = df.loc[(df['ClienteID'] == 2) & (df['MRR'] == 0), 'CancelledMRR'].iloc[0]
        mes_validacao3 = df.loc[(df['ClienteID'] == 3) & (df['MRR'] == 0), 'CancelledMRR'].iloc[0]

        assert mes_validacao1 == 100, erro
        assert mes_validacao2 == 250, erro
        assert mes_validacao3 == 250, erro 

    def test_calcular_contraction_expansion_e_resurrected_mrr(self):
        erro = "calcular_contraction_expansion_e_resurrected_mrr não calculou corretamente"    

        df = self.cria_data_frame_test()
        calculo = CalculoDadosPagamento()
        df = calculo.calcular_mrr(df)
        df = calculo.desagrupar_registros_em_pagamentos_mensais(df)

        df = formata.ordenar_df_data(df)
        df = formata.criar_chave_concatenada(df)
        df = calculo.calcular_new_mrr(df)

        df = formata.ordenar_df_data(df)
        df = calculo.calcular_cancelled_mrr(df)
        
        df = formata.ordenar_df_data(df)
        df = calculo.calcular_contraction_expansion_e_resurrected_mrr(df)
        
        valida_contraction  = df.loc[(df['chave'] == '1-2017-02-01 00:00:00-1'), 'ContractionMRR'].iloc[0]
        valida_expansion    = df.loc[(df['chave'] == '3-2017-06-05 00:00:00-1'), 'ExpansionMRR'].iloc[0]
        valida_resurrected  = df.loc[(df['chave'] == '2-2019-02-01 00:00:00-1'), 'ResurrectedMRR'].iloc[0]

        assert valida_contraction   == 299, erro
        assert valida_expansion     == 150, erro
        assert valida_resurrected   == 250, erro
