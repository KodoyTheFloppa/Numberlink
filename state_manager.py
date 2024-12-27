
import pickle
import os
import tkinter as tk

STATE_FILE = "numberlink_state.pkl"

def save_state(app):
    try:
        data = {
            "rows": app.rows,
            "cols": app.cols,
            "grid_numbers": app.grid_numbers,
            "walls": app.walls,
            "wall_mode": app.wall_mode,
            "number_mode": app.number_mode,
            "current_number": app.current_number,
            "history": app.history
        }
        with open(STATE_FILE, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print("Не удалось сохранить состояние:", e)

def load_state_if_exists(app):
    if not os.path.exists(STATE_FILE):
        return
    try:
        with open(STATE_FILE, "rb") as f:
            data = pickle.load(f)
        if data["rows"] == app.rows and data["cols"] == app.cols:
            app.grid_numbers = data["grid_numbers"]
            app.walls = data["walls"]
            app.wall_mode = data["wall_mode"]
            app.number_mode = data["number_mode"]
            app.current_number = data["current_number"]
            app.history = data.get("history", [])
            app.redraw_field()

            if app.number_mode:
                app.button_undo.config(state=tk.NORMAL)
                app.button_solve.config(state=tk.NORMAL)
    except Exception as e:
        print("Не удалось загрузить состояние:", e)
