import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from pathlib import Path

def selecionar_pasta():
    caminho_pasta = filedialog.askdirectory(
        title="Selecione a pasta"
    )
    if caminho_pasta:
        try:
            dados_json = []
            arquivos_processados = 0
            arquivos_ignorados = 0

            for raiz, dirs, arquivos in os.walk(caminho_pasta):
                for arquivo in arquivos:
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    conteudo = ler_arquivo_com_codificacoes(caminho_arquivo)
                    
                    if conteudo is not None:
                        dados_json.append({
                            "path": caminho_arquivo,
                            "content": conteudo
                        })
                        arquivos_processados += 1
                    else:
                        arquivos_ignorados += 1

            if dados_json:
                # Obter o caminho da pasta Documents
                documentos = Path.home() / "Documents"
                if not documentos.exists():
                    # Caso a pasta Documents não exista, use o diretório home
                    documentos = Path.home()

                # Nome do arquivo JSON
                nome_arquivo = "dados_pasta.json"
                caminho_json = documentos / nome_arquivo

                # Salvar o JSON na pasta Documents
                with open(caminho_json, 'w', encoding='utf-8') as json_file:
                    json.dump(dados_json, json_file, indent=4, ensure_ascii=False)

                mensagem = f"Arquivo JSON salvo em:\n{caminho_json}\n\nArquivos processados: {arquivos_processados}"
                if arquivos_ignorados > 0:
                    mensagem += f"\nArquivos ignorados (não de texto ou leitura falhou): {arquivos_ignorados}"
                
                messagebox.showinfo("Sucesso", mensagem)
            else:
                messagebox.showwarning("Nenhum Arquivo", "Nenhum arquivo de texto foi encontrado ou todos os arquivos falharam na leitura.")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

def ler_arquivo_com_codificacoes(caminho_arquivo):
    """
    Tenta ler o arquivo com várias codificações comuns.
    Retorna o conteúdo do arquivo como string se bem-sucedido, ou None caso contrário.
    """
    codificacoes = ['utf-8', 'latin1', 'cp1252']
    for codificacao in codificacoes:
        try:
            with open(caminho_arquivo, 'r', encoding=codificacao) as arquivo:
                return arquivo.read()
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    # Se nenhuma codificação funcionar, tentar ler com 'utf-8' substituindo erros
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', errors='replace') as arquivo:
            return arquivo.read()
    except Exception:
        return None

def criar_interface():
    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("Conversor de Pasta para JSON")
    janela.geometry("600x300")
    janela.resizable(False, False)

    # Ícone (opcional)
    # Você pode adicionar um ícone personalizado se desejar
    # janela.iconbitmap('caminho_para_seu_icone.ico')

    # Texto de instrução
    label = tk.Label(
        janela,
        text="Clique no botão abaixo para selecionar uma pasta e convertê-la em JSON.\nTodos os arquivos de texto dentro da pasta serão incluídos na íntegra.",
        wraplength=580,
        justify="center",
        font=("Arial", 12)
    )
    label.pack(pady=50)

    # Botão para selecionar a pasta
    botao = tk.Button(
        janela,
        text="Selecionar Pasta",
        command=selecionar_pasta,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12),
        activebackground="#45a049"
    )
    botao.pack()

    # Rodapé ou Informações Adicionais (opcional)
    rodape = tk.Label(
        janela,
        text="© 2025 - Leonardo Planello",
        font=("Arial", 8),
        fg="grey"
    )
    rodape.pack(side="bottom", pady=10)

    # Iniciar o loop da interface
    janela.mainloop()

if __name__ == "__main__":
    criar_interface()
