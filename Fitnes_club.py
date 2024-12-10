from functools import reduce

class User:
    def __init__(self, username, password, role="user"):
        self.username = username
        self.password = password
        self.role = role 
        self.purchase_history = []  
        self.subscription = None 

    def view_purchase_history(self):
        if not self.purchase_history:
            print("История покупок пуста.")
            return
        print("История покупок:")
        for service in self.purchase_history:
            print(f"Название услуги: {service.name}, Цена: {service.price}, Описание: {service.description}")

class Service:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

class FitnessClub:
    def __init__(self):
        self.users = []  
        self.services = []  

    def add_user(self, user):
        self.users.append(user)

    def add_service(self, service):
        self.services.append(service)

    def list_services(self):
        return self.services

    def filter_services(self, criterion):
        return sorted(self.services, key=lambda x: getattr(x, criterion))

    def remove_service(self, service_name):
        self.services = list(filter(lambda s: s.name != service_name, self.services))

    def purchase_service(self, username, service_name):
        user = next((u for u in self.users if u.username == username), None)
        if user:
            service = next((s for s in self.services if s.name == service_name), None)
            if service:
                user.purchase_history.append(service)
                print(f"{user.username} купил услугу {service.name}.")
                return
            print("Услуга не найдена.")
        else:
            print("Пользователь не найден.")

    def view_users(self):
        if not self.users:
            print("Пользователи отсутствуют.")
            return
        print("\nСписок пользователей:")
        
        users_statuses = list(zip([user.username for user in self.users], [user.role for user in self.users], [user.subscription for user in self.users]))
        
        for username, role, status in users_statuses:
            status_str = f"Абонемент: {status}" if status else "Абонемент: неактивен"
            print(f"Имя: {username}, Роль: {role}, {status_str}")

class AuthenticationSystem:
    def __init__(self, fitness_club):
        self.fitness_club = fitness_club

    def register(self, username, password):
        if any(user.username == username for user in self.fitness_club.users):
            print("Пользователь с таким именем уже существует.")
            return
        user = User(username, password)
        self.fitness_club.add_user(user)
        print(f"Пользователь {username} зарегистрирован.")

    def login(self, username, password):
        user = next((u for u in self.fitness_club.users if u.username == username), None)
        if user and user.password == password:
            print(f"Добро пожаловать, {username}!")
            return user
        print("Неверные учетные данные.")
        return None

def view_services(fitness_club):
    services = fitness_club.list_services()
    if services:
        print("\nДоступные услуги:")
        
        service_details = list(map(lambda s: f"Название: {s.name}, Цена: {s.price}, Описание: {s.description}", services))
        
        for detail in service_details:
            print(detail)
    else:
        print("Услуги отсутствуют.")

def purchase_service(fitness_club, username):
    service_name = input("Введите название услуги для покупки: ").strip()
    fitness_club.purchase_service(username, service_name)

def update_account(user):
    new_password = input("Введите новый пароль: ").strip()
    user.password = new_password
    print("Пароль обновлен.")

def admin_add_service(fitness_club):
    name = input("Введите название услуги: ").strip()
    price = float(input("Введите цену услуги: "))
    description = input("Введите описание услуги: ").strip()
    service = Service(name, price, description)
    fitness_club.add_service(service)
    print(f"Услуга {name} добавлена.")

def admin_remove_service(fitness_club):
    name = input("Введите название услуги для удаления: ").strip()
    fitness_club.remove_service(name)
    print(f"Услуга {name} удалена.")

def admin_view_users(fitness_club):
    fitness_club.view_users()

def admin_issue_subscription(user):
    user.subscription = "активен"
    print(f"Абонемент выдан пользователю {user.username}.")

def admin_block_subscription(user):
    user.subscription = "заблокирован"
    print(f"Абонемент пользователя {user.username} заблокирован.")

def main():
    fitness_club = FitnessClub()
    authentication_system = AuthenticationSystem(fitness_club)

    admin_user = User("admin", "adminpass", role="администратор")
    fitness_club.add_user(admin_user)

    initial_services = [
        Service("Фитнес-тренировка", 1000, "Индивидуальная тренировка с тренером"),
        Service("Групповая тренировка", 500, "Тренировка в группе до 10 человек"),
        Service("Йога", 800, "Занятия по йоге"),
        Service("Пилатес", 700, "Занятия по пилатесу"),
        Service("Кардиотренировка", 600, "Тренировка на кардиотренажерах"),
        Service("Силовая тренировка", 900, "Силовая тренировка с весами"),
        Service("Танцы", 750, "Занятия танцами"),
        Service("Секреты питания", 300, "Консультация по питанию"),
        Service("Массаж", 1200, "Расслабляющий массаж"),
        Service("Спортивная медицина", 1500, "Консультация врача-специалиста")
    ]

    for service in initial_services:
        fitness_club.add_service(service)

    while True:
        print("\n1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            authentication_system.register(username, password)
        
        elif choice == '2':
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            user = authentication_system.login(username, password)
            
            if user:
                while True:
                    if user.role == "администратор": 
                        print("\n1. Добавить услугу")
                        print("2. Удалить услугу")
                        print("3. Просмотреть услуги")
                        print("4. Просмотреть пользователей")
                        print("5. Выдать абонемент")
                        print("6. Заблокировать абонемент")
                        print("7. Выйти")
                        
                        admin_choice = input("Выберите действие: ").strip()
                        
                        if admin_choice == '1':
                            admin_add_service(fitness_club)
                        elif admin_choice == '2':
                            admin_remove_service(fitness_club)
                        elif admin_choice == '3':
                            view_services(fitness_club)
                        elif admin_choice == '4':
                            admin_view_users(fitness_club)
                        elif admin_choice == '5':
                            username_to_issue = input("Введите имя пользователя для выдачи абонемента: ").strip()
                            user_to_issue = next((u for u in fitness_club.users if u.username == username_to_issue), None)
                            if user_to_issue:
                                admin_issue_subscription(user_to_issue)
                            else:
                                print("Пользователь не найден.")
                        elif admin_choice == '6':
                            username_to_block = input("Введите имя пользователя для блокировки абонемента: ").strip()
                            user_to_block = next((u for u in fitness_club.users if u.username == username_to_block), None)
                            if user_to_block:
                                admin_block_subscription(user_to_block)
                            else:
                                print("Пользователь не найден.")
                        elif admin_choice == '7':
                            break
                    
                    else:
                        print("\n1. Просмотреть услуги")
                        print("2. Купить услугу")
                        print("3. Обновить учетную запись")
                        print("4. Просмотреть историю покупок")
                        print("5. Выйти")
                        
                        user_choice = input("Выберите действие: ").strip()
                        
                        if user_choice == '1':
                            view_services(fitness_club)
                        
                        elif user_choice == '2':
                            purchase_service(fitness_club, username)
                        
                        elif user_choice == '3':
                            update_account(user)
                        
                        elif user_choice == '4':
                            user.view_purchase_history()
                        
                        elif user_choice == '5':
                            break
        
        elif choice == '3':
            break

if __name__ == "__main__":
    main()