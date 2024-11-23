#%%
from src import soporte as sp
from src import variables as va

df = sp.pd.read_csv('archivos/hr_raw_data_final.csv', index_col=[0])

# limpiamos dataframe (duplicados, lower y strip)
sp.limpieza(df)
print("1. DataFrame limpiado: duplicados eliminados, minúsculas aplicadas y espacios eliminados.")
print(f"Primeras filas después de limpieza:\n{df.head()}")
#%%
# eliminamos columnas
df.drop(labels=va.columnas_drop, axis=1, inplace=True)
print(f"2. Columnas eliminadas: {va.columnas_drop}")
print(f"DataFrame después de eliminar columnas: {df.head()}")

# sustituimos 1 -> F y 0 -> M en 'gender'
df['gender'] = df['gender'].replace(1, 'F').replace(0, 'M')#.str.upper()
print("3. Columna 'gender' modificada: 1 -> F, 0 -> M y convertido a mayúsculas.")
print(f"Valores únicos en 'gender' después del cambio: {df['gender'].unique()}")

# cambiamos tipo de datos a float
sp.cambiar_tipo_dato(va.columnas_float)
print(f"4. Tipos de datos cambiados a float para las columnas: {va.columnas_float}")
print(f"Tipos de datos después del cambio: {df[va.columnas_float].dtypes}")

# Cambio de datos negativos a positivos en 'distancefromhome'
df['distancefromhome'] = df['distancefromhome'].apply(lambda x: -x if x < 0 else x)
print("5. Columna 'distancefromhome' corregida: los valores negativos se han convertido en positivos.")
print(f"Primeros valores de 'distancefromhome' después del cambio: {df['distancefromhome'].head()}")

# Corregir errata 'marreid' en 'maritalstatus'
df['maritalstatus'] = df['maritalstatus'].replace('marreid', 'married')
print("6. Columna 'maritalstatus' corregida: 'marreid' cambiado a 'married'.")
print(f"Valores únicos en 'maritalstatus' después del cambio: {df['maritalstatus'].unique()}")

# Unificar 'remotework'
dicc_remote = {'0': 'no', '1': 'si', 'True': 'si', 'False': 'no'}
df['remotework'] = df['remotework'].map(dicc_remote)
print("7. Columna 'remotework' unificada: valores mapeados a 'no' o 'si'.")
print(f"Valores únicos en 'remotework' después del cambio: {df['remotework'].unique()}")

# Businesstravel -> poner los NaN como 'non-travel'
df['businesstravel'] = df['businesstravel'].fillna('non-travel')
print("8. Columna 'businesstravel' corregida: valores nulos reemplazados por 'non-travel'.")
print(f"Valores nulos en 'businesstravel' después del cambio: {df['businesstravel'].isna().sum()}")

# Correción 'environmentsatisfaction'
df['environmentsatisfaction'] = df['environmentsatisfaction'].astype(str).str.extract(r'^([1-4])', expand=False).fillna(df['environmentsatisfaction']).astype(int)
print("9. Columna 'environmentsatisfaction' corregida: se extrajeron los valores de 1 a 4 y los NaN no cambiaron.")
print(f"Primeros valores de 'environmentsatisfaction' después del cambio: {df['environmentsatisfaction'].head()}")

# Corregimos la columna 'age'
df['age'] = df['datebirth'].apply(sp.actualizar_edad)
print("10. Columna 'age' actualizada: edad calculada a partir de la fecha de nacimiento.")
print(f"Primeros valores de 'age' después del cambio: {df[['datebirth', 'age']].head()}")

# Actualizamos los nulos de las columnas 'monthlyincome' y 'salary'
sp.actualizar_nulos(df)
print("11. Columnas 'monthlyincome' y 'salary' actualizadas: valores nulos corregidos.")
print(f"Valores nulos en 'monthlyincome' después del cambio: {df['monthlyincome'].isna().sum()}")
print(f"Valores nulos en 'salary' después del cambio: {df['salary'].isna().sum()}")