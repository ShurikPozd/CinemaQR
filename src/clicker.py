import time
import webbrowser
import pyautogui
from typing import List
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
from datetime import datetime
import sys


class TaskScheduler:
    """Планировщик задач для параллельного выполнения с использованием времени ожидания"""

    def __init__(self, log_callback=None):
        self.log_callback = log_callback
        self.running = False
        self.tasks = []
        self.current_task_index = 0
        self.browser_path = None
        self.browser_name = None
        self.stop_flag = False  # Флаг для остановки

    def set_log_callback(self, callback):
        self.log_callback = callback

    def log(self, message):
        """Вывод сообщения в лог"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        if self.log_callback:
            self.log_callback(f"[{timestamp}] {message}")

    def find_browser_later(self):
        """Поиск браузера"""
        browsers = [
            ("Yandex", os.path.expandvars(r"%PROGRAMFILES%\Yandex\YandexBrowser\Application\browser.exe")),
            ("Yandex", os.path.expandvars(r"%PROGRAMFILES(x86)%\Yandex\YandexBrowser\Application\browser.exe")),
            ("Yandex", os.path.expandvars(r"%LOCALAPPDATA%\Yandex\YandexBrowser\Application\browser.exe")),
            ("Chrome", os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe")),
            ("Chrome", os.path.expandvars(r"%PROGRAMFILES(x86)%\Google\Chrome\Application\chrome.exe")),
            ("Edge", os.path.expandvars(r"%PROGRAMFILES(x86)%\Microsoft\Edge\Application\msedge.exe")),
        ]

        for name, path in browsers:
            if os.path.exists(path):
                self.log(f"✅ Браузер найден: {name}")
                self.browser_path = path
                self.browser_name = name
                return

        self.log("⚠️ Браузер не найден, будет использоваться системный браузер")

    def open_url(self, url):
        """Открытие URL в браузере"""
        try:
            if self.browser_path and os.path.exists(self.browser_path):
                # Используем start чтобы не ждать закрытия
                if 'yandex' in self.browser_path.lower() or 'chrome' in self.browser_path.lower() or 'msedge' in self.browser_path.lower():
                    os.startfile(self.browser_path)  # Запускаем браузер
                    time.sleep(2)
                    # Открываем URL через pyautogui (более надежно)
                    pyautogui.hotkey('ctrl', 't')  # Новая вкладка
                    time.sleep(1)
                    pyautogui.write(url)
                    time.sleep(1)
                    pyautogui.press('enter')
                else:
                    subprocess.Popen([self.browser_path, url])

                self.log(f"✅ Страница открыта")
                time.sleep(3)
                return True
            else:
                webbrowser.open(url)
                return True
        except Exception as e:
            self.log(f"❌ Ошибка открытия URL: {e}")
            return False

    def close_current_tab(self):
        """Закрытие текущей вкладки браузера"""
        try:
            self.log(f"🖱️ Закрываю вкладку...")

            # Несколько попыток закрыть вкладку
            for attempt in range(3):
                if not self.running or self.stop_flag:
                    return

                # Способ 1: Ctrl+W
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(1)

                # Способ 2: Ctrl+F4 (запасной)
                pyautogui.hotkey('ctrl', 'f4')
                time.sleep(1)

                self.log(f"✅ Вкладка закрыта (попытка {attempt + 1})")
                time.sleep(1)
                return

        except Exception as e:
            self.log(f"⚠️ Ошибка при закрытии вкладки: {e}")

    def click_button(self, button_image: str, max_retries: int = 3):
        """Нажатие на кнопку"""
        for attempt in range(max_retries):
            if not self.running or self.stop_flag:
                return False

            try:
                if not os.path.exists(button_image):
                    self.log(f"❌ Файл {button_image} не найден!")
                    return False

                # Даем время на то, чтобы страница полностью загрузилась
                time.sleep(2)

                location = pyautogui.locateOnScreen(button_image, confidence=0.8)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.moveTo(center)
                    time.sleep(0.5)
                    pyautogui.click(center)
                    self.log(f"✅ Кнопка нажата")
                    return True
                else:
                    self.log(f"⚠️ Кнопка не найдена, попытка {attempt + 1}/{max_retries}")

                    # Делаем скриншот для отладки
                    if attempt == 0:
                        screenshot = pyautogui.screenshot()
                        screenshot.save(f"debug_button_{datetime.now().strftime('%H%M%S')}.png")

                    time.sleep(2)
            except Exception as e:
                self.log(f"⚠️ Ошибка клика: {e}")
                time.sleep(2)
        return False

    def click_stars(self, stars_image: str, max_retries: int = 3):
        """Нажатие на правую часть звезд"""
        for attempt in range(max_retries):
            if not self.running or self.stop_flag:
                return False

            try:
                if not os.path.exists(stars_image):
                    self.log(f"❌ Файл {stars_image} не найден!")
                    return False

                time.sleep(2)

                location = pyautogui.locateOnScreen(stars_image, confidence=0.8)
                if location:
                    center = pyautogui.center(location)
                    offset_x = int(location.width * 0.4)
                    click_x = center.x + offset_x
                    click_y = center.y

                    pyautogui.moveTo(click_x, click_y)
                    time.sleep(0.5)
                    pyautogui.click(click_x, click_y)
                    self.log(f"✅ Звезды нажаты")
                    return True
                else:
                    self.log(f"⚠️ Звезды не найдены, попытка {attempt + 1}/{max_retries}")

                    if attempt == 0:
                        screenshot = pyautogui.screenshot()
                        screenshot.save(f"debug_stars_{datetime.now().strftime('%H%M%S')}.png")

                    time.sleep(2)
            except Exception as e:
                self.log(f"⚠️ Ошибка клика по звездам: {e}")
                time.sleep(2)
        return False

    def add_task(self, task_type, items, base_url, delay_between,
                 needs_stars=False, button_file="button.png", stars_file="stars.png"):
        """Добавление задачи в планировщик"""
        task = {
            'type': task_type,
            'items': items.copy(),
            'base_url': base_url,
            'delay': delay_between,
            'needs_stars': needs_stars,
            'button_file': button_file,
            'stars_file': stars_file,
            'current_index': 0,
            'next_run_time': 0,
            'total_items': len(items),
            'completed': False
        }
        self.tasks.append(task)
        self.log(f"📋 Добавлена задача: {task_type} ({len(items)} шт, задержка {delay_between // 60} мин)")

    def run(self):
        """Запуск планировщика"""
        self.running = True
        self.stop_flag = False

        # Инициализируем время первого запуска для всех задач
        current_time = time.time()
        for task in self.tasks:
            task['next_run_time'] = current_time

        self.log("\n" + "=" * 70)
        self.log("🚀 ЗАПУСК ПЛАНИРОВЩИКА ЗАДАЧ")
        self.log("=" * 70)

        total_items = sum(task['total_items'] for task in self.tasks)
        self.log(f"📊 Всего задач: {len(self.tasks)}, всего элементов: {total_items}")
        self.log("=" * 70 + "\n")

        try:
            while self.running and not self.stop_flag:
                current_time = time.time()
                tasks_completed = 0

                for task in self.tasks:
                    if not self.running or self.stop_flag:
                        break

                    if task['completed']:
                        tasks_completed += 1
                        continue

                    # Проверяем, можно ли выполнить следующую задачу
                    if current_time >= task['next_run_time']:
                        self.execute_task_item(task)

                        # Если задача завершена, переходим к следующей
                        if task['current_index'] >= task['total_items']:
                            task['completed'] = True
                            self.log(f"\n✅ Задача '{task['type']}' полностью завершена!\n")
                        else:
                            # Планируем следующее выполнение
                            task['next_run_time'] = current_time + task['delay']

                            # Показываем время следующего запуска
                            next_time = datetime.fromtimestamp(task['next_run_time']).strftime("%H:%M:%S")
                            self.log(f"⏰ Следующая задача '{task['type']}' в {next_time}")

                    # Проверка на остановку после каждой итерации
                    if not self.running or self.stop_flag:
                        break

                # Если все задачи завершены, выходим
                if tasks_completed == len(self.tasks):
                    self.log("\n" + "=" * 70)
                    self.log("✨ ВСЕ ЗАДАЧИ УСПЕШНО ЗАВЕРШЕНЫ!")
                    self.log("=" * 70)
                    break

                # Проверка на остановку перед паузой
                if not self.running or self.stop_flag:
                    break

                # Небольшая пауза перед следующей проверкой
                for _ in range(10):  # Проверяем остановку каждую секунду
                    if not self.running or self.stop_flag:
                        break
                    time.sleep(0.1)

        except Exception as e:
            self.log(f"❌ Критическая ошибка в планировщике: {e}")
        finally:
            self.running = False
            self.log("⏹️ Планировщик остановлен")

    def execute_task_item(self, task):
        """Выполнение одного элемента задачи"""
        if task['current_index'] >= task['total_items'] or not self.running or self.stop_flag:
            return

        item = task['items'][task['current_index']]
        task['current_index'] += 1

        self.log(f"\n" + "-" * 60)
        self.log(f"📌 [{task['type']}] Выполняется {task['current_index']}/{task['total_items']}")

        # Формируем URL
        url = f"{task['base_url']}{item}"
        self.log(f"🌐 URL: {url}")

        # Открываем в браузере
        self.open_url(url)

        # Проверка остановки
        if not self.running or self.stop_flag:
            return

        self.log(f"⏳ Ожидание загрузки (5 сек)...")
        time.sleep(5)

        # Проверка остановки
        if not self.running or self.stop_flag:
            return

        # Выполняем действия
        if task['needs_stars']:
            self.log(f"⭐ Нажимаю звезды...")
            if self.click_stars(task['stars_file']):
                self.log(f"✅ Звезды нажаты")
                time.sleep(2)

                # Проверка остановки
                if not self.running or self.stop_flag:
                    return

                self.log(f"🖱️ Нажимаю кнопку...")
                if self.click_button(task['button_file']):
                    self.log(f"✅ Кнопка нажата")
                else:
                    self.log(f"❌ Не удалось нажать кнопку")
            else:
                self.log(f"❌ Не удалось нажать звезды")
        else:
            self.log(f"🖱️ Нажимаю кнопку...")
            if self.click_button(task['button_file']):
                self.log(f"✅ Кнопка нажата")
            else:
                self.log(f"❌ Не удалось нажать кнопку")

        # Проверка остановки
        if not self.running or self.stop_flag:
            return

        # Небольшая пауза перед закрытием вкладки
        self.log(f"⏳ Пауза перед закрытием...")
        time.sleep(2)

        # Проверка остановки
        if not self.running or self.stop_flag:
            return

        # Закрываем текущую вкладку
        self.close_current_tab()

        self.log(f"✅ [{task['type']}] Задача {task['current_index']}/{task['total_items']} завершена")
        self.log("-" * 60 + "\n")

    def stop(self):
        """Остановка планировщика"""
        self.log("⏹️ Получен сигнал остановки...")
        self.stop_flag = True
        self.running = False


class ClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Автоматический кликер")
        self.root.geometry("1000x800")

        try:
            self.root.iconbitmap(default='assets/icon.ico')
        except:
            pass

        self.scheduler = None
        self.thread = None
        self.monitor_thread = None

        # Список ID оборудования (20 шт)
        self.equipment_ids = [
            502, 510, 1475, 503, 511, 516, 1549, 504, 512, 517,
            1604, 513, 506, 518, 514, 1413, 1412, 505, 508, 515
        ]

        # Список ID складов (6 шт)
        self.warehouse_ids = [149, 150, 151, 153, 154, 155]

        # Список UUID залов (9 шт)
        self.hall_uuids = [
            "9908a8a2-8342-4e48-a8fa-1b50cd7343bb",
            "9908a8a3-cf34-47c8-a0b1-210f241048aa",
            "9908a8a4-053b-40c1-adcf-8fc7068b6314",
            "9908a8a4-7403-4f89-b154-1d01b1442200",
            "9908a8a4-e1ea-46b8-8cca-f1b2accc32de",
            "9908a8a5-3634-4ae6-a5b1-21d0060871af",
            "9908a8a4-aba0-4782-b6a3-5c865e16dec5",
            "9908a8a4-3c8e-48f1-a84a-cd0280919474",
            "9908a8a3-981f-4f3f-a350-bf3a96ef78e0"
        ]

        self.setup_ui()
        self.check_button_files()

    def check_button_files(self):
        """Проверка наличия файлов"""
        self.log_message("\n" + "=" * 50)
        self.log_message("🔍 ПРОВЕРКА ФАЙЛОВ")
        self.log_message("=" * 50)

        # Проверяем файлы в папке assets
        files_to_check = ['assets/button.png', 'assets/stars.png']
        for file in files_to_check:
            if os.path.exists(file):
                self.log_message(f"✅ {file} найден")
            else:
                self.log_message(f"❌ {file} НЕ найден!")

        self.log_message("=" * 50 + "\n")


    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        title_label = ttk.Label(main_frame, text="Автоматический кликер",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация", padding="10")
        info_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        info_text = """
        Программа автоматически открывает ссылки и нажимает на кнопки.

        Необходимые файлы:
        - button.png - для оборудования и складов
        - stars.png - для залов (звезды)
        """
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.grid(row=0, column=0, sticky=tk.W)

        # Панель выбора задач
        selection_frame = ttk.LabelFrame(main_frame, text="Выбор задач", padding="10")
        selection_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Переменные для чекбоксов
        self.equipment_var = tk.BooleanVar(value=True)
        self.warehouse_var = tk.BooleanVar(value=True)
        self.halls_var = tk.BooleanVar(value=True)

        # Чекбоксы
        ttk.Checkbutton(selection_frame, text="🏭 Оборудование (20 шт, задержка 1 мин)",
                        variable=self.equipment_var).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Checkbutton(selection_frame, text="📦 Склады (6 шт, задержка 5 мин)",
                        variable=self.warehouse_var).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        ttk.Checkbutton(selection_frame, text="🎭 Залы (9 шт, задержка 5 мин, звезды + кнопка)",
                        variable=self.halls_var).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        # Кнопки быстрого выбора
        button_frame = ttk.Frame(selection_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Выбрать всё",
                   command=self.select_all).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Снять всё",
                   command=self.deselect_all).grid(row=0, column=1, padx=5)

        # Статус
        self.status_var = tk.StringVar(value="Статус: Ожидание запуска")
        status_label = ttk.Label(main_frame, textvariable=self.status_var,
                                 font=('Arial', 10, 'bold'))
        status_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=5, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(control_frame, text="🚀 ЗАПУСТИТЬ",
                                       command=self.start_scheduler, width=20)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(control_frame, text="⏹️ СТОП",
                                      command=self.stop_scheduler, width=15, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)

        # Прогресс-бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        # Лог выполнения
        log_frame = ttk.LabelFrame(main_frame, text="Лог выполнения", padding="5")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, width=110, height=20,
                                                  wrap=tk.WORD, font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(7, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

    def select_all(self):
        """Выбрать все задачи"""
        self.equipment_var.set(True)
        self.warehouse_var.set(True)
        self.halls_var.set(True)

    def deselect_all(self):
        """Снять все задачи"""
        self.equipment_var.set(False)
        self.warehouse_var.set(False)
        self.halls_var.set(False)

    def log_message(self, message):
        """Добавление сообщения в лог"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_scheduler(self):
        """Запуск планировщика задач"""
        if not self.equipment_var.get() and not self.warehouse_var.get() and not self.halls_var.get():
            messagebox.showwarning("Предупреждение", "Выберите хотя бы один тип задач!")
            return

        # Проверяем наличие необходимых файлов
        missing_files = []
        if self.equipment_var.get() or self.warehouse_var.get():
            if not os.path.exists('assets/button.png'):
                missing_files.append('assets/button.png')
        if self.halls_var.get():
            if not os.path.exists('assets/stars.png'):
                missing_files.append('assets/stars.png')
            if not os.path.exists('assets/button.png'):
                missing_files.append('assets/button.png')


        if missing_files:
            response = messagebox.askyesno(
                "Файлы не найдены",
                f"Отсутствуют файлы: {', '.join(missing_files)}\n"
                "Продолжить без поиска?"
            )
            if not response:
                return

        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_var.set("Статус: Работает...")
        self.progress.start()

        # Создаем планировщик
        self.scheduler = TaskScheduler(log_callback=self.log_message)
        self.scheduler.find_browser_later()

        # Добавляем задачи
        if self.equipment_var.get():
            self.scheduler.add_task(
                task_type="ОБОРУДОВАНИЕ",
                items=self.equipment_ids,
                base_url="https://kinostore.cinemapark.ru/restaurant/journals/temperatures/equipments/new/",
                delay_between=60,
                needs_stars=False,
                button_file="assets/button.png"
            )

        if self.warehouse_var.get():
            self.scheduler.add_task(
                task_type="СКЛАД",
                items=self.warehouse_ids,
                base_url="https://kinostore.cinemapark.ru/restaurant/journals/temperatures/warehouses/new/",
                delay_between=300,
                needs_stars=False,
                button_file="assets/button.png"
            )

        if self.halls_var.get():
            self.scheduler.add_task(
                task_type="ЗАЛЫ",
                items=self.hall_uuids,
                base_url="https://kinostore.cinemapark.ru/ks/checks/halls/situation/new/",
                delay_between=300,
                needs_stars=True,
                button_file="assets/button.png",
                stars_file="assets/stars.png"
            )


        # Запускаем в отдельном потоке
        self.thread = threading.Thread(target=self.scheduler.run)
        self.thread.daemon = True
        self.thread.start()

        # Запускаем мониторинг
        self.monitor_thread = threading.Thread(target=self.monitor_scheduler)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def monitor_scheduler(self):
        """Мониторинг выполнения планировщика"""
        while self.scheduler and self.scheduler.running:
            time.sleep(0.5)
            # Проверяем, не завершился ли поток
            if self.thread and not self.thread.is_alive():
                break

        self.root.after(0, self.finish_scheduler)

    def stop_scheduler(self):
        """Остановка планировщика"""
        self.log_message("\n⏹️ Останавливаем планировщик...")

        if self.scheduler:
            self.scheduler.stop()

        # Даем время на остановку
        time.sleep(1)

        self.stop_button.config(state='disabled')
        self.status_var.set("Статус: Остановка...")

        # Принудительно завершаем
        self.finish_scheduler()

    def finish_scheduler(self):
        """Завершение работы планировщика"""
        self.progress.stop()
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_var.set("Статус: Завершено")

        if self.scheduler and self.scheduler.running:
            self.scheduler.running = False

        self.log_message("\n✨ Работа планировщика завершена!")


def main():
    """Главная функция"""
    root = tk.Tk()
    app = ClickerGUI(root)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()