# 🧪 Base Selenium - Framework de Automatización Web

Repositorio base para aprender automatización de pruebas web con **Python + Selenium + Behave (BDD)**.

Diseñado como material de apoyo para las charlas de automatización 2026. Los alumnos pueden clonar este proyecto y usarlo como punto de partida para automatizar cualquier aplicación web.

---

## 📌 ¿Qué hace este proyecto?

Automatiza pruebas funcionales web sobre [HakaTools](https://hakatools.hakalab.com) usando:

- **Behave** como framework BDD (escenarios en lenguaje natural)
- **Selenium WebDriver** para interactuar con el navegador
- **Allure Report** para generar reportes visuales con screenshots
- **Page Object Model (POM)** como patrón de diseño
- **Sistema de plugins (pluggy)** para arquitectura extensible

---

## 🛠️ Prerrequisitos técnicos

| Herramienta | Versión mínima | Notas |
|-------------|---------------|-------|
| Python | 3.9+ | [Descargar](https://www.python.org/downloads/) |
| pip | 21+ | Viene con Python |
| Google Chrome | Última estable | El framework usa Chrome por defecto |
| Java JRE/JDK | 8+ | Requerido para Allure Report |
| Git | 2.x | Para clonar el repositorio |

> **macOS**: Java se puede instalar con `brew install openjdk`  
> **Windows**: Descargar desde [adoptium.net](https://adoptium.net/)

---

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Base_selenium
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
EXECUTION_TYPE=manager
BROWSER=chrome
URL=https://hakatools.hakalab.com
TIME_IMPLICITY=10
```

| Variable | Valores posibles | Descripción |
|----------|-----------------|-------------|
| `EXECUTION_TYPE` | `manager` / `localhost` | `manager` descarga el driver automáticamente. `localhost` usa drivers locales del proyecto |
| `BROWSER` | `chrome` / `firefox` / `safari` | Navegador a utilizar |
| `URL` | URL válida | Dirección de la aplicación bajo prueba |
| `TIME_IMPLICITY` | Número (segundos) | Tiempo máximo de espera para encontrar elementos |
| `EXECUTOR_NAME` | Texto libre | Tu nombre (aparece en sección Executors del reporte) |
| `EXECUTOR_BUILD_NAME` | Texto libre | Nombre del build o rol (ej: "QA Automatizador") |
| `EXECUTOR_TYPE` | `local` / `jenkins` / `gitlab` | Tipo de ejecución para el reporte |

---

## 📁 Estructura del proyecto

```
Base_selenium/
├── features/                        # Capa de pruebas BDD
│   ├── HU1.feature                  # Escenarios en lenguaje Gherkin
│   ├── environment.py               # Hooks de Behave (orquestador de plugins)
│   └── steps/
│       └── test_selenium.py         # Steps: conectan Gherkin con código Python
│
├── helper/                          # Capa de soporte/framework
│   ├── pages/
│   │   └── page_hakatoolsl.py       # Page Object Model (localizadores de elementos)
│   ├── plugins/
│   │   ├── PluginSpec.py            # Especificación de hooks (contrato/interfaz)
│   │   ├── SeleniumPlugin.py        # Plugin: gestión del navegador
│   │   └── AllurePlugin.py          # Plugin: reportería y screenshots
│   ├── selenium_class/
│   │   ├── elements.py              # Clase de esperas explícitas
│   │   └── web_driver/              # Drivers locales por OS (Chrome, Firefox, etc.)
│   ├── services_class/
│   │   └── webformulario.py                   # Clase que maneja logica denegocio
│   └── vendor/
│       └── allure-2.13.6/           # Ejecutable de Allure Report
│
├── report/                          # Reportes generados (HTML)
├── .env                             # Variables de entorno (no se sube a git)
├── requirements.txt                 # Dependencias Python
└── README.md
```

---

## 🏗️ Arquitectura y flujo de ejecución

```
┌─────────────────────────────────────────────────────────────┐
│  .feature (Gherkin)                                         │
│  "Given ingreso a hakatools"                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ Behave conecta texto con función
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  steps/test_selenium.py                                     │
│  @given('ingreso a hakatools')                              │
│  def ingreso_a_hakatools(context):                          │
│      context.browser.get(os.getenv("URL"))                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ Usa localizadores de
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  pages/page_hakatoolsl.py (Page Object Model)               │
│  txt_email = (By.ID, "email")                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ Busca elementos con
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  selenium_class/elements.py                                 │
│  WebDriverWait + expected_conditions                        │
└─────────────────────────────────────────────────────────────┘
```

**Ciclo de vida por escenario:**

1. `SeleniumPlugin.before_scenario()` → Carga `.env`, abre el navegador
2. Se ejecutan los steps (Given → When → Then)
3. `AllurePlugin.after_step()` → Captura screenshot en cada paso
4. `SeleniumPlugin.after_scenario()` → Cierra el navegador

---

## ▶️ Ejecución de pruebas

### Ejecutar todos los escenarios

```bash
behave features/
```

### Ejecutar con reporte Allure

```bash
behave -f allure_behave.formatter:AllureFormatter -o report/allure-results ./features
```

### Ejecutar por tag específico

```bash
# Un tag
behave -f allure_behave.formatter:AllureFormatter -o report/allure-results --tags=@HU-2 ./features

# Múltiples tags (OR)
behave --tags=@HU-2,@HU-3 ./features

# Tag de regresión completa
behave --tags=@Regresion ./features
```

### Ejecutar un feature específico

```bash
behave features/HU1.feature
```

---

## 📊 Visualizar reporte Allure

Después de ejecutar las pruebas con el formatter de Allure:

```bash
./helper/vendor/allure-2.13.6/bin/allure serve report/allure-results
```

Esto genera el reporte HTML y lo abre automáticamente en el navegador.

> **Windows**: usar `helper\vendor\allure-2.13.6\bin\allure.bat serve report\allure-results`

---

## 🚀 Ejecución en Pipeline (GitHub Actions)

El proyecto incluye un workflow de GitHub Actions que ejecuta los escenarios **en paralelo** y publica el reporte Allure en GitHub Pages.

### Cómo funciona

```
  Push a main / PR / Manual
          │
    ┌─────┼─────┐
    ▼           ▼
┌────────┐ ┌────────┐
│ @HU-2  │ │ @HU-3  │   ← Jobs en PARALELO (Chrome headless)
└───┬────┘ └───┬────┘
    │           │
    └─────┬─────┘
          ▼
   ┌─────────────┐
   │  Reporte    │   ← Consolida resultados + publica en GitHub Pages
   │  Allure     │
   └─────────────┘
```

### Cuándo se ejecuta

| Evento | Descripción |
|--------|-------------|
| Push a `main` | Se ejecuta automáticamente |
| Pull Request a `main` | Se ejecuta para validar cambios |
| Manual | Desde la pestaña Actions → "Run workflow" |

### Cómo agregar más tests en paralelo

Editar `.github/workflows/test-parallel.yml` y agregar tags al array `matrix`:

```yaml
strategy:
  matrix:
    tag:
      - "@HU-2"
      - "@HU-3"
      - "@HU-4"    # ← Agregar nuevos tags aquí
      - "@smoke"
```

Cada tag genera un job independiente que se ejecuta simultáneamente.

### Configurar GitHub Pages (una sola vez)

1. Ir a **Settings → Pages** en el repositorio de GitHub
2. En **Source** seleccionar: **Deploy from a branch**
3. En **Branch** seleccionar: `gh-pages` / `/ (root)`
4. Guardar

Después del primer push a `main`, el reporte estará disponible en:

```
https://<tu-usuario>.github.io/<nombre-repo>/
```

### Secciones del reporte en pipeline

| Sección | Qué muestra |
|---------|-------------|
| **Trend** | Gráfico de tendencia (passed/failed) entre ejecuciones |
| **Executors** | Muestra "GitHub Actions" con el número de run |
| **Environment** | Browser, URL, OS del runner |
| **Timeline** | Duración de cada test en paralelo |

### Variables de entorno en el pipeline

Las variables se configuran directamente en el workflow (no se usa `.env` en CI):

```yaml
EXECUTION_TYPE=manager
BROWSER=chrome
URL=https://hakatools.hakalab.com
EXECUTOR_NAME=GitHub Actions
EXECUTOR_TYPE=github
```

> **Nota**: Para datos sensibles (passwords, tokens), usar **Settings → Secrets and variables → Actions** en GitHub y referenciarlos como `${{ secrets.MI_SECRETO }}`.

---

## 🧩 Cómo agregar nuevas pruebas

### 1. Crear o editar el archivo .feature

```gherkin
@mi_tag
Scenario: Mi nuevo escenario
  Given ingreso a hakatools
  When hago click en "Mi Elemento"
  Then valido que aparece "Resultado esperado"
```

### 2. Crear los localizadores en un Page Object

```python
# helper/pages/mi_pagina.py
from selenium.webdriver.common.by import By

class MiPagina:
    btn_elemento = (By.ID, "mi-boton")
    txt_resultado = (By.CSS_SELECTOR, ".resultado")
```

### 3. Implementar los steps

```python
# features/steps/mi_test.py
from behave import given, when, then
from helper.pages.mi_pagina import MiPagina

@when(u'hago click en "{elemento}"')
def click_elemento(context, elemento):
    context.elements._implicity_wait(element_by=MiPagina.btn_elemento).click()
```

---

## 📚 Conceptos clave para entender el código

| Concepto | Qué es | Dónde se usa |
|----------|--------|--------------|
| **BDD (Behave)** | Escribir pruebas en lenguaje natural | `features/*.feature` |
| **Page Object Model** | Separar localizadores del código de test | `helper/pages/` |
| **Esperas explícitas** | Esperar a que un elemento exista antes de interactuar | `elements.py` |
| **Plugins (pluggy)** | Extender funcionalidad sin modificar el core | `helper/plugins/` |
| **WebDriverManager** | Descarga automática del driver del navegador | `SeleniumPlugin.py` |
| **Allure Report** | Reportes HTML con screenshots paso a paso | `AllurePlugin.py` |
| **Soft assertions** | Validar múltiples campos sin detenerse en el primer fallo | `test_selenium.py` |

---

## ⚠️ Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Verificar que el entorno virtual está activo y ejecutar `pip install -r requirements.txt` |
| `WebDriverException: chromedriver not found` | Usar `EXECUTION_TYPE=manager` en `.env` para descarga automática |
| `SessionNotCreatedException: version mismatch` | Actualizar Chrome o usar `EXECUTION_TYPE=manager` |
| `FileNotFoundError: .env` | Crear el archivo `.env` siguiendo la sección de configuración |
| Allure no genera reporte | Verificar que Java está instalado (`java -version`) |

---

## 🤝 Contribuir

1. Crear una rama desde `main`
2. Implementar cambios siguiendo la estructura existente
3. Documentar los nuevos steps y page objects
4. Crear merge request

---

© 2026 - Material de apoyo para charlas de automatización. Centyc.cl
@author William Navarrete y Felipe Farias
