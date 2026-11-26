# Porsche Sales Intelligence

Dashboard HTML interativo para analisar 100 vendas de veículos Porsche. O painel responde a quatro perguntas de negócio sobre modelos, geografia, pagamento e operação de entregas.

## O que o dashboard mostra

- Desempenho comercial por modelo, com volume de vendas, receita e ticket médio.
- Concentração geográfica por estado e cidade, incluindo ranking das localidades com menor resultado no recorte filtrado.
- Preferência de pagamento e sua distribuição pelas faixas de preço do veículo.
- Desempenho dos vendedores, com receita, quantidade de vendas e distribuição de status.
- Indicadores de topo para vendas, receita, ticket médio, entregas concluídas e qualidade das datas.

## Como usar

1. Abra `index.html` em um navegador moderno.
2. Use os filtros de modelo, estado, cidade, ano, pagamento, vendedor e status.
3. Combine filtros para investigar um recorte específico.
4. Use o botão `Limpar filtros` para voltar à base completa.
5. Passe o mouse sobre as barras, segmentos de status e células da matriz de pagamento para ver detalhes.

O arquivo funciona como uma página estática. Não há servidor ou banco de dados necessário. A imagem principal já está embutida no `index.html`, portanto o dashboard continua funcionando mesmo quando o arquivo é aberto sozinho. A pasta `assets` mantém a versão original para futuras trocas visuais.

## Publicar no GitHub Pages

1. Crie um repositório no GitHub.
2. Envie `index.html`, `README.md`, a pasta `data` e a pasta `scripts`.
3. No repositório, abra **Settings**, depois **Pages**.
4. Em **Build and deployment**, selecione `Deploy from a branch`.
5. Escolha a branch principal e a pasta `/root`.
6. Salve e aguarde o endereço do GitHub Pages aparecer.

## Atualizar com uma nova planilha

A base inicial foi lida da aba `Sanitized`. O dashboard usa os campos tratados dessa aba para evitar diferenças de caixa, formato monetário e status.

Para gerar uma nova versão a partir de outra planilha:

```bash
pip install pandas openpyxl
python scripts/build_dashboard.py caminho/para/nova_base.xlsx
```

O script atualiza `data/porsche_sales.json` e substitui os dados incorporados no `index.html`. Depois, abra o HTML e confira filtros, totais e gráficos antes de enviar ao GitHub.

Também é possível enviar o `index.html` atual junto com a nova planilha para uma atualização assistida do dashboard.

## Regras de tratamento usadas

- `SalesPriceSanitized` é usado como valor numérico para receita e ticket.
- `PorscheModelSanitized`, `CitySanitized`, `StateSanitized` e `PayMethodSanitized` são usados nos filtros e agregações.
- Nomes de vendedores são normalizados apenas na apresentação para juntar diferenças de maiúsculas e minúsculas, como `PETER Lane` e `Peter Lane`.
- Datas cujo campo `SaleDateSanitized` é `INVALID` continuam nas análises de vendas e aparecem no indicador de qualidade. Na base original são 24 registros.
- Status com `Pending` ou `Awaiting` são tratados como pendências nos destaques operacionais. `Delivered`, `Cancelled`, `In Transit` e `Shipped` permanecem separados no gráfico detalhado.

## Identidade visual

A interface foi inspirada na experiência visual do site oficial da Porsche Brasil, usando navegação mínima, cabeçalho escuro em tela ampla, wordmark tipográfico, fundo claro, alto contraste, vermelho de destaque e cartões com bordas discretas. O dashboard é uma composição própria para dados e não reutiliza imagens ou componentes proprietários do site. A tipografia usa a pilha de fontes do sistema para manter o carregamento rápido em GitHub Pages e em navegadores sem internet.

## Estrutura

```text
.
├── index.html
├── README.md
├── assets/
│   └── hero-car.png
├── data/
│   └── porsche_sales.json
└── scripts/
    └── build_dashboard.py
```
