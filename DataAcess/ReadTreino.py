import json
import os


class TrainingSchedule:
    def __init__(self, ):
        project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
        file_path = os.path.join(project_root, '..', 'Data', 'set.json')
        # Carregar o JSON dos treinos
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        # Método para carregar o arquivo JSON
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get(self, date=None):
        # Método para retornar todos os treinos ou um treino específico por data
        if date:
            # Retorna o treino específico pela data
            return self.data["schedule"].get(date, None)
        else:
            # Retorna todos os treinos
            return self.data["schedule"]

    def display_schedule(self):
        # Iterar sobre cada treino no cronograma e exibir informações
        for date, treino in self.data["schedule"].items():
            print(f"\nData do treino: {date}")
            print(f"Tipo de treino: {treino['type']}")

            # Iterar sobre os exercícios
            self.display_exercises(treino["exercises"])

    def display_exercises(self, exercises):
        # Iterar sobre os exercícios
        for exercise in exercises:
            # Exibir categoria do exercício
            category = exercise.get("category", "Sem categoria")
            print(f"\nCategoria: {category}")

            # Exibir detalhes se existirem
            if "details" in exercise and exercise["details"]:
                print(f"Detalhes: {exercise['details']}")

            # Verificar e exibir exercícios específicos (caso existam)
            if "sets" in exercise:
                print("Exercícios:")
                self.display_sets(exercise["sets"])

    def display_sets(self, sets):
        # Exibir os detalhes dos sets do exercício
        for item in sets:
            print(f" - {item}")




# if __name__ == '__main__':
#     # Exemplo de uso

#     # Caminho para o arquivo JSON
    

#     # Criar uma instância da classe TrainingSchedule
#     training_schedule = TrainingSchedule()
#     last_3_dates = sorted(training_schedule.data['schedule'].keys(), reverse=True)[:3]
        
#     for date in last_3_dates:
#             treino = training_schedule.get(date)
#             print(treino)
#     # Exibir o cronograma de todos os treinos
#     #training_schedule.display_schedule()

#     # Exemplo de buscar treino específico por data
#     specific_date = "2024-09-29"
#     specific_training = training_schedule.get(specific_date)
#     if specific_training:
#         print(f"\nTreino encontrado para {specific_date}:")
#         print(f"Tipo de treino: {specific_training['type']}")
#     else:
#         print(f"\nNenhum treino encontrado para {specific_date}")
