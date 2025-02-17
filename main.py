import streamlit as st
from Interface import HealthDashboard
from streamlit.web import cli as stcli
from streamlit import runtime
import sys
import locale


def main():

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'C')  # Usa um locale genérico
        # Configuração inicial do estado
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'main'
    
    # Página principal
    if st.session_state.current_page == 'main':
        render_main_page()
    
    # Página do dashboard
    elif st.session_state.current_page == 'HealthDashboard':
        HealthDashboard.show()

def render_main_page():
    st.title("Dashboard de Monitoramento de Treinos")
    
    st.markdown(
        """
        O **Dashboard de Monitoramento de Treinos** é um projeto que visa a criação de um dashboard interativo para visualizar e analisar 
        dados coletados do sensor **Polar Verity Sense**. A plataforma permite acompanhar métricas importantes dos treinos, incluindo:
        
        - **Calorias Queimadas**
        - **Frequência Cardíaca Média (HRV)**
        - **Frequência Cardíaca Máxima**
        - **Duração do Treino**
        - **Nome dos Exercícios, Séries e Repetições**
        
        Além disso, o projeto permite a análise detalhada dos treinos e a segmentação dos dados em diferentes padrões 
        para melhor interpretação e acompanhamento do desempenho do usuário.
        """
    )
    
    # Botão único centralizado
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Ir para o Dashboard", use_container_width=True):
            st.session_state.current_page = 'HealthDashboard'
            st.rerun()  # Força atualização imediata


if __name__ == '__main__':
    if runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
