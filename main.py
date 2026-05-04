import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string

HISTORY_FILE = 'history.json'
MIN_LENGTH = 4
MAX_LENGTH = 32

def load_history():
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(data):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_password():
    length = scale_length.get()
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()

    if not (use_digits or use_letters or use_special):
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    password = ''.join(random.choices(chars, k=length))

    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)

    history.append(password)
    save_history(history)
    refresh_history()

def refresh_history():
    for item in tree.get_children():
        tree.delete(item)
    for pwd in history[::-1]:
        tree.insert("", "end", values=(pwd,))

# Загрузка истории
history = load_history()

# Создание главного окна
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x400")

# Блок параметров пароля
frame_options = ttk.LabelFrame(root, text="Параметры пароля")
frame_options.pack(padx=10, pady=10, fill="x")

ttk.Label(frame_options, text="Длина:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
scale_length = tk.Scale(frame_options, from_=MIN_LENGTH, to=MAX_LENGTH, orient="horizontal")
scale_length.set(12)
scale_length.grid(row=0, column=1, padx=5, pady=5)

var_digits = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_options, text="Цифры", variable=var_digits).grid(row=1, column=0, padx=5, pady=5, sticky="w")

var_letters = tk.BooleanVar(value=True)
ttk.Checkbutton(frame_options, text="Буквы", variable=var_letters).grid(row=1, column=1, padx=5, pady=5, sticky="w")

var_special = tk.BooleanVar(value=False)
ttk.Checkbutton(frame_options, text="Спецсимволы", variable=var_special).grid(row=1, column=2, padx=5, pady=5, sticky="w")

# Поле вывода пароля
entry_password = ttk.Entry(root, width=50)
entry_password.pack(pady=10)

# Кнопка генерации
btn_generate = ttk.Button(root, text="Сгенерировать", command=generate_password)
btn_generate.pack(pady=5)

# Таблица истории
frame_history = ttk.LabelFrame(root, text="История паролей")
frame_history.pack(padx=10, pady=10, fill="both", expand=True)

tree = ttk.Treeview(frame_history, columns=("Пароль",), show="headings")
tree.heading("Пароль", text="Пароль")
tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame_history, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

refresh_history()

root.mainloop()
