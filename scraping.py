from bs4 import BeautifulSoup
import pandas as pd
import requests


class Crawler:

    def obtem_html(self, url):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        response = requests.get(url, headers=header, verify=False)

        return response.content

    def gerando_df(self, content):

        soup = BeautifulSoup(content, 'html.parser')

        tabela = soup.find('table')

        str_tabela = str(tabela)

        tabela = pd.read_html(str_tabela)

        return tabela

    def executer(self, serie):

        conteudo = self.obtem_html(serie)

        df = self.gerando_df(conteudo)

        table = self.formater(df)

        return table


class CnnBrasilCrawler(Crawler):

    SERIEA_URL = "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-a-2022/"
    SERIEB_URL = "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-b-2022/"

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


class CbfCrawler(Crawler):

    SERIEA_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a'
    SERIEB_URL = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-b'

    def formater(self, table):

        serie = table[0]

        serie[['posicao', 'time']] = serie['Posição'].str.split(
            ' ', expand=True, n=1)

        serie[['time', 'estado']] = serie['time'].str.rsplit(
            ' ', expand=True, n=1)

        serie[['variação', 'time']] = serie['time'].str.split(
            ' ', expand=True, n=1)

        serie[['time', '-']] = serie['time'].str.split(
            ' ', expand=True, n=1)

        serie.drop(columns=['-'], inplace=True)

        serie.drop(columns=['Posição'], inplace=True)

        serie.drop(columns=['Próx'], inplace=True)

        serie = serie[['posicao', 'variação', 'time', 'estado', 'PTS', 'J',
                       'V', 'E', 'D', 'GP', 'GC', 'SG', 'CA', 'CV', '%', 'Recentes']]

        serie = serie.set_index('posicao')

        return serie


#crawler = Dados()
# print(crawler.executer(CnnBrasilCrawler.SERIEB_URL).to_string())

crawler = CbfCrawler()
print(crawler.executer(CbfCrawler.SERIEB_URL).to_string())
