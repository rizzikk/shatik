import random

class Player:
    def __init__(self):
        self.health = random.randint(70, 100) 
        self.inventory = []
        self.shelter_built = False
        self.tool = None

    def gather(self, item):
        self.inventory.append(item)
        print("Вы собрали: {item}.")

    def has_materials(self, materials):
        #Проверяет наличие необходимых материалов в инвентаре.
        return all(self.inventory.count(item) >= count for item, count in materials.items())

    def remove_materials(self, materials):
        #Удаляет использованные материалы из инвентаря.
        for item, count in materials.items():
            for _ in range(count):
                self.inventory.remove(item)

    def craft_tool(self):
        #Создает инструмент на основе выбора игрока.
        print("Доступные инструменты для создания:")
        print("1. Топор (2 дерева, 1 камень, 1 веревка)")
        print("2. Молоток (2 дерева, 2 камня, 1 веревка)")
        print("3. Нож (1 дерево, 1 камень, 1 веревка)")

        tool_choice = input("Какой инструмент вы хотите создать? (топор/молоток/нож): ").lower()
        
        if tool_choice == 'топор':
            materials = {'дерево': 2, 'камень': 1, 'веревка': 1}
            if self.has_materials(materials):
                print("Вы создали топор!")
                self.tool = 'топор'
                self.remove_materials(materials)
            else:
                print("Недостаточно материалов для создания топора.")
                
        elif tool_choice == 'молоток':
            materials = {'дерево': 2, 'камень': 2, 'веревка': 1}
            if self.has_materials(materials):
                print("Вы создали молоток!")
                self.tool = 'молоток'
                self.remove_materials(materials)
            else:
                print("Недостаточно материалов для создания молотка.")
                
        elif tool_choice == 'нож':
            materials = {'дерево': 1, 'камень': 1, 'веревка': 1}
            if self.has_materials(materials):
                print("Вы создали нож!")
                self.tool = 'нож'
                self.remove_materials(materials)
            else:
                print("Недостаточно материалов для создания ножа.")
                
        else:
            print("Неверный выбор инструмента.")

    def build_shelter(self):
        #Строит укрытие с использованием выбранного инструмента.
        if not self.shelter_built and self.has_materials({'дерево': 1, 'камень': 1, 'ветка': 2, 'листья': 3}):
            if self.tool is None:
                print("Для постройки укрытия вам нужен инструмент!")
                return

            print("Вы построили укрытие с помощью {self.tool}!")
            self.shelter_built = True
            self.remove_materials({'дерево': 1, 'камень': 1, 'ветка': 2, 'листья': 3})
        elif self.shelter_built:
            print("Укрытие уже построено.")
        else:
            print("Недостаточно материалов для постройки укрытия.")

    def build_hut(self):
        #Строит хижину с использованием необходимых материалов и инструмента.
        materials = {'дерево': 10, 'камень': 5, 'веревка': 2}
        
        if not self.has_materials(materials):
            print("Недостаточно материалов для постройки хижины.")
            return
        
        if self.tool not in ['молоток', 'топор']:
            print("Для постройки хижины вам нужен молоток или топор!")
            return
        
        print("Вы построили хижину с помощью {self.tool}!")
        self.remove_materials(materials)

    def attack(self, damage):
        #Атака животного.
        print("Вы атаковали животное и нанесли {damage} урона!")

    def take_damage(self, damage):
        #Получение урона.
        self.health -= damage
        print("Вы получили {damage} урона! Ваше здоровье: {self.health}")

    def explore_forest(self):
        #Разведка леса с шансом найти ящики или припасы.
        find_box_chance = random.random() < 0.3  # 30% шанс найти ящик
        find_supplies_chance = random.random() < 0.5  # 50% шанс найти припасы

        if find_box_chance:
            print("Вы нашли ящик! Открываете его...")
            items_found = ['еда', 'дерево', 'камень', 'веревка']
            found_item = random.choice(items_found)
            self.gather(found_item)
        
        elif find_supplies_chance:
            supplies_found = ['еда', 'веревка']
            found_supply = random.choice(supplies_found)
            self.gather(found_supply)

    def gather_leaves_and_sticks(self):
        #Собирает листья и ветки."""
        leaves_count = random.randint(1, 3)   # Случайное количество листьев
        sticks_count = random.randint(1, 3)    # Случайное количество веток
        for _ in range(leaves_count):
            self.gather('листья')
        
        for _ in range(sticks_count):
            self.gather('ветка')

def show_inventory(player):
    #Отображает инвентарь игрока.
    if player.inventory:
        print("В вашем инвентаре:", ', '.join(player.inventory))
    else:
        print("Ваш инвентарь пуст.")

def show_status(player):
    #Отображает текущее состояние игрока.
    print("Ваше здоровье: {player.health}")
    show_inventory(player)

def animal_attack(player):
    animal_damage = random.randint(10, 30)
    print("На вас напало дикое животное!")
    
    while True:
        action = input("Что вы хотите сделать? (атаковать/убежать/посмотреть инвентарь): ").lower()
        
        if action == "атаковать":
            if 'нож' in player.inventory:  
                knife_damage = random.randint(20, 40)  
                player.attack(knife_damage)
            else:
                player.attack(animal_damage)  
            print("Животное отступает.")
            break
        elif action == "убежать":
            if random.random() < 0.5:  
                print("Вы успешно убежали от животного!")
                break
            else:
                player.take_damage(animal_damage)
                print("Вы не смогли убежать и получили урон!")
                if player.health <= 0:
                    print("Вы погибли от ран.")
                    return False
        elif action == "посмотреть инвентарь":
            show_inventory(player)
        else:
            print("Неверный выбор. Попробуйте снова.")
    
    return True

def forest_scene(player):
    #Сцена в лесу с действиями игрока.
    show_status(player)  
    print("Вы находитесь в лесу. Что вы хотите сделать?")
    print("1. Собрать дерево")
    print("2. Собрать камень")
    print("3. Собрать еду")
    print("4. Собрать веревку")
    print("5. Собрать листья и ветки")
    print("6. Создать инструмент")
    print("7. Построить укрытие")
    print("8. Построить хижину")  
    print("9. Посмотреть инвентарь")
    print("10. Разведать лес")  

    choice = input("Ваш выбор: ")
    
    actions = {
        "1": lambda: player.gather('дерево'),
        "2": lambda: player.gather('камень'),
        "3": lambda: player.gather('еда'),
        "4": lambda: player.gather('веревка'),
        "5": player.gather_leaves_and_sticks,
        "6": player.craft_tool,
        "7": player.build_shelter,
        "8": player.build_hut,
        "9": lambda: show_inventory(player),
        "10": player.explore_forest,
    }
    
    action = actions.get(choice)
    
    if action:
        action()
    
    if random.random() < 0.2:  
        return animal_attack(player)

def introduction():
    #Вводная часть игры.
    print("Вы опытный путешественник, который отправился в поход по живописным лесам.")
    print("Однако во время одного из своих походов вы потерялись.")
    print("Непогода застала вас врасплох, и вы сбились с пути.")
    print("Теперь вы находитесь в густом лесу, полном опасностей и тайн.")
    print("Вокруг вас высокие деревья, шорохи дикой природы и запах свежей хвои.")
    print("Вам нужно действовать быстро: ваше здоровье зависит от еды и укрытия.")

def main():
    introduction()  
    
    player = Player()
    
    while player.health > 0:
        forest_scene(player)

if __name__ == "__main__":
    main()