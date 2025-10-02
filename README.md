## JSON Formatter — Convert Folders/Files to JSON, TXT, or CSV

Desktop app (Tkinter/Python) to extract either the folder tree or the textual contents of files from a project, and save everything as JSON, TXT, or CSV. Ideal for documenting projects, auditing repositories, and preparing datasets for LLMs (ChatGPT, Claude, etc.).

---

### Contents
- **Overview**
- **Supported platforms**
- **Installation**
- **How to run**
- **UI and flows (step-by-step with all buttons)**
- **How files are processed (inclusion/ignore rules)**
- **Output formats (with examples)**
- **Use cases — including sending a full repository to an LLM**
- **Tips for LLM usage**
- **Limitations and important notes**
- **Privacy**
- **Troubleshooting (FAQ)**
- **License**

---

## Overview
The app follows a simple guided flow:
1) Choose the mode (Structure or Content) → 2) Select files/folders → 3) Choose the output format (JSON/TXT/CSV) → 4) Watch logs and finish.

- **Structure mode**: generates the folder tree (similar to `tree`).
- **Content mode**: reads textual contents of files. Images are included with empty content; common media/binary files are ignored.

There is a persistent help “?” button (bottom-right) that opens an in-app tutorial, and a “<-- Back” button at the top to return to the previous step.

---

## Supported platforms
- App: works anywhere with Python 3 and Tkinter.
- **Structure mode**: relies on Windows `tree` command. On macOS/Linux this mode will show an error (“tree only supported on Windows”). **Content mode** works cross-platform.

---

## Installation
Prerequisite: **Python 3.x** with Tkinter (included in most default Python installs on Windows/macOS/Linux).

Source code setup:
1. Clone/download this repository.
2. Enter the project directory.
3. No external dependencies: standard library only.

Windows (optional): the repo may include `script.exe`. If present, double-click it to run the app without installing Python.

---

## How to run
- On Windows (recommended):
  - Go to the Releases page, download the latest `script.exe`, then double-click to run.
- With Python (alternative):
  ```bash
  python script.py
  ```

Note: this is a desktop GUI app; it does not start a server/HTTP port.

---

## UI and flows

### 1) “Choose Mode” screen
- **Structure**: selects the folder tree mode.
- **Content**: selects the file content mode.
- **Next >>**: moves to the file/folder selection screen.

Persistent elements across screens:
- **Title (“JSON FORMATTER”)** at the top.
- **<-- Back**: appears at the top when there is a previous step.
- **Help “?” button** at the bottom-right:
  - Click: opens/closes the tutorial overlay within the same window.
  - Hover: shows a small “tutorial” tooltip.

### 2) “Select how you want to pick files/folders” screen
- **Choose Entire Folder**: opens a folder picker. In Structure mode, only folders are meaningful. In Content mode, the folder is scanned recursively.
- **Select Multiple Files**: opens a file picker to select several specific files at once.
- **Text box (placeholder: “Or type the directories of files/folders here”)**: paste paths manually (one per line), mixing files and folders.
- **Next >> (below the text box)**: appears and enables automatically when there is valid text; moves forward and collects the paths you entered.

Other behaviors:
- Placeholder is removed on focus and restored if you clear everything and move focus away.
- When entering text manually, each non-empty line is treated as a path.

### 3) “Choose Output Format” screen
- **JSON / TXT / CSV**: select the final output format.
- **Next >>**: opens the “Save as” dialog so you can choose the output file (initial suggestion: `data.json`, `data.txt`, or `data.csv`).

### 4) “Processing… / Logs” screen
- **Logs**: real-time updates of what was processed/ignored with the item path and reason.
- **Ok**: when finished, returns to the start (clears selected paths).

Typical log messages:
- `[OK] /path/to/file.txt` — text file processed successfully.
- `[OK - IMAGE] /path/to/image.png` — image included with empty content.
- `[IGNORED - MEDIA FILE] /path/to/video.mp4` — media/binary files ignored.
- `[IGNORED - filename with strange chars] ...` — filename contains non-ASCII characters.
- `[IGNORED - not a folder] ...` (Structure mode) — path is not a folder.
- `Generating structure for: C:\project` — generating the tree.

---

## How files are processed

