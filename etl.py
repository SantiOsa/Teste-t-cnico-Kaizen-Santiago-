import requests
import pandas as pd
import json
import os

# Configuracoes da API
BASE_URL = "http://ec2-52-67-119-247.sa-east-1.compute.amazonaws.com:8000"
USERNAME = "kaizen-poke"
PASSWORD = "4w9f@D39fkkO"


def autenticar_api():
    """
    Realiza autenticacao JWT na API
    Endpoint: POST /login
    Retorna: token JWT ou None em caso de erro
    """
    print("Autenticando na API...")
    
    login_url = f"{BASE_URL}/login"
    login_data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(login_url, json=login_data, timeout=30)
        response.raise_for_status()
        token = response.json()["access_token"]
        print("Autenticacao realizada com sucesso!")
        return token
    except requests.RequestException as e:
        print(f"Erro na autenticacao: {e}")
        return None
    except KeyError:
        print("Erro: Token nao encontrado na resposta da API")
        return None


def extrair_lista_pokemons(headers):
    """
    Extrai lista de IDs/nomes de Pokemons da API
    Endpoint: GET /pokemon
    Retorna: lista de IDs/nomes
    """
    try:
        url = f"{BASE_URL}/pokemon"
        print(f"  Buscando lista: /pokemon")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        resposta_api = response.json()
        
        # Extrair lista de pokemons da resposta paginada
        if isinstance(resposta_api, dict) and 'pokemons' in resposta_api:
            lista_pokemons = resposta_api['pokemons']
        elif isinstance(resposta_api, list):
            lista_pokemons = resposta_api
        else:
            lista_pokemons = []
        
        print(f"  {len(lista_pokemons)} pokemons encontrados")
        return lista_pokemons
    
    except requests.RequestException as e:
        print(f"  Erro ao buscar lista de pokemons: {e}")
        return []


def extrair_detalhes_pokemon(pokemon_id, headers):
    """
    Busca atributos detalhados de um Pokemon específico
    Endpoint: GET /pokemon/{id}
    Retorna: dict com PokemonAttributes
    """
    try:
        url_detalhes = f"{BASE_URL}/pokemon/{pokemon_id}"
        response = requests.get(url_detalhes, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"    Erro ao buscar pokemon {pokemon_id}: {str(e)[:50]}")
        return None


def extrair_batalhas(headers):
    """
    Extrai dados de combates/batalhas da API
    Endpoint: GET /combats
    Retorna: lista de combates
    """
    try:
        url = f"{BASE_URL}/combats"
        print(f"  Buscando: /combats")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        resposta_combats = response.json()
        
        # Extrair lista de combates da resposta paginada
        if isinstance(resposta_combats, dict) and 'combats' in resposta_combats:
            lista_combates = resposta_combats['combats']
        elif isinstance(resposta_combats, list):
            lista_combates = resposta_combats
        else:
            lista_combates = []
        
        print(f"  {len(lista_combates)} combates obtidos")
        return lista_combates
    
    except requests.RequestException as e:
        print(f"  Erro ao buscar combates: {e}")
        return []


