
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Калькулятор")
root.geometry("300x400")
root.resizable(False, False)

# Поле для вывода
display = Entry(root, font="Arial 16", bd=5, relief="ridge", justify="right")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)

# Кнопки
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', '.', '=', '+'
]

row_idx = 1
col_idx = 0
for button_text in buttons:
    btn = Button(root, text=button_text, font="Arial 12", padx=20, pady=10)
    btn.grid(row=row_idx, column=col_idx, padx=3, pady=3)
    col_idx += 1
    if col_idx > 3:
        col_idx = 0
        row_idx += 1

# Логика кнопок
def click_button(char):
    if char == '=':
        try:
            result = eval(display.get())
            display.delete(0, END)
            display.insert(0, str(result))
        except:
            messagebox.showerror("Ошибка", "Некорректное выражение!")
    else:
        display.insert(END, char)

for btn in root.winfo_children()[1:]:
    if btn.winfo_class() == 'Button':
        btn.config(command=lambda x=btn['text']: click_button(x))

root.mainloop()
