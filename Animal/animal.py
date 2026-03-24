import time
import threading

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 100
        self.happiness = 100
        self.is_alive = True

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

    def check_status(self):
        with self.lock:
            if self.hunger == 0 or self.happiness == 0:
                self.is_alive = False
                print(f"{self.name} умер(ла)")

    def live(self):
        while self.is_alive:
            with self.lock:
                self.hunger -= 10
                self.happiness -= 10
                self.check_status()
            time.sleep(10)

def main():
    tamagotchi = Tamagotchi("Барсик")
    
    live_threard = threading.Thread(target=tamagotchi.live)
    live_threard.start()

    while tamagotchi.is_alive:
        command = input("Введите команду (feed, play): ")
        if command == "feed":
            food = int(input("Введите количество еды: "))
            tamagotchi.feed(food)
        elif command == "play":
            fun = int(input("Введите количество времени: "))
            tamagotchi.play(fun)
        else:
            print("Неизвестная команда")
        tamagotchi.check_status()
        print("Сытость ", tamagotchi.hunger, "\nРадость: ", tamagotchi.happiness)

    live_threard.join()

if __name__ == "__main__":
    main()