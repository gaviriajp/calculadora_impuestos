import sys
import unittest

sys.path.append(".")
sys.path.append("src")

from model.calculo_impuesto import CalculoImpuesto
from controller.calculos_controller import CalculosController


class TestCalculosBD(unittest.TestCase):
    """
    Suite de pruebas unitarias para la persistencia con PostgreSQL.
    Cumple con:
    1. Test Fixtures (setUpClass) para preparar el entorno de base de datos.
    2. Al menos un caso normal y uno de error por cada una de las 4 funcionalidades:
       - Crear tabla
       - Borrar tabla
       - Insertar (INSERT INTO)
       - Consultar (SELECT)
    3. Más de 5 casos de prueba dedicados a insertar y buscar.
    """

    @classmethod
    def setUpClass(cls):
        """
        Test Fixture: Se ejecuta al inicio para garantizar una base de datos limpia
        borrando y creando la tabla calculos.
        """
        CalculosController.borrar_tabla()
        CalculosController.crear_tabla()

    # =========================================================================
    # FUNCIONALIDAD 1: CREAR LAS TABLAS
    # =========================================================================

    def test_01_crear_tabla_caso_normal(self):
        """Caso normal: crear_tabla asegura que la tabla calculos existe y es consultable."""
        CalculosController.crear_tabla()
        cursor = CalculosController.obtener_cursor()
        cursor.execute("SELECT 1 FROM calculos LIMIT 1;")
        # Si la consulta no lanza excepcion, la tabla existe correctamente
        self.assertIsNotNone(cursor)
        cursor.close()
        cursor.connection.close()

    def test_02_crear_tabla_caso_error(self):
        """Caso de error: intentar crear una tabla con sintaxis SQL invalida debe fallar."""
        cursor = CalculosController.obtener_cursor()
        with self.assertRaises(Exception):
            cursor.execute("CREATE TABLE tabla_invalida (id INT TIPO_INVALIDO);")
        cursor.connection.rollback()
        cursor.close()
        cursor.connection.close()

    # =========================================================================
    # FUNCIONALIDAD 2: BORRAR LAS TABLAS
    # =========================================================================

    def test_03_borrar_tabla_caso_normal(self):
        """Caso normal: borrar una tabla existente elimina la tabla correctamente."""
        cursor = CalculosController.obtener_cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS calculos_temp (id INT);")
        cursor.connection.commit()
        cursor.execute("DROP TABLE IF EXISTS calculos_temp;")
        cursor.connection.commit()

        # Al consultar una tabla borrada debe dispararse una excepcion
        with self.assertRaises(Exception):
            cursor.execute("SELECT * FROM calculos_temp;")
        cursor.connection.rollback()
        cursor.close()
        cursor.connection.close()

    def test_04_borrar_tabla_caso_error(self):
        """Caso de error: intentar hacer DROP directo sin IF EXISTS de tabla inexistente debe fallar."""
        cursor = CalculosController.obtener_cursor()
        with self.assertRaises(Exception):
            cursor.execute("DROP TABLE tabla_inexistente_para_prueba;")
        cursor.connection.rollback()
        cursor.close()
        cursor.connection.close()

    # =========================================================================
    # FUNCIONALIDAD 3: INSERTAR EN LA DB (INSERT INTO)
    # =========================================================================

    def test_05_insertar_caso_normal_iva19(self):
        """Caso normal 1: Insertar un calculo valido con IVA 19%."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-101",
            precio_base=100000.0,
            nombre_impuesto="IVA 19%",
            valor_impuesto=19000.0,
            cantidad_bolsas=0,
            valor_bolsas=0.0,
            total=119000.0,
        )
        CalculosController.insertar(calculo)
        recuperado = CalculosController.buscar_calculo("CALC-101")
        self.assertIsNotNone(recuperado)
        self.assertTrue(recuperado.is_equal(calculo))

    def test_06_insertar_caso_normal_con_bolsas(self):
        """Caso normal 2: Insertar un calculo valido con INC y bolsas plasticas."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-102",
            precio_base=50000.0,
            nombre_impuesto="Impuesto Nacional al Consumo",
            valor_impuesto=4000.0,
            cantidad_bolsas=3,
            valor_bolsas=219.0,
            total=54219.0,
        )
        CalculosController.insertar(calculo)
        recuperado = CalculosController.buscar_por_id("CALC-102")
        self.assertIsNotNone(recuperado)
        self.assertTrue(recuperado.is_equal(calculo))

    def test_07_insertar_caso_normal_exento(self):
        """Caso normal 3: Insertar un calculo valido con producto exento."""
        calculo = CalculoImpuesto(
            id_calculo="CALC-103",
            precio_base=30000.0,
            nombre_impuesto="Exento",
            valor_impuesto=0.0,
            cantidad_bolsas=1,
            valor_bolsas=73.0,
            total=30073.0,
        )
        CalculosController.insertar(calculo)
        recuperado = CalculosController.buscar_calculo("CALC-103")
        self.assertIsNotNone(recuperado)
        self.assertTrue(recuperado.is_equal(calculo))

    def test_08_insertar_caso_error_clave_duplicada(self):
        """Caso de error 1 (Insertar): Insertar registro con primary key duplicada debe fallar."""
        calculo_duplicado = CalculoImpuesto(
            id_calculo="CALC-101",  # Ya existe en test_05
            precio_base=80000.0,
            nombre_impuesto="IVA 5%",
            valor_impuesto=4000.0,
            cantidad_bolsas=0,
            valor_bolsas=0.0,
            total=84000.0,
        )
        with self.assertRaises(Exception):
            CalculosController.insertar(calculo_duplicado)

    def test_09_insertar_caso_error_objeto_nulo(self):
        """Caso de error 2 (Insertar): Insertar None debe disparar ValueError."""
        with self.assertRaises(ValueError):
            CalculosController.insertar(None)

    # =========================================================================
    # FUNCIONALIDAD 4: CONSULTAR EN LA DB (SELECT)
    # =========================================================================

    def test_10_consultar_caso_normal(self):
        """Caso normal (Consultar): Buscar un registro existente retorna la instancia CalculoImpuesto."""
        recuperado = CalculosController.buscar_calculo("CALC-101")
        self.assertIsNotNone(recuperado)
        self.assertEqual(recuperado.id_calculo, "CALC-101")
        self.assertEqual(recuperado.nombre_impuesto, "IVA 19%")

    def test_11_consultar_caso_error_inexistente(self):
        """Caso de error (Consultar): Buscar un ID inexistente debe retornar None."""
        resultado = CalculosController.buscar_calculo("ID-TOTALMENTE-INEXISTENTE-999")
        self.assertIsNone(resultado)


if __name__ == "__main__":
    unittest.main()
