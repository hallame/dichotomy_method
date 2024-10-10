import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Variable globale pour le bouton "Stop"
stop_flag = False


# Fonction de minimisation par dichotomie avec option d'arrêt
def dichotomy_method(a, b, epsilon, func):
    global stop_flag
    delta = 1e-4 * (b - a)  # Fixer delta à une petite valeur relative à l'intervalle
    iter_data = []

    while (b - a) > epsilon:
        if stop_flag:  # Si le processus est arrêté, on sort de la boucle
            break
        m = (a + b) / 2
        x1 = m - delta
        x2 = m + delta
        if func(x1) < func(x2):
            b = x2
        else:
            a = x1
        iter_data.append((a, b, m))
    return (a + b) / 2, iter_data


# Fonction pour évaluer dynamiquement la fonction saisie par l'utilisateur
def eval_func(expr):
    def func(x):
        return eval(expr, {"x": x, "np": np})

    return func


# Fonction pour démarrer le processus de minimisation
def start_minimization():
    global stop_flag
    stop_flag = False  # Réinitialiser le drapeau d'arrêt

    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        epsilon = float(entry_epsilon.get())
        func_expr = entry_function.get()
        func = eval_func(func_expr)

        result, iterations = dichotomy_method(a, b, epsilon, func)
        messagebox.showinfo("Résultat", f"Le minimum approximatif est à x = {result:.6f}")

        # Tracer la fonction et le processus de minimisation
        plot_function_and_iterations(a, b, func, iterations)

    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la minimisation : {e}")


# Fonction pour stopper la minimisation
def stop_minimization():
    global stop_flag
    stop_flag = True  # Déclencher l'arrêt du processus


# Fonction pour tracer la fonction et le processus de minimisation
def plot_function_and_iterations(a, b, func, iterations):
    x = np.linspace(a, b, 500)
    y = [func(xi) for xi in x]

    plt.plot(x, y, label="Fonction")

    # Tracer les intervalles de chaque itération
    for i, (ai, bi, mi) in enumerate(iterations):
        plt.axvline(x=ai, color='r', linestyle='--', alpha=0.5)
        plt.axvline(x=bi, color='g', linestyle='--', alpha=0.5)
        plt.scatter(mi, func(mi), color='black')

    plt.title("Processus de minimisation par dichotomie")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.show()


# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Minimisation par dichotomie")

# Entrée pour la borne inférieure a
tk.Label(root, text="Borne inférieure a:").grid(row=0, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

# Entrée pour la borne supérieure b
tk.Label(root, text="Borne supérieure b:").grid(row=1, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1)

# Entrée pour la précision epsilon
tk.Label(root, text="Précision epsilon:").grid(row=2, column=0)
entry_epsilon = tk.Entry(root)
entry_epsilon.grid(row=2, column=1)

# Entrée pour la fonction à minimiser
tk.Label(root, text="Fonction f(x):").grid(row=3, column=0)
entry_function = tk.Entry(root)
entry_function.grid(row=3, column=1)
entry_function.insert(0, "x**2")  # Exemple par défaut

# Bouton pour démarrer la minimisation
start_button = tk.Button(root, text="Démarrer la minimisation", command=start_minimization)
start_button.grid(row=4, column=0, columnspan=2)

# Bouton pour arrêter la minimisation
stop_button = tk.Button(root, text="Arrêter", command=stop_minimization)
stop_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
