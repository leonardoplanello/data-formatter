import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from pathlib import Path

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo",
        filetypes=[("Todos os arquivos", "*.*")]
    )
    if caminho_arquivo:
        try:
            conteudo = ler_arquivo_com_codificacoes(caminho_arquivo)
            if conteudo is None:
                raise UnicodeDecodeError("Nenhuma codificação suportada foi capaz de ler o arquivo.")

            dados_json = {
                "path": caminho_arquivo,
                "content": conteudo
            }

            # Obter o caminho da pasta Documents
            documentos = Path.home() / "Documents"
            if not documentos.exists():
                # Caso a pasta Documents não exista, use o diretório home
                documentos = Path.home()

            # Nome do arquivo JSON
            nome_arquivo = Path(caminho_arquivo).stem + ".json"
            caminho_json = documentos / nome_arquivo

            # Salvar o JSON na pasta Documents
            with open(caminho_json, 'w', encoding='utf-8') as json_file:
                json.dump(dados_json, json_file, indent=4, ensure_ascii=False)

            messagebox.showinfo("Sucesso", f"Arquivo JSON salvo em:\n{caminho_json}")

        except UnicodeDecodeError as ude:
            messagebox.showerror("Erro de Decodificação", f"Não foi possível decodificar o arquivo com as codificações tentadas.\nDetalhes: {ude}")
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
    # Se nenhuma codificação funcionar, tentar ler com 'utf-8' substituindo erros
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', errors='replace') as arquivo:
            return arquivo.read()
    except Exception:
        return None

def criar_interface():
    # Configuração da janela principal
    janela = tk.Tk()
    janela.title("Conversor de Arquivo para JSON")
    janela.geometry("500x250")
    janela.resizable(False, False)

    # Ícone (opcional)
    # Você pode adicionar um ícone personalizado se desejar
    # janela.iconbitmap('caminho_para_seu_icone.ico')

    # Texto de instrução
    label = tk.Label(
        janela,
        text="Clique no botão abaixo para selecionar um arquivo e convertê-lo em JSON.",
        wraplength=480,
        justify="center",
        font=("Arial", 12)
    )
    label.pack(pady=30)

    # Botão para selecionar o arquivo
    botao = tk.Button(
        janela,
        text="Selecionar Arquivo",
        command=selecionar_arquivo,
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
        text="© 2025 Seu Nome ou Empresa",
        font=("Arial", 8),
        fg="grey"
    )
    rodape.pack(side="bottom", pady=10)

    # Iniciar o loop da interface
    janela.mainloop()

if __name__ == "__main__":
    criar_interface()
