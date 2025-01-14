import google.generativeai as genai
import streamlit as st
import tempfile
import os
def ia(pergunta,conteudo):
  # conteudo = r'C:\Users\juanz\OneDrive\Área de Trabalho\regras_do_volei.pdf'


    genai.configure(api_key=os.getenv("api")) 
    model = genai.GenerativeModel('gemini-1.5-flash') 
    chat = model.start_chat(history=[{"role":"user","parts":[genai.upload_file(conteudo)]}]) 
    response = chat.send_message(f'Você é um árbitro de volei e sua função é se um consultor dotado do conhecimento desse esporte e assim, ajudar com qualquer pergunta que lhe for necessitada. Suas informações devem ser respaldadas no livro de regras oficiais de volei que estou te passando. Assim sendo responda a essa pergunta:{pergunta}') 
    return st.info(response.text)

def create_temporary_file(file):
  with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(file.read())
        return tmp_file.name