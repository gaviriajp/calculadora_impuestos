# Calculadora de Impuestos

## Integrantes

* **Juan Pablo Gaviria Franco**
* **Juan Esteban Correa Guzman**

## INTEGRANTES DEL GUI

* **Andres Felipe Zora Sepulveda**
* **Juan Jose Camargo Chaverra**

## Descripción del proyecto

La aplicación permite ingresar el precio de un producto, seleccionar la categoría de impuesto correspondiente y calcular el valor del impuesto y el total a pagar.

El sistema también permite agregar el impuesto correspondiente a las bolsas plásticas cuando la compra las incluye.

El proyecto cuenta con dos interfaces para interactuar con la aplicación:

* **Interfaz de consola**, desarrollada en Python.
* **Interfaz gráfica**, desarrollada utilizando Kivy.

La lógica de negocio se encuentra separada de las interfaces de usuario, permitiendo reutilizar las funciones de cálculo y mantener las pruebas unitarias independientes de la interfaz.

---

## Arquitectura del Proyecto

```text
calculadora_impuestos/
├── src/
│   ├── model/
│   │   ├── __init__.py
│   │   └── calculadora_impuestos.py
│   │       # Lógica de negocio, cálculos y validaciones
│   │
│   └── view/
│       ├── __init__.py
│       ├── Main.py
│       │   # Interfaz gráfica desarrollada con Kivy
│       │
│       └── console/
│           ├── __init__.py
│           └── consola_calculadora.py
│               # Interfaz de consola
│
├── tests/
│   ├── __init__.py
│   └── test_calculadora.py
│       # Pruebas unitarias del model
│
└── doc/
    ├── Casos de prueba calculadora impuestos.xlsx
    └── Entrevista.mp4
```

La aplicación utiliza una separación entre la lógica de negocio y las interfaces de usuario.

La carpeta `model` contiene los cálculos, constantes, validaciones y excepciones del sistema.

La carpeta `view` contiene las diferentes interfaces mediante las cuales el usuario puede interactuar con la aplicación.

La carpeta `tests` contiene las pruebas unitarias utilizadas para verificar el funcionamiento de la lógica de negocio.

---

# Funcionalidades

La aplicación permite trabajar con las siguientes categorías:

* **IVA 19%**
* **IVA 5%**
* **Exento**
* **Excluido**
* **Impuesto Nacional al Consumo (INC)**
* **Impuesto a licores**
* **Impuesto de bolsas plásticas**

## Funcionalidad básica

La funcionalidad principal de la aplicación permite:

1. Ingresar el precio de un producto.
2. Seleccionar la categoría de impuesto correspondiente.
3. Calcular el valor del impuesto.
4. Calcular el valor total de la compra.
5. Mostrar el detalle del cálculo realizado.

Las categorías de impuesto disponibles son:

* IVA 19%
* IVA 5%
* Exento
* Excluido
* Impuesto Nacional al Consumo (INC)
* Impuesto a licores

El sistema permite seleccionar únicamente una categoría de impuesto para cada cálculo.

## Funcionalidad extra

Como funcionalidad adicional, la aplicación permite calcular el valor correspondiente a las bolsas plásticas.

El usuario puede ingresar la cantidad de bolsas utilizadas en la compra y el sistema calcula automáticamente su valor.

El valor establecido para cada bolsa plástica es:

```text
$73
```

Por ejemplo, si el usuario ingresa 3 bolsas:

```text
3 × $73 = $219
```

El valor calculado de las bolsas se suma al total de la compra.

---

# Entradas

## 1. Precio del producto

El usuario debe ingresar el precio del producto.

El valor:

* Debe ser un valor numérico.
* Debe ser mayor que cero.
* No puede superar el límite máximo establecido en el código.
* Puede contener comas como separadores al momento de ingresar el valor.

El límite máximo establecido actualmente es:

```text
$1.000.000.000
```

## 2. Categoría del impuesto

El usuario debe seleccionar una de las siguientes categorías:

```text
1. IVA 19%
2. IVA 5%
3. Exento
4. Excluido
5. Impuesto Nacional al Consumo (INC)
6. Impuesto a licores
```

Solo se puede seleccionar una categoría de impuesto por cálculo.

## 3. Bolsas plásticas

El usuario puede ingresar la cantidad de bolsas plásticas utilizadas en la compra.

Si no se utilizan bolsas, se puede ingresar:

```text
0
```

Si se utilizan bolsas, se debe ingresar una cantidad mayor que cero.

---

# Proceso

El funcionamiento general de la aplicación es:

