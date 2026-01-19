# Arquivo: organizador_llm.py
"""
Organizador de Arquivos Inteligente

Este script organiza arquivos automaticamente por data com interface moderna.
Funciona como um assistente que pergunta o que fazer e executa de forma segura.

Features:
- Modo simulação automático primeiro
- Interface amigável com emojis
- Backup automático opcional
- Multiplataforma (Windows/Mac/Linux)

Exemplo de uso:
    python organizador_llm.py
    # ou
    from organizador_llm import Organizador
    org = Organizador()
    org.organizar_agora("~/Downloads")
"""

from pathlib import Path
from datetime import datetime
import shutil
from typing import Optional, List, Dict, Any
import sys

class Organizador:
    """Organizador inteligente de arquivos"""
    
    def __init__(self):
        self.estatisticas: Dict[str, int] = {}
        self.emoji_status = {
            "sucesso": "✅",
            "erro": "❌",
            "info": "ℹ️",
            "alerta": "⚠️",
            "arquivo": "📄",
            "pasta": "📁"
        }
    
    def obter_data_arquivo(self, arquivo: Path, criterio: str = "modificacao") -> datetime:
        """Obtém a data do arquivo baseado no critério escolhido"""
        stat = arquivo.stat()
        
        mapeamento_datas = {
            "modificacao": stat.st_mtime,
            "criacao": stat.st_ctime,
            "acesso": stat.st_atime
        }
        
        return datetime.fromtimestamp(mapeamento_datas.get(criterio, stat.st_mtime))
    
    def criar_nome_pasta(self, data: datetime, formato: str = "%Y-%m") -> str:
        """Cria nome da pasta baseado no formato especificado"""
        return data.strftime(formato)
    
    def processar_pasta(self, 
                       caminho: str, 
                       criterio: str = "modificacao",
                       formato: str = "%Y-%m",
                       simular: bool = True,
                       backup: bool = False) -> Dict[str, int]:
        """
        Processa todos os arquivos na pasta especificada
        
        Args:
            caminho: Caminho da pasta
            criterio: "modificacao", "criacao" ou "acesso"
            formato: Formato strftime para nome da pasta
            simular: Se True, apenas mostra ações sem executar
            backup: Se True, cria backup antes de mover
        
        Returns:
            Dicionário com estatísticas da operação
        """
        pasta = Path(caminho).expanduser().resolve()
        
        if not pasta.exists():
            print(f"{self.emoji_status['erro']} Pasta não encontrada: {pasta}")
            return {}
        
        # Inicializar estatísticas
        stats = {
            "arquivos_processados": 0,
            "arquivos_movidos": 0,
            "pastas_criadas": 0,
            "erros": 0,
            "arquivos_ignorados": 0
        }
        
        print(f"\n{self.emoji_status['info']} Processando: {pasta}")
        print(f"{self.emoji_status['info']} Modo: {'Simulação' if simular else 'Execução'}")
        print("-" * 50)
        
        # Criar pasta de backup se necessário
        pasta_backup = None
        if backup and not simular:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta_backup = pasta / f"backup_{timestamp}"
            pasta_backup.mkdir(exist_ok=True)
            print(f"{self.emoji_status['info']} Backup em: {pasta_backup}")
        
        # Processar cada arquivo
        for item in pasta.iterdir():
            try:
                if item.is_file() and not item.is_symlink():
                    stats["arquivos_processados"] += 1
                    
                    # Obter data e nome da pasta
                    data = self.obter_data_arquivo(item, criterio)
                    nome_pasta = self.criar_nome_pasta(data, formato)
                    
                    # Criar pasta de destino
                    pasta_destino = pasta / nome_pasta
                    if not pasta_destino.exists():
                        if not simular:
                            pasta_destino.mkdir(parents=True, exist_ok=True)
                        stats["pastas_criadas"] += 1
                    
                    # Criar backup
                    if backup and not simular and pasta_backup:
                        shutil.copy2(item, pasta_backup / item.name)
                    
                    # Mover arquivo
                    if not simular:
                        # Evitar sobrescrita
                        destino_final = pasta_destino / item.name
                        contador = 1
                        while destino_final.exists():
                            novo_nome = f"{item.stem}_{contador}{item.suffix}"
                            destino_final = pasta_destino / novo_nome
                            contador += 1
                        
                        shutil.move(str(item), str(destino_final))
                        stats["arquivos_movidos"] += 1
                        emoji = "🚀"
                    else:
                        emoji = "👀"
                    
                    # Mostrar progresso
                    print(f"{emoji} {item.name} → {nome_pasta}/")
                    
                else:
                    stats["arquivos_ignorados"] += 1
                    
            except Exception as e:
                stats["erros"] += 1
                print(f"{self.emoji_status['erro']} Erro com {item.name}: {str(e)[:50]}...")
        
        return stats
    
    def mostrar_resumo(self, stats: Dict[str, int], simular: bool):
        """Mostra resumo amigável da operação"""
        print("\n" + "=" * 50)
        print(f"{self.emoji_status['info']} RESULTADO DA {'SIMULAÇÃO' if simular else 'ORGANIZAÇÃO'}")
        print("=" * 50)
        
        if not stats:
            print(f"{self.emoji_status['erro']} Nenhuma estatística disponível")
            return
        
        print(f"{self.emoji_status['arquivo']} Processados: {stats.get('arquivos_processados', 0)}")
        print(f"{self.emoji_status['pasta']} Pastas criadas: {stats.get('pastas_criadas', 0)}")
        print(f"{self.emoji_status['sucesso']} Movidos: {stats.get('arquivos_movidos', 0)}")
        print(f"{self.emoji_status['erro']} Erros: {stats.get('erros', 0)}")
        
        if simular and stats.get('arquivos_processados', 0) > 0:
            print(f"\n{self.emoji_status['alerta']} Modo simulação ativado!")
            print(f"{self.emoji_status['info']} Para executar realmente, use 'simular=False'")

