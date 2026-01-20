# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no ORIENTA |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Registrar e contextualizar interações anteriores com o usuário |
| `perfil_usuario.json` | JSON | Compreender o perfil, interesses e contexto do usuário |
| `metas_usuario.json` | JSON | Definir e acompanhar objetivos de carreira e estudo |
| `preferencias_usuario.csv` | CSV | Adaptar comunicação e sugestões ao estilo do usuário |
| `habilidades_usuario.json` | JSON | Mapear competências técnicas e comportamentais do usuário | 
| `feedback_usuario.csv` | CSV | Avaliar qualidade do atendimento e melhorar o ORIENTA |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Sim.

Os dados mockados foram modificados e expandidos para atender ao escopo do projeto do agente inteligente de orientação profissional e de carreira (ORIENTA).

Foram adicionados novos arquivos na pasta data, incluindo perfil_usuario, historico_atendimentos, metas_usuario, preferencias_usuario, progresso_usuario, habilidades_usuario e feedback_usuario.

Essas informações permitem que o agente compreenda melhor o perfil do usuário, acompanhe sua evolução e ofereça orientações mais precisas e personalizadas.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

O agente ORIENTA acessa sua base de conhecimento em Python por meio da leitura de arquivos JSON e CSV armazenados na pasta data/, carregando essas informações em memória para personalizar e contextualizar as orientações oferecidas ao usuário.

```python
import pandas as pd
import json

# JSONs
def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

perfil_usuario = carregar_json("data/perfil_usuario.json")
metas_usuario = carregar_json("data/metas_usuario.json")
preferencias_usuario = carregar_json("data/preferencias_usuario.json")


# CSVs
import csv

def carregar_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))

historico_atendimentos = carregar_csv("data/historico_atendimentos.csv")
feedbacks = carregar_csv("data/feedback_usuario.csv")


```


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?
> 
Como abordagem inicial, os dados podem ser incorporados diretamente ao prompt para fornecer ao agente um contexto completo da situação do usuário. Já em arquiteturas mais avançadas, essas informações devem ser obtidas de forma dinâmica, permitindo maior flexibilidade, manutenção e evolução do sistema.

``` text

Perfil do Usuario (data/perfil_do_usuario.json)
{
  "nome": "João Silva",
  "idade": 22,
  "escolaridade": "Ensino Médio Completo",
  "situacao_profissional": "Estudante",
  "area_interesse_principal": "Tecnologia",
  "interesses": [
    "Programação",
    "Lógica",
    "Resolução de problemas"
  ],
  "habilidades": [
    "Raciocínio lógico",
    "Organização",
    "Aprendizado rápido"
  ],
  "experiencia_profissional": "Nenhuma",
  "objetivo_profissional": "Ingressar na área de tecnologia",
  "nivel_clareza_carreira": "baixo",
  "disponibilidade_estudo_horas_dia": 2,
  "preferencia_trabalho": {
    "ambiente": "remoto",
    "estilo": "analitico",
    "interacao_pessoas": "moderada"
  },
  "carreiras_sugeridas": [
    "Desenvolvedor Backend",
    "Analista de Sistemas",
    "Analista de Dados",
    "Front-End"
  ],
  "plano_acao": [
    {
      "etapa": "Introdução à lógica de programação",
      "duracao_estimada_meses": 2,
      "prioridade": "alta"
    },
    {
      "etapa": "Aprender linguagem Java",
      "duracao_estimada_meses": 4,
      "prioridade": "alta"
    },
    {
      "etapa": "Construir projetos práticos",
      "duracao_estimada_meses": 3,
      "prioridade": "media"
    }
  ],
  "aceita_transicao_carreira": true,
  "observacoes_agente": "Usuário demonstra afinidade com tecnologia e perfil analítico, indicado para áreas técnicas de desenvolvimento."
}


Metas do Usuario (data/metas_usuario.json)
{
  "usuario_id": "usr_001",
  "metas": [
    {
      "id": "meta_01",
      "descricao": "Definir area profissional principal",
      "categoria": "carreira",
      "prazo": "2025-12",
      "status": "em_andamento",
      "prioridade": "alta"
    },
    {
      "id": "meta_02",
      "descricao": "Concluir curso introdutorio de programacao",
      "categoria": "educacao",
      "prazo": "2026-03",
      "status": "nao_iniciada",
      "prioridade": "media"
    }
  ]
}


Histórico de Atendimento (data/historico_atendimento.csv)
data,canal,tema,resumo,resolvido
2025-09-15,chat,Orientacao de carreira,Usuario relatou indecisao profissional e iniciou diagnostico guiado,sim
2025-09-22,chat,Perfil profissional,Agente identificou perfil analitico com interesse em tecnologia,sim
2025-10-01,chat,Sugestao de carreiras,Foram sugeridas areas de desenvolvimento e analise de dados,sim
2025-10-12,chat,Plano de estudo,Criacao de plano de estudos com foco em logica e programacao,sim
2025-10-25,chat,Acompanhamento de progresso,Plano ajustado conforme evolucao informada pelo usuario,sim


Preferências do Usuario (data/preferencias_usuario.json)
{
  "usuario_id": "usr_001",
  "estilo_aprendizado": "pratico",
  "formatos_preferidos": ["texto", "exercicios"],
  "horarios_preferidos": ["noite"],
  "frequencia_interacao": "semanal",
  "nivel_detalhamento": "medio"
}


Progresso do Usuario (data/progresso_usuario.json)
{
  "usuario_id": "usr_001",
  "progresso_geral": "moderado",
  "ultima_atualizacao": "2025-10-25",
  "registros": [
    {
      "data": "2025-10-01",
      "descricao": "Usuario demonstrou maior clareza sobre interesse em tecnologia",
      "impacto": "positivo"
    },
    {
      "data": "2025-10-20",
      "descricao": "Dificuldade em manter rotina de estudos",
      "impacto": "negativo"
    }
  ]
}


feedback Usuario (data/feedback_usuario.csv)
data,canal,avaliacao,comentario
2025-10-05,chat,5,Agente foi claro e ajudou a organizar minhas ideias
2025-10-18,chat,4,Bom acompanhamento mas poderia sugerir mais exemplos praticos
2025-10-25,chat,5,Senti evolucao no meu planejamento profissional

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.



```text
perfil_usuario = {
    "nome": "Joao",
    "area_interesse": "Tecnologia",
    "nivel_experiencia": "iniciante"
}

metas_usuario = {
    "metas": [
        {
            "descricao": "Concluir curso introdutorio de programacao",
            "prazo": "2026-03",
            "status": "em_andamento"
        }
    ]
}

preferencias_usuario = {
    "estilo_aprendizado": "pratico",
    "nivel_detalhamento": "medio"
}
```

...
```
