import os
import sys

sys.path.append(".")
sys.path.append("src")

import psycopg2
from model.calculo_impuesto import CalculoImpuesto

try:
    import secret_config
except ImportError:
    try:
        import secret_config_sample as secret_config
    except ImportError:
        secret_config = None


class CalculosController:
    """
    Controlador encargado de gestionar las operaciones de base de datos
    para los cálculos de impuestos.
    """

    @classmethod
    def obtener_cursor(cls):
        """Crea la conexión a la base de datos PostgreSQL y retorna un cursor."""
        params = {
            "database": secret_config.PGDATABASE,
            "user": secret_config.PGUSER,
            "password": secret_config.PGPASSWORD,
            "host": secret_config.PGHOST,
            "port": secret_config.PGPORT,
        }
        if hasattr(secret_config, "PGSSLMODE") and secret_config.PGSSLMODE:
            params["sslmode"] = secret_config.PGSSLMODE

        connection = psycopg2.connect(**params)
        return connection.cursor()


    @classmethod
    def crear_tabla(cls):
        """Crea la tabla calculos en la base de datos si no existe."""
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

    @classmethod
    def borrar_tabla(cls):
        """Borra la tabla calculos de la base de datos si existe."""
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

    @classmethod
    def insertar(cls, calculo: CalculoImpuesto):
        """Recibe una instancia de CalculoImpuesto y la inserta en la tabla calculos."""
        if calculo is None:
            raise ValueError("El calculo a insertar no puede ser nulo")

        cursor = cls.obtener_cursor()
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
        cursor.close()
        cursor.connection.close()

    @classmethod
    def buscar_calculo(cls, id_calculo: str) -> CalculoImpuesto:
        """Busca un calculo en la base de datos por su id y retorna la instancia CalculoImpuesto."""
        cursor = cls.obtener_cursor()
        consulta = f"""
        select id_calculo, precio_base, nombre_impuesto, valor_impuesto, cantidad_bolsas, valor_bolsas, total
        from calculos
        where id_calculo = '{id_calculo}';
        """
        cursor.execute(consulta)
        fila = cursor.fetchone()

        cursor.close()
        cursor.connection.close()

        if fila is None:
            return None

        return CalculoImpuesto(
            id_calculo=fila[0],
            precio_base=fila[1],
            nombre_impuesto=fila[2],
            valor_impuesto=fila[3],
            cantidad_bolsas=fila[4],
            valor_bolsas=fila[5],
            total=fila[6],
        )

    @classmethod
    def buscar_por_id(cls, id_calculo: str) -> CalculoImpuesto:
        """Alias de buscar_calculo para compatibilidad."""
        return cls.buscar_calculo(id_calculo)