1. El usuario inicia la aplicación.
2. Selecciona la interfaz de consola o ejecuta la interfaz gráfica.
3. Ingresa el precio del producto.
4. Selecciona la categoría de impuesto.
5. Ingresa la cantidad de bolsas plásticas.
6. El sistema valida los datos ingresados.
7. Se calcula el impuesto correspondiente.
8. Se calcula el valor de las bolsas cuando corresponde.
9. Se suman el precio base, el impuesto y el valor de las bolsas.
10. El sistema muestra el detalle y el total a pagar.

---

# Salidas

La aplicación muestra:

* Precio base del producto.
* Nombre del impuesto aplicado.
* Valor del impuesto.
* Valor del impuesto de bolsas plásticas.
* **Total a pagar.**

Ejemplo:

```text
========================================
       DETALLE DE LA COMPRA
========================================
Precio base:       $50000.00
IVA 19%:            $9500.00
Bolsas:               $0.00
----------------------------------------
TOTAL A PAGAR:     $59500.00
========================================
```

En la interfaz gráfica, el resultado se muestra directamente en pantalla después de presionar el botón **Calcular**.

---

# Interfaz gráfica

La aplicación cuenta con una interfaz gráfica desarrollada utilizando **Kivy**, pensada para ser clara y amigable con el usuario: campos de entrada bien identificados, botones de impuesto con selección visual y resultados organizados en un panel de resultado.

La GUI implementa tanto la **funcionalidad básica** (cálculo de impuestos por categoría) como la **funcionalidad extra** (cálculo del impuesto de bolsas plásticas), descritas anteriormente.

La interfaz gráfica permite:

* Ingresar el precio del producto.
* Seleccionar el tipo de impuesto.
* Seleccionar visualmente el impuesto mediante botones.
* Ingresar la cantidad de bolsas plásticas.
* Calcular el impuesto.
* Visualizar el precio base.
* Visualizar el nombre del impuesto aplicado.
* Visualizar el valor del impuesto.
* Visualizar el valor de las bolsas.
* Visualizar el total a pagar.
* Mostrar mensajes de error mediante ventanas emergentes.

## Diseño de la interfaz

La interfaz está organizada utilizando diferentes componentes de Kivy:

* `BoxLayout`
* `GridLayout`
* `Label`
* `TextInput`
* `Button`
* `Popup`

La interfaz está organizada en diferentes secciones para facilitar la interacción del usuario.

En la parte superior se encuentra el título y una instrucción para el usuario.

Posteriormente se encuentra el formulario para ingresar el precio y seleccionar el tipo de impuesto.

Los tipos de impuesto se presentan mediante botones:

```text
┌─────────────────────────────────────────────┐
│             CALCULADORA DE IMPUESTOS        │
│                                             │
│ Precio:          [____________________]     │
│                                             │
│ Seleccione impuesto:                        │
│                                             │
│ [IVA 19%] [IVA 5%] [INC 8%]                │
│ [Licores] [Exento] [Excluido]               │
│                                             │
│ Cantidad de bolsas: [__________]            │
│                                             │
│ Resultado:       [ CALCULAR ]               │
│                                             │
│ Base: $100,000.00                           │
│ IVA 19%: $19,000.00                         │
│ Bolsas: $0.00                               │
│ TOTAL: $119,000.00                          │
└─────────────────────────────────────────────┘
```

El botón del impuesto seleccionado se identifica visualmente para facilitar al usuario saber qué opción está utilizando.

---

# Manejo de excepciones

El sistema cuenta con manejo de excepciones tanto en la lógica de negocio como en la interfaz gráfica.

En la lógica de negocio se utilizan excepciones personalizadas para representar errores específicos:

```text
PrecioInvalidoError
ImpuestoInvalidoError
```

## PrecioInvalidoError

Esta excepción se utiliza cuando el precio ingresado no cumple con las condiciones establecidas.

Puede ocurrir cuando:

* El campo está vacío.
* El valor contiene texto no numérico.
* El precio es igual o menor que cero.
* El precio supera el límite máximo permitido.

## ImpuestoInvalidoError

Esta excepción se utiliza cuando la selección del impuesto no es válida.

Puede ocurrir cuando:

* No se selecciona ningún impuesto.
* Se seleccionan múltiples impuestos.
* Se seleccionan simultáneamente IVA 19% e IVA 5%.
* Se ingresan datos inválidos relacionados con las bolsas.

---

# Mensajes de error amigables

La interfaz gráfica utiliza bloques `try` y `except` para controlar los errores y evitar que la aplicación se cierre cuando el usuario ingresa información incorrecta.

Los errores son mostrados mediante una ventana emergente (`Popup`).

Los mensajes de error buscan indicar al usuario:

* **Qué sucedió.**
* **Dónde ocurrió el problema.**
* **Cómo solucionarlo.**

