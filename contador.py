import os

def contar_arquivos_pasta():
    """Versão simples que mostra os resultados no próprio terminal."""
    
    print("=" * 70)
    print("📁 CONTADOR DE ARQUIVOS POR PASTA")
    print("=" * 70)
    
    # Pede o caminho da pasta principal
    caminho_base = input("📍 Digite o caminho completo da pasta principal: ").strip()
    
    # Verifica se o caminho existe
    if not os.path.exists(caminho_base):
        print(f"\n❌ ERRO: Caminho não encontrado: {caminho_base}")
        return
    
    print(f"\n🔍 Analisando pasta: {caminho_base}")
    print("⏳ Aguarde um momento...\n")
    
    # Lista de pastas baseada na sua tabela
    pastas = [
        "01-Acidente de trabalho", "02-Acidente Animal Peçonhoto", "03-Anti-Rabico Humano",
        "04-Catapora", "05-Caxumba", "06-Chikungunya", "07-Coqueluche", "08-COVID",
        "09-Dengue", "10-Febre Amarela", "11-Febre Maculosa", "12-Hepatites", "13-HIV",
        "14-Influenza", "15-Intoxicação Exógena", "16-Leptospirose", "17-Malaria",
        "18-Meningite", "19-MPOX", "20-Oropouche", "21-Sífilis", "22-Tuberculose",
        "23-Violência", "24-Zika", "25-SRAG", "26-VSR (Internado)", "27-Sarampo",
        "28-Diarreia", "29-Reação Vacinal", "30-Toxoplasmose Gestacional",
        "31-Tentativa de Suicídio", "32-Toxoplasmose Congênita", "33-Monitoramento",
        "34-Adenovírus", "35-Esporotricose"
    ]
    
    # Cabeçalho da tabela
    print("═" * 60)
    print(f"{'Nº':<4} {'Pasta':<30} {'Arquivos':<10} {'Status':<12}")
    print("═" * 60)
    
    total_geral = 0
    encontradas = 0
    
    # Conta arquivos em cada pasta
    for i, pasta in enumerate(pastas, 1):
        caminho_completo = os.path.join(caminho_base, pasta)
        
        if os.path.exists(caminho_completo) and os.path.isdir(caminho_completo):
            encontradas += 1
            try:
                # Lista e conta arquivos
                itens = os.listdir(caminho_completo)
                arquivos = [item for item in itens if os.path.isfile(os.path.join(caminho_completo, item))]
                qtd = len(arquivos)
                total_geral += qtd
                
                # Formata o status com cores
                if qtd == 0:
                    status = "🔴 VAZIA"
                elif qtd < 10:
                    status = f"🟡 {qtd}"
                else:
                    status = f"🟢 {qtd}"
                
                # Formata o nome da pasta se for muito longo
                nome_exibicao = pasta
                if len(pasta) > 28:
                    nome_exibicao = pasta[:25] + "..."
                
                print(f"{i:<4} {nome_exibicao:<30} {qtd:<10} {status:<12}")
                
            except PermissionError:
                print(f"{i:<4} {pasta:<30} {'0':<10} 🔒 BLOQUEADO")
            except Exception as e:
                print(f"{i:<4} {pasta:<30} {'0':<10} ❌ ERRO")
        else:
            # Pasta não encontrada
            nome_exibicao = pasta
            if len(pasta) > 28:
                nome_exibicao = pasta[:25] + "..."
            print(f"{i:<4} {nome_exibicao:<30} {'0':<10} ❌ AUSENTE")
    
    print("═" * 60)
    
    # Estatísticas finais
    print(f"\n📊 RESUMO FINAL:")
    print(f"   • Total de pastas analisadas: {len(pastas)}")
    print(f"   • Pastas encontradas no sistema: {encontradas}")
    print(f"   • Pastas não encontradas: {len(pastas) - encontradas}")
    print(f"   • Total geral de arquivos: {total_geral}")
    
    # Pergunta se quer exportar
    print("\n" + "═" * 60)
    exportar = input("💾 Deseja salvar estes resultados em um arquivo? (S/N): ").strip().upper()
    
    if exportar == 'S':
        nome_arquivo = "contagem_arquivos.txt"
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("RELATÓRIO DE CONTAGEM DE ARQUIVOS\n")
                f.write("=" * 60 + "\n")
                f.write(f"Data: {os.path.basename(__file__)}\n")
                f.write(f"Caminho analisado: {caminho_base}\n\n")
                
                for i, pasta in enumerate(pastas, 1):
                    caminho_completo = os.path.join(caminho_base, pasta)
                    qtd = 0
                    if os.path.exists(caminho_completo):
                        try:
                            itens = os.listdir(caminho_completo)
                            qtd = len([item for item in itens if os.path.isfile(os.path.join(caminho_completo, item))])
                        except:
                            pass
                    f.write(f"{pasta}: {qtd} arquivos\n")
                
                f.write(f"\nTotal geral: {total_geral} arquivos\n")
            
            print(f"\n✅ Relatório salvo como: {nome_arquivo}")
            
            # Tenta abrir o arquivo (Windows)
            try:
                abrir = input("   Deseja abrir o arquivo agora? (S/N): ").strip().upper()
                if abrir == 'S':
                    os.startfile(nome_arquivo)
            except:
                pass
                
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {e}")

