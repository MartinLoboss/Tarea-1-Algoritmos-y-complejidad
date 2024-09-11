import numpy as np
import random
import os
import time

    

###########################################################
################CREACION DE LOS DATASETS###################
###########################################################

def generate_random_array(size):
    """Genera un array completamente aleatorio de tamaño `size`."""
    return np.random.randint(0, 101, size).tolist()

def generate_semi_ordered_array(size):
    """Genera un array semi ordenado con mitad ordenada y mitad aleatoria."""
    array = generate_random_array(size)
    midpoint = size // 2
    array[:midpoint] = sorted(array[:midpoint])
    return array

def generate_partially_ordered_array(size):
    """Genera un array parcialmente ordenado donde el 75% está ordenado."""
    array = generate_random_array(size)
    three_quarters = (3 * size) // 4
    array[:three_quarters] = sorted(array[:three_quarters])
    return array

def generate_reverse_ordered_array(size):
    """Genera un array completamente ordenado en orden decreciente."""
    array = sorted(generate_random_array(size), reverse=True)
    return array

def generate_sorted_array(size):
    """Genera un array completamente ordenado de menor a mayor."""
    return sorted(generate_random_array(size))

def save_array_to_file(array, filename):
    """Guarda un array en un archivo de texto."""
    with open(filename, 'w') as f:
        f.write(' '.join(map(str, array)) + '\n')

def generate_datasets():
    """Genera 5 datasets por nivel de tamaño desde 10^1 hasta 10^5."""
    sizes = [10**i for i in range(1, 6)]  # 10^1 hasta 10^5
    
    # Crear carpeta para guardar los datasets si no existe
    if not os.path.exists("datasets_a"):
        os.makedirs("datasets_a")

    for size in sizes:
        # Generar los 5 tipos de arrays
        random_array = generate_random_array(size)
        semi_ordered_array = generate_semi_ordered_array(size)
        partially_ordered_array = generate_partially_ordered_array(size)
        reverse_ordered_array = generate_reverse_ordered_array(size)
        sorted_array = generate_sorted_array(size)
        
        # Guardar los arrays en archivos de texto
        save_array_to_file(random_array, f'datasets_a/random_{size}.txt')
        save_array_to_file(semi_ordered_array, f'datasets_a/semi_ordered_{size}.txt')
        save_array_to_file(partially_ordered_array, f'datasets_a/partially_ordered_{size}.txt')
        save_array_to_file(reverse_ordered_array, f'datasets_a/reverse_ordered_{size}.txt')
        save_array_to_file(sorted_array, f'datasets_a/sorted_{size}.txt')

# Ejecutar la generación de datasets
generate_datasets()
print("Datasets Generados!")