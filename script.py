import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import csv
import tempfile
import platform
from pathlib import Path

###############################################################################
# Textos por idioma
###############################################################################
LANG_TEXTS = {
    "en": {
        "title": "Folder Converter",
        "lang_select": "Select your language:",
        "next": "Next >>",
        "mode_select": "Choose Mode:",
        "structure": "Structure",
        "content": "Content",
        "file_select": "Select how you want to pick files/folders:",
        "choose_folder": "Choose Entire Folder",
        "choose_files": "Select Multiple Files",
        "placeholder_manual": "Or type the directories of files/folders here",
        "format_select": "Choose Output Format:",
        "processing": "Processing... Please wait.",
        "logs": "Logs:",
        "done": "Done!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "Files processed: ",
        "ignored_files": "Files ignored: ",
        "saved_in": "File saved in:\n",
        "back": "<-- Back",
        "ok": "Ok",
        "manual_ok": "OK"
    },
    "pt_BR": {
        "title": "Folder Converter",
        "lang_select": "Selecione seu idioma:",
        "next": "Próximo >>",
        "mode_select": "Escolha o Modo:",
        "structure": "Estrutura",
        "content": "Conteúdo",
        "file_select": "Selecione como deseja escolher os arquivos/pastas:",
        "choose_folder": "Escolher Pasta Inteira",
        "choose_files": "Selecionar Múltiplos Arquivos",
        "placeholder_manual": "Ou escreva o diretorio dos arquivos e pastas aqui",
        "format_select": "Escolha o Formato de Saída:",
        "processing": "Processando... Por favor, aguarde.",
        "logs": "Logs:",
        "done": "Concluído!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "Arquivos processados: ",
        "ignored_files": "Arquivos ignorados: ",
        "saved_in": "Arquivo salvo em:\n",
        "back": "<-- Voltar",
        "ok": "Ok",
        "manual_ok": "OK"
    },
    "es": {
        "title": "Folder Converter",
        "lang_select": "Selecciona tu idioma:",
        "next": "Siguiente >>",
        "mode_select": "Elige el Modo:",
        "structure": "Estructura",
        "content": "Contenido",
        "file_select": "Selecciona cómo quieres elegir los archivos/carpetas:",
        "choose_folder": "Elegir Carpeta Entera",
        "choose_files": "Seleccionar Múltiples Archivos",
        "placeholder_manual": "O escribe aquí la ruta de los archivos y carpetas",
        "format_select": "Elige el Formato de Salida:",
        "processing": "Procesando... Por favor, espera.",
        "logs": "Registros:",
        "done": "¡Hecho!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "Archivos procesados: ",
        "ignored_files": "Archivos ignorados: ",
        "saved_in": "Archivo guardado en:\n",
        "back": "<-- Atrás",
        "ok": "Ok",
        "manual_ok": "OK"
    },
    "ru": {
        "title": "Folder Converter",
        "lang_select": "Выберите язык:",
        "next": "Далее >>",
        "mode_select": "Выберите режим:",
        "structure": "Структура",
        "content": "Содержимое",
        "file_select": "Выберите способ выбора файлов/папок:",
        "choose_folder": "Выбрать целую папку",
        "choose_files": "Выбрать несколько файлов",
        "placeholder_manual": "Или введите пути к файлам/папкам здесь",
        "format_select": "Выберите формат вывода:",
        "processing": "Обработка... Пожалуйста, подождите.",
        "logs": "Логи:",
        "done": "Готово!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "Файлы обработаны: ",
        "ignored_files": "Файлы пропущены: ",
        "saved_in": "Файл сохранен в:\n",
        "back": "<-- Назад",
        "ok": "Ok",
        "manual_ok": "OK"
    },
    "it": {
        "title": "Folder Converter",
        "lang_select": "Seleziona la tua lingua:",
        "next": "Avanti >>",
        "mode_select": "Scegli la Modalità:",
        "structure": "Struttura",
        "content": "Contenuto",
        "file_select": "Seleziona come scegliere i file/cartelle:",
        "choose_folder": "Scegli l'intera cartella",
        "choose_files": "Seleziona più file",
        "placeholder_manual": "Oppure scrivi qui i percorsi di file/cartelle",
        "format_select": "Scegli il formato di output:",
        "processing": "Elaborazione... Attendere prego.",
        "logs": "Log:",
        "done": "Fatto!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "File elaborati: ",
        "ignored_files": "File ignorati: ",
        "saved_in": "File salvato in:\n",
        "back": "<-- Indietro",
        "ok": "Ok",
        "manual_ok": "OK"
    },
    "zh": {
        "title": "Folder Converter",
        "lang_select": "选择语言：",
        "next": "下一步 >>",
        "mode_select": "选择模式：",
        "structure": "结构",
        "content": "内容",
        "file_select": "选择如何选取文件/文件夹：",
        "choose_folder": "选择整个文件夹",
        "choose_files": "选择多个文件",
        "placeholder_manual": "或者在这里输入文件/文件夹路径",
        "format_select": "选择输出格式：",
        "processing": "处理中...请等待。",
        "logs": "日志:",
        "done": "完成!",
        "json": "JSON",
        "txt": "TXT",
        "csv": "CSV",
        "success_files": "已处理的文件数: ",
        "ignored_files": "已忽略的文件数: ",
        "saved_in": "文件保存于:\n",
        "back": "<-- 返回",
        "ok": "Ok",
        "manual_ok": "OK"
    }
}

