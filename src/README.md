# Passo a Passo de Execução do Agente ORIENTA

 1. Instalar Ollama (ollama.com)
 2. Baixar um modelo leve(aqui utilizei o 'gemma:2b'
 3. Testar se funciona (ollama run gemma:2b)

## Código Completo
Todo Código Completo está no arquivo app.py 

## Como executar

# Instalar dependências
pip install -r requirements.txt

# Garantir que o ollama está funcionando
ollama serve

# Executar a aplicação
streamlit run app.py

