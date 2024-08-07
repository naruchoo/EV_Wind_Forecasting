# 概要
![286453455-c528e8bf-4fcd-45bf-8752-33393bcaaa39](https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/41a3c5b0-22ae-4097-84fb-9c6f583c605d)


上記コンペの"HYBRID ENERGY FORECASTING"のコード  
[ホームページ](https://ieee-dataport.org/competitions/hybrid-energy-forecasting-and-trading-competition#files)  
[Github](https://github.com/jbrowell/HEFTcom24)  

------------  
# 確率的な予測
## 太陽光発電と風力発電の地図
<img width="315" alt="スクリーンショット 2024-07-10 18 30 15" src="https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/31bc1236-c60c-4c31-9724-1d066f737c31">


## 30分刻みの発電量
![2020~23_風力と太陽光の推移](https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/4b4e0f98-afce-4b76-b363-b9e9b2a13fb2)

## 予測モデル  
■ 予測モデル  
CQM(Cumulative Quantile Mode)：太陽光と風力発電量を個別に予測し、その予測値を合計するモデル    
DQM(Direct Quantile Model)：総発電量を直接予測するモデル   

<img width="797" alt="スクリーンショット 2024-07-10 18 20 55" src="https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/0e3a9e42-7d9f-4bd5-974b-cb02a752b6e0">

■ 季節ごとの分類  
Seasonal：春(3-5月)、夏(6-8月)、秋(9-11月)、冬 (12-2月)に分類  
Non-seasonal：  

## ピンボールロスによる予測精度の評価
![DQMとCQMの比較_all](https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/81696682-752b-4cc6-9a0b-1dfbfe49b856)  

## 0時の気象予報データを用いた際の予測精度の比較  
![ピンボールロスの比較(発表時刻：0時)](https://github.com/naruchoo/EV_Wind_Forecasting/assets/130206918/e1dc8d37-b26e-41b2-9890-17fd977d289c)

------------  
# コードについて 
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
