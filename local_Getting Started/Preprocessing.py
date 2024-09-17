import pandas as pd
import xarray as xr
import numpy as np
import os

# get CWD
cwd = os.getcwd()

# wind speed data for Hornsea 1 from dwd
dwd_Hornsea1 = xr.open_dataset(cwd + "/Datasets/dwd_icon_eu_hornsea_1_20200920_20231027.nc")
dwd_Hornsea1_features = dwd_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
dwd_Hornsea1_features.rename(columns={"WindSpeed:100": "WindSpeed_dwd"}, inplace=True)
dwd_Hornsea1_features["ref_datetime"] = dwd_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
dwd_Hornsea1_features["valid_datetime"] = dwd_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(dwd_Hornsea1_features["valid_datetime"],unit="hours")

# wind speed data for Hornsea 1 from ncep
ncep_Hornsea1 = xr.open_dataset(cwd + "/Datasets/ncep_gfs_hornsea_1_20200920_20231027.nc")
ncep_Hornsea1_features = ncep_Hornsea1["WindSpeed:100"].mean(dim=["latitude","longitude"]).to_dataframe().reset_index()
ncep_Hornsea1_features.rename(columns={"WindSpeed:100": "WindSpeed_ncep"}, inplace=True)
ncep_Hornsea1_features["ref_datetime"] = ncep_Hornsea1_features["ref_datetime"].dt.tz_localize("UTC")
ncep_Hornsea1_features["valid_datetime"] = ncep_Hornsea1_features["ref_datetime"] + pd.TimedeltaIndex(ncep_Hornsea1_features["valid_datetime"],unit="hours")

# solar radiation data for East England PV from dwd
dwd_solar = xr.open_dataset(cwd + "/Datasets/dwd_icon_eu_pes10_20200920_20231027.nc")
dwd_solar_features = dwd_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
dwd_solar_features.rename(columns={"SolarDownwardRadiation": "Radiation_dwd"}, inplace=True)
dwd_solar_features["ref_datetime"] = dwd_solar_features["ref_datetime"].dt.tz_localize("UTC")
dwd_solar_features["valid_datetime"] = dwd_solar_features["ref_datetime"] + pd.TimedeltaIndex(dwd_solar_features["valid_datetime"],unit="hours")

# solar radiation data for East England PV from ncep
ncep_solar = xr.open_dataset(cwd + "/Datasets/ncep_gfs_pes10_20200920_20231027.nc")
ncep_solar_features = ncep_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
ncep_solar_features.rename(columns={"SolarDownwardRadiation": "Radiation_ncep"}, inplace=True)
ncep_solar_features["ref_datetime"] = ncep_solar_features["ref_datetime"].dt.tz_localize("UTC")
ncep_solar_features["valid_datetime"] = ncep_solar_features["ref_datetime"] + pd.TimedeltaIndex(ncep_solar_features["valid_datetime"],unit="hours")

# Read energy data from a CSV file
energy_data = pd.read_csv(cwd + "/Datasets/Energy_Data_20200920_20231027.csv")
energy_data["dtm"] = pd.to_datetime(energy_data["dtm"])
energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]
energy_data = energy_data[["dtm","Wind_MW","Solar_MW","Wind_MWh_credit", "Solar_MWh_credit"]]

# Merge all data
modelling_table_Hornsea1 = dwd_Hornsea1_features.merge(ncep_Hornsea1_features, how="outer", on=["ref_datetime", "valid_datetime"])
modelling_table_solar = dwd_solar_features.merge(ncep_solar_features, how="outer", on=["ref_datetime", "valid_datetime"])
modelling_table = modelling_table_Hornsea1.merge(modelling_table_solar, how="outer", on=["ref_datetime", "valid_datetime"])

# Ensure 'valid_datetime' and 'ref_datetime' are datetime types
modelling_table['valid_datetime'] = pd.to_datetime(modelling_table['valid_datetime'], utc=True)
modelling_table['ref_datetime'] = pd.to_datetime(modelling_table['ref_datetime'], utc=True)

# Set 'valid_datetime' as index
modelling_table.set_index('valid_datetime', inplace=True)

# resample（1hour -> 30min）と interpolate（欠損値の補完）
def resample_and_interpolate(group):
    # Ensure index is datetime
    group.index = pd.to_datetime(group.index)

    # Resample to 30-minute intervals
    resampled = group.resample('30T').asfreq()

    # Interpolate numeric columns
    numeric_cols = resampled.select_dtypes(include=[np.number]).columns
    resampled[numeric_cols] = resampled[numeric_cols].interpolate(method='linear')

    # Forward fill non-numeric columns
    non_numeric_cols = resampled.select_dtypes(exclude=[np.number]).columns
    resampled[non_numeric_cols] = resampled[non_numeric_cols].ffill()

    return resampled

# Apply the function with as_index=False
modelling_table = modelling_table.groupby('ref_datetime', as_index=False).apply(resample_and_interpolate)

# 続行
modelling_table = modelling_table.reset_index()  # Reset index to bring 'valid_datetime' back as a column
modelling_table = modelling_table.merge(energy_data, how="inner", left_on="valid_datetime", right_on="dtm")
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

# Save the preprocessed data
modelling_table.to_csv(cwd + "/Datasets/preprocessed_data.csv", index=False)
