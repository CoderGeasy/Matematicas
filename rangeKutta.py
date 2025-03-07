import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp

def runge_kutta(f_expr, x0, y0, h, n):
    x, y = sp.symbols('x y')
    f = sp.lambdify((x, y), f_expr, 'math')
    
    resultados = []
    for i in range(n):
        k1 = h * f(x0, y0)
        k2 = h * f(x0 + h/2, y0 + k1/2)
        k3 = h * f(x0 + h/2, y0 + k2/2)
        k4 = h * f(x0 + h, y0 + k3)
        
        y0 += (k1 + 2*k2 + 2*k3 + k4) / 6
        x0 += h
        resultados.append((i, round(x0, 5), round(y0, 5), round(k1, 5), round(k2, 5), round(k3, 5), round(k4, 5)))
    
    return resultados

def calcular():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        h = float(entry_h.get())
        n = int(entry_n.get())
        ver_iteraciones = int(entry_ver_iteraciones.get())
        f_expr = sp.sympify(entry_f.get())
        
        resultados = runge_kutta(f_expr, x0, y0, h, n)
        
        for row in tabla.get_children():
            tabla.delete(row)
        
        # Mostrar solo las primeras 'ver_iteraciones' o todas si es mayor a n
        for i, x, y, k1, k2, k3, k4 in resultados[:ver_iteraciones]:
            tabla.insert('', 'end', values=(i, x, y, k1, k2, k3, k4))
    
    except Exception as e:
        messagebox.showerror("Error", f"Entrada no válida: {e}")

app = tk.Tk()
app.title("Método de Runge-Kutta")

tk.Label(app, text="x0:").grid(row=0, column=0)
tk.Label(app, text="y0:").grid(row=1, column=0)
tk.Label(app, text="h:").grid(row=2, column=0)
tk.Label(app, text="n (Total de iteraciones):").grid(row=3, column=0)
tk.Label(app, text="Mostrar iteraciones:").grid(row=4, column=0)
tk.Label(app, text="f(x, y):").grid(row=5, column=0)

entry_x0 = tk.Entry(app)
entry_y0 = tk.Entry(app)
entry_h = tk.Entry(app)
entry_n = tk.Entry(app)
entry_ver_iteraciones = tk.Entry(app)  # Nuevo campo para elegir cuántas iteraciones ver
entry_f = tk.Entry(app)

entry_x0.grid(row=0, column=1)
entry_y0.grid(row=1, column=1)
entry_h.grid(row=2, column=1)
entry_n.grid(row=3, column=1)
entry_ver_iteraciones.grid(row=4, column=1)  # Posicionamos la nueva entrada
entry_f.grid(row=5, column=1)

tk.Button(app, text="Calcular", command=calcular).grid(row=6, column=0, columnspan=2)

columns = ("Iteración", "x", "y", "k1", "k2", "k3", "k4")
tabla = ttk.Treeview(app, columns=columns, show="headings")
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, width=100)

tabla.grid(row=7, column=0, columnspan=2)
app.mainloop()
