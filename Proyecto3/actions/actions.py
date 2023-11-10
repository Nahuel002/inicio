# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import csv
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import graphviz

RUTA_USUARIOS='/home/nahuel/ChatBot/Usuarios/usuarios.csv'
df = pd.read_csv('/home/nahuel/ChatBot/datos_productos.csv')
#df_usuarios = pd.read_csv(RUTA_USUARIOS)

def buscar_Producto(columna, descripcion):
    # Tokenizar la descripción de búsqueda
    tokens_busqueda = word_tokenize(descripcion.lower())
    # Función para verificar si todos los tokens de búsqueda están presentes en la descripción del producto
    def contiene_todos_tokens(descripcion_producto):
        tokens_producto = word_tokenize(descripcion_producto.lower())
        return all(token in tokens_producto for token in tokens_busqueda)
    # Filtrar el DataFrame para obtener productos que contengan todos los tokens de búsqueda
    resultados = df[df[columna].apply(contiene_todos_tokens)][[columna]].index.tolist()
    return resultados

LIMITE = 20 #usado para mostrar un tope de información de la lista de consulta.
def mostrar_Informacion(lista_index):
    informacion = ""
    indice = 0
    descuento = None
    contador=0
    for elemento in lista_index:
        contador = contador + 1
        if isinstance(elemento, str) and ';' in elemento:
            partes = elemento.strip('[]').split(';')
            indice = int(partes[0].rstrip(']'))
            descuento = float(partes[1])
        else:
            indice = elemento
            descuento = None
        if int(indice) < len(df):
            columna1_valor = df.loc[indice, 'Consulta_Nombre']
            columna2_valor = df.loc[indice, 'Precio']
            if descuento:
                columna2_valor = columna2_valor*(1-descuento);
                columna2_valor = "{:.2f}".format(columna2_valor)
            informacion += f"*{contador}-* {columna1_valor} $ {columna2_valor}\n"
    
    return informacion

def devolver_Lista_De_Prolog(lista_prolog):
    indice=1
    lista_index = []
    for producto_info in lista_prolog:
        nombre = producto_info['Producto']
        marca = producto_info['Marca']
        peso = producto_info['Peso']
        descuento = producto_info['DescuentoPorcentaje']
        formato = f"{nombre} {marca} de {peso}"
        producto_in_dataframe = buscar_Producto("Consulta_Nombre",formato)
        lista_index.append(f"{producto_in_dataframe};{descuento}")
    return lista_index



from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from swiplserver import PrologMQI
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted

import random

# Modifica la función para devolver la lista formateada y establecer el valor del slot
def format_prolog_response(response,marca,categoria,subcategoria) -> list:
    slot_lista_consulta = []
    
    for solution in response:
        nombre = solution['Nombre']
        if not marca:
            m = solution['Marca']
        else:
            m = marca
        if not categoria:
            c = solution['Categoria']
        else:
            c = categoria
        if not subcategoria:
            s = solution['Subcategoria']
        else:
            s = subcategoria
        peso = solution['Peso']
        precio = solution['Precio']
        resultado = f"Nombre: {nombre}, Categoria: {c}, Subcategoria: {s}, Marca: {m}, Peso: {peso}, Precio: {precio}"
        slot_lista_consulta.append(resultado)

    return slot_lista_consulta

""" Quedó del Proyecto viejo
# Nueva función para formatear la lista y devolverla como una cadena
def devolver_lista_cadena(slot_lista):
    formatted_list = []
    for elemento in slot_lista:
        # Divide la cadena en sus partes utilizando la coma como separador
        partes = elemento.split(', ')
        
        # Extrae los valores individuales de cada parte
        nombre = partes[0].split(': ')[1]
        categoria = partes[1].split(': ')[1]
        subcategoria = partes[2].split(': ')[1]
        marca = partes[3].split(': ')[1]
        peso = partes[4].split(': ')[1]
        precio = partes[5].split(': ')[1]
        
        # Formatea la cadena en el orden deseado
        nuevo_formato = f"- {subcategoria} {nombre} {marca} {peso} ${precio}"
        formatted_list.append(nuevo_formato)

    return "\n".join(formatted_list)"""

