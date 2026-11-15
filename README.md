# Projeto de Ciência de Dados — Telco Customer Churn

O ponto de entrada é [`projeto_churn.ipynb`](projeto_churn.ipynb). O notebook está em português e cobre auditoria, limpeza, engenharia de atributos, EDA, as quatro hipóteses da proposta, comparação de modelos, calibração, escolha de limiar, avaliação e recomendações. Os resultados ficam salvos no próprio notebook e em `outputs/`.

Foram lidos integralmente os dois PDFs locais e a proposta inicial do Google Docs, copiada para `docs/proposta_inicial.txt`. O convite do Overleaf retornou erro de acesso; o texto do artigo remoto não foi lido. O semestre diverge entre o nome do PDF e a proposta. Nenhum prazo foi inferido.

## Executar no Windows

Recomendado: Python 3.11. Na pasta deste projeto, abra o PowerShell e execute:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m jupyterlab projeto_churn.ipynb
```

No notebook, selecione o Python da `.venv` e execute **Restart Kernel and Run All**. A execução começa pelo CSV original e recria as saídas. Não é necessário ativar a `.venv` nem alterar a política de execução do PowerShell. Se a `.venv` já existe e está instalada, basta usar o terceiro comando.

Para executar tudo sem abrir a interface:

```powershell
.\.venv\Scripts\python.exe scripts/executar_notebook.py
.\.venv\Scripts\python.exe scripts/verificar_projeto.py
```

O executor usa um kernel privado em `tmp/kernels/` com o mesmo Python do comando. Não altera os kernels globais. Caso alguma célula falhe, salva as saídas e o erro no notebook para diagnóstico. O tempo depende da máquina; há 5 folds para seleção e 3 para calibração, com paralelismo limitado para portabilidade.

No VS Code, abra a pasta do projeto e selecione `.venv\Scripts\python.exe` como kernel. `requirements-lock.txt` registra o ambiente completo validado **no Windows**, incluindo dependências de plataforma.

## Executar no Google Colab

1. Acesse https://colab.research.google.com/ e abra `projeto_churn.ipynb` pela opção de enviar notebook.
2. Execute a seção **0. Preparação para Google Colab**. Quando aparecer o seletor, envie juntos `telco_pipeline.py` e `WA_Fn-UseC_-Telco-Customer-Churn.csv`, com esses nomes originais.
3. A preparação aproveita bibliotecas compatíveis já instaladas e instala apenas as ausentes/incompatíveis. Se pedir reinício após instalação, reinicie a sessão e execute novamente desde o começo.
4. Execute as demais células na ordem, ou use **Executar tudo** e aguarde o envio dos arquivos quando solicitado. Pode usar CPU: os algoritmos implementados não utilizam GPU.
5. Ao final, a seção **13. Baixar resultados no Colab** gera e baixa `resultados_churn.zip`, com `outputs/` e o módulo necessário para recarregar o modelo. Salve também o notebook com as saídas pelo menu de download do Colab.

Não é preciso enviar PDFs, `AGENTS.md`, `.venv`, `requirements-lock.txt` ou resultados antigos para executar a análise. As referências documentais já estão explicadas no notebook. Os arquivos enviados e gerados ficam no armazenamento temporário da sessão; baixe os resultados antes de encerrá-la.

O Colab usa faixas de versões compatíveis, registradas na primeira célula, em vez do lock do Windows. As versões realmente usadas ficam em `outputs/metadados.json`; resultados podem variar entre versões/plataformas. A execução local foi validada e o fluxo específico do Colab foi verificado por simulação; não houve execução autenticada no serviço do Google.

Referências oficiais: [FAQ do Colab](https://research.google.com/colaboratory/faq.html) e [implementação de upload/download](https://github.com/googlecolab/colabtools/blob/main/google/colab/files.py).

## O que foi tratado

- 7.043 clientes, 21 colunas e 19 preditores originais. O CSV original é preservado.
- Espaços em branco em `TotalCharges` viram ausência numérica. Os 11 casos com permanência zero recebem acumulado zero por uma hipótese de domínio explícita, mantendo indicador da ausência original. Outros nulos são imputados pela mediana no treino.
- `SeniorCitizen` é categórica. “Sem internet/telefone” permanece distinto de “não contratou”. IDs, alvo, valores negativos, categorias desconhecidas e combinações de serviços incoerentes são validados.
- Contagem de seis serviços adicionais e gasto acumulado por mês, sem divisão por zero.
- Imputação, one-hot e padronização dentro de cada fold do pipeline; extremos plausíveis são mantidos.

## Avaliação e decisões

A divisão estratificada usa semente 42 e aproximadamente 60% treino, 20% validação e 20% teste. EDA e inferência usam apenas o treino. H1–H4 recebem testes bilaterais, correção de Holm, tamanhos de efeito e intervalos de confiança.

Dummy, Regressão Logística, Árvore, Random Forest e HistGradientBoosting são comparados por average precision em CV de 5 folds. O boosting nativo evita dependências adicionais de XGBoost/LightGBM. O vencedor recebe calibração sigmoid em CV de 3 folds no treino e limiar F2 escolhido na validação. O teste final avalia a solução congelada e a referência Dummy. O modelo não é reajustado com validação/teste após escolher o limiar.

As recomendações têm evidência, ação, prazo e indicador. A simulação financeira usa premissas hipotéticas e unidades monetárias da base. Captura retrospectiva de churn não significa cancelamento evitado. Sem datas e janela de previsão, o notebook não comprova desempenho antecipatório em produção nem efeito causal de uma campanha.

## Arquivos importantes

| Arquivo | Uso |
|---|---|
| `projeto_churn.ipynb` | Análise completa, código e resultados |
| `AGENTS.md` | Contexto, fontes, requisitos e regras para manutenção |
| `telco_pipeline.py` | Tratamentos reutilizáveis e pipeline serializável |
| `docs/proposta_inicial.txt` | Cópia textual da proposta consultada |
| `docs/fontes_e_requisitos.md` | Fontes lidas, limitações de acesso e rastreabilidade |
| `requirements.txt` | Versões diretas validadas |
| `requirements-lock.txt` | Ambiente Windows completo |
| `scripts/executar_notebook.py` | Execução integral e salvamento com nbclient |
| `scripts/verificar_projeto.py` | Integridade, casos de tratamento, partições e recarga |

## Saídas geradas

| Caminho em `outputs/` | Conteúdo |
|---|---|
| `dados_limpos.csv` | Tabela com limpeza determinística, ID/alvo e indicador de ausência; sem imputação estatística global |
| `figuras/` | 11 gráficos PNG para análise e apresentação |
| `tabelas/` | Auditoria, dicionário, estatísticas, hipóteses, CV, teste, ICs, captura, interpretação e cenários |
| `resumo_resultados.md` | Síntese calculada a partir da execução |
| `metadados.json` | Hash do CSV, versões, parâmetros, partições, limiar e métricas |
| `modelo_churn.joblib` | Pipeline calibrado e limiar; manter `telco_pipeline.py` junto ao projeto |
| `exemplo_entrada.csv` | Exemplo dos 19 preditores brutos aceitos pelo modelo |

Exemplo de recarga, depois da execução:

```python
import joblib
import pandas as pd

