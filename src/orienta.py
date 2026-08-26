import json
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

# ============================================================
# CONFIGURAÇÃO
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
MODELO = "gemma:2b"


# ============================================================
# CARREGAR DADOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONHECIMENTO_DIR = DATA_DIR / "conhecimento"
HISTORICO_CSV_PATH = DATA_DIR / "historico_atendimento.csv"

with open(DATA_DIR / "perfil_do_usuario.json", encoding="utf-8") as arquivo:
    perfil = json.load(arquivo)

with open(DATA_DIR / "metas_usuario.json", encoding="utf-8") as arquivo:
    metas = json.load(arquivo)


# ============================================================
# MONTAR CONTEXTO DO CLIENTE (APENAS DADOS CADASTRAIS)
# ============================================================

contexto_cadastral = f"""
CLIENTE:

Nome: {perfil['nome']}
Idade: {perfil['idade']}
Escolaridade: {perfil['escolaridade']}
Situação profissional: {perfil['situacao_profissional']}
Área de interesse principal: {perfil['area_interesse_profissional']}

METAS DO USUÁRIO:
{metas}
"""


# ============================================================
# FUNÇÕES DE CONHECIMENTO PROFISSIONAL
# ============================================================

def normalizar_texto(texto):
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFD", texto)
    texto_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return texto_sem_acento.lower().strip().replace(" ", "_")


def carregar_conhecimento_profissional(area):
    if not area:
        return {}

    nome_arquivo = normalizar_texto(area)
    arquivo_conhecimento = CONHECIMENTO_DIR / f"{nome_arquivo}.json"

    if not arquivo_conhecimento.exists():
        return {}

    try:
        with open(arquivo_conhecimento, encoding="utf-8") as arquivo:
            conhecimento = json.load(arquivo)
        return conhecimento
    except Exception:
        return {}


def encontrar_profissoes_por_habilidade(conhecimento, habilidade):
    if not conhecimento:
        return []

    habilidade = habilidade.strip().lower()
    profissoes_encontradas = []

    for profissao in conhecimento.get("profissoes", []):
        habilidades = profissao.get("habilidades", [])
        for item in habilidades:
            if item.strip().lower() == habilidade:
                profissoes_encontradas.append(profissao)
                break

    return profissoes_encontradas


def identificar_habilidade(mensagem, conhecimento=None):
    mensagem = mensagem.lower()

    if conhecimento:
        for profissao in conhecimento.get("profissoes", []):
            for habilidade in profissao.get("habilidades", []):
                if habilidade.lower() in mensagem:
                    return habilidade.lower()

    if CONHECIMENTO_DIR.exists():
        for arquivo_json in CONHECIMENTO_DIR.glob("*.json"):
            try:
                with open(arquivo_json, encoding="utf-8") as f:
                    dados = json.load(f)
                    for profissao in dados.get("profissoes", []):
                        for habilidade in profissao.get("habilidades", []):
                            if habilidade.lower() in mensagem:
                                return habilidade.lower()
            except Exception:
                continue

    return None


def identificar_area_profissional(mensagem):
    mensagem = mensagem.lower()
    areas = {
        "tecnologia": [
            "tecnologia",
            "programação",
            "programacao",
            "programador",
            "desenvolvimento",
            "desenvolvedor",
            "software",
            "python",
            "java",
            "computação",
            "computacao",
            "dados",
            "inteligência artificial",
            "inteligencia artificial",
            "ia",
        ],
        "saude": [
            "saúde",
            "saude",
            "medicina",
            "enfermagem",
            "enfermeiro",
            "médico",
            "medico",
            "hospital",
            "fisioterapia",
            "fisioterapeuta",
            "nutrição",
            "farmácia",
        ],
        "engenharia": [
            "engenharia",
            "engenheiro",
            "engenheira",
            "obras",
            "civil",
            "mecânica",
            "elétrica",
        ],
        "administracao": [
            "administração",
            "administracao",
            "administrador",
            "gestão",
            "gestao",
            "financeiro",
            "recursos humanos",
            "rh",
            "fluxo de caixa",
            "excel",
        ],
        "educacao": [
            "educação",
            "educacao",
            "professor",
            "professora",
            "ensino",
            "pedagogia",
            "escola",
        ],
        "marketing": [
            "marketing",
            "publicidade",
            "propaganda",
            "social media",
            "copywriting",
            "tráfego",
        ],
    }

    for area, termos in areas.items():
        for termo in termos:
            if termo in mensagem:
                return area

    return None


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
VOCÊ É:
Você é o ORIENTA, um agente profissional de orientação de carreira.

