<img width="677" alt="スクリーンショット 2024-03-06 19 54 36" src="https://github.com/naruchoo/local_competition/assets/130206918/fd24abf9-b3d9-412d-8408-e42fdcfd5ae4"># "HYBRID ENERGY FORECASTING AND TRADING COMPETITION"のforecastingパートのコード
[ホームページ](https://ieee-dataport.org/competitions/hybrid-energy-forecasting-and-trading-competition#files)

[Github](https://github.com/jbrowell/HEFTcom24)

## 概要
2つの予測モデルを用いて、季節ごとに分類した予測とそうでない予測の4種類の予測を行った。

・予測モデル
CQM(Cumulative Quantile Mode)：太陽光と風力発電量を個別に予測し、その予測値を合計するモデル
DQM(Direct Quantile Model)：総発電 量を直接予測するモデル
<img width="889" alt="スクリーンショット 2024-03-10 15 18 22" src="https://github.com/naruchoo/local_competition/assets/130206918/85ea195d-1cf6-4af8-9081-bfb60a6f59a7">


### データの前処理
Preprocessing.ipynb

### 確率論的予測


### ピンボールロスでの評価
