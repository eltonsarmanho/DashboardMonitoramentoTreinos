
import os
import json
import pandas as pd
import datetime
import locale

class TrainingDataPolar:
    def __init__(self, file):
        """
        Inicializa a classe com os dados JSON fornecidos (espera uma lista de treinos)

        Args:
            file (str): Caminho para o arquivo JSON com os dados de treino.

        Attributes:
            data (list): Lista de dicionários com os dados de treino preprocessados.
        """
        with open(file, 'r') as file:
            json_data = json.load(file)
        self.data = json_data
        self.data = self.preprocess_data()
    
    def preprocess_data(self):  
        
        """
        Preprocessa os dados de treino JSON carregados.

        1. Renomeia as colunas 'heart_rate.average' e 'heart_rate.maximum' para 'heart_rate_avg' e 'heart_rate_max', respectivamente.
        2. Converte a coluna 'duration' do formato ISO 8601 (PT3370S) para número de segundos.
        3. Converte a coluna 'start_time' do formato 'YYYY-MM-DDTHH:MM:SSZ' para 'dd/mm (weekday)'.

        Retorna um DataFrame com os dados preprocessados.
        """
        df = pd.json_normalize(self.data)  # Normaliza a lista de dicionários para um DataFrame
        # Renomear a coluna 'heart_rate.average' para 'heart_rate_avg'
        if 'heart_rate.average' in df.columns:
            df.rename(columns={'heart_rate.average': 'heart_rate_avg'}, inplace=True)
        if 'heart_rate.maximum' in df.columns:
            df.rename(columns={'heart_rate.maximum': 'heart_rate_max'}, inplace=True)
        # 1. Converter 'duration' de formato ISO 8601 (PT3370S) para número de segundos
        df['duration'] = df['duration'].apply(lambda x: int(x[2:-1]) if isinstance(x, str) else 0)

        # 2. Converter 'start_time' para o formato 'dd/mm (weekday)'
        df['start_time'] = df['start_time'].apply(
                lambda x: datetime.datetime.strptime(x[:10], '%Y-%m-%d').strftime('%d/%m (%A)') if isinstance(x,
                                                                                                              str) else '')
        return df
    def get(self, exercise_id=None):
        """
        Método para obter dados de treinos específicos ou todos os treinos.
        Se um ID de treino for fornecido, retorna o treino correspondente, caso contrário, retorna todos os treinos.
        """
        if exercise_id:
            # Retorna o treino específico com o ID fornecido
            for index, exercise in self.data.iterrows():
                if exercise['id'] == exercise_id:
                    return exercise
            return None  # Se não encontrar o treino
        else:
            # Retorna todos os treinos
            return self.data
    def getData(self):
        """
        Método para retornar os dados como um DataFrame do pandas.
        Transforma a lista de treinos em um DataFrame para fácil manipulação.
        """
        return self.data

    def display_trainings(self):
        # Método para exibir todos os treinos
        for training in self.data:
            self.display_training_details(training)

    def display_training_details(self, training):
        # Método para exibir os detalhes de um treino específico
        print(f"\nID: {training['id']}")
        print(f"Sport: {training['sport']}")
        print(f"Calories: {training['calories']}")
        print(f"Duration: {training['duration']}")
        print(f"Heart Rate: Avg - {training['heart_rate_avg']} bpm, Max - {training['heart_rate_max']} bpm")
        print(f"Start Time: {training['start_time']}")
        print(f"Device: {training['device']}")

# Exemplo de uso



# if __name__ == '__main__':
#     # Carregar os dados JSON
#     project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
#     file_path = os.path.join(project_root, '..', 'Data', 'bioData.json')

#     # Criar uma instância da classe TrainingData
#     training_data = TrainingDataPolar(file_path)

#     # Exibir todos os treinos
#     print(training_data.getData()['id'])

#     # Obter um treino específico por ID
#     exercise_id = "y8aKxj2J"
#     specific_training = training_data.get(exercise_id)
#     if specific_training.any():
#         print("\nTreino encontrado:")
#         training_data.display_training_details(specific_training)
#     else:
#         print(f"\nNenhum treino encontrado com o ID {exercise_id}")
