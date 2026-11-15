"""Verifica o fluxo Colab em diretório temporário, sem acessar o serviço Google."""
from contextlib import contextmanager
from importlib import metadata
from pathlib import Path
import os
import sys
import tempfile
from types import ModuleType
from unittest.mock import Mock, patch
from zipfile import ZipFile

import nbformat

ROOT = Path(__file__).resolve().parents[1]
nb = nbformat.read(ROOT / "projeto_churn.ipynb", as_version=4)
def fonte(tag):
    return next(c.source for c in nb.cells if tag in c.metadata.get("tags", []))

preparar = compile(fonte("colab-preparacao"), "colab-preparacao", "exec")
baixar = compile(fonte("colab-download"), "colab-download", "exec")
necessarios = ["telco_pipeline.py", "WA_Fn-UseC_-Telco-Customer-Churn.csv"]


@contextmanager
def ambiente():
    anterior = Path.cwd()
    with tempfile.TemporaryDirectory(prefix="churn-colab-") as tmp:
        os.chdir(tmp)
        google = ModuleType("google")
        colab = ModuleType("google.colab")
        arquivos = ModuleType("google.colab.files")
        arquivos.upload = Mock()
        arquivos.download = Mock()
        colab.files = arquivos
        google.colab = colab
        try:
            with patch.dict(sys.modules, {"google": google, "google.colab": colab,
                                          "google.colab.files": arquivos}):
                yield Path(tmp), arquivos
        finally:
            os.chdir(anterior)


with ambiente() as (tmp, arquivos), patch("subprocess.check_call") as pip:
    def enviar():
        for nome in necessarios:
            (tmp / nome).write_bytes((ROOT / nome).read_bytes())
        return {nome: (tmp / nome).read_bytes() for nome in necessarios}
    arquivos.upload.side_effect = enviar
    contexto = {}
    exec(preparar, contexto)
    assert contexto["NO_COLAB"]
    assert all((tmp / nome).is_file() for nome in necessarios)
    arquivos.upload.assert_called_once()
    pip.assert_not_called()
    exec(preparar, contexto)
    arquivos.upload.assert_called_once()  # Não solicita de novo arquivos já presentes.
    print("OK: upload inicial e reexecução sem sobrescrever arquivos existentes.")

    contexto.update(ROOT=tmp, OUT=tmp / "outputs")
    try:
        exec(baixar, contexto)
    except RuntimeError as erro:
        assert "Execute todas" in str(erro)
    else:
        raise AssertionError("Download aceitou resultados incompletos.")
    contexto["OUT"].mkdir()
    (contexto["OUT"] / "metadados.json").write_text("{}", encoding="utf-8")
    (contexto["OUT"] / "modelo_churn.joblib").write_bytes(b"fixture")
    exec(baixar, contexto)
    zip_path = tmp / "resultados_churn.zip"
    arquivos.download.assert_called_once_with(str(zip_path))
    with ZipFile(zip_path) as pacote:
        assert set(pacote.namelist()) == {
            "outputs/metadados.json", "outputs/modelo_churn.joblib", "telco_pipeline.py"}
        assert pacote.read("telco_pipeline.py") == (ROOT / "telco_pipeline.py").read_bytes()
    print("OK: resultados incompletos bloqueados; ZIP contém resultados e módulo reutilizável.")

with ambiente() as (_, arquivos), patch("subprocess.check_call"):
    arquivos.upload.return_value = {}
    try:
        exec(preparar, {})
    except FileNotFoundError as erro:
        assert all(nome in str(erro) for nome in necessarios)
    else:
        raise AssertionError("Upload cancelado não apontou arquivos ausentes.")
    print("OK: cancelamento de upload informa os nomes necessários.")

versao_real = metadata.version
def versao_antiga(nome):
    return "1.3.0" if nome == "scikit-learn" else versao_real(nome)

with ambiente() as (_, arquivos), patch("subprocess.check_call") as pip:
    with patch("importlib.metadata.version", side_effect=versao_antiga), \
         patch.dict(sys.modules, {"sklearn": ModuleType("sklearn")}):
        try:
            exec(preparar, {})
        except RuntimeError as erro:
            assert "Reinicie" in str(erro) and "sklearn" in str(erro)
        else:
            raise AssertionError("Atualização de biblioteca importada não exigiu reinício.")
    pip.assert_called_once()
    comando = pip.call_args.args[0]
    assert comando[:3] == [sys.executable, "-m", "pip"]
    assert comando[-1] == "scikit-learn>=1.4,<2"
    arquivos.upload.assert_not_called()
    print("OK: dependência antiga é atualizada e biblioteca carregada exige reinício.")

print("Fluxo Colab verificado por simulação; não executado no serviço do Google.")
