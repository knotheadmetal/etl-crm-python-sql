
import schedule # Biblioteca para agendamento de tarefas
import time     # Biblioteca para controle de tempo
import subprocess # Biblioteca para executar comandos externos (outros scripts Python)
import os       # Biblioteca para interagir com o sistema operacional (caminhos de arquivo)

def run_etl_and_analysis():
    """
    Função principal que orquestra a execução do pipeline ETL e dos scripts de análise.
    Chama os scripts `etl_pipeline.py` e `analysis.py` em sequência.
    """
    print("Iniciando a execução do pipeline ETL e análises...")
    # Obtém o diretório atual do script para construir caminhos relativos
    script_dir = os.path.dirname(__file__)
    
    # Opcional: Executar o script de geração de dados se for necessário atualizar os dados fictícios
    # subprocess.run(["python3.11", os.path.join(script_dir, "generate_data.py")], cwd=script_dir)
    
    # Executa o script do pipeline ETL para extrair, transformar e carregar os dados
    subprocess.run(["python3.11", os.path.join(script_dir, "etl_pipeline.py")], cwd=script_dir)
    
    # Executa o script de análises e visualizações para gerar os relatórios
    subprocess.run(["python3.11", os.path.join(script_dir, "analysis.py")], cwd=script_dir)
    print("Execução do pipeline ETL e análises concluída.")

# Agendamento da tarefa:
# schedule.every(24).hours.do(run_etl_and_analysis) # Exemplo: Agendar para rodar a cada 24 horas
# schedule.every().day.at("10:30").do(run_etl_and_analysis) # Exemplo: Agendar para rodar todo dia às 10:30

# Para fins de demonstração e teste, o agendamento está configurado para rodar a cada 1 minuto.
schedule.every(1).minutes.do(run_etl_and_analysis)

print("Agendador de relatórios iniciado. Pressione Ctrl+C para parar.")

# Loop infinito para manter o agendador em execução
while True:
    schedule.run_pending() # Executa todas as tarefas agendadas que estão pendentes
    time.sleep(1)          # Espera 1 segundo antes de verificar novamente


