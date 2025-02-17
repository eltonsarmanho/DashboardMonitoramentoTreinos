import json
import sys
import os
import json
from datetime import datetime

class UserProfile:
    def __init__(self, file):
        with open(file, 'r') as file:
            json_data = json.load(file)
        self.data = json_data

    def get_user_info(self, index=0):
        # Acessa o usuário pelo índice (default é o primeiro usuário)
        user = self.data[index]
        return user

    def get_first_name(self, index=0):
        user = self.get_user_info(index)
        return user.get('first-name')

    def get_last_name(self, index=0):
        user = self.get_user_info(index)
        return user.get('last-name')

    def get_full_name(self, index=0):
        user = self.get_user_info(index)
        return f"{user.get('first-name')} {user.get('last-name')}"

    def get_birthdate(self, index=0):
        user = self.get_user_info(index)
        return user.get('birthdate')

    def get_gender(self, index=0):
        user = self.get_user_info(index)
        return user.get('gender')

    def get_height(self, index=0):
        user = self.get_user_info(index)
        return user.get('height')
    def get_age(self, index=0):


        data_nascimento_str = self.get_birthdate()

        # Converter a string para um objeto datetime
        data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d")

        # Data atual
        data_atual = datetime.now()

        # Calcular a idade
        idade = data_atual.year - data_nascimento.year

        # Ajustar caso o aniversário ainda não tenha ocorrido este ano
        if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
            idade -= 1
        return idade

    def get_weight(self, index=0):
        user = self.get_user_info(index)
        return user.get('weight')

    def get_member_id(self, index=0):
        user = self.get_user_info(index)
        return user.get('member-id')

    def get_polar_user_id(self, index=0):
        user = self.get_user_info(index)
        return user.get('polar-user-id')

    def get_registration_date(self, index=0):
        user = self.get_user_info(index)
        return user.get('registration-date')

    def get_extra_info(self, index=0):
        user = self.get_user_info(index)
        return user.get('extra-info', [])

if __name__ == '__main__':
    # Exemplo de uso
    # Caminho para o arquivo JSON fornecido
    project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
    file_path = os.path.join(project_root, '..', 'Data', 'profile.json')

    # Criando uma instância da classe UserProfile com o JSON
    user_profile = UserProfile(file_path)

    # Acessando dados usando os métodos da classe
    print("Full Name:", user_profile.get_full_name())
    print("Birthdate:", user_profile.get_birthdate())
    print("Age:", user_profile.get_age())
    print("Gender:", user_profile.get_gender())
    print("Height:", user_profile.get_height())
    print("Weight:", user_profile.get_weight())
    print("Member ID:", user_profile.get_member_id())
    print("Polar User ID:", user_profile.get_polar_user_id())
    print("Registration Date:", user_profile.get_registration_date())
    print("Extra Info:", user_profile.get_extra_info())
