"""
Módulo: page_hakatoolsl.py
Descripción: Page Object Model (POM) para la página de HakaTools.
             Centraliza los localizadores de elementos de la UI.
"""

from selenium.webdriver.common.by import By


class PageModel:
    """Localizadores de la página de formularios de HakaTools."""

    by_search_box = (By.XPATH, "//h1[text()='¡Bienvenidos a HakaTools!']")
    card_element = (By.XPATH, "//h2[text()='Formularios']")
    txt_first_name = (By.ID, "first_name")
    txt_email = (By.ID, "email")
    txt_direccion = (By.ID, "currentAddress")
    txt_direccion_permanente = (By.ID, "permanentAddress")
    btn_enviar = (By.ID, "submitBasicForm")
    txt_result_form = (By.ID, "resultBasicForm")
