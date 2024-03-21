import requests
import pandas as pd
import os
from dotenv import load_dotenv


class DadosRepositorios:

    def __init__(self, owner):
        load_dotenv()
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = str(os.getenv('access_token'))
        self.headers = {'Authorization': 'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        
    def lista_repositorios(self):
        repos_list = []

        for page_num in range (1, 20):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)

        return repos_list
    
    def nomes_repos(self, repos_list):
        repo_names = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except:
                    pass
        return repo_names

    def nomes_linguagens(self, repos_list):
        repo_languagens = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_languagens.append(repo['language'])
                except:
                    pass

        return repo_languagens
    
    def cria_df_linguagens(self):

        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados

amazon_rep = DadosRepositorios('amzn')
ling_main_usadas_amzn = amazon_rep.cria_df_linguagens()

netflix_rep = DadosRepositorios('netflix')
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens()

spotify_rep = DadosRepositorios('spotify')
ling_mais_usadas_spotify = spotify_rep.cria_df_linguagens()

# Salvando os dados
ling_main_usadas_amzn.to_csv('dados/linguagens_amzn.csv', index=False)
ling_mais_usadas_netflix.to_csv('dados/linguagens_netflix.csv', index=False)
ling_mais_usadas_spotify.to_csv('dados/linguagens_spotify.csv', index=False)