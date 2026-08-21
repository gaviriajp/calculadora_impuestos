TARIFA_IVA_GENERAL = 0.19
TARIFA_IVA_REDUCIDO = 0.05
TARIFA_INC = 0.08
TARIFA_LICOR = 0.25

VALOR_BOLSA = 73

PRECIO_MINIMO = 1
PRECIO_MAXIMO = 1_000_000_000


class PrecioInvalidoError(Exception):
    pass


class ImpuestoInvalidoError(Exception):
    pass


def procesar_precio(texto):
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
    impuesto_licor=False,
    bolsas=False,
    cantidad_bolsas=0
):
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
        impuesto_licor
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
            precio * TARIFA_IVA_GENERAL,
            2
        )

    elif iva5:
        nombre_impuesto = "IVA 5%"
        valor_impuesto = round(
            precio * TARIFA_IVA_REDUCIDO,
            2
        )

    elif inc:
        nombre_impuesto = "Impuesto Nacional al Consumo"
        valor_impuesto = round(
            precio * TARIFA_INC,
            2
        )

    elif impuesto_licor:
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