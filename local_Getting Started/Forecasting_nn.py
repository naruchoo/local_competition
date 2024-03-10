import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# Load the preprocessed data
modelling_table = pd.read_csv("preprocessed_data.csv")

# Prepare data for neural network
X = modelling_table[['Radiation_dwd', 'Radiation_ncep', 'WindSpeed_dwd', 'WindSpeed_ncep']] # 特徴量を選択
Y = modelling_table['total_generation_MWh']

# Build a neural network model for q50
nn_model = Sequential([
    Dense(64, activation='relu', input_shape=(X.shape[1],)),
    Dense(64, activation='relu'),
    Dense(1)
])
nn_model.compile(optimizer='adam', loss='mean_squared_error')
nn_model.fit(X, Y, epochs=10, batch_size=32)

# Use the neural network to predict q50
modelling_table['q50'] = nn_model.predict(X).flatten()
modelling_table.loc[modelling_table['q50'] < 0, 'q50'] = 0 # 発電量は0以上

# Save the neural network model
nn_model.save('models/model_nn_q50.h5')

# Save the analyzed data with q50 predictions
modelling_table[['ref_datetime','valid_datetime','Radiation_dwd', 'Radiation_ncep', 'WindSpeed_dwd', 'WindSpeed_ncep', 'q50','total_generation_MWh']].to_csv("analyzed_data_nn.csv", index=False)