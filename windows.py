import tkinter as tk
from tkinter import messagebox
from ui_components import MyFrame, MyButton, MyTree, MyLabel, MyEntry


class AddClientWindow(tk.Toplevel):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.title("Добавить клиента")
        self.geometry("400x250")
        self.transient(parent)
        self.grab_set()

        self.__app = app

        form = MyFrame(self)
        form.pack(fill=tk.BOTH, expand=True)

        MyLabel(form, text="ФИО:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.__entry_name = MyEntry(form, width=30)
        self.__entry_name.grid(row=0, column=1, padx=5, pady=5)

        MyLabel(form, text="Телефон:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.__entry_phone = MyEntry(form, width=30)
        self.__entry_phone.grid(row=1, column=1, padx=5, pady=5)
        self.__entry_phone.insert(0, "+7 (900) 000-00-00")

        MyLabel(form, text="Номер ВУ:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.__entry_license = MyEntry(form, width=30)
        self.__entry_license.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = MyFrame(form)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        MyButton(btn_frame, text="Сохранить", command=self._save).pack(side=tk.LEFT, padx=5)
        MyButton(btn_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _save(self):
        name = self.__entry_name.get().strip()
        phone = self.__entry_phone.get().strip()
        license_num = self.__entry_license.get().strip()

        if not name:
            messagebox.showwarning("Внимание", "Введите ФИО!")
            return
        if not phone:
            messagebox.showwarning("Внимание", "Введите телефон!")
            return
        if not license_num:
            messagebox.showwarning("Внимание", "Введите номер водительского удостоверения!")
            return

        for c in self.__app.clients:
            if c.get_license_number() == license_num:
                messagebox.showwarning("Внимание", "Клиент с таким номером ВУ уже существует!")
                return

        from entities import Client
        client = Client(name, phone, license_num)
        self.__app.clients.append(client)
        self.__app.client_map.put(license_num, client)

        self.__app.combo_client["values"] = [c.get_name() for c in self.__app.clients]
        self.__app.combo_client.set(name)
        self.__app.on_client_selected(None)

        self.__app.status.config(text=f"Добавлен клиент: {name}")
        self.destroy()


class ClientsWindow(tk.Toplevel):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.title("Список клиентов")
        self.geometry("700x450")
        self.transient(parent)
        self.grab_set()

        self.__app = app

        btn_frame = MyFrame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=2)

        MyButton(btn_frame, text="Удалить выбранного", command=self._delete_selected).pack(side=tk.LEFT, padx=5)
        MyButton(btn_frame, text="Обновить", command=self._refresh).pack(side=tk.LEFT, padx=5)
        MyButton(btn_frame, text="Закрыть", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        columns = ("name", "phone", "license", "active", "total")
        self.__tree = MyTree(self, columns=columns)
        self.__tree.heading("name", text="ФИО")
        self.__tree.heading("phone", text="Телефон")
        self.__tree.heading("license", text="Номер ВУ")
        self.__tree.heading("active", text="Активных аренд")
        self.__tree.heading("total", text="Всего аренд")
        self.__tree.column("name", width=150)
        self.__tree.column("phone", width=140)
        self.__tree.column("license", width=130)
        self.__tree.column("active", width=110)
        self.__tree.column("total", width=90)
        self.__tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.__tree.bind("<Double-1>", self._on_double_click)
        self._refresh()

    def _refresh(self):
        self.__tree.delete(*self.__tree.get_children())
        clients = self.__app.clients
        rentals = self.__app.rentals

        for c in clients:
            active_count = sum(1 for r in rentals if r.get_client() == c and r.is_active())
            total_count = sum(1 for r in rentals if r.get_client() == c)
            self.__tree.insert("", "end", values=(
                c.get_name(), c.get_phone(), c.get_license_number(),
                active_count, total_count
            ))

    def _on_double_click(self, event):
        self._delete_selected()

    def _delete_selected(self):
        selection = self.__tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите клиента в таблице!")
            return

        item = self.__tree.item(selection[0])
        values = item["values"]
        if not values:
            return

        client_name = values[0]
        license_num = values[2]

        client_to_delete = None
        for c in self.__app.clients:
            if c.get_license_number() == license_num:
                client_to_delete = c
                break

        if not client_to_delete:
            return

        active_rentals = [r for r in self.__app.rentals
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
            f"ВУ: {license_num}"
        )
        if not confirm:
            return

        self.__app.clients.remove(client_to_delete)
        self.__app.client_map.remove(license_num)

        self.__app.combo_client["values"] = [c.get_name() for c in self.__app.clients]
        if self.__app.clients:
            self.__app.combo_client.current(0)
            self.__app.on_client_selected(None)
        else:
            self.__app.combo_client.set("")
            self.__app.client_info_label.config(text="Нет клиентов")

        self.__app.status.config(text=f"Клиент удалён: {client_name}")
        self._refresh()


class CarsWindow(tk.Toplevel):

    def __init__(self, parent, app):
        super().__init__(parent)
        self.title("Список автомобилей")
        self.geometry("700x450")
        self.transient(parent)
        self.grab_set()

        self.__app = app

        btn_frame = MyFrame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=2)

        MyButton(btn_frame, text="Обновить", command=self._refresh).pack(side=tk.LEFT, padx=5)
        MyButton(btn_frame, text="Закрыть", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        columns = ("brand", "model", "year", "plate", "price", "status")
        self.__tree = MyTree(self, columns=columns)
        self.__tree.heading("brand", text="Марка")
        self.__tree.heading("model", text="Модель")
        self.__tree.heading("year", text="Год")
        self.__tree.heading("plate", text="Номер")
        self.__tree.heading("price", text="Цена/день")
        self.__tree.heading("status", text="Статус")
        self.__tree.column("brand", width=100)
        self.__tree.column("model", width=100)
        self.__tree.column("year", width=60)
        self.__tree.column("plate", width=90)
        self.__tree.column("price", width=90)
        self.__tree.column("status", width=90)
        self.__tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._refresh()

    def _refresh(self):
        self.__tree.delete(*self.__tree.get_children())
        cars = self.__app.cars

        for c in cars:
            status = "Свободен" if not c.is_rented() else "В аренде"
            self.__tree.insert("", "end", values=(
                c.get_brand(), c.get_model(), c.get_year(),
                c.get_plate(), f"{c.get_price_per_day()} руб", status
            ))
