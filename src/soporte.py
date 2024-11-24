# importamos las librerías que necesitamos

# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np

# Imputación de nulos usando métodos avanzados estadísticos
# -----------------------------------------------------------------------
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Librerías de visualización
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt
# Configuración
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames

#-------------------------------------
from datetime import datetime
#%%
# función limpieza de datos:
def limpieza(df):
    """
    Limpia un DataFrame eliminando duplicados y normalizando el texto.
    - Elimina filas duplicadas en el DataFrame.
    - Convierte todos los valores de las columnas a minúsculas y elimina espacios en blanco al inicio y al final.
    """
    # Eliminar duplicados
    df.drop_duplicates(inplace=True)
    columnas_obj = df.select_dtypes(include='O').columns
    for columna in columnas_obj:
        df[columna] = df[columna].str.lower().str.strip()
    return df
#%%
#Función para cambiar el tipo de dato a float:
def cambiar_tipo_dato(col):
    """
    Convierte los valores de una columna de tipo objeto a tipo float.

    - Elimina el símbolo `$` y reemplaza las comas `,` por puntos `.` en los valores.
    - Convierte los valores resultantes a tipo `float`.
    - Si el valor es `NaN`, lo conserva como `np.nan`.

    Parámetros:
        col (str): El valor de la columna a procesar (de tipo cadena u objeto).

    Retorna:
        float: El valor convertido a tipo flotante, o `np.nan` si el valor original era nulo.

    Notas:
        Si ocurre un error durante la conversión, imprime un mensaje indicando el error.
    """
    try: 
        #print('Entro en try')
        if pd.isna(col):  # Verificar si el valor es NaN
            return np.nan
        else:  # Es necesario pq sino devuelve todo nulos (sólo en los valores tipo float, no sé pq)
            col = col.replace(",", ".").replace('$', '')  # Reemplazar la coma por punto y eliminar '$' 
            #print(f'Primer replace: {col}')
            return float(col)
    except:
        print('Ha ocurrido un error')

#Función para actualizar la columna 'age'
def actualizar_edad(datebirth):
    """ 
    Calcula la edad de una persona basada en su año de nacimiento. 
    Parámetros: datebirth (int o str): El año de nacimiento de la persona. 
    Retorna: int: La edad calculada como la diferencia entre el año actual y el año de nacimiento. 
    Notas: 
    - El parámetro `datebirth` debe contener únicamente el año de nacimiento. 
    - Se utiliza el año actual del sistema para realizar el cálculo. 
    """
    año_actual = datetime.now().year
    edad = año_actual - int(datebirth) # datebirth tiene solo el año de nacimiento
    return edad

#Función para actualizar los valores nulos de 'monthlyincome' y 'salary'
def actualizar_nulos(df):
    """ 
    Actualiza valores nulos en las columnas 'monthlyincome' y 'salary' en un DataFrame. 
    - Reemplaza los valores nulos en 'monthlyincome' con el resultado de dividir 'salary' entre 12. 
    - Reemplaza los valores nulos en 'salary' con el resultado de multiplicar 'monthlyincome' por 12. 
    Parámetros: df (pd.DataFrame): El DataFrame que contiene las columnas 'monthlyincome' y 'salary'. 
    Retorna: pd.DataFrame: El DataFrame con los valores nulos actualizados. 
    """
    # Reemplazar valores nulos en 'monthlyincome' con el valor de 'salary' / 12
    df['monthlyincome'] = df.apply(
        lambda row: np.round((row['salary'] / 12), 2) if pd.isna(row['monthlyincome']) else row['monthlyincome'], axis=1
    )
    
    # Reemplazar valores nulos en 'salary' con el valor de 'monthlyincome' * 12
    df['salary'] = df.apply(
        lambda row: np.round((row['monthlyincome'] * 12), 2) if pd.isna(row['salary']) else row['salary'], axis=1
    )
    
    return df