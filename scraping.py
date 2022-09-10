from bs4 import BeautifulSoup
import pandas as pd
import requests


class CnnBrasilCrawler:

    SERIEA_URL = "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-a-2022/"
    SERIEB_URL = "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-b-2022/"

    def obtem_html(self, url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        response = requests.get(url, headers=header)

        return response.content

    def gerando_df(self, content):

        soup = BeautifulSoup(content, 'html.parser')

        tabela = soup.find('table')

        str_tabela = str(tabela)

        tabela = pd.read_html(str_tabela)

        return tabela

    def formater(self, table):

        serie = table[0]

        serie[['posicao', 'time']] = serie['Classificação'].str.split(
            ' ', expand=True, n=1)

        serie[['time', 'sigla']] = serie['time'].str.rsplit(
            ' ', expand=True, n=1)

        serie.drop(columns=['Classificação'], inplace=True)

        serie = serie[['posicao', 'time', 'sigla',
                       'p', 'j', 'v', 'e', 'd', 'g', 'gc', 'sg']]

        serie = serie.set_index('posicao')

        return serie

    def executer(self, serie):

        conteudo = self.obtem_html(serie)

        df = self.gerando_df(conteudo)

        table = self.formater(df)

        return table


crawler = CnnBrasilCrawler()
print(crawler.executer(CnnBrasilCrawler.SERIEB_URL).to_string())


"""pagina = arquivo()
hmlt1, html2 = pagina.obtem_html("https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-a-2022/", 
                            "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-b-2022/")
df1, df2 = pagina.gerando_df(hmlt1, html2)
serie_a, serie_b = pagina.formater(df1, df2)

print(serie_b.to_string())"""
