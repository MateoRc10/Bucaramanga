"""
Sistema de Gestión de Horarios con Prioridades
Autor: [Mateo Restrepo Ciro]
"""
import time
import random
import matplotlib.pyplot as plt

# Estructura de lista enlazada
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
    
    def agregar(self, valor):
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
    
    def mostrar(self):
        valores = []
        actual = self.cabeza
        while actual:
            valores.append(actual.valor)
            actual = actual.siguiente
        return valores

# Algoritmos para arreglos
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def cycle_sort(arr):
    0
    for cycle_start in range(0, len(arr)-1):
        item = arr[cycle_start]
        pos = cycle_start
        for i in range(cycle_start+1, len(arr)):
            if arr[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        writes += 1
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start+1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            writes += 1
    return arr

# Algoritmos para listas enlazadas
def insertion_sort_lista(lista):
    if not lista.cabeza:
        return
    sorted_list = None
    actual = lista.cabeza
    while actual:
        siguiente = actual.siguiente
        if not sorted_list or sorted_list.valor >= actual.valor:
            actual.siguiente = sorted_list
            sorted_list = actual
        else:
            temp = sorted_list
            while temp.siguiente and temp.siguiente.valor < actual.valor:
                temp = temp.siguiente
            actual.siguiente = temp.siguiente
            temp.siguiente = actual
        actual = siguiente
    lista.cabeza = sorted_list

# Funciones auxiliares
def generar_datos(cantidad, tipo):
    if tipo == 'numeros':
        return [random.randint(1, 1000) for _ in range(cantidad)]
    elif tipo == 'letras':
        return [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(cantidad)]
    return []

def cargar_archivo(nombre):
    try:
        with open(nombre, 'r') as f:
            return [int(x) if x.strip().isdigit() else x.strip() for x in f.read().split(',')]
    except:
        return []
        raise

def medir_tiempo(func, *args):
    start = time.time()
    func(*args)
    return time.time() - start

def analizar_rendimiento(datos):
    resultados = []
    
    # Arreglos
    arr = datos.copy()
    tiempo = medir_tiempo(insertion_sort, arr)
    resultados.append({'algoritmo': 'Insertion Sort', 'tipo': 'Array', 'tiempo': tiempo})
    
    arr = datos.copy()
    tiempo = medir_tiempo(quick_sort, arr)
    resultados.append({'algoritmo': 'Quick Sort', 'tipo': 'Array', 'tiempo': tiempo})
    
    arr = datos.copy()
    tiempo = medir_tiempo(cycle_sort, arr)
    resultados.append({'algoritmo': 'Cycle Sort', 'tipo': 'Array', 'tiempo': tiempo})
    
    # Listas enlazadas
    lista = ListaEnlazada()
    for item in datos:
        lista.agregar(item)
    tiempo = medir_tiempo(insertion_sort_lista, lista)
    resultados.append({'algoritmo': 'Insertion Sort', 'tipo': 'Lista', 'tiempo': tiempo})
    
    return resultados

def mostrar_resultados(resultados, n):
    print("\n=== RESULTADOS ===")
    print(f"Datos analizados: {n} elementos")
    print("{:<20} {:<10} {:<10}".format('Algoritmo', 'Tipo', 'Tiempo (s)'))
    print("-"*40)
    for r in resultados:
        print("{:<20} {:<10} {:<10.6f}".format(r['algoritmo'], r['tipo'], r['tiempo']))
    
    # Gráfico
    nombres = [f"{r['algoritmo']} ({r['tipo']})" for r in resultados]
    tiempos = [r['tiempo'] for r in resultados]
    
    plt.figure(figsize=(10,5))
    plt.bar(nombres, tiempos)
    plt.title('Comparación de Algoritmos')
    plt.ylabel('Tiempo (segundos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('resultados.png')
    plt.show()

def menu_principal():
    print("\n=== SISTEMA DE GESTIÓN DE HORARIOS ===")
    print("1. Generar datos aleatorios")
    print("2. Ingresar datos manualmente")
    print("3. Cargar desde archivo")
    print("4. Salir")
    return input("Seleccione una opción: ")

def main():
    datos = []
    
    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            n = int(input("Cantidad de datos: "))
            tipo = input("Tipo (numeros/letras): ")
            datos = generar_datos(n, tipo)
            
        elif opcion == '2':
            entrada = input("Ingrese datos separados por comas: ")
            datos = [x.strip() for x in entrada.split(',')]
            
        elif opcion == '3':
            archivo = input("Nombre del archivo: ")
            datos = cargar_archivo(archivo)
            
        elif opcion == '4':
            break
            
        if not datos:
            print("No hay datos válidos")
            continue
            
        print("\nMuestra de datos:", datos[:5], "...")
        
        resultados = analizar_rendimiento(datos)
        mostrar_resultados(resultados, len(datos))
        
        # Explicación de complejidades
        print("\n=== COMPLEJIDADES ===")
        print("Insertion Sort: O(n²) tiempo, O(1) espacio")
        print("Quick Sort: O(n log n) tiempo (promedio), O(log n) espacio")
        print("Cycle Sort: O(n²) tiempo, O(1) espacio")

if __name__ == "__main__":
    main()