# Versão SUPER SIMPLES - apenas pede caminho e mostra contagem
def versao_ultra_simples():
    """Versão ultra simples sem formatação complexa."""
    
    print("\n" + "=" * 50)
    print("CONTADOR SUPER SIMPLES DE ARQUIVOS")
    print("=" * 50)
    
    caminho = input("Caminho da pasta: ").strip()
    
    if not os.path.exists(caminho):
        print("❌ Pasta não encontrada!")
        return
    
    print("\n📁 CONTANDO...")
    print("-" * 50)
    
    total_arquivos = 0
    total_pastas = 0
    pastas_vazias = 0
    pastas_com_arquivos = 0
    
    # Lista todas as pastas e conta
    try:
        for item in os.listdir(caminho):
            item_path = os.path.join(caminho, item)
            if os.path.isdir(item_path):
                total_pastas += 1
                try:
                    arquivos = [f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))]
                    qtd = len(arquivos)
                    total_arquivos += qtd
                    
                    # Conta pastas vazias e com arquivos
                    if qtd == 0:
                        pastas_vazias += 1
                        print(f"📂 {item}: {qtd} arquivos")
                    else:
                        pastas_com_arquivos += 1
                        print(f"📁 {item}: {qtd} arquivos")
                        
                except PermissionError:
                    print(f"🔒 {item}: PERMISSÃO NEGADA")
                    total_pastas += 0  # Já contamos acima
                except Exception as e:
                    print(f"❌ {item}: ERRO ({str(e)[:30]})")
                    total_pastas += 0  # Já contamos acima
    
    except Exception as e:
        print(f"Erro ao acessar a pasta principal: {e}")
        return
    
    print("-" * 50)
    print(f"📊 RESUMO:")
    print(f"   • Pastas encontradas: {total_pastas}")
    print(f"   • Pastas com arquivos: {pastas_com_arquivos}")
    print(f"   • Pastas vazias: {pastas_vazias}")
    print(f"   • Total de arquivos: {total_arquivos}")
    print(f"   • Média por pasta: {total_arquivos/total_pastas:.1f}" if total_pastas > 0 else "   • Média por pasta: 0")
    print("-" * 50)

# Menu principal
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("ESCOLHA UMA OPÇÃO:")
    print("=" * 50)
    print("1. 📊 Contagem completa (com todas as 35 pastas)")
    print("2. ⚡ Contagem super rápida (todas as pastas encontradas)")
    print("3. 🔢 Contar apenas em UMA pasta específica")
    print("=" * 50)
    
    opcao = input("Digite sua opção (1, 2 ou 3): ").strip()
    
    if opcao == "1":
        contar_arquivos_pasta()
    elif opcao == "2":
        versao_ultra_simples()
    elif opcao == "3":
        # Contar apenas em uma pasta específica
        caminho_unico = input("\n📍 Digite o caminho completo de UMA pasta: ").strip()
        if os.path.exists(caminho_unico) and os.path.isdir(caminho_unico):
            arquivos = [f for f in os.listdir(caminho_unico) if os.path.isfile(os.path.join(caminho_unico, f))]
            print(f"\n📊 RESULTADO: {len(arquivos)} arquivos na pasta")
            print(f"📁 Pasta: {os.path.basename(caminho_unico)}")
        else:
            print("❌ Pasta inválida ou não encontrada!")
    else:
        print("❌ Opção inválida!")
    
    # Mantém o terminal aberto
    input("\nPressione ENTER para sair...")
