import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

def newton_raphson(f_expr, df_expr, x0, num_decimals, max_iter=100, tol=1e-10):
    x = sp.symbols('x')
    f = sp.lambdify(x, f_expr, 'math')
    df = sp.lambdify(x, df_expr, 'math')

    resultados = []
    iteracion = 0

    while iteracion < max_iter:
        fx0 = f(x0)
        dfx0 = df(x0)

        # Si la derivada es 0, no podemos continuar
        if dfx0 == 0:
            return [(0, round(x0, num_decimals), round(fx0, num_decimals))]

        # Calcular el siguiente valor de x
        x1 = x0 - fx0 / dfx0
        resultados.append((iteracion, round(x0, num_decimals), round(fx0, num_decimals)))

        # Criterios de parada mejorados:
        if abs(x1 - x0) < tol or round(x1, num_decimals) == round(x0, num_decimals):
            break

        x0 = x1
        iteracion += 1

    return resultados

def calcular():
    try:
        x0 = float(entry_x0.get())
        num_decimals = int(entry_decimals.get())
        f_expr = sp.sympify(entry_f.get())
        df_expr = sp.diff(f_expr, sp.symbols('x'))

        if num_decimals < 0:
            messagebox.showwarning("Advertencia", "Los decimales deben ser un número positivo.")
            return

        resultados = newton_raphson(f_expr, df_expr, x0, num_decimals)

        for row in tabla.get_children():
            tabla.delete(row)

        for i, x, fx in resultados:
            tabla.insert('', 'end', values=(i, x, fx))

    except Exception as e:
        messagebox.showerror("Error", f"Entrada no válida: {e}")

app = tk.Tk()
app.title("Método de Newton-Raphson")

tk.Label(app, text="f(x):").grid(row=0, column=0)
tk.Label(app, text="x0:").grid(row=1, column=0)
tk.Label(app, text="Decimales:").grid(row=2, column=0)

entry_f = tk.Entry(app)
entry_x0 = tk.Entry(app)
entry_decimals = tk.Entry(app)

entry_f.grid(row=0, column=1)
entry_x0.grid(row=1, column=1)
entry_decimals.grid(row=2, column=1)

tk.Button(app, text="Calcular", command=calcular).grid(row=3, column=0, columnspan=2)

columns = ("Iteración", "x", "f(x)")
tabla = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

tabla.grid(row=4, column=0, columnspan=2)

app.mainloop()
