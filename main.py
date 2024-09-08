# main.py

import os
from lexer import lexer
from parser import parse

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def main():
    while True:
        print("\nMenú:")
        print("1. Ejecutar el programa con test.txt")
        print("2. Ingresarlo manualmente")
        print("3. Ejecutar un archivo personalizado")
        print("4. Salir")
        print("5. Ejecutar pruebas con qTest.txt")
        
        option = input("Seleccione una opción (1-4): ")
        
        if option == '1':
            input_code = read_file('test.txt')
        elif option == '2':
            input_code = input("Ingrese el código del robot:\n")
        elif option == '3':
            file_path = input("Ingrese la ruta del archivo personalizado:\n")
            if os.path.isfile(file_path):
                input_code = read_file(file_path)
            else:
                print("Archivo no encontrado.")
                continue
        elif option == '4':
            break
        elif option == '5':
            input_code = read_file('qTest.txt')
        else:
            print("Opción no válida.")
            continue
        
        tokens = lexer(input_code)
        
        print("\n¿Desea ver el resultado solo (1) o también el input tokenizado (2)?")
        view_option = input("Seleccione una opción (1-2): ")
        
        if view_option == '1':
            print("\nResultado del análisis:", parse(tokens))
        elif view_option == '2':
            print("\nTokens generados:")
            print(tokens)
            print("\nResultado del análisis:", parse(tokens))
        else:
            print("Opción no válida.")
            continue

if __name__ == "__main__":
    main()
