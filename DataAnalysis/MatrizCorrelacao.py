import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Adicionando os dados de frequência cardíaca (média e máxima) ao DataFrame
heart_rate_avg = [entry["heart_rate"]["average"] for entry in json_data]
heart_rate_max = [entry["heart_rate"]["maximum"] for entry in json_data]

df['heart_rate_avg'] = heart_rate_avg
df['heart_rate_max'] = heart_rate_max

print(df.info())
df = df.drop(['start_time'], axis=1)

# Gerando a matriz de correlação
correlation_matrix = df.corr()


# Plotar a matriz de correlação como um heatmap

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlação com Valores')
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.show()