def interface_conversacional():
    """Interface que conversa com o usuário"""
    print("\n" + "🔍" * 25)
    print("🤖 ASSISTENTE DE ORGANIZAÇÃO DE ARQUIVOS")
    print("🔍" * 25)
    
    org = Organizador()
    
    while True:
        print("\n" + "-" * 50)
        print("📂 Qual pasta você gostaria de organizar?")
        print("   (ou digite 'sair' para encerrar)")
        
        caminho = input("👉 ").strip()
        
        if caminho.lower() in ['sair', 'exit', 'quit', 'q']:
            print(f"\n{org.emoji_status['info']} Até logo! 👋")
            break
        
        if not caminho:
            print(f"{org.emoji_status['alerta']} Por favor, digite um caminho válido")
            continue
        
        # Verificar caminho
        try:
            pasta = Path(caminho).expanduser()
            if not pasta.exists():
                print(f"{org.emoji_status['erro']} Esta pasta não existe: {pasta}")
                continue
        except Exception as e:
            print(f"{org.emoji_status['erro']} Caminho inválido: {e}")
            continue
        
        # Perguntar critério
        print("\n📅 Como devo organizar os arquivos?")
        print("   1. Por data de modificação (padrão)")
        print("   2. Por data de criação")
        print("   3. Por data de acesso")
        
        opcao = input("👉 Escolha (1-3) [1]: ").strip() or "1"
        criterios = {"1": "modificacao", "2": "criacao", "3": "acesso"}
        criterio = criterios.get(opcao, "modificacao")
        
        # Perguntar formato
        print("\n🗂️  Qual formato de pasta você prefere?")
        print("   1. Ano-Mês (2024-01)")
        print("   2. Ano (2024)")
        print("   3. Ano-Mês-Dia (2024-01-15)")
        
        formato_opcao = input("👉 Escolha (1-3) [1]: ").strip() or "1"
        formatos = {"1": "%Y-%m", "2": "%Y", "3": "%Y-%m-%d"}
        formato = formatos.get(formato_opcao, "%Y-%m")
        
        # Primeiro, simular
        print(f"\n{org.emoji_status['info']} Vou mostrar o que será feito...")
        print("-" * 50)
        
        stats = org.processar_pasta(
            caminho=caminho,
            criterio=criterio,
            formato=formato,
            simular=True,
            backup=False
        )
        
        org.mostrar_resumo(stats, simular=True)
        
        # Perguntar se quer executar
        if stats.get('arquivos_processados', 0) > 0:
            print("\n" + "=" * 50)
            resposta = input("👉 Deseja executar a organização? (s/n): ").strip().lower()
            
            if resposta == 's':
                backup_resp = input("👉 Criar backup antes? (s/n): ").strip().lower()
                
                print(f"\n{org.emoji_status['info']} Executando organização...")
                print("-" * 50)
                
                stats_real = org.processar_pasta(
                    caminho=caminho,
                    criterio=criterio,
                    formato=formato,
                    simular=False,
                    backup=(backup_resp == 's')
                )
                
                org.mostrar_resumo(stats_real, simular=False)
                
                print(f"\n{org.emoji_status['sucesso']} Organização concluída com sucesso!")
            else:
                print(f"\n{org.emoji_status['info']} Operação cancelada")
        
        # Perguntar se quer continuar
        continuar = input("\n👉 Organizar outra pasta? (s/n): ").strip().lower()
        if continuar != 's':
            print(f"\n{org.emoji_status['info']} Até a próxima! 👋")
            break

