import os
import shutil
from datetime import datetime

def organizar_por_data(caminho_pasta):
    for arquivo in os.listdir(caminho_pasta):
        caminho_origem = os.path.join(caminho_pasta, arquivo)
        
        if os.path.isfile(caminho_origem):
            # Obtém a data de modificação do arquivo
            timestamp = os.path.getmtime(caminho_origem)
            data = datetime.fromtimestamp(timestamp)
            nome_pasta = data.strftime("%Y-%m") # Ex: 2023-12
            
            pasta_destino = os.path.join(caminho_pasta, nome_pasta)
            os.makedirs(pasta_destino, exist_ok=True)
            
            shutil.move(caminho_origem, os.path.join(pasta_destino, arquivo))
            print(f"Organizado: {arquivo} em {nome_pasta}")

# Uso:
# organizar_por_data("C:/Users/SeuUsuario/Pictures")