###############################################################################
# Extensões de imagens
###############################################################################
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".webp", ".svg", ".heic", ".heif", ".ico", ".raw"
}

###############################################################################
# Funções de leitura e salvamento
###############################################################################
def ler_arquivo_com_codificacoes(caminho_arquivo):
    codificacoes = ['utf-8', 'latin1', 'cp1252']
    for codificacao in codificacoes:
        try:
            with open(caminho_arquivo, 'r', encoding=codificacao) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    # fallback: utf-8 + replace
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception:
        return None

def get_folder_structure_win(folder_path):
    """
    Executa 'tree /f /a folder_path' e retorna a string.
    Somente no Windows.
    """
    import tempfile
    if platform.system().lower() != "windows":
        return "ERROR: 'tree' command only supported on Windows."
    temp_file = os.path.join(tempfile.gettempdir(), "temp_tree.txt")
    cmd = f'tree /f /a "{folder_path}" > "{temp_file}"'
    os.system(cmd)
    try:
        with open(temp_file, 'r', encoding='utf-8', errors='replace') as f:
            structure = f.read()
        return structure
    except:
        return "ERROR reading tree output."

def salvar_como_json(dados, caminho):
    with open(caminho, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, indent=4, ensure_ascii=False)

def salvar_como_txt(dados, caminho):
    conteudo_final = []
    for item in dados:
        bloco = []
        bloco.append("---")
        bloco.append("path:")
        bloco.append(f"\"{item['path']}\",")
        bloco.append("")
        bloco.append("content:")
        bloco.append(item['content'])
        bloco.append("")
        conteudo_final.append("\n".join(bloco))

    resultado_txt = "\n".join(conteudo_final)
    with open(caminho, 'w', encoding='utf-8') as txt_file:
        txt_file.write(resultado_txt)

def salvar_como_csv(dados, caminho):
    with open(caminho, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["path", "content"])
        for item in dados:
            writer.writerow([item["path"], item["content"]])

