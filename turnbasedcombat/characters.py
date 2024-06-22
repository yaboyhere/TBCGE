class Character:
    def __init__(self, name, max_health, attack_power, max_mp,picture_path):
        self.name = name
        self.max_health = max_health
        self.current_health = max_health
        self.attack_power = attack_power
        self.max_mp = max_mp
        self.current_mp = max_mp
        self.picture_path=picture_path

    def attack(self, target):
        damage = self.attack_power
        target.take_damage(damage)

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0

    def __str__(self):
        return f"{self.name}: {self.current_health}/{self.max_health} HP, {self.current_mp}/{self.max_mp} MP"

class Mage(Character):
    def __init__(self):
        super().__init__(name="Mage", max_health=80, attack_power=25, max_mp=50,picture_path=r"C:\Users\User\turnbasedcombat\images\images.jpg")

    def fireball(self, target):
        if self.current_mp >= 15:
            damage = self.attack_power + 15  # Fireball does extra damage
            target.take_damage(damage)
            self.current_mp -= 15
            print(f"{self.name} used Fireball on {target.name} for {damage} damage!")
        else:
            print(f"{self.name} does not have enough MP to use Fireball!")

    def heal(self):
        if self.current_mp >= 10:
            healing_amount = 20
            self.current_health += healing_amount
            self.current_mp -= 10
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            print(f"{self.name} healed for {healing_amount} HP!")
        else:
            print(f"{self.name} does not have enough MP to heal!")

class Warrior(Character):
    def __init__(self):
        print('warior \n \n \n \n \n ')
        super().__init__(name="Warrior", max_health=120, attack_power=20, max_mp=30,picture_path=r"C:\Users\User\turnbasedcombat\images\images-_1_.jpg")

    def shield_bash(self, target):
        if self.current_mp >= 10:
            damage = self.attack_power + 10  # Shield Bash does extra damage
            target.take_damage(damage)
            self.current_mp -= 10
            print(f"{self.name} used Shield Bash on {target.name} for {damage} damage!")
        else:
            print(f"{self.name} does not have enough MP to use Shield Bash!")

    def berserk(self):
        if self.current_mp >= 5:
            self.attack_power += 10  # Increases attack power for future attacks
            self.current_mp -= 5
            print(f"{self.name} is now in Berserk mode! Attack power increased by 10!")
        else:
            print(f"{self.name} does not have enough MP to enter Berserk mode!")
class Cleric(Character):#make cleric class
    def __init__(self):
        super().__init__(name="Cleric", max_health=80, attack_power=25, max_mp=50,picture_path=r"C:\Users\User\turnbasedcombat\images\images-_2_.jpg")
        print("cleric\n\n\n\n")

    def fireball(self, target):
        if self.current_mp >= 15:
            damage = self.attack_power + 15  # Fireball does extra damage
            target.take_damage(damage)
            self.current_mp -= 15
            print(f"{self.name} used Fireball on {target.name} for {damage} damage!")
        else:
            print(f"{self.name} does not have enough MP to use Fireball!")

    def heal(self):
        if self.current_mp >= 10:
            healing_amount = 20
            self.current_health += healing_amount
            self.current_mp -= 10
            if self.current_health > self.max_health:
                self.current_health = self.max_health
            print(f"{self.name} healed for {healing_amount} HP!")
        else:
            print(f"{self.name} does not have enough MP to heal!")