### Structure mode
- For each provided path that is a folder (files are ignored), runs `tree /f /a` (Windows) and captures the textual tree.
- Each produced entry has `{ path: <folder>, content: <tree_text> }`.
- On non-Windows systems an error is logged because the used `tree` command is Windows-specific.

### Content mode
- Path is a file:
  - Image extensions (e.g., `.jpg`, `.png`, `.svg`, `.webp`, etc.): included with empty `content` (`""`) — useful to keep references in datasets.
  - Media/large/binary extensions (e.g., `.mp4`, `.mp3`, `.zip`, `.iso`, `.exe`, etc.): ignored by default.
  - Other extensions: the app attempts to read as text (tries `utf-8`, then `latin1`, then `cp1252`, with a fallback to `utf-8` using `errors='replace'`). If reading fails, the file is ignored.
- Path is a folder:
  - Recurses, ignoring folders: `node_modules`, `.next`, `.git`.
  - Filenames with non-ASCII characters are ignored to avoid serialization/compat issues.
  - For each file found, the same extension/reading rules above are applied.
- Saved `path` is normalized to POSIX (`/`) for consistency.

---

## Output formats

### JSON
Array of objects with two keys: `path` and `content`.
```json
[
  {
    "path": "repo/src/app.py",
    "content": "print('hello')\n"
  },
  {
    "path": "repo/assets/logo.png",
    "content": ""
  }
]
```

### TXT
Readable block format, great for pasting directly into LLMs, with separators and explicit fields:
```text
---
path:
"repo/src/app.py",

content:
print('hello')

---
path:
"repo/assets/logo.png",

content:

```

### CSV
Two columns: `path`, `content` (comma-separated, UTF-8). Useful for programmatic processing, spreadsheets, or chunking pipelines.

---

## Use cases (including LLMs)

### 1) Send a full repository to an LLM
Goal: provide complete project context for analysis/refactoring/diagnosis.

Suggested steps:
1. First run **Structure mode** on the repository root (Windows). Export as **TXT**. Paste the tree into the LLM to contextualize organization.
2. Then run **Content mode** on the repository root. Export as **TXT** when you want to paste chunks directly into the LLM, or **JSON/CSV** if you plan to feed a chunking tool.
3. If the repository is too large for token limits, prioritize relevant subfolders, or use a chunking pipeline (e.g., split by files/lines before sending to the LLM).
4. The app already ignores binaries and heavy media by extension, reducing noise and token usage.

Tips:
- **TXT** is great for direct copy/paste since it presents `path` before content in blocks.
- **JSON** is automation-friendly; **CSV** is convenient for spreadsheets and low-code tools.
- For focused reviews, use “Select Multiple Files” and pick only source files.

### 2) Project auditing/documentation
- Use **Structure mode** to quickly generate a project layout overview.
- Use **Content mode** to extract snippets/code in bulk.

### 3) Building textual datasets
- Export **CSV**/**JSON** for cleaning/normalization/chunking pipelines.
- Images are included with empty content but keep the `path` (useful to enrich metadata later).

---

## Tips for LLM usage
- Combine Structure + Content: provide the tree first, then relevant files.
- Split by parts: for large repos, generate outputs per submodule/package.
- Incremental context: start with TXT/JSON for key modules; provide more blocks as the LLM asks.
- Keep paths: many LLMs reason better when `path` precedes content.

---

## Limitations and important notes
- **Structure is Windows-only** (uses `tree /f /a`). On other platforms, use Content mode.
- Binary detection is based on common **file extensions**; unusual binaries without extensions might slip through (avoid adding them manually).
- Very large text files are read whole; consider filtering first (e.g., huge logs).
- Filenames containing non-ASCII characters are ignored for stability/compatibility.

---

## Privacy
The app runs 100% locally. No files are sent over the internet. You control what goes into the output and where it is saved.

---

## Troubleshooting (FAQ)
- “I got an error saying `tree` only works on Windows.”
  - Structure mode depends on Windows `tree`. Use Content mode or run on a Windows machine.
- “The Next button under the text box doesn’t show up.”
  - It only appears when there is valid (non-placeholder) text. Enter one path per line.
- “Some files were ignored.”
  - Check the logs: it may be due to media/binary extension, non-ASCII filename, or read error.
- “I only want certain file types (e.g., .py, .ts, .md).”
  - Use “Select Multiple Files” or paste filtered paths manually.

---

## License
MIT License.

