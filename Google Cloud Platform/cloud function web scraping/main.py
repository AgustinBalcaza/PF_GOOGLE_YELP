from bs4 import BeautifulSoup as bs
import requests as rq
import pandas as pd

url = 'https://www.datosmundial.com/america/usa/turismo.php'
page = rq.get(url).text
soup = bs(page)

table = soup.find('table')
df = pd.DataFrame(columns = ['year', 'visitantes', 'ingresos'])

df = pd.DataFrame(columns = ['year', 'visitantes', 'ingresos'])
for row in table.find_all('tr')[1::]:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]
    anio = cols[0]
    visitante = cols[1]
    ing = cols[2]
    df = df.append({'year':anio, 'visitantes':visitante, 'ingresos':ing}, ignore_index=True)

# Limpiar la columna 'visitante'
df['visitantes'] = df['visitantes'].str.replace(' ', '').str.replace('M', '').str.replace(',', '.')

# Convertir la columna a tipo numérico y multiplicar por 1,000,000
df['visitantes'] = pd.to_numeric(df['visitantes']) * 1000000

# Limpiar la columna 'ingresos'
df['ingresos'] = df['ingresos'].str.replace(' ', '').str.replace('MM€', '').str.replace(',', '.')

# Convertir la columna a tipo numérico y multiplicar por mil millones
df['ingresos'] = pd.to_numeric(df['ingresos']) * 1e9



df['id_estado'] = df.apply(lambda row: [1, 2, 3, 4, 5], axis=1)
df_presupuesto = df.explode('id_estado')

data = {'id_estado': [1, 2, 3, 4, 5],
        'ponderado': [0.298, 0.298, 0.186, 0.072, 0.054]}

df_ponderado = pd.DataFrame(data)

df_presupuesto_estado = pd.merge(df_presupuesto, df_ponderado, on='id_estado')

df_presupuesto_estado['visitantes_estado'] = df_presupuesto_estado['visitantes'] * df_presupuesto_estado['ponderado']
df_presupuesto_estado['ingresos_estado'] = df_presupuesto_estado['ingresos'] * df_presupuesto_estado['ponderado']

df_final = df_presupuesto_estado.drop(['visitantes', 'ingresos', 'ponderado'], axis=1)
df_final