# Omega Invasion 🛸

Un videojuego arcade espacial 2D desarrollado en **Python** con **Pygame Community Edition (pygame-ce)** y gestionado con **Poetry**.

El proyecto fue desarrollado para la asignatura de Fundamentos de Data Science de la Universidad Tecnológica Metropolitana (UTEM).

---
<img width="912" height="944" alt="Captura de pantalla 2026-09-08 a la(s) 12 52 19 a m" src="https://github.com/user-attachments/assets/bf480d4a-0015-41e1-9f5b-b81c4e4a0d57" />
<img width="912" height="944" alt="Captura de pantalla 2026-09-08 a la(s) 12 49 47 a m" src="https://github.com/user-attachments/assets/be2d4654-1156-4538-9120-f9d99eb52cb1" />
<img width="912" height="944" alt="Captura de pantalla 2026-09-08 a la(s) 12 50 05 a m" src="https://github.com/user-attachments/assets/9ceedae8-af2c-4e61-b721-f8e28db5b85e" />

---

## Requisitos

- **Python**: `>= 3.12`
- **Poetry**: Para gestión de dependencias y entorno virtual

---

## Instalación

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

En caso contrario, puedes instalar las dependencias e iniciar directamente el archivo `main.py`:

```bash
pip install pygame-ce
python src/omega_invasion/main.py
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

## Pruebas Automatizadas (Tests)

El proyecto cuenta con pruebas con la libreria **pytest** ejecutadas en modo *headless*:

```bash
# Ejecutar todas las pruebas
poetry run pytest

# Ejecutar con salida detallada
poetry run pytest -v
```

---

## Autor

- **Ian Salazar** ([isalazar@utem.cl](mailto:[salazar@utem.cl]))
