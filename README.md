# Omega Invasion 🛸

Un videojuego arcade espacial 2D desarrollado en **Python** con **Pygame Community Edition (pygame-ce)** y gestionado con **Poetry**.

El proyecto fue desarrollado para la asignatura de Fundamentos de Data Science de la Universidad Tecnológica Metropolitana (UTEM).

---

## Requisitos

- **Python**: `>= 3.12`
- **Poetry**: Para gestión de dependencias y entorno virtual

---

## 🚀 Instalación

1. Clona el repositorio y accede a la carpeta:
   ```bash
   git clone git@github.com:Naicriz/omega_invasion.git
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

### Controles

| Acción | Teclas |
|---|---|
| **Movimiento** | `W`, `A`, `S`, `D` o Flechas de dirección |
| **Disparo continuo** | `Barra Espaciadora` (mantener presionada) |
| **Seleccionar mejora** | Teclas `1`, `2`, `3` o Clic izquierdo sobre la carta |
| **Reiniciar partida** | `Enter`, `R` o Clic en "Reiniciar" (al morir) |
| **Salir del juego** | `ESC` o `Q` en pantalla de Game Over |

---

## Pruebas Automatizadas (Tests)

El proyecto cuenta con pruebas con la libreria **pytest** ejecutadas en modo *headless* (sin abrir ventanas):

```bash
# Ejecutar todas las pruebas
poetry run pytest

# Ejecutar con salida detallada
poetry run pytest -v
```

---

## Autor

- **Ian Salazar** ([isalazar@utem.cl](mailto:[salazar@utem.cl]))
