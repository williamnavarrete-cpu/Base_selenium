# Diagrama de Arquitectura - Framework de Automatización Web

Usa este contenido para generar un diagrama visual en herramientas como:
- [Mermaid Live Editor](https://mermaid.live)
- [Draw.io](https://app.diagrams.net)
- ChatGPT / Claude con generación de imágenes
- Excalidraw

---

## Diagrama Mermaid - Arquitectura General

```mermaid
graph TB
    subgraph "📄 Capa BDD - Gherkin"
        A[HU1.feature<br/>Escenarios en lenguaje natural]
    end

    subgraph "⚙️ Capa de Orquestación"
        B[environment.py<br/>Hooks de Behave]
        C[PluginManager - pluggy<br/>Gestiona ciclo de vida]
    end

    subgraph "🔌 Capa de Plugins"
        D[SeleniumPlugin<br/>Inicializa/cierra navegador]
        E[AllurePlugin<br/>Screenshots y reportes]
    end

    subgraph "🧪 Capa de Steps"
        F[test_selenium.py<br/>Given / When / Then]
    end

    subgraph "📐 Capa Page Object Model"
        G[page_hakatoolsl.py<br/>Localizadores de elementos]
    end

    subgraph "🔧 Capa de Selenium Helpers"
        H[elements.py<br/>Esperas explícitas]
        I[WebDriver<br/>Chrome / Firefox / Safari]
    end

    subgraph "🌐 Aplicación Bajo Prueba"
        J[HakaTools Web App]
    end

    subgraph "📊 Reportería"
        K[Allure Report<br/>HTML + Screenshots]
    end

    A -->|Behave parsea| B
    B -->|Delega a| C
    C -->|before_scenario| D
    C -->|after_step| E
    B -->|Ejecuta steps| F
    F -->|Usa localizadores| G
    F -->|Busca elementos| H
    H -->|Controla| I
    I -->|Interactúa con| J
    D -->|Crea instancia| I
    E -->|Genera| K
```

---

## Diagrama Mermaid - Flujo de Ejecución por Escenario

```mermaid
sequenceDiagram
    participant Behave
    participant Environment
    participant SeleniumPlugin
    participant AllurePlugin
    participant Steps
    participant Elements
    participant Browser
    participant App as HakaTools

    Note over Behave: Inicia ejecución del .feature

    Behave->>Environment: before_scenario()
    Environment->>SeleniumPlugin: before_scenario()
    SeleniumPlugin->>SeleniumPlugin: load_dotenv(.env)
    SeleniumPlugin->>Browser: Crear WebDriver (Chrome)
    Browser-->>SeleniumPlugin: Instancia del navegador
    SeleniumPlugin->>Elements: new Elements(browser)

    Note over Behave: Ejecuta cada Step

    Behave->>Steps: Given ingreso a hakatools
    Steps->>Browser: browser.get(URL)
    Browser->>App: HTTP Request
    App-->>Browser: Página cargada

    Behave->>Environment: after_step()
    Environment->>AllurePlugin: after_step()
    AllurePlugin->>Browser: get_screenshot_as_png()
    Browser-->>AllurePlugin: Screenshot PNG
    AllurePlugin->>AllurePlugin: Adjuntar a reporte

    Behave->>Steps: When ingreso nombre "Hakito"
    Steps->>Elements: _implicity_wait(txt_first_name)
    Elements->>Browser: WebDriverWait + find_element
    Browser-->>Elements: WebElement encontrado
    Elements-->>Steps: WebElement
    Steps->>Browser: element.send_keys("Hakito")

    Behave->>Environment: after_step()
    Environment->>AllurePlugin: Screenshot automático

    Note over Behave: ... más steps ...

    Behave->>Steps: Then valido resultados
    Steps->>Elements: _implicity_wait(txt_result_form)
    Elements-->>Steps: WebElement con texto
    Steps->>Steps: soft_assertions (validar datos)

    Behave->>Environment: after_scenario()
    Environment->>SeleniumPlugin: after_scenario()
    SeleniumPlugin->>Browser: browser.quit()
    Browser-->>SeleniumPlugin: Navegador cerrado
```

---

## Diagrama Mermaid - Estructura de Carpetas

```mermaid
graph LR
    subgraph "Raíz del Proyecto"
        ROOT[Base_selenium/]
    end

    subgraph "features/ - Pruebas BDD"
        F1[HU1.feature]
        F2[environment.py]
        F3[steps/test_selenium.py]
    end

    subgraph "helper/ - Framework"
        H1[pages/page_hakatoolsl.py]
        H2[plugins/PluginSpec.py]
        H3[plugins/SeleniumPlugin.py]
        H4[plugins/AllurePlugin.py]
        H5[selenium_class/elements.py]
        H6[vendor/allure-2.13.6/]
    end

    subgraph "Configuración"
        C1[.env]
        C2[requirements.txt]
        C3[.gitignore]
    end

    ROOT --> F1
    ROOT --> F2
    ROOT --> F3
    ROOT --> H1
    ROOT --> H2
    ROOT --> H3
    ROOT --> H4
    ROOT --> H5
    ROOT --> H6
    ROOT --> C1
    ROOT --> C2
    ROOT --> C3
```

---

## Diagrama Mermaid - Sistema de Plugins (pluggy)

```mermaid
graph LR
    subgraph "Especificación (Contrato)"
        SPEC[PluginSpec.py<br/>Define QUÉ hooks existen<br/>@hookspec]
    end

    subgraph "Implementaciones"
        IMPL1[SeleniumPlugin<br/>@hookimpl<br/>before_scenario<br/>after_scenario]
        IMPL2[AllurePlugin<br/>@hookimpl<br/>before_all<br/>after_step<br/>after_all]
        IMPL3[Tu Nuevo Plugin<br/>@hookimpl<br/>...]
    end

    subgraph "Gestor"
        PM[PluginManager<br/>pluggy]
    end

    SPEC -->|add_hookspecs| PM
    IMPL1 -->|register| PM
    IMPL2 -->|register| PM
    IMPL3 -.->|register| PM

    PM -->|pm.hook.before_scenario| IMPL1
    PM -->|pm.hook.after_step| IMPL2
```

---

## Prompt para IA generativa de imágenes

Si quieres generar una imagen visual del diagrama, usa este prompt:

> Crea un diagrama de arquitectura de software limpio y profesional para un framework de automatización de pruebas web. El diagrama debe mostrar las siguientes capas de arriba hacia abajo:
>
> 1. **Capa BDD** (arriba): Archivos .feature escritos en Gherkin (lenguaje natural)
> 2. **Capa de Orquestación**: environment.py con PluginManager de pluggy
> 3. **Capa de Plugins**: SeleniumPlugin (gestiona navegador) y AllurePlugin (reportes con screenshots)
> 4. **Capa de Steps**: Funciones Python decoradas con @given, @when, @then
> 5. **Capa Page Object Model**: Clases con localizadores de elementos (By.ID, By.XPATH)
> 6. **Capa Selenium**: Esperas explícitas (WebDriverWait) y WebDriver
> 7. **Aplicación web** (abajo): HakaTools como sistema bajo prueba
> 8. **Salida lateral**: Allure Report con HTML y screenshots
>
> Estilo: colores suaves, flechas que muestren el flujo de datos, iconos representativos para cada capa. Orientación vertical. Fondo blanco.

---

## Notas para presentación

- El **diagrama de arquitectura general** es ideal para explicar la visión completa del framework
- El **diagrama de secuencia** es perfecto para mostrar qué pasa cuando se ejecuta un test paso a paso
- El **diagrama de plugins** ayuda a entender cómo extender el framework sin tocar el código existente
- Todos los diagramas Mermaid se pueden pegar directamente en GitHub, GitLab, Notion o el [Mermaid Live Editor](https://mermaid.live)
