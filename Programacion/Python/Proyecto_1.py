import random
import string
import time
import pandas as pd
import matplotlib.pyplot as plt

# 1. Funciones para el origen de datos
def generar_datos_aleatorios(longitud, tipo):
    """Genera datos aleatorios de números o letras."""
    if tipo == "numeros":
        return [random.randint(0, 100) for _ in range(longitud)]
    elif tipo == "letras":
        return [random.choice(string.ascii_letters) for _ in range(longitud)]
    else:
        raise ValueError("Tipo de dato no válido. Usa 'numeros' o 'letras'.")

def entrada_manual():
    """Permite al usuario ingresar datos manualmente."""
    datos = input("Ingresa los datos separados por comas: ")
    return datos.split(",")

def leer_archivo(ruta):
    """Lee datos desde un archivo CSV."""
    datos = pd.read_csv(ruta, header=None)
    return datos.to_numpy().flatten().tolist()

# 2. Algoritmos de ordenamiento
def bubble_sort(arr):
    """Ordena un arreglo usando Bubble Sort (no recursivo)."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def quick_sort(arr):
    """Ordena un arreglo usando Quick Sort (recursivo)."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    """Ordena un arreglo usando Merge Sort (recursivo)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    """Fusión de dos listas ordenadas."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 3. Análisis de rendimiento
def medir_tiempo(algoritmo, datos):
    """Mide el tiempo de ejecución de un algoritmo."""
    inicio = time.time()
    algoritmo(datos.copy())  # Usamos una copia para no modificar los datos originales
    fin = time.time()
    return fin - inicio

def calcular_complejidad(algoritmo):
    """Calcula la complejidad temporal teórica de un algoritmo."""
    if algoritmo == bubble_sort:
        return "O(n²)"
    elif algoritmo == quick_sort:
        return "O(n log n) en promedio, O(n²) en el peor caso"
    elif algoritmo == merge_sort:
        return "O(n log n)"
    else:
        return "Desconocida"

# 4. Generación de tablas y gráficos
def generar_tabla(resultados):
    """Genera una tabla con los resultados."""
    df = pd.DataFrame(resultados)
    print("\nTabla de Resultados:")
    print(df)

def generar_grafica(resultados):
    """Genera una gráfica de barras con los tiempos de ejecución."""
    plt.bar(resultados["Algoritmo"], resultados["Tiempo (s)"])
    plt.xlabel("Algoritmo")
    plt.ylabel("Tiempo (s)")
    plt.title("Comparación de Algoritmos de Ordenamiento")
    plt.show()

# 5. Función principal
def main():
    print("Bienvenido al Sistema de Gestión de Horarios con Prioridades")

    # Selección del origen de datos
    print("\nSelecciona el origen de datos:")
    print("1. Generar datos aleatorios")
    print("2. Ingresar datos manualmente")
    print("3. Leer datos desde un archivo CSV")
    opcion = input("Opción: ")

    if opcion == "1":
        longitud = int(input("Longitud de los datos: "))
        tipo = input("Tipo de datos (numeros/letras): ")
        datos = generar_datos_aleatorios(longitud, tipo)
    elif opcion == "2":
        datos = entrada_manual()
    elif opcion == "3":
        ruta = input("Ruta del archivo CSV: ")
        datos = leer_archivo(ruta)
    else:
        print("Opción no válida. Saliendo del programa.")
        return

    print("\nDatos generados/leídos:", datos)

    # Selección de algoritmos de ordenamiento
    algoritmos = {
        "Bubble Sort": bubble_sort,
        "Quick Sort": quick_sort,
        "Merge Sort": merge_sort,
    }

    resultados = {
        "Algoritmo": [],
        "Tiempo (s)": [],
        "Complejidad Temporal": [],
    }

    for nombre, algoritmo in algoritmos.items():
        tiempo = medir_tiempo(algoritmo, datos)
        complejidad = calcular_complejidad(algoritmo)
        resultados["Algoritmo"].append(nombre)
        resultados["Tiempo (s)"].append(tiempo)
        resultados["Complejidad Temporal"].append(complejidad)

    # Mostrar resultados
    generar_tabla(resultados)
    generar_grafica(resultados)

if __name__ == "__main__":
    main()