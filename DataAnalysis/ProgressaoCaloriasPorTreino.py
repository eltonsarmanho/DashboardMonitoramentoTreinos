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


# Primeiro, criaremos um gráfico de linha para mostrar a progressão de calorias queimadas ao longo das sessões
# Gráfico de calorias queimadas ao longo das sessões com datas no eixo X
plt.figure(figsize=(10, 6))
plt.plot(df['start_time'], df['calories'], marker='o', linestyle='-', color='orange')
plt.title('Progressão de Calorias Queimadas ao Longo das Sessões')
plt.xlabel('Data (dd/MM)')
plt.ylabel('Calorias Queimadas')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()