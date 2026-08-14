import sys
sys.path.append("src")

import unittest
from model import calculadora_impuestos as calc


class CalculadoraImpuestosTest(unittest.TestCase):

    # ========================================================
    # CASOS NORMALES
    # ========================================================

    def test_cp01_iva_19(self):
        precio = calc.procesar_precio("100000")

        resultado = calc.calcular_impuestos(
            precio,
            iva19=True
        )

        esperado = 119000.0

        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )

    def test_cp02_inc(self):
        precio = calc.procesar_precio("40000")

        resultado = calc.calcular_impuestos(
            precio,
            inc=True
        )

        esperado = 43200.0

        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )

    def test_cp03_iva_19_con_bolsas(self):
        precio = calc.procesar_precio("100000")

        resultado = calc.calcular_impuestos(
            precio,
            iva19=True,
            bolsas=True,
            cantidad_bolsas=2
        )

        esperado = 119146.0

        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )

    # ========================================================
    # CASOS EXCEPCIONALES
    # ========================================================

    def test_cp04_precio_muy_alto(self):
        precio = calc.procesar_precio(
            "999999999"
        )

        resultado = calc.calcular_impuestos(
            precio,
            iva19=True
        )

        esperado = 1189999998.81

        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )

    def test_cp05_ningun_impuesto(self):
        precio = calc.procesar_precio(
            "50000"
        )

        with self.assertRaises(
            calc.ImpuestoInvalidoError
        ):
            calc.calcular_impuestos(
                precio
            )

    def test_cp06_excluido_con_bolsas(self):
        precio = calc.procesar_precio(
            "40000"
        )

        resultado = calc.calcular_impuestos(
            precio,
            excluido=True,
            bolsas=True,
            cantidad_bolsas=1
        )

        esperado = 40073.0

        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )

    # ========================================================
    # CASOS DE ERROR
    # ========================================================

    def test_cp07_precio_negativo(self):
        precio = "-50000"

        self.assertRaises(
            calc.PrecioInvalidoError,
            calc.procesar_precio,
            precio
        )

    def test_cp08_letras_en_precio(self):
        precio = "abc"

        with self.assertRaises(
            calc.PrecioInvalidoError
        ):
            calc.procesar_precio(
                precio
            )

    def test_cp09_precio_vacio(self):
        precio = ""

        with self.assertRaises(
            calc.PrecioInvalidoError
        ):
            calc.procesar_precio(
                precio
            )

    def test_cp10_doble_iva(self):
        precio = calc.procesar_precio(
            "100000"
        )

        with self.assertRaises(
            calc.ImpuestoInvalidoError
        ):
            calc.calcular_impuestos(
                precio,
                iva19=True,
                iva5=True
            )


# ============================================================
# INFORMACION DE LAS PRUEBAS
# ============================================================

def ejecutar_pruebas():

    print()
    print("=" * 60)
    print("       PRUEBAS DE LA CALCULADORA DE IMPUESTOS")
    print("=" * 60)
    print()

    nombres = [
        ("CP-01", "IVA 19%"),
        ("CP-02", "INC 8%"),
        ("CP-03", "IVA 19% + bolsas"),
        ("CP-04", "Precio muy alto"),
        ("CP-05", "Ningun impuesto"),
        ("CP-06", "Excluido + bolsas"),
        ("CP-07", "Precio negativo"),
        ("CP-08", "Letras en precio"),
        ("CP-09", "Precio vacio"),
        ("CP-10", "Doble IVA")
    ]

    suite = unittest.TestLoader().loadTestsFromTestCase(
        CalculadoraImpuestosTest
    )

    resultado = unittest.TextTestRunner(
        verbosity=0
    ).run(suite)

    total = resultado.testsRun
    fallidas = len(resultado.failures)
    errores = len(resultado.errors)
    exitosas = total - fallidas - errores

    print("RESULTADO DE CADA CASO")
    print("-" * 60)

    for codigo, nombre in nombres:

        fallo = False

        for prueba, mensaje in resultado.failures:
            if codigo.lower() in str(prueba).lower():
                fallo = True

        for prueba, mensaje in resultado.errors:
            if codigo.lower() in str(prueba).lower():
                fallo = True

        if fallo:
            estado = "[FALLÓ]"
        else:
            estado = "[PASÓ]"

        print(
            f"{codigo:<8} - {nombre:<30} {estado}"
        )

    print()
    print("=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)

    print(f"Pruebas ejecutadas: {total}")
    print(f"Pruebas exitosas:   {exitosas}")
    print(f"Pruebas fallidas:   {fallidas}")
    print(f"Errores:            {errores}")

    print()

    if fallidas == 0 and errores == 0:
        print("TODAS LAS PRUEBAS PASARON")
    else:
        print("HAY PRUEBAS QUE NO PASARON")

    print("=" * 60)


# ============================================================
# EJECUTAR PRUEBAS
# ============================================================

if __name__ == "__main__":
    ejecutar_pruebas()