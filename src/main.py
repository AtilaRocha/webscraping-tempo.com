import os
import pandas as pd
from extrair_tempo import raspagem

# Lista de cidades
cidades = ['imperatriz', 'codo', 'sao-luiz']

# Solicita ao usuário o caminho da pasta de destino
destino = 'G:/Atila_Rocha/Programacao/Github/webscraping-tempo.com/db'

# Itera sobre as cidades e obtém os dados do tempo
for cidade in cidades:
    try:
        # Obtém os dados da cidade
        nome_cidade, dados = raspagem(cidade)

        # Constrói o caminho completo do arquivo
        nome_arquivo = f"{nome_cidade.replace(' ', '_')}_Tempo.xlsx"
        caminho_completo = os.path.join(destino, nome_arquivo)

        # Salva o DataFrame em um arquivo Excel no caminho especificado
        dados.to_excel(caminho_completo, index=False)
        print(f'Dados da cidade {cidade} salvos com sucesso no arquivo: {nome_arquivo}')
    except Exception as e:
        print(f'Erro ao obter os dados do tempo da cidade {cidade}: {str(e)}')