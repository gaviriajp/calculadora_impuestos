import sys
import os

# Para las aplicaciones web creadas con Flask, debemos importar Blueprint
from flask import Blueprint, render_template, request

sys.path.append("src")

from model.calculo_impuesto import CalculoImpuesto
from model import calculadora_impuestos as calc
from controller.calculos_controller import CalculosController

# Blueprint para la vista web de calculos
vista = Blueprint("vista_calculos", __name__)


@vista.route('/')
def inicio():
    """Ruta principal con menú de inicio, formularios de calcular/insertar, buscar y gestión de tablas."""
    return render_template("crear_calculo.html")


@vista.route('/guardar_calculo', methods=['GET', 'POST'])
def guardar_calculo():
    """Calcula el impuesto y guarda el registro en la base de datos."""
    try:
        # Obtenemos los parametros tanto por GET como por POST
        datos = request.form if request.method == 'POST' else request.args

        id_calculo = datos.get("id_calculo", "").strip()
        texto_precio = datos.get("precio", "").strip()
        tipo_impuesto = datos.get("tipo_impuesto", "").strip()
        incluye_bolsas = datos.get("incluye_bolsas") in ["on", "true", "True", "1", "s", "si"]
        texto_bolsas = datos.get("cantidad_bolsas", "0").strip()

        if not id_calculo:
            return "Error: Debe ingresar un identificador único para el cálculo. <br><br><a href='/'>Volver al inicio</a>"

        if not texto_precio:
            return "Error: Debe ingresar el precio del producto. <br><br><a href='/'>Volver al inicio</a>"

        # Validar y convertir precio con la lógica del modelo
        precio = calc.validar_y_convertir_precio(texto_precio)

        # Configurar banderas según tipo de impuesto
        iva19 = tipo_impuesto == "iva19"
        iva5 = tipo_impuesto == "iva5"
        exento = tipo_impuesto == "exento"
        excluido = tipo_impuesto == "excluido"
        inc = tipo_impuesto == "inc"
        impuesto_licor = tipo_impuesto == "licor"

        cantidad_bolsas = 0
        if incluye_bolsas:
            try:
                cantidad_bolsas = int(texto_bolsas or "0")
            except ValueError:
                return "Error: La cantidad de bolsas debe ser un número entero. <br><br><a href='/'>Volver al inicio</a>"

        # Ejecutar lógica del modelo
        resultado = calc.calcular_impuestos(
            precio=precio,
            iva19=iva19,
            iva5=iva5,
            exento=exento,
            excluido=excluido,
            inc=inc,
            impuesto_licor=impuesto_licor,
            bolsas=incluye_bolsas,
            cantidad_bolsas=cantidad_bolsas
        )

        # Crear instancia del modelo CalculoImpuesto
        calculo = CalculoImpuesto(
            id_calculo=id_calculo,
            precio_base=resultado["precio_base"],
            nombre_impuesto=resultado["nombre_impuesto"],
            valor_impuesto=resultado["valor_impuesto"],
            cantidad_bolsas=cantidad_bolsas,
            valor_bolsas=resultado["valor_bolsas"],
            total=resultado["total"]
        )

        # Guardar en base de datos mediante el controlador
        CalculosController.insertar(calculo)

        return f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #4CAF50; border-radius: 8px; background-color: #f9fff9;">
            <h2 style="color: #2e7d32;">¡Cálculo guardado exitosamente en la Base de Datos!</h2>
            <p><strong>ID del cálculo:</strong> {calculo.id_calculo}</p>
            <p><strong>Precio Base:</strong> ${calculo.precio_base:,.2f}</p>
            <p><strong>Impuesto ({calculo.nombre_impuesto}):</strong> ${calculo.valor_impuesto:,.2f}</p>
            <p><strong>Bolsas plásticas ({calculo.cantidad_bolsas}):</strong> ${calculo.valor_bolsas:,.2f}</p>
            <hr style="border: 0; border-top: 1px solid #ccc;">
            <h3 style="color: #1b5e20;">Total a Pagar: ${calculo.total:,.2f}</h3>
            <br>
            <a href="/" style="display: inline-block; padding: 10px 15px; background-color: #0288d1; color: white; text-decoration: none; border-radius: 4px;">Volver al Menú Principal</a>
        </div>
        """

    except calc.PrecioInvalidoError as error:
        return f"Error en precio: {error} <br><br><a href='/'>Volver al formulario</a>"
    except calc.ImpuestoInvalidoError as error:
        return f"Error en impuestos: {error} <br><br><a href='/'>Volver al formulario</a>"
    except Exception as error:
        return f"No es posible guardar el cálculo en la base de datos: {error} <br><br><a href='/'>Volver al formulario</a>"


@vista.route('/buscar_calculo')
def buscar_calculo():
    """Busca un cálculo en la base de datos por su ID."""
    try:
        id_buscado = request.args.get("id_buscado", "").strip()
        if not id_buscado:
            return "Debe ingresar el identificador del cálculo que desea buscar. <br><br><a href='/'>Volver al formulario</a>"

        calculo_encontrado = CalculosController.buscar_calculo(id_buscado)
        return render_template("calculo_buscado.html", calculo=calculo_encontrado, id_buscado=id_buscado)

    except Exception as error:
        return f"No es posible buscar el cálculo: {error} <br><br><a href='/'>Volver al formulario</a>"


@vista.route('/crear_tablas')
def crear_tablas():
    """Crea las tablas en la base de datos PostgreSQL si no existen."""
    try:
        CalculosController.crear_tabla()
        return """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #2196F3; border-radius: 8px; background-color: #f0f7ff;">
            <h2 style="color: #0d47a1;">¡Tablas creadas exitosamente!</h2>
            <p>La tabla <code>calculos</code> ha sido creada o verificada correctamente en PostgreSQL.</p>
            <br>
            <a href="/" style="display: inline-block; padding: 10px 15px; background-color: #0288d1; color: white; text-decoration: none; border-radius: 4px;">Volver al Menú Principal</a>
        </div>
        """
    except Exception as error:
        return f"No es posible crear las tablas: {error} <br><br><a href='/'>Volver al formulario</a>"


@vista.route('/borrar_tablas')
def borrar_tablas():
    """Elimina las tablas en la base de datos PostgreSQL si existen."""
    try:
        CalculosController.borrar_tabla()
        return """
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #d32f2f; border-radius: 8px; background-color: #fffbfa;">
            <h2 style="color: #c62828;">¡Tablas eliminadas exitosamente!</h2>
            <p>La tabla <code>calculos</code> ha sido eliminada de la base de datos PostgreSQL.</p>
            <br>
            <a href="/" style="display: inline-block; padding: 10px 15px; background-color: #0288d1; color: white; text-decoration: none; border-radius: 4px;">Volver al Menú Principal</a>
        </div>
        """
    except Exception as error:
        return f"No es posible eliminar las tablas: {error} <br><br><a href='/'>Volver al formulario</a>"
