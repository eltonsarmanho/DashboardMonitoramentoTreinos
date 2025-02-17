import sys
import os
#Add Raiz ao sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from DataAcess.ReadTreino import TrainingSchedule
import pandas as pd
from DataAcess.UserProfile import UserProfile
from DataAcess.HealthData import HealthData
import streamlit as st
from streamlit_extras.chart_container import chart_container

def get_informacoes_usuario():
  # Instanciar a classe adaptadora
  project_root = os.path.dirname(os.path.abspath(__file__))  # Diretório do script atual
  file_path = os.path.join(project_root, '..', 'Data', 'profile.json')

  # Criando uma instância da classe UserProfile com o JSON
  user_profile = UserProfile(file_path)

  primeiro_nome = user_profile.get_full_name()
  peso = user_profile.get_weight()
  altura = user_profile.get_height()
  idade = user_profile.get_age()
  return  primeiro_nome,peso,altura, idade

def initializeData():
    # Inicializar o gerador LLM uma única vez
    if 'Healthdata' not in st.session_state:
        st.session_state.Healthdata = HealthData()

def my_metric(label, value, bg_color, icon="fas fa-asterisk"):
        fontsize = 30
        valign = "left"
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.7.2/css/all.css" crossorigin="anonymous">'

        bg_color_css = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.75)'

        htmlstr = f"""<p style='background-color: {bg_color_css}; 
                                font-size: {fontsize}px; 
                                border-radius: 7px; 
                                padding-left: 12px; 
                                padding-top: 18px; 
                                padding-bottom: 18px; 
                                line-height:25px;'>
                                <i class='{icon} fa-xs'></i> {value}
                                </style><BR><span style='font-size: 14px; 
                                margin-top: 0;'>{label}</style></span></p>"""

        st.markdown(lnk + htmlstr, unsafe_allow_html=True)

def card():
    violeta = (102, 102, 255)
    laranja = (255, 102, 102)
    vermelho = (255, 77, 109)
    icon_heart = "fas fa-duotone fa-solid fa-heart-pulse"
    icon_calorias = "fas fa-fire"
    icon_heart_max = "fas fa-heart-circle-bolt"

    col1, col2,col3 = st.columns(3)
    dict = st.session_state.Healthdata.get_last_n_days_avg(3)
    with col1:
        my_metric("Calorias", dict['calories'], vermelho, icon_calorias)
    with col2:
        my_metric("Frequência Cardíaca Média", dict['heart_rate_avg'], violeta, icon_heart)
    with col3:
        my_metric("Frequência Cardíaca Máxima", dict['heart_rate_max'], laranja, icon_heart_max)

def my_profile_card(name, weight, height, age, bg_color= (255, 102, 102), icon="fas fa-user"):
        fontsize = 18
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.7.2/css/all.css" crossorigin="anonymous">'

        bg_color_css = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.9)'

        htmlstr = f"""
        <div style='background-color: {bg_color_css}; 
                    color: white; 
                    font-size: {fontsize}px; 
                    border-radius: 20px; 
                    padding: 30px; 
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    width: 300px;'>
            <div style='display: flex; justify-content: space-between;'>
                <i class='{icon}' style="font-size: 40px;"></i>
                <div style='text-align: right;'>
                    <h3>{name}</h3>
                    <p></p>
                </div>
            </div>
            <hr>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <strong>{weight}kg</strong>
                    <p>Peso</p>
                </div>
                <div>
                    <strong>{height}cm</strong>
                    <p>Altura</p>
                </div>
                <div>
                    <strong>{age} Anos</strong>
                    <p>Idade</p>
                </div>
            </div>
        </div>
        """
        st.sidebar.markdown(lnk + htmlstr, unsafe_allow_html=True)


def main():

    st.set_page_config(layout='wide')
    st.title("Health Dashboard")
    initializeData()

    # Carregar configurações e informações do usuário
    meses_pt, anos_unicos = st.session_state.Healthdata.getDadosTempo()

    # Exibe o card de perfil sidebar
    name, weight, height, age = get_informacoes_usuario()
    # Cor de fundo do card
    my_profile_card(name, weight, height, age)

    col1, col2 = st.columns(2)
    
    
    with col1:
        st.subheader("Resumo dos Últimos 3 Treinos")
        card()

    st.divider()
    

    
    col1, col2 = st.columns([0.5,0.5])
    with col1:
        with st.container(border=True):
                st.subheader("Performance dos Treinos")
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    # Selecione o mês
                    selected_month = st.selectbox("Selecione o mês", list(meses_pt.keys()))
                with col1_2:
                    selected_year = st.selectbox("Selecione o ano", anos_unicos)
                # Chama a função para criar o gráfico, se necessário        
                fig = st.session_state.Healthdata.create_clustered_bar_chart(selected_month=meses_pt[selected_month],
                                                                            selected_year=selected_year)
                st.plotly_chart(fig)

                st.subheader("Indicadores de Treino")
                df_aux = st.session_state.Healthdata._get_metrics()
                
                y_col = st.selectbox("Selecione o atributo", df_aux.columns, key='y_col')
                fig_corr = st.session_state.Healthdata.get_chart_line(selected_month=meses_pt[selected_month],
                                                                            selected_year=selected_year,
                                                                            y_col=y_col)
                st.plotly_chart(fig_corr)
    with col2:
            with st.container(border=True):
                  st.markdown("### <i class='fa-solid fa-dumbbell'></i> Diário de Treinos", unsafe_allow_html=True)

                  training_schedule = TrainingSchedule()
                  last_3_dates = sorted(training_schedule.data['schedule'].keys(), reverse=True)[:5]
            
                  for date in last_3_dates:
                    treino = training_schedule.get(date)
                    with st.expander(f"Treino de {date}"):
                        st.write(f"#### Tipo de Treino: {treino['type']}", unsafe_allow_html=True)

                        
                        # Criar um dataframe para exibir os exercícios em tabela
                        exercises_data = []
                        for exercise in treino['exercises']:
                            category = exercise.get("category", "Sem categoria")
                            details = exercise.get("details", "")
                            sets = ", ".join(map(str, exercise.get("sets", []))) if "sets" in exercise else ""
                            exercises_data.append([category, details, sets])
                        
                        df_exercises = pd.DataFrame(exercises_data, columns=["Categoria", "Detalhes", "Séries/Repetições"])
                        st.dataframe(df_exercises, use_container_width=True)

#from streamlit.web import cli as stcli
# from streamlit import runtime
# if __name__ == '__main__':
#     if runtime.exists():
#         main()
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())