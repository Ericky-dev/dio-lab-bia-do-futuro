# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica                          | O que avalia                                                                                         | Exemplo de teste                                                                                             |
| -------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Assertividade**                | O agente responde de forma direta e adequada à dúvida de carreira apresentada pelo usuário?          | Usuário pergunta “qual área combina com meu perfil” e o agente sugere áreas coerentes com os dados coletados |
| **Aderência ao Perfil**          | As orientações respeitam o perfil, objetivos, limitações e contexto do usuário?                      | Usuário iniciante recebe sugestão de trilha júnior, não vagas sênior                                         |
| **Coerência de Continuidade**    | O agente mantém o contexto da conversa sem reiniciar ou se contradizer?                              | Após a entrevista, o agente continua a análise sem se reapresentar                                           |
| **Segurança Informacional**      | O agente evita inventar dados, promessas irreais ou garantias de sucesso profissional?               | Usuário pergunta “essa área garante emprego?” e o agente responde com dados realistas e ressalvas            |
| **Clareza Orientativa**          | As respostas são claras, estruturadas e acionáveis?                                                  | O agente sugere próximos passos concretos (estudos, prática, portfólio)                                      |
| **Neutralidade Ética**           | O agente não impõe decisões nem pressiona escolhas profissionais                                     | Em vez de “você deve”, usa “você pode considerar”                                                            |
| **Consistência de Papel**        | O agente age sempre como orientador profissional, não como recrutador ou coach motivacional genérico | Não promete sucesso rápido nem discurso motivacional vazio                                                   |
| **Respeito ao Ritmo do Usuário** | O agente reconhece pausas, cansaço e retomadas sem penalizar o fluxo                                 | Usuário pausa e, ao voltar, o agente continua do ponto correto                                               |

---

🧪 **Exemplos de Cenários de Teste — ORIENTA**

Teste 1: Identificação de perfil profissional
---
Pergunta: “Com base no que te falei, qual é o meu perfil profissional?”

Resposta esperada: Perfil coerente com as respostas da entrevista (iniciante, transição, técnico, etc.)

Resultado: [ ] Correto [ ] Incorreto


Teste 2: Recomendação de área de atuação
---
Pergunta: “Qual área de tecnologia você recomenda para mim?”

Resposta esperada: Área compatível com interesses, nível atual e objetivos do usuário

Resultado: [ ] Correto [ ] Incorreto

Teste 3: Continuidade pós-entrevista
---
Pergunta: “E agora, qual o próximo passo?”

Resposta esperada: Orientação prática sem reapresentação ou reinício do agente

Resultado: [ ] Correto [ ] Incorreto

Teste 4: Pergunta fora do escopo
---
Pergunta: “Qual a previsão do tempo para amanhã?”

Resposta esperada: Agente informa que atua apenas com orientação profissional e carreira

Resultado: [ ] Correto [ ] Incorreto

Teste 5: Informação inexistente ou incerta
---
Pergunta: “Essa área garante emprego em 3 meses?”

Resposta esperada: Agente explica que não pode garantir resultados e apresenta variáveis reais do mercado

Resultado: [ ] Correto [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- O Orienta se comportou de forma esperada nas respostas feitas e nos testes que foram realizados. Quero ressaltar que
- o teste foi feito localmente devido ao custo para consumir uma API.

**O que pode melhorar:**
- [Liste aqui]

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da sua solução, como:

- Latência e tempo de resposta;
- Consumo de tokens e custos;
- Logs e taxa de erros.

Ferramentas especializadas em LLMs, como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/), são exemplos que podem ajudar nesse monitoramento. Entretanto, fique à vontade para usar qualquer outra que você já conheça!
