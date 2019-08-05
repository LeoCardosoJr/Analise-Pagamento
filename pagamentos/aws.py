import pandas as pd
import configparser
import pandas_redshift as pr

class Aws:

    def __init__(self, config):        
        self.aws_access_key_id = config.get('AWS_S3','aws_access_key_id')
        self.aws_secret_access_key = config.get('AWS_S3','aws_secret_access_key')
        self.bucket = config.get('AWS_S3','bucket')
        
        self.dbname = config.get('AWS_REDSHIFT','dbname')
        self.host = config.get('AWS_REDSHIFT','host')
        self.user = config.get('AWS_REDSHIFT','user')
        self.password = config.get('AWS_REDSHIFT','password')

        self.redshift_table_name = config.get('AWS_REDSHIFT','redshift_table_name')

    def conectar_s3(self):
        pr.connect_to_s3(aws_access_key_id=self.aws_access_key_id, 
            aws_secret_access_key=self.aws_secret_access_key, bucket=self.bucket)
        
    def conectar_redshift(self):
        pr.connect_to_redshift(dbname=self.dbname, host=self.host, user=self.user, 
            port=5439, password=self.password)

    def enviar_df_para_redshift(self, df):
        pr.pandas_to_redshift(data_frame=df, redshift_table_name=self.redshift_table_name)
