# Case-H2

### Definição de como escolher os ativos:

Para realizar a definição de como iremos escolher esses ativos, vamos utilizar esse 5 indicativos.

##### 1. Liquidez (Volume Médio)
A liquidez de um ativo é a média do volume de transações (quantidade de ações negociadas) durante um período. Nesse caso, é calculada a média do volume diário das últimas 6 meses.

**Fórmula:**

$$\text{Liquidez (Volume Médio)} = \frac{\sum_{i=1}^{n} V_i}{n}$$

Onde:
- $V_i$ é o volume de transações no dia $i$.
- $n$ é o número total de dias no período considerado (6 meses no seu caso).

##### 2. Beta
O beta de um ativo é uma medida de sua volatilidade em relação ao mercado. Ele indica o quanto o preço de uma ação tende a se mover em relação a um índice de mercado, como o Ibovespa. O beta é calculado com base na covariância entre o retorno do ativo e o retorno do mercado, dividido pela variância do mercado.

**Fórmula:**

$$\beta = \frac{\text{Covariância}(r_{\text{ativo}}, r_{\text{mercado}})}{\text{Variância}(r_{\text{mercado}})}$$

Onde:
- $r_{\text{ativo}}$ é o retorno do ativo.
- $r_{\text{mercado}}$ é o retorno do mercado.
- A covariância mede o quanto o retorno do ativo e o retorno do mercado variam juntos.
- A variância do mercado é a medida de dispersão dos retornos do mercado.

##### 3. Sharpe Ratio
O Sharpe Ratio mede a relação entre o retorno excessivo de um ativo (retorno acima da taxa livre de risco) e a sua volatilidade. É uma métrica importante para avaliar o desempenho ajustado ao risco de um ativo.

**Fórmula:**

$$S = \frac{R_{\text{ativo}} - R_{\text{livre}}}{\sigma_{\text{ativo}}}$$

Onde:
- $R_{\text{ativo}}$ é o retorno médio diário do ativo.
- $R_{\text{livre}}$ é a taxa de retorno livre de risco anualizada (geralmente usada 6% ao ano, ajustada para um período diário).
- $\sigma_{\text{ativo}}$ é o desvio padrão do retorno diário do ativo (volatilidade).

##### 4. P/E Ratio (Price to Earnings Ratio)
O P/E Ratio (Preço sobre Lucro) é uma medida de avaliação que compara o preço atual da ação com o lucro por ação (LPA) da empresa. Ele é utilizado para avaliar se uma ação está cara ou barata em relação aos lucros da empresa.

**Fórmula:**

$$\text{P/E Ratio} = \frac{\text{Preço da Ação}}{\text{Lucro por Ação (LPA)}}$$

Onde:
- O preço da ação é o preço atual do ativo no mercado.
- O Lucro por Ação (LPA) é o lucro líquido da empresa dividido pelo número de ações em circulação.

##### 5. Momentum
O momentum é uma métrica que mede a direção do movimento de um ativo em um determinado período. Ele é calculado como a soma das variações percentuais diárias (retornos) durante um período específico, como 6 meses. Um valor positivo de momentum indica que o ativo está em alta, enquanto um valor negativo indica queda.

**Fórmula:**

$$\text{Momentum} = \sum_{i=1}^{n} \left( \frac{P_i - P_{i-1}}{P_{i-1}} \right)$$

Onde:
- $P_i$ é o preço de fechamento do ativo no dia $i$.
- $P_{i-1}$ é o preço de fechamento do ativo no dia anterior.
- A soma das variações percentuais diárias dá o momentum total do ativo durante o período.

---

AWS
terraform
git actions
streamlit
git summary
pre-commit.