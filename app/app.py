import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Time Tracker BI", layout="wide")
st.title("🕒 Time Tracker BI Dashboard")

# 1. Cargar o simular datos
if Path('../data/tracking_simulado.csv').exists():
    df = pd.read_csv('../data/tracking_simulado.csv', parse_dates=['fecha'])
else:
    st.warning("No se encontró el archivo de datos simulado. Sube un CSV o ejecuta el script de simulación.")
    st.stop()

uploaded_file = st.file_uploader("Sube tu archivo de tracking (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['fecha'])

# 2. Filtros rápidos
st.sidebar.header("Filtros")
actividad_sel = st.sidebar.multiselect("Actividad", options=df['actividad'].unique(), default=list(df['actividad'].unique()))
fecha_ini = st.sidebar.date_input("Desde", value=df['fecha'].min())
fecha_fin = st.sidebar.date_input("Hasta", value=df['fecha'].max())

df_filt = df[
    (df['actividad'].isin(actividad_sel)) &
    (df['fecha'] >= pd.to_datetime(fecha_ini)) &
    (df['fecha'] <= pd.to_datetime(fecha_fin))
]

# 3. KPIs principales
col1, col2, col3 = st.columns(3)
col1.metric("Total horas", int(df_filt['horas'].sum()))
col2.metric("Días registrados", df_filt['fecha'].nunique())
col3.metric("Horas promedio/día", round(df_filt.groupby('fecha')['horas'].sum().mean(), 1))

# 4. Gráficos
st.subheader("Distribución de horas por actividad")
st.bar_chart(df_filt.groupby('actividad')['horas'].sum())

st.subheader("Tendencia mensual")
df_filt['mes'] = df_filt['fecha'].dt.to_period('M')
st.line_chart(df_filt.groupby('mes')['horas'].sum())

# 5. Días más productivos
st.subheader("Top 5 días con más horas registradas")
dias_top = df_filt.groupby('fecha')['horas'].sum().nlargest(5)
st.table(dias_top)

# 6. Recomendaciones automáticas (ejemplo simple)
st.subheader("💡 Recomendaciones personalizadas")
msg = ""
avg_trabajo = df_filt[df_filt['actividad'] == "Trabajo"]['horas'].mean()
avg_ocio = df_filt[df_filt['actividad'] == "Ocio"]['horas'].mean()
if avg_trabajo < 4:
    msg += "- Dedicas menos de 4h/día a Trabajo en promedio. ¿Es suficiente para tus objetivos?\n"
if avg_ocio > 2:
    msg += "- ¡Cuidado! Tu promedio de horas de Ocio es alto. ¿Te ayuda a recargar energía?\n"
if msg == "":
    msg = "¡Buen equilibrio entre actividades!"
st.write(msg)

# 7. Descargar reporte filtrado
st.download_button(
    label="Descargar CSV filtrado",
    data=df_filt.to_csv(index=False).encode('utf-8'),
    file_name='tracking_filtrado.csv',
    mime='text/csv'
)
