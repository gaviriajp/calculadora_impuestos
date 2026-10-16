class CalculoImpuesto:
    """
    Pertenece a la Capa del Modelo (Reglas de Negocio / Entidad).
    Representa un cálculo o liquidación de impuestos realizada en el sistema.
    """

    def __init__(
        self,
        id_calculo: str,
        precio_base: float,
        nombre_impuesto: str,
        valor_impuesto: float,
        cantidad_bolsas: int,
        valor_bolsas: float,
        total: float,
    ):
        self.id_calculo = str(id_calculo)
        self.precio_base = float(precio_base)
        self.nombre_impuesto = str(nombre_impuesto)
        self.valor_impuesto = float(valor_impuesto)
        self.cantidad_bolsas = int(cantidad_bolsas)
        self.valor_bolsas = float(valor_bolsas)
        self.total = float(total)

    def is_equal(self, otro) -> bool:
        """
        Compara el objeto actual con otra instancia de CalculoImpuesto.
        Lanza AssertionError si algún atributo no coincide.
        """
        assert self.id_calculo == otro.id_calculo
        assert round(float(self.precio_base), 2) == round(float(otro.precio_base), 2)
        assert self.nombre_impuesto == otro.nombre_impuesto
        assert round(float(self.valor_impuesto), 2) == round(float(otro.valor_impuesto), 2)
        assert int(self.cantidad_bolsas) == int(otro.cantidad_bolsas)
        assert round(float(self.valor_bolsas), 2) == round(float(otro.valor_bolsas), 2)
        assert round(float(self.total), 2) == round(float(otro.total), 2)
        return True
