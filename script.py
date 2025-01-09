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
        "ok": "Ok"
    },
    "es": {
        "title": "Folder Converter",
        "lang_select": "Selecciona tu idioma:",
        "next": "Siguiente >>",
        "mode_select": "Elige el Modo:",
        "structure": "Estructura",
        "content": "Contenido",
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
        "ok": "Ok"
    },
    "ru": {
        "title": "Folder Converter",
        "lang_select": "Выберите язык:",
        "next": "Далее >>",
        "mode_select": "Выберите режим:",
        "structure": "Структура",
        "content": "Содержимое",
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
        "ok": "Ok"
    },
    "it": {
        "title": "Folder Converter",
        "lang_select": "Seleziona la tua lingua:",
        "next": "Avanti >>",
        "mode_select": "Scegli la Modalità:",
        "structure": "Struttura",
        "content": "Contenuto",
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
        "ok": "Ok"
    },
    "pt_BR": {
        "title": "Folder Converter",
        "lang_select": "Selecione seu idioma:",
        "next": "Próximo >>",
        "mode_select": "Escolha o Modo:",
        "structure": "Estrutura",
        "content": "Conteúdo",
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
        "ok": "Ok"
    },
    "zh": {
        "title": "Folder Converter",
        "lang_select": "选择语言：",
        "next": "下一步 >>",
        "mode_select": "选择模式：",
        "structure": "结构",
        "content": "内容",
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
        "ok": "Ok"
    }
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
        self.pasta_origem  = None
        self.caminho_saida = None

        # Atualiza UI quando idioma muda
        self.idioma_selecionado.trace_add("write", self._atualizar_textos_idioma)

        # Frames (telas)
        self.frame_idioma  = tk.Frame(self, bg="black")
        self.frame_modo    = tk.Frame(self, bg="black")
        self.frame_formato = tk.Frame(self, bg="black")
        self.frame_logs    = tk.Frame(self, bg="black")

        for f in (self.frame_idioma, self.frame_modo, self.frame_formato, self.frame_logs):
            f.place(x=0, y=0, width=700, height=500)

        # Construir telas
        self._montar_frame_idioma()
        self._montar_frame_modo()
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
            text="Select your language:",
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
            text="Next >>",
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
            text="(mode_select)",
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_mode_title.pack(pady=40)

        frm_modo = tk.Frame(self.frame_modo, bg="black")
        frm_modo.pack()

        self.rb_structure = tk.Radiobutton(
            frm_modo,
            text="Structure",
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
            text="Content",
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

        self.btn_next_mode = tk.Button(
            self.frame_modo,
            text="Next >>",
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._abrir_explorador_pasta
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

    def _abrir_explorador_pasta(self):
        self.pasta_origem = filedialog.askdirectory(title="Select Folder")
        if not self.pasta_origem:
            return
        self._ir_para_formato()

    ############################################################################
    # Tela 3: Formato
    ############################################################################
    def _montar_frame_formato(self):
        self._criar_botao_voltar(self.frame_formato, self._voltar_modo)

        self.lbl_format_title = tk.Label(
            self.frame_formato,
            text="(format_select)",
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_format_title.pack(pady=40)

        frm_format = tk.Frame(self.frame_formato, bg="black")
        frm_format.pack(pady=5)

        self.rb_json = tk.Radiobutton(
            frm_format,
            text="JSON",
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
            text="TXT",
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
            text="CSV",
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
            text="Next >>",
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._abrir_explorador_destino
        )
        self.btn_next_format.pack(pady=40)

    def _voltar_modo(self):
        self._mostrar_frame(self.frame_modo)

    def _atualizar_textos_formato(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_format_title.config(text=texts["format_select"])
        self.rb_json.config(text=texts["json"])
        self.rb_txt.config(text=texts["txt"])
        self.rb_csv.config(text=texts["csv"])
        self.btn_next_format.config(text=texts["next"])

    def _ir_para_formato(self):
        self._atualizar_textos_formato()
        self._mostrar_frame(self.frame_formato)

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
    # Tela 4: Logs
    ############################################################################
    def _montar_frame_logs(self):
        self._criar_botao_voltar(self.frame_logs, self._voltar_formato)

        self.lbl_logs_title = tk.Label(
            self.frame_logs,
            text="(processing...)",
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_logs_title.pack(pady=10)

        self.lbl_logs_subtitle = tk.Label(
            self.frame_logs,
            text="Logs:",
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
            text="Ok",
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
        Retorna à tela de escolher modo (Frame 2), ignorando a tela de formato.
        """
        self._mostrar_frame(self.frame_modo)

    def _iniciar_processamento(self):
        lang = self.idioma_selecionado.get()
        texts = LANG_TEXTS[lang]
        self.lbl_logs_title.config(text=texts["processing"])
        self.text_logs.delete("1.0", tk.END)
        self.update_idletasks()

        if not self.pasta_origem or not self.caminho_saida:
            self._log_line("No folder or output file selected.")
            return

        modo = self.modo_selecionado.get()
        formato = self.formato_selecionado.get()

        if modo == "structure":
            self._log_line(f"Generating structure for: {self.pasta_origem}")
            structure_text = get_folder_structure_win(self.pasta_origem)
            if not structure_text.startswith("ERROR"):
                dados = [{"path": self.pasta_origem, "content": structure_text}]
                self._salvar_dados(dados, self.caminho_saida, formato)
                self._log_line("Structure captured successfully.")
            else:
                self._log_line(structure_text)
        else:
            # Conteúdo
            dados_coletados = []
            arquivos_processados = 0
            arquivos_ignorados = 0

            for raiz, dirs, arquivos in os.walk(self.pasta_origem):
                for arquivo in arquivos:
                    caminho_arquivo = os.path.join(raiz, arquivo)
                    conteudo = ler_arquivo_com_codificacoes(caminho_arquivo)

                    if conteudo is not None:
                        caminho_posix = Path(caminho_arquivo).as_posix()
                        dados_coletados.append({
                            "path": caminho_posix,
                            "content": conteudo
                        })
                        arquivos_processados += 1
                        self._log_line(f"[OK] {caminho_posix}")
                    else:
                        arquivos_ignorados += 1
                        self._log_line(f"[IGNORED] {caminho_arquivo}")

                    self.update_idletasks()

            if dados_coletados:
                self._salvar_dados(dados_coletados, self.caminho_saida, formato)
                self._log_line(f"{texts['success_files']}{arquivos_processados}")
                self._log_line(f"{texts['ignored_files']}{arquivos_ignorados}")
            else:
                self._log_line("No valid text files found or all files failed to read.")

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
