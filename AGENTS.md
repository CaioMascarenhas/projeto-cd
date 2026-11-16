# Orientações do projeto

## Contexto e fontes

- Projeto de Ciência de Dados da UFAL/IC, docente Bruno Almeida Pimentel.
- Equipe na proposta: Arthur Vinicius Ferreira Rodrigues, Caio Mascarenhas Soares, Mírian Natália Gomes dos Santos e Vinicius Albuquerque Sales de Alencar.
- Leia `Projeto (2026-1).pdf` (11 páginas), `Aula_cd_projeto.pdf` (19 páginas) e `docs/proposta_inicial.txt` antes de alterar o escopo. O último é uma cópia textual do Google Docs indicado em `nossodocinicial.txt`, obtida em 15/11/2026.
- Há divergência de identificação do semestre: nome do PDF menciona 2026-1, proposta menciona 2026.2. Não resolver por suposição nem inventar prazos.
- `overleaf.txt` contém apenas o endereço do projeto, sem token de convite. A leitura pública inicialmente falhou, mas o usuário autorizou depois acesso pelo Chrome e atualização do projeto. O LaTeX foi lido integralmente, copiado para `docs/overleaf_backup/` e atualizado no Overleaf com permissão de edição. O backup é privado e ignorado pelo Git. Novas mudanças devem preservar a cópia original e o trabalho atual.
- Fonte da base declarada pela equipe: IBM Telco Customer Churn, distribuída em https://www.kaggle.com/datasets/blastchar/telco-customer-churn . O notebook usa apenas o CSV local, sem download em tempo de execução.

## Objetivo e requisitos

- Explicar associações com churn e avaliar classificação para priorizar retenção; não alegar causalidade ou ganhos reais sem experimento.
- Base original: `WA_Fn-UseC_-Telco-Customer-Churn.csv`, 7.043 clientes, 21 colunas, 19 preditores originais + alvo `Churn` + identificador `customerID`.
- Auditoria inicial: 1.869 `Yes`, 5.174 `No`, 11 espaços em branco em `TotalCharges`, todos com `tenure == 0`; nenhum ID ou registro completo duplicado.
- Não modificar ou substituir o CSV nem os PDFs originais. Não remover perfis repetidos de clientes distintos como se fossem duplicatas.
- Hipóteses: H1 contrato mensal; H2 permanência até 12 meses; H3 fibra sem segurança ou suporte; H4 fatura alta + cheque eletrônico versus pagamento automático com fatura alta. Definições exatas estão no notebook.
- Disciplina exige EDA, inferência, justificativa de métodos/métricas/avaliação e pelo menos três insights acionáveis, com evidência, ação e indicador de sucesso.
- Relatório final: modelo SBC, máximo 12 páginas. Apresentação: pitch de 5 minutos e técnica de 15 minutos. Entrega final inclui PDF, código, apresentação e adicionais em ZIP/RAR. A proposta é até 2 páginas. Datas devem ser conferidas no Classroom.
- Dashboard/Streamlit é recurso adicional planejado na proposta, não requisito do notebook e não implementado aqui. Gradient boosting do scikit-learn substitui a dependência opcional XGBoost/LightGBM, com justificativa no notebook.

## Arquivos e execução

