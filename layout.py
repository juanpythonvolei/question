import streamlit as st
from engine.assistente import *

col1,col2 = st.columns(2)
with col1:
    carregar_arquivo = st.toggle("Carregar arquivo")
with col2:
    tirar_foto = st.toggle("Tirar uma foto")
st.divider()
if carregar_arquivo:
    escolha = st.pills(label="Selecione a quantidade de arquivos",options=['Arquivo único','Vários Arquivos'])
    st.divider()
    if escolha:
        if escolha == 'Arquivo único':
            uploaded_file = st.file_uploader("Seleção", type=['pdf','xlsx','csv','jpg','py','html','css','js','txt','docx','jpg','mp4','mp3'], accept_multiple_files=False, help='Insira seus arquivos aqui')
        else:
            uploaded_file = st.file_uploader("Seleção Arquivos", type=['pdf','xlsx','csv','py','html','css','js','txt','jpg','docx','mp4','mp3'], accept_multiple_files=True, help='Insira seus arquivos aqui')
        st.divider()
        col3,col4 = st.columns(2)
        with col3:
            pergunta = st.text_input(placeholder='Faça sua pergunta', label='Pergunta')
        with col4:
            audio_value = st.audio_input(label="")
        if audio_value:
                pergunta = audio(audio_value=audio_value)
        if escolha == 'Arquivo único':
            if uploaded_file:
                if '.pdf' in uploaded_file.name:
                    conteudo = create_temporary_file(tipo='.pdf',file=uploaded_file)
                    botao_perguntar = st.button("Perguntar (PDF)")
                    if botao_perguntar:
                        if pergunta != '':
                            st.divider()
                            with st.status("Obtendo resposta",expanded=True,state='running') as status:
                                    response = ia(pergunta=pergunta, conteudo=conteudo)
                                    create_audio(response)
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
                                    create_audio(response)
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
                                    create_audio(response)
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
                            with st.status("Obtendo resposta",expanded=True,state='running') as status:
                                response = other_files_jpg(file=uploaded_file,pergunta=pergunta)
                                create_audio(response)
                                status.update(label="Resposta obtida",state='complete')
                            st.info(response)
                            botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                            if botao_download:
                                delete_temp_file(f'{pergunta}.tmp')
                        else:
                            alert()
                else:
                    button = st.button("Perguntar (Diversos)")
                    if button:
                        if pergunta != '':
                            tipo = str(uploaded_file.name).split('.')
                            content = create_temporary_file(tipo=f'.{tipo[1]}',file=uploaded_file)
                            st.divider()
                            with st.status("Obtendo resposta",expanded=True,state='running') as status:
                                if '.docx' in uploaded_file.name:
                                    response = read_word(pergunta=pergunta,conteudo=content)
                                else:
                                    response = ia(pergunta=pergunta,conteudo=content)
                                create_audio(response)
                                status.update(label="Resposta obtida",state='complete')
                            st.info(response)
                            st.audio('./audio/audio.mp3',format='audio/mpeg')
                            botao_download = st.download_button("Faça o download da Resposta",response,f"{pergunta}")
                            if botao_download:
                                delete_temp_file(f'{pergunta}.tmp')
                        else:
                            alert()
            else:
                try:
                    delete_temp_file('./audio/audio.mp3')
                except:
                    pass
        else:
            if uploaded_file:
                botao_arquivos = st.button("Perguntar (Vários arquivos)")
                if botao_arquivos:
                    if pergunta != '':
                        st.divider()
                        with st.status("Obtendo resposta",expanded=True,state='running') as status:
                            response = multiple_files(pergunta=pergunta,files=uploaded_file)
                            status.update(label="Resposta obtida",state='complete')
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
            

        
       