class ActionWithBuscarProducto(Action):
    def name(self) -> Text:
        return "action_consultar_producto"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mensaje = tracker.latest_message['text']
        # Lista de frases clave para buscar
        mensaje = mensaje.lower()
        cortar_cadenas = [
            "productos de la", "producto de la", "productos para el", "producto para el", "productos de",
            "producto de", "producto para", "productos para", "algo de", "opciones de",
            "comprar unos", "comprar uno", "comprar una", "comprar unas",
            "conseguir unos", "conseguir uno", "conseguir una", "conseguir unas",
            "buscame unos", "buscame uno", "buscame una", "buscame unas",
            "buscar unos", "buscar uno", "buscar una", "buscar unas",
            "quiero unos", "quiero uno", "quiero una", "quiero unas",
            "comprar", "conseguir", "buscame","buscar","quiero"
        ]
        resultado = None
        for clave in cortar_cadenas:
            if clave in mensaje:
                indice_frase_clave = mensaje.find(clave)
                resultado = mensaje[indice_frase_clave + len(clave):].strip()
                break
        lista = None
        if resultado:
            lista=buscar_Producto("Consulta_Nombre", resultado)
            if len(lista) > LIMITE:
                lista = random.sample(lista, LIMITE)
            if lista:
                informacion = mostrar_Informacion(lista)
                dispatcher.utter_message(f"Claro aquí tienes!\n{informacion}")
            else:
                dispatcher.utter_message("Lo siento, no encontré nada")
        else:
            dispatcher.utter_message("Lo siento, no encontré nada")

        return [SlotSet("consult_list", lista)]
    
class ActionWithConsultarCategoria(Action):
    def name(self) -> Text:
        return "action_consultar_categoria"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        categoria = next(tracker.get_latest_entity_values("categoria"), None)
        if not categoria:   
            dispatcher.utter_message("No se encontró dicha categoria")
            return []
        lista=buscar_Producto("Consulta_Categoria",categoria)
        if len(lista) > LIMITE:
                lista = random.sample(lista, LIMITE)
        if lista:
            informacion = mostrar_Informacion(lista)
            dispatcher.utter_message(f"Podes conseguir:\n{informacion}")
        else:
            dispatcher.utter_message(f"Lo siento, no encontré productos {categoria}")
        return [SlotSet("consult_list", lista)]
#Hasta acá se hacen consultas de los productos.

#nlu fallback
def numeroStringPos(posicion, posUltimo) -> int:
    mi_diccionario = {
        'primero': 0,
        'primer': 0,
        'primera': 0,
        'segundo': 1,
        'segunda': 1,
        'tercer': 2,
        'tercero': 2,
        'tercera': 2,
        'cuarto': 3,
        'cuarta': 3,
        'quinto': 4,
        'sexto': 5,
        'septimo': 6,
        'octavo': 7,
        'noveno': 8,
        'decimo': 9,
        'ultimo': posUltimo,
        'ultima': posUltimo
    }
    if posicion in mi_diccionario:
        return mi_diccionario[posicion]
    else:
        try:
            return int(posicion)-1
        except Exception:
            return None  


class ActionAgregarAlCarrito(Action):
    def name(self) -> Text:
        return "action_añadir_al_carrito"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        mensaje = tracker.latest_message["text"]
        numeros = [int(numero) for numero in re.findall(r'\d+', mensaje)]

        lista_consultas = tracker.get_slot("consult_list")
        carrito = tracker.get_slot("shopping_list")
        if (not numeros or len(numeros)==1):
            posicion = next(tracker.get_latest_entity_values("posicion"),None)
            nro = numeroStringPos(posicion,len(lista_consultas)-1)
            if nro is not None and 0 <= nro < len(lista_consultas):
                carrito.append(lista_consultas[nro])
                dispatcher.utter_message(f"Producto añadido exitosamente")
            else:
                dispatcher.utter_message(f"No se pudo añadir el producto")
        else:
            cant_agregados = 0
            for numero in numeros:
                numero = numero -1
                if 0 <= numero < len(lista_consultas):
                    cant_agregados = cant_agregados + 1
                    carrito.append(lista_consultas[numero])
            dispatcher.utter_message(f"Se agregaron: {cant_agregados} productos")
        return [SlotSet("shopping_list",carrito)]
    
