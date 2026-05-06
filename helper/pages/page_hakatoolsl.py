"""
=============================================================================
Módulo: page_hakatoolsl.py
Descripción: Page Object Model (POM) para la página de HakaTools.

Patrón Page Object Model:
    Es un patrón de diseño que crea una clase por cada página (o sección)
    de la aplicación web. Cada clase contiene:
    - Los LOCALIZADORES de los elementos de esa página (selectores)
    - Los MÉTODOS que representan acciones del usuario en esa página

    Ventajas:
    - Si cambia un elemento en la UI, solo se modifica en UN lugar
    - Los tests son más legibles (usan nombres descriptivos)
    - Facilita el mantenimiento cuando la aplicación cambia
    - Promueve la reutilización de código entre tests

Convención de nombres:
    - by_*    → Localizadores genéricos
    - card_*  → Elementos tipo tarjeta/card
    - txt_*   → Campos de texto (input)
    - btn_*   → Botones
    - lbl_*   → Labels/etiquetas
    - drp_*   → Dropdowns/selectores
=============================================================================
"""

from selenium.webdriver.common.by import By  # Enum con estrategias de localización de elementos


class PageModel:
    """
    Page Object para la página de formularios de HakaTools.

    Contiene los localizadores de todos los elementos con los que
    interactúan los tests. Cada localizador es una TUPLA con:
    - Primer elemento: estrategia de búsqueda (By.ID, By.XPATH, By.CSS_SELECTOR, etc.)
    - Segundo elemento: valor del selector

    Estrategias de localización más comunes:
        By.ID          → Busca por atributo id="valor" (más rápido y estable)
        By.XPATH       → Busca usando expresiones XPath (más flexible pero frágil)
        By.CSS_SELECTOR → Busca usando selectores CSS (buen balance)
        By.NAME        → Busca por atributo name="valor"
        By.CLASS_NAME  → Busca por clase CSS

    Recomendación: Priorizar By.ID > By.CSS_SELECTOR > By.XPATH
    """

    def __init__(self, browser):
        """
        Constructor del Page Object.

        Args:
            browser: Instancia del WebDriver para interactuar con la página.
                     Se almacena por si se necesitan métodos de acción en la clase.
        """
        self.browser = browser

    # === LOCALIZADORES DE ELEMENTOS ===
    # Cada variable es una tupla (By.ESTRATEGIA, "valor_selector")
    # Se usan como atributos de CLASE (no de instancia) para acceso directo

    # Título principal de la página de bienvenida
    # XPath busca un elemento <h1> cuyo texto sea exactamente '¡Bienvenidos a HakaTools!'
    by_search_box = (By.XPATH, "//h1[text()='¡Bienvenidos a HakaTools!']")

    # Tarjeta/card de "Formularios" en la página principal
    # XPath busca un elemento <h2> con texto 'Formularios'
    card_element = (By.XPATH, "//h2[text()='Formularios']")

    # Campo de texto para el nombre (primer nombre)
    # By.ID es la estrategia más eficiente y estable
    txt_first_name = (By.ID, "first_name")

    # Campo de texto para el correo electrónico
    txt_email = (By.ID, "email")

    # Campo de texto para la dirección actual
    txt_direccion = (By.ID, "currentAddress")

    # Campo de texto para la dirección permanente
    txt_direccion_permanente = (By.ID, "permanentAddress")

    # Botón para enviar el formulario básico
    btn_enviar = (By.ID, "submitBasicForm")

    # Contenedor donde se muestran los resultados después de enviar
    # Se usa para validar que los datos ingresados se procesaron correctamente
    txt_result_form = (By.ID, "resultBasicForm")
