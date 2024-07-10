# "HYBRID ENERGY FORECASTING AND TRADING COMPETITION"のFORECASTINGパートのコード  
![286453455-c528e8bf-4fcd-45bf-8752-33393bcaaa39](https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/41a3c5b0-22ae-4097-84fb-9c6f583c605d)



[ホームページ](https://ieee-dataport.org/competitions/hybrid-energy-forecasting-and-trading-competition#files)  
[Github](https://github.com/jbrowell/HEFTcom24)  

# 予測モデル  
■ 予測モデル  
CQM(Cumulative Quantile Mode)：太陽光と風力発電量を個別に予測し、その予測値を合計するモデル    
DQM(Direct Quantile Model)：総発電 量を直接予測するモデル   

<img width="805" alt="スクリーンショット 2024-07-10 18 15 17" src="https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/a51ae0ca-38b1-4eb5-a0b0-ca0d02f044bd">



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
