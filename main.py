"""
Random Task Generator - GUI приложение для генерации случайных задач
Автор: Алексей Смирнов
Версия: 1.0
"""

import json
import random
import os
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox


class TaskGenerator:
    """Главный класс приложения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator v1.0")
        self.root.geometry("700x650")
        self.root.resizable(False, False)
        
        # Цветовая схема
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'danger': '#f44336',
            'warning': '#ff9800'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Предопределённые задачи
        self.default_tasks = [
            {"text": "Прочитать статью по Python", "type": "учёба", "date": None},
            {"text": "Сделать 30 минут зарядки", "type": "спорт", "date": None},
            {"text": "Написать еженедельный отчёт", "type": "работа", "date": None},
            {"text": "Выучить 20 новых слов", "type": "учёба", "date": None},
            {"text": "Пробежать 3 км", "type": "спорт", "date": None},
            {"text": "Провести совещание", "type": "работа", "date": None},
            {"text": "Решить 5 задач на алгоритмы", "type": "учёба", "date": None},
            {"text": "Сделать растяжку", "type": "спорт", "date": None},
            {"text": "Завершить проект к дедлайну", "type": "работа", "date": None}
        ]
        
        # Загрузка данных
        self.load_data()
        
        # Переменные для фильтрации и добавления
        self.filter_type = StringVar(value="Все")
        self.new_task_text = StringVar()
        self.new_task_type = StringVar(value="учёба")
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление отображения
        self.refresh_history()
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists("tasks.json"):
            try:
                with open("tasks.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", self.default_tasks.copy())
                    self.history = data.get("history", [])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.tasks = self.default_tasks.copy()
                self.history = []
        else:
            self.tasks = self.default_tasks.copy()
            self.history = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        try:
            with open("tasks.json", "w", encoding="utf-8") as f:
                json.dump({
                    "tasks": self.tasks,
                    "history": self.history
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса"""
        
        # Заголовок
        title_frame = Frame(self.root, bg=self.colors['primary'], height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        
        Label(title_frame, text="🎲 Random Task Generator", 
              font=("Arial", 20, "bold"), 
              bg=self.colors['primary'], 
              fg="white").pack(expand=True)
        
        # Основной контейнер
        main_container = Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === Панель генерации ===
        gen_frame = LabelFrame(main_container, text="Генерация задачи", 
                               font=("Arial", 12, "bold"),
                               bg=self.colors['bg'], padx=10, pady=10)
        gen_frame.pack(fill="x", pady=(0, 10))
        
        # Кнопка генерации
        self.generate_btn = Button(gen_frame, text="🎲 Сгенерировать случайную задачу",
                                   command=self.generate_task,
                                   font=("Arial", 12),
                                   bg=self.colors['primary'],
                                   fg="white",
                                   cursor="hand2",
                                   height=2)
        self.generate_btn.pack(fill="x", pady=5)
        
        # === Панель фильтрации ===
        filter_frame = LabelFrame(main_container, text="Фильтрация",
                                  font=("Arial", 12, "bold"),
                                  bg=self.colors['bg'], padx=10, pady=10)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        filter_row = Frame(filter_frame, bg=self.colors['bg'])
        filter_row.pack()
        
        Label(filter_row, text="Фильтр по типу:", 
              font=("Arial", 10), bg=self.colors['bg']).pack(side="left", padx=5)
        
        types = ["Все", "учёба", "спорт", "работа"]
        self.filter_combo = ttk.Combobox(filter_row, textvariable=self.filter_type,
                                         values=types, state="readonly", width=15)
        self.filter_combo.pack(side="left", padx=5)
        self.filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_history())
        
        Button(filter_row, text="Применить фильтр", 
               command=self.refresh_history,
               bg=self.colors['secondary'],
               fg="white",
               cursor="hand2").pack(side="left", padx=10)
        
        # Статистика
        self.stats_label = Label(filter_frame, text="", 
                                 font=("Arial", 9), bg=self.colors['bg'])
        self.stats_label.pack(pady=(5, 0))
        
        # === Панель добавления задач ===
        add_frame = LabelFrame(main_container, text="Добавить новую задачу",
                               font=("Arial", 12, "bold"),
                               bg=self.colors['bg'], padx=10, pady=10)
        add_frame.pack(fill="x", pady=(0, 10))
        
        # Поле ввода текста
        text_row = Frame(add_frame, bg=self.colors['bg'])
        text_row.pack(fill="x", pady=5)
        Label(text_row, text="Текст задачи:", font=("Arial", 10),
              bg=self.colors['bg'], width=12, anchor="w").pack(side="left")
        self.text_entry = Entry(text_row, textvariable=self.new_task_text,
                                font=("Arial", 10), width=45)
        self.text_entry.pack(side="left", padx=5)
        
        # Выбор типа
        type_row = Frame(add_frame, bg=self.colors['bg'])
        type_row.pack(fill="x", pady=5)
        Label(type_row, text="Тип задачи:", font=("Arial", 10),
              bg=self.colors['bg'], width=12, anchor="w").pack(side="left")
        
        type_frame = Frame(type_row, bg=self.colors['bg'])
        type_frame.pack(side="left", padx=5)
        
        for t in ["учёба", "спорт", "работа"]:
            Radiobutton(type_frame, text=t, variable=self.new_task_type,
                       value=t, bg=self.colors['bg'], font=("Arial", 10)).pack(side="left", padx=10)
        
        # Кнопка добавления
        Button(add_frame, text="➕ Добавить задачу",
               command=self.add_task,
               bg=self.colors['warning'],
               fg="white",
               cursor="hand2",
               font=("Arial", 10),
               height=1).pack(pady=10)
        
        # === История задач ===
        history_frame = LabelFrame(main_container, text="История сгенерированных задач",
                                   font=("Arial", 12, "bold"),
                                   bg=self.colors['bg'], padx=10, pady=10)
        history_frame.pack(fill="both", expand=True)
        
        # Таблица для истории
        columns = ("№", "Время", "Задача", "Тип")
        self.history_tree = ttk.Treeview(history_frame, columns=columns,
                                         show="headings", height=12)
        
        # Настройка колонок
        self.history_tree.heading("№", text="№")
        self.history_tree.heading("Время", text="Время")
        self.history_tree.heading("Задача", text="Задача")
        self.history_tree.heading("Тип", text="Тип")
        
        self.history_tree.column("№", width=40, anchor="center")
        self.history_tree.column("Время", width=120, anchor="center")
        self.history_tree.column("Задача", width=350)
        self.history_tree.column("Тип", width=80, anchor="center")
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical",
                                  command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Кнопка очистки истории
        Button(main_container, text="🗑 Очистить всю историю",
               command=self.clear_history,
               bg=self.colors['danger'],
               fg="white",
               cursor="hand2",
               font=("Arial", 10),
               height=1).pack(pady=(10, 0))
    
    def generate_task(self):
        """Генерация случайной задачи с учётом фильтра"""
        # Фильтрация задач
        filter_value = self.filter_type.get()
        
        if filter_value == "Все":
            available_tasks = self.tasks
        else:
            available_tasks = [t for t in self.tasks if t["type"] == filter_value]
        
        # Проверка наличия задач
        if not available_tasks:
            messagebox.showwarning("Нет задач",
                                 f"Нет доступных задач типа '{filter_value}'. Добавьте новые задачи.")
            return
        
        # Выбор случайной задачи
        selected_task = random.choice(available_tasks).copy()
        
        # Добавление времени генерации
        current_time = datetime.now().strftime("%H:%M:%S")
        selected_task["date"] = current_time
        
        # Добавление в историю
        self.history.append(selected_task)
        
        # Сохранение
        self.save_data()
        
        # Обновление отображения
        self.refresh_history()
        
        # Показ уведомления
        messagebox.showinfo("Новая задача!", 
                          f"📌 {selected_task['text']}\n\nТип: {selected_task['type']}\nВремя: {current_time}")
    
    def refresh_history(self):
        """Обновление отображения истории"""
        # Очистка текущего отображения
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Применение фильтра к истории для отображения
        filter_value = self.filter_type.get()
        
        if filter_value == "Все":
            filtered_history = self.history
        else:
            filtered_history = [h for h in self.history if h["type"] == filter_value]
        
        # Добавление задач в таблицу (новые сверху)
        for idx, task in enumerate(filtered_history[::-1], 1):
            time_str = task.get("date", "Н/Д")
            self.history_tree.insert("", "end", 
                                    values=(idx, time_str, task["text"], task["type"]))
        
        # Обновление статистики
        total_gen = len(self.history)
        visible = len(filtered_history)
        self.stats_label.config(text=f"Всего сгенерировано: {total_gen} | Отображается: {visible}")
    
    def add_task(self):
        """Добавление новой задачи с валидацией"""
        # Валидация ввода
        task_text = self.new_task_text.get().strip()
        
        if not task_text:
            messagebox.showwarning("Ошибка", "Текст задачи не может быть пустым!")
            return
        
        if len(task_text) < 3:
            messagebox.showwarning("Ошибка", "Текст задачи должен содержать минимум 3 символа!")
            return
        
        # Создание новой задачи
        new_task = {
            "text": task_text,
            "type": self.new_task_type.get(),
            "date": None
        }
        
        # Добавление в список задач
        self.tasks.append(new_task)
        
        # Сохранение
        self.save_data()
        
        # Очистка полей
        self.new_task_text.set("")
        
        # Подтверждение
        messagebox.showinfo("Успех", f"Задача '{task_text}' успешно добавлена!")
    
    def clear_history(self):
        """Очистка всей истории"""
        if messagebox.askyesno("Подтверждение", 
                              "Вы уверены, что хотите очистить всю историю?\nЭто действие нельзя отменить!"):
            self.history = []
            self.save_data()
            self.refresh_history()
            messagebox.showinfo("Очищено", "История успешно очищена!")


def main():
    """Запуск приложения"""
    root = Tk()
    app = TaskGenerator(root)
    root.mainloop()


if __name__ == "__main__":
    main()