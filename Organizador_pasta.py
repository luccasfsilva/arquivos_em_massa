import os
import shutil

def organizar_por_extensao(caminho_pasta):
    # Mapeamento de pastas e suas extensões
    formatos = {
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Audio_Video": [".mp3", ".wav", ".mp4", ".mkv", ".mov"],
        "Executaveis_Zips": [".exe", ".msi", ".zip", ".rar", ".7z"]
    }

    for arquivo in os.listdir(caminho_pasta):
        nome, ext = os.path.splitext(arquivo)
        caminho_origem = os.path.join(caminho_pasta, arquivo)
        
        # Ignora se for uma pasta
        if os.path.isdir(caminho_origem):
            continue

        for pasta, extensoes in formatos.items():
            if ext.lower() in extensoes:
                pasta_destino = os.path.join(caminho_pasta, pasta)
                os.makedirs(pasta_destino, exist_ok=True)
                shutil.move(caminho_origem, os.path.join(pasta_destino, arquivo))
                print(f"Movido: {arquivo} -> {pasta}")

# Uso:
# organizar_por_extensao("C:/Users/SeuUsuario/Downloads")
