"""Tratamentos determinísticos e pipeline reutilizável do projeto Telco Churn."""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

SERVICOS = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
            "StreamingTV", "StreamingMovies"]
DOMINIOS = {
    "gender": ["Female", "Male"],
    "SeniorCitizen": [0, 1],
    "Partner": ["No", "Yes"], "Dependents": ["No", "Yes"],
    "PhoneService": ["No", "Yes"],
    "MultipleLines": ["No", "Yes", "No phone service"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    **{c: ["No", "Yes", "No internet service"] for c in SERVICOS},
    "Contract": ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": ["No", "Yes"],
    "PaymentMethod": ["Electronic check", "Mailed check",
                      "Bank transfer (automatic)", "Credit card (automatic)"],
}
NUMERICAS_ORIGINAIS = ["tenure", "MonthlyCharges", "TotalCharges"]
PREDITORES = list(DOMINIOS) + NUMERICAS_ORIGINAIS
NUMERICAS = NUMERICAS_ORIGINAIS + ["TotalChargesAusente", "ServicosAdicionais",
                                 "GastoMedioHistorico"]
CATEGORICAS = list(DOMINIOS)


def limpar_dados(dados):
    """Valida e limpa sem aprender estatísticas nem alterar a entrada.

    Aceita o CSV completo ou só os 19 preditores; preserva ID/alvo se presentes.
    Valores desconhecidos são rejeitados para não esconder erros de cadastro.
    Categorias ausentes, quando presentes, serão imputadas dentro do pipeline.
    """
    if not isinstance(dados, pd.DataFrame):
        raise TypeError("Forneça um pandas.DataFrame com os nomes das colunas.")
    faltantes = sorted(set(PREDITORES) - set(dados.columns))
    if faltantes:
        raise ValueError(f"Colunas obrigatórias ausentes: {faltantes}")
    df = dados.copy(deep=True)
    for c in df.columns:
        if pd.api.types.is_string_dtype(df[c]) or df[c].dtype == object:
            df[c] = df[c].astype(object).map(lambda x: x.strip() if isinstance(x, str) else x)
            df[c] = df[c].replace("", np.nan)
    for c in NUMERICAS_ORIGINAIS + ["SeniorCitizen"]:
        convertido = pd.to_numeric(df[c], errors="coerce")
        invalidos = df[c].notna() & convertido.isna()
        if invalidos.any():
            raise ValueError(f"{c}: texto não numérico em {int(invalidos.sum())} linhas.")
        if np.isinf(convertido.to_numpy(dtype=float, na_value=np.nan)).any():
            raise ValueError(f"{c}: valores infinitos não são permitidos.")
        df[c] = convertido.astype(float)
    if df[["tenure", "MonthlyCharges"]].isna().any().any():
        raise ValueError("tenure e MonthlyCharges são obrigatórios.")
    if (df[NUMERICAS_ORIGINAIS] < 0).any().any():
        raise ValueError("Permanência e cobranças devem ser não negativas.")
    if (df.tenure % 1 != 0).any():
        raise ValueError("tenure deve conter meses inteiros.")
    for c, dominio in DOMINIOS.items():
        desconhecidos = set(df[c].dropna().unique()) - set(dominio)
        if desconhecidos:
            raise ValueError(f"{c}: categorias desconhecidas: {desconhecidos}")
    if "customerID" in df:
        if df.customerID.isna().any() or df.customerID.duplicated().any():
            raise ValueError("customerID ausente ou duplicado: investigar antes de dividir.")
    if "Churn" in df:
        if df.Churn.isna().any() or not df.Churn.isin(["Yes", "No"]).all():
            raise ValueError("Churn deve conter apenas Yes/No, sem valores ausentes.")
    for c in SERVICOS:
        conhecidos = df.InternetService.notna() & df[c].notna()
        incoerente = conhecidos & (df.InternetService.eq("No") != df[c].eq("No internet service"))
        if incoerente.any():
            raise ValueError(f"{c}: inconsistência com InternetService.")
    conhecidos = df.PhoneService.notna() & df.MultipleLines.notna()
    if (conhecidos & (df.PhoneService.eq("No") != df.MultipleLines.eq("No phone service"))).any():
        raise ValueError("MultipleLines inconsistente com PhoneService.")
    df["TotalChargesAusente"] = df.TotalCharges.isna().astype(int)
    df.loc[df.TotalCharges.isna() & df.tenure.eq(0), "TotalCharges"] = 0.0
    # SeniorCitizen é nominal, embora venha como número no CSV.
    df["SeniorCitizen"] = df.SeniorCitizen.map({0: "No", 1: "Yes"})
    return df


def criar_atributos(dados):
    """Entrada bruta -> atributos sem ID/alvo; nenhuma estatística é ajustada."""
    df = limpar_dados(dados)
    df["ServicosAdicionais"] = df[SERVICOS].eq("Yes").sum(axis=1)
    df["GastoMedioHistorico"] = df.TotalCharges.div(df.tenure.where(df.tenure.gt(0)))
    return df[NUMERICAS + CATEGORICAS]


def montar_pipeline(modelo):
    numerico = Pipeline([
        ("imputar", SimpleImputer(strategy="median", keep_empty_features=True)),
        ("padronizar", StandardScaler()),
    ])
    categorico = Pipeline([
        ("imputar", SimpleImputer(strategy="most_frequent", keep_empty_features=True)),
        ("codificar", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return Pipeline([
        ("atributos", FunctionTransformer(criar_atributos, validate=False)),
        ("preprocessar", ColumnTransformer([
            ("numerico", numerico, NUMERICAS),
            ("categorico", categorico, CATEGORICAS),
        ], remainder="drop")),
        ("modelo", modelo),
    ])
