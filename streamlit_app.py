import streamlit as st
import pandas as pd
import plotly.express as px
import os

# === CONSTANTES GLOBAIS ===
RENAME_COLUNAS = {
    'name': 'Nome',
    'types': 'Tipos',
    'legendary': 'Lendário',
    'generation': 'Geração',
    'hp': 'HP',
    'attack': 'Ataque',
    'defense': 'Defesa',
    'sp_attack': 'Atq Especial',
    'sp_defense': 'Def Especial',
    'speed': 'Velocidade',
    'total_stats': 'Poder Total'
}

ATRIBUTOS_BATALHA = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
BACKGROUND_CHART = '#323232'

# === FUNÇÕES AUXILIARES ===
def extrair_tipos(tipos_str):
    """
    Extrai lista de tipos de uma string formatada como "['Fire', 'Flying']"
    """
    if pd.isna(tipos_str):
        return []
    
    tipos_str = str(tipos_str)
    tipos_limpos = tipos_str.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
    return [t.strip() for t in tipos_limpos.split(',') if t.strip()]

def aplicar_layout_padrao(fig, titulo=''):
    """
    Aplica layout padrão (fundo escuro, fonte branca) aos gráficos Plotly
    """
    fig.update_layout(
        plot_bgcolor=BACKGROUND_CHART,
        paper_bgcolor=BACKGROUND_CHART,
        font_color='white',
        title=titulo if titulo else None
    )
    return fig

def selecionar_colunas_display(df, incluir_total=True):
    """
    Seleciona colunas relevantes para exibição em tabelas
    Retorna lista de colunas que existem no DataFrame
    """
    cols_display = ['name']
    
    # Adiciona metadados
    for col in ['types', 'legendary', 'generation']:
        if col in df.columns:
            cols_display.append(col)
    
    # Adiciona atributos de batalha
    for attr in ATRIBUTOS_BATALHA:
        if attr in df.columns:
            cols_display.append(attr)
    
    # Adiciona total_stats se solicitado
    if incluir_total and 'total_stats' in df.columns:
        cols_display.append('total_stats')
    
    # Retorna apenas colunas existentes
    return [c for c in cols_display if c in df.columns]

st.set_page_config(page_title="Pokemon Analytics", layout="wide")

