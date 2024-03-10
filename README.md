# "HYBRID ENERGY FORECASTING AND TRADING COMPETITION"のFORECASTINGパートのコード
[ホームページ](https://ieee-dataport.org/competitions/hybrid-energy-forecasting-and-trading-competition#files)  
[Github](https://github.com/jbrowell/HEFTcom24)  

## 概要
2つの予測モデルを用いて、季節ごとに分類した場合とそうでない場合の4パターンの予測を行った。  

・予測モデル
CQM(Cumulative Quantile Mode)：太陽光と風力発電量を個別に予測し、その予測値を合計するモデル    
DQM(Direct Quantile Model)：総発電 量を直接予測するモデル   
<img width="872" alt="スクリーンショット 2024-03-10 15 22 33" src="https://github.com/naruchoo/local_competition/assets/130206918/e84f0f0c-5705-44e4-a6ec-bce980d23a25">  

・季節ごとの分類
Seasonal：春(3~5 月)、夏(6~8 月)、秋(9~11 月)、冬 (12~2 月)に分類  
Non-seasonal：分類しない  


### データの前処理
Preprocessing.ipynb

### 確率論的予測


### ピンボールロスでの評価
