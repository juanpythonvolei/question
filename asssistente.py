import google.generativeai as genai
import streamlit as st
import tempfile
import os
import pandas as pd

key = os.getenv('api')
genai.configure(api_key=key)


def other_files_jpg(file,pergunta):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        tmp_file.write(file.read())
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[{"role": "user", "parts": [genai.upload_file(tmp_file.name)]}])
    response = chat.send_message(f'Você é uma analista e sua função é reponder as peguntas se baseando nas informações que você está recebendo. Assim sendo responda a essa pergunta:{pergunta}')
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

def create_temporary_file(file):
  with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(file.read())
        return tmp_file.name
