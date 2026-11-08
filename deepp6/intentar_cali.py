
import math

def calcular_lado(d7, d8, t16):
    lado = math.sqrt(d8**2 + d7**2 - 2 * d8 * d7 * math.cos(t16))
    return lado

def calcular_angulo_lado(d3, d9, d7):
    cos_C = (d3**2 + d9**2 - d7**2) / (2 * d3 * d9)
    cos_C = max(-1, min(1, cos_C))
    C = math.acos(cos_C)
    return C

def calcular_transformacion(t9, t6, t10, t15, a1, a2, a3, a4):
    transformation_matrix = [
        [math.cos(t9 - t6 + t10 + t15),  -math.sin(t9 - t6 + t10 + t15), 0, a1 + a4 * math.cos(t9 - t6 + t15) + a3 * math.cos(t9 + t15) + a2 * math.cos(t15)],
        [math.sin(t9 - t6 + t10 + t15), math.cos(t9 - t6 + t10 + t15), 0, a4 * math.sin(t9 - t6 + t15) + a3 * math.sin(t9 + t15) + a2 * math.sin(t15)],
        [0, 0, 1.0, 0],
        [0, 0, 0, 1.0]
    ]
    
    coordenada_X = transformation_matrix[0][3]
    coordenada_Y = transformation_matrix[1][3]
    angulo_Z = math.atan2(transformation_matrix[1][0], transformation_matrix[0][0])
    angulo_Z_grados = math.degrees(angulo_Z)
    
    return coordenada_X, coordenada_Y, angulo_Z_grados



def realizar_calculos(a9=None, a7=None, a5=None, a8=None, a1=None, a2=None, a3=None, t7=None):
     # Verificar si los parámetros forman un triángulo válido
    if not (a9 + a7 > a3 and a9 + a3 > a7 and a7 + a3 > a9):
        print("Error: Los lados proporcionados no cumplen la propiedad del triángulo (la suma de dos lados debe ser mayor que el tercer lado).")
        return None, None, None
    
    # Verificar si faltan parámetros clave
    if None not in (a9, a7, a5, a8, t7):
        
        
        
    
        # Caso con todos los parámetros proporcionados
        t7_radianes = math.radians(t7)

        t3 = calcular_angulo_lado(a3, a9, a7)
        t1 = calcular_angulo_lado(a7, a3, a9)
        t17 = calcular_angulo_lado(a8, a7, a5)

        t16 = t17 - (math.radians(180) - (t3 + t1))
        #t50 =   calcular_angulo_lado(a3, a4 , a5)
        a4 = calcular_lado(a9, a8, t16)
        
        #a4 = math.radians( 180)        -   t50   
    
    
        t2 = calcular_angulo_lado(a9, a4, a8)

        t15 = math.radians(90)
        
        # if t2 >= math.radians(180):
        #     t6 = t2 - math.radians(180)

        t6 = -(t2 + t3) + math.radians(180)
        t6 = -(-t2 + t3) + math.radians(180)

        t9 = t1

        t10 = -((-t7_radianes) + math.radians(180) + math.radians(90))
                # Impresiones para este caso
        print("Caso con todos los parámetros:")
        print(f"t3: {t3}, t1: {t1}, t17: {t17}, t16: {t16}, a4: {a4}, t2: {t2}")
        print(f"t6: {t6}, t9: {t9}, t10: {t10}")


    else:
        # Caso con parámetros faltantes o valores predeterminados
        t7_radianes = math.radians(t7)
        t1 = calcular_angulo_lado(a7, a3, a9)

        a4 = 2.3185  # Valor fij
        a4 = 0.20442186127410336
        
        
        

        t15 = math.radians(90)

        t6 = 0.5372  # Valor fijo
        
        t6 = 2.9809020006378812
        t9 = t1

        t10 = -((-t7_radianes) + math.radians(180) + math.radians(90))
        
        
        
        
        
         # Impresiones para este caso
        print("Caso con valores predeterminados:")
        print(f"t1: {t1}, a4: {a4}, t6: {t6}, t9: {t9}, t10: {t10}")

    # Transformación final
    coordenada_X, coordenada_Y, angulo_Z_grados = calcular_transformacion(t9, t6, t10, t15, a1, a2, a3, a4)

    return coordenada_X, coordenada_Y, angulo_Z_grados





if __name__ == "__main__":
    # Ejemplo de uso con los parámetros
    a9 = 3
    a7 = 2.8
    a5 = 5.4
    a8 = 4
    a1, a2, a3 = 3.3, 3, 3.3
    t7 = 20

    coordenada_X, coordenada_Y, angulo_Z_grados = realizar_calculos(a9, a7, a5, a8, a1, a2, a3, t7)

    print("\nResultado final:")
    print(f"Coordenada X: {coordenada_X}")
    print(f"Coordenada Y: {coordenada_Y}")
    print(f"Ángulo en Z: {angulo_Z_grados}")



    # Ejemplo de uso con los parámetros
    a9 = 3
    a7 = 2.8
    a3 = 3.3


    coordenada_X, coordenada_Y,angulo_Z_grados = realizar_calculos(a9 = a9, a7 = a7,  a3 = a3, t7 = 20  , a1 = 3.3, a2 = 3, )

    print("\nResultado final:")
    print(f"Coordenada X: {coordenada_X}")
    print(f"Coordenada Y: {coordenada_Y}")
    print(f"Ángulo en Z: {angulo_Z_grados}")

    a9 =.5
    
    a7 = .16
    a5 = .3
    a8 =.3
    a1, a2, a3 = .6, .05, .5
    t7 = 0
    # a9 = 3
    # a7 = 2.8
    # a5 = 3
    # a8 = 3
    # a1, a2, a3 = 3.3, 3, 3
    # t7 = 0
    coordenada_X, coordenada_Y, angulo_Z_grados = realizar_calculos(a7 = a7 , a3 = a3 , a9 = a9 , t7 = 0, a1 = a1 , a2 = a2)

    print("\nResultado final:")
    print(f"Coordenada X: {coordenada_X}")
    print(f"Coordenada Y: {coordenada_Y}")
    print(f"Ángulo en Z: {angulo_Z_grados}")

    a9 =.5
    
    a7 = .16
    a5 = .3
    a8 =.3
    a1, a2, a3 = .6, .05, .5
    t7 = 0
    # a9 = 3
    # a7 = 2.8
    # a5 = 3
    # a8 = 3
    # a1, a2, a3 = 3.3, 3, 3
    # t7 = 0
    coordenada_X, coordenada_Y, angulo_Z_grados = realizar_calculos(a9, a7, a5, a8, a1, a2, a3, t7)

    print("\nResultado final:")
    print(f"Coordenada X: {coordenada_X}")
    print(f"Coordenada Y: {coordenada_Y}")
    print(f"Ángulo en Z: {angulo_Z_grados}")