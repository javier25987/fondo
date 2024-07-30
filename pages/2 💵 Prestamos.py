import streamlit as st
import pandas as pd
import Funciones

st.set_page_config(layout="wide")

st.session_state['preguntar clave'] = True

df = pd.read_csv(st.session_state.nombre_df)

index = st.session_state.usuario_actual_prestamos

index_de_usuario = st.sidebar.number_input('Numero de usuario.', value=0, step=1)

if st.sidebar.button('Buscar'):
    if 0 <= index_de_usuario < st.session_state.usuarios:
        st.session_state.usuario_actual_prestamos = index_de_usuario
        st.rerun()
    else:
        st.error('El numero de usuario esta fuera de rango.', icon="🚨")

if index == -1:
    st.title('Usuario Indeterminado')
else:
    st.title(f'№ {index} - {df['nombre'][index].title()}')

    prestamos_hechos = df['prestamos hechos'][index]
    capital = df['capital'][index]

    deudas_en_prestamos = str(df['deudas en prestamos'][index])
    tabla_por_prestamos = {}
    if deudas_en_prestamos != '-':
        deudas_en_prestamos = list(map(int, deudas_en_prestamos.split('-')))
        k = 1
        for i in deudas_en_prestamos:
            tabla_por_prestamos[str(k)] = i
            k += 1
        tabla_por_prestamos['Total'] = sum(deudas_en_prestamos)
    else:
        tabla_por_prestamos['Total'] = 0

    deudas_por_fiador = str(df['deudas por fiador'][index])
    tabla_por_fiador = {}
    if deudas_por_fiador != '-':
        deudas_por_fiador = list(map(int, deudas_por_fiador.split('-')))
        k = 1
        for i in deudas_por_fiador:
            tabla_por_fiador[str(k)] = i
            k += 1
        tabla_por_fiador['Total'] = sum(deudas_por_fiador)
    else:
        tabla_por_fiador['Total'] = 0

    interese_vencidos = str(df['intereses vencidos'][index])
    tabla_interese = {}
    if interese_vencidos != '-':
        interese_vencidos = list(map(float, interese_vencidos.split('-')))
        k = 1
        for i in interese_vencidos:
            tabla_interese[str(k)] = i
            k += 1
        tabla_interese['Total'] = sum(interese_vencidos)
    else:
        tabla_interese['Total'] = 0

    capital_disponible = int(capital*0.75 - tabla_por_prestamos['Total'] - tabla_por_fiador['Total'] -
                             tabla_interese['Total'])

    interes_por_prestamo = str(df['intereses en prestamos'][index]).split('-')
    fiadores = str(df['fiadores'][index]).split('-')
    deudas_con_fiadores = str(df['deudas con fiadores'][index]).split('-')
    fechas_de_pago = str(df['fechas de pagos'][index]).split('-')

    tab_1, tab_2, tab_3 = st.tabs(['Ver prestamos', 'Solicitar un prestamo', 'Consultar capital'])

    with tab_1:
        if prestamos_hechos == 0:
            st.header('No hay prestamos hechos')
        else:
            k = 0
            for tab_i in st.tabs([f'prestamo №{i}' for i in range(prestamos_hechos)]):
                with tab_i:
                    st.table({'deuda de el prestamo': deudas_en_prestamos[k],
                              'interes por prestamo': interes_por_prestamo[k],
                              'intereses vencidos': interese_vencidos[k],
                              'numero(s) de fiador(es)': fiadores[k],
                              'deuda(s) con fiador(es)': deudas_con_fiadores[k],
                              'fechas de pago': fechas_de_pago[k]})
                k += 1

    with tab_2:
        st.header('Formulario para la solicitud de un prestamo')
        valor_de_el_prestamo = st.number_input('Dinero a retirar.', value=0, step=1)

        st.divider()
        ide_fiadores = st.text_input('Fiadores de el prestamo')
        ide_deudas_con_fiadores = st.text_input('Deudas con fiadores')

        st.divider()
        if st.button('Tramitar prestamo'):
            if valor_de_el_prestamo < 0:
                if valor_de_el_prestamo < 0:
                    st.error('Creo que no se puede dar esa cantidad de dinero.', icon="🚨")
            else:
                control_dinero = False
                if Funciones.viavilidad_dinero(index=index, valor_de_el_prestamo=valor_de_el_prestamo,
                                               fiadores=ide_fiadores, deudas_con_fiadores=ide_deudas_con_fiadores):
                    control_dinero = True
                    st.success('El prestamo es economicamente viable.', icon="✅")
                else:
                    st.error(
                        '''
                        El prestamo no puede hacerse por temas economicos, revise que el capital disponible es 
                        suficiente para realizar el prestamo o que el formato de los fiadores y sus deudas esta
                        bien tramitado ya que esto tambien genera errores''',
                        icon="🚨"
                    )

                if control_dinero:
                    st.balloons()
                    Funciones.formato_de_prestamo(index=index, valor_de_el_prestamo=valor_de_el_prestamo,
                                                  fiadores=ide_fiadores, deudas_con_fiadores=ide_deudas_con_fiadores)

    with tab_3:
        st.subheader('Capital.')
        st.write(f'capital guardado: {"{:,}".format(capital)}')
        st.write(f'Capital disponible para retirar: {"{:,}".format(int(capital*0.75))}')

        st.subheader('Descuentos.')

        st.write('Descuentos por prestamos.')
        st.table(tabla_por_prestamos)

        st.write('Descuentos por fiador.')
        st.table(tabla_por_fiador)

        st.write('Descuentos por intereses vencidos.')
        st.table(tabla_interese)

        st.header(f'Capital disponible para retirar: {"{:,}".format(capital_disponible)}')

