import pandas as pd

class FormatadorDadosPagamentos:
    @staticmethod
    def formatar_valor_para_float(df):
        df["Valor"] = df["Valor"].map(lambda x: x[3::].replace(",", ".")).astype(float)
        return df

    @staticmethod
    def formatar_data_do_df_string_para_date(df):
        df["DataPagamento"] = pd.to_datetime(df["DataPagamento"], format="%d/%m/%Y")
        return df

    @staticmethod
    def ordenar_df_data(df):
        df = df.sort_values("DataPagamento")
        df = df.reset_index(drop=True)
        return df

    @staticmethod
    def separa_plano_meses_contrato(df):
        df["Meses"] = df['Plano'].str.rsplit("/", 1).str[-1]
        df['Meses'] = df['Meses'].astype(int)
        df["PlanoNormalizado"] = df['Plano'].str.rsplit("/", 1).str[0]
        return df

    @staticmethod
    def criar_chave_concatenada(df):
        df["chave"] = df["ClienteID"].map(str) + "-" + df["DataPagamento"].map(str) + "-" + df["Meses"].map(str)
        return df    
