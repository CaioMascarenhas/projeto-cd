# Síntese dos resultados

Base: 7,043 clientes; prevalência global de churn 26.54%.
Treino 4,225, validação 1,409, teste 1,409.

Selecionado em CV por AP: **Random Forest**, com calibração sigmoid.
Limiar F2 fixado na validação: **0.1003**.
No teste: ROC-AUC **0.843**, AP **0.654**,
precisão **41.7%**, revocação **93.6%**,
F1 **0.577**, F2 **0.749**.
Foram identificados 350 churns, 24 não foram sinalizados e houve 489 falsos positivos.
O limiar sinalizou 59.5% dos clientes do teste.

Com capacidade pré-fixada de 20%: 282 contatos,
49.2% dos churns alcançados, precisão 65.2%
e lift 2.46 em relação ao contato aleatório.
Capturar churns retrospectivos não significa evitá-los.

Recomendação: avaliar um piloto prospectivo com grupo controle, capacidade e
premissas financeiras aprovadas pela área de negócio. As quatro ações estão em
`tabelas/insights_acionaveis.csv`; só as que têm evidência favorável devem ser
priorizadas a partir destes contrastes. A meta de 10% é proposta para o piloto,
não ganho observado. Dimensionar a amostra e ajustar múltiplas comparações antes
do experimento. Validar disponibilidade das variáveis antes do cancelamento.
