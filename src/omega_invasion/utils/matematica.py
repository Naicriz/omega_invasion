from omega_invasion.utils.constants import TAU, PI

def normalizar_angulo(angulo: float) -> float:
    angulo = angulo % TAU
    if angulo > PI:
        angulo -= TAU
    return angulo

# La función acepta un argumento opcional llamado terminos. 
# Si no se especifica, se calcularán 7 términos.
#
# Esto permite que la función sea más flexible y se pueda ajustar la precisión del cálculo.
# Pero para el juego es suficiente con 7 términos.

def seno_taylor(x: float, terminos=7) -> float:
    """
    Calcula el seno de x (en radianes) usando la Serie de Taylor.
    
    Fórmula: sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + x⁹/9! - x¹¹/11! + x¹³/13!
    """
    # Paso 1: normalizar x al rango [-π, π] para mantener precisión
    x = normalizar_angulo(x)

    # Cualquier número elevado a la 1 es el mismo número y cualquier número factorial de 1 es 1.
    termino: float = x # Primer termino: xˆ1/1!
    termino_cuadrado: float = x ** 2
    resultado: float = 0.0

    # Paso 2: sumar los 7 términos de la serie
    # Pista: Cada término es ±(x^potencia / factorial)
    for i in range(1, terminos * 2, 2):
        resultado += termino
        
        # El signo negativo en -termino hace que los términos se alternen
        # En lugar de calcular (n!) a partir de 1, usamos el término anterior
        # (i + 1) * (i + 2) = (n - 1) * (n - 1 + 2) = n * (n + 1)
        termino = -termino * termino_cuadrado / ((i + 1) * (i + 2)) # Siguiente termino
        
    return resultado

def seno(x: float) -> float:
    """
    Se podria calcular el seno de x (en radianes) usando la identidad trigonométrica sin(x) = cos(x - PI/2).
    Pero es mejor usar la Serie de Taylor.
    """
    return seno_taylor(x)

def coseno_taylor(x: float, terminos: int = 7) -> float:
    """
    Calcula el coseno de x (en radianes) usando la Serie de Taylor.
    
    Fórmula: cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + x⁸/8! - x¹⁰/10! + x¹²/12!
    """
    # Paso 1: normalizar x al rango [-π, π] para mantener precisión
    x = normalizar_angulo(x)

    # Cualquier número elevado a la 0 es 1 y cualquier número factorial de 0 es 1.
    termino: float = 1.0 # Primer termino: xˆ0/0!
    termino_cuadrado: float = x ** 2
    resultado: float = 0.0

    # Paso 2: sumar los 7 términos de la serie
    for i in range(0, terminos * 2, 2):
        resultado += termino
        
        # Siguiente termino
        termino = -termino * termino_cuadrado / ((i + 1) * (i + 2))
        
    return resultado

def coseno(x: float) -> float:
    """
    Se podria calcular el coseno de x (en radianes) usando la identidad trigonométrica cos(x) = sin(x + PI/2).
    Pero es mejor usar la Serie de Taylor.
    """
    return coseno_taylor(x)

def tangente(x: float) -> float:
    """
    Calcula la tangente de x (en radianes) usando la identidad trigonométrica tan(x) = sin(x) / cos(x).
    """
    # Para que la tangente no sea indefinida, el coseno debe ser diferente de cero.
    cos_x: float = coseno(x)
    if cos_x == 0:
        raise ValueError("El coseno de x es cero, la tangente no está definida.")
    
    return seno(x) / cos_x

def raiz(n: float) -> float:
    """
    Calcula la raíz cuadrada de n usando el método iterativo de Newton-Raphson.
    
    Fórmula de iteración: x_siguiente = (x_actual + n / x_actual) / 2
    Se detiene cuando la diferencia entre iteraciones es menor a 0.0001.
    """
    # Casos especiales
    if n < 0:
        raise ValueError("No existe raíz cuadrada de un número negativo")
    if n == 0:
        return 0.0
    
    # Punto de partida: n/2
    x_actual: float = n / 2
    
    # Iterar hasta converger
    while True:
        x_siguiente = (x_actual + (n / x_actual)) / 2
        if abs(x_siguiente - x_actual) < 0.0001:
            return x_siguiente
        x_actual = x_siguiente

