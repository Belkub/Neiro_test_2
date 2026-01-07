import numpy as np
import math


import pickle
import streamlit as st
import pandas as pd
import speech_recognition as sr


#st.title('Bentonite Co')
img = Image.open("bent.png")
st.image(img, width=200)

st.subheader("Справочник реологических критериев качества бентонита")

df = pd.read_excel('krit.xls')

a = st.checkbox('Пластическая вязкость (PV)')
if a:
    st.success(df.loc[df['понятие'] == 'PV', 'вывод'][0])
b = st.checkbox('Динамическое напряжение сдвига или предел текучести (YP)')
if b:
    st.success(df.loc[df['понятие'] == 'YP', 'вывод'][1])
c = st.checkbox('Соотношение динамического напряжения сдвига и пластической вязкости (YP/PV)')
if c:
    st.success(df.loc[df['понятие'] == 'YP/PV', 'вывод'][2])
d = st.checkbox('Эффективная вязкость F')
if d:
    st.success(df.loc[df['понятие'] == 'ф600', 'вывод'][3])
e = st.checkbox('Понятие хрупкости структуры геля')
if e:
    st.success(df.loc[df['понятие'] == 'понятие хрупкости структуры геля', 'вывод'][4])
f = st.checkbox('Связь PV со свойствами бентонита')
if f:
    st.success(df.loc[df['понятие'] == 'связь PV с бентонитом', 'вывод'][5])
g = st.checkbox('Cвязь эффективной вязкости (ф600/2) со свойствами бентонита')
if g:
    st.success(df.loc[df['понятие'] == 'связь ф600 с бентонитом', 'вывод'][6])
h = st.checkbox('Связь YP со свойствами бентонита')
if h:
    st.success(df.loc[df['понятие'] == 'связь YP с бентонитом', 'вывод'][7])
i = st.checkbox('Баланс прочности структуры бентонитового геля')
if i:
    st.success(df.loc[df['понятие'] == 'баланс прочности', 'вывод'][8])
j = st.checkbox('Влияние активации содой на реологию суспензии бентонита')
if j:
    st.success(df.loc[df['понятие'] == 'активация содой', 'вывод'][9])
k = st.checkbox('Фактор YP/PV')
if k:
    st.success(df.loc[df['понятие'] == 'фактор YP/PV', 'вывод'][10])
m = st.checkbox('Критерий изотропии')
if m:
    st.success(df.loc[df['понятие'] == 'критерий изотропии', 'вывод'][11])
n = st.checkbox('Критерий генерации')
if n:
    st.success(df.loc[df['понятие'] == 'критерий генерации', 'вывод'][12])
o = st.checkbox('Критерий загущения')
if o:
    st.success(df.loc[df['понятие'] == 'критерий загущения', 'вывод'][13])
p = st.checkbox('Критерий полноты')
if p:
    st.success(df.loc[df['понятие'] == 'критерий полноты', 'вывод'][14])
r = st.checkbox('Приоритет критериев')
if r:
    st.success(df.loc[df['понятие'] == 'принятие решений', 'вывод'][15])




    



