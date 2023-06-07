import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para transformar str2intfloat
def str2intfloat(value):
    if "°" in value:
        value = value.replace("°", "")
        return int(value)
    elif " mm" in value:
        value = value.replace(" mm", "")
        return float(value)
    else:
        return None
    

# Criando Dataframe
def criar_dataframe(nome_cidade, dados):
    try:
        # Criar DataFrame a partir dos dados raspados
        df = pd.DataFrame(dados)

        # Converter as colunas de temperatura e chuva para valores numéricos
        df['Temperatura Máxima'] = df['Temperatura Máxima'].apply(str2intfloat)
        df['Temperatura Mínima'] = df['Temperatura Mínima'].apply(str2intfloat)
        df['Chuva'] = df['Chuva'].apply(str2intfloat)

        # Calcular a maior temperatura, a menor temperatura e a média da chuva
        maior_temp = df['Temperatura Máxima'].max()
        menor_temp = df['Temperatura Mínima'].min()
        media_chuva = df['Chuva'].mean()
        
        # Arredondar a média das chuvas para duas casas decimais
        media_chuva = round(media_chuva, 2)

        # Adicionar as colunas de Maior Temperatura, Menor Temperatura e Média das Chuvas
        df.loc[0,'Maior Temperatura'] = maior_temp
        df.loc[0,'Menor Temperatura'] = menor_temp
        df.loc[0,'Média das Chuvas'] = media_chuva

        # Retornar o DataFrame
        return df
    except:
        print("Erro ao obter os dados do tempo da cidade.")
        return None


# Função para obter os dados do tempo de uma cidade
def raspagem(cidade):
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
    classes_busca = ['dos-semanas noche-nuevo']

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
                'Chuva': chuva,
            })

            # Verifica se já foram obtidos 7 dias
            if len(dados) == 7:
                break
    else:
        dados = []

    # Cria o DataFrame com os dados
    df = criar_dataframe(nome_cidade, dados)
    
    # Retorna os dados da cidade
    return nome_cidade, df
