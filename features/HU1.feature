Feature: HU-721 - Formulario de registro básico de contacto
  Como usuario de HakaTools
  necesito registrar mis datos de contacto mediante un formulario básico
  para que el equipo comercial pueda contactarme posteriormente.

  Criterios de Aceptación:
    CA1: El usuario puede ingresar nombre, correo, dirección y dirección permanente.
    CA2: Al presionar "Enviar", el sistema muestra un resumen con los datos ingresados.
    CA3: Los datos del resumen deben coincidir exactamente con lo ingresado.

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

  @HU-2
  Examples: ejecucion combinatoria 1
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |

  @HU-3
  Examples: ejecucion combinatoria 2
    | usuario   | correo                | direccion           | direccion_permanente            |
    | "Hakito"  | "hakito@hakalab.com"  | "calle prueba 123"  | "calle permanente prueba 123 "  |
