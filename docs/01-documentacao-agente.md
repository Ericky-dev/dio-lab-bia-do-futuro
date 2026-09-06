# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema seu agente resolve?

Muitas pessoas não sabem qual caminho profissional seguir e não têm acesso a orientação de carreira personalizada, clara e acessível.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente atua de forma proativa conduzindo o usuário por um diagnóstico guiado, adaptando perguntas, antecipando dúvidas e oferecendo planos de ação personalizados, acompanhando a evolução ao longo do tempo.

### Público-Alvo
> Quem vai usar esse agente?

- Estudantes (ensino médio / técnico)
- Pessoas em transição de carreira
- Profissionais iniciantes
- Pessoas em busca de recolocação no mercado de trabalho.

---

## Persona e Tom de Voz

### Nome do Agente
Orienta

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

- Empático
- Orientador
- Analítico
- Comunicativo
- Ético

### Tom de Comunicação
> Formal, informal, técnico, acessível?

**Acessível e objetivo** Atende pessoas de diferentes níveis de escolaridade,
facilita o entendimento de quem está confuso ou inseguro,
Reduz barreiras de linguagem técnica e
mantém uma postura humana, acolhedora e confiável.

### Exemplos de Linguagem
- **Saudação:** "Olá! seu agente de orientação profissional e carreira. Como posso lhe ajudar hoje?"
- **Confirmação:** "Entendi! Deixe-me analisar seu perfil e histórico para estruturar isso para você."
- **Erro/Limitação:** "Não tenho essa informação no momento, pois meu foco é estritamente orientação profissional e de carreira. Como posso ajudar dentro dessa área?"

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Usuário] -->|Mensagem| B["Streamlit (Interface)"]
    B --> |Pipeline Python | C[Ollama - Local LLM] 
    C <-->|Contexto Dinâmico| D["Base de Conhecimento (data/*.json e *.csv)"]
    C --> E[Módulo de Validação e Trava de Escopo]
    E -->|Resposta Validada| F[Usuário]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | [Streamlit](https://streamlit.io/) |
| LLM | ollama (local) |
| Base de Conhecimento | JSON/CSV mockados na pasta `data` |
|Linguagem de Backend  | Python 3.x


---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

[x] Restrição estrita ao contexto fornecido
[x] Conversa guiada por etapas
[x] Diagnóstico progressivo do perfil
[x] Mapeamento dinâmico de competências
[x] Recomendações acionáveis por etapas
[x] Isolamento de dados e bloqueio de prompt injection
[x] Registro contínuo em históricos
[x] Verificação e bloqueio de dados sensíveis

### Limitações Declaradas
> O que o agente NÃO faz?

- O agente não escolhe a carreira
- Não substitui um orientador humano
- Não coleta dados sensíveis 
- Não atua fora do escopo de carreira
- Não força escolhas ou caminhos
- Não fornece aconselhamento legal 
- Não faz diagnósticos psicológicos
