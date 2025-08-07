
import pandas as pd
import os

def extract_data(data_path=\'../data/\'):
    """
    Extrai os dados brutos dos arquivos CSV.

    Args:
        data_path (str): Caminho para o diretório contendo os arquivos CSV de dados brutos.

    Returns:
        tuple: Uma tupla de DataFrames (customers_df, contacts_df, sales_df, funnel_df).
    """
    # Carrega cada arquivo CSV em um DataFrame pandas
    customers_df = pd.read_csv(f\'{data_path}customers.csv\')
    contacts_df = pd.read_csv(f\'{data_path}contacts.csv\')
    sales_df = pd.read_csv(f\'{data_path}sales.csv\')
    funnel_df = pd.read_csv(f\'{data_path}funnel.csv\')
    return customers_df, contacts_df, sales_df, funnel_df

def transform_data(customers_df, contacts_df, sales_df, funnel_df):
    """
    Transforma os dados brutos, realizando limpeza, conversão de tipos e junções.

    Args:
        customers_df (pd.DataFrame): DataFrame de clientes.
        contacts_df (pd.DataFrame): DataFrame de contatos.
        sales_df (pd.DataFrame): DataFrame de vendas.
        funnel_df (pd.DataFrame): DataFrame de funil de vendas.

    Returns:
        tuple: Uma tupla de DataFrames transformados e unidos.
    """
    # Converte colunas de data para o tipo datetime e extrai o mês
    contacts_df[\'contact_date\'] = pd.to_datetime(contacts_df[\'contact_date\'])
    contacts_df[\'contact_month\'] = contacts_df[\'contact_date\'].dt.to_period(\'M\')

    sales_df[\'sale_date\'] = pd.to_datetime(sales_df[\'sale_date\'])
    sales_df[\'sale_month\'] = sales_df[\'sale_date\'].dt.to_period(\'M\')

    funnel_df[\'start_date\'] = pd.to_datetime(funnel_df[\'start_date\'])
    funnel_df[\'end_date\'] = pd.to_datetime(funnel_df[\'end_date\'])
    # Calcula a duração em dias para as etapas do funil
    funnel_df[\'duration_days\'] = (funnel_df[\'end_date\'] - funnel_df[\'start_date\']).dt.days

    # Realiza junções (merges) para criar DataFrames para análises combinadas
    customers_contacts = pd.merge(customers_df, contacts_df, on=\'customer_id\', how=\'left\')
    customers_sales = pd.merge(customers_df, sales_df, on=\'customer_id\', how=\'left\')
    funnel_customers = pd.merge(funnel_df, customers_df, on=\'customer_id\', how=\'left\')

    return customers_df, contacts_df, sales_df, funnel_df, customers_contacts, customers_sales, funnel_customers

def load_data(customers_df, contacts_df, sales_df, funnel_df, customers_contacts, customers_sales, funnel_customers, output_path=\'../data/processed/\'):
    """
    Carrega os dados transformados em arquivos CSV no diretório de saída.

    Args:
        customers_df (pd.DataFrame): DataFrame de clientes processado.
        contacts_df (pd.DataFrame): DataFrame de contatos processado.
        sales_df (pd.DataFrame): DataFrame de vendas processado.
        funnel_df (pd.DataFrame): DataFrame de funil de vendas processado.
        customers_contacts (pd.DataFrame): DataFrame de clientes e contatos unidos.
        customers_sales (pd.DataFrame): DataFrame de clientes e vendas unidos.
        funnel_customers (pd.DataFrame): DataFrame de funil e clientes unidos.
        output_path (str): Caminho para o diretório onde os dados processados serão salvos.
    """
    # Cria o diretório de saída se ele não existir
    os.makedirs(output_path, exist_ok=True)

    # Salva cada DataFrame processado em um arquivo CSV
    customers_df.to_csv(f\'{output_path}customers_processed.csv\', index=False)
    contacts_df.to_csv(f\'{output_path}contacts_processed.csv\', index=False)
    sales_df.to_csv(f\'{output_path}sales_processed.csv\', index=False)
    funnel_df.to_csv(f\'{output_path}funnel_processed.csv\', index=False)
    customers_contacts.to_csv(f\'{output_path}customers_contacts_processed.csv\', index=False)
    customers_sales.to_csv(f\'{output_path}customers_sales_processed.csv\', index=False)
    funnel_customers.to_csv(f\'{output_path}funnel_customers_processed.csv\', index=False)

    print("Dados processados salvos em \'crm_etl_project/data/processed/\'.")

if __name__ == \'__main__\':
    # Bloco principal de execução quando o script é chamado diretamente
    print("Iniciando o pipeline ETL...")
    # Extração
    customers, contacts, sales, funnel = extract_data()
    # Transformação
    customers_p, contacts_p, sales_p, funnel_p, customers_contacts_p, customers_sales_p, funnel_customers_p = transform_data(customers, contacts, sales, funnel)
    # Carga
    load_data(customers_p, contacts_p, sales_p, funnel_p, customers_contacts_p, customers_sales_p, funnel_customers_p)
    print("Pipeline ETL concluído com sucesso!")


