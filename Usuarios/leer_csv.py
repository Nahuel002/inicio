RUTA_USUARIOS = '/home/nahuel/ChatBot/Usuarios/usuarios.csv'

import pandas as pd

id_user = 4123
nombre_user = 'Nahuel'
df_usuarios = pd.read_csv(RUTA_USUARIOS)
new_user = pd.DataFrame({'id': [id_user], 'nombre': [nombre_user], 'gastos': [0]})
df_usuarios = pd.concat([df_usuarios, new_user], ignore_index=True)

df_usuarios.to_csv(RUTA_USUARIOS, index=False)

