"""
Módulo: elements.py
Descripción: Esperas explícitas de Selenium para buscar elementos en el DOM.
"""

import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Elements:
    """Proporciona esperas explícitas para interactuar con elementos del DOM."""

    def __init__(self, browser):
        self.__browser = browser

    def _implicity_wait(self, element_by=By):
        """
        Espera hasta que el elemento sea visible en el DOM y lo retorna.

        Args:
            element_by (tuple): Tupla (By.ESTRATEGIA, "valor").
                                Ej: (By.ID, "email"), (By.XPATH, "//button")

        Returns:
            WebElement: Elemento encontrado, listo para .click() o .send_keys()

        Raises:
            AssertionError: Si el elemento no aparece dentro del timeout.
        """
        try:
            element = WebDriverWait(
                self.__browser,
                int(os.getenv("TIME_IMPLICITY", 10))
            ).until(
                expected_conditions.visibility_of_element_located(element_by)
            )
        except Exception as ex:
            print(ex)
            assert False, f"Elemento no encontrado en el DOM: {element_by}"

        return element
