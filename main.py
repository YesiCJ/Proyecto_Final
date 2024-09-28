
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st


# Cargar datos desde GitHub
st.set_page_config(layout="centered")
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/YesiCJ/Proyecto_Final/refs/heads/main/Datos_proyecto_limpios.csv'
    df = pd.read_csv(url)
    return df

# Cargar el dataset
df = load_data()
# Título del tablero
st.title('Dashboard de Análisis de Ratios Financieros')
st.subheader("Dashboard elaborado por: Yesika Correa Jaime")



# 1. Dividir las columnas por un millón
columnas_a_dividir = ['Total_Revenue', 'Short_Term_Debt', 'Long_Term_Debt', 'Current_Assets','Current_Liabilities', 'Equity', 'Financial_Expenses']
df[columnas_a_dividir] = df[columnas_a_dividir] / 1000000

st.dataframe(df.head(5))

# 2. Recalcular las variables solicitadas
# Nota: Asegúrate de que los nombres de las columnas coincidan exactamente con los de tu DataFrame

# Recalcular Current_Ratio
df['Current_Ratio'] = df['Current_Assets'] / df['Current_Liabilities']

# Recalcular Debt_to_Equity_Ratio
df['Debt_to_Equity_Ratio'] = (df['Short_Term_Debt'] + df['Long_Term_Debt']) / df['Equity']

# Recalcular Interest_Coverage_Ratio
df['Interest_Coverage_Ratio'] = df['Total_Revenue'] / df['Financial_Expenses']


############################################################
# Crear los filtros interactivos
company_size_filter = st.multiselect('Seleccionar Tamaño de Empresa', options=df['Company_Size'].unique(), default=df['Company_Size'].unique())
industry_filter = st.multiselect('Seleccionar Industria', options=df['Industry'].unique(), default=df['Industry'].unique())
country_filter = st.multiselect('Seleccionar País', options=df['Country'].unique(), default=df['Country'].unique())


#################################################
# Filtros interactivos
#st.sidebar.header('Filtros')
#company_size = st.sidebar.multiselect('Selecciona el tamaño de la empresa', options=df['Company_Size'].unique(), default=df['Company_Size'].unique())
#industry = st.sidebar.multiselect('Selecciona la industria', options=df['Industry'].unique(), default=df['Industry'].unique())
#country = st.sidebar.multiselect('Selecciona el país', options=df['Country'].unique(), default=df['Country'].unique())

# Filtrar los datos en función de los filtros seleccionados
df_filtered = df[(df['Company_Size'].isin(company_size_filter)) & 
                 (df['Industry'].isin(industry_filter)) & 
                 (df['Country'].isin(country_filter))]

# KPIs Principales


# KPIs en la parte superior
st.header('KPIs Principales')
col1, col2, col3 = st.columns(3)

with col1:
    current_ratio_mean = df_filtered['Current_Ratio'].mean()
    st.metric(label='Promedio Current Ratio', value=round(current_ratio_mean, 2))

with col2:
    debt_to_equity_mean = df_filtered['Debt_to_Equity_Ratio'].mean()
    st.metric(label='Promedio Debt to Equity Ratio', value=round(debt_to_equity_mean, 2))

with col3:
    interest_coverage_mean = df_filtered['Interest_Coverage_Ratio'].mean()
    st.metric(label='Promedio Interest Coverage Ratio', value=round(interest_coverage_mean,2))



# Gráficas interactivas
st.header('Análisis de Ratios Financieros')


# Gráfica de Distribución
#st.subheader('Distribución de Current Ratio por País')
fig_box = px.box(df_filtered, 
                 x=['Country', 'Company_Size'],
                 y='Current_Ratio', 
                 color='Country',
                 title='Distribución de Current Ratio por País')

st.plotly_chart(fig_box)

# Gráfica de Distribución
#st.subheader('Distribución de Debt to Equity Ratio por País')
fig_box = px.box(df_filtered, 
                 x=['Country', 'Company_Size'],
                 y='Debt_to_Equity_Ratio', 
                 color='Country',
                 title='Distribución de Debt to Equity Ratio por País')

st.plotly_chart(fig_box)

#st.subheader('Distribución de Inetrest Coverage Ratio por País')
fig_box = px.box(df_filtered, 
                 x=['Country', 'Company_Size'],
                 y='Interest_Coverage_Ratio', 
                 color='Country',
                 title='Distribución de Interest Coverage Ratio por País')

st.plotly_chart(fig_box)





# Gráfica de barras para analizar el Interest Coverage Ratio por industria
#st.subheader('Interest Coverage Ratio por Industria')
fig_bar = px.bar(df_filtered, 
                 x=['Industry','Country'] ,
                 y='Total_Revenue', 
                 color='Industry', 
                 title='Total de Ingresos por Industria y país')

st.plotly_chart(fig_bar)

fig_bar = px.bar(df_filtered, 
                 x=['Industry','Country'] ,
                 y='Financial_Expenses', 
                 color='Industry', 
                 title='Total de Gastos Financieros por Industria y país')

st.plotly_chart(fig_bar)



# Crear gráfica de pie para la proporción de registros por Country
fig = px.pie(df_filtered, names='Country', title='Proporción de empresas por País', hole=0.3)
st.plotly_chart(fig)

# Crear gráfica de pie para la proporción de registros por Industry
fig = px.pie(df_filtered, names='Industry', title='Proporción de empresas por Industria', hole=0.3)
st.plotly_chart(fig)
# Crear gráfica de pie para la proporción de registros por Company Size
fig = px.pie(df_filtered, names='Company_Size', title='Proporción de empresas por Tamaño', hole=0.3)
# Mostrar gráfica (en Streamlit o en otro entorno)
st.plotly_chart(fig)



