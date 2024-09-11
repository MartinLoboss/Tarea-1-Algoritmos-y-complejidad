import numpy as np
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

# Algoritmos de ordenamiento

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def sort_with_builtin(arr):
    return sorted(arr)

# Función para medir el tiempo de los algoritmos
def measure_sorting_time(algorithm, arr):
    start_time = time.time()
    if algorithm == "bubble_sort":
        bubble_sort(arr)
    elif algorithm == "merge_sort":
        merge_sort(arr)
    elif algorithm == "quick_sort":
        arr = quick_sort(arr)
    elif algorithm == "sorted_builtin":
        arr = sort_with_builtin(arr)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return arr, elapsed_time

# Función para guardar el arreglo ordenado
def save_sorted_array(arr, filename):
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filename, 'w') as f:
        f.write(' '.join(map(str, arr)) + '\n')

# Función para guardar el tiempo de análisis
def save_sorting_time(algorithm_name, size, elapsed_time, filename):
    folder_name = f"Result_of_{algorithm_name}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    time_file = os.path.join(folder_name, f"Resultado_{filename}AnalisisTiempo_{size}.txt")
    with open(time_file, 'w') as f:
        f.write(f"Tiempo para ordenar el archivo de tamaño {size}: {elapsed_time} segundos\n")

# Función para procesar todos los archivos y aplicar los algoritmos
def process_datasets():
    dataset_folder = "datasets_a"
    algorithms = ["bubble_sort", "merge_sort", "quick_sort", "sorted_builtin"]
    results = []

    # Para cada archivo en la carpeta datasets
    for filename in os.listdir(dataset_folder):
        file_path = os.path.join(dataset_folder, filename)
        with open(file_path, 'r') as file:
            data = list(map(int, file.readline().split()))

        # Extraer el tamaño del archivo del nombre
        size = filename.split('_')[-1].replace('.txt', '')
        
        # Extraer el tipo de conjunto de datos del nombre del archivo
        data_type = filename.split('_')[0]

        # Aplicar cada algoritmo de ordenamiento
        for algorithm in algorithms:
            arr_copy = data.copy()
            sorted_arr, elapsed_time = measure_sorting_time(algorithm, arr_copy)
            
            # Guardar el arreglo ordenado
            result_file = f"Result_of_{algorithm}/{filename}"
            save_sorted_array(sorted_arr, result_file)

            # Guardar el tiempo de ejecución
            save_sorting_time(algorithm, size, elapsed_time, filename)
            
            # Guardar resultados en la lista
            results.append({"algorithm": algorithm, "size": size, "data_type": data_type, "time": elapsed_time})
    
    # Crear un DataFrame con los resultados
    df = pd.DataFrame(results)
    
    # Generar gráficos para cada algoritmo
    generate_plots(df)

    print("Resultados Generados! :D")

def generate_plots(df):
    algorithms = df['algorithm'].unique()
    data_types = df['data_type'].unique()

    for algorithm in algorithms:
        plt.figure(figsize=(10, 6))
        
        for data_type in data_types:
            subset = df[(df['algorithm'] == algorithm) & (df['data_type'] == data_type)]
            plt.plot(subset['size'].astype(int), subset['time'], marker='o', label=data_type)
        
        plt.title(f"Tiempos de Ejecución para {algorithm}")
        plt.xlabel("Tamaño del arreglo (10^n)")
        plt.ylabel("Tiempo de ejecución (segundos)")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{algorithm}_times.png")
        plt.show()

# Ejecutar el proceso
process_datasets()