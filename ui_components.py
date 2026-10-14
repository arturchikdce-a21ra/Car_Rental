import tkinter as tk
from tkinter import ttk


class MyLabel(tk.Label):
    def __init__(self, master, **kw):
        kw.setdefault("anchor", "w")
        super().__init__(master, **kw)


class MyButton(tk.Button):
    def __init__(self, master, **kw):
        kw.setdefault("padx", 5)
        kw.setdefault("pady", 2)
        super().__init__(master, **kw)


class MyEntry(tk.Entry):
    def __init__(self, master, **kw):
        kw.setdefault("width", 20)
        super().__init__(master, **kw)


class MyFrame(tk.Frame):
    def __init__(self, master, **kw):
        kw.setdefault("padx", 5)
        kw.setdefault("pady", 3)
        super().__init__(master, **kw)


class MyTree(ttk.Treeview):
    def __init__(self, master, **kw):
        kw.setdefault("show", "headings")
        super().__init__(master, **kw)


class MyCombo(ttk.Combobox):
    def __init__(self, master, **kw):
        kw.setdefault("state", "readonly")
        kw.setdefault("width", 18)
        super().__init__(master, **kw)


class MyCheck(tk.Checkbutton):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)


class MyRadio(tk.Radiobutton):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)


class MyList(tk.Listbox):
    def __init__(self, master, **kw):
        kw.setdefault("width", 35)
        kw.setdefault("height", 6)
        super().__init__(master, **kw)


class MyLabelFrame(tk.LabelFrame):
    def __init__(self, master, **kw):
        kw.setdefault("padx", 10)
        kw.setdefault("pady", 5)
        super().__init__(master, **kw)
