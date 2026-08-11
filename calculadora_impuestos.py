# calculadora_impuestos.py
#
# Calculadora de Impuestos de Venta
#
# Universidad de Medellin
# Lenguajes de Programacion y Codigo Limpio


# ============================================================
# CONSTANTES
# ============================================================

TARIFA_IVA_19 = 0.19
TARIFA_IVA_5 = 0.05
TARIFA_INC = 0.08
TARIFA_LICOR = 0.25

VALOR_BOLSA = 50

PRECIO_MINIMO = 1
PRECIO_MAXIMO = 1_000_000_000


# ============================================================
# EXCEPCIONES
# ============================================================

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


# ============================================================
# PROCESAMIENTO DEL PRECIO
# ============================================================

def procesar_precio(texto):
    """
    Valida y convierte el precio ingresado como texto
    a un numero.

    Valida:
    - Campo vacio.
    - Caracteres no numericos.
    - Precio menor o igual a cero.
    - Precio superior al limite permitido.
    """

    # CP-09: precio vacio
    if texto is None or texto.strip() == "":
        raise PrecioInvalidoError(
            "El precio es obligatorio, no puede quedar vacio."
        )

    texto_limpio = texto.strip().replace(",", "")

    # CP-08: letras en el precio
    try:
        precio = float(texto_limpio)
    except ValueError:
        raise PrecioInvalidoError(
            "El precio debe ser un valor numerico."
        )

    # CP-07: precio negativo o cero
    if precio <= 0:
        raise PrecioInvalidoError(
            "El precio debe ser mayor que cero."
        )

    # CP-04: limite superior
    if precio < PRECIO_MINIMO or precio > PRECIO_MAXIMO:
        raise PrecioInvalidoError(
            "El precio debe estar entre "
            + str(PRECIO_MINIMO)
            + " y "
            + str(PRECIO_MAXIMO)
            + "."
        )

    return precio


# ============================================================
# CALCULO DE IMPUESTOS
# ============================================================

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

    El producto puede tener una sola categoria de impuesto
    principal:

    - IVA 19%
    - IVA 5%
    - Exento
    - Excluido
    - INC
    - Licor

    El impuesto de bolsas plasticas puede aplicarse
    adicionalmente.
    """

    # --------------------------------------------------------
    # CP-10:
    # No se permite IVA 5% e IVA 19% simultaneamente.
    # --------------------------------------------------------

    if iva19 and iva5:
        raise ImpuestoInvalidoError(
            "No se puede seleccionar IVA 5% e IVA 19% "
            "al mismo tiempo."
        )

    # --------------------------------------------------------
    # Contar las categorias principales seleccionadas.
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # CP-05:
    # No se selecciono ningun impuesto.
    # --------------------------------------------------------

    if cantidad_seleccionados == 0:
        raise ImpuestoInvalidoError(
            "Debe seleccionar al menos un tipo de impuesto "
            "(o Exento/Excluido)."
        )

    # --------------------------------------------------------
    # Solo puede existir una categoria principal.
    # --------------------------------------------------------

    if cantidad_seleccionados > 1:
        raise ImpuestoInvalidoError(
            "Solo se puede seleccionar una categoria "
            "de impuesto principal por producto."
        )

    # --------------------------------------------------------
    # Calcular impuesto principal.
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Impuesto de bolsas plasticas.
    #
    # Este impuesto es independiente del impuesto principal.
    # Por eso puede combinarse con IVA, INC, Exento o Excluido.
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    total = round(
        precio + valor_impuesto + valor_bolsas,
        2
    )

    # --------------------------------------------------------
    # Resultado
    # --------------------------------------------------------

    resultado = {
        "precio_base": precio,
        "nombre_impuesto": nombre_impuesto,
        "valor_impuesto": valor_impuesto,
        "valor_bolsas": valor_bolsas,
        "total": total
    }

    return resultado
# ============================================================
# INTERFAZ DE CONSOLA
# ============================================================

def mostrar_resultado(resultado):
    print("\n========================================")
    print("       DETALLE DE LA COMPRA")
    print("========================================")

    print("Precio base:       $%.2f" % resultado["precio_base"])
    print(
        (resultado["nombre_impuesto"] + ":").ljust(20)
        + "$%.2f" % resultado["valor_impuesto"]
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
    respuesta = input(pregunta + " (s/n): ").strip().lower()
    return respuesta == "s"


def ejecutar_calculo():

    print("\n========================================")
    print("      CALCULADORA DE IMPUESTOS")
    print("========================================")

    # --------------------------------------------------------
    # Precio
    # --------------------------------------------------------

    texto_precio = input(
        "Ingrese el precio del producto: "
    )

    try:
        precio = procesar_precio(texto_precio)

    except PrecioInvalidoError as error:
        print("\nError:", error)
        return

    # --------------------------------------------------------
    # Categoria del impuesto
    # --------------------------------------------------------

    print("\nSeleccione la categoria del producto:")
    print("1. IVA 19%")
    print("2. IVA 5%")
    print("3. Exento")
    print("4. Excluido")
    print("5. Impuesto Nacional al Consumo (INC)")
    print("6. Impuesto a licores")

    categoria = input("Seleccione una opcion: ").strip()

    iva19 = categoria == "1"
    iva5 = categoria == "2"
    exento = categoria == "3"
    excluido = categoria == "4"
    inc = categoria == "5"
    licor = categoria == "6"

    # --------------------------------------------------------
    # Validar opcion de categoria
    # --------------------------------------------------------

    if categoria not in ("1", "2", "3", "4", "5", "6"):
        print("\nError: debe seleccionar una categoria valida.")
        return

    # --------------------------------------------------------
    # Bolsas plasticas
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Calcular
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Mostrar resultado
    # --------------------------------------------------------

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


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    menu_principal()