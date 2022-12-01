# Nepieciešamo moduļu pievienošana
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import base64

# Pārlūkprogrammas cilnes virsraksts un attēls
st.set_page_config(page_title="Projektēšanas laboratorija", page_icon=":basketball:", layout="wide")

# Sānjoslas virsraksts (nepieciešams, lai jau sākumā attēlotu sānjoslu) 
st.sidebar.header("Parametri")

# Datnes izvēlne
sagataves = True
# sagataves = st.sidebar.checkbox("Izmantot iepriekš sagatavotas tabulas", True)

# Ja ir ieķeksēts, tad izvēlas jau sagatavotu tabulu
if sagataves == True:
    datne = "NBA2022-23.csv"
# Ja izņem ķeksi, tad lietotājam nepieciešams augšupielādēt .csv datni patstāvīgi
if sagataves == False:
    datne = st.file_uploader("Augšupielādēt CSV datni", type=".csv")

# Brīdī, kad ir zināms, kura datne tiks lietota, notiek sekojošās darbības:
if datne:

    # Satura sadalījums kolonnās
    col1, col2 = st.columns(2)

    # Datnes nolasīšana
    df = pd.read_csv(datne)
    # Nepieciešamo datu atlase (atmet liekos datus)
    if sagataves == True:
        df_komandas = df.drop(["GP","W","L","WIN%","Min","FGM","FGA","FG%","3PM","3PA","3P%","FTM","FTA","FT%","OREB","DREB","TOV","BLK","BLKA","PF","PFD"], axis=1)
    else:
        df_komandas = df

    # Datu tabulas priekšskatījums
    with col1:
        st.header("Tabulas priekšskatījums")
        st.dataframe(df_komandas)



    # Sānjosla - Mājnieku komandas izvēle
    majnieku_izvelne = sorted(df_komandas['Team'].unique())
    majnieki = st.sidebar.selectbox('Mājnieki', majnieku_izvelne)

    # Sānjosla - Viesu komandas izvēle
    viesu_izvelne = sorted(df_komandas.Team.unique())
    viesi = st.sidebar.selectbox('Viesi', viesu_izvelne)

    with col2:
        # Mājnieku atlases tabulas priekšskatījums
        df_majnieki = df_komandas.loc[df_komandas["Team"] == majnieki]
        st.header("Mājnieki:")
        st.dataframe(df_majnieki)
    
        # Viesu atlases tabulas priekšskatījums
        df_viesi = df_komandas.loc[df_komandas["Team"] == viesi]
        st.header("Viesi:")
        st.dataframe(df_viesi)



    # Vērtību atlase aprēķiniem
    # Points(PTS) 5
    m_pts = df_majnieki.iloc[0,1]
    v_pts = df_viesi.iloc[0,1]
    # Rebounds(REB) 2
    m_reb = df_majnieki.iloc[0,2]
    v_reb = df_viesi.iloc[0,2]
    # Assists(AST) 3
    m_ast = df_majnieki.iloc[0,3]
    v_ast = df_viesi.iloc[0,3]
    # Steals(STL) 1
    m_stl = df_majnieki.iloc[0,4]
    v_stl = df_viesi.iloc[0,4]
    # +/- 4
    m_pm = df_majnieki.iloc[0,5]
    v_pm = df_viesi.iloc[0,5]

    rez1,rez2,rez3,rez4,rez5 = st.columns(5)
    with rez1:
        metric("PTS", m_pts, m_pts - v_pts)
    with rez2:
        metric("REB", m_reb, m_reb - v_reb)
    with rez3:
        metric("AST", m_ast, m_ast - v_ast)
    with rez4:
        metric("STL", m_stl, m_stl - v_stl)
    with rez5:
        metric("+/-", m_pm, m_pm - v_pm)