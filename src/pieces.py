class Piece:
    def __init__(self, name, player):
        """
        name: Nombre de la pieza (E: Elefante, C: Camello, etc.)
        player: Jugador dueño de la pieza ("P1" o "P2").
        """
        self.name = name
        self.player = player
        self.strength = self.piece_value()

    def __str__(self):
        return f"{self.name}{self.player[-1]}"
    
    def piece_value(self):
        """
        Devuelve el valor de la pieza según su tipo.
        
        Returns:
            int: El valor de la pieza.
        """
        values = {
            "R": 1,  # Conejo
            "G": 2,  # Gato
            "C": 3,  # Camello
            "H": 4,  # Caballo
            "D": 5,  # Perro
            "E": 6   # Elefante
        }
        return values.get(self.name, 0)  # Devuelve 0 si el nombre no es válido
