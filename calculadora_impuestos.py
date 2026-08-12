TARIFA_IVA_19 = 0.19
TARIFA_IVA_5 = 0.05
TARIFA_INC = 0.08
TARIFA_LICOR = 0.25

VALOR_BOLSA = 73

PRECIO_MINIMO = 1
PRECIO_MAXIMO = 1_000_000_000


class PrecioInvalidoError(Exception):
    """
    Se lanza cuando el precio ingresado
    no cumple las validaciones.
    """
    pass


class ImpuestoInvalidoError(Exception):
    """
    Se lanza cuando la seleccion de impuestos
    no cumple las reglas del sistema.
    """
    pass


def procesar_precio(texto):
    """
    Valida y convierte el precio ingresado como texto
    a un numero.
    """

    if texto is None or texto.strip() == "":
        raise PrecioInvalidoError(
            "El precio es obligatorio, no puede quedar vacio."
        )

    texto_limpio = texto.strip().replace(",", "")

    try:
        precio = float(texto_limpio)
    except ValueError:
        raise PrecioInvalidoError(
            "El precio debe ser un valor numerico."
        )

    if precio <= 0:
        raise PrecioInvalidoError(
            "El precio debe ser mayor que cero."
        )

    if precio < PRECIO_MINIMO or precio > PRECIO_MAXIMO:
        raise PrecioInvalidoError(
            "El precio debe estar entre "
            + str(PRECIO_MINIMO)
            + " y "
            + str(PRECIO_MAXIMO)
            + "."
        )

    return precio


def calcular_impuestos(
    precio,
    iva19=False,
    iva5=False,
    exento=False,
    excluido=False,
    inc=False,
    licor=False,
    bolsas=False,
    cantidad_bolsas=0
):
    """
    Calcula los impuestos y el total de una compra.
    """

    if iva19 and iva5:
        raise ImpuestoInvalidoError(
            "No se puede seleccionar IVA 5% e IVA 19% "
            "al mismo tiempo."
        )

    cantidad_seleccionados = 0

    for opcion in (
        iva19,
        iva5,
        exento,
        excluido,
        inc,
        licor
    ):
        if opcion:
            cantidad_seleccionados += 1

    if cantidad_seleccionados == 0:
        raise ImpuestoInvalidoError(
            "Debe seleccionar al menos un tipo de impuesto "
            "(o Exento/Excluido)."
        )

    if cantidad_seleccionados > 1:
        raise ImpuestoInvalidoError(
            "Solo se puede seleccionar una categoria "
            "de impuesto principal por producto."
        )

    if iva19:
        nombre_impuesto = "IVA 19%"
        valor_impuesto = round(
            precio * TARIFA_IVA_19,
            2
        )

    elif iva5:
        nombre_impuesto = "IVA 5%"
        valor_impuesto = round(
            precio * TARIFA_IVA_5,
            2
        )

    elif inc:
        nombre_impuesto = "Impuesto Nacional al Consumo"
        valor_impuesto = round(
            precio * TARIFA_INC,
            2
        )

    elif licor:
        nombre_impuesto = "Impuesto a licores"
        valor_impuesto = round(
            precio * TARIFA_LICOR,
            2
        )

    elif exento:
        nombre_impuesto = "Exento"
        valor_impuesto = 0.0

    else:
        nombre_impuesto = "Excluido"
        valor_impuesto = 0.0

    valor_bolsas = 0.0

    if bolsas:

        if cantidad_bolsas <= 0:
            raise ImpuestoInvalidoError(
                "Debe indicar una cantidad valida "
                "de bolsas plasticas."
            )

        valor_bolsas = round(
            cantidad_bolsas * VALOR_BOLSA,
            2
        )

    total = round(
        precio + valor_impuesto + valor_bolsas,
        2
    )

    resultado = {
        "precio_base": precio,
        "nombre_impuesto": nombre_impuesto,
        "valor_impuesto": valor_impuesto,
        "valor_bolsas": valor_bolsas,
        "total": total
    }

    return resultado


def mostrar_resultado(resultado):

    print("\n========================================")
    print("       DETALLE DE LA COMPRA")
    print("========================================")

    print(
        "Precio base:       $%.2f"
        % resultado["precio_base"]
    )

    print(
        (resultado["nombre_impuesto"] + ":").ljust(20)
        + "$%.2f"
        % resultado["valor_impuesto"]
    )

    if resultado["valor_bolsas"] > 0:
        print(
            "Impuesto bolsas:   $%.2f"
            % resultado["valor_bolsas"]
        )

    print("----------------------------------------")

    print(
        "TOTAL A PAGAR:     $%.2f"
        % resultado["total"]
    )

    print("========================================\n")


def pedir_si_no(pregunta):

    respuesta = input(
        pregunta + " (s/n): "
    ).strip().lower()

    return respuesta == "s"


def ejecutar_calculo():

    print("\n========================================")
    print("      CALCULADORA DE IMPUESTOS")
    print("========================================")

    texto_precio = input(
        "Ingrese el precio del producto: "
    )

    try:
        precio = procesar_precio(texto_precio)

    except PrecioInvalidoError as error:
        print("\nError:", error)
        return

    print("\nSeleccione la categoria del producto:")
    print("1. IVA 19%")
    print("2. IVA 5%")
    print("3. Exento")
    print("4. Excluido")
    print("5. Impuesto Nacional al Consumo (INC)")
    print("6. Impuesto a licores")

    categoria = input(
        "Seleccione una opcion: "
    ).strip()

    iva19 = categoria == "1"
    iva5 = categoria == "2"
    exento = categoria == "3"
    excluido = categoria == "4"
    inc = categoria == "5"
    licor = categoria == "6"

    if categoria not in ("1", "2", "3", "4", "5", "6"):
        print("\nError: debe seleccionar una categoria valida.")
        return

    usa_bolsas = pedir_si_no(
        "\n¿La compra incluye bolsas plasticas?"
    )

    cantidad_bolsas = 0

    if usa_bolsas:

        texto_cantidad = input(
            "Ingrese la cantidad de bolsas: "
        ).strip()

        try:
            cantidad_bolsas = int(texto_cantidad)

        except ValueError:
            print(
                "\nError: la cantidad de bolsas "
                "debe ser un numero entero."
            )
            return

    try:

        resultado = calcular_impuestos(
            precio,
            iva19=iva19,
            iva5=iva5,
            exento=exento,
            excluido=excluido,
            inc=inc,
            licor=licor,
            bolsas=usa_bolsas,
            cantidad_bolsas=cantidad_bolsas
        )

    except ImpuestoInvalidoError as error:
        print("\nError:", error)
        return

    mostrar_resultado(resultado)


def menu_principal():

    while True:

        print("\n========================================")
        print("   CALCULADORA DE IMPUESTOS DE VENTA")
        print("========================================")
        print("1. Calcular impuestos de una compra")
        print("2. Salir")

        opcion = input(
            "Seleccione una opcion: "
        ).strip()

        if opcion == "1":
            ejecutar_calculo()

        elif opcion == "2":
            print("\nHasta luego.")
            break

        else:
            print(
                "\nOpcion invalida. "
                "Seleccione 1 o 2."
            )


if __name__ == "__main__":
    menu_principal()