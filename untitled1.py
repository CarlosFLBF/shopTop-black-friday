# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WHYxheDSpOtlo1ogdVej4FWupCnhSegP
"""

!pip install -U kaleido

!apt-get install -y xvfb libgtk2.0-0 libgconf-2-4
!pip install -U orca
!pip install -U psutil  # Dependência necessária para orca

import plotly.io as pio
pio.orca.config.use_xvfb = True

# Instalação das dependências (executar no Google Colab)
!apt-get install -y xvfb libgtk2.0-0 libgconf-2-4
!pip install -U orca
!pip install -U psutil
!pip install pandas numpy matplotlib seaborn plotly

# Importação das bibliotecas
import pandas as pd
import numpy as np
import random
from datetime import timedelta, date
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.io as pio

# Configurar orca para usar xvfb
pio.orca.config.use_xvfb = True

# Função para gerar uma data aleatória
def random_date(start_date, end_date):
    """
    Gera uma data aleatória entre start_date e end_date.
    """
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

# Função para criar o DataFrame simulado
def create_simulated_data(start_date, end_date, num_samples=2000):
    """
    Cria um DataFrame simulado com dados de vendas.
    """
    produtos = ['Smartphone', 'Laptop', 'Tablet', 'Camiseta', 'Calça', 'Livro', 'Fone de ouvido', 'Mouse', 'Teclado', 'Cadeira']
    categorias = ['Eletrônicos', 'Roupas', 'Livros', 'Escritório']
    regioes = ['Norte', 'Sul', 'Leste', 'Oeste']
    idades = np.random.randint(18, 70, num_samples)
    sexos = random.choices(['M', 'F'], k=num_samples)
    campanhas = random.choices(['Padrao', 'BlackFriday', 'Promocao'], k=num_samples)

    data = {
        'produto': random.choices(produtos, k=num_samples),
        'categoria': random.choices(categorias, k=num_samples),
        'preco': np.random.uniform(20, 1000, num_samples),
        'data': [random_date(start_date, end_date) for _ in range(num_samples)],
        'regiao': random.choices(regioes, k=num_samples),
        'quantidade': np.random.randint(1, 10, num_samples),
        'desconto': np.random.uniform(0, 0.3, num_samples),
        'idade': idades,
        'sexo': sexos,
        'campanha': campanhas
    }

    df = pd.DataFrame(data)
    df['data'] = pd.to_datetime(df['data'])  # Conversão da coluna 'data' para datetime
    return df

# Função para ajustar sazonalidade
def adjust_seasonality(df):
    """
    Ajusta a sazonalidade das vendas (aumenta vendas em novembro e dezembro).
    """
    try:
        df['mes'] = df['data'].dt.month
        df.loc[df['mes'].isin([11, 12]), 'quantidade'] *= 1.5
    except Exception as e:
        print(f"Erro ao ajustar sazonalidade: {e}")
    return df

# Função para salvar e carregar o DataFrame
def save_and_load_data(df, filename='vendas_simuladas_avancado.csv'):
    """
    Salva o DataFrame em um arquivo CSV e o carrega novamente.
    """
    try:
        df.to_csv(filename, index=False)
        df = pd.read_csv(filename)
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df = df.dropna(subset=['data'])
    except Exception as e:
        print(f"Erro ao salvar/carregar dados: {e}")
    return df

# Função para plotar as análises
def plot_analyses(df):
    """
    Gera gráficos para análise exploratória de dados.
    """
    # Gráfico de distribuição de idade
    plt.figure(figsize=(12, 6))
    sns.histplot(df['idade'], bins=20, kde=True, color='blue')
    plt.title('Distribuição de Idade dos Clientes', fontsize=16)
    plt.xlabel('Idade', fontsize=12)
    plt.ylabel('Frequência', fontsize=12)
    plt.savefig('distribuicao_idade.png')  # Salva o gráfico como imagem
    plt.show()

    # Gráfico de distribuição por sexo
    plt.figure(figsize=(8, 5))
    sns.countplot(x='sexo', data=df, palette='viridis')
    plt.title('Distribuição de Clientes por Sexo', fontsize=16)
    plt.xlabel('Sexo', fontsize=12)
    plt.ylabel('Contagem', fontsize=12)
    plt.savefig('distribuicao_sexo.png')  # Salva o gráfico como imagem
    plt.show()

    # Gráfico de vendas por campanha
    plt.figure(figsize=(10, 5))
    sns.countplot(x='campanha', data=df, palette='coolwarm')
    plt.title('Distribuição de Vendas por Campanha', fontsize=16)
    plt.xlabel('Campanha', fontsize=12)
    plt.ylabel('Contagem', fontsize=12)
    plt.savefig('vendas_por_campanha.png')  # Salva o gráfico como imagem
    plt.show()

    # Gráfico de vendas mensais
    vendas_mensais = df.groupby(df['data'].dt.to_period('M'))['quantidade'].sum().reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(x='data', y='quantidade', data=vendas_mensais, palette='magma')
    plt.title('Vendas Mensais ao Longo do Tempo', fontsize=16)
    plt.xlabel('Mês', fontsize=12)
    plt.ylabel('Quantidade Vendida', fontsize=12)
    plt.xticks(rotation=45)
    plt.savefig('vendas_mensais.png')  # Salva o gráfico como imagem
    plt.show()

    # Matriz de correlação
    corr_matrix = df[['preco', 'quantidade', 'desconto', 'idade']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matriz de Correlação', fontsize=16)
    plt.savefig('matriz_correlacao.png')  # Salva o gráfico como imagem
    plt.show()

    # Gráfico de vendas por categoria e sexo (Plotly)
    fig = px.bar(df, x='categoria', y='quantidade', color='sexo', barmode='group',
                 title='Vendas por Categoria e Sexo', labels={'quantidade': 'Quantidade Vendida'})
    fig.write_image('vendas_por_categoria_sexo.png')  # Salva o gráfico como imagem
    fig.show()

    # Gráfico de vendas por região e campanha (Plotly)
    fig = px.bar(df, x='regiao', y='quantidade', color='campanha', barmode='group',
                 title='Vendas por Região e Campanha', labels={'quantidade': 'Quantidade Vendida'})
    fig.write_image('vendas_por_regiao_campanha.png')  # Salva o gráfico como imagem
    fig.show()

# Data de início e fim para a simulação
start_date = date(2022, 1, 1)
end_date = date(2023, 12, 31)

# Criação dos dados simulados
df = create_simulated_data(start_date, end_date)

# Ajuste sazonal
df = adjust_seasonality(df)

# Salvando e carregando os dados
df = save_and_load_data(df)

# Plotando as análises
plot_analyses(df)