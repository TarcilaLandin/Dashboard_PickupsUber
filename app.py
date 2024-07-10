import streamlit as st
import pandas as pd
import numpy as np

# Configura o layout para usar a largura total da página
st.set_page_config(layout="wide")

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    try:
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

data_load_state = st.text('Loading data...')
data = load_data(10000)
#data_load_state.text("Done! (using st.cache_data)")

if not data.empty:  # Verifica se os dados foram carregados corretamente
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    # Criando as colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Number of pickups by hour')
        hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

 # Filtro de hora acima do mapa
    #st.subheader('Filter by hour')
   

    with col2:
        hour_to_filter = st.slider('hour', 0, 23, 17)
        filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
        st.subheader(f'Map of all pickups at {hour_to_filter}:00')
        st.map(filtered_data)
else:
    st.warning("No data available. Please check the data source.")