###############################################################################
# Classe Principal
###############################################################################
class FolderConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Folder Converter")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg="black")

        # Estados
        self.idioma_selecionado = tk.StringVar(value="en")
        self.modo_selecionado   = tk.StringVar(value="content")  # structure|content
        self.formato_selecionado= tk.StringVar(value="json")     # json|txt|csv

        # Vamos armazenar múltiplos caminhos (arquivos ou pastas)
        self.caminhos_entrada = []

        # Atualiza UI quando idioma muda
        self.idioma_selecionado.trace_add("write", self._atualizar_textos_idioma)

        # Frames (telas)
        self.frame_idioma      = tk.Frame(self, bg="black")
        self.frame_modo        = tk.Frame(self, bg="black")
        self.frame_file_select = tk.Frame(self, bg="black")
        self.frame_formato     = tk.Frame(self, bg="black")
        self.frame_logs        = tk.Frame(self, bg="black")

        for f in (
            self.frame_idioma,
            self.frame_modo,
            self.frame_file_select,
            self.frame_formato,
            self.frame_logs
        ):
            f.place(x=0, y=0, width=700, height=500)

        # Construir telas
        self._montar_frame_idioma()
        self._montar_frame_modo()
        self._montar_frame_file_select()
        self._montar_frame_formato()
        self._montar_frame_logs()

        self._mostrar_frame(self.frame_idioma)

    def _mostrar_frame(self, frame):
        frame.lift()

    ############################################################################
    # Seta Voltar
    ############################################################################
    def _criar_botao_voltar(self, parent_frame, comando):
        lbl = tk.Label(
            parent_frame,
            text="<--",
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        lbl.place(x=10, y=10)
        lbl.bind("<Button-1>", lambda e: comando())

    ############################################################################
    # Tela 1: Idioma
    ############################################################################
    def _montar_frame_idioma(self):
        self.lbl_lang_title = tk.Label(
            self.frame_idioma,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["lang_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_lang_title.pack(pady=40)

        frm_langs = tk.Frame(self.frame_idioma, bg="black")
        frm_langs.pack()

        langs = ["en", "es", "ru", "it", "pt_BR", "zh"]
        for lang in langs:
            rb = tk.Radiobutton(
                frm_langs,
                text=lang,
                variable=self.idioma_selecionado,
                value=lang,
                indicatoron=False,
                width=8,
                bg="#333333",
                fg="#00FF00",
                selectcolor="#006600",
                font=("Consolas", 12, "bold"),
                borderwidth=2,
                relief="ridge"
            )
            rb.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_next_lang = tk.Button(
            self.frame_idioma,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["next"],
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._ir_para_modo
        )
        self.btn_next_lang.pack(pady=40)

    def _ir_para_modo(self):
        # Vai para tela de modo
        self._atualizar_textos_modo()
        self._mostrar_frame(self.frame_modo)

    def _atualizar_textos_idioma(self, *args):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_lang_title.config(text=texts["lang_select"])
        self.btn_next_lang.config(text=texts["next"])
        self.title(texts["title"])

    ############################################################################
    # Tela 2: Modo (Estrutura ou Conteúdo)
    ############################################################################
    def _montar_frame_modo(self):
        self._criar_botao_voltar(self.frame_modo, self._voltar_idioma)

        self.lbl_mode_title = tk.Label(
            self.frame_modo,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["mode_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_mode_title.pack(pady=40)

        frm_modo = tk.Frame(self.frame_modo, bg="black")
        frm_modo.pack()

        self.rb_structure = tk.Radiobutton(
            frm_modo,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["structure"],
            variable=self.modo_selecionado,
            value="structure",
            indicatoron=False,
            width=12,
            bg="#333333",
            fg="#00FF00",
            selectcolor="#006600",
            font=("Consolas", 12, "bold"),
            borderwidth=2,
            relief="ridge"
        )
        self.rb_structure.pack(side=tk.LEFT, padx=20)

        self.rb_content = tk.Radiobutton(
            frm_modo,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["content"],
            variable=self.modo_selecionado,
            value="content",
            indicatoron=False,
            width=12,
            bg="#333333",
            fg="#00FF00",
            selectcolor="#006600",
            font=("Consolas", 12, "bold"),
            borderwidth=2,
            relief="ridge"
        )
        self.rb_content.pack(side=tk.LEFT, padx=20)

        # Botão "Next >>"
        self.btn_next_mode = tk.Button(
            self.frame_modo,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["next"],
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._ir_para_file_select
        )
        self.btn_next_mode.pack(pady=40)

    def _voltar_idioma(self):
        self._mostrar_frame(self.frame_idioma)

    def _atualizar_textos_modo(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_mode_title.config(text=texts["mode_select"])
        self.rb_structure.config(text=texts["structure"])
        self.rb_content.config(text=texts["content"])
        self.btn_next_mode.config(text=texts["next"])

    def _ir_para_file_select(self):
        self._atualizar_textos_file_select()
        self._mostrar_frame(self.frame_file_select)

    ############################################################################
    # Tela 3: Seleção de Arquivos/Pastas
    ############################################################################
    def _montar_frame_file_select(self):
        self._criar_botao_voltar(self.frame_file_select, self._voltar_modo)

        self.lbl_file_select_title = tk.Label(
            self.frame_file_select,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["file_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_file_select_title.pack(pady=20)

        # Frame para os 2 botões (empilhados verticalmente)
        frm_buttons = tk.Frame(self.frame_file_select, bg="black")
        frm_buttons.pack(pady=10)

        # Botão 1: Escolher Pasta Inteira
        self.btn_choose_folder = tk.Button(
            frm_buttons,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["choose_folder"],
            font=("Consolas", 14, "bold"),
            bg="#333333",
            fg="#00FF00",
            width=30,
            command=self._choose_entire_folder
        )
        self.btn_choose_folder.pack(pady=5)

        # Botão 2: Selecionar Múltiplos Arquivos
        self.btn_choose_files = tk.Button(
            frm_buttons,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["choose_files"],
            font=("Consolas", 14, "bold"),
            bg="#333333",
            fg="#00FF00",
            width=30,
            command=self._choose_multiple_files
        )
        self.btn_choose_files.pack(pady=5)

        # Caixa de texto para inserir manualmente
        placeholder_text = LANG_TEXTS[self.idioma_selecionado.get()]["placeholder_manual"]
        self.manual_input_box = tk.Text(
            self.frame_file_select,
            width=60,
            height=4,
            bg="#00FF00",       # Verde com menor opacidade simulada
            fg="#CCCCCC",
            font=("Consolas", 10),
            borderwidth=2,
            relief="solid"
        )
        self.manual_input_box.pack(pady=10)
        self.manual_input_box.insert("1.0", placeholder_text)
        self._is_placeholder_active = True

        # Botão OK (aparece somente quando há algo digitado)
        self.btn_ok_manual = tk.Button(
            self.frame_file_select,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["manual_ok"],
            font=("Consolas", 12, "bold"),
            bg="#00AA00",
            fg="black",
            width=10,
            command=self._manual_ok_clicked
        )
        # Inicialmente invisível
        self.btn_ok_manual.pack(pady=5)
        self.btn_ok_manual.pack_forget()

        # Vincula eventos para gerenciar placeholder e exibir/esconder botão OK
        self.manual_input_box.bind("<FocusIn>", self._on_focus_in)
        self.manual_input_box.bind("<FocusOut>", self._on_focus_out)
        self.manual_input_box.bind("<KeyRelease>", self._on_key_release)

    def _voltar_modo(self):
        self._mostrar_frame(self.frame_modo)

    def _atualizar_textos_file_select(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_file_select_title.config(text=texts["file_select"])
        self.btn_choose_folder.config(text=texts["choose_folder"])
        self.btn_choose_files.config(text=texts["choose_files"])
        # Atualiza placeholder
        self.manual_input_box.delete("1.0", tk.END)
        self.manual_input_box.insert("1.0", texts["placeholder_manual"])
        self.manual_input_box.config(fg="#CCCCCC")
        self._is_placeholder_active = True
        # Esconde o botão OK
        self.btn_ok_manual.pack_forget()

    def _choose_entire_folder(self):
        pasta_escolhida = filedialog.askdirectory(title="Selecione uma pasta inteira")
        if pasta_escolhida:
            self.caminhos_entrada.append(pasta_escolhida)
            # Assim que escolhe, vamos pra próxima tela
            self._ir_para_formato()

    def _choose_multiple_files(self):
        arquivos_escolhidos = filedialog.askopenfilenames(title="Selecione múltiplos arquivos")
        if arquivos_escolhidos:
            for arq in arquivos_escolhidos:
                self.caminhos_entrada.append(arq)
            # Assim que escolhe, vamos pra próxima tela
            self._ir_para_formato()

    def _on_focus_in(self, event):
        # Remove placeholder se ainda estiver ativo
        if self._is_placeholder_active:
            self.manual_input_box.delete("1.0", tk.END)
            self.manual_input_box.config(fg="white")
            self._is_placeholder_active = False

    def _on_focus_out(self, event):
        # Se caixa está vazia, restaura placeholder
        current_text = self.manual_input_box.get("1.0", tk.END).strip()
        if not current_text:
            self.manual_input_box.config(fg="#CCCCCC")
            self.manual_input_box.delete("1.0", tk.END)
            self.manual_input_box.insert("1.0", LANG_TEXTS[self.idioma_selecionado.get()]["placeholder_manual"])
            self._is_placeholder_active = True
            # Esconde o botão OK
            self.btn_ok_manual.pack_forget()

    def _on_key_release(self, event):
        # Verifica se há algo digitado (diferente do placeholder)
        current_text = self.manual_input_box.get("1.0", tk.END).strip()
        if self._is_placeholder_active or not current_text:
            self.btn_ok_manual.pack_forget()
        else:
            # Mostra botão OK abaixo da caixa de texto
            self.btn_ok_manual.pack(pady=5)

    def _manual_ok_clicked(self):
        # Coletar dados da caixa
        text_data = self.manual_input_box.get("1.0", tk.END).strip()
        # Se ainda estiver com placeholder, ignorar
        if self._is_placeholder_active or (not text_data):
            return

        # Se tem conteúdo, cada linha é um item
        lines = text_data.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                self.caminhos_entrada.append(line)

        # Limpa e restaura placeholder
        self.manual_input_box.delete("1.0", tk.END)
        self.manual_input_box.config(fg="#CCCCCC")
        self.manual_input_box.insert("1.0", LANG_TEXTS[self.idioma_selecionado.get()]["placeholder_manual"])
        self._is_placeholder_active = True
        self.btn_ok_manual.pack_forget()

        # Vai pra próxima tela
        self._ir_para_formato()

    def _ir_para_formato(self):
        self._atualizar_textos_formato()
        self._mostrar_frame(self.frame_formato)

    ############################################################################
    # Tela 4: Formato
    ############################################################################
    def _montar_frame_formato(self):
        self._criar_botao_voltar(self.frame_formato, self._voltar_file_select)

        self.lbl_format_title = tk.Label(
            self.frame_formato,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["format_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_format_title.pack(pady=40)

        frm_format = tk.Frame(self.frame_formato, bg="black")
        frm_format.pack(pady=5)

        self.rb_json = tk.Radiobutton(
            frm_format,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["json"],
            variable=self.formato_selecionado,
            value="json",
            indicatoron=False,
            width=8,
            bg="#333333",
            fg="#00FF00",
            selectcolor="#006600",
            font=("Consolas", 12, "bold"),
            borderwidth=2,
            relief="ridge"
        )
        self.rb_json.pack(side=tk.LEFT, padx=10)

        self.rb_txt = tk.Radiobutton(
            frm_format,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["txt"],
            variable=self.formato_selecionado,
            value="txt",
            indicatoron=False,
            width=8,
            bg="#333333",
            fg="#00FF00",
            selectcolor="#006600",
            font=("Consolas", 12, "bold"),
            borderwidth=2,
            relief="ridge"
        )
        self.rb_txt.pack(side=tk.LEFT, padx=10)

        self.rb_csv = tk.Radiobutton(
            frm_format,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["csv"],
            variable=self.formato_selecionado,
            value="csv",
            indicatoron=False,
            width=8,
            bg="#333333",
            fg="#00FF00",
            selectcolor="#006600",
            font=("Consolas", 12, "bold"),
            borderwidth=2,
            relief="ridge"
        )
        self.rb_csv.pack(side=tk.LEFT, padx=10)

        self.btn_next_format = tk.Button(
            self.frame_formato,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["next"],
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._abrir_explorador_destino
        )
        self.btn_next_format.pack(pady=40)

    def _voltar_file_select(self):
        self._mostrar_frame(self.frame_file_select)

    def _atualizar_textos_formato(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_format_title.config(text=texts["format_select"])
        self.rb_json.config(text=texts["json"])
        self.rb_txt.config(text=texts["txt"])
        self.rb_csv.config(text=texts["csv"])
        self.btn_next_format.config(text=texts["next"])

    def _abrir_explorador_destino(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]

        formato = self.formato_selecionado.get()
        ext = ".json" if formato == "json" else (".txt" if formato == "txt" else ".csv")
        filetypes_map = {
            "json": [("JSON Files", "*.json"), ("All Files", "*.*")],
            "txt":  [("Text Files", "*.txt"),  ("All Files", "*.*")],
            "csv":  [("CSV Files", "*.csv"),   ("All Files", "*.*")]
        }

        caminho_salvar = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=ext,
            initialfile="data",
            filetypes=filetypes_map.get(formato, [("All Files", "*.*")])
        )
        if not caminho_salvar:
            return

        self.caminho_saida = caminho_salvar
        # Ir para logs + processar
        self._mostrar_frame(self.frame_logs)
        self._iniciar_processamento()

    ############################################################################
    # Tela 5: Logs
    ############################################################################
    def _montar_frame_logs(self):
        self._criar_botao_voltar(self.frame_logs, self._voltar_formato)

        self.lbl_logs_title = tk.Label(
            self.frame_logs,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["processing"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_logs_title.pack(pady=10)

        self.lbl_logs_subtitle = tk.Label(
            self.frame_logs,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["logs"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 12, "bold")
        )
        self.lbl_logs_subtitle.pack()

        self.text_logs = tk.Text(
            self.frame_logs,
            width=80,
            height=15,
            bg="black",
            fg="#00FF00",
            font=("Consolas", 10),
            insertbackground="#00FF00",
            borderwidth=2,
            relief="ridge"
        )
        self.text_logs.pack(pady=5)

        # Botão "Ok" ao final
        self.btn_ok = tk.Button(
            self.frame_logs,
            text=LANG_TEXTS[self.idioma_selecionado.get()]["ok"],
            font=("Consolas", 12, "bold"),
            bg="#00AA00",
            fg="black",
            width=8,
            command=self._ok_concluido
        )
        self.btn_ok.pack(side=tk.BOTTOM, pady=10)

    def _voltar_formato(self):
        self._mostrar_frame(self.frame_formato)

    def _ok_concluido(self):
        """
        Retorna à tela de escolher modo (Frame 2) e limpa a memória do script.
        """
        self.caminhos_entrada.clear()  # Limpa os caminhos selecionados
        self._mostrar_frame(self.frame_modo)

    def _iniciar_processamento(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_logs_title.config(text=texts["processing"])
        self.text_logs.delete("1.0", tk.END)
        self.update_idletasks()

        # Se não há caminhos ou não há saída, não processamos
        if not self.caminhos_entrada or not hasattr(self, 'caminho_saida'):
            self._log_line("No input paths or output file selected.")
            return

        modo = self.modo_selecionado.get()
        formato = self.formato_selecionado.get()

        dados_coletados = []
        arquivos_processados = 0
        arquivos_ignorados = 0

        if modo == "structure":
            # Para cada caminho, se for pasta, capturar 'tree'
            # Se for arquivo, ignoramos
            for caminho in self.caminhos_entrada:
                if os.path.isdir(caminho):
                    self._log_line(f"Generating structure for: {caminho}")
                    structure_text = get_folder_structure_win(caminho)
                    if not structure_text.startswith("ERROR"):
                        dados_coletados.append({
                            "path": caminho,
                            "content": structure_text
                        })
                        arquivos_processados += 1
                    else:
                        arquivos_ignorados += 1
                        self._log_line(structure_text)
                else:
                    arquivos_ignorados += 1
                    self._log_line(f"[IGNORED - not a folder] {caminho}")

        else:
            # Conteúdo (sem incluir o conteúdo de imagens)
            for caminho in self.caminhos_entrada:
                if os.path.isfile(caminho):
                    # É um arquivo
                    ext_arq = os.path.splitext(caminho)[1].lower()
                    caminho_posix = Path(caminho).as_posix()

                    if ext_arq in IMAGE_EXTENSIONS:
                        dados_coletados.append({
                            "path": caminho_posix,
                            "content": ""
                        })
                        arquivos_processados += 1
                        self._log_line(f"[OK - IMAGE] {caminho_posix}")
                    else:
                        conteudo = ler_arquivo_com_codificacoes(caminho)
                        if conteudo is not None:
                            dados_coletados.append({
                                "path": caminho_posix,
                                "content": conteudo
                            })
                            arquivos_processados += 1
                            self._log_line(f"[OK] {caminho_posix}")
                        else:
                            arquivos_ignorados += 1
                            self._log_line(f"[IGNORED] {caminho_posix}")

                elif os.path.isdir(caminho):
                    # Se for pasta, processar todos arquivos dentro
                    for raiz, dirs, arquivos in os.walk(caminho):
                        for arquivo in arquivos:
                            fullpath = os.path.join(raiz, arquivo)
                            ext_arq = os.path.splitext(arquivo)[1].lower()
                            caminho_posix = Path(fullpath).as_posix()

                            if ext_arq in IMAGE_EXTENSIONS:
                                dados_coletados.append({
                                    "path": caminho_posix,
                                    "content": ""
                                })
                                arquivos_processados += 1
                                self._log_line(f"[OK - IMAGE] {caminho_posix}")
                            else:
                                conteudo = ler_arquivo_com_codificacoes(fullpath)
                                if conteudo is not None:
                                    dados_coletados.append({
                                        "path": caminho_posix,
                                        "content": conteudo
                                    })
                                    arquivos_processados += 1
                                    self._log_line(f"[OK] {caminho_posix}")
                                else:
                                    arquivos_ignorados += 1
                                    self._log_line(f"[IGNORED] {caminho_posix}")
                else:
                    arquivos_ignorados += 1
                    self._log_line(f"[IGNORED - invalid path] {caminho}")

        # Salva se há algo
        if dados_coletados:
            self._salvar_dados(dados_coletados, self.caminho_saida, formato)
            self._log_line(f"{texts['success_files']}{arquivos_processados}")
            self._log_line(f"{texts['ignored_files']}{arquivos_ignorados}")
            self._log_line(f"\n{texts['saved_in']}{self.caminho_saida}")
        else:
            self._log_line("No valid items found or all were ignored.")

        self._log_line(f"\n{texts['done']}")

    def _salvar_dados(self, dados, caminho, formato):
        if formato == "json":
            salvar_como_json(dados, caminho)
        elif formato == "txt":
            salvar_como_txt(dados, caminho)
        else:
            salvar_como_csv(dados, caminho)

    def _log_line(self, text):
        self.text_logs.insert(tk.END, text + "\n")
        self.text_logs.see(tk.END)

###############################################################################
# Execução
###############################################################################
if __name__ == "__main__":
    app = FolderConverterApp()
    app.mainloop()
