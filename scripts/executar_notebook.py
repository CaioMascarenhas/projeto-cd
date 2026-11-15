"""Execute com o Python do ambiente instalado; salva saídas mesmo em caso de erro."""
from pathlib import Path
import os
import sys
import asyncio

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager
from jupyter_client import AsyncKernelManager

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
# Kernel privado deste projeto; não modifica kernels globais do usuário.
kernel_dir = ROOT / "tmp" / "kernels" / "projeto-churn"
kernel_dir.mkdir(parents=True, exist_ok=True)
import json
(kernel_dir / "kernel.json").write_text(json.dumps({
    "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
    "display_name": "Python (projeto churn)", "language": "python",
}), encoding="utf-8")
ksm = KernelSpecManager(kernel_dirs=[str(kernel_dir.parent)])
km = AsyncKernelManager(kernel_name="projeto-churn", kernel_spec_manager=ksm)
path = ROOT / "projeto_churn.ipynb"
nb = nbformat.read(path, as_version=4)
client = NotebookClient(nb, km=km, timeout=1200, kernel_name="projeto-churn",
                        resources={"metadata": {"path": str(ROOT)}},
                        )
def informar(cell, cell_index, **kwargs):
    if cell.cell_type == "code":
        print(f"Executando célula {cell_index + 1}/{len(nb.cells)}", flush=True)
client.on_cell_start = informar
try:
    client.execute(cleanup_kc=True)
finally:
    nbformat.write(nb, path)
print(f"Notebook executado: {path}")
