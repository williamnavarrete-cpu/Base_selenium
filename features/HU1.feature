# ATDD: Este escenario SE ESCRIBIÓ ANTES de desarrollar la funcionalidad.
#       El desarrollador lo usó como guía para saber cuándo terminó.
# BDD:  Está escrito en lenguaje natural para que PO, QA y Dev lo entiendan.
# =========================================================================

# Estructura de un archivo .feature:
#   @Tag          → Etiquetas para filtrar/agrupar pruebas
#   Feature       → Nombre de la funcionalidad a probar
#   Scenario      → Un caso de prueba específico
#   Scenario Outline → Caso de prueba parametrizado (se ejecuta N veces)
#   Examples      → Tabla de datos para Scenario Outline
#
# Keywords de Gherkin:
#   Given → Precondición (estado inicial del sistema)
#   When  → Acción del usuario
#   And   → Continuación del keyword anterior (Given/When/Then)
#   Then  → Resultado esperado (validación)
#
# Parámetros:
#   <variable>    → Se reemplaza por valores de la tabla Examples
#   "texto"       → Texto literal que se pasa al step como argumento
# =============================================================================


Feature: HU-721 - Formulario de registro básico de contacto
  Como usuario de HakaTools
  necesito que los usuarios puedan registrar sus datos de contacto
  mediante un formulario básico en la plataforma
  para almacenar la información y contactarlos posteriormente.

  Contexto de negocio:
    El equipo comercial necesita capturar datos de potenciales clientes
    que visitan la plataforma. El formulario debe ser simple y rápido
    de completar para no generar fricción en el usuario.

  Criterios de Aceptación:
    CA1: El usuario debe poder ingresar nombre, correo, dirección actual
         y dirección permanente en el formulario básico.
    CA2: Al presionar el botón "Enviar", el sistema debe mostrar un resumen
         con todos los datos ingresados para que el usuario confirme visualmente
         que la información es correcta.
    CA3: Todos los campos ingresados deben reflejarse exactamente igual
         en el resumen de confirmación (sin alteraciones).


  @hakatools @formulario_basico @HU-721
  Scenario Outline: Registro exitoso de datos de contacto en formulario básico
    Given ingreso a hakatools
    When selecciono la lista "Formularios"
    And ingreso nombre de usuario <usuario>
    And ingreso correo <correo>
    And ingreso direccion <direccion>
    And ingreso direccion permanente <direccion_permanente>
    And selecciono opcion enviar
    Then valido resultados de formulario <usuario><correo><direccion><direccion_permanente>

  # Primer conjunto de datos de prueba
  # Cada fila de la tabla genera una ejecución independiente del Scenario Outline
  # El tag @HU-2 permite ejecutar solo esta combinación
  @HU-2
  Examples: ejecucion combinatoria 1
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  # Segundo conjunto de datos (puede tener datos diferentes para probar más casos)
  @HU-3
  Examples: ejecucion combinatoria 2
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |
