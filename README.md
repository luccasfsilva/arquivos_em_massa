# Gerenciador de Arquivos CLI 🗂️

Um programa simples em Python para gerenciar arquivos de texto via linha de comando com sistema de menu interativo.

## Funcionalidades ✨

- ✅ Criar novos arquivos
- ✅ Adicionar linhas com formatação automática
- ✅ Visualizar conteúdo de arquivos
- ✅ Interface amigável com menu
- ✅ Validação de entradas

## Como Usar 🚀

### Pré-requisitos
- Python 3.x instalado

### Execução


```bash
https://github.com/luccasfsilva/pythonRAD

# Acesse o diretório
cd file-manager-cli

# Execute o programa
python file_manager.py
```

### Exemplo de Uso
```
Menu:
1. Criar um arquivo
2. Acrescentar linhas ao arquivo
3. Mostrar o conteudo do arquivo
0. Sair

Opcao: 1
Informe o nome do arquivo: [arquivo.txt]

Opcao: 2
Digite as linhas a serem acrescentadas (0 para parar):
> exemplo de linha
> OUTRA LINHA
> 0

Opcao: 3
Exemplo de linha
Outra linha
```

## Formatação Automática 🔠
Todas as linhas são automaticamente convertidas para:
- Primeira letra maiúscula
- Demais caracteres minúsculos

Exemplo de conversão:
```
Entrada: "ESTA É UMA LINHA"
Saída: "Esta é uma linha"
```

