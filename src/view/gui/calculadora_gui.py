import os
import sys

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

sys.path.append(".")
sys.path.append("src")

from model.calculadora_impuestos import (
    ImpuestoInvalidoError,
    PrecioInvalidoError,
    calcular_impuestos,
    validar_y_convertir_precio,
)
from model.calculo_impuesto import CalculoImpuesto
from controller.calculos_controller import CalculosController

CATEGORIAS_IMPUESTO = {
    "IVA 19%": {"iva19": True},
    "IVA 5%": {"iva5": True},
    "Exento": {"exento": True},
    "Excluido": {"excluido": True},
    "Impuesto Nacional al Consumo": {"inc": True},
    "Impuesto a licores": {"impuesto_licor": True},
}


class CalculadoraApp(App):

    def build(self):
        self.ultimo_resultado = None

        contenedor = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(8),
        )
        with contenedor.canvas.before:
            Color(0.93, 0.96, 0.98, 1)
            fondo = Rectangle(pos=contenedor.pos, size=contenedor.size)
        contenedor.bind(
            pos=lambda widget, valor: setattr(fondo, "pos", valor),
            size=lambda widget, valor: setattr(fondo, "size", valor),
        )

        titulo = Label(
            text="CALCULADORA DE IMPUESTOS",
            color=(0.05, 0.22, 0.35, 1),
            font_size=dp(22),
            bold=True,
            size_hint_y=None,
            height=dp(36),
        )
        contenedor.add_widget(titulo)

        subtitulo = Label(
            text="Gestión de impuestos con persistencia en PostgreSQL",
            color=(0.25, 0.35, 0.42, 1),
            font_size=dp(13),
            size_hint_y=None,
            height=dp(24),
        )
        contenedor.add_widget(subtitulo)

        # Fila ID para la Base de Datos
        fila_id = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(36))
        fila_id.add_widget(self.etiqueta("ID del cálculo (BD):"))
        self.id_calculo = TextInput(
            hint_text="Ejemplo: CALC-001",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.05, 0.12, 0.18, 1),
            hint_text_color=(0.45, 0.55, 0.60, 1),
        )
        fila_id.add_widget(self.id_calculo)
        contenedor.add_widget(fila_id)

        # Fila Precio
        fila_precio = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(36))
        fila_precio.add_widget(self.etiqueta("Precio de la compra:"))
        self.valor_compra = TextInput(
            hint_text="Ejemplo: 100000",
            input_filter="float",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.05, 0.12, 0.18, 1),
            hint_text_color=(0.45, 0.55, 0.60, 1),
        )
        fila_precio.add_widget(self.valor_compra)
        contenedor.add_widget(fila_precio)

        # Fila Categoría
        fila_categoria = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(36))
        fila_categoria.add_widget(self.etiqueta("Categoría del impuesto:"))
        self.categoria = Spinner(
            text="Seleccione una categoría",
            values=tuple(CATEGORIAS_IMPUESTO),
            background_normal="",
            background_color=(0.12, 0.52, 0.62, 1),
            color=(1, 1, 1, 1),
        )
        fila_categoria.add_widget(self.categoria)
        contenedor.add_widget(fila_categoria)

        # Fila Bolsas
        fila_bolsas = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(32))
        fila_bolsas.add_widget(self.etiqueta("¿Incluye bolsas plásticas?"))
        self.incluye_bolsas = CheckBox(active=False)
        fila_bolsas.add_widget(self.incluye_bolsas)
        contenedor.add_widget(fila_bolsas)

        # Fila Cantidad de Bolsas
        fila_cantidad = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=None, height=dp(36))
        fila_cantidad.add_widget(self.etiqueta("Cantidad de bolsas:"))
        self.cantidad_bolsas = TextInput(
            hint_text="Ejemplo: 2",
            input_filter="int",
            multiline=False,
            disabled=True,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.05, 0.12, 0.18, 1),
            hint_text_color=(0.45, 0.55, 0.60, 1),
        )
        fila_cantidad.add_widget(self.cantidad_bolsas)
        contenedor.add_widget(fila_cantidad)
        self.incluye_bolsas.bind(active=self.actualizar_cantidad_bolsas)

        # Botones Principales (Calcular, Guardar en BD, Limpiar)
        fila_botones = BoxLayout(
            orientation="horizontal",
            spacing=dp(8),
            size_hint_y=None,
            height=dp(42),
        )
        boton_calcular = Button(
            text="Calcular",
            background_normal="",
            background_color=(0.05, 0.45, 0.55, 1),
            color=(1, 1, 1, 1),
        )
        boton_calcular.bind(on_press=self.calcular_impuesto)
        fila_botones.add_widget(boton_calcular)

        boton_guardar = Button(
            text="Guardar en BD",
            background_normal="",
            background_color=(0.15, 0.55, 0.35, 1),
            color=(1, 1, 1, 1),
        )
        boton_guardar.bind(on_press=self.guardar_en_bd)
        fila_botones.add_widget(boton_guardar)

        boton_limpiar = Button(
            text="Limpiar",
            background_normal="",
            background_color=(0.38, 0.46, 0.50, 1),
            color=(1, 1, 1, 1),
        )
        boton_limpiar.bind(on_press=self.limpiar_formulario)
        fila_botones.add_widget(boton_limpiar)
        contenedor.add_widget(fila_botones)

        # Sección de Búsqueda en Base de Datos
        fila_buscar = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(38))
        fila_buscar.add_widget(self.etiqueta("Buscar ID en BD:"))
        self.id_buscar = TextInput(
            hint_text="ID a buscar...",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.05, 0.12, 0.18, 1),
            hint_text_color=(0.45, 0.55, 0.60, 1),
        )
        fila_buscar.add_widget(self.id_buscar)

        boton_buscar = Button(
            text="Buscar",
            size_hint_x=0.4,
            background_normal="",
            background_color=(0.18, 0.45, 0.72, 1),
            color=(1, 1, 1, 1),
        )
        boton_buscar.bind(on_press=self.buscar_en_bd)
        fila_buscar.add_widget(boton_buscar)
        contenedor.add_widget(fila_buscar)

        # Etiqueta de Resultado
        self.resultado = Label(
            text="Aquí aparecerá el resultado o estado de la consulta",
            markup=True,
            color=(0.05, 0.22, 0.35, 1),
            font_size=dp(16),
            halign="center",
        )
        self.resultado.bind(
            size=lambda label, valor: setattr(label, "text_size", valor)
        )
        contenedor.add_widget(self.resultado)

        return contenedor

    def etiqueta(self, texto):
        return Label(
            text=texto,
            color=(0.05, 0.22, 0.35, 1),
            font_size=dp(14),
            halign="left",
            size_hint_x=0.85,
        )

    def limpiar_formulario(self, sender):
        self.id_calculo.text = ""
        self.valor_compra.text = ""
        self.categoria.text = "Seleccione una categoría"
        self.incluye_bolsas.active = False
        self.cantidad_bolsas.text = ""
        self.cantidad_bolsas.disabled = True
        self.id_buscar.text = ""
        self.ultimo_resultado = None
        self.resultado.text = "Aquí aparecerá el resultado o estado de la consulta"

    def actualizar_cantidad_bolsas(self, checkbox, incluye_bolsas):
        self.cantidad_bolsas.disabled = not incluye_bolsas
        if not incluye_bolsas:
            self.cantidad_bolsas.text = ""

    def mostrar_error(self, mensaje):
        self.resultado.text = f"[color=cc0000]Error: {mensaje}[/color]"

    def calcular_impuesto(self, sender):
        try:
            precio = validar_y_convertir_precio(self.valor_compra.text)
            opciones = CATEGORIAS_IMPUESTO.get(self.categoria.text)
            if opciones is None:
                raise ImpuestoInvalidoError()

            incluye_bolsas = self.incluye_bolsas.active
            cantidad = int(self.cantidad_bolsas.text or "0")
            resultado = calcular_impuestos(
                precio,
                bolsas=incluye_bolsas,
                cantidad_bolsas=cantidad,
                **opciones,
            )

            self.ultimo_resultado = {
                "precio_base": precio,
                "nombre_impuesto": resultado["nombre_impuesto"],
                "valor_impuesto": resultado["valor_impuesto"],
                "cantidad_bolsas": cantidad,
                "valor_bolsas": resultado["valor_bolsas"],
                "total": resultado["total"],
            }

            self.resultado.text = (
                f"[b]{resultado['nombre_impuesto']}:[/b] ${resultado['valor_impuesto']:.2f} | "
                f"[b]Bolsas:[/b] ${resultado['valor_bolsas']:.2f}\n"
                f"[size=20][b]TOTAL A PAGAR: ${resultado['total']:.2f}[/b][/size]"
            )
            return self.ultimo_resultado
        except (PrecioInvalidoError, ImpuestoInvalidoError) as error:
            self.mostrar_error(str(error))
            return None
        except ValueError:
            self.mostrar_error("La cantidad de bolsas debe ser un número entero")
            return None

    def guardar_en_bd(self, sender):
        id_calc = self.id_calculo.text.strip()
        if not id_calc:
            self.mostrar_error("Debe ingresar un ID para el cálculo antes de guardar")
            return

        # Si aún no ha calculado, intenta calcular con los datos ingresados
        if self.ultimo_resultado is None:
            calc_res = self.calcular_impuesto(sender)
            if calc_res is None:
                return
        else:
            calc_res = self.ultimo_resultado

        try:
            nuevo_calculo = CalculoImpuesto(
                id_calculo=id_calc,
                precio_base=calc_res["precio_base"],
                nombre_impuesto=calc_res["nombre_impuesto"],
                valor_impuesto=calc_res["valor_impuesto"],
                cantidad_bolsas=calc_res["cantidad_bolsas"],
                valor_bolsas=calc_res["valor_bolsas"],
                total=calc_res["total"],
            )
            CalculosController.insertar(nuevo_calculo)
            self.resultado.text = (
                f"[color=008800][b]¡Cálculo '{id_calc}' guardado en la base de datos con éxito![/b][/color]\n"
                f"Total guardado: ${nuevo_calculo.total:.2f}"
            )
        except Exception as error:
            self.mostrar_error(f"Error al guardar en BD: {error}")

    def buscar_en_bd(self, sender):
        id_busqueda = self.id_buscar.text.strip()
        if not id_busqueda:
            self.mostrar_error("Ingrese un ID en el campo de búsqueda")
            return

        try:
            calculo = CalculosController.buscar_calculo(id_busqueda)
            if calculo is None:
                self.mostrar_error(f"No se encontró ningún cálculo con el ID '{id_busqueda}'")
                return

            self.id_calculo.text = calculo.id_calculo
            self.valor_compra.text = str(calculo.precio_base)
            self.categoria.text = calculo.nombre_impuesto if calculo.nombre_impuesto in CATEGORIAS_IMPUESTO else "Seleccione una categoría"
            self.incluye_bolsas.active = calculo.cantidad_bolsas > 0
            self.cantidad_bolsas.text = str(calculo.cantidad_bolsas) if calculo.cantidad_bolsas > 0 else ""

            self.resultado.text = (
                f"[color=0055aa][b]Registro encontrado [ID: {calculo.id_calculo}][/b][/color]\n"
                f"Precio base: ${calculo.precio_base:.2f} | Impuesto: {calculo.nombre_impuesto} (${calculo.valor_impuesto:.2f})\n"
                f"Bolsas: {calculo.cantidad_bolsas} (${calculo.valor_bolsas:.2f}) | [b]TOTAL: ${calculo.total:.2f}[/b]"
            )
        except Exception as error:
            self.mostrar_error(f"Error al buscar en BD: {error}")


if __name__ == "__main__":
    CalculadoraApp().run()