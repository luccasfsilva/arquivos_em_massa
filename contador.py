import os

def listar_pastas(caminho):
    """Retorna lista de subpastas (nomes) dentro do caminho, ignorando arquivos."""
    try:
        itens = sorted(os.listdir(caminho))
    except PermissionError:
        print("🔒 Sem permissão para acessar essa pasta.")
        return []
    except Exception as e:
        print(f"❌ Erro ao acessar a pasta: {e}")
        return []

    pastas = [item for item in itens if os.path.isdir(os.path.join(caminho, item))]
    return pastas


def contar_arquivos(caminho):
    """Conta arquivos (não-pastas) dentro do caminho informado."""
    try:
        itens = os.listdir(caminho)
    except PermissionError:
        print("🔒 Sem permissão para acessar essa pasta.")
        return None
    except Exception as e:
        print(f"❌ Erro ao acessar a pasta: {e}")
        return None

    arquivos = [item for item in itens if os.path.isfile(os.path.join(caminho, item))]
    return arquivos


def escolher_subpasta(caminho_atual):
    """
    Mostra as subpastas do caminho atual e deixa o usuário escolher uma,
    voltar, ou contar os arquivos da pasta atual.
    Retorna:
      - ('entrar', nome_da_pasta_escolhida)
      - ('contar', None)  -> usuário quer contar arquivos do caminho_atual
      - ('voltar', None)  -> usuário quer subir um nível
      - ('sair', None)    -> usuário quer encerrar
    """
    pastas = listar_pastas(caminho_atual)
    arquivos = contar_arquivos(caminho_atual)
    qtd_arquivos = len(arquivos) if arquivos is not None else 0

    print("\n" + "─" * 60)
    print(f"📂 Você está em: {caminho_atual}")
    print(f"   ({qtd_arquivos} arquivo(s) direto nesta pasta, {len(pastas)} subpasta(s))")
    print("─" * 60)

    if not pastas:
        print("   (Não há subpastas aqui — apenas arquivos, se houver)")
    else:
        for i, pasta in enumerate(pastas, 1):
            print(f"   {i}. 📁 {pasta}")

    print("\n   [C] Contar arquivos DESTA pasta (a que você está vendo agora)")
    print("   [V] Voltar um nível")
    print("   [S] Sair do programa")

    escolha = input("\n➡️  Escolha um número, ou C / V / S: ").strip().upper()

    if escolha == "S":
        return ("sair", None)
    if escolha == "V":
        return ("voltar", None)
    if escolha == "C":
        return ("contar", None)

    if escolha.isdigit():
        idx = int(escolha)
        if 1 <= idx <= len(pastas):
            return ("entrar", pastas[idx - 1])

    print("❌ Opção inválida, tente novamente.")
    return escolher_subpasta(caminho_atual)


def navegar_e_contar():
    print("=" * 70)
    print("📁 CONTADOR DE ARQUIVOS - MODO NAVEGAÇÃO")
    print("=" * 70)
    print("Você vai navegar pasta por pasta até achar a que quer contar.\n")

    caminho_base = input("📍 Digite o caminho completo da pasta principal: ").strip()

    if not os.path.exists(caminho_base):
        print(f"\n❌ ERRO: Caminho não encontrado: {caminho_base}")
        return

    if not os.path.isdir(caminho_base):
        print(f"\n❌ ERRO: O caminho informado não é uma pasta: {caminho_base}")
        return

    pilha_caminhos = [caminho_base]  # histórico para permitir "voltar"

    while True:
        caminho_atual = pilha_caminhos[-1]
        acao, valor = escolher_subpasta(caminho_atual)

        if acao == "sair":
            print("\n👋 Encerrando o programa. Até mais!")
            return

        elif acao == "voltar":
            if len(pilha_caminhos) > 1:
                pilha_caminhos.pop()
            else:
                print("⚠️  Você já está na pasta principal, não é possível voltar mais.")

        elif acao == "entrar":
            novo_caminho = os.path.join(caminho_atual, valor)
            pilha_caminhos.append(novo_caminho)

        elif acao == "contar":
            arquivos = contar_arquivos(caminho_atual)
            if arquivos is None:
                continue

            qtd = len(arquivos)
            print("\n" + "═" * 60)
            print(f"📊 RESULTADO DA CONTAGEM")
            print("═" * 60)
            print(f"📂 Pasta contada : {caminho_atual}")
            print(f"📄 Total de arquivos: {qtd}")
            print("═" * 60)

            if qtd > 0:
                ver_lista = input("\n👀 Quer ver a lista dos arquivos? (S/N): ").strip().upper()
                if ver_lista == "S":
                    for nome_arquivo in sorted(arquivos):
                        print(f"   • {nome_arquivo}")

            # Pergunta se quer continuar contando outras pastas
            print("\n" + "─" * 60)
            continuar = input("➡️  Quer contar outra pasta agora? (S/N): ").strip().upper()
            if continuar != "S":
                print("\n👋 Encerrando o programa. Até mais!")
                return
            # Se quiser continuar, simplesmente volta ao loop
            # mantendo a posição atual na árvore de pastas


if __name__ == "__main__":
    try:
        navegar_e_contar()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário.")

    input("\nPressione ENTER para sair...")
