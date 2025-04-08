"""
Proyecto: Sistema de Gestión de Horarios con Prioridades
Autor: [Tu nombre]
Descripción: Comparación de algoritmos de ordenamiento con análisis de complejidad
"""

import time
import random
import math
import matplotlib.pyplot as plt
from typing import List, Union

# Clase para lista enlazada simple
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def agregar(self, valor):
        nuevo_nodo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def mostrar(self):
        valores = []
        actual = self.cabeza
        while actual:
            valores.append(actual.valor)
            actual = actual.siguiente
        return valores

# Algoritmos de ordenamiento para listas (arrays)
def bubble_sort(arr: List[Union[int, str]]) -> List[Union[int, str]]:
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def bubble_sort_recursivo(arr: List[Union[int, str]], n: int = None) -> List[Union[int, str]]:
    if n is None:
        n = len(arr)
    if n == 1:
        return arr
    for i in range(n-1):
        if arr[i] > arr[i+1]:
            arr[i], arr[i+1] = arr[i+1], arr[i]
    return bubble_sort_recursivo(arr, n-1)

def selection_sort(arr: List[Union[int, str]]) -> List[Union[int, str]]:
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def selection_sort_recursivo(arr: List[Union[int, str]], index: int = 0) -> List[Union[int, str]]:
    if index >= len(arr)-1:
        return arr
    min_idx = index
    for j in range(index+1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[index], arr[min_idx] = arr[min_idx], arr[index]
    return selection_sort_recursivo(arr, index+1)

def tim_sort(arr: List[Union[int, str]]) -> List[Union[int, str]]:
    return sorted(arr)  # Python usa TimSort por defecto en sorted()

# Algoritmos para listas enlazadas
def bubble_sort_lista_enlazada(lista: ListaEnlazada):
    if not lista.cabeza:
        return
    cambiado = True
    while cambiado:
        cambiado = False
        actual = lista.cabeza
        previo = None
        while actual.siguiente:
            siguiente = actual.siguiente
            if actual.valor > siguiente.valor:
                # Intercambiar nodos
                if previo:
                    previo.siguiente = siguiente
                else:
                    lista.cabeza = siguiente
                actual.siguiente = siguiente.siguiente
                siguiente.siguiente = actual
                previo = siguiente
                cambiado = True
            else:
                previo = actual
                actual = actual.siguiente

def bubble_sort_lista_enlazada_recursivo(nodo_actual, cambiado=True):
    if not nodo_actual or not nodo_actual.siguiente or not cambiado:
        return
    
    cambiado = False
    if nodo_actual.valor > nodo_actual.siguiente.valor:
        # Intercambiar valores (simplificado para recursión)
        nodo_actual.valor, nodo_actual.siguiente.valor = nodo_actual.siguiente.valor, nodo_actual.valor
        cambiado = True
    
    # Llamada recursiva
    bubble_sort_lista_enlazada_recursivo(nodo_actual.siguiente, cambiado)

def selection_sort_lista_enlazada(lista: ListaEnlazada):
    actual = lista.cabeza
    while actual:
        min_nodo = actual
        siguiente = actual.siguiente
        while siguiente:
            if siguiente.valor < min_nodo.valor:
                min_nodo = siguiente
            siguiente = siguiente.siguiente
        # Intercambiar valores
        actual.valor, min_nodo.valor = min_nodo.valor, actual.valor
        actual = actual.siguiente

# Funciones para cálculo de complejidad
def calcular_complejidad(algoritmo: str, n: int) -> str:
    if "Bubble" in algoritmo:
        return f"O(n²) [n={n}] -> {n**2}"
    elif "Selection" in algoritmo:
        return f"O(n²) [n={n}] -> {n**2}"
    elif "Tim" in algoritmo:
        return f"O(n log n) [n={n}] -> {round(n * math.log2(n) if n > 0 else 0, 2)}"
    return "Desconocida"

def calcular_complejidad_espacial(algoritmo: str) -> str:
    if "Bubble" in algoritmo or "Selection" in algoritmo:
        return "O(1)"
    elif "Tim" in algoritmo:
        return "O(n)"
    return "Desconocida"

# Funciones auxiliares
def generar_datos_aleatorios(cantidad: int, tipo: str) -> List[Union[int, str]]:
    if tipo == 'numeros':
        return [random.randint(1, 1000) for _ in range(cantidad)]
    elif tipo == 'letras':
        return [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(cantidad)]
    else:
        return []

def cargar_desde_archivo(nombre_archivo: str) -> List[Union[int, str]]:
    try:
        with open(nombre_archivo, 'r') as f:
            contenido = f.read().strip().split(',')
            datos = []
            for item in contenido:
                item = item.strip()
                if item.isdigit():
                    datos.append(int(item))
                else:
                    datos.append(item)
            return datos
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def medir_tiempo(func, *args):
    inicio = time.time()
    func(*args)
    fin = time.time()
    return fin - inicio

def mostrar_comparacion(resultados, n):
    print("\n--- Resultados de Comparación ---")
    print("{:<25} {:<15} {:<15} {:<20} {:<15}".format(
        'Algoritmo', 'Tipo', 'Tiempo (s)', 'Complejidad Temp.', 'Complejidad Esp.'))
    print("-" * 90)
    
    for resultado in resultados:
        temp = calcular_complejidad(resultado['algoritmo'], n)
        esp = calcular_complejidad_espacial(resultado['algoritmo'])
        
        print("{:<25} {:<15} {:<15.6f} {:<20} {:<15}".format(
            resultado['algoritmo'], 
            resultado['tipo'], 
            resultado['tiempo'],
            temp,
            esp
        ))
    
    # Crear gráfico
    algoritmos = [f"{r['algoritmo']} ({r['tipo']})" for r in resultados]
    tiempos = [r['tiempo'] for r in resultados]
    
    plt.figure(figsize=(12, 6))
    plt.bar(algoritmos, tiempos)
    plt.xlabel('Algoritmo')
    plt.ylabel('Tiempo (segundos)')
    plt.title(f'Comparación de Algoritmos (n={n})')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Guardar gráfico
    plt.savefig('comparacion_ordenamiento.png')
    print("\nGráfico guardado como 'comparacion_ordenamiento.png'")
    plt.show()

def explicar_complejidad():
    print("\n--- Explicación de Complejidad ---")
    print("1. Bubble Sort:")
    print("   - Complejidad temporal: O(n²) en peor caso y promedio, O(n) en mejor caso (lista ordenada)")
    print("   - Complejidad espacial: O(1) (ordenamiento in-place)")
    
    print("\n2. Selection Sort:")
    print("   - Complejidad temporal: O(n²) en todos los casos")
    print("   - Complejidad espacial: O(1) (ordenamiento in-place)")
    
    print("\n3. Tim Sort:")
    print("   - Complejidad temporal: O(n log n) en peor caso, O(n) en mejor caso")
    print("   - Complejidad espacial: O(n)")
    
    print("\nNota: Las versiones recursivas generalmente mantienen la misma complejidad,")
    print("pero pueden usar más memoria por la pila de llamadas recursivas.")

def menu_principal():
    print("\n--- Sistema de Gestión de Horarios con Prioridades ---")
    print("1. Generar datos aleatorios")
    print("2. Ingresar datos manualmente")
    print("3. Cargar datos desde archivo")
    print("4. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion

def main():
    datos = []
    lista_enlazada = ListaEnlazada()
    
    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            cantidad = int(input("Cantidad de datos a generar: "))
            tipo = input("Tipo de datos (numeros/letras): ").lower()
            datos = generar_datos_aleatorios(cantidad, tipo)
            
        elif opcion == '2':
            entrada = input("Ingrese datos separados por comas: ")
            datos = [item.strip() for item in entrada.split(',')]
            # Intentar convertir a números si es posible
            for i, item in enumerate(datos):
                if item.isdigit():
                    datos[i] = int(item)
                    
        elif opcion == '3':
            archivo = input("Nombre del archivo CSV: ")
            datos = cargar_desde_archivo(archivo)
            
        elif opcion == '4':
            print("Saliendo del programa...")
            break
            
        else:
            print("Opción no válida. Intente nuevamente.")
            continue
        
        if not datos:
            print("No hay datos para ordenar. Intente nuevamente.")
            continue
        
        # Actualizar lista enlazada
        lista_enlazada = ListaEnlazada()
        for item in datos:
            lista_enlazada.agregar(item)
        
        print("\nDatos a ordenar:", datos[:10], "...") if len(datos) > 10 else print("\nDatos a ordenar:", datos)
        
        # Medir tiempos
        resultados = []
        n = len(datos)
        
        # Bubble Sort array
        arr_copy = datos.copy()
        tiempo = medir_tiempo(bubble_sort, arr_copy)
        resultados.append({
            'algoritmo': 'Bubble Sort',
            'tipo': 'Array (iter)',
            'tiempo': tiempo
        })
        
        # Bubble Sort recursivo array
        arr_copy = datos.copy()
        tiempo = medir_tiempo(bubble_sort_recursivo, arr_copy)
        resultados.append({
            'algoritmo': 'Bubble Sort',
            'tipo': 'Array (rec)',
            'tiempo': tiempo
        })
        
        # Selection Sort array
        arr_copy = datos.copy()
        tiempo = medir_tiempo(selection_sort, arr_copy)
        resultados.append({
            'algoritmo': 'Selection Sort',
            'tipo': 'Array (iter)',
            'tiempo': tiempo
        })
        
        # Selection Sort recursivo array
        arr_copy = datos.copy()
        tiempo = medir_tiempo(selection_sort_recursivo, arr_copy)
        resultados.append({
            'algoritmo': 'Selection Sort',
            'tipo': 'Array (rec)',
            'tiempo': tiempo
        })
        
        # Tim Sort array
        arr_copy = datos.copy()
        tiempo = medir_tiempo(tim_sort, arr_copy)
        resultados.append({
            'algoritmo': 'Tim Sort',
            'tipo': 'Array (iter)',
            'tiempo': tiempo
        })
        
        # Bubble Sort lista enlazada (iterativo)
        lista_copy = ListaEnlazada()
        for item in datos:
            lista_copy.agregar(item)
        tiempo = medir_tiempo(bubble_sort_lista_enlazada, lista_copy)
        resultados.append({
            'algoritmo': 'Bubble Sort',
            'tipo': 'Lista (iter)',
            'tiempo': tiempo
        })
        
        # Bubble Sort lista enlazada (recursivo)
        lista_copy = ListaEnlazada()
        for item in datos:
            lista_copy.agregar(item)
        tiempo = medir_tiempo(bubble_sort_lista_enlazada_recursivo, lista_copy.cabeza)
        resultados.append({
            'algoritmo': 'Bubble Sort',
            'tipo': 'Lista (rec)',
            'tiempo': tiempo
        })
        
        # Selection Sort lista enlazada
        lista_copy = ListaEnlazada()
        for item in datos:
            lista_copy.agregar(item)
        tiempo = medir_tiempo(selection_sort_lista_enlazada, lista_copy)
        resultados.append({
            'algoritmo': 'Selection Sort',
            'tipo': 'Lista (iter)',
            'tiempo': tiempo
        })
        
        # Mostrar resultados
        mostrar_comparacion(resultados, n)
        explicar_complejidad()
        
        # Guardar resultados
        guardar = input("\n¿Desea guardar los resultados? (s/n): ").lower()
        if guardar == 's':
            with open('resultados_ordenamiento.txt', 'w') as f:
                f.write("Resultados de Comparación (n={})\n".format(n))
                f.write("-" * 50 + "\n")
                f.write("{:<25} {:<15} {:<15} {:<20} {:<15}\n".format(
                    'Algoritmo', 'Tipo', 'Tiempo (s)', 'Complejidad Temp.', 'Complejidad Esp.'))
                for r in resultados:
                    temp = calcular_complejidad(r['algoritmo'], n)
                    esp = calcular_complejidad_espacial(r['algoritmo'])
                    f.write("{:<25} {:<15} {:<15.6f} {:<20} {:<15}\n".format(
                        r['algoritmo'], r['tipo'], r['tiempo'], temp, esp
                    ))
                f.write("\nGrfico guardado como 'comparacion_ordenamiento.png'\n")
            print("Resultados guardados en 'resultados_ordenamiento.txt'")

if __name__ == "__main__":
    main()
