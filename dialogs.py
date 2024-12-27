import tkinter as tk
from tkinter import messagebox

class GridSizeDialog:
    def __init__(self, on_generate):
        self.on_generate = on_generate

        self.dialog = tk.Tk()
        self.dialog.title("Ввод размеров")

        self.rows_var = tk.StringVar()
        self.cols_var = tk.StringVar()

        tk.Label(self.dialog, text="Количество строк:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.dialog, textvariable=self.rows_var, width=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.dialog, text="Количество столбцов:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.dialog, textvariable=self.cols_var, width=5).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.dialog, text="Сгенерировать", command=self.generate_clicked).grid(row=2, column=0, columnspan=2, pady=10)
        self.dialog.mainloop()

    def generate_clicked(self):
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
            if rows <= 0 or cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные размеры поля.")
            return

        self.dialog.destroy()
        self.on_generate(rows, cols)
