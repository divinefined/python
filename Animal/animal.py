import time
import threading

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 100
        self.happiness = 100
        self.is_alive = True
        self.lock = threading.RLock()

    def feed(self, food):
        with self.lock:    
            if self.is_alive:
                self.hunger += food
                if self.hunger > 100:
                    self.hunger = 100
                print(f"{self.name} накормлен(а)")
            else:
                print(f"{self.name} мертв(а)")

    def play(self, fun):
        with self.lock:
            if self.is_alive:
                self.happiness += fun
                if self.happiness > 100:
                    self.happiness = 100
                self.hunger -= fun
                if self.hunger < 0:
                    self.hunger = 0
                print(f"{self.name} поиграл(а)")
            else:
                print(f"{self.name} мертв(а)")

    def _check_status(self):
        """Внутренний метод - вызывается уже под защитой lock"""
        if self.hunger == 0 or self.happiness == 0:
            self.is_alive = False
            print(f"{self.name} умер(ла)")

    def check_status(self):
        """Публичный метод - захватывает lock"""
        with self.lock:
            self._check_status()

    def live(self):
        while True:
            with self.lock:
                if not self.is_alive:
                    break
                self.hunger -= 10
                self.happiness -= 10
                self._check_status()
            time.sleep(10)

def main():
    tamagotchi = Tamagotchi("Барсик")
    
    live_threard = threading.Thread(target=tamagotchi.live)
    live_threard.start()

    while True:
        with tamagotchi.lock:
            if not tamagotchi.is_alive:
                break
        
        command = input("Введите команду (feed, play): ")
        if command == "feed":
            try:
                food = int(input("Введите количество еды: "))
                if food <= 0:
                    print("Количество еды должно быть больше 0!")
                    continue
                tamagotchi.feed(food)
            except ValueError:
                print("Пожалуйста, введите число!")
                continue
        elif command == "play":
            try:
                fun = int(input("Введите количество времени: "))
                if fun <= 0:
                    print("Время игры должно быть больше 0!")
                    continue
                tamagotchi.play(fun)
            except ValueError:
                print("Пожалуйста, введите число!")
                continue
        else:
            print("Неизвестная команда")
        tamagotchi.check_status()
        with tamagotchi.lock:
            print("Сытость ", tamagotchi.hunger, "\nРадость: ", tamagotchi.happiness)

    live_threard.join()

if __name__ == "__main__":
    main()