"""File Integrity Monitor.

GUI simples para selecionar um arquivo, salvar seu hash SHA-256 e verificar
depois se o conteúdo foi alterado.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

APP_TITLE = "File Integrity Monitor"
HASH_FILE = Path(__file__).with_name("hash_data.json")
TKINTER_ERROR = None


try:
    from tkinter import Button, Label, Tk, filedialog, messagebox
    HAS_TKINTER = True
except Exception as exc:  # pragma: no cover - depends on local Python build
    Button = Label = Tk = filedialog = messagebox = None
    HAS_TKINTER = False
    TKINTER_ERROR = exc


TkBase = Tk if HAS_TKINTER else object


def calculate_hash(file_path: str) -> str:
    """Calcula o hash SHA-256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file_handle:
        for byte_block in iter(lambda: file_handle.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def save_hash_data(file_path: str, hash_value: str) -> None:
    """Salva os dados do arquivo monitorado em JSON."""
    data = {"file_path": file_path, "hash_value": hash_value}
    with open(HASH_FILE, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)


def load_hash_data() -> dict:
    """Carrega os dados salvos do arquivo JSON."""
    with open(HASH_FILE, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def _tk_candidate_pythons() -> list[str]:
    # Prioriza versões que já foram validadas com criação de janela Tk neste ambiente.
    candidates = [
        "/Library/Frameworks/Python.framework/Versions/3.12/bin/python3",
        "/Library/Frameworks/Python.framework/Versions/3.11/bin/python3",
        "/usr/local/bin/python3",
    ]
    unique_candidates = []
    for candidate in candidates:
        if candidate and candidate not in unique_candidates:
            unique_candidates.append(candidate)
    return unique_candidates


def _python_has_tk(python_executable: str) -> bool:
    probe = subprocess.run(
        [python_executable, "-c", "import tkinter"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return probe.returncode == 0


def _relaunch_with_tk_python() -> bool:
    """Tenta relançar o script em um Python que tenha tkinter."""
    if os.environ.get("FIM_RELAUNCHED_WITH_TK") == "1":
        return False

    for candidate in _tk_candidate_pythons():
        if candidate == sys.executable:
            continue
        if os.path.exists(candidate) and _python_has_tk(candidate):
            os.environ["FIM_RELAUNCHED_WITH_TK"] = "1"
            os.execv(candidate, [candidate, __file__, *sys.argv[1:]])
            return True
    return False


class FIMApp(TkBase):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("520x260")
        self.resizable(False, False)

        self.file_path = ""
        self.hash_value = ""

        self._build_ui()

    def _build_ui(self):
        Label(self, text="File Integrity Monitor", font=("Arial", 16, "bold")).pack(pady=(18, 8))
        Label(
            self,
            text="Selecione um arquivo, salve o hash e depois verifique se ele mudou.",
            wraplength=460,
            justify="center",
        ).pack(pady=(0, 16))

        Button(self, text="Selecionar arquivo", width=24, command=self.select_file).pack(pady=4)
        Button(self, text="Salvar hash", width=24, command=self.save_hash).pack(pady=4)
        Button(self, text="Verificar arquivo", width=24, command=self.verify_file).pack(pady=4)

        self.status_label = Label(self, text="Nenhum arquivo selecionado.", wraplength=480, justify="center")
        self.status_label.pack(pady=(16, 0))

    def select_file(self):
        selected_file = filedialog.askopenfilename(title="Selecione um arquivo")
        if not selected_file:
            return

        self.file_path = selected_file
        self.hash_value = calculate_hash(self.file_path)
        self.status_label.config(text=f"Arquivo selecionado:\n{self.file_path}\n\nHash atual:\n{self.hash_value}")

    def save_hash(self):
        if not self.file_path or not self.hash_value:
            messagebox.showerror("Erro", "Selecione um arquivo antes de salvar o hash.")
            return

        save_hash_data(self.file_path, self.hash_value)
        messagebox.showinfo("Sucesso", f"Hash salvo em {HASH_FILE.name}.")

    def verify_file(self):
        if not HASH_FILE.exists():
            messagebox.showerror("Erro", "Nenhum hash salvo encontrado. Clique em 'Salvar hash' primeiro.")
            return

        data = load_hash_data()
        saved_file_path = data.get("file_path", "")
        saved_hash_value = data.get("hash_value", "")

        if not saved_file_path or not os.path.exists(saved_file_path):
            messagebox.showerror("Erro", "O arquivo salvo não existe mais no caminho original.")
            return

        current_hash = calculate_hash(saved_file_path)

        if current_hash == saved_hash_value:
            messagebox.showinfo("Sucesso", "Integridade verificada. Nenhuma alteração detectada.")
        else:
            messagebox.showwarning("Atenção", "Arquivo modificado! A integridade foi comprometida.")


def main() -> int:
    if HAS_TKINTER:
        app = FIMApp()
        app.mainloop()
        return 0

    if _relaunch_with_tk_python():
        return 0

    print("Este Python não tem suporte a tkinter (_tkinter ausente).")
    print("Use um Python com Tk instalado, por exemplo: /usr/bin/python3")
    if TKINTER_ERROR is not None:
        print(f"Erro ao importar tkinter: {TKINTER_ERROR}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())