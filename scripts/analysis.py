
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Carregar dados processados
processed_data_path = \'../data/processed/\'
customers_df = pd.read_csv(f\'{processed_data_path}customers_processed.csv\')
customers_sales = pd.read_csv(f\'{processed_data_path}customers_sales_processed.csv\')
funnel_customers = pd.read_csv(f\'{processed_data_path}funnel_customers_processed.csv\')
contacts_df = pd.read_csv(f\'{processed_data_path}contacts_processed.csv\')

# Merge contacts_df with customers_df to get customer names for analysis
contacts_with_names = pd.merge(contacts_df, customers_df[[\'customer_id\', \'customer_name\']], on=\'customer_id\', how=\'left\')

# Criar diretório para salvar os relatórios se não existir
reports_path = \'../reports/\'
os.makedirs(reports_path, exist_ok=True)

# Análise 1: Clientes Mais Ativos (por número de contatos)
def plot_active_clients(data):
    """
    Gera um gráfico de barras dos 10 clientes mais ativos com base no número de contatos.

    Args:
        data (pd.DataFrame): DataFrame contendo dados de contatos com nomes de clientes.
    """
    # Agrupa os dados por nome do cliente e conta o número de contatos, pegando os 10 maiores
    active_clients = data.groupby(\'customer_name\')[\'contact_id\'].count().nlargest(10)
    
    plt.figure(figsize=(12, 6))
    active_clients.plot(kind=\'bar\', color=\'skyblue\')
    plt.title(\'Top 10 Clientes Mais Ativos por Número de Contatos\')
    plt.xlabel(\'Cliente\')
    plt.ylabel(\'Número de Contatos\')
    plt.xticks(rotation=45) # Rotaciona os rótulos do eixo X para melhor legibilidade
    plt.tight_layout() # Ajusta o layout para evitar sobreposição
    plt.savefig(f\'{reports_path}active_clients.png\') # Salva o gráfico como imagem
    plt.close() # Fecha a figura para liberar memória

# Análise 2: Taxa de Conversão por Etapa do Funil
def plot_conversion_rate(data):
    """
    Gera um gráfico de funil mostrando a taxa de conversão entre as etapas do funil de vendas.

    Args:
        data (pd.DataFrame): DataFrame contendo dados do funil de vendas.
    """
    # Define a ordem das etapas do funil para garantir a visualização correta
    funnel_stages_order = [\'Lead\', \'Qualificação\', \'Proposta\', \'Negociação\', \'Fechado Ganho\', \'Fechado Perdido\']
    # Conta a ocorrência de cada estágio e reindexa para a ordem definida
    stage_counts = data[\'stage\'].value_counts().reindex(funnel_stages_order)
    
    # Remover estágios nulos ou com contagem zero para evitar erros no funil Plotly
    stage_counts = stage_counts.dropna()
    stage_counts = stage_counts[stage_counts > 0]

    if stage_counts.empty:
        print("Não há dados suficientes para gerar o funil de vendas.")
        return

    # Cria o gráfico de funil usando Plotly Express
    fig = px.funnel(x=stage_counts.values, y=stage_counts.index, title=\'Funil de Vendas e Taxa de Conversão\')
    fig.update_traces(textinfo=\'value+percent initial\') # Mostra o valor e a porcentagem inicial
    fig.write_image(f\'{reports_path}conversion_funnel.png\') # Salva o gráfico como imagem

# Análise 3: Tempo Médio de Resposta (exemplo fictício, pois não temos dados de resposta direta)
def plot_avg_response_time(data):
    """
    Gera um gráfico de barras do tempo médio de duração por etapa do funil de vendas.
    Utiliza a duração do funil como um proxy para o tempo de resposta.

    Args:
        data (pd.DataFrame): DataFrame contendo dados do funil de vendas com a duração em dias.
    """
    # Calcula a média da duração em dias para cada estágio do funil
    avg_duration_per_stage = data.groupby(\'stage\')[\'duration_days\'].mean().dropna()
    
    if avg_duration_per_stage.empty:
        print("Não há dados de duração de funil para analisar o tempo médio de resposta.")
        return

    plt.figure(figsize=(10, 6))
    avg_duration_per_stage.plot(kind=\'bar\', color=\'lightgreen\')
    plt.title(\'Tempo Médio de Duração por Etapa do Funil (Proxy para Tempo de Resposta)\'
)    plt.xlabel(\'Etapa do Funil\')
    plt.ylabel(\'Tempo Médio (Dias)\'
)    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f\'{reports_path}avg_response_time.png\')
    plt.close()

if __name__ == \'__main__\':
    # Bloco principal de execução quando o script é chamado diretamente
    print("Gerando análises e visualizações...")
    # Chama as funções de plotagem com os DataFrames apropriados
    plot_active_clients(contacts_with_names)
    plot_conversion_rate(funnel_customers)
    plot_avg_response_time(funnel_customers)
    print("Análises e visualizações geradas e salvas em \'crm_etl_project/reports/\'.")


