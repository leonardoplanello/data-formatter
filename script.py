import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import csv
import tempfile
import platform
from pathlib import Path

###############################################################################
# English-only UI texts
###############################################################################
TEXTS = {
    "title": "JSON FORMATTER",
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
}

###############################################################################
# img ext
###############################################################################
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".webp", ".svg", ".heic", ".heif", ".ico", ".raw"
}

###############################################################################
# media ext (vid/audio/etc)
###############################################################################
MEDIA_EXTENSIONS = {
    ".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".mpeg", ".mpg",
    ".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma", ".m4a",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
    ".iso", ".dmg",
    ".exe", ".dll", ".msi", ".apk"
}

###############################################################################
# IO helpers
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
    # fallback: utf-8 w/ replace
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception:
        return None

def get_folder_structure_win(folder_path):
    """run 'tree /f /a folder_path' (win-only) n return txt."""
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
        self.title("JSON FORMATTER")
        self.geometry("700x600")  # taller so stuff fits
        self.resizable(False, True)
        self.configure(bg="black")

        # state
        self.modo_selecionado   = tk.StringVar(value="content")  # structure|content
        self.formato_selecionado= tk.StringVar(value="json")     # json|txt|csv

        # store multi paths (files or dirs)
        self.caminhos_entrada = []

        # sticky header (title)
        self.header_label = tk.Label(
            self,
            text="JSON FORMATTER",
            bg="black",
            fg="#00FF00",
            font=("Consolas", 26, "bold")
        )
        # reserve space under header
        self.header_label.place(x=0, y=6, width=700, height=50)

        # back label (persistent)
        self.back_label = tk.Label(
            self,
            text=TEXTS["back"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        # hidden @ start
        self.back_label.place_forget()
        self._current_back_command = None

        # screens
        self.frame_modo        = tk.Frame(self, bg="black")
        self.frame_file_select = tk.Frame(self, bg="black")
        self.frame_formato     = tk.Frame(self, bg="black")
        self.frame_logs        = tk.Frame(self, bg="black")

        for f in (
            self.frame_modo,
            self.frame_file_select,
            self.frame_formato,
            self.frame_logs
        ):
            # place below header so title stays visible
            f.place(x=0, y=70, width=700, height=530)

        
        # build screens
        self._montar_frame_modo()
        self._montar_frame_file_select()
        self._montar_frame_formato()
        self._montar_frame_logs()

        self._mostrar_frame(self.frame_modo)

        
    def _mostrar_frame(self, frame):
        frame.lift()

    

    def _set_back(self, comando):
        self._current_back_command = comando
        self.back_label.bind("<Button-1>", lambda e: comando())
        self.back_label.place(x=10, y=12)

    def _hide_back(self):
        self.back_label.place_forget()

    ############################################################################
    # back label
    ############################################################################
    def _criar_botao_voltar(self, parent_frame, comando):
        lbl = tk.Label(
            parent_frame,
            text=TEXTS["back"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        lbl.place(x=10, y=10)
        lbl.bind("<Button-1>", lambda e: comando())

    ############################################################################
    # screen 2: Mode (Structure or Content)
    ############################################################################
    def _montar_frame_modo(self):
        self.lbl_mode_title = tk.Label(
            self.frame_modo,
            text=TEXTS["mode_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        # add top padding (space for header)
        self.lbl_mode_title.pack(pady=35)

        frm_modo = tk.Frame(self.frame_modo, bg="black")
        frm_modo.pack()

        self.rb_structure = tk.Radiobutton(
            frm_modo,
            text=TEXTS["structure"],
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
        self.rb_structure.pack(side=tk.LEFT, padx=10)

        self.rb_content = tk.Radiobutton(
            frm_modo,
            text=TEXTS["content"],
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
        self.rb_content.pack(side=tk.LEFT, padx=10)

        # Next btn
        self.btn_next_mode = tk.Button(
            self.frame_modo,
            text=TEXTS["next"],
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._ir_para_file_select
        )
        self.btn_next_mode.pack(pady=20)

    def _atualizar_textos_modo(self):
        self.lbl_mode_title.config(text=TEXTS["mode_select"])
        self.rb_structure.config(text=TEXTS["structure"])
        self.rb_content.config(text=TEXTS["content"])
        self.btn_next_mode.config(text=TEXTS["next"])

    def _ir_para_file_select(self):
        self._atualizar_textos_file_select()
        self._mostrar_frame(self.frame_file_select)
        self._set_back(self._voltar_modo)

    ############################################################################
    # screen 3: File/Folder selection
    ############################################################################
    def _montar_frame_file_select(self):

        self.lbl_file_select_title = tk.Label(
            self.frame_file_select,
            text=TEXTS["file_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_file_select_title.pack(pady=15)

        # buttons container (stacked)
        frm_buttons = tk.Frame(self.frame_file_select, bg="black")
        frm_buttons.pack(pady=5)

        # choose entire folder
        self.btn_choose_folder = tk.Button(
            frm_buttons,
            text=TEXTS["choose_folder"],
            font=("Consolas", 14, "bold"),
            bg="#333333",
            fg="#00FF00",
            width=30,
            command=self._choose_entire_folder
        )
        self.btn_choose_folder.pack(pady=4)

        # select multiple files
        self.btn_choose_files = tk.Button(
            frm_buttons,
            text=TEXTS["choose_files"],
            font=("Consolas", 14, "bold"),
            bg="#333333",
            fg="#00FF00",
            width=30,
            command=self._choose_multiple_files
        )
        self.btn_choose_files.pack(pady=4)

        # manual input box
        placeholder_text = TEXTS["placeholder_manual"]
        self.manual_input_box = tk.Text(
            self.frame_file_select,
            width=60,
            height=4,
            bg="#33FF33",       # light green bg (fake ~20% opacity vibe)
            fg="black",
            font=("Consolas", 10),
            borderwidth=2,
            relief="solid"
        )
        self.manual_input_box.pack(pady=6)
        self.manual_input_box.insert("1.0", placeholder_text)
        self._is_placeholder_active = True

        # "Next >>" for manual input
        self.btn_next_manual = tk.Button(
            self.frame_file_select,
            text="Next >>",
            font=("Consolas", 12, "bold"),
            bg="#00AA00",
            fg="black",
            width=10,
            state=tk.DISABLED,  # disabled initially
            command=self._manual_next_clicked
        )
        self.btn_next_manual.pack(pady=5)
        self.btn_next_manual.pack_forget()  # hide initially

        # events to handle placeholder + toggle next btn
        self.manual_input_box.bind("<FocusIn>", self._on_focus_in)
        self.manual_input_box.bind("<FocusOut>", self._on_focus_out)
        self.manual_input_box.bind("<KeyRelease>", self._on_key_release)

    def _voltar_modo(self):
        self._mostrar_frame(self.frame_modo)
        self._hide_back()

    def _atualizar_textos_file_select(self):
        self.lbl_file_select_title.config(text=TEXTS["file_select"])
        self.btn_choose_folder.config(text=TEXTS["choose_folder"])
        self.btn_choose_files.config(text=TEXTS["choose_files"])
        # reset placeholder
        self.manual_input_box.delete("1.0", tk.END)
        self.manual_input_box.insert("1.0", TEXTS["placeholder_manual"])
        self.manual_input_box.config(fg="black")
        self._is_placeholder_active = True
        # hide "Next >>"
        self.btn_next_manual.pack_forget()

    def _choose_entire_folder(self):
        pasta_escolhida = filedialog.askdirectory(title=TEXTS["choose_folder"])
        if pasta_escolhida:
            self.caminhos_entrada.append(pasta_escolhida)
            # go next right away
            self._ir_para_formato()

    def _choose_multiple_files(self):
        arquivos_escolhidos = filedialog.askopenfilenames(title=TEXTS["choose_files"])
        if arquivos_escolhidos:
            for arq in arquivos_escolhidos:
                self.caminhos_entrada.append(arq)
            # go next right away
            self._ir_para_formato()

    def _on_focus_in(self, event):
        # drop placeholder if active
        if self._is_placeholder_active:
            self.manual_input_box.delete("1.0", tk.END)
            self.manual_input_box.config(fg="black")
            self._is_placeholder_active = False

    def _on_focus_out(self, event):
        # if empty, restore placeholder
        current_text = self.manual_input_box.get("1.0", tk.END).strip()
        if not current_text:
            self.manual_input_box.config(fg="black")
            self.manual_input_box.delete("1.0", tk.END)
            self.manual_input_box.insert("1.0", TEXTS["placeholder_manual"])
            self._is_placeholder_active = True
            # hide "Next >>"
            self.btn_next_manual.pack_forget()

    def _on_key_release(self, event):
        # check if user typed (not placeholder)
        current_text = self.manual_input_box.get("1.0", tk.END).strip()
        if self._is_placeholder_active or not current_text:
            self.btn_next_manual.config(state=tk.DISABLED)
            self.btn_next_manual.pack_forget()
        else:
            # show + enable "Next >>"
            self.btn_next_manual.config(state=tk.NORMAL)
            self.btn_next_manual.pack(pady=5)

    def _manual_next_clicked(self):
        # grab text
        text_data = self.manual_input_box.get("1.0", tk.END).strip()
        # ignore if still placeholder
        if self._is_placeholder_active or (not text_data):
            return

        # split lines into items
        lines = text_data.split("\n")
        for line in lines:
            line = line.strip()
            if line:
                self.caminhos_entrada.append(line)

        # reset placeholder
        self.manual_input_box.delete("1.0", tk.END)
        self.manual_input_box.config(fg="black")
        self.manual_input_box.insert("1.0", TEXTS["placeholder_manual"])
        self._is_placeholder_active = True
        # disable + hide "Next >>"
        self.btn_next_manual.config(state=tk.DISABLED)
        self.btn_next_manual.pack_forget()

        # go next
        self._ir_para_formato()

    def _ir_para_formato(self):
        self._atualizar_textos_formato()
        self._mostrar_frame(self.frame_formato)
        self._set_back(self._voltar_file_select)

    ############################################################################
    # screen 4: Format
    ############################################################################
    def _montar_frame_formato(self):

        self.lbl_format_title = tk.Label(
            self.frame_formato,
            text=TEXTS["format_select"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_format_title.pack(pady=10)

        frm_format = tk.Frame(self.frame_formato, bg="black")
        frm_format.pack(pady=5)

        self.rb_json = tk.Radiobutton(
            frm_format,
            text=TEXTS["json"],
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
            text=TEXTS["txt"],
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
            text=TEXTS["csv"],
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
            text=TEXTS["next"],
            font=("Consolas", 14, "bold"),
            bg="#00AA00",
            fg="black",
            width=15,
            command=self._abrir_explorador_destino
        )
        self.btn_next_format.pack(pady=40)

    def _voltar_file_select(self):
        self._mostrar_frame(self.frame_file_select)
        self._set_back(self._voltar_modo)

    def _atualizar_textos_formato(self):
        self.lbl_format_title.config(text=TEXTS["format_select"])
        self.rb_json.config(text=TEXTS["json"])
        self.rb_txt.config(text=TEXTS["txt"])
        self.rb_csv.config(text=TEXTS["csv"])
        self.btn_next_format.config(text=TEXTS["next"])

    def _abrir_explorador_destino(self):
        formato = self.formato_selecionado.get()
        ext = ".json" if formato == "json" else (".txt" if formato == "txt" else ".csv")
        filetypes_map = {
            "json": [("JSON Files", "*.json"), ("All Files", "*.*")],
            "txt":  [("Text Files", "*.txt"),  ("All Files", "*.*")],
            "csv":  [("CSV Files", "*.csv"),   ("All Files", "*.*")]
        }

        caminho_salvar = filedialog.asksaveasfilename(
            title=TEXTS["format_select"],
            defaultextension=ext,
            initialfile="data",
            filetypes=filetypes_map.get(formato, [("All Files", "*.*")])
        )
        if not caminho_salvar:
            return

        self.caminho_saida = caminho_salvar
        # go to logs + process
        self._mostrar_frame(self.frame_logs)
        self._iniciar_processamento()

    ############################################################################
    # screen 5: Logs
    ############################################################################
    def _montar_frame_logs(self):

        self.lbl_logs_title = tk.Label(
            self.frame_logs,
            text=TEXTS["processing"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 16, "bold")
        )
        self.lbl_logs_title.pack(pady=60)

        self.lbl_logs_subtitle = tk.Label(
            self.frame_logs,
            text=TEXTS["logs"],
            bg="black",
            fg="#00FF00",
            font=("Consolas", 12, "bold")
        )
        self.lbl_logs_subtitle.pack()

        self.text_logs = tk.Text(
            self.frame_logs,
            width=80,
            height=15,
            bg="#33FF33",
            fg="black",
            font=("Consolas", 10),
            insertbackground="black",
            borderwidth=2,
            relief="ridge"
        )
        self.text_logs.pack(pady=5, fill=tk.BOTH, expand=True)

        # Ok btn at bottom
        self.btn_ok = tk.Button(
            self.frame_logs,
            text=TEXTS["ok"],
            font=("Consolas", 12, "bold"),
            bg="#00AA00",
            fg="black",
            width=8,
            command=self._ok_concluido
        )
        self.btn_ok.pack(side=tk.BOTTOM, pady=10)

    

    def _voltar_formato(self):
        self._mostrar_frame(self.frame_formato)
        self._set_back(self._voltar_file_select)

    def _ok_concluido(self):
        """go back to mode screen & clear state."""
        self.caminhos_entrada.clear()
        self._mostrar_frame(self.frame_modo)
        self._hide_back()

    def _iniciar_processamento(self):
        self.lbl_logs_title.config(text=TEXTS["processing"])
        self.text_logs.delete("1.0", tk.END)
        self.update_idletasks()

        # no inputs or no output? bail
        if not self.caminhos_entrada or not hasattr(self, 'caminho_saida'):
            self._log_line("No input paths or output file selected.")
            return

        modo = self.modo_selecionado.get()
        formato = self.formato_selecionado.get()

        dados_coletados = []
        arquivos_processados = 0
        arquivos_ignorados = 0

        if modo == "structure":
            # folders -> run tree; files -> ignore
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
            # content mode (img -> empty content)
            for caminho in self.caminhos_entrada:
                if os.path.isfile(caminho):
                    # it's a file
                    ext_arq = os.path.splitext(caminho)[1].lower()
                    caminho_posix = Path(caminho).as_posix()

                    if ext_arq in IMAGE_EXTENSIONS:
                        dados_coletados.append({
                            "path": caminho_posix,
                            "content": ""
                        })
                        arquivos_processados += 1
                        self._log_line(f"[OK - IMAGE] {caminho_posix}")
                    elif ext_arq in MEDIA_EXTENSIONS:
                        arquivos_ignorados += 1
                        self._log_line(f"[IGNORED - MEDIA FILE] {caminho_posix}")
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
                    # folder -> process all files inside
                    for raiz, dirs, arquivos in os.walk(caminho):
                        # ignore node_modules, .next, .git
                        ignore_folders = ['node_modules', '.next', '.git']
                        dirs[:] = [d for d in dirs if d not in ignore_folders]

                        for arquivo in arquivos:
                            fullpath = os.path.join(raiz, arquivo)
                            caminho_posix = Path(fullpath).as_posix()
                            try:
                                arquivo.encode('ascii')
                            except UnicodeEncodeError:
                                arquivos_ignorados += 1
                                self._log_line(f"[IGNORED - filename with strange chars] {caminho_posix}")
                                continue  # skip this file

                            ext_arq = os.path.splitext(arquivo)[1].lower()

                            if ext_arq in IMAGE_EXTENSIONS:
                                dados_coletados.append({
                                    "path": caminho_posix,
                                    "content": ""
                                })
                                arquivos_processados += 1
                                self._log_line(f"[OK - IMAGE] {caminho_posix}")
                            elif ext_arq in MEDIA_EXTENSIONS:
                                arquivos_ignorados += 1
                                self._log_line(f"[IGNORED - MEDIA FILE] {caminho_posix}")
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

        # save if any
        if dados_coletados:
            self._salvar_dados(dados_coletados, self.caminho_saida, formato)
            self._log_line(f"{TEXTS['success_files']}{arquivos_processados}")
            self._log_line(f"{TEXTS['ignored_files']}{arquivos_ignorados}")
            self._log_line(f"\n{TEXTS['saved_in']}{self.caminho_saida}")
        else:
            self._log_line("No valid items found or all were ignored.")

        self._log_line(f"\n{TEXTS['done']}")

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
