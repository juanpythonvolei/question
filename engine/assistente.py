import google.generativeai as genai
import streamlit as st
import tempfile
import os
import pandas as pd
import speech_recognition as sr
from gtts import gTTS
key = os.getenv('api')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-1.5-flash')


def create_audio(text):
    audio = gTTS(text,lang='pt')
    if os.path.exists('./audio'):
          audio.save('./audio/audio.mp3')
    else:
          os.makedirs('./audio')
          audio.save('./audio/audio.mp3')

def multiple_files(pergunta,files):
        uploaded_parts = []
        final = ''
        for file in files:
            if '.pdf' in file.name:
                tempfile = create_temporary_file(tipo='.pdf',file=file)
                arquivo_carregado = genai.upload_file(tempfile)
                uploaded_parts.append(arquivo_carregado)
                delete_temp_file(tempfile)
            elif '.xlsx' in file.name or '.csv' in file.name :   
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    try:
                        data  = pd.read_excel(tempfile)
                    except:
                          data = pd.read_csv(tempfile)
                    texto = data.to_string()
                    final += f'''Dados do arquivo {tempfile}:\n
                    {texto}
                    \n'''
                    delete_temp_file(tempfile)
            elif '.jpg' in file.name or '.jpeg' in file.name:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    arquivo_carregado = genai.upload_file(tempfile)
                    uploaded_parts.append(arquivo_carregado)
                    delete_temp_file(tempfile)
            elif '.docx' in file.name:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    doc = Document(tempfile)
                    for paragraph in doc.paragraphs:
                        final += f'{paragraph.text}\n'
                    delete_temp_file(tempfile)
            else:
                    arquivo = str(file.name).split('.')
                    tempfile = create_temporary_file(tipo=f'.{arquivo[1]}',file=file)
                    with open(tempfile,'rb') as tmp:
                        txt = tmp.read()
                    final += str(f'''Conteúdo código {tempfile}:\n
                                     {txt}
\n''')
                    delete_temp_file(tempfile)
        uploaded_parts.append({'text':final})
        model = genai.GenerativeModel('gemini-1.5-flash') 
        chat = model.start_chat(history=[{"role":"user","parts":uploaded_parts}]) 
        response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
        return response.text
        

              
@st.dialog("Atenção")
def alert():
     st.text("Você deve realizar uma pergunta")

def audio(audio_value):
    rec = sr.Recognizer()
    with sr.AudioFile(audio_value) as arquivo_audio:
                    audio = rec.record(arquivo_audio)
                    texto = rec.recognize_google(audio,language ='pt-BR ')
    return texto

def delete_temp_file(file):
    if os.path.exists(file): 
        os.remove(file)

def other_files_jpg(file,pergunta):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(file.read())
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [genai.upload_file(tmp_file.name)]}])
    with st.status("Obtendo resposta",expanded=True,state='running') as status:
                            response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
                            status.update(label="Resposta obtida",state='complete')
    delete_temp_file(tmp_file.name)
    return response.text

def other_files_csv(file,pergunta):
    arquivo  = pd.read_csv(file)
    texto = arquivo.to_string()
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [{"text": texto}]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
    return response.text

def other_files_excel(file,pergunta):
    arquivo  = pd.read_excel(file)
    texto = arquivo.to_string()
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [{"text": texto}]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
    return response.text


def ia(pergunta,conteudo,mime=None):
    if '.mp4' in conteudo or '.mp3' in conteudo:
          mime = 'video/mp4' 
    model = genai.GenerativeModel('gemini-1.5-flash') 
    chat = model.start_chat(history=[{"role":"user","parts":[genai.upload_file(conteudo,mime_type=mime)]}]) 
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}') 
    return response.text

def create_temporary_file(tipo,file):
  with tempfile.NamedTemporaryFile(delete=False, suffix=tipo) as tmp_file:
        tmp_file.write(file.read())
        return tmp_file.name
  
def read_word(pergunta,conteudo):
    texto = ''
    doc = Document(conteudo)
    for paragraph in doc.paragraphs:
          texto += f'{paragraph.text}\n'
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [{"text": texto}]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
    delete_temp_file(conteudo)
    return response.text
