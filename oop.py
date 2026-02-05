
class Vehiculo:
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        self.color = color
        self.marca = marca
        self.modelo = modelo
        self.odo = odo

    def acelerar(self) -> None:
        print(f"El vehiculo {self.marca} {self.modelo} está acelerando")
    
    def frenar(self) -> None:
        print(f"El vehiculo {self.marca} {self.modelo} está frenando")

class Auto(Vehiculo):
    q_ruedas = 4
    
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        super().__init__(color, marca, modelo, odo)
    
    def acelerar(self) -> None:
        print(f"El auto {self.marca} {self.modelo} está acelerando")
    
    def frenar(self) -> None:
        print(f"El auto {self.marca} {self.modelo} está frenando")

class Moto(Vehiculo):
    q_ruedas = 2
    
    def __init__(self, color: str, marca: str, modelo: str, odo: int) -> None:
        super().__init__(color, marca, modelo, odo)


swift = Auto("rojo", "Suzuki", "Swift", 100000)

# swift.color = "verde"
print(swift.color)

bugatti = Auto((255, 0, 0), "Bugatti", "Veyron", 20000)














# # Class method
# @classmethod
# def get_q_ruedas(cls) -> int:
#     return cls.q_ruedas

# # Static method
# @staticmethod
# def get_info() -> str:
#     return "Este es un auto"