def hipotenusa(a: float, b: float) -> float:
    """
    Calcula la hipotenusa de un triángulo rectángulo usando el Teorema de Pitágoras.
    
    Fórmula: c = √(a² + b²)
    """
    return raiz(a**2 + b**2)

def atan(x: float, terminos: int = 15) -> float: # Los terminos estan en 15, ya que converge mas lento que la del seno y coseno
    """
    Calcula la arcotangente usando la serie de Maclaurin.
    atan(x) = x - x³/3 + x⁵/5 - x⁷/7 + ...
    
    Solo converge bien para |x| <= 1.
    Para |x| > 1 usar la identidad: atan(x) = PI/2 - atan(1/x)
    """
    # Caso especial: atan(1) = π/4 (la serie de Leibniz converge muy lento en x=±1)
    if x == 1.0:
        return PI / 4
    if x == -1.0:
        return -PI / 4

    if x > 1:
        return (PI/2) - atan(1/x)
    if x < -1:
        return (-PI/2) - atan(1/x)
    
    termino: float = x # Primer termino: xˆ1/1
    termino_cuadrado: float = x ** 2
    resultado: float = 0.0

    for i in range(1, terminos * 2, 2):
        resultado += termino
        termino = -termino * termino_cuadrado * i / (i + 2) # solo divide por i+2
    return resultado

def atan2(y: float, x: float) -> float:
    """
    Calcula el ángulo en radianes del vector (x, y) en los cuatro cuadrantes.
    Equivalente a math.atan2(y, x).
    """
    if x > 0:
        return atan(y / x)
    if x < 0:
        if y >= 0:
            return atan(y / x) + PI
        else:
            return atan(y / x) - PI
    if y > 0:
        return PI / 2
    if y < 0:
        return -PI / 2
    return 0.0

def radianes_a_grados(rad: float) -> float:
    """Convierte radianes a grados. 180° = π radianes."""
    return rad * (180 / PI)

if __name__ == "__main__":
    import math
    # Comparar con la función seno incorporada de Python
    print(f"---------- seno ----------")
    print(f"PI/2 * 1.5 es {PI * 1.5}")
    print(f"Seno de PI/2 * 1.5 es {seno(PI/2 * 1.5)}")
    print(f"Seno incorporado de Python de PI/2 * 1.5 es {math.sin(PI/2 * 1.5)}")
    # Comparar con la función coseno incorporada de Python
    print(f"---------- coseno ----------")
    print(f"PI/2 * 1.5 es {PI * 1.5}")
    print(f"Coseno de PI/2 * 1.5 es {coseno(PI/2 * 1.5)}")
    print(f"Coseno incorporado de Python de PI/2 * 1.5 es {math.cos(PI/2 * 1.5)}")
    # Comparar con la función tangente incorporada de Python
    print(f"---------- tangente ----------")
    print(f"PI/2 * 1.5 es {PI * 1.5}")
    print(f"Tangente de PI/2 * 1.5 es {tangente(PI/2 * 1.5)}")
    print(f"Tangente incorporada de Python de PI/2 * 1.5 es {math.tan(PI/2 * 1.5)}")
    # Comparar con la función raíz incorporada de Python
    print(f"---------- raíz ----------")
    print(f"9 es {9}")
    print(f"Raíz de 9 es {raiz(9)}")
    print(f"Raíz incorporada de Python de 9 es {math.sqrt(9)}")
    # Comparar con la función atan2 incorporada de Python
    print(f"---------- atan2 ----------")
    print(f"atan2(1, 0) es {atan2(1, 0)} esperado {PI/2}")
    print(f"atan2(0, 1) es {atan2(0, 1)} esperado {0}")
    print(f"atan2(-1, 0) es {atan2(-1, 0)} esperado {-PI/2}")
    print(f"atan2(1, -1) es {atan2(1, -1)} esperado {math.atan2(1,-1)}")