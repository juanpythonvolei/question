import streamlit as st
import google.generativeai as genai

from asssistente import ia,create_temporary_file

uploaded_file = st.file_uploader("Seleção", type=['pdf'], accept_multiple_files=False, help='Insira suas notas aqui', key='Faturamento')
pergunta = st.text_input(placeholder='Faça sua pergunta', label='Pergunta')
if uploaded_file:
    conteudo = create_temporary_file(uploaded_file)
    botao_perguntar = st.button("Perguntar")
    if botao_perguntar:
        ia(pergunta=pergunta, conteudo=conteudo)
