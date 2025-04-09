"""
Sistema de Gestión de Horarios con Prioridades
Autor: [Mateo Restrepo Ciro]

Este sistema compara el rendimiento de algoritmos de ordenamiento en arreglos y listas enlazadas,
implementando versiones recursivas e iterativas de cada algoritmo.
"""

import time
import random
import sys
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

# Estructura de lista enlazada
class Nodo:
    def _init_(self, valor):
        self.valor = valor
        self.siguiente = None

class ListaEnlazada:
    def _init_(self):
        self.cabeza = None
        self.longitud = 0
    
    def agregar(self, valor):
        nuevo = Nodo(valor)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self.longitud += 1
    
    def mostrar(self):
        valores = []
        actual = self.cabeza
        while actual:
            valores.append(actual.valor)
            actual = actual.siguiente
        return valores
    
    def copiar(self):
        nueva_lista = ListaEnlazada()
        actual = self.cabeza
        while actual:
            nueva_lista.agregar(actual.valor)
            actual = actual.siguiente
        return nueva_lista

# Algoritmos para arreglos - Versiones iterativas y recursivas
def insertion_sort_iterativo(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

def insertion_sort_recursivo(arr, n=None):
    if n is None:
        n = len(arr)
    if n <= 1:
        return
    insertion_sort_recursivo(arr, n-1)
    key = arr[n-1]
    j = n-2
    while j >= 0 and arr[j] > key:
        arr[j+1] = arr[j]
        j -= 1
    arr[j+1] = key

def quick_sort_recursivo(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort_recursivo(left) + middle + quick_sort_recursivo(right)

def quick_sort_iterativo(arr):
    stack = [(0, len(arr)-1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = arr[(low + high) // 2]
        i = low - 1
        j = high + 1
        while True:
            i += 1
            while arr[i] < pivot:
                i += 1
            j -= 1
            while arr[j] > pivot:
                j -= 1
            if i >= j:
                break
            arr[i], arr[j] = arr[j], arr[i]
        stack.append((low, j))
        stack.append((j+1, high))

def cycle_sort_iterativo(arr):
    writes = 0
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

# Algoritmos para listas enlazadas - Versiones iterativas y recursivas
def insertion_sort_lista_iterativo(lista):
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

def insertion_sort_lista_recursivo(nodo):
    if not nodo or not nodo.siguiente:
        return nodo
    resto = insertion_sort_lista_recursivo(nodo.siguiente)
    if nodo.valor <= resto.valor:
        nodo.siguiente = resto
        return nodo
    actual = resto
    while actual.siguiente and nodo.valor > actual.siguiente.valor:
        actual = actual.siguiente
    nodo.siguiente = actual.siguiente
    actual.siguiente = nodo
    return resto

def quick_sort_lista_recursivo(nodo):
    if nodo is None or nodo.siguiente is None:
        return nodo

    pivot = nodo
    izquierda_cabeza = izquierda_actual = Nodo(None)
    derecha_cabeza = derecha_actual = Nodo(None)

    actual = nodo.siguiente
    while actual:
        if actual.valor < pivot.valor:
            izquierda_actual.siguiente = actual
            izquierda_actual = izquierda_actual.siguiente
        else:
            derecha_actual.siguiente = actual
            derecha_actual = derecha_actual.siguiente
        actual = actual.siguiente

    izquierda_actual.siguiente = None
    derecha_actual.siguiente = None

    izquierda = quick_sort_lista_recursivo(izquierda_cabeza.siguiente)
    derecha = quick_sort_lista_recursivo(derecha_cabeza.siguiente)

    if izquierda:
        actual = izquierda
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = pivot
    else:
        izquierda = pivot

    pivot.siguiente = derecha
    return izquierda

def quick_sort_lista_iterativo(lista):
    if not lista.cabeza or not lista.cabeza.siguiente:
        return lista

    stack = []
    stack.append((lista.cabeza, None))  # (head, tail)

    nueva_cabeza = None
    nueva_cola = None

    while stack:
        head, tail = stack.pop()
        if not head or head == tail:
            continue

        pivot = head
        current = head.siguiente
        pivot.siguiente = None

        menor_head = menor_tail = None
        mayor_head = mayor_tail = None

        while current and current != tail:
            siguiente = current.siguiente
            if current.valor < pivot.valor:
                if not menor_head:
                    menor_head = menor_tail = current
                else:
                    menor_tail.siguiente = current
                    menor_tail = current
            else:
                if not mayor_head:
                    mayor_head = mayor_tail = current
                else:
                    mayor_tail.siguiente = current
                    mayor_tail = current
            current = siguiente

        if menor_tail:
            menor_tail.siguiente = None
        if mayor_tail:
            mayor_tail.siguiente = None

        stack.append((mayor_head, mayor_tail))
        stack.append((pivot, None))
        stack.append((menor_head, menor_tail))

        if not nueva_cabeza:
            current = None
            while stack:
                temp_head, temp_tail = stack[-1]
                if not temp_head:
                    stack.pop()
                    continue
                if not current:
                    current = temp_head
                    nueva_cabeza = current
                else:
                    current.siguiente = temp_head
                    current = temp_tail if temp_tail else temp_head
                stack.pop()
            if current:
                current.siguiente = None
            nueva_cola = current

    lista.cabeza = nueva_cabeza
    return lista

def cycle_sort_lista_iterativo(lista):
    if not lista.cabeza:
        return

    actual = lista.cabeza
    while actual:
        pos = actual
        siguiente = pos.siguiente

        while siguiente:
            if siguiente.valor < pos.valor:
                pos.valor, siguiente.valor = siguiente.valor, pos.valor
            siguiente = siguiente.siguiente

        actual = actual.siguiente

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

def medir_tiempo(func, *args):
    start = time.time()
    func(*args)
    return time.time() - start

def medir_memoria(func, *args):
    def wrapper():
        return func(*args)
    mem_usage = memory_usage(wrapper, interval=0.01, timeout=1)
    return max(mem_usage) - min(mem_usage)

def analizar_rendimiento(datos):
    resultados = []
    
    # Crear copias de los datos para no modificar el original
    arr = datos.copy()
    
    # Algoritmos para arreglos - Iterativos
    tiempo = medir_tiempo(insertion_sort_iterativo, arr.copy())
    memoria = medir_memoria(insertion_sort_iterativo, arr.copy())
    resultados.append({
        'algoritmo': 'Insertion Sort', 
        'tipo': 'Array', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    arr = datos.copy()
    tiempo = medir_tiempo(quick_sort_iterativo, arr.copy())
    memoria = medir_memoria(quick_sort_iterativo, arr.copy())
    resultados.append({
        'algoritmo': 'Quick Sort', 
        'tipo': 'Array', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    arr = datos.copy()
    tiempo = medir_tiempo(cycle_sort_iterativo, arr.copy())
    memoria = medir_memoria(cycle_sort_iterativo, arr.copy())
    resultados.append({
        'algoritmo': 'Cycle Sort', 
        'tipo': 'Array', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    # Algoritmos para arreglos - Recursivos
    arr = datos.copy()
    tiempo = medir_tiempo(insertion_sort_recursivo, arr.copy())
    memoria = medir_memoria(insertion_sort_recursivo, arr.copy())
    resultados.append({
        'algoritmo': 'Insertion Sort', 
        'tipo': 'Array', 
        'version': 'Recursivo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    arr = datos.copy()
    tiempo = medir_tiempo(lambda x: quick_sort_recursivo(x), arr.copy())
    memoria = medir_memoria(lambda x: quick_sort_recursivo(x), arr.copy())
    resultados.append({
        'algoritmo': 'Quick Sort', 
        'tipo': 'Array', 
        'version': 'Recursivo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    # Listas enlazadas - Iterativos
    lista = ListaEnlazada()
    for item in datos:
        lista.agregar(item)
    copia_lista = lista.copiar()
    tiempo = medir_tiempo(insertion_sort_lista_iterativo, copia_lista)
    memoria = medir_memoria(insertion_sort_lista_iterativo, lista.copiar())
    resultados.append({
        'algoritmo': 'Insertion Sort', 
        'tipo': 'Lista', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    copia_lista = lista.copiar()
    tiempo = medir_tiempo(quick_sort_lista_iterativo, copia_lista)
    memoria = medir_memoria(quick_sort_lista_iterativo, lista.copiar())
    resultados.append({
        'algoritmo': 'Quick Sort', 
        'tipo': 'Lista', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    copia_lista = lista.copiar()
    tiempo = medir_tiempo(cycle_sort_lista_iterativo, copia_lista)
    memoria = medir_memoria(cycle_sort_lista_iterativo, lista.copiar())
    resultados.append({
        'algoritmo': 'Cycle Sort', 
        'tipo': 'Lista', 
        'version': 'Iterativo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    # Listas enlazadas - Recursivos
    copia_lista = lista.copiar()
    tiempo = medir_tiempo(lambda l: setattr(l, 'cabeza', insertion_sort_lista_recursivo(l.cabeza)), copia_lista)
    memoria = medir_memoria(lambda l: setattr(l, 'cabeza', insertion_sort_lista_recursivo(l.cabeza)), lista.copiar())
    resultados.append({
        'algoritmo': 'Insertion Sort', 
        'tipo': 'Lista', 
        'version': 'Recursivo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    copia_lista = lista.copiar()
    tiempo = medir_tiempo(lambda l: setattr(l, 'cabeza', quick_sort_lista_recursivo(l.cabeza)), copia_lista)
    memoria = medir_memoria(lambda l: setattr(l, 'cabeza', quick_sort_lista_recursivo(l.cabeza)), lista.copiar())
    resultados.append({
        'algoritmo': 'Quick Sort', 
        'tipo': 'Lista', 
        'version': 'Recursivo',
        'tiempo': tiempo,
        'memoria': memoria
    })
    
    return resultados

def guardar_resultados(resultados, n, filename='resultados.txt'):
    with open(filename, 'w') as f:
        f.write("=== RESULTADOS DE ORDENAMIENTO ===\n")
        f.write(f"Datos analizados: {n} elementos\n\n")
        f.write("{:<20} {:<10} {:<12} {:<15} {:<15}\n".format(
            'Algoritmo', 'Tipo', 'Versión', 'Tiempo (s)', 'Memoria (MB)'))
        f.write("-"*72 + "\n")
        
        for r in resultados:
            tiempo = "{:.6f}".format(r['tiempo'])
            memoria = "{:.4f}".format(r.get('memoria', 0))
            f.write("{:<20} {:<10} {:<12} {:<15} {:<15}\n".format(
                r['algoritmo'], 
                r['tipo'], 
                r['version'],
                tiempo,
                memoria
            ))
        
        f.write("\n=== COMPLEJIDADES TEÓRICAS ===\n")
        f.write("Insertion Sort:\n")
        f.write("  - Tiempo: O(n²)\n")
        f.write("  - Espacio: O(1)\n")
        f.write("  - Estable: Sí\n")
        f.write("\nQuick Sort:\n")
        f.write("  - Tiempo: O(n log n) promedio, O(n²) peor caso\n")
        f.write("  - Espacio: O(log n)\n")
        f.write("  - Estable: No\n")
        f.write("\nCycle Sort:\n")
        f.write("  - Tiempo: O(n²)\n")
        f.write("  - Espacio: O(1)\n")
        f.write("  - Estable: Sí\n")
        f.write("  - Minimiza escrituras en memoria\n")

def mostrar_resultados(resultados, n):
    # Diccionario de complejidades teóricas
    complejidades = {
        'Insertion Sort': 'O(n²) tiempo | O(1) espacio',
        'Quick Sort': 'O(n log n) tiempo | O(log n) espacio',
        'Cycle Sort': 'O(n²) tiempo | O(1) espacio'
    }
    
    print("\n=== RESULTADOS ===")
    print(f"Datos analizados: {n} elementos")
    print("{:<20} {:<10} {:<12} {:<15} {:<15}".format(
        'Algoritmo', 'Tipo', 'Versión', 'Tiempo (s)', 'Memoria (MB)'))
    print("-"*72)
    
    for r in resultados:
        tiempo = "{:.6f}".format(r['tiempo'])
        memoria = "{:.4f}".format(r.get('memoria', 0))
        print("{:<20} {:<10} {:<12} {:<15} {:<15}".format(
            r['algoritmo'], 
            r['tipo'], 
            r['version'],
            tiempo,
            memoria
        ))
    
    # Gráfico de tiempos
    plt.figure(figsize=(14, 6))
    nombres = [f"{r['algoritmo']}\n({r['tipo']}, {r['version']})" for r in resultados]
    tiempos = [r['tiempo'] for r in resultados]
    
    plt.subplot(1, 2, 1)
    plt.bar(nombres, tiempos)
    plt.title(f'Comparación de Tiempos (n={n})')
    plt.ylabel('Tiempo (segundos)')
    plt.xticks(rotation=45, ha='right')
    
    # Gráfico de memoria
    memorias = [r.get('memoria', 0) for r in resultados]
    
    plt.subplot(1, 2, 2)
    plt.bar(nombres, memorias, color='orange')
    plt.title(f'Uso de Memoria (n={n})')
    plt.ylabel('Memoria (MB)')
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('resultados.png')
    plt.show()
    
    # Guardar resultados en archivo
    guardar_resultados(resultados, n)
    print("\nResultados guardados en 'resultados.txt'")

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

if _name_ == "_main_":
    main()