def extrair_dados(token):
    """
    Extrai dados dos endpoints da API usando o token JWT
    Orquestra extração de pokemons e batalhas
    """
    print("\nExtraindo dados da API...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 1. Extrair lista de Pokemons
    lista_pokemons = extrair_lista_pokemons(headers)
    
    # 2. Buscar atributos detalhados de cada Pokemon
    print(f"  Buscando atributos detalhados...")
    pokemons_completos = []
    
    for idx, item in enumerate(lista_pokemons, 1):
        # Identificar o ID do pokemon
        if isinstance(item, dict):
            pokemon_id = item.get('id') or item.get('name')
        elif isinstance(item, (str, int)):
            pokemon_id = item
        else:
            continue
        
        pokemon_detalhado = extrair_detalhes_pokemon(pokemon_id, headers)
        if pokemon_detalhado:
            pokemons_completos.append(pokemon_detalhado)
        
        if idx % 10 == 0:
            print(f"    Processados: {idx}/{len(lista_pokemons)}")
    
    print(f"  Total: {len(pokemons_completos)} pokemons com atributos completos")
    
    # 3. Extrair Combates
    lista_combates = extrair_batalhas(headers)
    
    return {
        'pokemons': pokemons_completos,
        'battles': lista_combates
    }


def transformar_pokemons(pokemons_raw):
    """
    Transforma os dados brutos de Pokemons em um DataFrame tratado
    Schema: PokemonAttributes (id, name, hp, attack, defense, sp_attack, sp_defense, speed, generation, legendary, types)
    """
    print("\nTransformando dados de Pokemons...")
    
    df_pokemons = pd.DataFrame(pokemons_raw)
    
    if df_pokemons.empty:
        print("  Nenhum dado encontrado")
        return df_pokemons
    
    # Limpeza de valores nulos
    if 'id' in df_pokemons.columns and 'name' in df_pokemons.columns:
        df_pokemons = df_pokemons.dropna(subset=['id', 'name'])
    
    # Converter tipos de dados
    if 'legendary' in df_pokemons.columns:
        df_pokemons['legendary'] = df_pokemons['legendary'].astype(bool)
    
    print(f"  {len(df_pokemons)} Pokemons processados")
    print(f"  Colunas: {', '.join(df_pokemons.columns.tolist())}")
    
    return df_pokemons


def transformar_batalhas(battles_raw, df_pokemons):
    """
    Transforma os dados brutos de batalhas em um DataFrame tratado
    Schema: Combat (first_pokemon, second_pokemon, winner)
    """
    print("\nTransformando dados de Batalhas...")
    
    df_battles = pd.DataFrame(battles_raw)
    
    if df_battles.empty:
        print("  Nenhum dado encontrado")
        return df_battles
    
    # Verificacao de campos essenciais do schema Combat
    campos_essenciais = ['first_pokemon', 'second_pokemon', 'winner']
    campos_faltantes = [campo for campo in campos_essenciais if campo not in df_battles.columns]
    
    if campos_faltantes:
        print(f"  Campos faltantes: {campos_faltantes}")
    else:
        print(f"  Campos do schema Combat encontrados: first_pokemon, second_pokemon, winner")
    
    # Limpeza de valores nulos
    df_battles = df_battles.dropna()
    
    print(f"  {len(df_battles)} batalhas processadas")
    print(f"  Colunas: {', '.join(df_battles.columns.tolist())}")
    
    return df_battles


def calcular_metricas(df_pokemons, df_battles):
    """
    Calcula metricas e estatisticas relevantes para analise
    Utiliza atributos do PokemonAttributes: hp, attack, defense, sp_attack, sp_defense, speed, legendary
    """
    print("\nCalculando metricas...")
    
    metricas = {}
    
    if not df_pokemons.empty:
        metricas['total_pokemons'] = len(df_pokemons)
        
        # Metricas de atributos se existirem
        atributos_numericos = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        for atributo in atributos_numericos:
            if atributo in df_pokemons.columns:
                metricas[f'media_{atributo}'] = float(df_pokemons[atributo].mean())
                metricas[f'max_{atributo}'] = int(df_pokemons[atributo].max())
        
        # Contagem de lendarios
        if 'legendary' in df_pokemons.columns:
            metricas['total_lendarios'] = int(df_pokemons['legendary'].sum())
            metricas['percentual_lendarios'] = float((df_pokemons['legendary'].sum() / len(df_pokemons)) * 100)
    
    if not df_battles.empty:
        metricas['total_batalhas'] = len(df_battles)
    
    print(f"  {len(metricas)} metricas calculadas")
    return metricas


def carregar_dados(df_pokemons, df_battles, metricas):
    """
    Carrega (salva) os dados processados em arquivos CSV
    """
    print("\nSalvando dados...")
    
    os.makedirs('data', exist_ok=True)
    
    if not df_pokemons.empty:
        df_pokemons.to_csv('data/pokemons.csv', index=False)
        print("  Pokemons salvos")
    
    if not df_battles.empty:
        df_battles.to_csv('data/battles.csv', index=False)
        print("  Batalhas salvas")
    
    if metricas:
        with open('data/metricas.json', 'w') as f:
            json.dump(metricas, f, indent=4)
        print("  Metricas salvas")
    
    print("\nETL concluido com sucesso!")


def executar_etl():
    """
    Função principal que executa todo o processo ETL
    """
    print("=" * 50)
    print("ETL - POKEMON DATA PIPELINE")
    print("=" * 50)
    
    # 1. Extração
    token = autenticar_api()
    if not token:
        print("Erro: Nao foi possivel autenticar")
        return
    
    dados_brutos = extrair_dados(token)
    
    # 2. Transformação
    df_pokemons = transformar_pokemons(dados_brutos.get('pokemons', []))
    df_battles = transformar_batalhas(dados_brutos.get('battles', []), df_pokemons)
    metricas = calcular_metricas(df_pokemons, df_battles)
    
    # 3. Carregamento
    carregar_dados(df_pokemons, df_battles, metricas)
    
    print("=" * 50)


if __name__ == "__main__":
    executar_etl()
