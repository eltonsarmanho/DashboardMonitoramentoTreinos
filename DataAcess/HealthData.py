import sys
import os
#Add Raiz ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
import re

from DataAcess.TrainingDataPolar import TrainingDataPolar

class HealthData:
    def __init__(self, file_path='../Data/bioData.json'):
        project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
        file_path = os.path.join(project_root, '..', 'Data', 'bioData.json')

        # Criar uma instância da classe TrainingData
        training_data = TrainingDataPolar(file_path)

        self.df = training_data.getData()
        self.preprocess_data()

    def _get_metrics(self):
        
        # Filtrando dados por mês e ano
        return self.df[['calories', 'duration', 'heart_rate_avg', 'heart_rate_max']].rename(columns={
            'calories': 'Calorias',
            'duration': 'Duração',
            'heart_rate_avg': 'Frequência Cardíaca Média',
            'heart_rate_max': 'Frequência Cardíaca Máxima'
        })
    
   
    def get_last_n_days_avg(self, n):
        """
        Retorna a média dos últimos N dias registrados no dataset para as métricas:
        'calories', 'duration', 'heart_rate_avg' e 'heart_rate_max'.

        Parameters
        ----------
        n : int
            Número de dias recentes a considerar.

        Returns
        -------
        dict
            Dicionário contendo as médias das métricas especificadas.
        """
        if self.df.empty:
            return {
                'calories': None,
                'duration': None,
                'heart_rate_avg': None,
                'heart_rate_max': None
            }
        
        # Ordenar por data mais recente
        filtered_df = self.df.sort_values(by='start_time', ascending=False).head(n) 
        # Filtrar os últimos N dias registrados
        
        # Calcular médias
        averages = filtered_df[['calories', 'duration', 'heart_rate_avg', 'heart_rate_max']].mean().round(2).to_dict()
        
        return averages
    
    def preprocess_data(self):
        # Remover o dia da semana do campo 'start_time' e converter para datetime
        self.df['start_time'] = self.df['start_time'].apply(
            lambda x: re.match(r'\d{2}/\d{2}', x).group(0) + '/2024')
        self.df['start_time'] = pd.to_datetime(self.df['start_time'], format='%d/%m/%Y')

        # Ajustar o tamanho dos pontos e formatar as datas no hover
        self.df['Data'] = self.df['start_time'].dt.strftime('%d/%m/%Y')

        X = self.df[['heart_rate_avg', 'calories', 'duration']]
        # Aplicar KMeans para segmentação dos dados em clusters
        self.kmeans = KMeans(n_clusters=3,  n_init=10,random_state=0).fit(X)
        self.df['cluster'] = self.kmeans.labels_
        self.df['month'] = self.df['start_time'].dt.month
        self.df['year'] = self.df['start_time'].dt.year

        # Calcular a média de frequência cardíaca e calorias por cluster
        cluster_means = self.df.groupby('cluster')[['heart_rate_avg', 'calories']].mean()

        # Ordenar os clusters por calorias e atribuir rótulos baseados nas médias
        sorted_clusters = cluster_means.sort_values(by='calories')
        cluster_labels = {sorted_clusters.index[0]: 'Baixa Intensidade',
                          sorted_clusters.index[1]: 'Intensidade Moderada',
                          sorted_clusters.index[2]: 'Alta Intensidade'}

        # Atribuir os rótulos categorizados aos clusters no DataFrame
        self.df.loc[:, 'cluster_category'] = self.df['cluster'].map(cluster_labels)
   
    def getDadosTempo(self):
    # Criando o dicionário de meses automaticamente
        self.nomes_meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        self.meses_dict = {mes: i for i, mes in enumerate(self.nomes_meses, start=1)}

        # Definição de constantes para os anos
        ANO_INICIAL = 2024
        ANO_FINAL = 2030

        # Gerando a lista de anos únicos
        anos_unicos = list(range(ANO_INICIAL, ANO_FINAL + 1))
        return self.meses_dict, anos_unicos
    
    def get_mes_pelo_indice(self,indice):
        """
        Retorna o nome do mês pelo índice (1-12).
        
        Parameters
        indice : int
            Índice do mês (1-12).
        
        Returns
        -------
        str
            Nome do mês referente ao índice.
        """           
        
        if 1 <= indice <= 12:
            return self.nomes_meses[indice - 1]  # Ajuste para índice começar do 1
        else:
            return "Índice inválido"
   
    def create_clustered_bar_chart(self, selected_month=10, selected_year=2024):
        # Filtrando dados por mês e ano
        filtered_df = self.df[(self.df['month'] == selected_month) & (self.df['year'] == selected_year)].copy()

        # Se o DataFrame filtrado estiver vazio, retorna um gráfico vazio
        if filtered_df.empty:
            fig = px.bar(filtered_df, x='cluster_category', y='calories',
                         color='cluster_category', color_discrete_map={},
                         labels={'calories': 'Calorias Queimadas', 'cluster_category': 'Intensidade do Treino'},
                         title=f'Sem registros disponíveis para este período.')
            return fig


        # Definir cores para cada categoria de cluster
        color_map = {
            'Baixa Intensidade': 'green',
            'Intensidade Moderada': 'blue',
            'Alta Intensidade': 'red'
        }

        # Criar gráfico de barras para mostrar a relação de calorias por cluster
        fig = px.bar(filtered_df, x='cluster_category', y='calories',
                     color='cluster_category', color_discrete_map=color_map,
                     labels={'calories': 'Calorias Queimadas', 'cluster_category': 'Intensidade do Treino'},
                     title=f'Distribuição de Calorias Queimadas por Intensidade de Treino ({selected_month}/{selected_year})')

        return fig

    def get_chart_line(self,selected_month=10, selected_year=2024,y_col='Calorias'):
        """
        Gera um gráfico de dispersão com tendência para a variável escolhida ao longo dos dias.
        
        Parameters
        ----------
        selected_month : int
            Mês selecionado para filtragem dos dados.
        selected_year : int
            Ano selecionado para filtragem dos dados.
        y_col : str
            Coluna a ser usada no eixo Y.
        
        Returns
        -------
        plotly.graph_objects.Figure
            Gráfico gerado.
        """
        df_aux = self.df[(self.df['month'] == selected_month) & (self.df['year'] == selected_year)].copy()
        
        
        
        df_aux =df_aux[['calories', 'duration', 'heart_rate_avg', 'heart_rate_max','start_time','cluster_category']].rename(columns={
            'calories': 'Calorias',
            'duration': 'Duração',
            'heart_rate_avg': 'Frequência Cardíaca Média',
            'heart_rate_max': 'Frequência Cardíaca Máxima',
            'start_time': 'Dias'
        })

        # Definir cores para cada categoria de cluster
        color_map = {
            'Baixa Intensidade': 'green',
            'Intensidade Moderada': 'blue',
            'Alta Intensidade': 'red'
        }


        if df_aux.empty:
            return px.scatter(df_aux, x='Dias', y=y_col, trendline="ols", 
                              labels={'Dias': 'Data'},
                              color='cluster_category', color_discrete_map={},
                              title=f'Sem registros disponíveis para este período.')
        
        return px.scatter(df_aux, x='Dias', y=y_col, 
                          color='cluster_category', color_discrete_map=color_map,
                          size=y_col,  # Ajuste o tamanho dos pontos com base nas calorias
                          size_max=20,  # Define um tamanho máximo para melhor visualização
                          labels={'Dias': 'Data','cluster_category': 'Intensidade do Treino'},
                          title=f"Correlação entre Dias e {y_col}")

    