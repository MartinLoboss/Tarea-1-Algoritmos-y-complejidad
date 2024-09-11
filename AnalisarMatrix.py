import numpy as np
import os
import time
import math

# Algoritmo cúbico tradicional para la multiplicación de matrices
def traditional_multiplication(A, B):
    """Algoritmo iterativo cúbico tradicional para multiplicación de matrices."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return C

# Algoritmo cúbico optimizado transponiendo la segunda matriz
def optimized_multiplication(A, B):
    """Algoritmo iterativo cúbico optimizado para la localidad de datos (transponiendo la segunda matriz)."""
    n = len(A)
    B_transpose = list(zip(*B))  # Transponemos la matriz B
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B_transpose[j][k] for k in range(n))
    return C

# Algoritmo de Strassen para multiplicación de matrices con umbral
def strassen_multiplication(A, B, threshold=64):
    """Algoritmo de Strassen con umbral para el tamaño mínimo de recursión."""
    n = len(A)
    
    # Si el tamaño de la matriz es menor o igual al umbral, usar el algoritmo cúbico tradicional
    if n <= threshold:
        return traditional_multiplication(A, B)
    
    # Continuar con Strassen si el tamaño de la matriz es mayor que el umbral
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    else:
        mid = n // 2
        A11, A12, A21, A22 = partition_matrix(A, mid)
        B11, B12, B21, B22 = partition_matrix(B, mid)

        M1 = strassen_multiplication(add_matrices(A11, A22), add_matrices(B11, B22), threshold)
        M2 = strassen_multiplication(add_matrices(A21, A22), B11, threshold)
        M3 = strassen_multiplication(A11, subtract_matrices(B12, B22), threshold)
        M4 = strassen_multiplication(A22, subtract_matrices(B21, B11), threshold)
        M5 = strassen_multiplication(add_matrices(A11, A12), B22, threshold)
        M6 = strassen_multiplication(subtract_matrices(A21, A11), add_matrices(B11, B12), threshold)
        M7 = strassen_multiplication(subtract_matrices(A12, A22), add_matrices(B21, B22), threshold)

        C11 = add_matrices(subtract_matrices(add_matrices(M1, M4), M5), M7)
        C12 = add_matrices(M3, M5)
        C21 = add_matrices(M2, M4)
        C22 = add_matrices(subtract_matrices(add_matrices(M1, M3), M2), M6)

        return combine_matrices(C11, C12, C21, C22)

# Funciones auxiliares para el algoritmo de Strassen
def add_matrices(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A))] for i in range(len(A))]

def subtract_matrices(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]

def partition_matrix(A, mid):
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    return A11, A12, A21, A22

def combine_matrices(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom

# Función para medir el tiempo de los algoritmos
def measure_multiplication_time(algorithm, A, B):
    A_padded, B_padded = pad_matrices(A, B)  # Asegura que las matrices sean de tamaño potencia de 2
    start_time = time.time()
    if algorithm == "traditional":
        C = traditional_multiplication(A_padded, B_padded)
    elif algorithm == "optimized":
        C = optimized_multiplication(A_padded, B_padded)
    elif algorithm == "strassen":
        C = strassen_multiplication(A_padded, B_padded, threshold=64)  # Se añade el umbral
    end_time = time.time()
    elapsed_time = end_time - start_time
    return C, elapsed_time

# Función para cargar matrices desde archivos de texto
def load_matrix_from_file(filename):
    return np.loadtxt(filename, dtype=int).tolist()

# Función para guardar la matriz resultante
def save_matrix_to_file(matrix, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    np.savetxt(filename, matrix, fmt='%d', delimiter=' ')

# Función para guardar el tiempo de análisis
# Función para guardar el tiempo de análisis
def save_multiplication_time(algorithm_name, size, elapsed_time):
    folder_name = f"Result_of_{algorithm_name}"
    os.makedirs(folder_name, exist_ok=True)
    time_file = os.path.join(folder_name, f"ResultadoAnalisisTiempo_{size}.txt")
    with open(time_file, 'w') as f:
        f.write(f"Tiempo para multiplicar matrices de tamaño {size}: {elapsed_time} segundos\n")

# Función para procesar todos los archivos y aplicar los algoritmos
def process_matrix_datasets():
    dataset_folder = "matrix_datasets"
    algorithms = ["traditional", "optimized", "strassen"]

    for filename in os.listdir(dataset_folder):
        # Procesar matrices cuadradas
        if 'square_matrix_1' in filename:
            file_size = filename.split('_')[-1].replace('.txt', '')
            file_path_A = os.path.join(dataset_folder, filename)
            file_path_B = os.path.join(dataset_folder, f'square_matrix_2_{file_size}.txt')

            A = load_matrix_from_file(file_path_A)
            B = load_matrix_from_file(file_path_B)

            # Aplicar cada algoritmo de multiplicación de matrices
            for algorithm in algorithms:
                C, elapsed_time = measure_multiplication_time(algorithm, A, B)

                # Guardar la matriz resultante
                result_file = f"Result_of_{algorithm}/matrix_result_{file_size}.txt"
                save_matrix_to_file(C, result_file)

                # Guardar el tiempo de ejecución
                save_multiplication_time(algorithm, file_size, elapsed_time)

        # Procesar matrices rectangulares
        elif 'rectangular_matrix_1' in filename:
            # Extraer el tamaño de la matriz rectangular desde el nombre del archivo
            size_parts = filename.split('_')[-1].replace('.txt', '').split('x')
            num_rows_A = int(size_parts[0])  # Número de filas de A
            num_cols_A = int(size_parts[1])  # Número de columnas de A

            # Crear el nombre del archivo para la segunda matriz rectangular
            file_path_A = os.path.join(dataset_folder, filename)
            file_path_B = os.path.join(dataset_folder, f'rectangular_matrix_2_{num_cols_A}x{num_rows_A}.txt')

            # Comprobar si el archivo B existe
            if os.path.exists(file_path_B):
                # Cargar las matrices A y B
                A = load_matrix_from_file(file_path_A)
                B = load_matrix_from_file(file_path_B)

                # Aplicar cada algoritmo de multiplicación de matrices
                for algorithm in algorithms:
                    C, elapsed_time = measure_multiplication_time(algorithm, A, B)

                    # Guardar la matriz resultante
                    result_file = f"Result_of_{algorithm}/rectangular_matrix_result_{num_rows_A}x{num_cols_A}.txt"
                    save_matrix_to_file(C, result_file)

                    # Guardar el tiempo de ejecución
                    save_multiplication_time(algorithm, f"{num_rows_A}x{num_cols_A}", elapsed_time)
            else:
                print(f"Archivo {file_path_B} no encontrado. No se puede realizar la multiplicación.")
# Función para rellenar matrices si el tamaño no es potencia de 2
def pad_matrices(A, B):
    n = len(A)
    m = 2**math.ceil(math.log2(n))  # Encuentra el tamaño más cercano que es potencia de 2
    if n == m:
        return A, B  # Si ya es potencia de 2, no se hace nada

    # Rellenar matrices con ceros
    A_padded = [[A[i][j] if i < n and j < n else 0 for j in range(m)] for i in range(m)]
    B_padded = [[B[i][j] if i < n and j < n else 0 for j in range(m)] for i in range(m)]
    return A_padded, B_padded

# Ejecutar el proceso de análisis de matrices
process_matrix_datasets()
print("Análisis de matrices completado!")