FINALIDADE:
Sua única finalidade é auxiliar o usuário em assuntos relacionados a:
- carreira profissional;
- mercado de trabalho;
- desenvolvimento profissional;
- estudos relacionados à carreira;
- habilidades profissionais;
- formação profissional;
- currículo;
- entrevistas de emprego;
- transição de carreira;
- planejamento profissional.

==================================================
REGRA CRÍTICA DE ISOLAMENTO DE DADOS (ATENÇÃO)
==================================================
- NUNCA atribua habilidades ao usuário a menos que ele as tenha mencionado EXPLICITAMENTE na conversa atual.
- Se o usuário disser apenas que tem interesse em uma área (ex: "tenho afinidade com tecnologia"), responda confirmando o interesse na área e PERGUNTE o que ele gosta de fazer ou já estudou nessa área.
- NUNCA assuma ou diga que o usuário possui habilidades como redação, storytelling ou marketing a menos que ele diga isso AGORA.

==================================================
IDIOMA
==================================================
Responda SEMPRE em português do Brasil.
NUNCA responda em inglês ou alterne entre idiomas.

==================================================
APRESENTAÇÃO
==================================================
Na primeira resposta da conversa, apresente-se brevemente como ORIENTA.
Exemplo: "Olá! Eu sou o ORIENTA, seu agente de orientação profissional e de carreira."
Depois da primeira resposta, NÃO se apresente novamente.

==================================================
FIDELIDADE AO USUÁRIO
==================================================
Nunca presuma informações que o usuário não forneceu na sessão atual.

==================================================
ESCOPO
==================================================
Se a mensagem for de carreira, responda normalmente.
Se NÃO for de carreira, informe que sua finalidade é orientação profissional.

==================================================
INFORMAÇÕES PRIVADAS
==================================================
Nunca forneça senhas, dados bancários ou documentos.

==================================================
PERGUNTAS
==================================================
Faça no máximo uma pergunta por resposta, apenas quando estritamente necessário.

