"""
=============================================================================
Módulo: elements.py
Descripción: Clase base que encapsula las esperas explícitas de Selenium.
             Permite buscar elementos en el DOM esperando a que estén presentes
             antes de interactuar con ellos, evitando errores por carga lenta.
=============================================================================
"""

import os  # Módulo estándar para acceder a variables de entorno del sistema

from selenium.webdriver.common.by import By  # Enum con estrategias de localización (ID, XPATH, CSS, etc.)
from selenium.webdriver.support import expected_conditions  # Condiciones predefinidas para esperas explícitas
from selenium.webdriver.support.ui import WebDriverWait  # Clase que implementa esperas explícitas en Selenium
from selenium.webdriver.support.select import Select  # Clase para interactuar con elementos <select> de HTML


class Elements:
    """
    Clase que proporciona métodos para interactuar con elementos del DOM
    utilizando esperas explícitas (explicit waits) de Selenium.

    Las esperas explícitas permiten que el test espere hasta que un elemento
    esté disponible en el DOM antes de intentar interactuar con él.
    Esto es fundamental para páginas con carga dinámica (JavaScript/AJAX).

    Atributos:
        __browser: Instancia privada del WebDriver (Chrome, Firefox, etc.)
                   Se recibe en el constructor y se usa internamente.
    """

    def __init__(self, browser):
        """
        Constructor de la clase Elements.

        Args:
            browser: Instancia del WebDriver de Selenium (ej: webdriver.Chrome()).
                     Se almacena como atributo privado (__browser) para uso interno.
        """
        self.__browser = browser  # Almacena el driver como atributo privado (name mangling)

    def _implicity_wait(self, element_by=By):
        """
        Espera explícita que busca un elemento en el DOM hasta que esté presente.

        Este método utiliza WebDriverWait para esperar un tiempo máximo definido
        por la variable de entorno TIME_IMPLICITY. Si el elemento aparece antes
        del timeout, lo retorna inmediatamente. Si no aparece, lanza una excepción.

        NOTA: A pesar del nombre "implicity_wait", este método implementa una
        ESPERA EXPLÍCITA (explicit wait), que es más precisa y recomendada
        que las esperas implícitas (implicit waits) de Selenium.

        Args:
            element_by (tuple): Tupla con la estrategia de localización y el valor.
                                Ejemplo: (By.ID, "mi_elemento")
                                         (By.XPATH, "//button[@id='submit']")
                                         (By.CSS_SELECTOR, ".clase-css")

        Returns:
            WebElement: El elemento encontrado en el DOM, listo para interactuar
                        (click, send_keys, get text, etc.)

        Raises:
            AssertionError: Si el elemento no se encuentra dentro del tiempo de espera.

        Ejemplo de uso:
            # Buscar un botón por ID y hacer click
            self._implicity_wait(element_by=(By.ID, "btn_login")).click()

            # Buscar un campo de texto por XPATH y escribir
            self._implicity_wait(element_by=(By.XPATH, "//input[@name='user']")).send_keys("admin")
        """
        try:
            # WebDriverWait espera hasta TIME_IMPLICITY segundos
            # expected_conditions.presence_of_element_located verifica que el elemento
            # exista en el DOM (no necesariamente visible, solo presente)
            element = WebDriverWait(
                self.__browser,                                    # Driver del navegador
                int(os.getenv("TIME_IMPLICITY", 10))              # Timeout en segundos (default 10)
            ).until(
                expected_conditions.presence_of_element_located(element_by)  # Condición a cumplir
            )
        except Exception as ex:
            # Si ocurre un timeout o error, se imprime el detalle
            print(ex)
            # Se fuerza un fallo del test con un mensaje descriptivo
            assert False, f"Elemento no encontrado en el DOM: {element_by}"

        return element  # Retorna el WebElement encontrado para encadenar acciones
