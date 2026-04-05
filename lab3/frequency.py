string_analize = input("Введите строку для анализа: ")
choice = int(input("Введите цифру 1 для сортировки по возрастанию, 2 - для сортировки по убыванию: "))



# редактиурем строку: удаляем все знаки препинания, приводим к нижнему регистру, возвращаем список слов
def obrabotchik(s):
    s = s.lower()
    for i in ".,?!:":
        s = s.replace(i, "")

    return s.split(" ")

# формирование словаря из уникальных слов и сортировка
def to_form_rating(r, type_sort=1):
    dictionary = {}
    try:
        for i in r:
            if i in dictionary:
                dictionary[i] += 1
            else:
                dictionary[i] = 1
        if type_sort == 1:
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))

        elif type_sort == 2:
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        else:
            print("Тип сортировки не определён.")
            return 0
    except Exception:
        print("Введено недопустимое значение! Проверьте входящие переменные.")

    return dictionary

def view(d, type_sort):
    try:
        cnt = 0
        a = "ЧАСТЫХ" if type_sort == 2 else "РЕДКИХ"
        print(f"ТОП 5 САМЫХ {a} СЛОВ")
        print("="*50)
        for i in dict(d.items()):
            print(i, d[i])
            cnt += 1
            if cnt == 5:
                break
    except Exception:
        print("Отображение сломано. Тип сортировки не определён.")

# print(to_from_rating(obrabotchik(string_analize), choice))
view(to_from_rating(obrabotchik(string_analize), choice), choice)