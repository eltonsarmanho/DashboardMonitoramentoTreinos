import streamlit as st
import random
import sys

import streamlit as st
from streamlit.web import cli as stcli
from streamlit import runtime
import os
import sys
def main():

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


    def display_dashboard():
        roxo = (160, 105, 255)
        red = (255, 102, 102)
        icon_heart = "fas fa-duotone fa-solid fa-heart-pulse"
        icon_calorias = "fas fa-fire"


        my_metric("Calorias", 123, red,icon_calorias)
        my_metric("Frequência Cardíaca", 13, roxo, icon_heart)

        st.markdown("# In columns")

        col1, col2 = st.columns(2)
        with col1:
            my_metric("Calorias", 123, red, icon_calorias)
        with col2:
            my_metric("Frequência Cardíaca", 13, roxo, icon_heart)

    # Exibir o dashboard
    display_dashboard()


# if __name__ == '__main__':
#     if runtime.exists():
#         main()
#     else:
#         sys.argv = ["streamlit", "run", sys.argv[0]]
#         sys.exit(stcli.main())