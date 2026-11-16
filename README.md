# Análise de churn em telecomunicações

Projeto de Ciência de Dados da **UFAL / Instituto de Computação**, com a base IBM Telco Customer Churn. Estudamos quais perfis apresentam mais cancelamentos e como organizar uma lista de risco para priorizar ações de retenção.

## Do que se trata este repositório?

**Churn significa quando um cliente cancela um serviço.** Pense em alguém que deixa de usar sua operadora de telefone ou internet.

Este repositório reúne um trabalho de graduação que busca responder: **quais características aparecem com mais frequência entre os clientes que cancelaram e como identificar perfis com maior risco de cancelamento?** A ideia é ajudar uma empresa a decidir quais clientes merecem atenção primeiro, quando ela não consegue entrar em contato com todos.

Usamos uma base de estudo com informações de **7.043 clientes**, como tipo de contrato, tempo na empresa, valor da conta, serviços contratados e registro de cancelamento. Os dados já estavam disponíveis; não fizemos uma pesquisa com clientes nem executamos uma campanha real.

O trabalho percorre estas etapas:

1. **Conferir e tratar os dados:** verificar informações vazias e preparar os campos para a análise.
2. **Entender os cancelamentos:** comparar grupos de clientes e investigar as quatro hipóteses da proposta inicial.
3. **Comparar modelos:** testar métodos que calculam uma pontuação de risco a partir das características dos clientes.
4. **Avaliar os resultados:** medir quantos cancelamentos o modelo encontra, quantos alertas ele erra e como o ranking funciona com uma quantidade limitada de contatos.
5. **Comunicar as conclusões:** reunir os resultados no notebook, no artigo e nos slides da apresentação.

**O principal resultado:** no conjunto reservado para avaliação, os 20% de clientes com maior pontuação concentraram cerca de 49% dos cancelamentos. Isso indica que o ranking pode ajudar a priorizar a atenção. Ainda seria preciso testar a estratégia com dados novos e clientes ativos para saber se ela realmente reduz cancelamentos.

Para **entender o trabalho**, comece pelo artigo ou pelos slides abaixo. Para **reproduzir a análise**, abra o notebook no Colab e siga as instruções deste README.

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CaioMascarenhas/projeto-cd/blob/main/projeto_churn.ipynb)

## Entregas

| Material | Conteúdo |
|---|---|
| [Notebook executado](projeto_churn.ipynb) | Tratamentos, quatro hipóteses e comparação dos modelos |
| [Artigo em PDF](output/pdf/artigo_churn_atualizado.pdf) | Relatório SBC com 9 páginas |
| [Código LaTeX](output/overleaf/main.tex) | Texto e tabelas do artigo |
| [Pacote para Overleaf](output/overleaf/artigo_atualizado.zip) | LaTeX, estilo SBC e duas figuras |
| [Apresentação em PDF](output/pdf/apresentacao_churn_final.pdf) | 11 slides para até 10 minutos |
| [Slides editáveis](output/apresentacao/apresentacao_churn_final.pptx) | PowerPoint com gráficos, tabelas e notas de fala |
| [Roteiro](output/apresentacao/roteiro_fala.md) | Planejamento de 9 minutos e apoio para perguntas |
| [Resumo dos resultados](outputs/resumo_resultados.md) | Síntese da execução validada |

## Resultados principais

A base contém **7.043 clientes**, 21 colunas e **26,54% de churn**. Contrato mensal, permanência curta, falta de segurança/suporte na fibra e cheque eletrônico entre faturas altas apresentaram associação com mais cancelamentos no treino, após correção de Holm.

A Random Forest obteve a maior average precision (AP) na validação cruzada, com diferença pequena para a Regressão Logística. Após calibração, no teste reservado:

| Indicador | Resultado |
|---|---:|
| ROC-AUC | 0,843 |
| Average precision (AP) | 0,654 |
| Revocação no corte F2 | 93,6% |
| Precisão nesse corte | 41,7% |
| Clientes sinalizados nesse corte | 59,5% |
| Captura nos 20% de maior risco | 49,2% dos churns |
| Precisão nesses 20% | 65,2% |

O corte F2 encontrou 350 dos 374 churns do teste, com 489 falsos positivos. Sua acurácia foi 63,6%, abaixo dos 73,5% de sempre prever não churn. AUC e AP não são porcentagens de acertos. Os resultados mostram a troca entre detecção, quantidade de contatos e precisão.

A análise é retrospectiva e observacional. Ela não comprova antecipação em produção, efeito causal das ofertas ou lucro de campanha. A simulação financeira usa premissas hipotéticas e unidades monetárias da base. Propomos um piloto prospectivo com grupo controle.

## Google Colab

1. Clique em **Abrir no Colab** e execute a seção **0**.
2. Quando solicitado, envie [telco_pipeline.py](telco_pipeline.py) e [o CSV original](WA_Fn-UseC_-Telco-Customer-Churn.csv), mantendo os nomes.
3. A preparação aproveita bibliotecas compatíveis e instala apenas as ausentes/incompatíveis. Se pedir reinício, reinicie a sessão e execute desde o começo.
4. Use **Executar tudo**, com **CPU**, sem necessidade de GPU.
5. A seção **13** baixa os resultados em ZIP. Salve também o notebook com as saídas.

