import google.generativeai as genai
import streamlit as st
import tempfile
import os
import pandas as pd
import speech_recognition as sr
key = os.getenv('api')
genai.configure(api_key=key)


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

def other_files_video(file,pergunta):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(file.read())
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [genai.upload_file(tmp_file.name)]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
    delete_temp_file(tmp_file.name)
    return response.text

def other_files_jpg(file,pergunta):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(file.read())
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [genai.upload_file(tmp_file.name)]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
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


def ia(pergunta,conteudo): 
    model = genai.GenerativeModel('gemini-1.5-flash') 
    chat = model.start_chat(history=[{"role":"user","parts":[genai.upload_file(conteudo)]}]) 
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}') 
    return response.text

def create_temporary_file(tipo,file):
  with tempfile.NamedTemporaryFile(delete=False, suffix=tipo) as tmp_file:
        tmp_file.write(file.read())
        return tmp_file.name
