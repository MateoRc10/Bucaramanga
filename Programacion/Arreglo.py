import pandas as pd
import numpy as np

# Generar 10,000 números aleatorios entre 0 y 1,000,000
numeros = np.random.randint(0, 1000000, size=10000)

# Crear un DataFrame de pandas
df = pd.DataFrame(numeros, columns=['numeros'])

# Guardar en un archivo CSV
df.to_csv('numeros_aleatorios.csv', index=False)

print("Archivo 'numeros_aleatorios.csv' generado con éxito con 10,000 números.")
