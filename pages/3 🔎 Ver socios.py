import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

tab_1, tab_2 = st.tabs(['Buscar socios', 'Estado de cuenta'])

with tab_1:
    c_1, c_2 = st.columns(2, vertical_alignment="bottom")

    with c_1:
        nombre_a_buscar = st.text_input('Nombre')

    with c_2:
        if st.button('Buscar'):
            st.session_state.nombre_para_busqueda = nombre_a_buscar
            st.rerun()

    st.divider()

    if st.session_state.nombre_para_busqueda == '':
        st.table(df[['nombre','puestos', 'numero_telefonico', 'estado', 'capital']])
    else:
        nuevo_data_frame = df[df['nombre'].str.contains(nombre_a_buscar, case=False, na=False)]
        st.table(nuevo_data_frame[['nombre', 'puestos', 'numero_telefonico', 'estado', 'capital']])

with tab_2:

    index = st.session_state.usuario_actual_ver

    index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

    if st.sidebar.button('Buscar', key='00011'):
        if 0 <= index_de_usuario < st.session_state.usuarios:
            st.session_state.usuario_actual_ver = index_de_usuario
            st.rerun()
        else:
            st.error('El numero de usuario esta fuera de rango.', icon="🚨")