# Tema Pokedex Classica
st.markdown("""
<style>
    /* === CORES BASE === */
    .stApp { background-color: #383838; }
    [data-testid="stSidebar"] { background-color: #5a0000 !important; }
    header[data-testid="stHeader"] { background-color: #000000 !important; }
    
    /* === SIDEBAR (texto amarelo + borda azul) === */
    [data-testid="stSidebar"] * {
        color: #FFCC00 !important;
        -webkit-text-stroke: 1px #356ABD;
        paint-order: stroke fill;
    }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-weight: bold !important;
        font-size: 1.8rem !important;
    }
    
    /* === TÍTULOS (amarelo + borda azul) === */
    h1, h2, h3 {
        color: #FFCC00 !important;
        font-weight: bold !important;
        -webkit-text-stroke: 2px #356ABD;
        paint-order: stroke fill;
    }
    
    /* === TEXTOS GERAIS === */
    p, span, div { color: #e8e8e8 !important; }
    
    /* === BOTÕES (vermelho Pokedex) === */
    .stButton > button {
        background: linear-gradient(to bottom, #cc0000 0%, #990000 100%);
        color: white;
        border: 3px solid #333;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(to bottom, #ff0000 0%, #cc0000 100%);
        border-color: #000;
    }
    
    /* === MENSAGENS === */
    .stSuccess { background-color: #d4edda; border-left: 5px solid #28a745; }
    .stInfo { background-color: #d1ecf1; border-left: 5px solid #0c5460; }
    .stWarning { background-color: #fff3cd; border-left: 5px solid #856404; }
    
    /* === SELECTBOX & DROPDOWNS === */
    [data-baseweb="select"] { background-color: #222222 !important; border: 2px solid #cc0000; border-radius: 8px; }
    [data-baseweb="select"] > div, [role="listbox"], [role="option"] {
        background-color: #323232 !important;
        color: white !important;
    }
    
    /* === TABELAS === */
    .centered-table table { margin-left: auto !important; margin-right: auto !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    if os.path.exists('data/pokemons.csv'):
        df = pd.read_csv('data/pokemons.csv')
        atributos = ['hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
        cols = [c for c in atributos if c in df.columns]
        if cols:
            df['total_stats'] = df[cols].sum(axis=1)
        return df
    return pd.DataFrame()

def insight1_todos_pokemons(df):
    st.subheader("1. Todos os Pokémon e seus Status")
    if df.empty:
        st.warning("Dados insuficientes")
        return
    
    st.markdown("#### Base de Dados Completa")
    
    # Seleciona colunas e prepara DataFrame (usa função auxiliar)
    cols_existentes = selecionar_colunas_display(df, incluir_total=True)
    df_display = df[cols_existentes].copy()
    
    # Ordena por poder total (decrescente)
    if 'total_stats' in df_display.columns:
        df_display = df_display.sort_values('total_stats', ascending=False)
    
    # Renomeia colunas (usa constante global)
    df_display = df_display.rename(columns=RENAME_COLUNAS)
    
    # Controles de ordenação
    col_ord1, col_ord2 = st.columns(2)
    with col_ord1:
        coluna_ordenar = st.selectbox(
            "Ordenar por:",
            options=list(df_display.columns),
            index=list(df_display.columns).index('Poder Total') if 'Poder Total' in df_display.columns else 0,
            key="ord_col"
        )
    with col_ord2:
        ordem = st.selectbox(
            "Ordem:",
            options=["Decrescente (maior → menor)", "Crescente (menor → maior)"],
            index=0,
            key="ord_dir"
        )
    
    # Aplica ordenação
    ascending = ordem.startswith("Crescente")
    df_display = df_display.sort_values(coluna_ordenar, ascending=ascending)
    df_display = df_display.reset_index(drop=True)
    df_display.index = df_display.index + 1
    
    # Exibe tabela centralizada
    st.markdown('<div class="centered-table">' + df_display.to_html() + '</div>', unsafe_allow_html=True)
    
    # Estatísticas resumidas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Pokémon", len(df))
    with col2:
        if 'legendary' in df.columns:
            st.metric("Lendários", int(df['legendary'].sum()))
    with col3:
        if 'generation' in df.columns:
            st.metric("Gerações", df['generation'].nunique())
    with col4:
        if 'total_stats' in df.columns:
            st.metric("Poder Médio", round(df['total_stats'].mean(), 1))

def insight2_tipo_ataque(df):
    st.subheader("2. Qual o tipo com a maior média de ataque?")
    if df.empty or 'types' not in df.columns or 'attack' not in df.columns:
        st.warning("Dados insuficientes")
        return
    
    tipos_atk = {}
    tipos_pokemons = {}
    for _, row in df.iterrows():
        tipos = row['types']
        atk = row['attack']
        nome = row.get('name', 'Desconhecido')
        if pd.notna(tipos) and pd.notna(atk):
            # Usa função auxiliar para extrair tipos
            lista_tipos = extrair_tipos(tipos)
            for t in lista_tipos:
                if t not in tipos_atk:
                    tipos_atk[t] = []
                    tipos_pokemons[t] = []
                tipos_atk[t].append(float(atk))
                tipos_pokemons[t].append(nome)
    
    medias = []
    for tipo, ataques in tipos_atk.items():
        if ataques:
            pokemons_lista = ', '.join(tipos_pokemons[tipo])
            medias.append({'Tipo': tipo, 'Media_Ataque': round(sum(ataques)/len(ataques), 2), 'Quantidade': len(ataques), 'Pokemons': pokemons_lista})
    
    if medias:
        df_m = pd.DataFrame(medias).sort_values('Media_Ataque', ascending=False)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Ranking por Média de Ataque")
            st.markdown(df_m.to_html(index=False), unsafe_allow_html=True)
        with col2:
            fig = px.bar(df_m, x='Tipo', y='Media_Ataque', title='Média de Ataque por Tipo', color='Media_Ataque', color_continuous_scale='Viridis', text='Media_Ataque')
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            aplicar_layout_padrao(fig)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        melhor = df_m.iloc[0]
        st.success(f"O tipo **{melhor['Tipo']}** tem a maior média de ataque: **{melhor['Media_Ataque']}**")

def insight3_indice_poder(df):
    st.subheader("3. Índice de Poder - Top 10 Pokémon")
    if df.empty or 'total_stats' not in df.columns:
        st.warning("Dados insuficientes")
        return
    
    top10 = df.nlargest(10, 'total_stats')
    
    # Usa função auxiliar para selecionar colunas
    cols_ex = selecionar_colunas_display(top10, incluir_total=True)
    
    st.markdown("#### Top 10 Ranking")
    df_d = top10[cols_ex].copy()
    
    # Renomeia colunas para português (usa constante global)
    df_d = df_d.rename(columns=RENAME_COLUNAS)
    
    df_d = df_d.reset_index(drop=True)
    df_d.index = df_d.index + 1
    st.markdown('<div class="centered-table">' + df_d.to_html() + '</div>', unsafe_allow_html=True)
    
    st.markdown("#### Gráfico de Poder Total")
    fig = px.bar(top10, x='total_stats', y='name', orientation='h', title='Top 10 por Poder Total', color='total_stats', color_continuous_scale='Viridis', text='total_stats')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    aplicar_layout_padrao(fig)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    if 'legendary' in top10.columns:
        leg = top10['legendary'].sum()
        st.info(f"{leg} dos 10 mais poderosos são Lendários!")

def insight4_simulador_batalha(df):
    st.subheader("4. Simulador de Batalha Pokémon")
    if df.empty or 'name' not in df.columns:
        st.warning("Dados insuficientes")
        return
    
    st.markdown("Escolha dois Pokemon para batalhar e descubra quem vence!")
    
    col1, col2 = st.columns(2)
    
    pokemon_names = sorted(df['name'].tolist())
    
    with col1:
        st.markdown("#### Pokémon 1")
        pokemon1_name = st.selectbox("Selecione o primeiro Pokémon:", pokemon_names, key="p1")
        pokemon1 = df[df['name'] == pokemon1_name].iloc[0]
        
        st.markdown(f"**Nome:** {pokemon1['name']}")
        if 'types' in df.columns:
            st.markdown(f"**Tipo:** {pokemon1['types']}")
        if 'legendary' in df.columns:
            st.markdown(f"**Lendário:** {'Sim' if pokemon1['legendary'] else 'Não'}")
        if 'total_stats' in df.columns:
            st.markdown(f"**Poder Total:** {pokemon1['total_stats']}")
        
        # Usa constante global para atributos
        stats1 = {attr.replace('_', ' ').title(): pokemon1[attr] for attr in ATRIBUTOS_BATALHA if attr in df.columns}
        
        if stats1:
            df_stats1 = pd.DataFrame(list(stats1.items()), columns=['Atributo', 'Valor'])
            fig1 = px.bar(df_stats1, x='Atributo', y='Valor', title=f'Atributos de {pokemon1_name}', color='Valor', color_continuous_scale='Blues')
            aplicar_layout_padrao(fig1)
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("#### Pokémon 2")
        pokemon2_name = st.selectbox("Selecione o segundo Pokémon:", pokemon_names, key="p2")
        pokemon2 = df[df['name'] == pokemon2_name].iloc[0]
        
        st.markdown(f"**Nome:** {pokemon2['name']}")
        if 'types' in df.columns:
            st.markdown(f"**Tipo:** {pokemon2['types']}")
        if 'legendary' in df.columns:
            st.markdown(f"**Lendário:** {'Sim' if pokemon2['legendary'] else 'Não'}")
        if 'total_stats' in df.columns:
            st.markdown(f"**Poder Total:** {pokemon2['total_stats']}")
        
        # Usa constante global para atributos
        stats2 = {attr.replace('_', ' ').title(): pokemon2[attr] for attr in ATRIBUTOS_BATALHA if attr in df.columns}
        
        if stats2:
            df_stats2 = pd.DataFrame(list(stats2.items()), columns=['Atributo', 'Valor'])
            fig2 = px.bar(df_stats2, x='Atributo', y='Valor', title=f'Atributos de {pokemon2_name}', color='Valor', color_continuous_scale='Reds')
            aplicar_layout_padrao(fig2)
            st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    if st.button("INICIAR BATALHA!", type="primary", use_container_width=True):
        st.markdown("### Resultado da Batalha")
        
        if 'total_stats' in df.columns:
            poder1 = pokemon1['total_stats']
            poder2 = pokemon2['total_stats']
            
            col_result1, col_result2, col_result3 = st.columns(3)
            
            with col_result1:
                st.metric(f"{pokemon1_name}", f"Poder: {poder1}")
            
            with col_result2:
                st.markdown("### VS")
            
            with col_result3:
                st.metric(f"{pokemon2_name}", f"Poder: {poder2}")
            
            st.divider()
            
            if poder1 > poder2:
                diferenca = poder1 - poder2
                percentual = (diferenca / poder2) * 100
                st.success(f"🏆 **{pokemon1_name}** VENCEU a batalha!")
                st.info(f"{pokemon1_name} é **{percentual:.1f}%** mais forte que {pokemon2_name} (diferença de {diferenca} pontos)")
            elif poder2 > poder1:
                diferenca = poder2 - poder1
                percentual = (diferenca / poder1) * 100
                st.success(f"🏆 **{pokemon2_name}** VENCEU a batalha!")
                st.info(f"{pokemon2_name} é **{percentual:.1f}%** mais forte que {pokemon1_name} (diferença de {diferenca} pontos)")
            else:
                st.warning(f"⚔️ EMPATE! Ambos tem o mesmo poder total: {poder1}")
            
            # Usa constante global para comparação de atributos
            comparacao = []
            for attr in ATRIBUTOS_BATALHA:
                if attr in df.columns:
                    val1 = pokemon1[attr]
                    val2 = pokemon2[attr]
                    vencedor = pokemon1_name if val1 > val2 else (pokemon2_name if val2 > val1 else "Empate")
                    comparacao.append({
                        'Atributo': attr.replace('_', ' ').title(),
                        pokemon1_name: val1,
                        pokemon2_name: val2,
                        'Vencedor': vencedor
                    })
            
            if comparacao:
                df_comp = pd.DataFrame(comparacao)
                st.markdown("#### Comparação Detalhada de Atributos")
                st.markdown(df_comp.to_html(index=False), unsafe_allow_html=True)
        else:
            st.error("Dados de poder total não disponíveis para calcular o vencedor")

def insight5_melhor_equipe(df):
    st.subheader("5. Composição da Equipe Ideal")
    if df.empty or 'total_stats' not in df.columns:
        st.warning("Dados insuficientes")
        return
    
    st.markdown("Análise estratégica para montar uma equipe balanceada com maior probabilidade de vitória")
    
    # Tamanho da equipe
    tamanho_equipe = st.slider("Tamanho da equipe:", min_value=3, max_value=6, value=6, key="team_size")
    
    # Estratégia de seleção
    col1, col2 = st.columns(2)
    
    with col1:
        estrategia = st.radio(
            "Estratégia de seleção:",
            ["Poder Total (Força Bruta)", "Balanceamento de Atributos", "Diversidade de Tipos"],
            key="strategy"
        )
    
    with col2:
        incluir_lendarios = st.checkbox("Incluir Lendários", value=True, key="legends")
    
    # Filtra dataset
    df_disponivel = df.copy()
    if not incluir_lendarios and 'legendary' in df.columns:
        df_disponivel = df_disponivel[df_disponivel['legendary'] == False]
    
    if df_disponivel.empty:
        st.warning("Nenhum Pokémon disponível com os filtros selecionados")
        return
    
    # Monta equipe baseado na estratégia
    if estrategia == "Poder Total (Força Bruta)":
        # Seleciona os N mais fortes
        equipe = df_disponivel.nlargest(tamanho_equipe, 'total_stats')
        st.info("Estratégia: Seleciona os Pokémon com maior poder total absoluto")
        
    elif estrategia == "Balanceamento de Atributos":
        # Calcula score de balanceamento (usa constante global)
        cols_disponiveis = [c for c in ATRIBUTOS_BATALHA if c in df_disponivel.columns]
        
        if cols_disponiveis:
            df_disponivel['balance_score'] = df_disponivel[cols_disponiveis].std(axis=1)
            # Combina poder total com balanceamento (menor std = melhor)
            df_disponivel['final_score'] = df_disponivel['total_stats'] - (df_disponivel['balance_score'] * 10)
            equipe = df_disponivel.nlargest(tamanho_equipe, 'final_score')
            st.info("Estratégia: Prioriza Pokémon com atributos equilibrados e bom poder total")
        else:
            equipe = df_disponivel.nlargest(tamanho_equipe, 'total_stats')
            
    else:  # Diversidade de Tipos
        # Tenta maximizar diversidade de tipos
        equipe_list = []
        tipos_usados = set()
        
        for _, pokemon in df_disponivel.nlargest(len(df_disponivel), 'total_stats').iterrows():
            if len(equipe_list) >= tamanho_equipe:
                break
            
            # Usa função auxiliar para extrair tipos
            tipos_pokemon = extrair_tipos(pokemon.get('types', ''))
            
            # Verifica se adiciona tipos novos
            novos_tipos = set(tipos_pokemon) - tipos_usados
            if novos_tipos or len(equipe_list) < 2:  # Garante pelo menos 2 pokemon
                equipe_list.append(pokemon)
                tipos_usados.update(tipos_pokemon)
        
        equipe = pd.DataFrame(equipe_list)
        st.info("Estratégia: Maximiza diversidade de tipos para cobrir mais fraquezas")
    
    # Exibe equipe selecionada
    st.markdown("### Equipe Ideal Selecionada")
    
    # Usa função auxiliar para selecionar colunas
    cols_existentes = selecionar_colunas_display(equipe, incluir_total=True)
    equipe_display = equipe[cols_existentes].copy()
    equipe_display = equipe_display.reset_index(drop=True)
    equipe_display.index = equipe_display.index + 1
    
    # Renomeia colunas (usa constante global + mapeamento customizado)
    rename_custom = RENAME_COLUNAS.copy()
    rename_custom.update({'sp_attack': 'Atq Esp', 'sp_defense': 'Def Esp', 'speed': 'Vel', 'total_stats': 'Poder'})
    equipe_display = equipe_display.rename(columns=rename_custom)
    
    st.markdown('<div class="centered-table">' + equipe_display.to_html() + '</div>', unsafe_allow_html=True)
    
    # Estatísticas da equipe
    st.markdown("### Análise da Equipe")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Poder Total", int(equipe['total_stats'].sum()))
    with col2:
        st.metric("Poder Médio", round(equipe['total_stats'].mean(), 1))
    with col3:
        if 'legendary' in equipe.columns:
            st.metric("Lendários", int(equipe['legendary'].sum()))
    with col4:
        if 'types' in equipe.columns:
            # Usa função auxiliar para extrair tipos
            todos_tipos = []
            for tipos in equipe['types']:
                todos_tipos.extend(extrair_tipos(tipos))
            st.metric("Tipos Únicos", len(set(todos_tipos)))
    
    # Gráfico de atributos da equipe (usa constante global)
    cols_disponiveis = [c for c in ATRIBUTOS_BATALHA if c in equipe.columns]
    
    if cols_disponiveis:
        st.markdown("### Perfil de Atributos da Equipe")
        medias = equipe[cols_disponiveis].mean()
        
        df_radar = pd.DataFrame({
            'Atributo': [c.replace('_', ' ').title() for c in cols_disponiveis],
            'Media': medias.values
        })
        
        fig = px.bar(df_radar, x='Atributo', y='Media', 
                     title='Média dos Atributos da Equipe',
                     color='Media', color_continuous_scale='Viridis')
        aplicar_layout_padrao(fig)
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("Pokémon Analytics - Insights e Simulador de Batalha")
    st.markdown("Análise de dados extraídos via ETL")
    st.divider()
    
    df = carregar_dados()
    if df.empty:
        st.error("Nenhum dado encontrado! Execute: python etl.py")
        return
    
    with st.sidebar:
        st.header("Informações")
        st.metric("Total Pokémons", len(df))
        if 'legendary' in df.columns:
            st.metric("Lendários", int(df['legendary'].sum()))
        if 'generation' in df.columns:
            st.metric("Gerações", df['generation'].nunique())
        st.divider()
        st.markdown("### Insights")
        st.markdown("1. Todos os Pokémons")
        st.markdown("2. Maior média de ataque por tipo")
        st.markdown("3. Top 10 poderosos")
        st.markdown("4. Simulador de Batalha")
        st.markdown("5. Equipe Ideal")

    insight1_todos_pokemons(df)
    st.divider()
    insight2_tipo_ataque(df)
    st.divider()
    insight3_indice_poder(df)
    st.divider()
    insight4_simulador_batalha(df)
    st.divider()
    insight5_melhor_equipe(df)

if __name__ == "__main__":
    main()
