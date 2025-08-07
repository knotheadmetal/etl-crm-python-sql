
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_crm_data(num_records=1000):
    """
    Gera dados fictícios para um CRM, incluindo informações de clientes, contatos, vendas e funil de vendas.

    Args:
        num_records (int): Número base de registros a serem gerados. O número real de registros pode variar
                           para cada DataFrame (contatos, vendas, funil).

    Returns:
        tuple: Uma tupla contendo quatro DataFrames do pandas: customers_df, contacts_df, sales_df, funnel_df.
    """
    np.random.seed(42) # Para reprodutibilidade dos dados

    # Geração de dados de Clientes
    customer_ids = [f'CUST{i:04d}' for i in range(1, num_records + 1)]
    customer_names = [f'Cliente {i}' for i in range(1, num_records + 1)]
    customer_segments = np.random.choice(['Pequena Empresa', 'Média Empresa', 'Grande Empresa', 'Autônomo'], num_records, p=[0.4, 0.3, 0.2, 0.1])
    customer_regions = np.random.choice(['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte'], num_records)

    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'customer_name': customer_names,
        'segment': customer_segments,
        'region': customer_regions
    })

    # Geração de dados de Contatos
    contact_ids = [f'CONT{i:04d}' for i in range(1, num_records * 2 + 1)]
    contact_customer_ids = np.random.choice(customer_ids, num_records * 2)
    contact_types = np.random.choice(['Email', 'Telefone', 'Reunião', 'Chat'], num_records * 2, p=[0.4, 0.3, 0.2, 0.1])
    contact_dates = [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(num_records * 2)]
    contact_outcomes = np.random.choice(['Sucesso', 'Falha', 'Não Atendido'], num_records * 2, p=[0.7, 0.2, 0.1])

    contacts_df = pd.DataFrame({
        'contact_id': contact_ids,
        'customer_id': contact_customer_ids,
        'contact_type': contact_types,
        'contact_date': contact_dates,
        'contact_outcome': contact_outcomes
    })

    # Geração de dados de Vendas
    sale_ids = [f'SALE{i:04d}' for i in range(1, int(num_records * 0.8) + 1)]
    sale_customer_ids = np.random.choice(customer_ids, int(num_records * 0.8))
    sale_dates = [datetime.now() - timedelta(days=np.random.randint(1, 300)) for _ in range(int(num_records * 0.8))]
    sale_values = np.random.uniform(50, 5000, int(num_records * 0.8)).round(2)
    sale_products = np.random.choice(['Produto A', 'Produto B', 'Serviço X', 'Serviço Y'], int(num_records * 0.8))

    sales_df = pd.DataFrame({
        'sale_id': sale_ids,
        'customer_id': sale_customer_ids,
        'sale_date': sale_dates,
        'sale_value': sale_values,
        'product': sale_products
    })

    # Geração de dados de Funil de Vendas
    funnel_ids = [f'FUNNEL{i:04d}' for i in range(1, int(num_records * 0.5) + 1)]
    funnel_customer_ids = np.random.choice(customer_ids, int(num_records * 0.5))
    funnel_stages = np.random.choice(['Lead', 'Qualificação', 'Proposta', 'Negociação', 'Fechado Ganho', 'Fechado Perdido'], int(num_records * 0.5), p=[0.25, 0.2, 0.2, 0.15, 0.1, 0.1])
    funnel_start_dates = [datetime.now() - timedelta(days=np.random.randint(1, 180)) for _ in range(int(num_records * 0.5))]
    # Define end_date only for 'Fechado Ganho' or 'Fechado Perdido' stages
    funnel_end_dates = [d + timedelta(days=np.random.randint(5, 60)) if s in ['Fechado Ganho', 'Fechado Perdido'] else None for d, s in zip(funnel_start_dates, funnel_stages)]

    funnel_df = pd.DataFrame({
        'funnel_id': funnel_ids,
        'customer_id': funnel_customer_ids,
        'stage': funnel_stages,
        'start_date': funnel_start_dates,
        'end_date': funnel_end_dates
    })

    return customers_df, contacts_df, sales_df, funnel_df

if __name__ == '__main__':
    # Executa a função de geração de dados quando o script é chamado diretamente
    customers, contacts, sales, funnel = generate_crm_data()

    # Salva os DataFrames gerados em arquivos CSV na pasta 'data/'
    customers.to_csv('../data/customers.csv', index=False)
    contacts.to_csv('../data/contacts.csv', index=False)
    sales.to_csv('../data/sales.csv', index=False)
    funnel.to_csv('../data/funnel.csv', index=False)

    print("Dados fictícios de CRM gerados e salvos em 'crm_etl_project/data/'.")