- `projeto_churn.ipynb`: roteiro executável em português, com resultados salvos.
- `telco_pipeline.py`: validação, limpeza determinística, engenharia de atributos e pipeline serializável. Deve acompanhar o notebook e o modelo exportado.
- `requirements.txt`: versões diretas do ambiente validado; `requirements-lock.txt`: ambiente completo.
- `README.md`: instalação, execução e mapa das saídas.
- `scripts/executar_notebook.py`: executa e salva o notebook via nbclient, usando o mesmo Python do script.
- `scripts/verificar_projeto.py`: verificações de integridade, tratamentos, divisão e recarga do modelo.
- `outputs/`: tabelas, figuras, dados limpos, modelo e metadados gerados; nunca usar essas saídas como entrada de treinamento.
- Windows: `py -3.11 -m venv .venv`, `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, `.\.venv\Scripts\python.exe scripts/executar_notebook.py`.
- Validar: `.\.venv\Scripts\python.exe scripts/verificar_projeto.py`.
- Kernel: Python 3.11 ou superior; usar o ambiente instalado. Na execução local, não instalar pacotes automaticamente no notebook.
- Colab: a seção 0 prepara dependências ausentes/incompatíveis e oferece upload do CSV original e de `telco_pipeline.py`. A instalação foi autorizada pelo usuário ao solicitar a adaptação para Colab. Usa os pacotes compatíveis já presentes, sem aplicar o lock do Windows. Se atualizar uma biblioteca já importada, interrompe com instrução de reiniciar a sessão.
- A seção 13 baixa `outputs/` e `telco_pipeline.py` em ZIP no Colab; os arquivos da sessão são temporários. `scripts/verificar_colab.py` verifica os ramos de preparação, upload e download por simulação, sem afirmar que o runtime real do Google foi executado.

## Regras metodológicas

- Semente 42. Divisão estratificada por cliente: aproximadamente 60% treino, 20% validação de limiar, 20% teste final; grupos sem interseção.
- EDA e inferência apenas no treino. Auditoria estrutural e prevalência global podem inspecionar o arquivo completo.
- Comparar Dummy, Regressão Logística, Árvore, Random Forest e HistGradientBoosting. Selecionar por average precision em CV estratificada de 5 folds no treino. Não confundir AP com área trapezoidal sob a curva PR.
- Imputação, codificação e escalonamento devem ser ajustados dentro de cada fold, por `Pipeline`/`ColumnTransformer`. Nunca ajustar transformações com validação/teste.
- Converter `TotalCharges` para número. Valor ausente com tenure zero recebe zero por regra explícita de domínio; outros ausentes continuam para imputação pela mediana aprendida no treino. Preservar indicador de ausência original. Nunca dividir por zero.
- Preservar `No internet service` e `No phone service` como estados distintos de `No`; `SeniorCitizen` é categórica; `customerID` e `Churn` não entram nos preditores.
- Auditar extremos por IQR no treino, sem excluir valores plausíveis automaticamente.
- Usar pesos de classe como candidatos nos algoritmos compatíveis, sem SMOTE pré-divisão.
- Calibração sigmoid com CV de 3 folds somente no treino, após seleção. Escolher limiar por F2 na validação. Não reajustar no treino+validação depois: isso mudaria a escala sobre a qual o limiar foi escolhido.
- Teste final avalia apenas a solução congelada e a referência Dummy. Não escolher modelo/limiar a partir do teste. Permutação para interpretação usa validação, não teste.
- H1-H4: testes bilaterais com correção de Holm na família de quatro testes, tamanhos de efeito e ICs. Mann-Whitney é análise complementar, rotulada exploratória. Associação observacional não implica efeito de intervenção.
- Não inventar séries temporais: não há datas/horizonte futuro explícito. A base não valida capacidade de antecipação em produção.
- Simulação financeira deve explicitar custo, margem, horizonte e eficácia hipotéticos. `MonthlyCharges` é faturamento, não lucro; valores monetários em unidades da base, sem conversão para reais. Não tratar cancelamentos passados como clientes ativos para uma campanha real.
- Reexecutar do início ao fim após mudanças na lógica. Conferir imagens e saídas. Registrar versão, hash do CSV, partições, parâmetros e limiar. Não carregar arquivos joblib de terceiros.

## Resultados de referência

- Execução da base fornecida em 15/11/2026: Random Forest selecionada por AP em CV (0,672), com 180 árvores, profundidade 8, folha mínima 5 e sem pesos de classe; depois calibrada no treino.
- Teste independente: ROC-AUC 0,843, AP 0,654; limiar F2 da validação aproximadamente 0,10035. Nesse limiar, precisão 41,7%, revocação 93,6% e 59,5% dos clientes sinalizados. Não apresentar revocação sem esse custo de contato/falsos positivos.
- Top 20% do ranking no teste: captura de 49,2% dos churns e precisão de 65,2%, em avaliação retrospectiva.
- H1–H4 tiveram associação no sentido previsto após Holm. Não interpretar como eficácia das ações sugeridas.
- Os valores completos e os intervalos estão em `outputs/`; esses arquivos são a referência após qualquer nova execução.

## Apresentação dos resultados

- `output/apresentacao/apresentacao_churn_final.pptx`: 11 slides editáveis, com gráficos e tabelas nativos e notas de fala.
- `output/pdf/apresentacao_churn_final.pdf`: versão para apresentar ou compartilhar, com texto selecionável.
- `output/apresentacao/roteiro_fala.md`: roteiro de 9 minutos, com tempo por slide e apoio para perguntas.
- O usuário pediu até 10 minutos e palavras simples. Esse limite prevalece sobre os 20 minutos descritos nos documentos da disciplina.
- Os slides distinguem taxas descritivas no treino de avaliação no teste. Apresentam 93,6% de revocação junto de 41,7% de precisão e 59,5% de clientes sinalizados, além do cenário com 20% de capacidade. As ações e a meta de redução são propostas para um piloto, não efeitos demonstrados.

## Artigo no Overleaf

- Projeto atualizado com autorização do usuário: `https://pt.overleaf.com/project/6afa1469a1368d20c9cba380`.
- Cópia original integral em `docs/overleaf_backup/projeto_original.zip`; fonte original em `docs/overleaf_backup/main.tex`.
- Fonte revisada, estilo SBC e duas figuras em `output/overleaf/`; pacote em `artigo_atualizado.zip`. Gerador: `scripts/preparar_artigo.py`, que usa as saídas validadas do notebook.
- PDF compilado pelo Overleaf e revisado: `output/pdf/artigo_churn_atualizado.pdf`, 9 páginas, dentro do limite de 12.
- Corrigidos placeholders, autoria, atributos, divisão 60/20/20, boosting utilizado, seleção por AP, calibração e limiar. O texto distingue a comparação em CV da avaliação final, e propostas de piloto dos resultados observados.

## Publicação e manutenção

- Repositório: https://github.com/CaioMascarenhas/projeto-cd, branch `main`. O usuário autorizou organizar e publicar as mudanças nesta sessão.
- Não versionar ambientes, backups privados, tokens, arquivos `.chart-data-*` ou o arquivo local `projeto_cd.zip`.
- `scripts/preparar_artigo.py` pode usar o estilo SBC já versionado em `output/overleaf/`, sem depender do backup privado.
- `.github/workflows/verificar.yml` executa o notebook, verifica o projeto, simula o fluxo Colab e gera as fontes do artigo em Linux/Python 3.11. Informar o resultado real da execução, sem presumir sucesso.
- Um convite antigo do Overleaf apareceu no histórico anterior. A limpeza do arquivo atual não revoga esse convite nem remove o histórico. Não reescrever o histórico remoto sem autorização explícita.
