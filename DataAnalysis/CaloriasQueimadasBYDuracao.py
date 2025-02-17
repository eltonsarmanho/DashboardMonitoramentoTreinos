import plotly.express as px
import pandas as pd
import re
from DataLoader import DataLoader
import sys
import os
import json
# Função para definir níveis de intensidade com base nas calorias queimadas
def define_level(calories):
    if calories < 400:
        return 'Baixa Intensidade'
    elif 400 <= calories <= 500:
        return 'Intensidade Moderada'
    else:
        return 'Alta Intensidade'

# Caminho para o arquivo JSON fornecido
project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path = os.path.join(project_root,'..' ,'Data', 'bioData.json')


data_loader = DataLoader(file_path)

# Exemplo de como carregar os dados (usando sua classe DataLoader)
data_loader = DataLoader(file_path)
json_data = data_loader.load_json_data()
df = data_loader.extract_data()

# Remover o dia da semana do campo 'start_time' e converter para datetime
df['start_time'] = df['start_time'].apply(lambda x: re.match(r'\d{2}/\d{2}', x).group(0) + '/2024')
df['start_time'] = pd.to_datetime(df['start_time'], format='%d/%m/%Y')

# Adicionar a coluna de nível de intensidade
df['level'] = df['calories'].apply(define_level)

# Ajustar o tamanho dos pontos e formatar as datas no hover
df['Data'] = df['start_time'].dt.strftime('%d/%m/%Y')

color_map = {
    'Alta Intensidade': 'red',
    'Baixa Intensidade': 'green',
    'Intensidade Moderada': 'blue',

}
# Criar gráfico de dispersão interativo usando Plotly
fig = px.scatter(df, x='duration', y='calories', color='level',color_discrete_map=color_map,
                 hover_data={'Data': True}, labels={
                     'duration': 'Duração do Treino (segundos)',
                     'calories': 'Calorias Queimadas',
                     'level': 'Nível de Intensidade'
                 },
                 title='Relação entre Duração do Treino e Calorias Queimadas por Nível de Intensidade',
                 category_orders={"level": ["Alta Intensidade", "Intensidade Moderada", "Baixa Intensidade"]}# Ordem personalizada das legendas
                 )


# Aumentar o tamanho dos pontos
fig.update_traces(marker=dict(size=14))

# Calcular a média de calorias por nível de intensidade
mean_calories = df.groupby('level')['calories'].mean().reset_index()

# Adicionar linhas horizontais para a média de calorias por nível
for level, mean_cal in zip(mean_calories['level'], mean_calories['calories']):
    fig.add_hline(y=mean_cal, line_dash="dash", line_color='black', annotation_text=f"Média das Calorias por Nível {level}: {mean_cal:.2f} cal")

project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path = os.path.join(project_root,'..' ,'html', 'Plot_Calorias_Duracao.html')
fig.write_html(file_path)
# Exibir o gráfico interativo
fig.show()