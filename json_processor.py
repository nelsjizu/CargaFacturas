import json
import os

def procesar_json(archivo_json):
    """
    Procesa un archivo JSON y extrae claves y valores de cada registro.
    
    Args:
        archivo_json (str): Ruta al archivo JSON
    """
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_json):
        print(f"Error: El archivo '{archivo_json}' no existe.")
        return
    
    try:
        # Cargar el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        print(f"Archivo '{archivo_json}' cargado exitosamente.\n")
        
        # Si es una lista de objetos
        if isinstance(datos, list):
            print(f"Se encontraron {len(datos)} registros en el archivo.\n")
            
            for i, registro in enumerate(datos, 1):
                print(f"--- REGISTRO {i} ---")
                procesar_registro(registro)
                
                # Pausa para revisar cada registro (opcional)
                input("\nPresiona Enter para continuar al siguiente registro...")
                print()
        
        # Si es un solo objeto
        elif isinstance(datos, dict):
            print("Se encontró un objeto JSON.\n")
            print("--- REGISTRO ÚNICO ---")
            procesar_registro(datos)
        
        else:
            print("El formato del JSON no es compatible (debe ser un objeto o una lista de objetos).")
    
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo_json}'.")
    except Exception as e:
        print(f"Error inesperado: {e}")

def procesar_registro(registro, nivel=0):
    """
    Procesa un registro individual y extrae todas las claves y valores.
    
    Args:
        registro: El registro a procesar (dict, list, o valor simple)
        nivel (int): Nivel de anidación para la indentación
    """
    indentacion = "  " * nivel
    
    if isinstance(registro, dict):
        for clave, valor in registro.items():
            if isinstance(valor, (dict, list)):
                print(f"{indentacion}Clave: '{clave}' -> Tipo: {type(valor).__name__}")
                procesar_registro(valor, nivel + 1)
            else:
                print(f"{indentacion}Clave: '{clave}' -> Valor: {valor} (Tipo: {type(valor).__name__})")
    
    elif isinstance(registro, list):
        print(f"{indentacion}Lista con {len(registro)} elementos:")
        for i, elemento in enumerate(registro):
            print(f"{indentacion}  Elemento {i}:")
            procesar_registro(elemento, nivel + 1)
    
    else:
        print(f"{indentacion}Valor: {registro} (Tipo: {type(valor).__name__})")

def extraer_claves_especificas(archivo_json, claves_deseadas):
    """
    Extrae solo claves específicas de cada registro.
    
    Args:
        archivo_json (str): Ruta al archivo JSON
        claves_deseadas (list): Lista de claves que se desean extraer
    """
    
    try:
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        registros_extraidos = []
        
        # Procesar según el tipo de estructura
        if isinstance(datos, list):
            for registro in datos:
                if isinstance(registro, dict):
                    registro_filtrado = {}
                    for clave in claves_deseadas:
                        if clave in registro:
                            registro_filtrado[clave] = registro[clave]
                        else:
                            registro_filtrado[clave] = None
                    registros_extraidos.append(registro_filtrado)
        
        elif isinstance(datos, dict):
            registro_filtrado = {}
            for clave in claves_deseadas:
                if clave in datos:
                    registro_filtrado[clave] = datos[clave]
                else:
                    registro_filtrado[clave] = None
            registros_extraidos.append(registro_filtrado)
        
        return registros_extraidos
    
    except Exception as e:
        print(f"Error al extraer claves específicas: {e}")
        return []

def main():
    """
    Función principal para ejecutar el procesador de JSON.
    """
    print("=== PROCESADOR DE ARCHIVOS JSON ===\n")
    
    # Solicitar la ruta del archivo
    archivo_json = input("Ingresa la ruta del archivo JSON: ").strip()
    
    if not archivo_json:
        print("No se proporcionó ninguna ruta de archivo.")
        return
    
    print("\nOpciones de procesamiento:")
    print("1. Procesar todos los registros completos")
    print("2. Extraer claves específicas")
    
    opcion = input("\nSelecciona una opción (1 o 2): ").strip()
    
    if opcion == "1":
        procesar_json(archivo_json)
    
    elif opcion == "2":
        claves_input = input("Ingresa las claves que deseas extraer (separadas por comas): ")
        claves_deseadas = [clave.strip() for clave in claves_input.split(",") if clave.strip()]
        
        if not claves_deseadas:
            print("No se proporcionaron claves válidas.")
            return
        
        resultados = extraer_claves_especificas(archivo_json, claves_deseadas)
        
        print(f"\n--- CLAVES EXTRAÍDAS ---")
        for i, registro in enumerate(resultados, 1):
            print(f"Registro {i}:")
            for clave, valor in registro.items():
                print(f"  {clave}: {valor}")
            print()
    
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()

# Ejemplo de uso directo:
# procesar_json("mi_archivo.json")
# 
# claves = ["nombre", "edad", "email"]
# resultados = extraer_claves_especificas("mi_archivo.json", claves)
# print(resultados)