import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

def euler_mejorado(f_expr, x0, y0, h, n_max):
    x, y = sp.symbols('x y')
    f = sp.lambdify((x, y), f_expr, 'math')

    resultados = []
    iteracion = 0

    while x0 < n_max:  
        if x0 + h > n_max:  
            h = n_max - x0  # Ajustar el último paso para no pasarse

        y_pred = y0 + h * f(x0, y0)
        y_corr = y0 + (h / 2) * (f(x0, y0) + f(x0 + h, y_pred))
        error = abs(y_corr - y0)

        resultados.append((iteracion, round(x0, 5), round(y0, 5), round(y_corr, 5), round(error, 5)))

        x0 += h
        y0 = y_corr  
        iteracion += 1

    return resultados

def calcular():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        h = float(entry_h.get())
        n_max = float(entry_nmax.get())  
        f_expr = sp.sympify(entry_f.get())

        if h <= 0:
            messagebox.showwarning("Advertencia", "El paso h debe ser mayor que 0.")
            return
        if n_max <= x0:
            messagebox.showwarning("Advertencia", "El valor final de x debe ser mayor que x0.")
            return

        resultados = euler_mejorado(f_expr, x0, y0, h, n_max)

        for row in tabla.get_children():
            tabla.delete(row)
        
        for i, x, y, y_next, error in resultados:
            tabla.insert('', 'end', values=(i, x, y, y_next, error))

    except Exception as e:
        messagebox.showerror("Error", f"Entrada no válida: {e}")

app = tk.Tk()
app.title("Método de Euler Mejorado")

tk.Label(app, text="x0:").grid(row=0, column=0)
tk.Label(app, text="y0:").grid(row=1, column=0)
tk.Label(app, text="h (paso):").grid(row=2, column=0)
tk.Label(app, text="Valor final de x (n_max):").grid(row=3, column=0)  
tk.Label(app, text="f(x, y):").grid(row=4, column=0)

entry_x0 = tk.Entry(app)
entry_y0 = tk.Entry(app)
entry_h = tk.Entry(app)
entry_nmax = tk.Entry(app)
entry_f = tk.Entry(app)

entry_x0.grid(row=0, column=1)
entry_y0.grid(row=1, column=1)
entry_h.grid(row=2, column=1)
entry_nmax.grid(row=3, column=1)
entry_f.grid(row=4, column=1)

tk.Button(app, text="Calcular", command=calcular).grid(row=5, column=0, columnspan=2)

columns = ("Iteración", "x", "y", "y_siguiente", "Error")
tabla = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

tabla.grid(row=6, column=0, columnspan=2)

app.mainloop()
