import streamlit as st
import google.generativeai as genai

from asssistente import *

col1,col2 = st.columns(2)
with col1:
    carregar_arquivo = st.toggle("Carregar arquivo")
with col2:
    tirar_foto = st.toggle("Tirar uma foto")

if carregar_arquivo:
    uploaded_file = st.file_uploader("Seleção", type=['pdf','xlsx','csv','jpg'], accept_multiple_files=False, help='Insira suas notas aqui', key='Faturamento')
    pergunta = st.text_input(placeholder='Faça sua pergunta', label='Pergunta')
    if uploaded_file:
        if '.pdf' in uploaded_file.name:
            conteudo = create_temporary_file(file=uploaded_file)
            botao_perguntar = st.button("Perguntar (PDF)")
            if botao_perguntar:
                response = ia(pergunta=pergunta, conteudo=conteudo)
                st.info(response)
                botao_download  = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                delete_temp_file(conteudo)
                if botao_download:
                    delete_temp_file(f"{pergunta}.tmp")
        elif '.xlsx' in uploaded_file.name:
            content = create_temporary_file(file=uploaded_file)
            button = st.button("Perguntar (EXCEL)")
            if button:
                response = other_files_excel(file=content,pergunta=pergunta)
                st.info(response)
                botao_download = st.download_button("Faça o download da Resposta",response,f'{pergunta}')
                delete_temp_file(content)
                if botao_download:
                    delete_temp_file(f"{pergunta}.tmp")
        elif '.csv' in uploaded_file.name:
            content = create_temporary_file(file=uploaded_file)
            button = st.button("Perguntar (CSV)")
            if button:
                response = other_files_csv(file=content,pergunta=pergunta)
                st.info(response)
                botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                delete_temp_file(content)
                if botao_download:
                    delete_temp_file(f"{pergunta}.tmp")
        elif '.jpeg' in uploaded_file.name or '.jpg' in uploaded_file.name:
            button = st.button("Perguntar (Imagem)")
            if button:
                response = other_files_jpg(file=uploaded_file,pergunta=pergunta)
                st.info(response)
                botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                if botao_download:
                    delete_temp_file(f'{pergunta}.tmp')

elif tirar_foto:
    foto = st.camera_input("Tire aqui sua foto e a envie para a ia")
    if foto:
        pergunta_da_foto = st.text_input(label="Pergunta",placeholder='Insira sua pergunta')
        if pergunta_da_foto:
            botao_foto= st.button("Fazer pergunta da foto")
            if botao_foto:
                response = other_files_jpg(file=foto,pergunta=pergunta_da_foto)
                st.info(response)
                botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta_da_foto}")
                if botao_download:
                    delete_temp_file(f'{pergunta_da_foto}.tmp')
            