Não é preciso enviar PDFs, `.venv` ou o lock do Windows. O armazenamento da sessão é temporário. As versões efetivas ficam em `outputs/metadados.json`. O fluxo específico de upload/download foi testado por simulação; as execuções integrais validadas ocorreram localmente.

## Executar localmente

Use **Python 3.11** e execute os comandos na raiz do projeto.

### Windows / PowerShell

```powershell
git clone https://github.com/CaioMascarenhas/projeto-cd.git
cd projeto-cd
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/executar_notebook.py
.\.venv\Scripts\python.exe scripts/verificar_projeto.py
.\.venv\Scripts\python.exe scripts/verificar_colab.py
```

Para abrir a interface:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab projeto_churn.ipynb
```

### Linux / macOS

```bash
git clone https://github.com/CaioMascarenhas/projeto-cd.git
cd projeto-cd
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/executar_notebook.py
.venv/bin/python scripts/verificar_projeto.py
.venv/bin/python scripts/verificar_colab.py
```

O executor usa um kernel privado em `tmp/kernels/` com o mesmo Python do comando. O notebook salva as saídas, inclusive em caso de erro para diagnóstico. A execução gera `outputs/modelo_churn.joblib`, que fica fora do Git. Execute o notebook antes da verificação completa do modelo.

`requirements.txt` fixa as dependências diretas validadas. `requirements-lock.txt` registra o ambiente completo do **Windows**; não o instale diretamente no Colab ou Linux. A verificação automática no GitHub usa Python 3.11 no Linux.

## Preparação e avaliação

- O CSV original é preservado. Os 11 espaços em branco em `TotalCharges`, todos com `tenure=0`, recebem acumulado zero por regra explícita de domínio, mantendo indicador da ausência original.
- `SeniorCitizen` é categórica. Estados “sem internet/telefone” continuam distintos de “não contratou”. IDs e combinações de serviços são validados.
- Criamos contagem de seis serviços adicionais e gasto acumulado por mês, sem divisão por zero. Extremos plausíveis são mantidos.
- Semente 42 e divisão estratificada: **4.225 no treino, 1.409 na validação e 1.409 no teste**. EDA e inferência usam o treino.
- Imputação, one-hot e padronização são ajustados dentro de cada fold.
- Dummy, Logística, Árvore, Random Forest e HistGradientBoosting são comparados por AP em CV de 5 folds. O vencedor recebe calibração sigmoid em 3 folds do treino. A validação escolhe o limiar F2.
- O teste avalia a solução congelada e a referência. Não há reajuste com validação/teste após escolher o limiar.

## Organização

```text
projeto_churn.ipynb       Análise completa e resultados salvos
telco_pipeline.py        Tratamentos e pipeline reutilizável
scripts/                 Execução, verificações e geração do artigo
docs/                    Proposta inicial e rastreabilidade das fontes
outputs/                 Tabelas, 11 figuras, dados limpos e metadados
output/overleaf/          Fontes e pacote do artigo SBC
output/pdf/              PDFs do artigo e da apresentação
output/apresentacao/     Slides editáveis e roteiro
AGENTS.md                Orientações de manutenção e metodologia
```

`outputs/` armazena os resultados computacionais; `output/` reúne os materiais de entrega. Temporários, ambientes virtuais, modelos serializados, backups privados e tokens de convite não devem ser versionados.

### Reutilizar o modelo

Depois de executar o notebook, mantenha `telco_pipeline.py` disponível e forneça os **19 preditores brutos**:

```python
import joblib
import pandas as pd

artefato = joblib.load("outputs/modelo_churn.joblib")
clientes = pd.read_csv("outputs/exemplo_entrada.csv")
probabilidades = artefato["pipeline"].predict_proba(clientes)[:, 1]
sinalizados = probabilidades >= artefato["limiar"]
```

Use apenas artefatos joblib de origem confiável. `dados_limpos.csv` é uma saída de auditoria, não a entrada bruta desse pipeline. O ranking exportado descreve o teste, não uma campanha com clientes ativos.

### Atualizar o artigo

```powershell
.\.venv\Scripts\python.exe scripts/preparar_artigo.py
```

O comando usa as saídas do notebook para gerar o LaTeX, duas figuras e o ZIP. Não compila o PDF nem publica no Overleaf. Compile o pacote no Overleaf, confira o limite de 12 páginas e atualize o PDF exportado. O PDF incluído tem 9 páginas, compiladas no Overleaf e revisadas visualmente. Mudanças nos resultados também exigem revisar os slides e o roteiro.

## Equipe e fontes

**Equipe:** Arthur Vinicius Ferreira Rodrigues, Caio Mascarenhas Soares, Mírian Natália Gomes dos Santos e Vinicius Albuquerque Sales de Alencar. **Docente:** Prof. Dr. Bruno Almeida Pimentel.

Base: [IBM Telco Customer Churn no Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). As condições de uso dos dados e do template SBC pertencem às fontes originais; este repositório não atribui uma nova licença a esses materiais.

Os PDFs da disciplina e a proposta orientaram o trabalho. Veja [fontes e requisitos](docs/fontes_e_requisitos.md). O nome de um PDF e a proposta divergem quanto ao semestre; nenhum calendário foi inferido. O artigo e os slides estão concluídos. Streamlit e validação em produção permanecem como trabalhos futuros.
