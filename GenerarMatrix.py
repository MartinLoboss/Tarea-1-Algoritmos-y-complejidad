import numpy as np
import os

# Función para generar una matriz cuadrada
def generate_square_matrix(size):
    """Genera una matriz cuadrada de tamaño `size` x `size` con valores aleatorios entre 0 y 100."""
    return np.random.randint(0, 101, (size, size))

# Función para generar una matriz rectangular
def generate_rectangular_matrix(rows, cols):
    """Genera una matriz rectangular de tamaño `rows` x `cols` con valores aleatorios entre 0 y 100."""
    return np.random.randint(0, 101, (rows, cols))

# Función para guardar matrices en archivos de texto
def save_matrix_to_file(matrix, filename):
    """Guarda una matriz en un archivo de texto."""
    np.savetxt(filename, matrix, fmt='%d', delimiter=' ')

# Función para generar datasets de multiplicación de matrices
def generate_matrix_datasets():
    """Genera 5 datasets de matrices cuadradas y no cuadradas para diferentes tamaños."""
    sizes = [10**i for i in range(1, 4)]  # Vamos de 10^1 hasta 10^3 por practicidad (ajusta según necesidad)
    
    # Crear carpeta para guardar los datasets si no existe
    if not os.path.exists("matrix_datasets"):
        os.makedirs("matrix_datasets")

    for size in sizes:
        # Generar matrices cuadradas de tamaño size x size
        square_matrix_1 = generate_square_matrix(size)
        square_matrix_2 = generate_square_matrix(size)
        # Generar matrices rectangulares de diferentes dimensiones
        rectangular_matrix_1 = generate_rectangular_matrix(size, size + 20)
        rectangular_matrix_2 = generate_rectangular_matrix(size + 20, size)
        

        # Guardar las matrices cuadradas en archivos
        save_matrix_to_file(square_matrix_1, f'matrix_datasets/square_matrix_1_{size}x{size}.txt')
        save_matrix_to_file(square_matrix_2, f'matrix_datasets/square_matrix_2_{size}x{size}.txt')

        # Guardar las matrices rectangulares en archivos
        save_matrix_to_file(rectangular_matrix_1, f'matrix_datasets/rectangular_matrix_1_{size}x{size+20}.txt')
        save_matrix_to_file(rectangular_matrix_2, f'matrix_datasets/rectangular_matrix_2_{size+20}x{size}.txt')

# Ejecutar la generación de datasets
generate_matrix_datasets()
print("Datasets de matrices generados!")
