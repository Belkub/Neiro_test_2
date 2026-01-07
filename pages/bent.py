import numpy as np
import math
from PIL import Image

import pickle
import streamlit as st
import pandas as pd
import speech_recognition as sr

def voice():
    def speech_to_text(audio_file):
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language="ru-RU")
                return text
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError as e:
                return f"Error: {str(e)}"
    recognizer = sr.Recognizer()   
    audio_value = st.audio_input("Record a voice message")
    if audio_value:
       # st.audio(audio_value)
        text = speech_to_text(audio_value)
        return text


#st.title('Bentonite Co')
img = Image.open("bent.png")
st.image(img, width=200)

st.subheader("Анализ бентопорошка")



rr_1 = st.checkbox('Голосовой ввод названия бентонита')
if rr_1:
    text = voice()
    if text:
        with open("file.txt", "w") as file:  
            file.write(text)
            file.close()
with open("file.txt", "r") as file:  
    text = file.read()
    file.close()
name = st.text_input('Название бентонита: ', value = text)

MM = st.number_input('Смектит, %: ', min_value = 40.0, max_value = 100.0, value = 70.0, step = 0.5)
KOE = st.number_input('Обменная емкость мс, мг-экв/100г: ', min_value = 30.0, max_value = 160.0, value = 70.0, step = 0.5)
W = st.number_input('Влажность порошка, %: ', min_value = 2.0, max_value = 25.0, value = 12.0, step = 0.5)

bn = st.checkbox('Рассчитать эквивалент?')
if bn:
    w = st.number_input('Влага глины, %: ', min_value = 2.0, max_value = 40.0, value = 15.0, step = 0.5)
    m = st.number_input('Молек масса ПАВ, г/моль: ', min_value = 80.0, max_value = 700.0, value = 500.0, step = 0.5)
    E = round(0.001*10*m*(1 - w*0.01)*KOE/(1-W*0.01), 1)

st.write('API-test')
f600 = st.slider('FANN_600', 10, 140, 70)

f300 = st.slider('FANN_300', 5, 130, 60)

PV = f600 - f300
YP = f300 - PV
 
n = round(3.32*math.log10((YP+PV+PV)/(YP+PV)),1)
K = round((YP+PV)*0.511/(511**n),1)
PKOE = round(KOE/(1-0.01*W),1)
LSRV = round(1000*n*K*(0.3/60)**(n-1),1)
I = round(MM*MM*0.01*0.01*(0.5-(YP/f600-0.5)**2),2)
V = round(f600/(0.01*0.01*MM*MM*KOE),2)
GEN = round(f600*(1 - (YP/f600))*MM/KOE,1)

POL = round(KOE*MM*MM*0.01*0.01*math.log10(f600*0.001)**2/(YP/f600),1)

if st.button('Расчет'):

    if YP/PV > 6:
        st.error(f'YP/PV: {YP/PV:,.1f}')
    elif YP/PV <= 6 and YP/PV > 3:
        st.warning(f'YP/PV: {YP/PV:,.1f}')
    else:
        st.success(f'YP/PV: {YP/PV:,.1f}')

    if I < 0.2:
        st.error(f'Критерий изотропии: {I:,.2f}')
    elif I >= 0.2 and I < 0.24:
        st.warning(f'Критерий изотропии: {I:,.2f}')
    else:
        st.success(f'Критерий изотропии: {I:,.2f}')

    if GEN < 4:
        st.error(f'Критерий генерации: {GEN:,.1f}')
    elif GEN >= 4 and GEN < 12:
        st.warning(f'Критерий генерации: {GEN:,.1f}')
    else:
        st.success(f'Критерий генерации: {GEN:,.1f}')

    if V > 1.3:
        st.error(f'Критерий загущения: {V:,.2f}')
    elif V <= 1.3 and V >= 1:
        st.warning(f'Критерий загущения: {V:,.2f}')
    else:
        st.success(f'Критерий загущения: {V:,.2f}')

    if POL < 100:
        st.error(f'Критерий полноты: {POL:,.1f}')
    elif POL >= 100 and POL <= 115:
        st.warning(f'Критерий полноты: {POL:,.1f}')
    else:
        st.success(f'Критерий полноты: {POL:,.1f}')

    if bn:
        st.success(f'Эквивалент ПАВ, г/кг: {E:,.1f}')
        
    df = pd.DataFrame({'Бентонит':[name], 'Смектит %':[MM], 'КОЕ мг-экв/100г':[KOE], 'Влажность %':[W], 'ПКОЕ мг-экв/100г': [round(PKOE,1)], 'F sP':[round(f600/2,1)], 'PV sP':[PV], 'YP sqf':[YP], 'K sP**n':[round(K,1)], 'n':[round(n,1)], 'LSRV sP':[round(LSRV,1)]})   
    df_1 = pd.DataFrame({'Бентонит':[name], 'YP/PV':[round(YP/PV,1)], 'Критерий изотропии':[round(I,2)], 'Критерий генерации':[round(GEN,1)], 'Критерий загущения': [round(V,2)], 'Критерий полноты':[round(POL,1)]})
    
##    pp = st.checkbox('Сформировать сводную таблицу реологии')
##    ss = st.checkbox('Сформировать сводную таблицу критериев')
##    if pp:
    st.snow()
    st.subheader(f"Реологические свойства суспензии бентонита '{name}' по API")
    st.dataframe(df)
    st.subheader(f"Критерии пригодности бентонита '{name}' для органомодификации")
    st.dataframe(df_1)
    if bn:
        df_2 = pd.DataFrame({'Бентонит':[name], 'Смектит %':[MM], 'КОЕ мг-экв/100г':[KOE], 'Влага глины %':[w], 'ПКОЕ мг-экв/100г': [round(PKOE,1)],'Эквивалент ПАВ г/кг': [E]})
        st.subheader(f"Эквивалент ПАВ для бентонита '{name}'")
        st.dataframe(df_2)
##        st.title('Создание сводной таблицы реологии')
##        bn = st.checkbox('Вывести таблицу и ограничить число полей')
##        if bn:
##            number = df.columns
##            num = st.multiselect('Выбрать значимые поля', list(df.columns))
##            if num:
##                number = num
##            
##            if st.button('Вывести таблицу'):
##                st.snow()
##                st.dataframe(df[number]) 
##            
##        else:
##            number = list(df.columns)
##    if ss:
##        st.title('Создание сводной таблицы критериев')
##        bb = st.checkbox('Вывести таблицу и ограничить число полей')
##        if bb:
##            number = df_1.columns
##            num = st.multiselect('Выбрать значимые поля', list(df_1.columns))
##            if num:
##                number = num
##            
##            if st.button('Вывести таблицу'):
##                st.snow()
##                st.dataframe(df_1[number]) 
##            
##        else:
##            number = list(df_1.columns)    


