import json
import pandas as pd
import matplotlib.pyplot as plt

from DataLoader import DataLoader

import sys
import os
import json
# Caminho para o arquivo JSON fornecido
project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
file_path = os.path.join(project_root,'..' ,'Data', 'bioData.json')

data_loader = DataLoader(file_path)
json_data = data_loader.load_json_data()
df = data_loader.extract_data()

# Gráfico de duração dos treinos por sessão com datas no eixo X
plt.figure(figsize=(10, 10))
plt.bar(df['start_time'], df['duration'], color='green')
plt.title('Duração dos Treinos por Data e Dia da Semana')
plt.xlabel('Data (dd/MM - Dia da Semana)')
plt.ylabel('Duração (segundos)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()