class ActionMostrarCarrito(Action):
    def name(self) -> Text:
        return "action_mostrar_carrito"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carrito = tracker.get_slot("shopping_list")
        formatted_msg = 'Lo siento, no tienes ningún producto'
        if carrito:
            formatted_msg = mostrar_Informacion(carrito)
        dispatcher.utter_message(f"{formatted_msg}")
        return []
    
class ActionSaludar(Action):
    def name(self) -> Text:
        return "action_saludar"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       # first_name = None
        first_name = tracker.latest_message.get("metadata").get("message", {}).get("from", {}).get("first_name")
        #print(tracker.latest_message.get("metadata").get("message", {}).get("from", {}))
        if first_name:
            message = f"Hola, {first_name}! En qué puedo ayudarte?"
        else:
            message = "Hola, ¿en qué puedo ayudarte?"
        dispatcher.utter_message(text=message)
        return []
    
# Agregado de descuentos
class ActionDescuentoWithProlog(Action):
    def name(self) -> Text:
        return "action_descuentos_aleatorio"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        formato = "Lo siento, hasta el momento no tengo descuento para ofrecer"
        lista = []
        descuentos_ya_consultados = tracker.get_slot("descuentos_cat_slot") or []
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('/home/nahuel/ChatBot/base_conocimiento2.pl')")
                categorias_disponibles = ['Pastas Secas', 'Encurtidos', 'Conservas', 'Aperitivo y Coctel', 'Vino',
                                          'Limpieza de Ropa', 'Limpieza Pisos y Grandes Superficie']
                if (len(descuentos_ya_consultados) < len(categorias_disponibles)):
                    categorias_disponibles = [p for p in categorias_disponibles if p not in descuentos_ya_consultados]
                else:
                    descuentos_ya_consultados = []
                
                categoria_aleatoria = random.choice(categorias_disponibles)
                query = f"consulta_categoria_con_descuento('{categoria_aleatoria}', Producto, PrecioConDescuento, DescuentoPorcentaje, Marca, Peso)"
                descuentos_ya_consultados.append(categoria_aleatoria)
                productos_con_descuento = prolog_thread.query(query)
                # Tengo que modificarlo para que sea agregado al dispatcher.
                if productos_con_descuento:
                    productos_con_descuento = list(productos_con_descuento)
                    lista = list(productos_con_descuento)
                    lista = devolver_Lista_De_Prolog(lista)
                    descuento = lista[0].strip('[]').split(';')[1]
                    descuento = float(descuento) * 100
                    formato = f"Los siguientes productos tienen un descuento del {descuento}% \n"+mostrar_Informacion(lista)
                    
        dispatcher.utter_message(text=formato)   
        return [SlotSet("consult_list", lista),SlotSet("descuentos_cat_slot", descuentos_ya_consultados)]
model = None
explicativas = None
def entrenarModelo(id_user,nombre_user):
    df_gustos = pd.read_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv')
    global explicativas
    if(len(df_gustos) >= 30):
        df = pd.get_dummies(data=df_gustos, drop_first=True)
        explicativas = df.drop(columns='me_gusta')
        objetivo = df.me_gusta
        global model
        model = DecisionTreeClassifier(max_depth=5)
        model.fit(X=explicativas, y=objetivo)
        dot_data = tree.export_graphviz(model,out_file=None,feature_names=explicativas.columns.tolist(),
                                class_names=df['me_gusta'].astype(str).unique().tolist(),
                                filled=True, rounded=True,
                                special_characters=True)
        graph = graphviz.Source(dot_data)
        graph.render(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}')
    return None   