artefato = joblib.load("outputs/modelo_churn.joblib")
clientes = pd.read_csv("outputs/exemplo_entrada.csv")
probabilidades = artefato["pipeline"].predict_proba(clientes)[:, 1]
sinalizados = probabilidades >= artefato["limiar"]
```

Use apenas artefatos joblib gerados por você ou de origem confiável. A entrada deve ter o esquema bruto do CSV; não envie `dados_limpos.csv` como se fosse entrada bruta, pois `SeniorCitizen` já foi transformada. O ranking exportado é uma avaliação retrospectiva do teste, não uma lista de clientes ativos para contato real.

O notebook fornece os experimentos e evidências para o artigo SBC de até 12 páginas. O artigo final e o Streamlit planejado na proposta são entregáveis separados.

## Apresentação dos resultados

O pedido posterior do grupo definiu uma apresentação de até 10 minutos. A versão preparada tem 11 slides e roteiro de 9 minutos, com uma margem para pausas:

- [Slides editáveis](output/apresentacao/apresentacao_churn_final.pptx), com notas de fala, gráficos e tabelas editáveis.
- [PDF para apresentar](output/pdf/apresentacao_churn_final.pdf).
- [Roteiro de fala](output/apresentacao/roteiro_fala.md), com tempo por slide e respostas para perguntas comuns.

A sequência apresenta objetivo, preparação, quatro hipóteses, comparação dos modelos, resultados no teste, prioridade de contato, ações e limites. O limite de 10 minutos solicitado pelo grupo substitui, para este material, o tempo maior descrito nos PDFs da disciplina.
