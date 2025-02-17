import streamlit as st
import random
import sys
import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
import os
import sys

def main():

    def my_profile_card(name, location, weight, height, age, bg_color, icon="fas fa-user"):
        fontsize = 18
        lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v6.7.2/css/all.css" crossorigin="anonymous">'

        bg_color_css = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.9)'

        htmlstr = f"""
        <div style='background-color: {bg_color_css}; 
                    color: white; 
                    font-size: {fontsize}px; 
                    border-radius: 10px; 
                    padding: 20px; 
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); 
                    width: 300px;'>
            <div style='display: flex; justify-content: space-between;'>
                <i class='{icon}' style="font-size: 40px;"></i>
                <div style='text-align: right;'>
                    <h3>{name}</h3>
                    <p>{location}</p>
                </div>
            </div>
            <hr>
            <div style='display: flex; justify-content: space-between;'>
                <div>
                    <strong>{weight}kg</strong>
                    <p>Weight</p>
                </div>
                <div>
                    <strong>{height}m</strong>
                    <p>Height</p>
                </div>
                <div>
                    <strong>{age} yrs</strong>
                    <p>Age</p>
                </div>
            </div>
        </div>
        """
        st.sidebar.markdown(lnk + htmlstr, unsafe_allow_html=True)


    def display_dashboard():
        # Exemplo de dados
        name = "Thomas Fletcher"
        location = "Sydney, Australia"
        weight = 75
        height = 6.5
        age = 25
        bg_color = (255, 102, 102)  # Cor de fundo do card

        # Exibe o card de perfil
        my_profile_card(name, location, weight, height, age, bg_color)

    # Exibir o dashboard
    display_dashboard()


# if __name__ == '__main__':
#     if runtime.exists():
#         main()
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())
