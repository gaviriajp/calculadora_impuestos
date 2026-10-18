import os
import sys

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)

from model import calculadora_impuestos as calc


OPCION_IVA_19 = "1"
OPCION_IVA_5 = "2"
OPCION_EXENTO = "3"
OPCION_EXCLUIDO = "4"
OPCION_INC = "5"
OPCION_LICOR = "6"

OPCIONES_VALIDAS = (
    OPCION_IVA_19,
    OPCION_IVA_5,
    OPCION_EXENTO,
    OPCION_EXCLUIDO,
    OPCION_INC,
    OPCION_LICOR
)


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
    while True:
        respuesta = input(
            pregunta + " (s/n): "
        ).strip().lower()

        if respuesta == "s":
            return True

        if respuesta == "n":
            return False

        print(
            "Error: debe responder 's' o 'n'."
        )


def ejecutar_calculo():
    print("\n========================================")
    print("      CALCULADORA DE IMPUESTOS")
    print("========================================")

    texto_precio = input(
        "Ingrese el precio del producto: "
    )

    try:
        precio = calc.validar_y_convertir_precio(
            texto_precio
        )

    except calc.PrecioInvalidoError as error:
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

    if categoria not in OPCIONES_VALIDAS:
        print(
            "\nError: debe seleccionar "
            "una categoria valida."
        )
        return

    iva19 = categoria == OPCION_IVA_19
    iva5 = categoria == OPCION_IVA_5
    exento = categoria == OPCION_EXENTO
    excluido = categoria == OPCION_EXCLUIDO
    inc = categoria == OPCION_INC
    licor = categoria == OPCION_LICOR

    incluye_bolsas = pedir_si_no(
        "\n¿La compra incluye bolsas plasticas?"
    )

    cantidad_bolsas = 0

    if incluye_bolsas:
        texto_cantidad = input(
            "Ingrese la cantidad de bolsas: "
        ).strip()

        try:
            cantidad_bolsas = int(
                texto_cantidad
            )

        except ValueError:
            print(
                "\nError: la cantidad de bolsas "
                "debe ser un numero entero."
            )
            return

    try:
        resultado = calc.calcular_impuestos(
    precio,
    iva19=iva19,
    iva5=iva5,
    exento=exento,
    excluido=excluido,
    inc=inc,
    impuesto_licor=licor,
    bolsas=incluye_bolsas,
    cantidad_bolsas=cantidad_bolsas
)

    except calc.ImpuestoInvalidoError as error:
        print("\nError:", error)
        return

    mostrar_resultado(resultado)

    guardar = pedir_si_no("¿Desea guardar este cálculo en la base de datos?")
    if guardar:
        id_calculo = input("Ingrese un identificador para el cálculo (ej. CALC-001): ").strip()
        while not id_calculo:
            print("El identificador no puede estar vacío.")
            id_calculo = input("Ingrese un identificador: ").strip()

        try:
            from model.calculo_impuesto import CalculoImpuesto
            from controller.calculos_controller import CalculosController

            nuevo_calculo = CalculoImpuesto(
                id_calculo=id_calculo,
                precio_base=resultado["precio_base"],
                nombre_impuesto=resultado["nombre_impuesto"],
                valor_impuesto=resultado["valor_impuesto"],
                cantidad_bolsas=cantidad_bolsas,
                valor_bolsas=resultado["valor_bolsas"],
                total=resultado["total"],
            )
            CalculosController.insertar(nuevo_calculo)
            print(f"\n¡Cálculo '{id_calculo}' guardado exitosamente en la base de datos!")
        except Exception as error:
            print(f"\nError al guardar en la base de datos: {error}")


def ejecutar_busqueda():
    print("\n========================================")
    print("   BUSCAR CÁLCULO EN LA BASE DE DATOS")
    print("========================================")
    id_busqueda = input("Ingrese el ID del cálculo a buscar: ").strip()
    if not id_busqueda:
        print("\nError: el identificador no puede estar vacío.")
        return

    try:
        from controller.calculos_controller import CalculosController

        calculo = CalculosController.buscar_calculo(id_busqueda)
        if calculo is None:
            print(f"\nNo se encontró ningún cálculo con el ID '{id_busqueda}'.")
            return

        resultado = {
            "precio_base": calculo.precio_base,
            "nombre_impuesto": calculo.nombre_impuesto,
            "valor_impuesto": calculo.valor_impuesto,
            "valor_bolsas": calculo.valor_bolsas,
            "total": calculo.total,
        }
        print(f"\n--- INFORMACIÓN DEL REGISTRO [{calculo.id_calculo}] ---")
        mostrar_resultado(resultado)
    except Exception as error:
        print(f"\nError al consultar la base de datos: {error}")


def menu_principal():
    while True:
        print("\n========================================")
        print("   CALCULADORA DE IMPUESTOS DE VENTA")
        print("========================================")
        print("1. Calcular impuestos de una compra")
        print("2. Buscar cálculo en la base de datos")
        print("3. Salir")

        opcion = input(
            "Seleccione una opcion: "
        ).strip()

        if opcion == "1":
            ejecutar_calculo()

        elif opcion == "2":
            ejecutar_busqueda()

        elif opcion == "3":
            print("\nHasta luego.")
            break

        else:
            print(
                "\nOpcion invalida. "
                "Seleccione 1, 2 o 3."
            )


if __name__ == "__main__":
    menu_principal()