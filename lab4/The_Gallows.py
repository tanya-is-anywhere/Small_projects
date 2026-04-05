import tkinter as tk
from tkinter import messagebox
import random


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Виселица")
        self.root.geometry("800x800")
        self.root.resizable(False, False)

        # Словарь слов по категориям
        self.words = {
            "Животные": ["КОШКА", "СОБАКА", "ТИГР", "СЛОН", "ЖИРАФ", "ЗЕБРА", "МЕДВЕДЬ", "ЛИСА", "ВОЛК", "ЗАЯЦ"],
            "Фрукты": ["ЯБЛОКО", "ГРУША", "АПЕЛЬСИН", "БАНАН", "ВИНОГРАД", "АРБУЗ", "КИВИ", "МАНГО", "АНАНАС"],
            "Страны": ["РОССИЯ", "ГЕРМАНИЯ", "ФРАНЦИЯ", "ИТАЛИЯ", "ИСПАНИЯ", "КИТАЙ", "ЯПОНИЯ", "БРАЗИЛИЯ"],
            "Программирование": ["PYTHON", "JAVA", "JAVASCRIPT", "HTML", "CSS", "PHP", "RUBY", "C_PLUS_PLUS"],
            "Погодные явления": ["СМЕРЧ", "УРАГАН", "РАДУГА", "ДОЖДЬ", "ТУМАН", "РОСА", "СЫРОСТЬ", "СНЕГОПАД"]
        }

        # Состояние игры
        self.secret_word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.category = ""

        # Настройка цветов
        self.colors = {
            "bg": "#2C3E50",
            "fg": "#ECF0F1",
            "button": "#3498DB",
            "button_hover": "#2980B9",
            "wrong": "#E74C3C",
            "correct": "#2ECC71",
            "word_display": "#F39C12"
        }

        self.setup_ui()
        self.new_game()
        self.root.bind("<Key>", self.on_key_press)

    def setup_ui(self):
        # Фоновый цвет окна
        self.root.configure(bg=self.colors["bg"])

        # Заголовок
        title_label = tk.Label(
            self.root,
            text="ВИСЕЛИЦА",
            font=("Arial", 24, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        title_label.pack(pady=10)

        # Рамка для виселицы
        self.gallows_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.gallows_frame.pack(pady=10)

        self.canvas = tk.Canvas(
            self.gallows_frame,
            width=300,
            height=250,
            bg=self.colors["bg"],
            highlightthickness=0
        )
        self.canvas.pack()

        # Рамка для отображения слова
        self.word_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.word_frame.pack(pady=20)

        self.word_label = tk.Label(
            self.word_frame,
            text="",
            font=("Courier", 36, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["word_display"]
        )
        self.word_label.pack()

        # Рамка для информации об игре
        self.info_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.info_frame.pack(pady=10)

        self.category_label = tk.Label(
            self.info_frame,
            text="Категория: ",
            font=("Arial", 12),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        self.category_label.pack()

        self.wrong_label = tk.Label(
            self.info_frame,
            text=f"Ошибок: {self.wrong_guesses}/{self.max_wrong}",
            font=("Arial", 12),
            bg=self.colors["bg"],
            fg=self.colors["wrong"]
        )
        self.wrong_label.pack()

        self.guessed_label = tk.Label(
            self.info_frame,
            text="Использованные буквы: ",
            font=("Arial", 10),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            wraplength=600
        )
        self.guessed_label.pack(pady=5)

        # Рамка для букв
        self.letters_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.letters_frame.pack(pady=20)

        # Создание кнопок для букв (русский алфавит)
        self.create_letter_buttons()

        # Кнопка новой игры
        self.new_game_btn = tk.Button(
            self.root,
            text="Новая игра",
            command=self.new_game,
            font=("Arial", 12, "bold"),
            bg=self.colors["button"],
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.new_game_btn.pack(pady=10)

        # Эффект наведения для кнопки
        self.new_game_btn.bind("<Enter>", lambda e: self.new_game_btn.configure(bg=self.colors["button_hover"]))
        self.new_game_btn.bind("<Leave>", lambda e: self.new_game_btn.configure(bg=self.colors["button"]))

    def create_letter_buttons(self):
        """Создание кнопок для букв с двумя блоками клавиатуры"""

        # Создаём основной фрейм с прокруткой
        self.canvas_frame = tk.Canvas(self.letters_frame, bg=self.colors["bg"], height=250, width=490)
        self.scrollbar = tk.Scrollbar(self.letters_frame, orient="vertical", command=self.canvas_frame.yview)
        self.scrollable_frame = tk.Frame(self.canvas_frame, bg=self.colors["bg"])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))
        )

        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=self.scrollbar.set)

        self.canvas_frame.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Привязываем колесо мыши для прокрутки
        def on_mousewheel(event):
            self.canvas_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas_frame.bind("<MouseWheel>", on_mousewheel)

        # Русская клавиатура
        russian_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

        # Заголовок для русской клавиатуры
        rus_label = tk.Label(
            self.scrollable_frame,
            text="RU РУССКАЯ КЛАВИАТУРА",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        rus_label.grid(row=0, column=0, columnspan=10, pady=(10, 5))

        # Создание кнопок русской клавиатуры
        self.letter_buttons = {}
        row = 1
        col = 0

        # Первый ряд русской клавиатуры
        first_row = "ЙЦУКЕНГШЩ"
        for letter in first_row:
            self.create_button(letter, row, col)
            col += 1
        row += 1
        col = 0

        # Второй ряд русской клавиатуры
        second_row = "ФЫВАПРОЛД"
        for letter in second_row:
            self.create_button(letter, row, col)
            col += 1
        row += 1
        col = 0

        # Третий ряд русской клавиатуры
        third_row = "ЯЧСМИТЬБЮ"
        for letter in third_row:
            self.create_button(letter, row, col)
            col += 1
        row += 1
        col = 0

        # Четвёртый ряд (оставшиеся буквы)
        fourth_row = "ЁЭЗ"
        for letter in fourth_row:
            self.create_button(letter, row, col)
            col += 1

        # Разделитель
        separator = tk.Frame(self.scrollable_frame, height=2, bg=self.colors["fg"])
        separator.grid(row=row + 1, column=0, columnspan=10, pady=15, sticky="ew")

        # Английская клавиатура
        english_alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM"

        # Заголовок для английской клавиатуры
        eng_label = tk.Label(
            self.scrollable_frame,
            text="EN АНГЛИЙСКАЯ КЛАВИАТУРА",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        eng_label.grid(row=row + 2, column=0, columnspan=10, pady=(10, 5))

        # Создание кнопок английской клавиатуры
        row = row + 3
        col = 0

        # Первый ряд английской клавиатуры
        first_row_en = "QWERTYUIO"
        for letter in first_row_en:
            self.create_button(letter, row, col)
            col += 1
        row += 1
        col = 0

        # Второй ряд английской клавиатуры
        second_row_en = "ASDFGHJKL"
        for letter in second_row_en:
            self.create_button(letter, row, col)
            col += 1
        row += 1
        col = 0

        # Третий ряд английской клавиатуры
        third_row_en = "ZXCVBNMP"
        for letter in third_row_en:
            self.create_button(letter, row, col)
            col += 1

        # Добавляем информационную метку
        info_label = tk.Label(
            self.scrollable_frame,
            text="Подсказка: используйте клавиатуру компьютера для ввода букв",
            font=("Arial", 10, "italic"),
            bg=self.colors["bg"],
            fg=self.colors["fg"]
        )
        info_label.grid(row=row + 2, column=0, columnspan=10, pady=10)

    def create_button(self, letter, row, col):
        """Создание отдельной кнопки"""
        btn = tk.Button(
            self.scrollable_frame,
            text=letter,
            font=("Arial", 12, "bold"),
            width=4,
            height=1,
            bg=self.colors["button"],
            fg="white",
            cursor="hand2",
            command=lambda l=letter: self.guess_letter(l)
        )
        btn.grid(row=row, column=col, padx=2, pady=2)

        # Эффект наведения
        btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.colors["button_hover"]))
        btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.colors["button"]))

        self.letter_buttons[letter] = btn

    def on_key_press(self, event):
        """Обработка нажатий клавиш на физической клавиатуре"""
        key = event.char.upper()

        # Проверяем, является ли нажатая клавиша буквой
        if key in self.letter_buttons:
            self.guess_letter(key)
        elif key == '\r':  # Enter
            self.new_game()
        elif key == '\x1b':  # Escape
            self.root.quit()

    def draw_gallows(self):
        """Рисование виселицы и человечка"""
        self.canvas.delete("all")

        # Основание виселицы
        self.canvas.create_line(50, 220, 250, 220, width=3, fill=self.colors["fg"])  # Основание
        self.canvas.create_line(150, 220, 150, 50, width=3, fill=self.colors["fg"])  # Столб
        self.canvas.create_line(150, 50, 220, 50, width=3, fill=self.colors["fg"])  # Верхняя перекладина
        self.canvas.create_line(220, 50, 220, 80, width=3, fill=self.colors["fg"])  # Веревка

        # Рисование человечка в зависимости от количества ошибок
        if self.wrong_guesses >= 1:
            # Голова
            self.canvas.create_oval(205, 80, 235, 110, width=2, outline=self.colors["fg"])

        if self.wrong_guesses >= 2:
            # Тело
            self.canvas.create_line(220, 110, 220, 160, width=2, fill=self.colors["fg"])

        if self.wrong_guesses >= 3:
            # Левая рука
            self.canvas.create_line(220, 120, 200, 140, width=2, fill=self.colors["fg"])

        if self.wrong_guesses >= 4:
            # Правая рука
            self.canvas.create_line(220, 120, 240, 140, width=2, fill=self.colors["fg"])

        if self.wrong_guesses >= 5:
            # Левая нога
            self.canvas.create_line(220, 160, 200, 190, width=2, fill=self.colors["fg"])

        if self.wrong_guesses >= 6:
            # Правая нога
            self.canvas.create_line(220, 160, 240, 190, width=2, fill=self.colors["fg"])

    def update_word_display(self):
        """Обновление отображения угаданного слова"""
        display_word = ""
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        self.word_label.config(text=display_word.strip())

    def update_info(self):
        """Обновление информационной панели"""
        self.wrong_label.config(text=f"Ошибок: {self.wrong_guesses}/{self.max_wrong}")

        guessed_str = "Использованные буквы: " + ", ".join(sorted(self.guessed_letters))
        self.guessed_label.config(text=guessed_str)

    def guess_letter(self, letter):
        """Обработка угадывания буквы"""
        if letter in self.guessed_letters:
            messagebox.showinfo("Информация", f"Буква '{letter}' уже была использована!")
            return

        self.guessed_letters.add(letter)

        # Отключаем кнопку
        self.letter_buttons[letter].config(state="disabled", bg="gray")

        if letter in self.secret_word:
            # Правильная догадка
            self.letter_buttons[letter].config(bg=self.colors["correct"])
            self.update_word_display()

            # Проверка победы
            if all(letter in self.guessed_letters for letter in self.secret_word):
                self.game_won()
        else:
            # Неправильная догадка
            self.wrong_guesses += 1
            self.letter_buttons[letter].config(bg=self.colors["wrong"])
            self.draw_gallows()
            self.update_info()

            # Проверка поражения
            if self.wrong_guesses >= self.max_wrong:
                self.game_lost()

    def new_game(self):
        """Начало новой игры"""
        # Выбор случайной категории и слова
        self.category = random.choice(list(self.words.keys()))
        self.secret_word = random.choice(self.words[self.category])

        # Сброс состояния
        self.guessed_letters.clear()
        self.wrong_guesses = 0

        # Обновление интерфейса
        self.update_word_display()
        self.update_info()
        self.draw_gallows()

        # Обновление категории
        self.category_label.config(text=f"Категория: {self.category}")

        # Восстановление кнопок
        for letter, btn in self.letter_buttons.items():
            btn.config(state="normal", bg=self.colors["button"])

    def game_won(self):
        """Действия при победе"""
        messagebox.showinfo("Поздравляем!",
                            f"Вы выиграли!\nЗагаданное слово: {self.secret_word}")
        self.new_game()

    def game_lost(self):
        """Действия при поражении"""
        messagebox.showinfo("Игра окончена",
                            f"Вы проиграли!\nЗагаданное слово было: {self.secret_word}")
        self.new_game()


# Запуск игры
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()