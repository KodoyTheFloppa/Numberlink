# app.py
import tkinter as tk
from tkinter import messagebox
import os
import pickle
from collections import deque
import solver
import state_manager

STATE_FILE = "numberlink_state.pkl"

class NumberlinkApp:
    def __init__(self, rows, cols):
        self.root = tk.Tk()
        self.root.title("Numberlink Solver")

        self.rows = rows
        self.cols = cols

        self.cell_size = 50
        self.grid_numbers = [[0] * self.cols for _ in range(self.rows)]
        self.walls = {}
        self.wall_mode = True
        self.number_mode = False
        self.current_number = 1

        self.history = []

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.button_start_numbers = tk.Button(btn_frame, text="Начать ввод чисел", command=self.start_number_input)
        self.button_start_numbers.pack(side=tk.LEFT, padx=5)

        self.button_undo = tk.Button(btn_frame, text="Возврат", command=self.undo_action, state=tk.DISABLED)
        self.button_undo.pack(side=tk.LEFT, padx=5)

        self.button_solve = tk.Button(btn_frame, text="Найти решение", command=self.solve, state=tk.DISABLED)
        self.button_solve.pack(side=tk.LEFT, padx=5)

        self.button_repeat = tk.Button(btn_frame, text="Повторить", command=self.restart)
        self.button_repeat.pack(side=tk.RIGHT, padx=5)

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side=tk.TOP, padx=5, pady=5)

        width = self.cols * self.cell_size
        height = self.rows * self.cell_size
        self.canvas.config(width=width, height=height)

        self.draw_empty_grid()

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        state_manager.load_state_if_exists(self)

        self.root.mainloop()

    def draw_empty_grid(self):
        self.canvas.delete("all")
        for r_i in range(self.rows):
            for c_i in range(self.cols):
                x1 = c_i * self.cell_size
                y1 = r_i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=1)

    def redraw_field(self):
        self.draw_empty_grid()
        for r_i in range(self.rows):
            for c_i in range(self.cols):
                val = self.grid_numbers[r_i][c_i]
                if val != 0:
                    self.draw_number(r_i, c_i, val)
        self.redraw_walls()

    def draw_number(self, r, c, val):
        x_mid = c * self.cell_size + self.cell_size // 2
        y_mid = r * self.cell_size + self.cell_size // 2
        self.canvas.create_text(
            x_mid, y_mid,
            text=str(val),
            fill="black",
            tag=f"num_{r}_{c}",
            font=("Arial", 16, "bold")
        )

    def redraw_walls(self):
        self.canvas.delete("wall_line")
        for key in self.walls:
            (r1, c1), (r2, c2) = key
            if r1 == r2:
                c_min = min(c1, c2)
                x1 = c_min * self.cell_size + self.cell_size
                y1 = r1 * self.cell_size
                x2 = x1
                y2 = y1 + self.cell_size
            else:
                r_min = min(r1, r2)
                x1 = c1 * self.cell_size
                y1 = r_min * self.cell_size + self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="black", width=4,
                tag="wall_line"
            )

    def start_number_input(self):
        self.wall_mode = False
        self.number_mode = True
        self.button_undo.config(state=tk.NORMAL)
        self.button_solve.config(state=tk.NORMAL)
        messagebox.showinfo("Режим чисел", "Теперь кликайте по клеткам, чтобы расставлять пары чисел.")

    def on_canvas_click(self, event):
        if self.rows == 0 or self.cols == 0:
            return

        c_i = event.x // self.cell_size
        r_i = event.y // self.cell_size

        if r_i < 0 or r_i >= self.rows or c_i < 0 or c_i >= self.cols:
            return

        if self.wall_mode:
            self.handle_wall_click(r_i, c_i, event)
        elif self.number_mode:
            self.handle_number_click(r_i, c_i)

    def handle_wall_click(self, r_i, c_i, event):
        threshold = 5
        x_in_cell = event.x % self.cell_size
        y_in_cell = event.y % self.cell_size

        left_edge = x_in_cell
        right_edge = self.cell_size - x_in_cell
        top_edge = y_in_cell
        bottom_edge = self.cell_size - y_in_cell

        if left_edge < threshold and c_i > 0:
            cell_a = (r_i, c_i - 1)
            cell_b = (r_i, c_i)
            self.toggle_wall(cell_a, cell_b)
        elif right_edge < threshold and c_i < self.cols - 1:
            cell_a = (r_i, c_i)
            cell_b = (r_i, c_i + 1)
            self.toggle_wall(cell_a, cell_b)
        elif top_edge < threshold and r_i > 0:
            cell_a = (r_i - 1, c_i)
            cell_b = (r_i, c_i)
            self.toggle_wall(cell_a, cell_b)
        elif bottom_edge < threshold and r_i < self.rows - 1:
            cell_a = (r_i, c_i)
            cell_b = (r_i + 1, c_i)
            self.toggle_wall(cell_a, cell_b)

        self.redraw_walls()
        state_manager.save_state(self)

    def handle_number_click(self, r_i, c_i):
        self.save_history()

        current_val = self.grid_numbers[r_i][c_i]
        if current_val != 0:
            self.grid_numbers[r_i][c_i] = 0
            self.canvas.delete(f"num_{r_i}_{c_i}")
        else:
            self.grid_numbers[r_i][c_i] = self.current_number
            self.draw_number(r_i, c_i, self.current_number)
            cnt = sum(row.count(self.current_number) for row in self.grid_numbers)
            if cnt == 2:
                self.current_number += 1

        state_manager.save_state(self)

    def toggle_wall(self, cell_a, cell_b):
        key = tuple(sorted([cell_a, cell_b]))
        if key in self.walls:
            del self.walls[key]
        else:
            self.walls[key] = True

    def save_history(self):
        snap = {
            "grid_numbers": [row[:] for row in self.grid_numbers],
            "walls": dict(self.walls),
            "current_number": self.current_number
        }
        self.history.append(snap)

    def undo_action(self):
        if not self.history:
            return
        last = self.history.pop()
        self.grid_numbers = [row[:] for row in last["grid_numbers"]]
        self.walls = dict(last["walls"])
        self.current_number = last["current_number"]
        self.redraw_field()
        state_manager.save_state(self)

    def restart(self):
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)

        self.grid_numbers = [[0] * self.cols for i in range(self.rows)]
        self.walls.clear()
        self.wall_mode = True
        self.number_mode = False
        self.current_number = 1
        self.history.clear()

        self.redraw_field()
        self.button_undo.config(state=tk.DISABLED)
        self.button_solve.config(state=tk.DISABLED)

        state_manager.save_state(self)

    def solve(self):
        solution = solver.solve_puzzle(self.rows, self.cols, self.grid_numbers, self.walls)
        if solution:
            self.show_solution(solution)
        else:
            messagebox.showinfo("Результат", "Не удалось найти решение для текущей конфигурации.")

    def show_solution(self, solution_paths):
        self.canvas.delete("path_line")

        colors = [
            "red", "blue", "magenta", "cyan", "purple",
            "yellow", "green", "orange", "gray", "brown"
        ]
        color_index = 0

        for num, path_coords in sorted(solution_paths.items(), key=lambda x: x[0]):
            color = colors[color_index % len(colors)]
            color_index += 1

            for i in range(len(path_coords) - 1):
                (r1, c1) = path_coords[i]
                (r2, c2) = path_coords[i + 1]
                x1 = c1 * self.cell_size + self.cell_size // 2
                y1 = r1 * self.cell_size + self.cell_size // 2
                x2 = c2 * self.cell_size + self.cell_size // 2
                y2 = r2 * self.cell_size + self.cell_size // 2
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill=color, width=4,
                    tag="path_line"
                )

        messagebox.showinfo("Результат", "Все пары успешно соединены!")

    def save_state(self):
        state_manager.save_state(self)
