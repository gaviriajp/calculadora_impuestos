# test_calculadora.py

# Todas las pruebas unitarias importan unittest
import unittest

# Importar el modulo que contiene la funcionalidad
import calculadora_impuestos as calc


class CalculadoraImpuestosTest(unittest.TestCase):

    # ========================================================
    # CASOS NORMALES
    # ========================================================

    # CP-01
    # Calculo de IVA del 19%
    def test_cp01_iva_19(self):

        # Datos de entrada
        precio = calc.procesar_precio("100000")

        # Proceso
        resultado = calc.calcular_impuestos(
            precio,
            iva19=True
        )

        # Datos de salida esperados
        esperado = 119000.0

        # Verificacion
        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )


    # CP-02
    # Producto con Impuesto Nacional al Consumo
    def test_cp02_inc(self):

        # Datos de entrada
        precio = calc.procesar_precio("40000")

        # Proceso
        resultado = calc.calcular_impuestos(
            precio,
            inc=True
        )

        # Datos de salida esperados
        esperado = 43200.0

        # Verificacion
        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )


    # CP-03
    # IVA 19% + bolsas plasticas
    def test_cp03_iva_19_con_bolsas(self):

        # Datos de entrada
        precio = calc.procesar_precio("100000")

        # Proceso
        resultado = calc.calcular_impuestos(
            precio,
            iva19=True,
            bolsas=True,
            cantidad_bolsas=2
        )

        # IVA = 19000
        # Bolsas = 2 * 50 = 100
        # Total = 119100

        # Datos de salida esperados
        esperado = 119100.0

        # Verificacion
        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )


    # ========================================================
    # CASOS EXCEPCIONALES
    # ========================================================

    # CP-04
    # Precio muy alto
    def test_cp04_precio_muy_alto(self):

        # Datos de entrada
        precio = calc.procesar_precio(
            "999999999"
        )

        # Proceso
        resultado = calc.calcular_impuestos(
            precio,
            iva19=True
        )

        # Datos de salida esperados
        esperado = 1189999998.81

        # Verificacion
        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )


    # CP-05
    # No seleccionar ningun impuesto
    def test_cp05_ningun_impuesto(self):

        # Datos de entrada
        precio = calc.procesar_precio(
            "50000"
        )

        # Verificar que se genere la excepcion
        with self.assertRaises(
            calc.ImpuestoInvalidoError
        ):

            calc.calcular_impuestos(
                precio
            )


    # CP-06
    # Excluido + bolsas plasticas
    def test_cp06_excluido_con_bolsas(self):

        # Datos de entrada
        precio = calc.procesar_precio(
            "40000"
        )

        # Proceso
        resultado = calc.calcular_impuestos(
            precio,
            excluido=True,
            bolsas=True,
            cantidad_bolsas=1
        )

        # Producto excluido no genera impuesto
        # 1 bolsa = 50
        # Total = 40050

        # Datos de salida esperados
        esperado = 40050.0

        # Verificacion
        self.assertAlmostEqual(
            esperado,
            resultado["total"],
            2
        )


    # ========================================================
    # CASOS DE ERROR
    # ========================================================

    # CP-07
    # Precio negativo
    def test_cp07_precio_negativo(self):

        # Datos de entrada
        precio = "-50000"

        # Verificar excepcion
        self.assertRaises(
            calc.PrecioInvalidoError,
            calc.procesar_precio,
            precio
        )


    # CP-08
    # Letras en el campo de precio
    def test_cp08_letras_en_precio(self):

        # Datos de entrada
        precio = "abc"

        # Verificar excepcion
        with self.assertRaises(
            calc.PrecioInvalidoError
        ):

            calc.procesar_precio(
                precio
            )


    # CP-09
    # Campo de precio vacio
    def test_cp09_precio_vacio(self):

        # Datos de entrada
        precio = ""

        # Verificar excepcion
        with self.assertRaises(
            calc.PrecioInvalidoError
        ):

            calc.procesar_precio(
                precio
            )


    # CP-10
    # IVA 5% e IVA 19% simultaneamente
    def test_cp10_doble_iva(self):

        # Datos de entrada
        precio = calc.procesar_precio(
            "100000"
        )

        # Verificar excepcion
        with self.assertRaises(
            calc.ImpuestoInvalidoError
        ):

            calc.calcular_impuestos(
                precio,
                iva19=True,
                iva5=True
            )


# ============================================================
# EJECUCION DE LAS PRUEBAS
# ============================================================

if __name__ == "__main__":
    unittest.main()