
class Vehiculo:
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        self.color = color
        self.marca = marca
        self.modelo = modelo
        self.odo = odo

    def vender(self) -> None:
        print(f"El vehiculo {self.marca} {self.modelo} se ha vendido")
        
    def comprar(self) -> None:
        print(f"El vehiculo {self.marca} {self.modelo} se ha comprado")


    @property
    def color(self) -> str:
        return self._color
    
    @color.setter
    def color(self, color: str) -> None:
        if len(color) < 3 or len(color) > 10:
            raise ValueError("El color debe tener entre 3 y 10 caracteres")
        self._color = color
    
    @color.getter
    def color(self) -> str:
        return self._color



class Auto(Vehiculo):
    q_ruedas = 4
    
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        super().__init__(color, marca, modelo, odo)
    

class Moto(Vehiculo):
    q_ruedas = 2
    
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        super().__init__(color, marca, modelo, odo)






# # Class method
# @classmethod
# def get_q_ruedas(cls) -> int:
#     return cls.q_ruedas

# # Static method
# @staticmethod
# def get_info() -> str:
#     return "Este es un auto"






