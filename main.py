import pandas as pd

#---Parte 0
from pathlib import Path

CORPUS_DIR = Path("insumos_Desafio_Bootcamp_SEP26/corpus")

metadados = pd.read_csv("insumos_Desafio_Bootcamp_SEP26/metadados.csv")

"""
Função que recebe um arquivo e devolte todo 
conteudo inteiro como uma só String
"""
def ler_texto(arquivo):
    caminho = CORPUS_DIR / arquivo
    return caminho.read_text(encoding = "utf-8")

metadados["texto"] = metadados["arquivo"].apply(ler_texto)

metadados["num_palavras"] = metadados["texto"].str.split().str.len()

print("----------------------------------------------------------------------------------Parte 0")
print(metadados[["doc_id", "status", "num_palavras"]])

print(metadados["status"].value_counts())

#---Parte 1

import re

def dividir_chunks(linha):
    texto = linha["texto"]

    partes = re.split(r'(?m)^##\s+(.+)$', texto)

    chunks = []

    for i in range(1, len(partes), 2):
        nome_secao = partes[i].strip()
        texto_secao = partes[i + 1].strip()
        chunks.append({
            "doc_id":linha["doc_id"],
            "titulo":linha["titulo"],
            "secao":nome_secao,
            "status":linha["status"],
            "texto":texto_secao,
        })
    return chunks

lista_chunks = []
for _, linha in metadados.iterrows():
    lista_chunks.extend(dividir_chunks(linha))

df_chunks = pd.DataFrame(lista_chunks)

print("----------------------------------------------------------------------------------Parte 1")
print("Total de chunks:", len(df_chunks))
print(df_chunks.groupby("doc_id").size())
print(df_chunks.iloc[0].to_dict())  # exemplo completo de 1 chunk

#---Parte 2

from sklearn.feature_extraction.text import TfidfVectorizer

vetorizador = TfidfVectorizer(lowercase=True)
matriz_chunks = vetorizador.fit_transform(df_chunks["texto"])
print("------------Parte 2")
print(matriz_chunks.shape) 

#---Parte 3

from sklearn.metrics.pairwise import cosine_similarity

def buscar(pergunta, k=3, apenas_vigentes = True):
    vetor_pergunta = vetorizador.transform([pergunta])
    scores = cosine_similarity(vetor_pergunta, matriz_chunks)[0]

    resultado = df_chunks.copy()
    resultado["score"] = scores.round(2)

    if apenas_vigentes:
        resultado = resultado[resultado["status"] == "vigente"]

    resultado = resultado.sort_values("score", ascending=False).head(k)
    return resultado[["doc_id", "secao", "score"]]

print("----------------------------------------------------------------------Parte 3")
print("---------------------------------P01---------------------------------")
print(buscar("Com quantos dias de antecedência devo solicitar minhas férias?", k=3))
print("---------------------------------P02---------------------------------")
print(buscar("Quantos dias por semana posso trabalhar de forma remota?", k=3)) 
print("---------------------------------P10---------------------------------")
print(buscar("Qual é a política de estacionamento da empresa?", k=3))  

#----------------------------------------------------------------------------------Parte 4
gabarito = pd.read_csv("insumos_Desafio_Bootcamp_SEP26/perguntas_gabarito.csv")
"""print(gabarito)"""

# definição de threshold 0.28
for _, linha in gabarito.iterrows():
    top1 = buscar(linha["pergunta"], k=1)
    score = top1.iloc[0]["score"]
    doc_retornado = top1.iloc[0]["doc_id"]
    print(f"{linha['pergunta_id']}: score={score:.2f} | esperado={linha['doc_esperado']} | retornado={doc_retornado}")

THRESHOLD = 0.29

def responder(pergunta):
    top1 = buscar(pergunta, k=1).iloc[0]

    if top1["score"] < THRESHOLD:
        return {
            "PERGUNTA": pergunta,
            "RESPOSTA": "Não encontrei essa informação nas políticas vigentes. Procure a área de Pessoas e Cultura.",
            "FONTE": "nenhuma",
            "SCORE": round(top1["score"], 2),
            "STATUS": "nao_encontrado",
        }
    chunk = df_chunks[
        (df_chunks["doc_id"] == top1["doc_id"]) &
        (df_chunks["secao"] == top1["secao"])
    ].iloc[0]

    return {
        "PERGUNTA": pergunta,
        "RESPOSTA": chunk["texto"],
        "FONTE": f"{chunk['doc_id']} | {chunk['titulo']} | Seção: {chunk['secao']}",
        "SCORE": round(top1["score"], 2),
        "STATUS": "encontrado",
    }

def imprimir_resposta(r):
    print(f"PERGUNTA: {r['PERGUNTA']}")
    print(f"RESPOSTA: {r['RESPOSTA']}")
    print(f"FONTE: {r['FONTE']}")
    print(f"SCORE: {r['SCORE']}")
    print(f"STATUS: {r['STATUS']}")

print("----------------------------------------------------------------------------------Parte 4")
print("-------------------------------------------P02-------------------------------------------")
imprimir_resposta(responder("Quantos dias por semana posso trabalhar de forma remota?"))
print("-------------------------------------------P10-------------------------------------------")
imprimir_resposta(responder("Qual é a política de estacionamento da empresa?"))

#----------------------------------------------------------------------------------Parte 5
linhas_avaliacao = []

for _, linha in gabarito.iterrows():
    top1 = buscar(linha["pergunta"], k=1).iloc[0]
    r = responder(linha["pergunta"])

    doc_esperado = linha["doc_esperado"]
    doc_retornado = top1["doc_id"] if r["STATUS"] == "encontrado" else "nao_encontrado"
    acerto = (doc_retornado == doc_esperado)

    linhas_avaliacao.append({
        "pergunta_id": linha["pergunta_id"],
        "doc_esperado": doc_esperado,
        "doc_retornado_1": doc_retornado,
        "score": round(top1["score"], 2),
        "STATUS": r["STATUS"],
        "acerto": "sim" if acerto else "não",
    })

df_avaliacao = pd.DataFrame(linhas_avaliacao)
print("----------------------------------------------------------------------------------Parte 5")
print(df_avaliacao)

perguntas_com_resposta = gabarito[gabarito["doc_esperado"] != "nao_encontrado"]

hit1_total = 0
hit3_total = 0

for _, linha in perguntas_com_resposta.iterrows():
    top3 = buscar(linha["pergunta"], k=3)
    docs_top3 = top3["doc_id"].tolist()

    if docs_top3[0] == linha["doc_esperado"]:
        hit1_total += 1
    if linha["doc_esperado"] in docs_top3:
        hit3_total += 1

hit1 = hit1_total / len(perguntas_com_resposta)
hit3 = hit3_total / len(perguntas_com_resposta)

print(f"Hit@1: {hit1:.2f}")
print(f"Hit@3: {hit3:.2f}")

p10 = gabarito[gabarito["pergunta_id"] == "P10"].iloc[0]
status_p10 = responder(p10["pergunta"])["STATUS"]
print("P10 correta:", status_p10 == "nao_encontrado")