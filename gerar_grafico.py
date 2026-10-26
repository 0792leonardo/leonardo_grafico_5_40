#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gráfico 5.40 – Benzeno – Evolução das concentrações médias anuais
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das concentrações médias anuais de BEN (benzeno) para diferentes estações
de monitoramento no estado de São Paulo.

O gráfico exibe:
- Séries temporais para cada estação (2016-2025)
- Cores personalizadas para cada localidade (definidas no dicionário styles)
- Dados carregados de um arquivo CSV
- Layout otimizado para visualização e análise

BEN = Benzeno - Composto Orgânico Volátil (COV) aromático, classificado como
cancerígeno do Grupo 1 pela IARC. É emitido principalmente por veículos
automotores, indústrias petroquímicas e refinarias. Mesmo em baixas
concentrações, representa risco à saúde humana.

Autor: Leonardo Rocha
Data: 2026-09-22
Versão: 1.0.0
"""

# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path  # Para manipulação de caminhos de arquivos de forma segura
import pandas as pd       # Para leitura e manipulação de dados em tabelas (DataFrames)
import plotly.graph_objects as go  # Para criação de gráficos interativos


# =============================================================================
# LEITURA DOS DADOS
# =============================================================================

# Define o caminho do arquivo CSV com os dados
CSV = Path("Dd_grafico_5_40.csv")

# Lê o arquivo CSV com parâmetros específicos para o padrão brasileiro:
# - sep=";": separador ponto-e-vírgula
# - decimal=",": vírgula como separador decimal
# - encoding="utf-8-sig": remove o BOM automaticamente
df = pd.read_csv(CSV, sep=";", decimal=",", encoding="utf-8-sig")

# Normaliza os nomes das colunas removendo espaços em branco extras
df.columns = [str(c).strip() for c in df.columns]


# =============================================================================
# CONFIGURAÇÃO DOS PARÂMETROS
# =============================================================================

# Nome da coluna que contém os nomes das estações
# Neste caso, a coluna se chama "Ano" mas contém os nomes das estações
# (nome um pouco confuso, mas é o que está no CSV)
station_col = "Ano"

# Lista de anos (2016 a 2025) como strings
# IMPORTANTE: aqui os anos são as COLUNAS do CSV, não linhas
years = [str(y) for y in range(2016, 2026)]


# =============================================================================
# PREPARAÇÃO DOS DADOS
# =============================================================================

# --- Conversão das colunas de anos para numérico ---
# Aceita vírgula como separador decimal (padrão brasileiro)
# Exemplo: "0,45" → 0.45
for c in years:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),
        errors="coerce"  # Valores inválidos se tornam NaN
    )


# =============================================================================
# DEFINIÇÃO DOS ESTILOS VISUAIS (POR ESTAÇÃO)
# =============================================================================

# Dicionário de estilos específicos para cada estação de monitoramento
# 
# DIFERENÇA IMPORTANTE: Ao contrário dos scripts anteriores que usavam listas
# com aplicação cíclica, aqui usamos um DICIONÁRIO onde cada estação tem
# sua cor e símbolo pré-definidos. Isso garante consistência visual em
# diferentes versões do gráfico.
# 
# Vantagens:
# - Cada estação sempre terá a mesma cor em qualquer execução
# - Fácil de ajustar cores específicas
# - Todas as estações usam o mesmo símbolo (circle) mas cores diferentes
styles = {
    "Cubatão-Centro(A)": ("#16638A", "circle"),           # Azul escuro
    "Paulínia(A)": ("#F2762E", "circle"),                 # Laranja
    "Pinheiros(A)": ("#176B2B", "circle"),                # Verde escuro
    "S.André-Capuava(A)": ("#169BCB", "circle"),          # Azul ciano
    "S.José Campos(A)": ("#9B2A9D", "circle"),            # Roxo
    "S.José Campos-V.Verde(A)": ("#4EA52C", "circle"),    # Verde
    "Ibirapuera(M)": ("#FF0000", "circle"),               # Vermelho
}


# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()

# Itera sobre cada linha do DataFrame (cada linha = uma estação)
# Nota: usa "_" para ignorar o índice, já que não é usado
for _, row in df.iterrows():
    # Obtém o nome da estação e remove espaços extras
    station = str(row[station_col]).strip()
    
    # Busca a cor e símbolo no dicionário styles
    # Se a estação não existir no dicionário, usa valores padrão
    # (.get com valor padrão: cinza e círculo)
    color, symbol = styles.get(station, ("#555555", "circle"))
    
    # Extrai os valores de BEN para cada ano
    y = [row[c] for c in years]
    
    # Formata os valores para o tooltip (padrão brasileiro)
    # - NaN → string vazia
    # - Numérico → 2 casas decimais com vírgula
    customdata = [
        "" if pd.isna(v) else f"{float(v):.1f}".replace(".", ",")
        for v in y
    ]
    
    # Adiciona uma série (traço) ao gráfico
    fig.add_trace(go.Scatter(
        # Dados do eixo X (anos) e eixo Y (valores de BEN)
        x=years,
        y=y,
        
        # Modo: linha conectando pontos + marcadores nos pontos
        mode="lines+markers",
        
        # Nome da estação (aparece na legenda)
        name=station,
        
        # Não conecta gaps (NaN) - a linha terá interrupções
        connectgaps=False,
        
        # Configuração da linha
        line=dict(
            color=color,          # Cor definida no dicionário styles
            width=3.2             # Linha GROSSA para destaque (BEN é cancerígeno)
        ),
        
        # Configuração dos marcadores
        marker=dict(
            color=color,          # Cor do marcador (mesma da linha)
            symbol=symbol,        # Símbolo (circle para todas)
            size=8                # Tamanho do marcador
        ),
        
        # Dados customizados para o tooltip (valores formatados em BR)
        customdata=customdata,
        
        # Template do tooltip
        hovertemplate=(
            "<b>%{fullData.name}</b><br>"  # Nome da estação em negrito
            "BEN: %{customdata} µg/m³<extra></extra>"  # Valor em µg/m³
        )
    ))


# =============================================================================
# CONFIGURAÇÃO DO LAYOUT (APARÊNCIA DO GRÁFICO)
# =============================================================================

fig.update_layout(
    # Tema claro com fundo branco
    template="plotly_white",
    
    # Altura da figura em pixels
    height=700,
    
    # Margens ao redor do gráfico
    # Margem esquerda maior (105px) para título do eixo Y
    # Margem inferior (135px) para legenda horizontal
    margin=dict(l=105, r=35, t=25, b=135),
    
    # Cor de fundo do papel (área externa ao gráfico)
    paper_bgcolor="#ffffff",                  # Branco
    
    # Cor de fundo da área do gráfico
    plot_bgcolor="#ffffff",                   # Branco
    
    # Modo de hover: exibe informações de todas as séries simultaneamente
    hovermode="x unified",
    
    # Configuração da fonte global
    font=dict(
        family="Arial, sans-serif",           # Fonte sans-serif
        size=14,                              # Tamanho padrão
        color="#555555"                       # Cinza escuro
    ),
    
    # Configuração do eixo X (horizontal)
    xaxis=dict(
        type="category",                      # Tipo categórico
        tickmode="array",                     # Ticks definidos manualmente
        tickvals=years,                       # Posições dos ticks = anos
        ticktext=years,                       # Rótulos dos ticks = anos
        showgrid=False,                       # Sem linhas de grade verticais
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#AAAAAA",                   # Cor da linha do eixo (cinza claro)
        ticks="inside",                            # Marcadores dentro do eixo
        range=[-0.0, len(years) - 0.0],              # Cola o 1º ponto no eixo Y
        categoryorder="array",                        # Mantém ordem original
        categoryarray=years                          # Ordem das categorias
    ),
    
    # Configuração do eixo Y (vertical)
    yaxis=dict(
        title="BEN (µg/m³)",                          # Título do eixo (unidade implícita: µg/m³)
        range=[0, 3],                         # Limites: 0 a 3 µg/m³
        dtick=0.5,                            # Intervalo de 0.5 em 0.5 µg/m³
        
        # Ticks personalizados com formato brasileiro (vírgula + 2 decimais)
        tickvals=[0, 0.5, 1, 1.5, 2, 2.5, 3],                       # Posições
        ticktext=["0,0", "0,5", "1,0", "1,5", "2,0", "2,5", "3,0"],  # Rótulos
        
        showgrid=True,                        # Mostra linhas de grade horizontais
        gridcolor="rgba(150,150,150,0.35)",   # Cinza com 35% de opacidade
        griddash="dot",                       # Linhas pontilhadas
        zeroline=False,                       # Sem linha no zero
        showline=True,                        # Mostra a linha do eixo
        linecolor="#AAAAAA",                   # Cor da linha do eixo
        ticks="outside"                           # Marcadores fora do eixo
    ),
    
    # Configuração da legenda
    legend=dict(
        orientation="h",                      # Horizontal
        yanchor="top",                        # Âncora no topo
        y=-0.16,                              # Posicionada abaixo do gráfico
        xanchor="center",                     # Centralizada horizontalmente
        x=0.5,                                # Centro do eixo X
        font=dict(size=12)                    # Tamanho da fonte da legenda
    )
)


# =============================================================================
# EXPORTAÇÃO DO GRÁFICO
# =============================================================================

# Salva o gráfico em um arquivo HTML (autônomo, com Plotly embutido)
fig.write_html(
    "index.html",                             # Nome do arquivo de saída
    include_plotlyjs=True,                    # Inclui a biblioteca Plotly (offline)
    full_html=True,                           # Gera um documento HTML completo
    config={                                  # Configurações do gráfico
        "responsive": True,                   # Gráfico se adapta à tela
        "displaylogo": False,                 # Remove o logo da Plotly
        "scrollZoom": True                    # Permite zoom com scroll
    }
)


# =============================================================================
# MENSAGEM DE CONFIRMAÇÃO
# =============================================================================

print("=" * 70)
print("✅ GRÁFICO DE BEN (BENZENO) GERADO COM SUCESSO!")
print("=" * 70)
print(f"📊 Arquivo: index.html")
print(f"📍 Local: {Path.cwd()}")
print(f"📈 Estações: {len(df)}")
print(f"📅 Período: {years[0]} a {years[-1]} ({len(years)} anos)")
print(f"🎨 Estilos personalizados: {len(styles)} estações")
print()
print("📋 Estações no gráfico:")
for _, row in df.iterrows():
    station = str(row[station_col]).strip()
    if station in styles:
        print(f"   ✅ {station}")
    else:
        print(f"   ⚠️  {station} (usando cor padrão)")
print("=" * 70)