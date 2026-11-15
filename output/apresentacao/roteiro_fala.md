# Roteiro de fala

11 slides. Tempo planejado: 9 minutos. Reserve até 1 minuto para pausas ou perguntas.

## 1. Cancelamento de clientes em telecomunicações

Tempo: 20s (0:00 a 0:20).

Nosso projeto analisa o cancelamento de clientes de uma operadora. Esse cancelamento também recebe o nome de churn. Usamos os dados para entender em quais perfis ele aparece mais e avaliar uma forma de escolher quem a empresa poderia procurar primeiro.

## 2. O problema e o objetivo do grupo

Tempo: 45s (0:20 a 1:05).

A base tem 7.043 clientes. Desses, 1.869 cancelaram, o que representa 26,5%, ou aproximadamente 27 de cada 100. Na proposta inicial, nosso objetivo era entender os fatores ligados a essa saída e identificar clientes com maior risco, para direcionar ações de retenção. A ideia é ajudar a empresa a organizar o contato e avaliar ofertas com mais critério. Ao longo da apresentação, vamos separar os padrões observados do resultado do modelo.

## 3. Como preparamos e testamos a análise

Tempo: 60s (1:05 a 2:05).

Começamos pela limpeza. A base tem 21 colunas. Retirando o identificador e a resposta que queremos prever, ficam 19 informações para os modelos. Encontramos 11 cobranças acumuladas em branco, todas de clientes com zero mês de permanência. Assumimos zero nesses casos e mantivemos um indicador da ausência. Também criamos a quantidade de serviços e o gasto médio por mês. Dividimos os clientes em treino, validação e teste. No treino, comparamos os modelos em cinco partes. A validação ajudou a escolher o corte de risco. Só depois usamos o teste para medir o resultado. Os tratamentos aprendidos, como a mediana e a padronização, ficaram dentro de cada treinamento.

## 4. Contrato e tempo na empresa

Tempo: 60s (2:05 a 3:05).

Os primeiros dois resultados aparecem nestes gráficos. Entre os clientes com contrato mensal, 43,1% cancelaram. Entre os contratos de um ou dois anos, a taxa foi 6,3%. O segundo gráfico compara a permanência. Até 12 meses, a taxa foi 47,3%. Acima de um ano, foi 17,1%. Isso aponta dois perfis que merecem atenção: quem tem contrato mensal e quem está no início do relacionamento. Fizemos testes estatísticos para essas comparações. As associações continuaram presentes após corrigir os quatro testes. Porém, os dados não mostram que obrigar alguém a mudar de contrato evitaria o cancelamento.

## 5. Serviços e forma de pagamento

Tempo: 60s (3:05 a 4:05).

Na fibra, comparamos quem não tinha segurança ou suporte com quem tinha os dois serviços. As taxas foram 45,9% e 14%. Depois, olhamos apenas as faturas altas, definidas a partir de 89,75 unidades da base, que é o percentil 75 do treino. Nesse grupo, quem pagava por cheque eletrônico teve 47,1% de cancelamentos, contra 21,7% no pagamento automático por débito ou cartão. Essas comparações também tiveram associação após a correção estatística. São pistas para investigar problemas de atendimento e cobrança. Outros fatores podem explicar parte das diferenças, por isso uma oferta precisa passar por um teste real.

## 6. Qual modelo organizou melhor a lista de risco?

Tempo: 55s (4:05 a 5:00).

Comparamos quatro modelos e uma referência que usa somente a proporção de cancelamentos. A Random Forest combina várias árvores de decisão e teve a maior AP, com 0,672. Essa medida resume o equilíbrio entre encontrar cancelamentos e acertar os clientes sinalizados ao percorrer o ranking. Quanto maior, melhor. A Regressão Logística ficou próxima, com 0,667. Então a vantagem da Random Forest foi pequena, e não demonstramos superioridade estatística entre os dois métodos. Selecionamos o vencedor pelo treino, antes de olhar o teste final. Depois ajustamos suas probabilidades usando apenas o treino.

## 7. Mais cancelamentos encontrados, mais alertas

Tempo: 70s (5:00 a 6:10).

Agora usamos os clientes do teste, que ficaram separados. Escolhemos antes um corte de risco que dá prioridade a encontrar cancelamentos. O modelo encontrou 350 dos 374 cancelamentos, ou 93,6%, e deixou passar 24. Mas sinalizou 839 pessoas. Dessas, 489 não cancelaram. A precisão foi 41,7%. Portanto, encontrar quase todos os cancelamentos exigiria falar com muita gente. A AUC foi 0,843 e avalia a ordenação de risco, não a porcentagem de acertos. A acurácia nesse corte ficou em 63,6%, abaixo da referência de sempre prever que o cliente fica, com 73,5%. Isso mostra por que precisamos olhar o objetivo e o custo dos alertas, além da acurácia.

