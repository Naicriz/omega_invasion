# Omega Invasion

Un videojuego arcade 2D desarrollado en **Python** con **Pygame** y gestionado con **Poetry**.

Proyecto desarrollado para la asignatura de Fundamentos de Data Science de la **Universidad Tecnológica Metropolitana (UTEM)**.

---
<img width="912" height="944" alt="Gameplay" src="https://github.com/user-attachments/assets/bf480d4a-0015-41e1-9f5b-b81c4e4a0d57" />
<img width="912" height="944" alt="GameOver" src="https://github.com/user-attachments/assets/be2d4654-1156-4538-9120-f9d99eb52cb1" />
<img width="912" height="944" alt="UpgradeMenu" src="https://github.com/user-attachments/assets/9ceedae8-af2c-4e61-b721-f8e28db5b85e" />

---

## Requisitos

- **Python**: `>= 3.12`
- **Poetry**: Para gestión de dependencias y entorno virtual

---

## Instalación

1. Clona el repositorio y accede a la carpeta:
   ```bash
   git clone https://github.com/Naicriz/omega_invasion.git
   cd omega_invasion
   ```

2. Instala las dependencias:
   ```bash
   poetry install
   ```

---

## Cómo Jugar

Inicia el juego ejecutando:

```bash
poetry run omega-invasion
```

*(También puedes iniciar con: `poetry run python -m omega_invasion.main`)*

En caso contrario, puedes crear tu propio entorno virtual con pip, instalar las dependencias (`requirements.txt`) e iniciar directamente el archivo `main.py`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m omega_invasion.main
```

### Controles

| Acción | Teclas |
|---|---|
| **Movimiento** | `W`, `A`, `S`, `D` o Flechas de dirección |
| **Disparo continuo** | `Barra Espaciadora` (mantener presionada) |
| **Seleccionar mejora** | Teclas `1`, `2`, `3` o Clic izquierdo sobre la carta |
| **Reiniciar partida** | `Enter`, `R` o Clic en "Reiniciar" (al morir) |
| **Salir del juego** | `ESC` o `Q` en pantalla de Game Over |

---

## Matemáticas Implementadas

Para la asignatura **Fundamentos de Data Science** de la Universidad Tecnológica Metropolitana (UTEM) investigué los algoritmos y estudié sobre ellos, por lo que se creó el módulo `utils/matematica.py` que implementa las siguientes funciones **sin usar `import math`**, reemplazando todas las llamadas de la librería estándar en el proyecto:

| Función | Algoritmo | Uso en el juego |
|---|---|---|
| `seno(x)` | Serie de Taylor (7 términos) | Movimiento en zigzag de los drones, escudo visual, explosiones |
| `coseno(x)` | Serie de Taylor (7 términos) | Inclinación de naves, dirección de partículas de explosión |
| `tangente(x)` | Identidad `sin(x) / cos(x)` | — |
| `raiz(n)` | Método iterativo de Newton-Raphson | Base para `hipotenusa` |
| `hipotenusa(a, b)` | Teorema de Pitágoras con `raiz()` propia | Distancia en el escudo visual del jugador |
| `atan(x)` | Serie de Maclaurin (15 términos) | Base para `atan2` |
| `atan2(y, x)` | Lógica de cuadrantes con `atan()` propia | Rotación de sprites de balas hacia su dirección de vuelo |
| `radianes_a_grados(r)` | Conversión directa con `PI` propio | Ángulo de rotación de sprites |

### Algoritmos destacados

**Serie de Taylor para `seno`** — cada término se obtiene multiplicando el anterior por el ratio `(-x²) / ((i+1)(i+2))`, evitando recalcular potencias y factoriales desde cero. El ángulo se normaliza al rango `[-π, π]` antes de calcular para mantener precisión numérica.

**Newton-Raphson para `raiz`** — iteración `x_siguiente = (x + n/x) / 2` con convergencia cuadrática (cada iteración duplica los decimales correctos). Converge en ~4 iteraciones con error < 1e-10.

**Serie de Maclaurin para `atan`** — denominadores de enteros impares (`1, 3, 5...`) en lugar de factoriales. El ratio entre términos es `(-x²) * i / (i+2)`. Se aplica la identidad `atan(x) = π/2 - atan(1/x)` para valores fuera del rango de convergencia `|x| > 1`.

---

## Estructura del proyecto

```
src/omega_invasion/
├── main.py                  # Punto de entrada
├── game.py                  # Bucle principal y lógica de juego
├── settings.py              # Constantes globales
├── entities/
│   ├── base.py              # Clase base NaveBase
│   ├── player.py            # Jugador, propulsor y escudo visual
│   ├── enemy.py             # Dron, Cazador y Nodriza enemigos
│   ├── bullet.py            # Proyectiles (Bala y BolaEnergia)
│   ├── effects.py           # Partículas y explosiones
│   └── upgrades.py          # Catálogo de mejoras
├── scenes/
│   ├── upgrade_menu.py      # Menú de selección de mejoras
│   └── game_over_menu.py    # Pantalla de fin de partida
└── utils/
    ├── constants.py         # Constantes matemáticas (PI, TAU)
    ├── matematica.py        # Funciones matemáticas propias (sin import math)
    ├── vector2d.py          # Clase Vector2D propia (pendiente)
    ├── assets.py            # Carga de sprites, fuentes y audio
    └── background.py        # Fondo estelar con paralaje
```

---

## Pruebas Automatizadas (Tests)

El proyecto cuenta con pruebas con la librería **pytest** ejecutadas en modo *headless*:

```bash
# Ejecutar todas las pruebas
poetry run pytest

# Ejecutar con salida detallada
poetry run pytest -v
```

---

## Autor

- **Ian Salazar** ([isalazar@utem.cl](mailto:[salazar@utem.cl]))
