import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para obter os dados do tempo de uma cidade
def obter_dados_tempo(cidade):
    # Constrói a URL da cidade
    url = f'https://www.tempo.com/{cidade}.htm'

    # Faz a requisição HTTP para obter o conteúdo da página
    response = requests.get(url)

    # Faz o parsing do conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Obtém o nome da cidade
    nome_cidade_element = soup.find(class_='breadcrumb').find_all('li')[-1]
    nome_cidade = nome_cidade_element.get_text().strip()

    # Lista de classes para buscar
    classes_busca = ['dos-semanas nuevo-4', 'dos-semanas nuevo-5']

    # Encontra o elemento que contém os dias da semana
    dias_semana_element = soup.find(class_=classes_busca)

    if dias_semana_element:
        # Encontra todos os elementos de cada dia da semana
        dias_semana = dias_semana_element.find_all('li')

        # Lista para armazenar os dados
        dados = []

        # Itera sobre cada elemento <li> para obter as informações desejadas
        for dia in dias_semana:
            # Obtém a data do dia
            data_element = dia.find(class_='cuando')
            if data_element:
                data = ''.join(filter(str.isdigit, data_element.get_text()))
            else:
                data = "Data não disponível"

            # Obtém as informações de temperatura máxima e mínima
            temperatura_maxima = dia.find(class_='maxima').get_text().strip()
            temperatura_minima = dia.find(class_='minima').get_text().strip()

            # Verifica se o elemento de chuva existe
            chuva_element = dia.find(class_='changeUnitR')
            if chuva_element:
                chuva = chuva_element.get_text().strip()
            else:
                chuva = '0 mm'

            # Formata os dados
            dados.append({
                'Data': data,
                'Temperatura Máxima': temperatura_maxima,
                'Temperatura Mínima': temperatura_minima,
                'Chuva': chuva
            })

            # Verifica se já foram obtidos 7 dias
            if len(dados) == 7:
                break
    else:
        dados = []

    # Retorna os dados da cidade
    return nome_cidade, dados


# Lista de cidades
cidades = ['imperatriz', 'codo','sao-luiz']

# Solicita ao usuário o caminho da pasta de destino
destino = 'G:\Atila_Rocha\Programacao\Github\webscraping-tempo.com\src\db'

# Itera sobre as cidades e obtém os dados do tempo
for cidade in cidades:
    # Obtém os dados da cidade
    nome_cidade, dados = obter_dados_tempo(cidade)

    # Constrói o caminho completo do arquivo
    nome_arquivo = f"{nome_cidade.replace(' ', '_')}_Tempo.xlsx"
    caminho_completo = f"{destino}/{nome_arquivo}"

    # Cria um DataFrame a partir dos dados
    df = pd.DataFrame(dados)

    # Salva o DataFrame em um arquivo Excel no caminho especificado
    df.to_excel(caminho_completo, index=False)
    print(f'Dados da cidade {cidade} salvos com sucesso no arquivo: {caminho_completo}')