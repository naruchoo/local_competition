import pandas as pd
import xarray as xr
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.iolib.smpickle import load_pickle

#import comp_utils

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pickle as pkl

plt.rcParams['font.family'] = 'Hiragino sans'



# Step1 : Data preprocessing

# wind speed data for Hornsea 1 from dwd
dwd_Hornsea1 = xr.open_dataset("dwd_icon_eu_hornsea_1_20200920_20231027.nc")
dwd_Hornsea1_features = dwd_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
dwd_Hornsea1_features.rename(columns={"WindSpeed:100": "WindSpeed_dwd"}, inplace=True)
dwd_Hornsea1_features["ref_datetime"] = dwd_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
dwd_Hornsea1_features["valid_datetime"] = dwd_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(dwd_Hornsea1_features["valid_datetime"],unit="hours")

# wind speed data for Hornsea 1 from ncep
ncep_Hornsea1 = xr.open_dataset("ncep_gfs_hornsea_1_20200920_20231027.nc")
ncep_Hornsea1_features = ncep_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
ncep_Hornsea1_features.rename(columns={"WindSpeed:100": "WindSpeed_ncep"}, inplace=True)
ncep_Hornsea1_features["ref_datetime"] = ncep_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
ncep_Hornsea1_features["valid_datetime"] = ncep_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(ncep_Hornsea1_features["valid_datetime"],unit="hours")

# solar radiation data for East England PV from dwd
dwd_solar = xr.open_dataset("dwd_icon_eu_pes10_20200920_20231027.nc")
dwd_solar_features = dwd_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
dwd_solar_features.rename(columns={"SolarDownwardRadiation": "Radiation_dwd"}, inplace=True)
dwd_solar_features["ref_datetime"] = dwd_solar_features["ref_datetime"].dt.tz_localize("UTC")
dwd_solar_features["valid_datetime"] = dwd_solar_features["ref_datetime"] + pd.TimedeltaIndex(dwd_solar_features["valid_datetime"],unit="hours")

# solar radiation data for East England PV from ncep
ncep_solar = xr.open_dataset("ncep_gfs_pes10_20200920_20231027.nc")
ncep_solar_features = ncep_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
ncep_solar_features.rename(columns={"SolarDownwardRadiation": "Radiation_ncep"}, inplace=True)
ncep_solar_features["ref_datetime"] = ncep_solar_features["ref_datetime"].dt.tz_localize("UTC")
ncep_solar_features["valid_datetime"] = ncep_solar_features["ref_datetime"] + pd.TimedeltaIndex(ncep_solar_features["valid_datetime"],unit="hours")

# Read energy data from a CSV file
energy_data = pd.read_csv("Energy_Data_20200920_20231027.csv")
energy_data["dtm"] = pd.to_datetime(energy_data["dtm"])
energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]
energy_data = energy_data[["dtm","Wind_MW","Solar_MW","Wind_MWh_credit", "Solar_MWh_credit"]]

# Merge all date
modelling_table_Hornsea1 = dwd_Hornsea1_features.merge(ncep_Hornsea1_features,how="outer",on=["ref_datetime","valid_datetime"])
modelling_table_solar = dwd_solar_features.merge(ncep_solar_features,how="outer",on=["ref_datetime","valid_datetime"])
modelling_table = modelling_table_Hornsea1.merge(modelling_table_solar,how="outer",on=["ref_datetime","valid_datetime"])
modelling_table = modelling_table.set_index("valid_datetime").groupby("ref_datetime").resample("30T").interpolate("linear")
modelling_table = modelling_table.drop(columns="ref_datetime",axis=1).reset_index()
modelling_table = modelling_table.merge(energy_data,how="inner",left_on="valid_datetime",right_on="dtm")
modelling_table = modelling_table.drop("dtm", axis=1)
modelling_table["total_generation_MWh"] = modelling_table["Wind_MWh_credit"] + modelling_table["Solar_MWh_credit"]

# 48時間以内のデータのみを抽出
modelling_table = modelling_table[modelling_table["valid_datetime"] - modelling_table["ref_datetime"] <= np.timedelta64(48,"h")] #444264行

# 欠損値のある行を削除
modelling_table = modelling_table[modelling_table["WindSpeed_dwd"].notnull()]
modelling_table = modelling_table[modelling_table["WindSpeed_ncep"].notnull()]
modelling_table = modelling_table[modelling_table["Radiation_dwd"].notnull()]
modelling_table = modelling_table[modelling_table["Radiation_ncep"].notnull()] # 444264行
modelling_table = modelling_table[modelling_table["Wind_MW"].notnull()] # 441426行
modelling_table = modelling_table[modelling_table["Solar_MW"].notnull()] # 440823行
modelling_table = modelling_table.drop(["Wind_MW", "Solar_MW"], axis=1)

# 重複行を削除
modelling_table = modelling_table.drop_duplicates() # 435479行
modelling_table.reset_index(drop=True, inplace=True)



# Step2 : Analysis and Forecast

# quantile regression
mod = smf.quantreg('total_generation_MWh ~ bs(Radiation_dwd,df=5) + bs(Radiation_ncep,df=5) + bs(WindSpeed_dwd,df=8) + bs(WindSpeed_ncep,df=8)', data=modelling_table)

forecast_models = dict()
for quantile in range(10,100,10):
    forecast_models[f"q{quantile}"] = mod.fit(q=quantile/100,max_iter=2500)
    modelling_table[f"q{quantile}"] = forecast_models[f"q{quantile}"].predict(modelling_table) 
    modelling_table.loc[modelling_table[f"q{quantile}"] < 0, f"q{quantile}"] = 0 #発電量は0以上
    
modelling_table.to_csv("analyzed_data.csv", index=False)

# Save the quantile regression models to files   
for quantile in range(10,100,10):
    forecast_models[f"q{quantile}"].save(f"models/model_q{quantile}.pickle")




# Step3 : Evaluation
  
# Define the Pinball function
def pinball(y,q,alpha):
    return (y-q)*alpha*(y>=q) + (q-y)*(1-alpha)*(y<q)

# Calculate the Pinball Score
def pinball_score(df):
    score = list()
    for qu in range(10,100,10):
        score.append(pinball(y=df["total_generation_MWh"], q=df[f"q{qu}"], alpha=qu/100).mean())
    return sum(score)/len(score)

# Calculate and print the Pinball Score
score = pinball_score(modelling_table)
print("pinball loss =", score)