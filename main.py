import pandas as pd
from pathlib import Path

#objeto Path CONST
CORPUS_DIR = Path("insumos_Desafio_Bootcamp_SEP26/corpus")

metadados = pd.read_csv("insumos_Desafio_Bootcamp_SEP26/metadados.csv")

"""
Função que recebe um arquivo e devolte todo 
conteudo inteiro como uma só String
"""
def ler_texto(arquivo):
    caminho = CORPUS_DIR / arquivo

    return caminho.read_text(encoding = "utf-8")


#apply(ler_texto) chama a função ler_texto uma vez para cada valor da coluna arquivo.
metadados["texto"] = metadados["arquivo"].apply(ler_texto)

#.str.split() pega cada String da coluna texto e quebra em uma lista de palavras
#.str.len() conta quantos 
metadados["num_palavras"] = metadados["texto"].str.split().str.len()
print(metadados[["doc_id", "status", "num_palavras"]])

print(metadados["status"].value_counts())