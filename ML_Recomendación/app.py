import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template, url_for
import pickle
import sklearn
import streamlit as st

PATH = 'cos_sim.npy'

def recomendacion_hotel(nombre_hotel: str):
    recomendacionhotel = pd.read_parquet('ml_model.parquet')
    nombre_hotel = nombre_hotel.lower()
    if nombre_hotel not in recomendacionhotel['business_name'].str.lower().values:
        error_message = {"Error": "Nombre de negocio incorrecto"}
        return error_message
    path = PATH
    cosine_sim = np.load(path)
    idx = recomendacionhotel[recomendacionhotel['business_name'].str.lower() == nombre_hotel].index[0]
    rec_hoteles = recomendacionhotel.iloc[cosine_sim[idx]]
    rec_hoteles = rec_hoteles.sort_values(by='avg_rating', ascending=False)
    info = {'recomendaciones': None}
    info['recomendaciones'] = list(rec_hoteles['business_name'])
    return info

def main():
    
    modelo=''

    # Se carga el modelo
    if modelo=='':
        with open(PATH, 'rb') as file:
            modelo = np.load(file)
    
    # Título
    html_temp = """
    <h1 style="color:#181082;text-align:center;">SISTEMA DE RECOMENDACIÓN PARA HOTELES </h1>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    # Lecctura de datos
    hotel = st.text_input("Nombre Hotel:")
    
    # El botón recomendación se usa para iniciar el procesamiento
    if st.button("Recomendación :"): 
        recomend = recomendacion_hotel(hotel)
        if 'recomendaciones' in recomend:
            st.success('LOS MEJORES HOTELES RECOMENDADOS SON: {}'.format(recomend['recomendaciones'][:5]).upper())
        else:
            st.error('Nombre de Hotel Inválido')

if __name__ == '__main__':
    main()