Por ejemplo, cuando se ingresa un precio inválido, el sistema muestra un mensaje similar a:

```text
Error de precio

Qué sucedió:
el precio ingresado no es válido.

Dónde:
campo Precio.

Cómo se soluciona:
ingrese un valor numérico mayor que 0
y hasta 1.000.000.000.

Ejemplo:
2500000

                    [Cerrar]
```

De esta manera, el usuario puede identificar el problema y corregirlo sin necesidad de cerrar la aplicación.

También se controlan errores inesperados mediante una excepción general:

```
except Exception as error:
```

Esto permite mostrar un mensaje al usuario en lugar de finalizar abruptamente la aplicación.

---

# Validaciones

El sistema valida diferentes situaciones para evitar cálculos incorrectos.

Entre ellas:

* Precio vacío.
* Precio con letras o caracteres no numéricos.
* Precio negativo.
* Precio igual a cero.
* Precio superior al límite establecido.
* No seleccionar una categoría de impuesto.
* Seleccionar simultáneamente IVA 5% e IVA 19%.
* Seleccionar más de una categoría de impuesto.
* Ingresar una cantidad inválida de bolsas.
* Ingresar una cantidad negativa de bolsas.

Las validaciones principales relacionadas con el precio se realizan mediante la función:

```
validar_y_convertir_precio(texto)
```

Mientras que el cálculo principal se realiza mediante:

```
calcular_impuestos(...)
```

---

# Pruebas unitarias

Las pruebas unitarias del proyecto se encuentran en la carpeta `tests/`, específicamente en el archivo:

```text
tests/
├── __init__.py
└── test_calculadora.py
```

El archivo `test_calculadora.py` contiene 10 casos de prueba para verificar el correcto funcionamiento de la calculadora de impuestos.

### Distribución de las pruebas

| Código | Tipo de prueba | Descripción |
| ------ | -------------- | ----------------------------------------------------- |
| CP-01 | Normal | Cálculo de IVA del 19% |
| CP-02 | Normal | Cálculo del Impuesto Nacional al Consumo (INC) del 8% |
| CP-03 | Normal | IVA del 19% incluyendo bolsas plásticas |
| CP-04 | Excepcional | Cálculo con un precio muy alto |
| CP-05 | Excepcional | Compra sin seleccionar ningún impuesto |
| CP-06 | Excepcional | Producto excluido con bolsas plásticas |
| CP-07 | Error | Ingreso de un precio negativo |
| CP-08 | Error | Ingreso de letras en el precio |
| CP-09 | Error | Ingreso de un precio vacío |
| CP-10 | Error | Selección simultánea de IVA del 19% e IVA del 5% |

### ¿Cómo ejecutar las pruebas?

Para ejecutar las pruebas unitarias, primero se debe abrir una terminal ubicada en la carpeta raíz del proyecto:

```text
calculadora_impuestos/
```

Luego se ejecuta el siguiente comando:

```bash
python tests/test_calculadora.py
```

El programa ejecutará automáticamente los 10 casos de prueba y mostrará en consola el resultado de cada uno.

### Resultado esperado

Cuando todas las pruebas funcionan correctamente, se mostrará un resultado similar al siguiente:

```text
============================================================
       PRUEBAS DE LA CALCULADORA DE IMPUESTOS
============================================================

RESULTADO DE CADA CASO
------------------------------------------------------------
CP-01    - IVA 19%                        [PASÓ]
CP-02    - INC 8%                         [PASÓ]
CP-03    - IVA 19% + bolsas               [PASÓ]
CP-04    - Precio muy alto                [PASÓ]
CP-05    - Ningún impuesto                [PASÓ]
CP-06    - Excluido + bolsas              [PASÓ]
CP-07    - Precio negativo                [PASÓ]
CP-08    - Letras en precio               [PASÓ]
CP-09    - Precio vacío                   [PASÓ]
CP-10    - Doble IVA                      [PASÓ]

============================================================
RESULTADO FINAL
============================================================
Pruebas ejecutadas: 10
Pruebas exitosas:   10
Pruebas fallidas:   0
Errores:            0

TODAS LAS PRUEBAS PASARON
============================================================
```

Las pruebas utilizan el módulo `unittest` de Python y permiten comprobar tanto los cálculos correctos como el manejo de situaciones excepcionales y errores de entrada.

---

# Ejecución de la aplicación por consola

La aplicación cuenta con una interfaz de consola que permite al usuario calcular los impuestos correspondientes a una compra.

El archivo principal de la interfaz se encuentra en:

```text
src/
└── view/
    └── console/
        └── consola_calculadora.py
```

## ¿Cómo ejecutar la aplicación?

