import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import json
pd.set_option('display.max_rows', 150)

st.write("Buscador de ranking:")


keyword = st.text_input("KEYWORD", '')
site = st.text_input("site", "MLA")
api_search = f'https://api.mercadolibre.com/{site}/MLA/search?q={keyword}' 

for keyword in keyword:
    data = []
    for offset in range(0, 150, 50): 
        url = api_search + '&offset=' + str(offset)
        r = requests.get(url)
        a = json.loads(r.text)
        data += a['results']
df = pd.DataFrame(data)  
df['seller'] = df['seller'].astype(str)  
df['seller'] = df.seller.str.split("{'id': ").str[1]
df['seller'] = df.seller.str.split(",").str[0]
df = df[['id', 'site_id', 'title', 'seller', 'price', 'original_price']]

st.write(df)

seller = st.text_input("SELLER ID", 'Ingrese el seller id')

def check(val):
    a = df.index[df['seller'].str.contains(val)]
    if a.empty:
        return 'not found'
    elif len(a) > 1:
        return a.tolist()
    else:
        return a.item()

ranking = check(seller)

"""Ranking"""
st.write(ranking)        