==================================================
ESTILO
==================================================
Seja claro, objetivo, profissional, natural e curto.
"""


# ============================================================
# MEMÓRIA DA CONVERSA
# ============================================================

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "primeira_mensagem" not in st.session_state:
    st.session_state.primeira_mensagem = True


# ============================================================
# FUNÇÕES DE PERSISTÊNCIA NO CSV
# ============================================================

def salvar_historico_no_csv():
    """
    Agrupa os pares de Pergunta (user) e Resposta (assistant)
    da sessão atual e grava no arquivo historico_atendimento.csv.
    """
    mensagens = st.session_state.mensagens
    if not mensagens:
        return False

    novos_registros = []
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nome_usuario = perfil.get("nome", "Usuário")

    # Mapeia mensagens do usuário com as respostas correspondentes do assistente
    i = 0
    while i < len(mensagens):
        if mensagens[i]["role"] == "user":
            pergunta = mensagens[i]["content"]
            resposta = ""
            if i + 1 < len(mensagens) and mensagens[i + 1]["role"] == "assistant":
                resposta = mensagens[i + 1]["content"]
                i += 1

            novos_registros.append(
                {
                    "data": data_atual,
                    "usuario": nome_usuario,
                    "mensagem_usuario": pergunta,
                    "resposta_agente": resposta,
                }
            )
        i += 1

    if novos_registros:
        df_novos = pd.DataFrame(novos_registros)
        if HISTORICO_CSV_PATH.exists():
            df_novos.to_csv(
                HISTORICO_CSV_PATH, mode="a", header=False, index=False, encoding="utf-8"
            )
        else:
            df_novos.to_csv(HISTORICO_CSV_PATH, mode="w", header=True, index=False, encoding="utf-8")
        return True

    return False


# ============================================================
# FUNÇÕES DE VALIDAÇÃO E OLLAMA
# ============================================================

def detectar_informacao_privada(pergunta):
    pergunta = pergunta.lower()
    termos_sensiveis = [
        "senha",
        "password",
        "código de acesso",
        "codigo de acesso",
        "token de acesso",
        "login de outra pessoa",
        "conta de outra pessoa",
        "dados bancários",
        "dados bancarios",
        "número do cartão",
        "numero do cartao",
    ]
    return any(termo in pergunta for termo in termos_sensiveis)


def detectar_fora_de_escopo(pergunta):
    pergunta = pergunta.lower()
    termos_fora = [
        "receita",
        "bolo",
        "ingredientes",
        "culinária",
        "futebol",
        "copa",
        "jogo",
        "time",
        "previsão do tempo",
        "clima",
        "chover",
        "filme",
        "série",
        "música",
        "piada",
    ]
    return any(termo in pergunta for termo in termos_fora)


def perguntar(msg):
    area_detectada = identificar_area_profissional(msg)
    conhecimento_temporario = (
        carregar_conhecimento_profissional(area_detectada) if area_detectada else None
    )
    habilidade_detectada = identificar_habilidade(msg, conhecimento_temporario)

    area_da_habilidade = None
    if habilidade_detectada and CONHECIMENTO_DIR.exists():
        for arquivo_json in CONHECIMENTO_DIR.glob("*.json"):
            try:
                with open(arquivo_json, encoding="utf-8") as f:
                    dados = json.load(f)
                    for prof in dados.get("profissoes", []):
                        if any(
                            h.lower() == habilidade_detectada for h in prof.get("habilidades", [])
                        ):
                            area_da_habilidade = dados.get("area", "").lower()
                            break
            except Exception:
                continue

    area_final = (
        area_da_habilidade or area_detectada or perfil.get("area_interesse_profissional", "")
    )
    conhecimento_profissional = carregar_conhecimento_profissional(area_final)

    if habilidade_detectada:
        profissoes_relacionadas = encontrar_profissoes_por_habilidade(
            conhecimento_profissional, habilidade_detectada
        )
    else:
        profissoes_relacionadas = conhecimento_profissional.get("profissoes", [])

    contexto_profissional = json.dumps(
        {
            "area": conhecimento_profissional.get("area", area_final.capitalize()),
            "habilidade_detectada_nesta_mensagem": habilidade_detectada,
            "profissoes_disponiveis": profissoes_relacionadas,
        },
        ensure_ascii=False,
        indent=2,
    )

    if st.session_state.primeira_mensagem:
        instrucao_apresentacao = (
            "ESTA É A PRIMEIRA RESPOSTA DA CONVERSA. "
            "Apresente-se brevemente como ORIENTA, agente profissional de orientação de carreira. "
            "Depois, responda à dúvida."
        )
        st.session_state.primeira_mensagem = False
    else:
        instrucao_apresentacao = (
            "ESTA NÃO É A PRIMEIRA RESPOSTA DA CONVERSA. "
            "NÃO se apresente novamente. Continue a conversa."
        )

    messages_payload = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": instrucao_apresentacao},
        {"role": "system", "content": f"DADOS CADASTRAIS DO CLIENTE:\n\n{contexto_cadastral}"},
        {"role": "system", "content": f"CONHECIMENTO DA ÁREA CONSULTADA:\n\n{contexto_profissional}"},
    ]

    messages_payload.extend(st.session_state.mensagens)

    try:
        resposta_ollama = requests.post(
            OLLAMA_URL,
            json={
                "model": MODELO,
                "messages": messages_payload,
                "stream": False,
                "options": {"temperature": 0.2, "top_p": 0.8},
            },
            timeout=120,
        )
        resposta_ollama.raise_for_status()
        return resposta_ollama.json()["message"]["content"]

    except requests.exceptions.ConnectionError:
        return "Não foi possível conectar ao Ollama. Verifique se ele está rodando."
    except Exception as erro:
        return f"Erro ao consultar o Ollama: {erro}"


# ============================================================
# INTERFACE STREAMLIT
# ============================================================

st.title("🤖 ORIENTA")
st.subheader("Seu Orientador de Carreira Profissional")

# Painel Lateral para Gestão da Sessão
with st.sidebar:
    st.header("Opções da Sessão")
    if st.button("💾 Finalizar e Salvar Atendimento"):
        if st.session_state.mensagens:
            sucesso = salvar_historico_no_csv()
            if sucesso:
                st.success("Atendimento salvo no histórico!")
                st.session_state.mensagens = []
                st.session_state.primeira_mensagem = True
                st.rerun()
            else:
                st.warning("Não há novas mensagens para salvar.")
        else:
            st.info("O histórico está vazio.")

# Renderiza histórico na tela
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

# Captura novo input
if pergunta := st.chat_input("Sua dúvida sobre carreira profissional..."):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        if detectar_informacao_privada(pergunta):
            resposta = "Não posso fornecer, descobrir ou orientar sobre senhas, códigos de acesso ou informações privadas de outras pessoas."
        elif detectar_fora_de_escopo(pergunta):
            resposta = "Sou o ORIENTA, um agente de orientação profissional. Posso ajudar apenas com questões relacionadas a carreira, estudos, habilidades e desenvolvimento profissional."
        else:
            with st.spinner("ORIENTA está pensando..."):
                resposta = perguntar(pergunta)

        st.write(resposta)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
