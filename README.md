# "HYBRID ENERGY FORECASTING AND TRADING COMPETITION"のFORECASTINGパートのコード  
![DataPort 43_0](https://github.com/naruchoo/local_competition/assets/130206918/818db57c-a684-4aa0-b9a3-3e364a936019)  



[ホームページ](https://ieee-dataport.org/competitions/hybrid-energy-forecasting-and-trading-competition#files)  
[Github](https://github.com/jbrowell/HEFTcom24)  

# 予測モデル  
■ 予測モデル  
CQM(Cumulative Quantile Mode)：太陽光と風力発電量を個別に予測し、その予測値を合計するモデル    
DQM(Direct Quantile Model)：総発電 量を直接予測するモデル   

<img width="859" alt="スクリーンショット 2024-03-10 15 29 53" src="https://github.com/naruchoo/local_competition/assets/130206918/597519de-b4c5-43e7-8066-7544ebe3446e">  


■ 季節ごとの分類  
Seasonal：春(3-5月)、夏(6-8月)、秋(9-11月)、冬 (12-2月)に分類  
Non-seasonal：  

# コード  
■ データの前処理  
Preprocessing.ipynb  

■ 確率論的予測  
① Forecasting_CQM,N.ipynb：CQM、Non-seaasonal  
② Forecasting_DQM,N.ipynb：DQM、Non-seaasonal  
③ Forecasting_CQM,S.ipynb：CQM、Seaasonal  
④ Forecasting_DQM,S.ipynb：DQM、Seaasonal  

■ 予測精度の評価  
① Evaluation_CQM,N.ipynb：CQM、Non-seaasonal  
② Evaluation_DQM,N.ipynb：DQM、Non-seaasonal  
③ Evaluation_CQM,S.ipynb：CQM、Seaasonal  
④ Evaluation_DQM,S.ipynb：DQM、Seaasonal  


# その他のコード  