fue_ejecutado = False
# CHEQUEAR LO DEL DEF RUN
class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        global fue_ejecutado
        if fue_ejecutado:
            metadata = tracker.latest_message.get("metadata").get("message", {}).get("from", {})
            nombre_user = metadata.get("first_name")
            id_user = metadata.get("id")
            
            df_usuarios = pd.read_csv(f'{RUTA_USUARIOS}')
            if id_user in df_usuarios['id'].values:
                dispatcher.utter_message(text="Hola de nuevo! Te gustaría conocer nuestros descuentos especiales?")
                entrenarModelo(id_user,nombre_user)
            else:
                # Agregar el nuevo usuario al DataFrame
                new_user = pd.DataFrame({'id': [id_user], 'nombre': [nombre_user], 'gastos': [0]})
                df_usuarios = pd.concat([df_usuarios, new_user], ignore_index=True)
                df_usuarios.to_csv(RUTA_USUARIOS, index=False)
                columnas = ["me_gusta", "Marca", "Categoria", "Subcategoria"]
                nombre_archivo = f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv'
                # Abre el archivo CSV en modo escritura
                with open(nombre_archivo, mode="w", newline="") as archivo_csv:
                    escritor = csv.writer(archivo_csv)
                    escritor.writerow(columnas)
                dispatcher.utter_message(text="Hola! Te gustaría conocer nuestros descuentos especiales?")
                
            # Ejecuta la acción que recomienda descuentos
            action_descuentos = ActionDescuentoWithProlog()
            action_descuentos.run(dispatcher, tracker, domain)
            descuentos_ya_consultados = tracker.get_slot("descuentos_cat_slot") or []
            print(descuentos_ya_consultados)
            return [SessionStarted(), ActionExecuted("action_listen")]
        else:
            fue_ejecutado = True
            return [SessionStarted(), ActionExecuted("action_listen")]

def prediccionConIndice(indice_tupla):
    global model
    global explicativas
    df_tupla_aux = df.loc[indice_tupla, ['Marca', 'Categoria', 'Subcategoria']].to_frame().T
    df_tupla_aux = pd.get_dummies(data=df_tupla_aux)
    df_tupla = pd.DataFrame(False, index=[0], columns=explicativas.columns)
    for columna in explicativas.columns:
        if columna in df_tupla_aux.columns:
            df_tupla.at[0, columna] = True
    y_pred = model.predict(df_tupla)
    return y_pred[00]

# A partir de acá es todo lo nuevo para implementar árboles de decisión y finalizar la compra
class ActionRecomendar(Action):
    def name(self) -> Text:
        return "action_recomendar"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        df = pd.read_csv('/home/nahuel/ChatBot/datos_productos.csv')
        metadata = tracker.latest_message.get("metadata").get("message", {}).get("from", {})
        nombre_user = metadata.get("first_name")
        id_user = metadata.get("id")
        df_gustos = pd.read_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv')

        cantidad_tuplas = len(df)
        indice_aleatorio = random.randint(0,cantidad_tuplas -1)

        informacion = None
        global explicativas
        if(len(df_gustos) >= 30 and not explicativas.empty):
            cortar = False
            while not cortar:
                if(prediccionConIndice(indice_aleatorio) == 1):
                    cortar = True
                    informacion = "El siguiente producto podría llegar a gustarte:\n"
                else:
                    print("Hola")
                    indice_aleatorio = random.randint(0,cantidad_tuplas -1)
        else:
            informacion = "Te podría llegar a recomendar el siguiente producto\n"
        informacion = informacion + mostrar_Informacion([indice_aleatorio])
        dispatcher.utter_message(text=informacion)
        return [SlotSet("producto_recomendado",indice_aleatorio)]
        