Para ejecutar la aplicación, se debe abrir una terminal ubicada en la carpeta raíz del proyecto:

```text
calculadora_impuestos/
```

Luego ejecutar el siguiente comando:

```bash
python src/view/console/consola_calculadora.py
```

## Menú principal

Al iniciar la aplicación se muestra el siguiente menú:

```text
========================================
   CALCULADORA DE IMPUESTOS DE VENTA
========================================
1. Calcular impuestos de una compra
2. Salir
Seleccione una opcion:
```

Las opciones disponibles son:

* **1. Calcular impuestos de una compra:** inicia el proceso para calcular los impuestos de una compra.
* **2. Salir:** finaliza la aplicación.

## Proceso de cálculo

Al seleccionar la opción 1, la aplicación solicita el precio de la compra y posteriormente permite seleccionar el tipo de impuesto que corresponde al producto.

Las categorías disponibles son:

```text
1. IVA 19%
2. IVA 5%
3. Exento
4. Excluido
5. Impuesto Nacional al Consumo (INC)
6. Impuesto a licores
```

Después de seleccionar la categoría, la aplicación pregunta si la compra incluye bolsas plásticas:

```text
¿La compra incluye bolsas plasticas? (s/n):
```

Si la respuesta es `s`, se solicita la cantidad de bolsas incluidas en la compra.

Finalmente, la aplicación calcula y muestra el detalle de los impuestos y el valor total a pagar.

## Ejemplo de ejecución

Un ejemplo de cálculo utilizando un producto de $50.000 con IVA del 19% y sin bolsas plásticas es:

```text
========================================
   CALCULADORA DE IMPUESTOS DE VENTA
========================================
1. Calcular impuestos de una compra
2. Salir
Seleccione una opcion: 1

========================================
      CALCULADORA DE IMPUESTOS
========================================
Ingrese el precio del producto: 50000

Seleccione la categoria del producto:
1. IVA 19%
2. IVA 5%
3. Exento
4. Excluido
5. Impuesto Nacional al Consumo (INC)
6. Impuesto a licores
Seleccione una opcion: 1

¿La compra incluye bolsas plasticas? (s/n): n
```

El sistema realiza el cálculo correspondiente y muestra el detalle de la compra junto con el total a pagar.

---

# Ejecución de la interfaz gráfica

La aplicación cuenta con una interfaz gráfica desarrollada utilizando Kivy.

Para ejecutar la interfaz gráfica se requiere tener Python instalado y las dependencias del proyecto configuradas.

Desde la carpeta raíz del proyecto:

```text
calculadora_impuestos/
```

se debe ejecutar:

```bash
python src/view/gui/calculadora_gui.py
```

Al ejecutar el comando se abrirá la ventana de la calculadora de impuestos.

## Proceso de cálculo en la GUI

Para realizar un cálculo:

1. Ingresar el precio del producto.
2. Seleccionar una categoría de impuesto.
3. Ingresar la cantidad de bolsas plásticas.
4. Presionar el botón **Calcular**.
5. Revisar el detalle del cálculo y el total a pagar.

Si los datos ingresados no son válidos, la aplicación mostrará una ventana emergente con información sobre el error y la forma de solucionarlo.

---

# Código limpio

El proyecto busca aplicar buenas prácticas de código limpio para facilitar la lectura, mantenimiento y modificación del código.

Entre las prácticas utilizadas se encuentran:

* Utilizar nombres descriptivos para variables, funciones y clases.
* Separar la lógica de negocio de la interfaz de usuario.
* Dividir las responsabilidades en diferentes métodos.
* Utilizar constantes para valores que no cambian.
* Utilizar excepciones personalizadas para errores específicos.
* Utilizar comentarios y docstrings cuando son necesarios.
* Evitar repetir lógica innecesariamente.
* Mantener una estructura organizada de archivos.
* Mantener las pruebas unitarias independientes de la interfaz gráfica.

La lógica de negocio se encuentra separada de las interfaces de usuario, permitiendo que las funciones de cálculo puedan ser probadas independientemente mediante las pruebas unitarias.

---

# Ejecución y dependencias

Para ejecutar el proyecto se requiere:

* Python 3.
* Kivy para la interfaz gráfica.

Las dependencias necesarias deben estar instaladas en el entorno de Python utilizado para ejecutar el proyecto.

Para instalar Kivy se puede utilizar:

```bash
pip install kivy
```

Una vez instaladas las dependencias, se puede ejecutar la interfaz gráfica mediante:

```bash
python src/view/gui/calculadora_gui.py
```

La interfaz de consola puede ejecutarse mediante:

```bash
python src/view/console/consola_calculadora.py
```

---