## 8. Priorização dos 20% de maior risco

Tempo: 55s (6:10 a 7:05).

Uma equipe pode não conseguir falar com todos os clientes sinalizados. Por isso, avaliamos uma capacidade de contato definida em 20% dos clientes do teste. O topo da lista tem 282 pessoas e inclui 184 dos 374 cancelamentos. Isso significa alcançar 49,2% dos cancelamentos, com precisão de 65,2% nesse grupo. Se a escolha fosse aleatória, o esperado seria alcançar cerca de 20%. A lista ajuda a concentrar o trabalho. Porém, estamos reconhecendo cancelamentos que já ocorreram na base. Ainda precisamos testar se um contato feito antes da saída consegue mudar esse resultado.

## 9. Ações que os resultados sugerem testar

Tempo: 60s (7:05 a 8:05).

As recomendações são testes práticos ligados aos padrões encontrados. Para contratos mensais, podemos testar uma migração voluntária com um benefício que caiba na margem. Para clientes novos, um acompanhamento nos primeiros meses. Para fibra sem segurança ou suporte, um diagnóstico técnico e uma oferta adequada. Para faturas altas com cheque eletrônico, revisar a cobrança e facilitar a adesão voluntária ao pagamento automático. Propomos um piloto de 90 dias. Dentro de cada perfil, um sorteio separaria quem recebe a ação e quem serve de comparação. A meta sugerida é reduzir o churn em pelo menos 10% em termos relativos, com margem incremental positiva. Essa é uma meta futura, não um resultado observado.

## 10. Conclusão e próximo passo

Tempo: 45s (8:05 a 8:50).

A análise atende à parte de entender os padrões e avaliar uma lista de prioridade para retenção. O resultado principal é que os 20% de maior risco concentraram quase metade dos cancelamentos do teste. Os dados também mostraram diferenças por contrato, permanência, suporte e pagamento. O próximo passo seria usar informações registradas antes do cancelamento e testar as ações com clientes ativos. A base não tem datas suficientes para comprovar essa antecipação. Também não demonstramos que uma oferta causa redução no churn ou gera lucro. Por isso, a recomendação final é validar o ranking e as ações em um piloto acompanhado.

## 11. Fontes dos dados e dos resultados

Tempo: 10s (8:50 a 9:00).

Estas são as fontes utilizadas. Os números apresentados vêm do notebook e das tabelas exportadas. Obrigado.

## Apoio para perguntas

- **Churn:** cancelamento do serviço.
- **Random Forest:** modelo que combina várias árvores de decisão para reconhecer padrões.
- **Revocação:** entre quem cancelou, quantos o modelo encontrou.
- **Precisão:** entre quem o modelo sinalizou, quantos realmente cancelaram.
- **AUC 0,843:** mede a ordenação de risco e não significa 84,3% de acertos.
- **AP:** resume a relação entre precisão e revocação ao percorrer o ranking.
- **F2:** dá mais peso a encontrar cancelamentos e foi a regra para escolher o corte na validação.
- **Corte 0,1003:** pontuação a partir da qual sinalizamos risco. Ele foi escolhido antes de avaliar o teste.
- **Os testes das hipóteses:** qui-quadrado bilateral com correção de Holm para as quatro comparações. Todos tiveram p ajustado menor que 0,05. Associação não prova causa.
- **Modelo próximo da Logística:** a diferença de AP foi pequena. Não fizemos um teste para afirmar superioridade entre esses modelos.
- **Lucro:** o notebook só simulou cenários. Com custo de 10 por contato, 3 meses e margem de 40%, eficácia hipotética de 20% daria saldo de 598,31 unidades monetárias. O equilíbrio seria perto de 16,5% de eficácia. Não são resultados de uma campanha.
- **Limite de antecipação:** precisamos de variáveis registradas antes do evento e avaliação temporal com clientes ativos.

## Fontes

Base local e proposta inicial da equipe. Resultados em `outputs/tabelas/` e `outputs/metadados.json`. Os PDFs da disciplina orientaram a sequência problema, método, resultado e decisão. O pedido de até 10 minutos prevaleceu sobre a duração maior citada nos materiais.
