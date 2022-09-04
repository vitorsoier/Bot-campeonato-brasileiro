from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np

class arquivo():

    def obtem_html(self,url1, url2):
        header =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        req_serie_a = requests.get(url1, headers= header)
        req_serie_b = requests.get(url2, headers= header)

        return req_serie_a, req_serie_b

    def gerando_df(self, req1, req2):

        content_a = req1.content
        content_b = req2.content

        soup_a = BeautifulSoup(content_a, 'html.parser')
        soup_b = BeautifulSoup(content_b, 'html.parser')

        tabela_a = soup_a.find('table')
        tabela_b = soup_b.find('table')

        str_tabela_a = str(tabela_a)
        str_tabela_b = str(tabela_b)

        tabela_serie_a = pd.read_html(str_tabela_a)
        tabela_serie_b = pd.read_html(str_tabela_b)
        
        return tabela_serie_a, tabela_serie_b

    def formater(self, table1, table2):
       
        serie_a = table1[0]
        serie_b = table2[0]
    
        serie_a[['posicao', 'time']] = serie_a['Classificação'].str.split(' ', expand= True, n=1)
        serie_b[['posicao', 'time']] = serie_b['Classificação'].str.split(' ', expand= True, n=1)

        serie_a[['time', 'sigla']] = serie_a['time'].str.rsplit(' ', expand= True, n=1)
        serie_b[['time', 'sigla']] = serie_b['time'].str.rsplit(' ', expand= True, n=1)

        serie_a.drop(columns= ['Classificação'], inplace= True)
        serie_b.drop(columns= ['Classificação'], inplace= True)

        serie_a = serie_a[['posicao', 'time', 'sigla', 'p', 'j', 'v', 'e', 'd', 'g', 'gc', 'sg' ]]
        serie_b = serie_b[['posicao', 'time', 'sigla', 'p', 'j', 'v', 'e', 'd', 'g', 'gc', 'sg' ]]

        serie_a = serie_a.set_index('posicao')
        serie_b = serie_b.set_index('posicao')

        return serie_a, serie_b


"""pagina = arquivo()
hmlt1, html2 = pagina.obtem_html("https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-a-2022/", 
                            "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-b-2022/")
df1, df2 = pagina.gerando_df(hmlt1, html2)
serie_a, serie_b = pagina.formater(df1, df2)

print(serie_b.to_string())"""




        