class ActionAddNotLike(Action):
    def name(self) -> Text:
        return "action_no_gusto"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]) -> List[Dict[Text,Any]]:
        producto_recomendado = tracker.get_slot("producto_recomendado") or None
        producto_recomendado=int(producto_recomendado)
        mensaje = None
        if(producto_recomendado):
            metadata = tracker.latest_message.get("metadata").get("message", {}).get("from", {})
            nombre_user = metadata.get("first_name")
            id_user = metadata.get("id")
            global df
            marca = df['Marca'].iloc[producto_recomendado]
            categoria = df['Categoria'].iloc[producto_recomendado]
            subcategoria = df['Subcategoria'].iloc[producto_recomendado]
            me_gusta = 0
            nueva_fila = {
                'me_gusta': me_gusta,
                'Marca': marca,
                'Categoria': categoria,
                'Subcategoria': subcategoria
            }
            nueva_fila_df = pd.DataFrame(nueva_fila, index=[0])
            print(nueva_fila)
            df_gustos = pd.read_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv')
            df_gustos = pd.concat([df_gustos, nueva_fila_df], ignore_index=True)
            df_gustos = df_gustos.drop_duplicates()
            print(df_gustos)
            df_gustos.to_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv', index=False)
            print(producto_recomendado)
            mensaje = "Gracias por avisarme! Lo tendré en cuenta para un futuro"
        else:
            mensaje = "Lo siento, no tengo ningún producto que te haya recomendado"
        dispatcher.utter_message(text=mensaje)
        return []
    
class ActionShowTotal(Action):
    def name(self) -> Text:
        return "action_mostrar_total"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carrito = tracker.get_slot("shopping_list")
        informacion = mostrar_Informacion(carrito)

        suma_total =0.0
        filas = informacion.strip().split('\n')
        # Recorrer cada fila y extraer el último número
        for fila in filas:
            partes = fila.split()
            numero = float(partes[-1])
            suma_total += numero
        dispatcher.utter_message(text=f"El monto total que llevas en el carrito es: ${suma_total}")
        return [SlotSet("precio_total_slot",suma_total)]

def agregarListaAlCSV(lista,id_user,nombre_user):
    resultados = []
    for elemento in lista:
        # Comprobar si el elemento es una cadena que comienza y termina con comillas simples
        if isinstance(elemento, str):
            match = re.search(r'\[(\d+)\]', elemento)
            indice = int(match.group(1))
            resultados.append(indice)
        elif isinstance(elemento, int):
            resultados.append(elemento)
    df_user = pd.read_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv')
    df_temp = pd.DataFrame(columns=["me_gusta", "Marca", "Categoria", "Subcategoria"])
    #Recorrer la lista de índices y agregar las filas al DataFrame temporal
    for numero_fila in resultados:
        fila_interes = df.loc[numero_fila]
        nueva_fila = pd.DataFrame([[1, fila_interes["Marca"], fila_interes["Categoria"], fila_interes["Subcategoria"]]],
                                columns=["me_gusta", "Marca", "Categoria", "Subcategoria"])
        
        df_temp = pd.concat([df_temp, nueva_fila], ignore_index=True)
    # Concatenar el DataFrame temporal con el segundo DataFrame (df_user)
    df_user = pd.concat([df_user, df_temp], ignore_index=True)
    df_user = df_user.drop_duplicates()
    df_user.to_csv(f'/home/nahuel/ChatBot/Usuarios/{id_user}_{nombre_user}.csv', index=False)
    return []

def agregarPrecioAlCSV(precio,id_user):
    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('/home/nahuel/ChatBot/Usuarios/usuarios.csv')
    fila = df[df['id'] == id_user]
    if not fila.empty:
        df.loc[df['id'] == id_user, 'gastos'] += precio
        df.to_csv('/home/nahuel/ChatBot/Usuarios/usuarios.csv', index=False)
    else:
        print(f"Usuario con ID {id_user} no encontrado.")
    return []

class ActionCompraFinalizada(Action):
    def name(self) -> Text:
        return "action_finalizar_compra"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        carrito = tracker.get_slot("shopping_list")
        precio_total = tracker.get_slot("precio_total_slot") or 0
        metadata = tracker.latest_message.get("metadata").get("message", {}).get("from", {})
        nombre_user = metadata.get("first_name")
        id_user = metadata.get("id")
        agregarListaAlCSV(carrito,id_user,nombre_user)
        agregarPrecioAlCSV(precio_total,id_user)
        dispatcher.utter_message(text="Compra finalizada con éxito, la cuenta ha sido actualizada")
        carrito = []
        return [SlotSet("shopping_list",carrito)]
