# main.py

import calculadora_impuestos as calc


def mostrar_resultado(resultado):

    print("\n----- DETALLE DE LA COMPRA -----")

    print(
        "Precio base:            $%.2f"
        % resultado["precio_base"]
    )

    print(
        (resultado["nombre_impuesto"] + ":").ljust(25)
        + "$%.2f"
        % resultado["valor_impuesto"]
    )

    if resultado["valor_bolsas"] > 0:

        print(
            "Impuesto bolsas:        $%.2f"
            % resultado["valor_bolsas"]
        )

    print("-" * 33)

    print(
        "TOTAL A PAGAR:          $%.2f"
        % resultado["total"]
    )

    print("---------------------------------\n")


def pedir_si_no(pregunta):

    respuesta = input(
        pregunta + " (s/n): "
    ).strip().lower()

    return respuesta == "s"


def ejecutar_calculo():

    texto_precio = input(
        "Ingrese el precio del producto: "
    )

    try:

        precio = calc.procesar_precio(
            texto_precio
        )

    except calc.PrecioInvalidoError as error:

        print("Error: " + str(error))
        return

    print(
        "\nSeleccione la categoria de impuesto "
        "del producto:"
    )

    print("1. IVA 19%")
    print("2. IVA 5%")
    print("3. Exento")
    print("4. Excluido")
    print("5. Impuesto Nacional al Consumo (INC)")
    print("6. Impuesto a licores")

    categoria = input("Opcion: ").strip()

    iva19 = categoria == "1"
    iva5 = categoria == "2"
    exento = categoria == "3"
    excluido = categoria == "4"
    inc = categoria == "5"
    licor = categoria == "6"

    if categoria not in ["1", "2", "3", "4", "5", "6"]:

        print("Error: categoria de impuesto invalida.")
        return

    usa_bolsas = pedir_si_no(
        "Incluye bolsas plasticas?"
    )

    cantidad_bolsas = 0

    if usa_bolsas:

        texto_cantidad = input(
            "Cantidad de bolsas: "
        ).strip()

        try:

            cantidad_bolsas = int(
                texto_cantidad
            )

        except ValueError:

            print(
                "Error: la cantidad de bolsas "
                "debe ser un numero entero."
            )

            return

    try:

        resultado = calc.calcular_impuestos(
            precio,
            iva19,
            iva5,
            exento,
            excluido,
            inc,
            licor,
            usa_bolsas,
            cantidad_bolsas
        )

    except calc.ImpuestoInvalidoError as error:

        print("Error: " + str(error))
        return

    mostrar_resultado(resultado)


def menu_principal():

    while True:

        print(
            "\n===== CALCULADORA DE IMPUESTOS DE VENTA ====="
        )

        print("1. Calcular impuestos de una compra")
        print("2. Salir")

        opcion = input(
            "Seleccione una opcion: "
        ).strip()

        if opcion == "1":

            ejecutar_calculo()

        elif opcion == "2":

            print("Hasta luego.")
            break

        else:

            print(
                "Opcion invalida, intente de nuevo."
            )


if __name__ == "__main__":
    menu_principal()
    