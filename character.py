class Character:
    def __init__(self, name: str, hp: int, attack: int):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        self.hp = max(self.hp - amount, 0)

    def heal(self, amount: int):
        self.hp = min(self.hp + amount, self.max_hp)
