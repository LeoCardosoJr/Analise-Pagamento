import pandas as pd
from pagamentos import FormatadorDadosPagamentos as formata

class CalculoDadosPagamento:

    def calcular_mrr(self, df):
        df['MRR'] = df['Valor'] / df['Meses']
        return df

    def subtrair_mes_se_maior_que_um(self, mes):
        if mes > 1:
            novo_mes = mes - 1
        else:
            novo_mes = mes
        
        return novo_mes

    def calcular_new_mrr(self, df):
        df_new_mrr = df.groupby('ClienteID').first()["chave"]
        df["newMRR"] = df[df["chave"].isin(df_new_mrr.values)]["MRR"]
        df["newMRR"].fillna(0, inplace=True)
        return df

    def desagrupar_registros_em_pagamentos_mensais(self, df):
        new_df = pd.DataFrame()

        for i in range(df["Meses"].max()):
            new_df = pd.concat([new_df, df[df["Meses"] > 1]], ignore_index=True)
            df["Meses"] = df["Meses"].apply(self.subtrair_mes_se_maior_que_um)
            df[df["Meses"] > 1]
        
        new_df = formata.criar_chave_concatenada(new_df)
        df = pd.concat([new_df, df], ignore_index=True)
        df = self.add_meses_registros_desagrupados_datas_mrr(df)

        return df

    def add_meses_registros_desagrupados_datas_mrr(self, df):
        df["DataPagamento"] = df.apply(lambda x: x["DataPagamento"] + pd.DateOffset(months = x["Meses"] - 1), axis=1)
        return df


    def calcular_cancelled_mrr(self, df):
        df["CancelledMRR"] = 0
        new_df = pd.DataFrame()

        chave_df_cancelled_mrr = df.groupby('ClienteID').last()["chave"]
        cancelled_mrr = df["chave"].isin(chave_df_cancelled_mrr.values)    
        data_ultimoMes = self.retornar_data_ultimo_mes_e_dez_dias() > df["DataPagamento"]

        new_df = pd.concat([new_df, df[(cancelled_mrr) & (data_ultimoMes)]], ignore_index=True)
        new_df["CancelledMRR"] = new_df["MRR"]
        new_df["DataPagamento"] = new_df.apply(lambda x: x["DataPagamento"] + pd.DateOffset(months = 1), axis=1)
        
        new_df.loc[:, ["MRR", "newMRR", "Valor", "Plano", "Meses", "PlanoNormalizado"]] = 0
        new_df = formata.criar_chave_concatenada(new_df)
        df = pd.concat([new_df, df], ignore_index=True)
        return df

    def calcular_contraction_expansion_e_resurrected_mrr(self, df):
        
        for i, row in enumerate(df.itertuples(), 1):        
        
            if row.newMRR == 0 and row.CancelledMRR == 0:
                primeiro_dia_mes_anterior = self.retornar_primeiro_dia_mes_anterior(row.DataPagamento)
                
                is_cliente_id = df["ClienteID"] == row.ClienteID
                is_mais_novo_que_mes_anterior = df["DataPagamento"] >= primeiro_dia_mes_anterior
                is_mais_antigo_que_registro = df["DataPagamento"] < row.DataPagamento
                
                registro_mes_anterior = df[is_cliente_id & is_mais_novo_que_mes_anterior & is_mais_antigo_que_registro].iloc[-1:]

                if registro_mes_anterior.empty:
                    df.loc[df.index == row.Index, "ResurrectedMRR"] = row.MRR
                elif row.MRR == registro_mes_anterior["MRR"].item():
                    continue
                elif row.MRR < registro_mes_anterior["MRR"].item():
                    df.loc[df.index == row.Index, "ContractionMRR"] = registro_mes_anterior["MRR"].item() - row.MRR
                elif row.MRR > registro_mes_anterior["MRR"].item():
                    df.loc[df.index == row.Index, "ExpansionMRR"] = row.MRR - registro_mes_anterior["MRR"].item()


        if "ResurrectedMRR" in df.columns:
            df["ResurrectedMRR"].fillna(0, inplace=True)

        if "ContractionMRR" in df.columns:
            df["ContractionMRR"].fillna(0, inplace=True)

        if "ExpansionMRR" in df.columns:
            df["ExpansionMRR"].fillna(0, inplace=True)

        return df

    def retornar_data_ultimo_mes_e_dez_dias(self):
        mes_anterior = pd.DateOffset(months = -1, days = -10) + pd.datetime.now()
        return mes_anterior

    def retornar_primeiro_dia_mes_anterior(self, data_pagamento):
        mes_anterior = pd.DateOffset(months = -1) + data_pagamento
        return mes_anterior.replace(day=1)
