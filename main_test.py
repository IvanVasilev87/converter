import tkinter as tk
from tkinter import ttk
from convert_funcs import options, convert


class Conversion:
    """
    just a comment to check the github how it does work
    """

    def create_some_frames(self, fatherframe, nframes, names):
        frames = []
        labels = []
        stringvars = []
        entries = []
        for i in range(nframes):
            frames.append(tk.Frame(fatherframe))
            frames[i].pack(side='left')                            # левый блок
            labels.append(tk.Label(frames[i], text=names[i]))
            labels[i].pack(side='top')
            stringvars.append(tk.StringVar())
            # stringvars[i].trace_add('write', lambda name, index, mode: computefcts[i])  # быстрая конвертация - как оптимизация кода
            entries.append(tk.Entry(frames[i], textvariable=stringvars[i]))
            entries[i].pack(side='top')
        return frames, labels, stringvars, entries

    def set_mode(self):                         # функционал вызываемой функции
        mode_num = self.mode.get()
        self.mainFrame['text'] = options[mode_num]['name']
        self.labels[0]['text'] = options[mode_num]['units'][0]
        self.labels[1]['text'] = options[mode_num]['units'][1]
        self.labels[2]['text'] = options[mode_num]['units'][2]
        self.units[0].set('')
        self.units[1].set('')
        self.units[2].set('')
        self.entries[0].focus_set()               # курсор в первый юнит и клавиша табуляции переключится

    def __init__(self, root):
        self.root = root
        self.root.title("Conversion")
        w = 512
        h = 384
        self.root.geometry("+{}+{}".format(w, h))

        self.mode = tk.IntVar()
        self.mode.set(0)

        self.mainFrame = tk.LabelFrame(root, text="Init")
        self.mainFrame.pack(side='top', expand=True, fill=tk.BOTH)

        framevars = tk.Frame(self.mainFrame, background='yellow')
        framevars.pack(side='left', expand=True, fill=tk.BOTH)  # левый блок

        tk.Label(framevars, text="Choose your desired conversion unit:", justify=tk.LEFT, padx=20).pack()
        for num, parameter in enumerate(options):
            ttk.Radiobutton(framevars,                            #набор словарей - к ключу name имя конвертируемого параметра
                           text=parameter['name'],
                           # indicatoron=0,
                           width=20,
                           # padx=20,
                           variable=self.mode,
                           command=self.set_mode,              # вызов функции
                           value=num).pack(anchor=tk.CENTER)


        names = ["U1", "U2", "U3"]
        nframes = 3
        frames, self.labels, self.units, self.entries = self.create_some_frames(framevars, nframes, names)

        self.units[0].trace_add('write', lambda name, index, mode: self.compute_one())  # быстрая конвертация - как оптимизация кода
        self.units[1].trace_add('write', lambda name, index, mode: self.compute_two())  # быстрая конвертация - как оптимизация кода
        self.units[2].trace_add('write', lambda name, index, mode: self.compute_three())  # быстрая конвертация - как оптимизация кода

        self.set_mode()                 # включение режим конвертации
        root.mainloop()

    def compute_one(self):                       # привязана к переменной в первой ячейки
        if self.root.focus_get() == self.entries[0]:   #курсор на данном окне - иначе будут процесс изменения других переменных (будет конвертация)
            unit_one, unit_two, unit_three = convert(self.mode.get(), unit_one=self.units[0].get()) # величины которые конвертируем в остальные два -
            self.units[0].set(unit_one)          # после конвертации устанавливаем значение величины
            self.units[1].set(unit_two)
            self.units[2].set(unit_three)

    def compute_two(self):
        if self.root.focus_get() == self.entries[1]:
            unit_one, unit_two, unit_three = convert(self.mode.get(), unit_two=self.units[1].get())
            self.units[0].set(unit_one)          # после конвертации устанавливаем значение величины
            self.units[1].set(unit_two)
            self.units[2].set(unit_three)

    def compute_three(self):
        if self.root.focus_get() == self.entries[2]:
            unit_one, unit_two, unit_three = convert(self.mode.get(), unit_three=self.units[2].get())
            self.units[0].set(unit_one)          # после конвертации устанавливаем значение величины
            self.units[1].set(unit_two)
            self.units[2].set(unit_three)


root = tk.Tk()
conv = Conversion(root)
