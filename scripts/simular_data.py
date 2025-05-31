import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
start_date = pd.to_datetime('2024-06-01')
end_date = pd.to_datetime('2025-05-31')
dates = pd.date_range(start_date, end_date, freq='D')

activities = ['Trabajo', 'Estudio', 'Ejercicio', 'Ocio', 'Social', 'Hogar']

data = []
for date in dates:
    day_data = []
    total_hours = 0
    np.random.shuffle(activities)
    for activity in activities:
        max_hours = min(4, 16 - total_hours)
        if max_hours <= 0:
            hours = 0
        else:
            hours = np.random.randint(0, max_hours + 1)
        if hours > 0:
            day_data.append((date, activity, hours))
            total_hours += hours
    data.extend(day_data)

df_sim = pd.DataFrame(data, columns=['fecha', 'actividad', 'horas'])
Path('data').mkdir(exist_ok=True)
df_sim.to_csv('data/tracking_simulado.csv', index=False)
print("Base de datos simulada generada en data/tracking_simulado.csv")
