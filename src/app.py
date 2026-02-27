import json
import streamlit as st
import  pandas as pd
import requests

# ===================== CONFIGURAÇÃO =====================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gemma:2b"

# ===================== Carregar Dados =====================

perfil = json.load(open('./data/perfil_do_usuario.json'))
historico = pd.read_csv('./data/historico_atendimento.csv')
metas = json.load(open('./data/metas_usuario.json'))




# ===================== Montar Contexto =====================
contexto = f"""
CLIENTE : {perfil['nome']}, {perfil['idade']} anos,perfil {perfil['escolaridade']} , {perfil ['situacao_profissional']} , {['area_interesse_profissional']}


Atendimentos Anteriores :
{historico.to_string(index=False)}



"""
PERGUNTAS_ENTREVISTA = [
    "Como você se sente em relação à sua situação profissional atual?",
    "Você está satisfeito com sua carreira hoje?",
    "Quais habilidades você acredita que mais domina?",
    "Qual é seu principal objetivo profissional no momento?"
]

# ===================== SYSTEM PROMPT =====================

SYSTEM_PROMPT = """
Você é o ORIENTA, um agente profissional de orientação de carreira.

OBJETIVO:
Orientar sobre Carreira Profissional.

REGRAS ABSOLUTAS:
1. Identifique-se como ORIENTA apenas na primeira resposta da conversa. Nunca se reapresente depois.
2. Nunca reinicie a conversa. Toda pergunta do usuário deve ser tratada como continuação do diálogo.
3. Não faça perguntas meta ou de boas-vindas. Sempre mantenha foco na orientação profissional.
4. Use apenas informações explicitamente fornecidas nesta sessão. Não presuma histórico, intenções ou objetivos do usuário.
5. Quando houver informações suficientes, infira e declare um perfil profissional inicial. Sempre deixe claro que é provisório.
6. Se o usuário pedir avaliação "com base no que já foi informado", responda diretamente com o que é possível e declare limites se necessário.
7. Faça no máximo uma pergunta por resposta, apenas se for absolutamente necessária e relevante.
8. Linguagem curta, neutra e profissional. Máximo de 2 frases para entradas curtas.
9. Nunca transforme inferência em afirmação de objetivo. Objetivos só podem ser declarados se o usuário os tiver dito explicitamente.
10. Perguntas como "e agora?" ou "qual o próximo passo?" devem gerar apenas orientação prática direta, sem novas perguntas.
11 - Dados Sensíveis jamais serão fornecidos Peça desculpas e admita não ter acesso a essa informação.
12 - Perguntas fora do tema sobre Carreira Profissional , não poderão ser respondidas, caso ocorra responda lembrando qual a sua finalidade  como Orientador Profissional.
13 -  Se não souber algo, admita e ofereça alternativas.
14 - Sempre ao final de cada resposta pergunte se o usuário entendeu.
"""


# ===================== CHAMAR OLLAMA =====================

def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""
        
    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

# ============ INTERFACE ============
st.title(" Orienta, Seu Orientador de Carreira Profissional")

if pergunta := st.chat_input("Sua Dúvida sobre Carreira Profissional..."):
   st.chat_message("user").write(pergunta)
   with st.spinner("..."):
       st.chat_message("assistant").write(perguntar(pergunta)) 
