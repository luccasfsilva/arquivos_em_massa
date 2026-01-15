import os

filename = 'arquivo.txt'

while True:
    print("\nMenu:")
    print("1. Criar um arquivo")
    print("2. Acrescentar linhas ao arquivo")
    print("3. Mostrar o conteudo do arquivo")
    print("0. Sair")
    opcao = input("Opcao: ").strip()

    if opcao == '1':
        new_name = input("Informe o nome do arquivo: ").strip()
        if not new_name:
            new_name = 'arquivo.txt'
        filename = new_name
        with open(filename, 'w') as arquivo:
            pass
        print(f"Arquivo '{filename}' criado.")
    elif opcao == '2':
        file_is_empty = not os.path.exists(filename) or os.path.getsize(filename) == 0
        print("Digite as linhas a serem acrescentadas (0 para parar):")
        with open(filename, 'a') as arquivo:
            first_line = True
            while True:
                linha = input("> ").strip()
                if linha == '0':
                    break
                processada = linha.lower().capitalize()
                if first_line:
                    if file_is_empty:
                        arquivo.write(processada)
                    else:
                        arquivo.write('\n' + processada)
                    first_line = False
                else:
                    arquivo.write('\n' + processada)
        print("Linhas adicionadas com sucesso.")
    elif opcao == '3':
        try:
            with open(filename, 'r') as arquivo:
                conteudo = arquivo.read()
                if conteudo:
                    print(conteudo)
                else:
                    print("O arquivo está vazio.")
        except FileNotFoundError:
            print("Arquivo não encontrado.")
    elif opcao == '0':
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")
