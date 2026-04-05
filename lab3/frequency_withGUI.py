import tkinter as tk
from tkinter import scrolledtext, messagebox


def obrabotchik(s):
    s = s.lower()
    for i in ".,?!:":
        s = s.replace(i, " ")
    return s.split()


def to_form_rating(r, type_sort=1):
    dictionary = {}
    try:
        for word in r:
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1

        # Сортировка
        if type_sort == 1:  # По возрастанию (редкие сначала)
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1]))
        elif type_sort == 2:  # По убыванию (частые сначала)
            dictionary = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        else:
            return None
    except Exception:
        return None
    return dictionary


def view(d, type_sort, text_widget):
    # Отображение результатов в текстовом поле
    text_widget.delete(1.0, tk.END)  # Очищаем текстовое поле

    if not d:
        text_widget.insert(tk.END, "Ошибка: не удалось обработать данные.\nПроверьте введённую строку.")
        return

    try:
        a = "ЧАСТЫХ" if type_sort == 2 else "РЕДКИХ"
        text_widget.insert(tk.END, f"ТОП 5 САМЫХ {a} СЛОВ\n")
        text_widget.insert(tk.END, "=" * 50 + "\n")

        cnt = 0
        for word, count in d.items():
            if word:  # Пропускаем пустые строки
                text_widget.insert(tk.END, f"{word}: {count}\n")
                cnt += 1
                if cnt == 5:
                    break

        if cnt == 0:
            text_widget.insert(tk.END, "Слова не найдены.\n")

    except Exception as e:
        text_widget.insert(tk.END, f"Ошибка отображения: {e}")


def analyze():
    """Основная функция анализа"""
    text_input = input_text.get("1.0", tk.END).strip()

    if not text_input:
        messagebox.showwarning("Предупреждение", "Введите текст для анализа!")
        return

    choice = sort_var.get()

    if choice == 0:
        messagebox.showwarning("Предупреждение", "Выберите тип сортировки!")
        return

    # Обработка и анализ
    words = obrabotchik(text_input)
    result = to_form_rating(words, choice)
    view(result, choice, output_text)


def clear_all():
    """Очистка всех полей"""
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)
    sort_var.set(0)


# Создание главного окна
root = tk.Tk()
root.title("Анализатор текста")
root.geometry("600x500")
root.resizable(True, True)

# Переменная для хранения выбора сортировки
sort_var = tk.IntVar(value=0)

# Фрейм для ввода текста
input_frame = tk.LabelFrame(root, text="Введите текст для анализа", padx=10, pady=10)
input_frame.pack(fill="both", expand=True, padx=10, pady=5)

input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD, font=("Arial", 10))
input_text.pack(fill="both", expand=True)

# Фрейм для выбора сортировки
sort_frame = tk.LabelFrame(root, text="Выберите тип сортировки", padx=10, pady=10)
sort_frame.pack(fill="x", padx=10, pady=5)

radio_frame = tk.Frame(sort_frame)
radio_frame.pack()

tk.Radiobutton(radio_frame, text="По возрастанию (редкие сначала)",
               variable=sort_var, value=1, font=("Arial", 10)).pack(side="left", padx=10)
tk.Radiobutton(radio_frame, text="По убыванию (частые сначала)",
               variable=sort_var, value=2, font=("Arial", 10)).pack(side="left", padx=10)

# Фрейм для кнопок
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

analyze_btn = tk.Button(button_frame, text="Анализировать", command=analyze,
                        bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5)
analyze_btn.pack(side="left", padx=5)

clear_btn = tk.Button(button_frame, text="Очистить", command=clear_all,
                      bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=20, pady=5)
clear_btn.pack(side="left", padx=5)

# Фрейм для вывода результатов
output_frame = tk.LabelFrame(root, text="Результат анализа", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, height=12, wrap=tk.WORD, font=("Courier", 10))
output_text.pack(fill="both", expand=True)

# Статусная строка
status_bar = tk.Label(root, text="Готов к работе", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Запуск приложения
root.mainloop()