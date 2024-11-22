from src import soporte as sp
from src import variables as va

df = sp.pd.read_csv('archivos/hr_raw_data_final.csv', index_col=[0])

# limpiamos dataframe (duplicados, lower y strip)

sp.limpieza(df)

# eliminamos columnas

df.drop(labels= va.columnas_drop, axis=1, inplace=True)
print('columnas eliminadas')


# sustituimos 1 -> F y 0 -> M

df['gender'] = df['gender'].replace(1, 'F').replace(0, 'M').str.upper()


# cambiamos tipo de datos a float

sp.cambiar_tipo_dato(va.columnas_float)

#Cambio de datos negativos a positivos

df['distancefromhome'] = df['distancefromhome'].apply(lambda x: -x if x < 0 else x)

#Corregir errata 'Marreid'

df['maritalstatus'] = df['maritalstatus'].replace('marreid','married')

#unificar 'remotework'
dicc_remote = {'0':'no','1':'si','True':'si','False':'no'}
df['remotework'] = df['remotework'].map(dicc_remote)

#businesstravel -> poner los nan como non travel
df['businesstravel'] = df['businesstravel'].fillna('non-travel')

#correción 'environmentsatisfaction'
df['environmentsatisfaction'] = df['environmentsatisfaction'].astype(str).str.extract(r'^([1-4])', expand=False).fillna(df['environmentsatisfaction']).astype(int)

# Corregimos la columna 'age':

df['age'] = df['datebirth'].apply(sp.actualizar_edad)