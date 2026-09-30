from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

import sys

sys.path.append("src")
from model.calculadora_impuestos import (
    ImpuestoInvalidoError,
    PrecioInvalidoError,
    calcular_impuestos,
    validar_y_convertir_precio,
)

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
        contenedor = BoxLayout(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(12),
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
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(48),
        )
        contenedor.add_widget(titulo)
        subtitulo = Label(
            text="Calcula el total de tu compra de forma sencilla",
            color=(0.25, 0.35, 0.42, 1),
            font_size=dp(14),
            size_hint_y=None,
            height=dp(28),
        )
        contenedor.add_widget(subtitulo)

        fila_precio = BoxLayout(orientation="horizontal", spacing=dp(10))
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

        fila_categoria = BoxLayout(orientation="horizontal", spacing=dp(10))
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

        fila_bolsas = BoxLayout(orientation="horizontal", spacing=dp(10))
        fila_bolsas.add_widget(self.etiqueta("¿Incluye bolsas plásticas?"))
        self.incluye_bolsas = CheckBox(active=False)
        fila_bolsas.add_widget(self.incluye_bolsas)
        contenedor.add_widget(fila_bolsas)

        fila_cantidad = BoxLayout(orientation="horizontal", spacing=dp(10))
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

        botones = AnchorLayout(
            anchor_x="center",
            size_hint_y=None,
            height=dp(52),
        )
        fila_botones = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_x=None,
            width=dp(340),
        )
        boton_calcular = Button(
            text="Calcular impuesto",
            background_normal="",
            background_color=(0.05, 0.45, 0.55, 1),
            color=(1, 1, 1, 1),
        )
        boton_calcular.bind(on_press=self.calcular_impuesto)
        fila_botones.add_widget(boton_calcular)

        boton_limpiar = Button(
            text="Limpiar formulario",
            background_normal="",
            background_color=(0.38, 0.46, 0.50, 1),
            color=(1, 1, 1, 1),
        )
        boton_limpiar.bind(on_press=self.limpiar_formulario)
        fila_botones.add_widget(boton_limpiar)
        botones.add_widget(fila_botones)
        contenedor.add_widget(botones)

        self.resultado = Label(
            text="Aquí aparecerá el resultado",
            markup=True,
            color=(0.05, 0.22, 0.35, 1),
            font_size=dp(18),
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
            font_size=dp(15),
            halign="left",
            size_hint_x=0.9,
        )

    def limpiar_formulario(self, sender):
        self.valor_compra.text = ""
        self.categoria.text = "Seleccione una categoría"
        self.incluye_bolsas.active = False
        self.cantidad_bolsas.text = ""
        self.cantidad_bolsas.disabled = True
        self.resultado.text = "Aquí aparecerá el resultado"

    def actualizar_cantidad_bolsas(self, checkbox, incluye_bolsas):
        self.cantidad_bolsas.disabled = not incluye_bolsas
        if not incluye_bolsas:
            self.cantidad_bolsas.text = ""

    def mostrar_error(self, mensaje):
        self.resultado.text = f"[color=ff0000]Error: {mensaje}[/color]"

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

            self.resultado.text = (
                f"{resultado['nombre_impuesto']}: "
                f"${resultado['valor_impuesto']:.2f}\n"
                f"Bolsas: ${resultado['valor_bolsas']:.2f}\n"
                f"TOTAL: ${resultado['total']:.2f}"
            )
        except (PrecioInvalidoError, ImpuestoInvalidoError) as error:
            self.mostrar_error(str(error))
        except ValueError:
            self.mostrar_error("La cantidad de bolsas debe ser un entero")


if __name__ == "__main__":
    CalculadoraApp().run()