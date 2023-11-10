"""import csv

# Define las columnas
columnas = ["me_gusta", "Marca", "Categoria", "Subcategoria"]

# Especifica el nombre del archivo CSV
nombre_archivo = "archivo.csv"

# Abre el archivo CSV en modo escritura
with open(nombre_archivo, mode="w", newline="") as archivo_csv:
    escritor = csv.writer(archivo_csv)

    # Escribe las columnas en la primera fila del archivo
    escritor.writerow(columnas)"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz
df_gustos = pd.read_csv('/home/nahuel/ChatBot/Usuarios/user_gustos.csv')

fila_aleatoria = df_gustos.iloc[2]
valores = fila_aleatoria[["Marca","Categoria","Subcategoria"]]
print(valores)

df = pd.get_dummies(data=df_gustos, drop_first=True)
explicativas = df.drop(columns='me_gusta')
objetivo = df.me_gusta
#Entrenar el modelo
model = DecisionTreeClassifier()
model.fit(X=explicativas, y=objetivo)
""""
#plot_tree(decision_tree=model, feature_names=explicativas.columns, filled=True)
dot_data = tree.export_graphviz(model,out_file=None,feature_names=explicativas.columns.tolist(),
                                class_names=df['me_gusta'].astype(str).unique().tolist(),
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("arbolPreview")"""

df_productos = pd.read_csv('/home/nahuel/ChatBot/datos_productos.csv')
df_tupla_aux = df_productos.loc[10, ['Marca', 'Categoria', 'Subcategoria']].to_frame().T #Acá poner como un nro dado.
print(df_tupla_aux)
df_tupla_aux = pd.get_dummies(data=df_tupla_aux)
# Crear tupla con el mismo formato que explicativas
df_tupla = pd.DataFrame(False, index=[0], columns=explicativas.columns)
for columna in explicativas.columns:
    if columna in df_tupla_aux.columns:
        df_tupla.at[0, columna] = True

y_pred = model.predict(df_tupla)
print(y_pred)
if(y_pred[0]==1):
    print("Acertado")
else:
    print("No acertado")





marca = df_productos['Marca'].iloc[100]
categoria = df_productos['Categoria'].iloc[100]
subcategoria = df_productos['Subcategoria'].iloc[100]
me_gusta = 0

# Crear un nuevo diccionario con los valores de la nueva fila
nueva_fila = {
    'me_gusta': me_gusta,
    'Marca': marca,
    'Categoria': categoria,
    'Subcategoria': subcategoria
}

# Convertir el diccionario en un DataFrame temporal
nueva_fila_df = pd.DataFrame(nueva_fila, index=[0])
df_gustos = pd.read_csv('/home/nahuel/ChatBot/Usuarios/archivo.csv')
# Concatenar el DataFrame temporal con tu DataFrame original
df_gustos = pd.concat([df_gustos, nueva_fila_df], ignore_index=True)
print(df_gustos)
#df_gustos.to_csv("agregado.csv", index=False)
df_gustos.to_csv("archivo.csv", index=False)
# Ahora, fila_deseada contiene el valor de la fila 3 en la columna 'Nombre'










import pandas as pd

# Cargar los DataFrames desde los archivos CSV
df = pd.read_csv('archivo_df.csv')
df_2 = pd.read_csv('archivo_df_2.csv')

# Inicializar un DataFrame temporal con las columnas deseadas
df_temp = pd.DataFrame(columns=["me_gusta", "Marca", "Categoria", "Subcategoria"])

# Lista de números que indican las filas de interés
numeros_filas_interes = [1, 25, 10, 2, 5]

# Recorrer la lista de números y agregar las filas al DataFrame temporal
for numero_fila in numeros_filas_interes:
    # Extraer la fila correspondiente del primer DataFrame
    fila_interes = df.loc[numero_fila - 1]  # Restar 1 ya que los índices empiezan en 0

    # Agregar una fila al DataFrame temporal con los valores deseados
    nueva_fila = pd.DataFrame([[1, fila_interes["Marca"], fila_interes["Categoria"], fila_interes["Subcategoria"]]],
                             columns=["me_gusta", "Marca", "Categoria", "Subcategoria"])
    
    df_temp = pd.concat([df_temp, nueva_fila], ignore_index=True)

# Concatenar el DataFrame temporal con el segundo DataFrame (df_2)
df_2 = pd.concat([df_2, df_temp], ignore_index=True)

# Guardar df_2 en un nuevo archivo CSV
df_2.to_csv('nuevo_archivo_df_2.csv', index=False)






