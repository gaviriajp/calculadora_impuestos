# Calculadora de Impuestos de Venta

Aplicación desarrollada en Python para calcular el valor total a pagar por una compra, discriminando los impuestos aplicables según la categoría del producto.

## Integrantes

* **Juan Pablo Gaviria Franco**
* **Juan Esteban Correa Guzman**

## Descripción del proyecto

La aplicación permite ingresar el precio de un producto, seleccionar la categoría de impuesto correspondiente y calcular el valor del impuesto y el total a pagar.

El sistema también permite agregar el impuesto correspondiente a las bolsas plásticas cuando la compra las incluye.

El proyecto fue desarrollado como parte de la asignatura **Lenguajes de Programación y Código Limpio** de la **Universidad de Medellín**.

## Funcionalidades

La aplicación permite trabajar con las siguientes categorías:

* **IVA 19%**
* **IVA 5%**
* **Exento**
* **Excluido**
* **Impuesto Nacional al Consumo (INC)**
* **Impuesto a licores**
* **Impuesto de bolsas plásticas**

El sistema discrimina los impuestos y muestra el total final de la compra.

## Entradas

El programa recibe los siguientes datos:

1. **Precio del producto**

   * Debe ser un valor numérico.
   * Debe ser mayor que cero.
   * El sistema maneja un límite máximo de precio establecido en el código.

2. **Categoría del impuesto**

   * IVA 19%
   * IVA 5%
   * Exento
   * Excluido
   * Impuesto Nacional al Consumo
   * Impuesto a licores

3. **Bolsas plásticas**

   * El usuario indica si la compra incluye bolsas.
   * Si incluye bolsas, debe ingresar la cantidad.

## Proceso

El funcionamiento general de la aplicación es:

1. El usuario inicia la aplicación.
2. Selecciona la opción para calcular los impuestos.
3. Ingresa el precio del producto.
4. Selecciona la categoría de impuesto.
5. Indica si la compra incluye bolsas plásticas.
6. Si corresponde, ingresa la cantidad de bolsas.
7. El sistema valida los datos ingresados.
8. Se calcula el impuesto correspondiente.
9. Se calcula el impuesto de las bolsas, cuando aplica.
10. Se suman el precio base y los impuestos.
11. El sistema muestra el detalle y el total a pagar.

## Salidas

La aplicación muestra:

* Precio base del producto.
* Nombre del impuesto aplicado.
* Valor del impuesto.
* Valor del impuesto de bolsas plásticas, cuando corresponde.
* **Total a pagar.**

Ejemplo:

```text
========================================
       DETALLE DE LA COMPRA
========================================
Precio base:       $50000.00
IVA 19%:            $9500.00
----------------------------------------
TOTAL A PAGAR:     $59500.00
========================================
```

## Validaciones y manejo de errores

El sistema valida diferentes situaciones para evitar cálculos incorrectos.

Entre ellas:

* Precio vacío.
* Precio con letras o caracteres no numéricos.
* Precio negativo.
* Precio igual a cero.
* Precio superior al límite establecido.
* No seleccionar una categoría de impuesto.
* Seleccionar simultáneamente IVA 5% e IVA 19%.
* Ingresar una cantidad inválida de bolsas.

Cuando se presenta una situación inválida, el programa muestra un mensaje indicando el problema.

## Ejecución de la aplicación

Para ejecutar la aplicación desde la terminal, ubicarse en la carpeta del proyecto y ejecutar:

```bash
python calculadora_impuestos.py
```

La aplicación mostrará el menú principal:

```text
===== CALCULADORA DE IMPUESTOS DE VENTA =====

1. Calcular impuestos de una compra
2. Salir
```


