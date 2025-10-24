# Pokémon Analytics - ETL e Dashboard Interativo

Projeto completo de **ETL (Extract, Transform, Load)** que consome uma API REST protegida por autenticação JWT, processa dados de Pokémons e batalhas, e exibe análises interativas em um dashboard Streamlit com **tema Pokédex clássico**.

## 📋 Sobre o Projeto

Este projeto demonstra:
- ✅ **Consumo de API REST** com autenticação JWT
- ✅ **Processo ETL completo** com tratamento de erros específico
- ✅ **Manipulação e análise de dados** com Pandas
- ✅ **Dashboard interativo** com Streamlit e Plotly
- ✅ **Código limpo e refatorado** seguindo boas práticas
- ✅ **Simulador de batalhas** Pokémon interativo
- ✅ **Análise estratégica** para composição de equipes
- ✅ **Tema visual personalizado** inspirado na Pokédex clássica

---

## 🚀 Instalação e Configuração

### **Requisitos**
- Python 3.8 ou superior
- Conexão com internet (para acessar a API)
- Git (para clonar o repositório)

### **Passo 1: Clonar o Repositório**

    git clone https://github.com/SantiOsa/Teste-t-cnico-Kaizen-Santiago-.git
    cd Teste-t-cnico-Kaizen-Santiago-

### **Passo 2: Criar Ambiente Virtual**

IMPORTANTE: Use um ambiente virtual para isolar as dependências do projeto.

No Windows (PowerShell):

    py -m venv .venv

NOTA: Se o comando `python` não funcionar no Windows, use `py` em vez de `python`. Isso acontece quando o Windows redireciona `python` para a Microsoft Store.

No Linux/Mac:

    python3 -m venv .venv

### **Passo 3: Ativar o Ambiente Virtual**

No Windows (PowerShell):

    .\.venv\Scripts\Activate.ps1

NOTA: Se aparecer erro de permissão, execute uma vez:

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

No Linux/Mac:

    source .venv/bin/activate

Após ativar, você verá (.venv) no início da linha do terminal.

### **Passo 4: Instalar as Dependências**

Com o ambiente virtual ativo, execute:

    pip install -r requirements.txt

Isso instalará apenas as bibliotecas essenciais:
- requests - Consumo de API REST
- pandas - Manipulação e análise de dados
- streamlit - Framework para dashboard interativo
- plotly - Visualizações e gráficos interativos

---

## 🎮 Como Executar o Projeto

IMPORTANTE: Sempre ative o ambiente virtual antes de executar os scripts!

Windows:

    .\.venv\Scripts\Activate.ps1

Linux/Mac:

    source .venv/bin/activate

### **Passo 1: Executar o ETL**

O ETL extrai os dados da API, transforma e salva em arquivos CSV na pasta data/.

Com o ambiente virtual ativo, execute no terminal:

    python etl.py

**O que o ETL faz:**
1. 🔐 **Autenticação JWT** - Conecta na API com credenciais seguras
2. 📡 **Extração de Dados** - Busca lista de Pokémons e seus atributos detalhados
3. 📡 **Extração de Batalhas** - Busca histórico de combates
4. 🔄 **Transformação** - Limpa e processa os dados brutos
5. 📊 **Cálculo de Métricas** - Estatísticas e análises automáticas
6. 💾 **Carregamento** - Salva tudo na pasta `data/` (CSV e JSON)

**Saída esperada:**

    ==================================================
    ETL - POKEMON DATA PIPELINE
    ==================================================
    Autenticando na API...
    Autenticacao realizada com sucesso!
    
    Extraindo dados da API...
      Buscando lista: /pokemon
      10 pokemons encontrados
      Buscando atributos detalhados...
        Processados: 10/10
      Total: 10 pokemons com atributos completos
      Buscando: /combats
      10 combates obtidos
    
    Transformando dados de Pokemons...
      10 Pokemons processados
      Colunas: id, name, hp, attack, defense, sp_attack, sp_defense, speed, generation, legendary, types
    
    Transformando dados de Batalhas...
      Campos do schema Combat encontrados: first_pokemon, second_pokemon, winner
      10 batalhas processadas
    
    Calculando metricas...
      16 metricas calculadas
    
    Salvando dados...
      Pokemons salvos
      Batalhas salvas
      Metricas salvas
    
    ETL concluido com sucesso!
    ==================================================

---

### **Passo 2: Executar o Dashboard Streamlit**

Após executar o ETL com sucesso, inicie o dashboard:

    streamlit run streamlit_app.py

