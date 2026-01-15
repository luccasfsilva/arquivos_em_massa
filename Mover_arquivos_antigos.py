import os
import shutil
import time

def arquivar_antigos(caminho_pasta, dias=30):
    pasta_destino = os.path.join(caminho_pasta, "Arquivo_Morto")
    os.makedirs(pasta_destino, exist_ok=True)
    
    segundos_limite = dias * 24 * 60 * 60
    tempo_atual = time.time()

    for arquivo in os.listdir(caminho_pasta):
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        
        if os.path.isfile(caminho_arquivo):
            tempo_arquivo = os.path.getatime(caminho_arquivo) # Data do último acesso
            
            if (tempo_atual - tempo_arquivo) > segundos_limite:
                shutil.move(caminho_arquivo, os.path.join(pasta_destino, arquivo))
                print(f"Arquivado por inatividade: {arquivo}")

# Uso:
# arquivar_antigos("C:/Users/SeuUsuario/Desktop", dias=15)
