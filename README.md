# Omega Invasion 🛸

Un videojuego arcade espacial 2D desarrollado en **Python** utilizando **Pygame Community Edition (pygame-ce)** y gestionado con **Poetry**.

---

## 📋 Requisitos Previos

- **Python**: `>= 3.12` (compatible con 3.14)
- **Poetry**: Para gestión de dependencias y entornos virtuales.

---

## 🚀 Instalación y Configuración

1. **Clonar el repositorio o ingresar al directorio del proyecto**:
   ```bash
   cd omega_invasion
   ```

2. **Instalar dependencias del proyecto**:
   ```bash
   poetry install
   ```

---

## 🎮 Ejecución del Juego

Puedes iniciar el juego directamente mediante el comando registrado en Poetry:

```bash
poetry run omega-invasion
```

O también ejecutando el módulo principal de Python:

```bash
poetry run python -m omega_invasion.main
```

### Controles Básicos (Por defecto)
- **ESC**: Salir del juego / cerrar ventana.

---

## 🧪 Pruebas Automatizadas (Testing)

El proyecto utiliza **pytest** configurado en modo *headless* (sin abrir ventanas físicas), lo que permite ejecutar pruebas ultrarrápidas y aptas para entornos de integración continua (CI).

### Comandos de prueba

```bash
# Ejecutar toda la suite de pruebas
poetry run pytest

# Ejecutar en modo detallado (verbose)
poetry run pytest -v

# Ejecutar un archivo de prueba específico
poetry run pytest tests/test_ajustes.py
```

### Ejemplo para nuevas pruebas de entidades

Al crear nuevas entidades (por ejemplo `src/omega_invasion/entities/jugador.py`), puedes agregar pruebas de lógica en `tests/`:

```python
# tests/test_jugador.py
def test_jugador_no_puede_salir_del_borde_izquierdo():
    jugador = Jugador(x=0, y=500)
    jugador.mover_izquierda()
    assert jugador.rect.x >= 0
```

---

## 📂 Estructura del Proyecto

El código sigue el estándar de empaquetado moderno **`src-layout`**:

```text
omega_invasion/
├── assets/                       # Recursos multimedia (imágenes, sonidos, fuentes)
│   ├── fonts/
│   ├── images/
│   └── sounds/
├── src/
│   └── omega_invasion/           # Paquete principal del juego
│       ├── __init__.py
│       ├── main.py               # Punto de entrada (función principal)
│       ├── settings.py           # Constantes y configuración global
│       ├── game.py               # Clase 'Juego' (loop principal, eventos, render)
│       ├── entities/             # Clases del juego (jugador, enemigos, balas)
│       ├── scenes/               # Escenas o estados (menú, juego, fin)
│       └── utils/                # Funciones auxiliares y cargadores de recursos
├── tests/                        # Suite de pruebas unitarias
│   ├── conftest.py               # Configuración headless de Pygame para pytest
│   ├── test_ajustes.py           # Pruebas de configuración
│   └── test_juego.py             # Pruebas del ciclo de juego
├── pyproject.toml                # Definición de dependencias y scripts con Poetry
└── README.md
```

---

## 👤 Autor

- **Ian Salazar** ([isalazarjara@gmail.com](mailto:isalazarjara@gmail.com))
