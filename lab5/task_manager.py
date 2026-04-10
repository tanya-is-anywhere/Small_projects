'''
Данный таск менеджер управляется через интерактивную строку.
Суть:
Хранилище задач - словарь,
где ключи "Задача 1", "Задача 2" и т.д.
а значения - это {"время создания":time, "содержание задачи":string, "статус": выполнена/не выполнена}
Команды, которые нам нужны:
1 - добавить задачу
2 - удалить задачу
3 - показать список
4* - редактировать существующую задачу
Взаимодействуем с JSON-файлом.
Библиотеки, которые понадобятся: datetime, json
Буду использовать класс для создания менеджера, внутри которого пропишу весь функционал
'''
import datetime
import json


class TaskManager:
    def __init__(self):
        self.task_dict = {}
        self.load_from_file()

    def update_json(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.task_dict, ensure_ascii=False, indent=4))

    def load_from_file(self):
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                self.task_dict = json.load(f)
        except FileNotFoundError:
            self.task_dict = {}
    def add_task(self):
        if not self.task_dict.items():
            number = 1
        else:
            number = list(self.task_dict.items())[-1][0]+1
        task = input("Введите задачу: ")
        status = "Не выполнено"
        time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        json_task = {
            "time": time,
            "task": task,
            "status": status
        }
        self.task_dict[number] = json_task
        print(f"Задача {number} добавлена")
        self.update_json()

    def remove_task(self):
        num = int(input("Введите номер задачи, которую хотите удалить: "))
        permission = input("Вы уверены, что хотите УДАЛИТЬ задачу? y/n")
        if permission == "y":
            del self.task_dict[num]
        elif permission == "n":
            print("Действие отменено")
        else:
            print("Действие отменено. Причина: НЕКОРРЕКТНЫЙ ВВОД")
        print(f"Задача {num} удалена")
        self.update_json()


    def show_tasks(self):
        if not self.task_dict:
            print("Список задач пуст!")
            return

        print("СПИСОК ВСЕХ ЗАДАЧ МЕНЕДЖЕРА")
        print("="*50)
        for key, value in self.task_dict.items():
            time, task, status = value["time"], value["task"], value["status"]
            print(f"Задача {key} (создана {time}, статус {status}): {task}")
        print("=" * 50)

    def show_tasks_json(self):
        with open("tasks.json", "r", encoding="utf-8") as f:
            print(f.read())

    def edit_task(self):
        num = int(input("Введите номер задачи, которую хотите изменить: "))
        task = input("Введите НОВУЮ задачу: ")
        permission = input("Вы уверены, что хотите ИЗМЕНИТЬ задачу? y/n ")
        if permission == "y":
            self.task_dict[num]["task"] = task
            print(f"Задача {num} изменена")
        elif permission == "n":
            print("Действие отменено")
        else:
            print("Действие отменено. Причина: НЕКОРРЕКТНЫЙ ВВОД")
        self.update_json()

    def complete_task(self):
        num = int(input("Введите задачу, которую хотите отметить как ВЫПОЛНЕННУЮ: "))
        status = "Выполнено"
        self.task_dict[num]["status"] = status
        print(f"Задача {num} изменена")
        self.update_json()

if __name__ == "__main__":
    manager = TaskManager()
    print("Добро пожаловать в TaskManager! Чтобы взаимодействовать с консольным приложением, ознакомьтесь с командами ниже.")
    instruction = """
    add - создать задачу
    remove - удалить задачу
    show - показать все задачи
    showjs - вывести содержимое JSON-файла
    edit - редактировать задачу
    complete - отметить задачу "выполненной"
    stop - завершить работу программы
    """
    print(instruction)
    while True:
        command = input()
        if command == "add":
            manager.add_task()
        elif command == "remove":
            manager.remove_task()
        elif command == "show":
            manager.show_tasks()
        elif command == "showjs":
            manager.show_tasks_json()
        elif command == "edit":
            manager.edit_task()
        elif command == "complete":
            manager.complete_task()
        elif command == "stop":
            print("Программа завершила работу.")
            break
        elif command == "help":
            print(instruction)
        else:
            print("Неверный ввод! Используйте команду help для просмотра комманд.")


