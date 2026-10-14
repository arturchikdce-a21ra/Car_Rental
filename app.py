import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from my_map import MyMap
from entities import Car, Client, Rental
from ui_components import (MyLabel, MyButton, MyEntry, MyFrame, MyTree,
                           MyCombo, MyCheck, MyLabelFrame)
from windows import AddClientWindow, ClientsWindow, CarsWindow


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Аренда автомобилей")
        self.geometry("1000x750")

        self.cars = []
        self.clients = []
        self.rentals = []
        self.car_map = MyMap()
        self.client_map = MyMap()

        self._create_test_data()
        self._build_ui()
        self._refresh_all_tabs()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_test_data(self):
        cars_data = [
            ("Toyota", "Camry", 2022, "О854РС", 3500),
            ("BMW", "X5", 2021, "Е303ХР", 7500),
            ("Mercedes", "E-Class", 2023, "О777МВ", 8000),
            ("Hyundai", "Solaris", 2020, "А099РС", 2000),
            ("Kia", "Rio", 2021, "С666НО", 2200),
            ("Audi", "A6", 2022, "Р678РС", 6500),
        ]
        for brand, model, year, plate, price in cars_data:
            car = Car(brand, model, year, plate, price)
            self.cars.append(car)
            self.car_map.put(plate, car)

        clients_data = [
            ("Иванов И.И.", "+7 (900) 111-11-11", "1274961242"),
            ("Петров П.П.", "+7 (900) 222-22-22", "2184761952"),
            ("Сидоров С.С.", "+7 (900) 333-33-33", "7916581201"),
            ("Козлов К.К.", "+7 (900) 444-44-44", "128407142"),
            ("Новиков Н.Н.", "+7 (900) 555-55-55", "12084714287"),
            ("Морозов М.М.", "+7 (900) 666-66-66", "2381237796"),
        ]
        for name, phone, license_num in clients_data:
            client = Client(name, phone, license_num)
            self.clients.append(client)
            self.client_map.put(license_num, client)

    def _build_ui(self):
        self.__notebook = ttk.Notebook(self)
        self.__notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # === Вкладка 1: Аренда ===
        tab_rental = MyFrame(self.__notebook)
        self.__notebook.add(tab_rental, text=" Аренда")

        # Панель оформления аренды с прокруткой
        top_outer = MyLabelFrame(tab_rental, text="Оформление аренды")
        top_outer.pack(fill=tk.X, padx=5, pady=5)

        self.__top_canvas = tk.Canvas(top_outer, highlightthickness=0)
        self.__top_scrollbar = ttk.Scrollbar(top_outer, orient="horizontal",
                                             command=self.__top_canvas.xview)
        self.__top_inner_frame = MyFrame(self.__top_canvas)

        self.__top_canvas.configure(xscrollcommand=self.__top_scrollbar.set)
        self.__top_canvas.create_window((0, 0), window=self.__top_inner_frame, anchor="nw")

        self.__top_canvas.pack(fill=tk.X, padx=5, pady=(5, 0))
        self.__top_scrollbar.pack(fill=tk.X, padx=5, pady=(0, 5))

        def _on_inner_frame_configure(event):
            self.__top_canvas.configure(scrollregion=self.__top_canvas.bbox("all"))
        self.__top_inner_frame.bind("<Configure>", _on_inner_frame_configure)

        def _on_mousewheel(event):
            self.__top_canvas.xview_scroll(-1 * (event.delta // 120), "units")
        self.__top_canvas.bind("<MouseWheel>", _on_mousewheel)
        self.__top_inner_frame.bind("<MouseWheel>", _on_mousewheel)

        # Кнопки
        MyLabel(self.__top_inner_frame, text="Клиент:").grid(row=0, column=0, padx=3, pady=2)
        self.combo_client = MyCombo(self.__top_inner_frame,
                                    values=[c.get_name() for c in self.clients])
        self.combo_client.grid(row=0, column=1, padx=3, pady=2)
        if self.clients:
            self.combo_client.current(0)
        self.combo_client.bind("<<ComboboxSelected>>", self.on_client_selected)

        MyLabel(self.__top_inner_frame, text="Авто:").grid(row=0, column=2, padx=3, pady=2)
        self.combo_car = MyCombo(self.__top_inner_frame,
                                 values=[c.get_full_name() for c in self.cars])
        self.combo_car.grid(row=0, column=3, padx=3, pady=2)
        if self.cars:
            self.combo_car.current(0)
        self.combo_car.bind("<<ComboboxSelected>>", self.on_car_selected)

        MyLabel(self.__top_inner_frame, text="Дней:").grid(row=0, column=4, padx=3, pady=2)
        self.__entry_days = MyEntry(self.__top_inner_frame, width=5)
        self.__entry_days.insert(0, "1")
        self.__entry_days.grid(row=0, column=5, padx=3, pady=2)

        MyButton(self.__top_inner_frame, text="Оформить",
                 command=self._start_rental).grid(row=0, column=6, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="Завершить",
                 command=self._end_rental).grid(row=0, column=7, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="Завершить выбранную",
                 command=self._end_selected_rental).grid(row=0, column=8, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="+ Клиент",
                 command=self._add_client).grid(row=0, column=9, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="- Клиент",
                 command=self._delete_client).grid(row=0, column=10, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="Клиенты",
                 command=self._show_clients).grid(row=0, column=11, padx=3, pady=2)
        MyButton(self.__top_inner_frame, text="Авто",
                 command=self._show_cars).grid(row=0, column=12, padx=3, pady=2)

        # Панель информации
        info_frame = MyLabelFrame(tab_rental, text="Информация")
        info_frame.pack(fill=tk.X, padx=5, pady=5)

        self.client_info_label = MyLabel(info_frame, text="")
        self.client_info_label.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        MyLabel(info_frame, text="|").grid(row=0, column=1, padx=5)

        self.__car_info_label = MyLabel(info_frame, text="")
        self.__car_info_label.grid(row=0, column=2, padx=10, pady=2, sticky="w")

        self.on_client_selected(None)
        self.on_car_selected(None)

        # Таблица текущих аренд
        current_frame = MyLabelFrame(tab_rental, text="Текущие аренды")
        current_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("client", "phone", "car", "plate", "start", "price")
        self.__tree_current = MyTree(current_frame, columns=columns)
        self.__tree_current.heading("client", text="Клиент")
        self.__tree_current.heading("phone", text="Телефон")
        self.__tree_current.heading("car", text="Автомобиль")
        self.__tree_current.heading("plate", text="Номер авто")
        self.__tree_current.heading("start", text="Начало аренды")
        self.__tree_current.heading("price", text="Сумма (руб)")
        self.__tree_current.column("client", width=120)
        self.__tree_current.column("phone", width=120)
        self.__tree_current.column("car", width=120)
        self.__tree_current.column("plate", width=90)
        self.__tree_current.column("start", width=140)
        self.__tree_current.column("price", width=90)
        self.__tree_current.pack(fill=tk.BOTH, expand=True)

        self.__tree_current.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.__tree_current.bind("<Double-1>", self._on_tree_double_click)

        #Вкладка 2: История аренд
        tab_history = MyFrame(self.__notebook)
        self.__notebook.add(tab_history, text=" История аренд")

        history_frame = MyLabelFrame(tab_history, text="Все аренды")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("client", "phone", "car", "plate", "start", "end", "price", "status")
        self.__tree_history = MyTree(history_frame, columns=columns)
        self.__tree_history.heading("client", text="Клиент")
        self.__tree_history.heading("phone", text="Телефон")
        self.__tree_history.heading("car", text="Автомобиль")
        self.__tree_history.heading("plate", text="Номер авто")
        self.__tree_history.heading("start", text="Начало аренды")
        self.__tree_history.heading("end", text="Окончание")
        self.__tree_history.heading("price", text="Сумма (руб)")
        self.__tree_history.heading("status", text="Статус")
        self.__tree_history.column("client", width=110)
        self.__tree_history.column("phone", width=120)
        self.__tree_history.column("car", width=120)
        self.__tree_history.column("plate", width=90)
        self.__tree_history.column("start", width=130)
        self.__tree_history.column("end", width=130)
        self.__tree_history.column("price", width=90)
        self.__tree_history.column("status", width=90)
        self.__tree_history.pack(fill=tk.BOTH, expand=True)

        self.__tree_history.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.__tree_history.bind("<Double-1>", self._on_tree_double_click)

        #Вкладка 3: Текущие аренды
        tab_active = MyFrame(self.__notebook)
        self.__notebook.add(tab_active, text=" Текущие аренды")

        active_frame = MyLabelFrame(tab_active, text="Активные аренды")
        active_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("client", "phone", "car", "plate", "start", "price")
        self.__tree_active = MyTree(active_frame, columns=columns)
        self.__tree_active.heading("client", text="Клиент")
        self.__tree_active.heading("phone", text="Телефон")
        self.__tree_active.heading("car", text="Автомобиль")
        self.__tree_active.heading("plate", text="Номер авто")
        self.__tree_active.heading("start", text="Начало аренды")
        self.__tree_active.heading("price", text="Сумма (руб)")
        self.__tree_active.column("client", width=120)
        self.__tree_active.column("phone", width=120)
        self.__tree_active.column("car", width=120)
        self.__tree_active.column("plate", width=90)
        self.__tree_active.column("start", width=140)
        self.__tree_active.column("price", width=90)
        self.__tree_active.pack(fill=tk.BOTH, expand=True)

        self.__tree_active.bind("<<TreeviewSelect>>", self._on_tree_select)
        self.__tree_active.bind("<Double-1>", self._on_tree_double_click)

        #Вкладка 4: Завершённые
        tab_completed = MyFrame(self.__notebook)
        self.__notebook.add(tab_completed, text=" Завершённые")

        completed_frame = MyLabelFrame(tab_completed, text="Завершённые аренды")
        completed_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("client", "phone", "car", "plate", "start", "end", "price")
        self.__tree_completed = MyTree(completed_frame, columns=columns)
        self.__tree_completed.heading("client", text="Клиент")
        self.__tree_completed.heading("phone", text="Телефон")
        self.__tree_completed.heading("car", text="Автомобиль")
        self.__tree_completed.heading("plate", text="Номер авто")
        self.__tree_completed.heading("start", text="Начало аренды")
        self.__tree_completed.heading("end", text="Окончание")
        self.__tree_completed.heading("price", text="Сумма (руб)")
        self.__tree_completed.column("client", width=120)
        self.__tree_completed.column("phone", width=120)
        self.__tree_completed.column("car", width=120)
        self.__tree_completed.column("plate", width=90)
        self.__tree_completed.column("start", width=130)
        self.__tree_completed.column("end", width=130)
        self.__tree_completed.column("price", width=90)
        self.__tree_completed.pack(fill=tk.BOTH, expand=True)

        #Вкладка 5: Прибыль
        tab_profit = MyFrame(self.__notebook)
        self.__notebook.add(tab_profit, text=" Прибыль")

        profit_frame = MyLabelFrame(tab_profit, text="Прибыль за период")
        profit_frame.pack(fill=tk.X, padx=5, pady=5)

        MyLabel(profit_frame, text="С:").grid(row=0, column=0, padx=5, pady=2)
        self.__entry_date_from = MyEntry(profit_frame, width=12)
        self.__entry_date_from.insert(0, "01.10.2026")
        self.__entry_date_from.grid(row=0, column=1, padx=5, pady=2)

        MyLabel(profit_frame, text="По:").grid(row=0, column=2, padx=5, pady=2)
        self.__entry_date_to = MyEntry(profit_frame, width=12)
        self.__entry_date_to.insert(0, "31.12.2026")
        self.__entry_date_to.grid(row=0, column=3, padx=5, pady=2)

        MyButton(profit_frame, text="Рассчитать прибыль",
                 command=self._calculate_profit).grid(row=0, column=4, padx=5, pady=2)
        MyButton(profit_frame, text="Сбросить фильтр",
                 command=self._reset_profit_filter).grid(row=0, column=5, padx=5, pady=2)

        self.__profit_label = MyLabel(profit_frame,
                                      text="Нажмите «Рассчитать прибыль»",
                                      fg="green", font=("Arial", 10, "bold"))
        self.__profit_label.grid(row=0, column=6, padx=15, pady=2)

        profit_table_frame = MyLabelFrame(tab_profit, text="Аренды за период")
        profit_table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = ("client", "car", "start", "end", "days", "price")
        self.__tree_profit = MyTree(profit_table_frame, columns=columns)
        self.__tree_profit.heading("client", text="Клиент")
        self.__tree_profit.heading("car", text="Автомобиль")
        self.__tree_profit.heading("start", text="Начало")
        self.__tree_profit.heading("end", text="Окончание")
        self.__tree_profit.heading("days", text="Дней")
        self.__tree_profit.heading("price", text="Сумма (руб)")
        self.__tree_profit.column("client", width=120)
        self.__tree_profit.column("car", width=120)
        self.__tree_profit.column("start", width=130)
        self.__tree_profit.column("end", width=130)
        self.__tree_profit.column("days", width=70)
        self.__tree_profit.column("price", width=90)
        self.__tree_profit.pack(fill=tk.BOTH, expand=True)

        # Нижняя панель
        bot = MyFrame(self)
        bot.pack(fill=tk.X, padx=5, pady=5)

        self.status = MyLabel(bot, text="Готов к работе", fg="blue")
        self.status.pack(side=tk.LEFT, padx=5)

        self.__check_var = tk.BooleanVar(value=True)
        MyCheck(bot, text="Завершить активные аренды при выходе",
                variable=self.__check_var).pack(side=tk.LEFT, padx=10)

    def on_client_selected(self, event):
        name = self.combo_client.get()
        if not name:
            self.client_info_label.config(text="Клиент не выбран")
            return
        for c in self.clients:
            if c.get_name() == name:
                self.client_info_label.config(
                    text=f" {c.get_name()}  |   {c.get_phone()}  |  ВУ: {c.get_license_number()}"
                )
                return
        self.client_info_label.config(text="Клиент не выбран")

    def on_car_selected(self, event):
        name = self.combo_car.get()
        if not name:
            self.__car_info_label.config(text="Автомобиль не выбран")
            return
        for c in self.cars:
            if c.get_full_name() == name:
                status = " В аренде" if c.is_rented() else " Свободен"
                self.__car_info_label.config(
                    text=f" {c.get_full_name()}  |   {c.get_year()} г.  |  "
                         f" {c.get_plate()}  |  {c.get_price_per_day()} руб/день  |  {status}"
                )
                return
        self.__car_info_label.config(text="Автомобиль не выбран")

    def _add_client(self):
        AddClientWindow(self, self)

    def _delete_client(self):
        client_name = self.combo_client.get()
        if not client_name:
            messagebox.showwarning("Внимание", "Выберите клиента для удаления!")
            return

        client_to_delete = None
        for c in self.clients:
            if c.get_name() == client_name:
                client_to_delete = c
                break

        if not client_to_delete:
            return

        active_rentals = [r for r in self.rentals
                         if r.get_client() == client_to_delete and r.is_active()]
        if active_rentals:
            messagebox.showwarning(
                "Внимание",
                f"Нельзя удалить клиента {client_name}!\n"
                f"У него есть {len(active_rentals)} активная(ых) аренда(ы).\n"
                f"Сначала завершите аренды."
            )
            return

        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Удалить клиента {client_name}?\n"
            f"Телефон: {client_to_delete.get_phone()}\n"
            f"ВУ: {client_to_delete.get_license_number()}\n\n"
            f"Это действие нельзя отменить!"
        )
        if not confirm:
            return

        self.clients.remove(client_to_delete)
        self.client_map.remove(client_to_delete.get_license_number())

        self.combo_client["values"] = [c.get_name() for c in self.clients]
        if self.clients:
            self.combo_client.current(0)
            self.on_client_selected(None)
        else:
            self.combo_client.set("")
            self.client_info_label.config(text="Нет клиентов")

        self.status.config(text=f"Клиент удалён: {client_name}")
        self._refresh_all_tabs()

    def _on_tree_select(self, event):
        tree = event.widget
        selection = tree.selection()
        if not selection:
            return

        item = tree.item(selection[0])
        values = item["values"]
        if not values:
            return

        client_name = values[0]
        car_name = values[2]

        if client_name in self.combo_client["values"]:
            self.combo_client.set(client_name)
            self.on_client_selected(None)

        if car_name in self.combo_car["values"]:
            self.combo_car.set(car_name)
            self.on_car_selected(None)

        self.status.config(text=f"Выбрана аренда: {client_name} -> {car_name}")

    def _on_tree_double_click(self, event):
        tree = event.widget
        selection = tree.selection()
        if not selection:
            return

        item = tree.item(selection[0])
        values = item["values"]
        if not values:
            return

        if len(values) > 7 and values[7] != "Активна":
            messagebox.showinfo("Инфо", "Эта аренда уже завершена")
            return

        client_name = values[0]
        car_name = values[2]

        for r in self.rentals:
            if (r.get_client_name() == client_name and
                r.get_car_name() == car_name and
                r.is_active()):
                r.set_end_time(datetime.now())
                r.get_car().set_rented(False)
                self.status.config(text=f"Аренда завершена: {client_name} -> {car_name}")
                self._refresh_all_tabs()
                self.on_car_selected(None)
                return

    def _end_selected_rental(self):
        selection = self.__tree_current.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите аренду в таблице")
            return

        item = self.__tree_current.item(selection[0])
        values = item["values"]
        if not values:
            return

        client_name = values[0]
        car_name = values[2]

        for r in self.rentals:
            if (r.get_client_name() == client_name and
                r.get_car_name() == car_name and
                r.is_active()):
                r.set_end_time(datetime.now())
                r.get_car().set_rented(False)
                self.status.config(text=f"Аренда завершена: {client_name} -> {car_name}")
                self._refresh_all_tabs()
                self.on_car_selected(None)
                return

    def _show_clients(self):
        ClientsWindow(self, self)

    def _show_cars(self):
        CarsWindow(self, self)

    def _refresh_all_tabs(self):
        fmt = "%d.%m.%Y %H:%M:%S"

        self.__tree_current.delete(*self.__tree_current.get_children())
        for r in self.rentals:
            if r.is_active():
                self.__tree_current.insert("", "end", values=(
                    r.get_client_name(),
                    r.get_client().get_phone(),
                    r.get_car_name(),
                    r.get_car_plate(),
                    r.get_start_time().strftime(fmt),
                    "—"
                ))

        self.__tree_history.delete(*self.__tree_history.get_children())
        for r in self.rentals:
            end_str = r.get_end_time().strftime(fmt) if r.get_end_time() else "—"
            price_str = str(r.get_total_price()) if r.get_end_time() else "—"
            status_str = "Активна" if r.is_active() else "Завершена"
            self.__tree_history.insert("", "end", values=(
                r.get_client_name(),
                r.get_client().get_phone(),
                r.get_car_name(),
                r.get_car_plate(),
                r.get_start_time().strftime(fmt),
                end_str,
                price_str,
                status_str
            ))

        self.__tree_active.delete(*self.__tree_active.get_children())
        for r in self.rentals:
            if r.is_active():
                self.__tree_active.insert("", "end", values=(
                    r.get_client_name(),
                    r.get_client().get_phone(),
                    r.get_car_name(),
                    r.get_car_plate(),
                    r.get_start_time().strftime(fmt),
                    "—"
                ))

        self.__tree_completed.delete(*self.__tree_completed.get_children())
        for r in self.rentals:
            if not r.is_active():
                self.__tree_completed.insert("", "end", values=(
                    r.get_client_name(),
                    r.get_client().get_phone(),
                    r.get_car_name(),
                    r.get_car_plate(),
                    r.get_start_time().strftime(fmt),
                    r.get_end_time().strftime(fmt),
                    r.get_total_price()
                ))

    def _start_rental(self):
        client_name = self.combo_client.get()
        car_name = self.combo_car.get()
        days_str = self.__entry_days.get()

        if not client_name or not car_name:
            messagebox.showwarning("Внимание", "Выберите клиента и автомобиль")
            return

        try:
            days = int(days_str)
            if days < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Внимание", "Введите корректное количество дней (>=1)")
            return

        client = None
        for c in self.clients:
            if c.get_name() == client_name:
                client = c
                break

        car = None
        for c in self.cars:
            if c.get_full_name() == car_name:
                car = c
                break

        if not client or not car:
            messagebox.showerror("Ошибка", "Не удалось найти клиента или автомобиль")
            return

        if car.is_rented():
            messagebox.showwarning("Внимание", f"{car.get_full_name()} уже в аренде")
            return

        rental = Rental(client, car)
        self.rentals.append(rental)
        car.set_rented(True)

        self.status.config(text=f"Аренда оформлена: {client_name} -> {car_name}")
        self._refresh_all_tabs()
        self.on_car_selected(None)

    def _end_rental(self):
        client_name = self.combo_client.get()
        car_name = self.combo_car.get()

        for r in self.rentals:
            if (r.get_client_name() == client_name and
                r.get_car_name() == car_name and
                r.is_active()):
                r.set_end_time(datetime.now())
                r.get_car().set_rented(False)
                self.status.config(text=f"Аренда завершена: {client_name} -> {car_name}")
                self._refresh_all_tabs()
                self.on_car_selected(None)
                return

        messagebox.showinfo("Инфо", "Активная аренда не найдена")

    def _calculate_profit(self):
        date_from_str = self.__entry_date_from.get().strip()
        date_to_str = self.__entry_date_to.get().strip()

        try:
            date_from = datetime.strptime(date_from_str, "%d.%m.%Y")
            date_to = datetime.strptime(date_to_str, "%d.%m.%Y")
        except ValueError:
            messagebox.showwarning("Внимание", "Неверный формат даты. Используйте дд.мм.гггг")
            return

        if date_from > date_to:
            messagebox.showwarning("Внимание", "Дата «С» не может быть позже даты «По»")
            return

        filtered_rentals = []
        total_profit = 0
        total_days = 0

        for r in self.rentals:
            if r.get_end_time() is None:
                continue

            start_date = r.get_start_time().replace(hour=0, minute=0, second=0, microsecond=0)
            if date_from <= start_date <= date_to:
                filtered_rentals.append(r)
                total_profit += r.get_total_price()
                total_days += r.get_duration_days()

        count = len(filtered_rentals)
        text = (f"Период: {date_from_str} - {date_to_str}  |  "
                f"Аренд: {count}  |  Дней: {total_days}  |  "
                f"Прибыль: {total_profit} руб")
        self.__profit_label.config(text=text)

        self.__tree_profit.delete(*self.__tree_profit.get_children())
        fmt = "%d.%m.%Y %H:%M:%S"
        for r in filtered_rentals:
            self.__tree_profit.insert("", "end", values=(
                r.get_client_name(),
                r.get_car_name(),
                r.get_start_time().strftime(fmt),
                r.get_end_time().strftime(fmt),
                r.get_duration_days(),
                r.get_total_price()
            ))

        self.status.config(text=f"Прибыль за период: {total_profit} руб ({count} аренд)")

    def _reset_profit_filter(self):
        self.__profit_label.config(text="Нажмите «Рассчитать прибыль»")
        self.__entry_date_from.delete(0, tk.END)
        self.__entry_date_from.insert(0, "01.10.2026")
        self.__entry_date_to.delete(0, tk.END)
        self.__entry_date_to.insert(0, "31.12.2026")
        self.__tree_profit.delete(*self.__tree_profit.get_children())
        self.status.config(text="Фильтр сброшен")

    def _on_close(self):
        if self.__check_var.get():
            for r in self.rentals:
                if r.is_active():
                    r.set_end_time(datetime.now())
                    r.get_car().set_rented(False)
        self._save_report()
        self.destroy()

    def _save_report(self):
        fmt = "%d.%m.%Y %H:%M:%S"
        lines = []

        header = "+-------------+--------------------+--------------------+"
        lines.append(header)
        lines.append("|   login     |      time_in       |      time_out      |")
        lines.append("|-------------+--------------------+--------------------|")

        for r in self.rentals:
            login = r.get_client_name()
            time_in = r.get_start_time().strftime(fmt)
            time_out = r.get_end_time().strftime(fmt) if r.get_end_time() else "—"
            line = f"| {login:<11} | {time_in:<18} | {time_out:<18} |"
            lines.append(line)

        lines.append(header)

        with open("rental_report.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print("Отчёт сохранён в rental_report.txt")
