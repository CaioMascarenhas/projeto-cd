# Fontes consultadas e escopo

Consulta em 15/11/2026, para implementar o notebook a partir dos materiais existentes.

| Fonte | Leitura | Informações usadas |
|---|---|---|
| `Projeto (2026-1).pdf` | Integral, 11 páginas; texto extraído e páginas inspecionadas visualmente | Objetivo, requisitos da base, três insights, estrutura técnica, formato SBC, limite de páginas, apresentação e submissão |
| `Aula_cd_projeto.pdf` | Integral, 19 páginas; texto extraído e páginas inspecionadas visualmente | Narrativa de EDA, tratamento, comparação de modelos, validação, explicabilidade e decisão gerencial |
| `nossodocinicial.txt` | Integral; contém link, não o conteúdo da proposta | Localização do Google Docs |
| Google Docs “Parte 1” | Integral por exportação pública em texto; cópia em `proposta_inicial.txt` | Equipe, base, problema, H1–H4, tratamentos e métodos possíveis |
| Projeto Overleaf | Leitura integral pela sessão autorizada do Chrome | Artigo atualizado, compilado e revisado com 9 páginas; link versionado sem token de convite |
| CSV local | Todas as linhas/colunas auditadas por código | Dados efetivamente analisados; hash registrado nos metadados |

Documento inicial: https://docs.google.com/document/d/1zYuZ4hVkP1XcLnEA3_y3MBFziVSHbs_Tl5khLn4gcOU/edit

Origem da base declarada na proposta: https://www.kaggle.com/datasets/blastchar/telco-customer-churn . O notebook usa o arquivo local; não depende de acesso ao Kaggle. A página do Kaggle não foi usada como fonte de resultados ou de características adicionais não presentes nos arquivos.

## Rastreabilidade dos requisitos

| Requisito | Implementação |
|---|---|
| Mais de 5.000 linhas e ≥10 colunas úteis | Auditoria confirma 7.043, 19 preditores + alvo, sem ID |
| Dados numéricos e categóricos, alvo e preparação | Dicionário, limpeza de cobrança, codificação, escalonamento e engenharia |
| Estatística descritiva e inferência | Distribuições, medidas por grupo, Spearman, H1–H4 com Holm e efeitos; Mann-Whitney exploratório |
| Métodos e justificativas | Dummy, Logística, Árvore, Random Forest e HistGradientBoosting |
| Métricas e método de avaliação | CV estratificada, validação separada, teste, AP/ROC-AUC/precisão/recall/F1/F2/Brier e bootstrap |
| Explicabilidade | Permutação na validação por blocos coerentes de serviços |
| Pelo menos três insights acionáveis | Quatro contrastes com evidência e interpretação; ações condicionadas à evidência favorável, KPI e piloto proposto |
| Relação com decisão e impacto | Captura por capacidade de contato e simulação com custos, margem e eficácia explícitos |
| Comunicação | Síntese automática e roteiro para artigo/pitch no notebook |

## Decisões do experimento que não são exigências dos documentos

- Divisão 60/20/20, semente 42, 5 folds de seleção e 3 de calibração.
- AP para selecionar modelo e F2 para escolher limiar; capacidade financeira fixada em 20%.
- Mediana para outros valores ausentes; acumulado zero para ausentes com permanência zero, mantendo indicador da ausência.
- H2 usa limite de 12 meses; H3 compara fibra com ambos os serviços contra falta de ao menos um; H4 usa P75 de cobrança aprendido no treino e compara métodos dentro das faturas altas.
- Correção de Holm na família H1–H4 e testes bilaterais. ICs individuais não corrigidos são identificados como tais.
- Custos, margem, eficácia, horizonte e meta do piloto são premissas didáticas, não informações medidas ou fornecidas pela operadora.
- Boosting do scikit-learn foi escolhido para reduzir dependências. Os métodos da proposta são possibilidades, não compromisso, conforme o PDF da disciplina.

## Limites desta entrega

O artigo no Overleaf foi lido e atualizado após autorização. O relatório SBC de 9 páginas e os 11 slides com roteiro de 9 minutos estão em `output/`. Streamlit permanece como recurso futuro. Não há datas suficientes para inferir cronograma da turma ou horizonte temporal da previsão. O nome do PDF e o semestre da proposta divergem; a divergência foi preservada nas notas.
