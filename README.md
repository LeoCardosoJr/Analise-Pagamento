# Análise de dados de Pagamentos de clientes
 
Análise de dados de pagamentos de clientes utilizando Python (Pandas e PyTest) e a Amazon Web Services (AWS) com os produtos (S3, Redshift e QuickSight)

Este programa importará os dados fará os cálculos que serão carregados para a AWS S3 e posteriormente armazenados no AWS Redshift, com isso, pode-se utilizar QuickSight (serviço de BI) e fazer a Análise gráfica dos dados.

## Instalação

Após clonar o repositório, edite o arquivo [config.cfg](https://github.com/LeoCardosoJr/Analise-Pagamento/blob/master/pagamentos/config.cfg) que esta dentro da pasta [pagamentos](https://github.com/LeoCardosoJr/Analise-Pagamento/tree/master/pagamentos) com os seus dados da amazon e localização dos dados dos clientes e pagamentos conforme os dados de exemplo [na pasta data](https://github.com/LeoCardosoJr/Analise-Pagamento/tree/master/data)

### Pré-requisitos

* Windows 10 com 64 bits
* [Python 3.6.6](https://www.python.org/downloads/release/python-366/)
* Conta na [AWS](https://aws.amazon.com/pt/)

### Instalação

É necessário instalar as bibliotecas utilizadas no projeto, que estão listadas dentro do [requirements.txt](https://github.com/LeoCardosoJr/Analise-Pagamento/blob/master/requirements.txt) e para isso, após abrir a pasta do projeto no prompt de comando do windows pode-se utilizar o comando abaixo:

```
python -m pip install -r requirements.txt
```

## Executando o programa

Para executar você pode abrir a pasta principal do projeto e executar o comando abaixo:
```
python app.py
```
Após isso o programa irá rodar, fazendo os cálculos e depois carregando os dados na AWS para que se possa fazer a análise de dados.

## Executando os testes

Para executar os testes você pode abrir a pasta principal do projeto e executar:
```
python -m pytest
```
O resultado deve ser similar ao da imagem abaixo:

![](https://leocardosojr.s3.sa-east-1.amazonaws.com/tests.png)

## Construído com

* [Python](https://github.com/python) - Linguagem de programação
* [PyTest](https://github.com/pytest-dev/pytest) - Framework de Testes
* [Pandas](https://github.com/pandas-dev/pandas) - Pacote construído para Python para análise de dados
* [Pandas Redshift](https://github.com/agawronski/pandas_redshift) - Pacote construído para Python para comunicação do pacote pandas com o Redshift da AWS
* [ConfigParser ](https://github.com/jaraco/configparser) - Pacote construído para Python para facilitar a alteração de configurações
