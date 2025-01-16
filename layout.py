import streamlit as st
from asssistente import *

col1,col2 = st.columns(2)
with col1:
    carregar_arquivo = st.toggle("Carregar arquivo")
with col2:
    tirar_foto = st.toggle("Tirar uma foto")

if carregar_arquivo:
    
    uploaded_file = st.file_uploader("Seleção", type=['pdf','xlsx','csv','jpg','mp3','mp4'], accept_multiple_files=False, help='Insira seus arquivos aqui')
    st.divider()
    col3,col4 = st.columns(2)
    with col3:
        pergunta = st.text_input(placeholder='Faça sua pergunta', label='Pergunta')
    with col4:
        audio_value = st.audio_input(label="")
    if audio_value:
            pergunta = audio(audio_value=audio_value)
    if uploaded_file:
        if '.pdf' in uploaded_file.name:
            conteudo = create_temporary_file(tipo='.pdf',file=uploaded_file)
            botao_perguntar = st.button("Perguntar (PDF)")
            if botao_perguntar:
                if pergunta != '':
                    st.divider()
                    with st.status("Obtendo resposta",expanded=True,state='running') as status:
                            response = ia(pergunta=pergunta, conteudo=conteudo)
                            status.update(label="Resposta obtida",state='complete')
                    st.info(response)
                    botao_download  = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                    delete_temp_file(conteudo)
                    if botao_download:
                        delete_temp_file(f"{pergunta}.tmp")
                else:
                    alert()
        elif '.xlsx' in uploaded_file.name:
            content = create_temporary_file(tipo='.xlsx',file=uploaded_file)
            button = st.button("Perguntar (EXCEL)")
            if button:
                if pergunta != '':
                    st.divider()
                    with st.status("Obtendo resposta",expanded=True,state='running') as status:
                            response = other_files_excel(pergunta=pergunta, file=content)
                            status.update(label="Resposta obtida",state='complete')
                    st.info(response)
                    botao_download = st.download_button("Faça o download da Resposta",response,f'{pergunta}')
                    delete_temp_file(content)
                    if botao_download:
                        delete_temp_file(f"{pergunta}.tmp")
                else:
                    alert()
        elif '.csv' in uploaded_file.name:
            content = create_temporary_file(tipo='.csv',file=uploaded_file)
            button = st.button("Perguntar (CSV)")
            if button:
                if pergunta != '':
                    st.divider()
                    with st.status("Obtendo resposta",expanded=True,state='running') as status:
                            response = other_files_csv(pergunta=pergunta, file=content)
                            status.update(label="Resposta obtida",state='complete')
                    st.info(response)
                    botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                    delete_temp_file(content)
                    if botao_download:
                        delete_temp_file(f"{pergunta}.tmp")
                else:
                    alert()
        elif '.jpeg' in uploaded_file.name or '.jpg' in uploaded_file.name:
            button = st.button("Perguntar (Imagem)")
            if button:
                if pergunta != '':
                    st.divider()
                    response = other_files_jpg(file=uploaded_file,pergunta=pergunta)
                    st.info(response)
                    botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                    if botao_download:
                        delete_temp_file(f'{pergunta}.tmp')
                else:
                    alert()
        elif '.mp3' in uploaded_file.name or '.mp4' in uploaded_file.name:
            button = st.button("Perguntar (Video)")
            if button:
                if pergunta != '':
                    if '.mp3' in uploaded_file.name:
                        tipo = '.mp3'
                    else:
                        tipo = '.mp4'
                    conteudo = create_temporary_file(tipo=tipo,file=uploaded_file)
                    st.divider()
                    response = ia(pergunta=pergunta,conteudo=conteudo)
                    st.info(response)
                    botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                    if botao_download:
                        delete_temp_file(f'{pergunta}.tmp')
                else:
                    alert()

elif tirar_foto:
    foto = st.camera_input("Tire aqui sua foto e a envie para a ia")
    if foto:
        st.divider()
        col5,col6 = st.columns(2)
        with col5:
            pergunta_da_foto = st.text_input(label="Pergunta",placeholder='Insira sua pergunta')
        with col6:
            audio_value_foto = st.audio_input(label="")
            if audio_value_foto:
                 pergunta_da_foto = audio(audio_value=audio_value_foto)
        if pergunta_da_foto:
            botao_foto= st.button("Fazer pergunta da foto")
            if botao_foto:
                if pergunta_da_foto != '':
                    st.divider()
                    response = other_files_jpg(file=foto,pergunta=pergunta_da_foto)
                    st.info(response)
                    botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta_da_foto}")
                    if botao_download:
                        delete_temp_file(f'{pergunta_da_foto}.tmp')
                else:
                    alert()
            

        
       
