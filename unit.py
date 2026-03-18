from data import UNIT_TYPES


class Unit:
    """戦闘ユニット（複数の兵で構成）"""
    def __init__(self, unit_type: str, groups: int, commander: str):
        self.unit_type = unit_type
        self.groups = groups  # 兵数を40単位で管理
        self.commander = commander
        
        # ユニットタイプから属性を取得
        if unit_type not in UNIT_TYPES:
            raise ValueError(f"Unknown unit type: {unit_type}")
        
        self.specs = UNIT_TYPES[unit_type]
        self.cost = self.specs["cost"]
        self.attack_power = self.specs["attack"]
        self.attack_range = self.specs["range"]
        self.move_range = self.specs["move"]
        
        # HP は兵数に比例
        self.max_hp = groups * 40  # 1組 = 40人
        self.hp = self.max_hp

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, damage: int):
        """ダメージを受ける"""
        self.hp = max(self.hp - damage, 0)
        
    def get_remaining_groups(self) -> int:
        """現在の部隊数を返す（40単位）"""
        return max(1, (self.hp + 39) // 40)

    def calc_attack_damage(self) -> int:
        """攻撃ダメージ計算（ユニット数と攻撃力に基づく）"""
        base_damage = self.attack_power * self.groups
        import random
        variance = random.randint(-5, 5)  # ±5のばらつき
        return max(1, int(base_damage + variance))

    def __repr__(self):
        return f"{self.commander}({self.unit_type}) 兵:{self.get_remaining_groups()}組 HP:{self.hp}"


class Army:
    """軍（複数のユニットで構成）"""
    def __init__(self, name: str, units: list):
        self.name = name
        self.units = units  # List[Unit]

    def is_defeated(self) -> bool:
        """全ユニットが撃破されたかどうか"""
        return all(not unit.is_alive() for unit in self.units)

    def get_alive_units(self):
        """生存しているユニットのみを返す"""
        return [u for u in self.units if u.is_alive()]

    def __repr__(self):
        return f"{self.name}: {len(self.get_alive_units())}/{len(self.units)} ユニット"
