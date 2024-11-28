class Piece:
    def __init__(self, name, player):
        """
        name: Nombre de la pieza (E: Elefante, C: Camello, etc.)
        player: Jugador dueño de la pieza ("P1" o "P2").
        """
        self.name = name
        self.player = player

    def __str__(self):
        return f"{self.name}{self.player[-1]}" 