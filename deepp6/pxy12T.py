import sys
from a_star11 import *
from reemplazar import *

from buscarGuardar import *







from xyTarget import *






def mapear_posicion_a_celda(X, Y, tamaño_celda=0.125, num_filas=40, num_columnas=40):
    centro_x = (num_columnas * tamaño_celda) / 2
    centro_y = (num_filas * tamaño_celda) / 2
    columna = int((X + centro_x) // tamaño_celda)
    fila = int((Y + centro_y) // tamaño_celda)
    return (fila, columna) if 0 <= columna < num_columnas and 0 <= fila < num_filas else None

def calcular_xyT(a, b, c, d): 
    return (a, b), (c, d)

def manejar_busqueda(x1, y1, x2, y2, buscar=True, tamaño_celda=0.125, num_filas=40, num_columnas=40):
    
    y1 = -y1
    y2  = -y2
    
    global punto_interseccion,  ruta_ordenada 
    if not (-5 <= x1 <= 5 and -5 <= y1 <= 5 and -5 <= x2 <= 5 and -5 <= y2 <= 5):
        print("Se espera un valor de coordenadas válido en el rango de -5 a 5")
        return None, None
    
    celda1 = mapear_posicion_a_celda(x1, y1, tamaño_celda, num_filas, num_columnas)
    celda2 = mapear_posicion_a_celda(x2, y2, tamaño_celda, num_filas, num_columnas)
        
    if buscar:
        if celda1 and celda2 and celda1 == celda2:
            print("Las coordenadas de inicio y de fin coinciden con la misma celda, el robot llegó a su destino.")
        else:
            print("Buscando las celdas correspondientes...")
            
             
             
             
             
             
            # Cargar el estado de la cuadrícula desde el archivo CSV existente
            estado_celdas = cargar_estado_csv("estado_celdas.csv")





            # Ejemplo de uso de borrar valores específicos
            valores_a_borrar = [1, 2 ,3]  # Valores que deseas borrar (modifica esta lista según tus necesidades)
            borrar_valores(estado_celdas, valores_a_borrar)
            
            agregar_estado(estado_celdas, x1 , y1,1)
            
        
            
            
            
            agregar_estado(estado_celdas, x2, y2,   2)
            


            reemplazar_valor(estado_celdas , 4 ,5)
        
        
        
        
            
            guardar_estado_csv(estado_celdas, "estado_celdas.csv")
            ejecutar_búsqueda()
            
            # Obtener y convertir posiciones de las celdas con valor 1
            posiciones_valor_1 = obtener_posiciones_valores_csv([1], "estado_celdas.csv")
            coordenadas_valor_1 = convertir_a_coordenadas(posiciones_valor_1)

            # Obtener y convertir posiciones de las celdas con valor 2
            posiciones_valor_2 = obtener_posiciones_valores_csv([2], "estado_celdas.csv")
            coordenadas_valor_2 = convertir_a_coordenadas(posiciones_valor_2)

            # Obtener y convertir posiciones de las celdas con valor 3 o 4
            posiciones_valor_3_y_4 = obtener_posiciones_valores_csv([3, 4], "estado_celdas.csv")
            coordenadas_valor_3_y_4 = convertir_a_coordenadas(posiciones_valor_3_y_4)

            # Obtener la ruta ordenada desde el inicio (valor 1) hasta el final (valor 2)
            ruta_ordenada = obtener_ruta_ordenada(coordenadas_valor_1[0], coordenadas_valor_3_y_4, coordenadas_valor_2[0])

            # Definir el radio y el centro del círculo (origen)
            centro_circulo = ruta_ordenada[0]
            radio_circulo = 0.2

            # Encontrar el punto de intersección entre la ruta y el círculo
            punto_interseccion = encontrar_interseccion_circulo_y_ruta(ruta_ordenada, centro_circulo, radio_circulo)

            if punto_interseccion:
                print(f"Coordenadas de la intersección: {punto_interseccion}")
                
                return punto_interseccion
            else:
                print(f"No se encontró intersección. Coordenadas del punto final: {ruta_ordenada[-1]}")
                return ruta_ordenada[-1]
            
            
            
            
        
    else:
        print("No se busca, Agregando La posición de robot al mapa")
        
        # Cargar el estado de la cuadrícula desde el archivo CSV existente
        estado_celdas = cargar_estado_csv("estado_celdas.csv")

        # Ejemplo de uso de borrar valores específicos
        valores_a_borrar = [1, 2]  # Valores que deseas borrar (modifica esta lista según tus necesidades)
        borrar_valores(estado_celdas, valores_a_borrar)
        
        agregar_estado(estado_celdas, x1, y2,  1)
        
        
        
        guardar_estado_csv(estado_celdas, "estado_celdas.csv")

    
    
    
    
    
    
    

    return None, None


if __name__ == "__main__":
    x1, y1 = 0.5, 1.5
    x2, y2 = -1.4, 2.3

    coordenadas1, coordenadas2 = manejar_busqueda(x1, -y1, x2, -y2, buscar=True)
    print("Coordenadas 1:", coordenadas1)
    print("Coordenadas 2:", coordenadas2)

    x1, y1 = 1.0, 1.0
    x2, y2 = 1.6, 1

    coordenadas1, coordenadas2 = manejar_busqueda(x1, y1, x2, y2, buscar=True)
    print("Coordenadas 1:", coordenadas1)
    print("Coordenadas 2:", coordenadas2)
    






    # coordenadas1, coordenadas2 = manejar_busqueda(x1, y1, x2, y2, buscar=False)
    # print("Coordenadas 1:", coordenadas1)
    # print("Coordenadas 2:", coordenadas2)

























