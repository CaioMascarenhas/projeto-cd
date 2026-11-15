"""Verificações significativas dos dados, do experimento e do artefato exportado."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import joblib
import nbformat
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from sklearn.model_selection import StratifiedKFold
from telco_pipeline import PREDITORES, NUMERICAS, limpar_dados, criar_atributos


def rejeitar(entrada, mensagem):
    try:
        limpar_dados(entrada)
    except ValueError:
        return
    raise AssertionError(mensagem)


raw = pd.read_csv(ROOT / "WA_Fn-UseC_-Telco-Customer-Churn.csv")
original = raw.copy(deep=True)
limpos = limpar_dados(raw)
atributos = criar_atributos(raw)
assert_frame_equal(raw, original)
assert len(raw) == 7043 and raw.shape[1] == 21
assert raw.customerID.is_unique and not raw.duplicated().any()
assert len(atributos) == len(raw)
assert not {"customerID", "Churn"} & set(atributos.columns)
ausentes = pd.to_numeric(raw.TotalCharges, errors="coerce").isna()
assert ausentes.sum() == 11
assert raw.loc[ausentes, "tenure"].eq(0).all()
assert limpos.loc[ausentes, "TotalCharges"].eq(0).all()
assert limpos.loc[ausentes, "TotalChargesAusente"].eq(1).all()
assert atributos.loc[ausentes, "GastoMedioHistorico"].isna().all()
assert "No internet service" in set(limpos.OnlineSecurity)
assert not np.isinf(atributos[NUMERICAS].to_numpy(dtype=float)).any()

# Cenários diferentes da base fornecida: não esconder erro nem imputar globalmente.
caso = raw.iloc[[0]].copy()
caso["TotalCharges"] = " "
assert caso.tenure.iloc[0] > 0
assert limpar_dados(caso).TotalCharges.isna().all()
assert criar_atributos(caso).GastoMedioHistorico.isna().all()
invalido = raw.iloc[[0]].copy()
invalido["TotalCharges"] = "texto inválido"
rejeitar(invalido, "Texto inválido foi aceito como nulo silenciosamente.")
invalido = raw.iloc[[0]].copy()
invalido["MonthlyCharges"] = -1
rejeitar(invalido, "Cobrança negativa foi aceita.")
invalido = raw.iloc[[0]].copy()
invalido["InternetService"] = "No"
rejeitar(invalido, "Serviços incoerentes foram aceitos.")
rejeitar(pd.concat([raw.iloc[[0]], raw.iloc[[0]]]), "ID duplicado foi aceito.")
rejeitar(raw.drop(columns="Contract"), "Esquema incompleto foi aceito.")
print("OK: dados preservados, ausência estrutural, divisão por zero e erros de cadastro.")

nb = nbformat.read(ROOT / "projeto_churn.ipynb", as_version=4)
nbformat.validate(nb)
codigos = [c for c in nb.cells if c.cell_type == "code"]
assert codigos and all(c.execution_count is not None for c in codigos), "Notebook não executado integralmente."
assert not [o for c in codigos for o in c.outputs if o.output_type == "error"]
for c in codigos:
    compile(c.source, "notebook", "exec")
print(f"OK: notebook válido, {len(codigos)} células de código executadas sem erros.")

out = ROOT / "outputs"
meta = json.loads((out / "metadados.json").read_text(encoding="utf-8"))
assert meta["sha256_csv"] == hashlib.sha256((ROOT / meta["csv"]).read_bytes()).hexdigest()
particoes = pd.read_csv(out / "tabelas" / "particoes.csv")
assert particoes.customerID.is_unique
assert set(particoes.customerID) == set(raw.customerID)
assert set(particoes.particao) == {"treino", "validacao", "teste"}
for nome, n in meta["particoes"].items():
    assert particoes.particao.eq(nome).sum() == n
treino_ids = set(particoes.loc[particoes.particao.eq("treino"), "customerID"])
teste_ids = set(particoes.loc[particoes.particao.eq("teste"), "customerID"])
assert not treino_ids & teste_ids
print("OK: hash do CSV, cobertura e exclusividade das partições.")

artefato = joblib.load(out / "modelo_churn.joblib")
assert np.isclose(artefato["limiar"], meta["limiar"])
ranking = pd.read_csv(out / "tabelas" / "ranking_teste_retrospectivo.csv")
assert set(ranking.customerID) == teste_ids
entrada = raw.set_index("customerID").loc[ranking.customerID, PREDITORES]
prob = artefato["pipeline"].predict_proba(entrada)[:, 1]
np.testing.assert_allclose(prob, ranking.probabilidade, rtol=1e-10, atol=1e-12)
np.testing.assert_array_equal(prob >= meta["limiar"], ranking.decisao_limiar.to_numpy(dtype=bool))
np.testing.assert_array_equal(raw.set_index("customerID").loc[ranking.customerID, "Churn"].eq("Yes"),
                              ranking.churn_real.to_numpy(dtype=bool))
print("OK: recarga do modelo em processo separado reproduz todas as previsões do teste.")

# Auditar o ajuste: cada imputador do calibrador deve ter aprendido no seu fold de treino.
# Recriar a ordem original do train_test_split a partir do protocolo, não da tabela ordenada por ID.
from sklearn.model_selection import train_test_split
y = raw.Churn.eq("Yes").astype(int)
dev, _ = train_test_split(raw.index.to_numpy(), test_size=.2, stratify=y, random_state=42)
tr, _ = train_test_split(dev, test_size=.25, stratify=y.loc[dev], random_state=42)
assert set(raw.loc[tr, "customerID"]) == treino_ids
xt = raw.loc[tr, PREDITORES]
yt = y.loc[tr]
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=43)
for calibrado, (fit_ix, _) in zip(artefato["pipeline"].calibrated_classifiers_, cv.split(xt, yt)):
    pipe = calibrado.estimator
    imputer = pipe.named_steps["preprocessar"].named_transformers_["numerico"].named_steps["imputar"]
    esperado = criar_atributos(xt.iloc[fit_ix])[NUMERICAS].median().to_numpy()
    np.testing.assert_allclose(imputer.statistics_, esperado, equal_nan=True)
print("OK: medianas dos três pipelines calibrados correspondem apenas aos respectivos folds de treino.")

hip = pd.read_csv(out / "tabelas" / "testes_hipoteses.csv")
assert set(hip.hipotese) == {"H1", "H2", "H3", "H4"}
assert (hip.p_holm >= hip.p_valor - 1e-12).all()
assert len(list((out / "figuras").glob("*.png"))) == 11
assert all(p.stat().st_size > 5000 for p in (out / "figuras").glob("*.png"))
print("OK: quatro hipóteses corrigidas e 11 figuras exportadas.")
print("Todas as verificações passaram.")