def modo_rapido():
    """Modo rápido para uso via linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Organiza arquivos por data de forma inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s ~/Downloads                      # Organiza Downloads
  %(prog)s ~/Pictures --criterio criacao    # Por data de criação
  %(prog)s ~/Desktop --simular              # Apenas simula
  %(prog)s --interativo                     # Modo conversacional
        """
    )
    
    parser.add_argument(
        "pasta",
        nargs="?",
        help="Pasta a ser organizada (opcional no modo interativo)"
    )
    
    parser.add_argument(
        "--criterio", "-c",
        choices=["modificacao", "criacao", "acesso"],
        default="modificacao",
        help="Critério de data (padrão: modificacao)"
    )
    
    parser.add_argument(
        "--formato", "-f",
        default="%Y-%m",
        help="Formato da pasta (strftime, padrão: %%Y-%%m)"
    )
    
    parser.add_argument(
        "--simular", "-s",
        action="store_true",
        help="Apenas simular sem alterar arquivos"
    )
    
    parser.add_argument(
        "--backup", "-b",
        action="store_true",
        help="Criar backup antes de organizar"
    )
    
    parser.add_argument(
        "--interativo", "-i",
        action="store_true",
        help="Modo interativo conversacional"
    )
    
    args = parser.parse_args()
    
    org = Organizador()
    
    if args.interativo or not args.pasta:
        interface_conversacional()
    else:
        stats = org.processar_pasta(
            caminho=args.pasta,
            criterio=args.criterio,
            formato=args.formato,
            simular=args.simular,
            backup=args.backup
        )
        
        org.mostrar_resumo(stats, simular=args.simular)

# Funções de conveniência para uso rápido
def organizar_agora(pasta: str, **kwargs):
    """Função de conveniência para organização rápida"""
    org = Organizador()
    return org.processar_pasta(pasta, **kwargs)

def simular_organizacao(pasta: str, **kwargs):
    """Apenas simula a organização"""
    org = Organizador()
    return org.processar_pasta(pasta, simular=True, **kwargs)

# Exemplo de uso como módulo
if __name__ == "__main__":
    # Se não houver argumentos, usar interface conversacional
    if len(sys.argv) == 1:
        interface_conversacional()
    else:
        modo_rapido()

# Sugestão de uso no README virtual:
"""
📚 COMO USAR:

1. Modo interativo (recomendado):
   python organizador_llm.py
   # ou
   python organizador_llm.py --interativo

2. Modo rápido:
   python organizador_llm.py ~/Downloads
   python organizador_llm.py ~/Pictures --criterio criacao --backup

3. Como módulo Python:
   from organizador_llm import Organizador, organizar_agora
   
   # Opção 1: Com classe
   org = Organizador()
   org.processar_pasta("~/Downloads", simular=True)
   
   # Opção 2: Função rápida
   organizar_agora("~/Downloads", criterio="criacao", backup=True)
"""

# Documentação adicional
__all__ = ['Organizador', 'organizar_agora', 'simular_organizacao', 'interface_conversacional']
__version__ = "1.0.0"
__author__ = "Assistente de Organização"
__description__ = "Organizador inteligente de arquivos com interface conversacional"