O Streamlit abrirá automaticamente no navegador (geralmente em http://localhost:8501 ou http://localhost:8502).

---

## 📂 Estrutura de Arquivos Gerados

Após executar o ETL, será criada automaticamente a pasta data/ contendo:

    data/
    ├── pokemons.csv      # Dados completos dos Pokémon
    ├── battles.csv       # Histórico de batalhas
    └── metricas.json     # Estatísticas e métricas calculadas

---

## 🔄 Uso Diário

Após a instalação inicial, toda vez que abrir um novo terminal:

1. Ative o ambiente virtual

Windows:

    .\.venv\Scripts\Activate.ps1

Linux/Mac:

    source .venv/bin/activate

2. (Opcional) Atualize os dados executando o ETL novamente

    python etl.py

3. Inicie o dashboard

    streamlit run streamlit_app.py

---

## 📊 Insights do Dashboard

O dashboard apresenta **5 insights principais** com análises interativas:

### **1️⃣ Todos os Pokémon e seus Status**
- 📋 Tabela completa com todos os Pokémon
- 🔄 Ordenação dinâmica por qualquer atributo (crescente/decrescente)
- 📊 Métricas resumidas: Total de Pokémon, Lendários, Gerações e Poder Médio
- 🎨 Nomes das colunas em português

### **2️⃣ Qual o tipo com a maior média de ataque?**
- 📊 Ranking completo de tipos por média de ataque
- 📈 Gráfico de barras interativo com escala Viridis
- 📋 Tabela com tipo, média de ataque, quantidade e lista de Pokémon
- 🏆 Destaque para o tipo com maior média

### **3️⃣ Índice de Poder - Top 10 Pokémon**
- 👑 Ranking dos 10 Pokémon mais poderosos
- 📊 Tabela detalhada com todos os atributos em português
- 📈 Gráfico horizontal de barras do poder total
- ℹ️ Quantidade de lendários entre os top 10

### **4️⃣ Simulador de Batalha Pokémon**
- 🎮 Seleção interativa de 2 Pokémon para batalhar
- 📊 Gráficos de atributos individuais (azul vs vermelho)
- ⚔️ Cálculo automático do vencedor baseado em poder total
- 📈 Diferença percentual de poder entre os lutadores
- 📋 Comparação detalhada atributo por atributo

### **5️⃣ Composição da Equipe Ideal**
- 🎯 **3 estratégias de montagem:**
  - **Poder Total (Força Bruta):** Seleciona os mais fortes
  - **Balanceamento de Atributos:** Prioriza equilíbrio + poder
  - **Diversidade de Tipos:** Maximiza cobertura de tipos
- ⚙️ Slider para escolher tamanho da equipe (3-6 Pokémon)
- 🔘 Opção de incluir/excluir Lendários
- 📊 Análise completa da equipe:
  - Poder Total e Poder Médio
  - Quantidade de Lendários
  - Tipos Únicos na equipe
- 📈 Gráfico de perfil de atributos da equipe

---

## 📁 Estrutura do Projeto

```
teste_Tecnico-Santiago/
│
├── etl.py                  # Script ETL completo
├── streamlit_app.py        # Dashboard interativo
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
│
└── data/                  # Dados processados (criado após ETL)
    ├── pokemons.csv       # Dados dos Pokémons
    ├── battles.csv        # Dados das batalhas
    └── metricas.json      # Métricas calculadas
```

---

## 🎨 Tema Visual - Pokédex Clássica

O dashboard utiliza um tema personalizado inspirado na Pokédex clássica:

- CORES PRINCIPAIS:
  - Fundo: #383838 (cinza escuro)
  - Sidebar: #5a0000 (vermelho Pokédex)
  - Títulos: #FFCC00 (amarelo) com borda #356ABD (azul)
  - Header: #000000 (preto)

- GRÁFICOS:
  - Fundo: #323232 (cinza escuro)
  - Escala de cores: Viridis
  - Fonte: Branca para contraste

- BOTÕES:
  - Gradiente vermelho Pokédex
  - Bordas estilizadas
  - Efeito hover

## 🔧 Detalhes Técnicos

### **API Utilizada**
- Base URL: http://ec2-52-67-119-247.sa-east-1.compute.amazonaws.com:8000
- Autenticação: JWT Bearer Token
- Credenciais:
  - Username: kaizen-poke
  - Password: 4w9f@D39fkkO
- Endpoints principais:
  - POST /login - Autenticação JWT
  - GET /pokemon - Lista de Pokémon
  - GET /pokemon/{id} - Detalhes de um Pokémon específico
  - GET /combats - Lista de combates

### **Arquitetura do ETL (Refatorado)**

#### **Extração (Extract)** - 4 funções especializadas

    # 1. Autenticação
    token = autenticar_api()
    
    # 2. Extração modular
    lista_pokemons = extrair_lista_pokemons(headers)
    pokemon_detalhado = extrair_detalhes_pokemon(pokemon_id, headers)
    batalhas = extrair_batalhas(headers)
    
    # 3. Orquestração
    dados = extrair_dados(token)  # Coordena todas as extrações

#### **Transformação (Transform)**

    # 4. Processamento de Pokémon
    df_pokemons = transformar_pokemons(dados['pokemons'])
    # - Remove valores nulos de id/name
    # - Converte legendary para boolean
    # - Mantém schema: id, name, hp, attack, defense, sp_attack, 
    #   sp_defense, speed, generation, legendary, types
    
    # 5. Processamento de Batalhas
    df_battles = transformar_batalhas(dados['battles'], df_pokemons)
    # - Valida campos essenciais: first_pokemon, second_pokemon, winner
    # - Remove valores nulos
    
    # 6. Cálculo de Métricas
    metricas = calcular_metricas(df_pokemons, df_battles)
    # - Total de pokémons e batalhas
    # - Médias e máximos de atributos
    # - Percentual de lendários

#### **Carregamento (Load)**

    # 7. Salvamento
    carregar_dados(df_pokemons, df_battles, metricas)
    # - data/pokemons.csv
    # - data/battles.csv
    # - data/metricas.json

### **Tratamento de Erros**
- Exceções específicas (requests.RequestException)
- Validação de resposta da API
- Logs detalhados de cada etapa
- Graceful degradation (continua com dados parciais)

## 🐛 Solução de Problemas

### **Erro: "Python não foi encontrado" no Windows**
Se aparecer a mensagem que redireciona para Microsoft Store:
1. Use `py` em vez de `python` para criar o ambiente virtual:
   ```
   py -m venv .venv
   ```
2. **OU** desabilite o alias do Windows:
   - Abra **Configurações** → **Aplicativos** → **Aplicativos e recursos**
   - Clique em **Aliases de execução de aplicativo**
   - Desative os aliases para `python.exe` e `python3.exe`

### **Erro: Módulo não encontrado**

    pip install -r requirements.txt

### **Erro: Não foi possível conectar à API**
1. Verifique sua conexão com a internet
2. Confirme se a API está acessível
3. Verifique as credenciais no arquivo etl.py

### **Erro: Dados não encontrados no dashboard**
1. Execute primeiro o ETL: python etl.py
2. Verifique se a pasta data/ foi criada
3. Confirme se os arquivos CSV estão presentes

### **Dashboard não abre automaticamente**
Acesse manualmente: http://localhost:8501 ou http://localhost:8502

### **🔧 Funções Auxiliares Criadas**

    # Constantes Globais
    RENAME_COLUNAS = {...}      # Tradução de colunas
    ATRIBUTOS_BATALHA = [...]   # Lista de atributos
    BACKGROUND_CHART = '#323232' # Cor padrão dos gráficos
    
    # Funções Auxiliares
    extrair_tipos(tipos_str)           # Parse de tipos
    aplicar_layout_padrao(fig)          # Layout de gráficos
    selecionar_colunas_display(df)     # Seleção inteligente de colunas

## 📚 Bibliotecas Utilizadas

- requests - Consumo de API REST com JWT
- pandas - Manipulação e análise de dados
- streamlit - Framework para dashboard interativo
- plotly - Visualizações e gráficos interativos

## 📝 Notas Importantes

- O ETL deve ser executado ANTES do dashboard
- Os dados são salvos na pasta data/ em formato CSV e JSON
- O dashboard usa cache para melhor performance
- O cálculo de total_stats é feito automaticamente ao carregar os dados
- Todos os textos estão em português com acentuação correta
- O tema visual é aplicado via CSS customizado

## 🎓 Conceitos Demonstrados

### **ETL (Extract, Transform, Load)**
- ✅ Extração de dados via API REST
- ✅ Autenticação JWT
- ✅ Transformação e limpeza de dados
- ✅ Validação de schemas
- ✅ Cálculo de métricas derivadas
- ✅ Persistência em arquivos

### **Análise de Dados**
- ✅ Manipulação com Pandas
- ✅ Agregações e estatísticas
- ✅ Análise exploratória
- ✅ Cálculo de métricas customizadas

### **Visualização**
- ✅ Dashboard interativo com Streamlit
- ✅ Gráficos com Plotly
- ✅ Tema visual personalizado
- ✅ Responsividade e UX