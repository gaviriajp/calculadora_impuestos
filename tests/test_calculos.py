import sys
import unittest

sys.path.append(".")
sys.path.append("src")

from model.calculo_impuesto import CalculoImpuesto
from controller.calculos_controller import CalculosController


class TestCalculosBD(unittest.TestCase):
    """
    Pruebas unitarias para las operaciones con la base de datos PostgreSQL.
    Incluye Test Fixture (setUpClass) y casos normales y de error para insertar y buscar.
    """

    @classmethod
    def setUpClass(cls):
        """
        Test Fixture: Se ejecuta una sola vez al inicio de la suite de pruebas.
        Limpia y crea las tablas en la base de datos para garantizar un entorno limpio.
        """
        CalculosController.borrar_tabla()
        CalculosController.crear_tabla()

    def test_01_insertar_y_buscar_normal(self):
        """Caso normal 1: Insertar un cálculo de IVA 19% y verificar que se recupere correctamente."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-001",
            precio_base=100000.0,
            nombre_impuesto="IVA 19%",
            valor_impuesto=19000.0,
            cantidad_bolsas=0,
            valor_bolsas=0.0,
            total=119000.0,
        )

        # Inserción en la base de datos
        CalculosController.insertar(calculo)

        # Búsqueda por ID
        calculo_recuperado = CalculosController.buscar_calculo("CALC-001")

        self.assertIsNotNone(calculo_recuperado)
        self.assertTrue(calculo_recuperado.is_equal(calculo))

    def test_02_insertar_y_buscar_con_bolsas(self):
        """Caso normal 2: Insertar un cálculo con INC 8% y bolsas plásticas."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-002",
            precio_base=50000.0,
            nombre_impuesto="Impuesto Nacional al Consumo",
            valor_impuesto=4000.0,
            cantidad_bolsas=3,
            valor_bolsas=219.0,
            total=54219.0,
        )

        CalculosController.insertar(calculo)

        calculo_recuperado = CalculosController.buscar_por_id("CALC-002")

        self.assertIsNotNone(calculo_recuperado)
        self.assertTrue(calculo_recuperado.is_equal(calculo))

    def test_03_insertar_y_buscar_exento(self):
        """Caso normal 3: Insertar un cálculo de producto exento."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-003",
            precio_base=30000.0,
            nombre_impuesto="Exento",
            valor_impuesto=0.0,
            cantidad_bolsas=1,
            valor_bolsas=73.0,
            total=30073.0,
        )

        CalculosController.insertar(calculo)

        calculo_recuperado = CalculosController.buscar_calculo("CALC-003")

        self.assertIsNotNone(calculo_recuperado)
        self.assertTrue(calculo_recuperado.is_equal(calculo))

    def test_04_buscar_error_id_inexistente(self):
        """Caso de error 1: Buscar un ID que no existe en la base de datos debe retornar None."""
        calculo_inexistente = CalculosController.buscar_calculo("ID-TOTALMENTE-INEXISTENTE-999")
        self.assertIsNone(calculo_inexistente)

    def test_05_insertar_error_clave_duplicada(self):
        """Caso de error 2: Intentar insertar un cálculo con un ID ya existente debe fallar por primary key."""
        calculo_duplicado = CalculoImpuesto(
            id_calculo="CALC-001",  # Ya fue insertado en test_01
            precio_base=80000.0,
            nombre_impuesto="IVA 5%",
            valor_impuesto=4000.0,
            cantidad_bolsas=0,
            valor_bolsas=0.0,
            total=84000.0,
        )

        with self.assertRaises(Exception):
            CalculosController.insertar(calculo_duplicado)

    def test_06_insertar_error_objeto_nulo(self):
        """Caso de error 3: Intentar insertar None debe disparar un ValueError."""
        with self.assertRaises(ValueError):
            CalculosController.insertar(None)


if __name__ == "__main__":
    unittest.main()
