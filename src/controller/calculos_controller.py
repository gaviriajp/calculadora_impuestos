import os
import sys

sys.path.append(".")
sys.path.append("src")

import psycopg2
from psycopg2 import errors as pg_errors
from model.calculo_impuesto import CalculoImpuesto

try:
    import secret_config
except ImportError:
    try:
        import secret_config_sample as secret_config
    except ImportError:
        secret_config = None


# =============================================================================
# CLASES DE EXCEPCIÓN PROPIAS DEL CONTROLADOR
# =============================================================================

class CalculoNoEncontradoError(Exception):
    """Excepción que se genera cuando no se encuentra un cálculo en la base de datos."""

    def __init__(self, id_calculo: str = ""):
        mensaje = f"No se encontró ningún cálculo con el identificador '{id_calculo}' en la base de datos." if id_calculo else "El cálculo no fue encontrado en la base de datos."
        super().__init__(mensaje)


class CalculoYaExisteError(Exception):
    """Excepción que se genera al intentar insertar un cálculo con una clave primaria ya existente."""

    def __init__(self, id_calculo: str = ""):
        mensaje = f"Ya existe un cálculo registrado con el identificador '{id_calculo}' en la base de datos." if id_calculo else "El cálculo ya existe en la base de datos."
        super().__init__(mensaje)


class ErrorBaseDatos(Exception):
    """Excepción que encapsula errores de comunicación o ejecución con el motor PostgreSQL."""

    def __init__(self, mensaje: str = "Error inesperado en la base de datos."):
        super().__init__(mensaje)


class DatosCalculoInvalidosError(Exception):
    """Excepción que se genera cuando el objeto de cálculo a insertar es nulo o inválido."""

    def __init__(self, mensaje: str = "Los datos del cálculo son inválidos o nulos."):
        super().__init__(mensaje)


# =============================================================================
# CONTROLADOR MVC
# =============================================================================

class CalculosController:
    """
    Controlador encargado de gestionar las operaciones de base de datos
    para los cálculos de impuestos.
    """

    @classmethod
    def obtener_cursor(cls):
        """Crea la conexión a la base de datos PostgreSQL y retorna un cursor."""
        try:
            # Priorizar variables de entorno de Render / Hosting o secret_config
            host = os.environ.get("PGHOST") or getattr(secret_config, "PGHOST", "localhost")
            database = os.environ.get("PGDATABASE") or getattr(secret_config, "PGDATABASE", "")
            user = os.environ.get("PGUSER") or getattr(secret_config, "PGUSER", "")
            password = os.environ.get("PGPASSWORD") or getattr(secret_config, "PGPASSWORD", "")
            port = os.environ.get("PGPORT") or getattr(secret_config, "PGPORT", 5432)
            sslmode = os.environ.get("PGSSLMODE") or getattr(secret_config, "PGSSLMODE", None)

            params = {
                "database": database,
                "user": user,
                "password": password,
                "host": host,
                "port": int(port),
            }
            if sslmode:
                params["sslmode"] = sslmode

            connection = psycopg2.connect(**params)
            return connection.cursor()
        except Exception as err:
            raise ErrorBaseDatos(f"No fue posible conectarse a la base de datos: {err}")

    @classmethod
    def crear_tabla(cls):
        """Crea la tabla calculos en la base de datos si no existe."""
        try:
            cursor = cls.obtener_cursor()

            ruta_sql = os.path.join(os.path.dirname(__file__), "..", "..", "sql", "crear-calculos.sql")
            if os.path.exists(ruta_sql):
                with open(ruta_sql, "r", encoding="utf-8") as archivo:
                    consulta = archivo.read()
            else:
                consulta = """
                create table if not exists calculos (
                  id_calculo varchar(40) primary key not null,
                  precio_base decimal not null,
                  nombre_impuesto varchar(50) not null,
                  valor_impuesto decimal not null,
                  cantidad_bolsas int not null,
                  valor_bolsas decimal not null,
                  total decimal not null
                );
                """

            cursor.execute(consulta)
            cursor.connection.commit()
            cursor.close()
            cursor.connection.close()
        except Exception as err:
            raise ErrorBaseDatos(f"Error al crear la tabla en la base de datos: {err}")

    @classmethod
    def borrar_tabla(cls):
        """Borra la tabla calculos de la base de datos si existe."""
        try:
            cursor = cls.obtener_cursor()

            ruta_sql = os.path.join(os.path.dirname(__file__), "..", "..", "sql", "borrar-calculos.sql")
            if os.path.exists(ruta_sql):
                with open(ruta_sql, "r", encoding="utf-8") as archivo:
                    consulta = archivo.read()
            else:
                consulta = "drop table if exists calculos;"

            cursor.execute(consulta)
            cursor.connection.commit()
            cursor.close()
            cursor.connection.close()
        except Exception as err:
            raise ErrorBaseDatos(f"Error al borrar la tabla de la base de datos: {err}")

    @classmethod
    def insertar(cls, calculo: CalculoImpuesto):
        """Recibe una instancia de CalculoImpuesto y la inserta en la tabla calculos."""
        if calculo is None:
            raise DatosCalculoInvalidosError("El cálculo a insertar no puede ser nulo")

        cursor = cls.obtener_cursor()
        try:
            consulta = f"""
            insert into calculos (
                id_calculo, precio_base, nombre_impuesto,
                valor_impuesto, cantidad_bolsas, valor_bolsas, total
            ) values (
                '{calculo.id_calculo}', {calculo.precio_base}, '{calculo.nombre_impuesto}',
                {calculo.valor_impuesto}, {calculo.cantidad_bolsas}, {calculo.valor_bolsas}, {calculo.total}
            );
            """
            cursor.execute(consulta)
            cursor.connection.commit()
        except pg_errors.UniqueViolation:
            cursor.connection.rollback()
            raise CalculoYaExisteError(calculo.id_calculo)
        except Exception as err:
            cursor.connection.rollback()
            raise ErrorBaseDatos(f"Error al insertar el cálculo en la base de datos: {err}")
        finally:
            cursor.close()
            cursor.connection.close()

    @classmethod
    def buscar_calculo(cls, id_calculo: str) -> CalculoImpuesto:
        """Busca un cálculo en la base de datos por su id y retorna la instancia CalculoImpuesto.
        Lanza CalculoNoEncontradoError si no existe."""
        if not id_calculo:
            raise CalculoNoEncontradoError(id_calculo)

        cursor = cls.obtener_cursor()
        try:
            consulta = f"""
            select id_calculo, precio_base, nombre_impuesto, valor_impuesto, cantidad_bolsas, valor_bolsas, total
            from calculos
            where id_calculo = '{id_calculo}';
            """
            cursor.execute(consulta)
            fila = cursor.fetchone()

            if fila is None:
                raise CalculoNoEncontradoError(id_calculo)

            return CalculoImpuesto(
                id_calculo=fila[0],
                precio_base=fila[1],
                nombre_impuesto=fila[2],
                valor_impuesto=fila[3],
                cantidad_bolsas=fila[4],
                valor_bolsas=fila[5],
                total=fila[6],
            )
        except CalculoNoEncontradoError:
            raise
        except Exception as err:
            raise ErrorBaseDatos(f"Error al consultar el cálculo en la base de datos: {err}")
        finally:
            cursor.close()
            cursor.connection.close()

    @classmethod
    def buscar_por_id(cls, id_calculo: str) -> CalculoImpuesto:
        """Alias de buscar_calculo para compatibilidad."""
        return cls.buscar_calculo(id_calculo)
