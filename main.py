import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Global flag to stop the process
stop_flag = False


# Dichotomy method with dynamic graph update
def dichotomy_method(a, b, epsilon, func_str, ax):
    global stop_flag
    delta = 1e-4 * (b - a)
    iter_data = []
    iteration_count = 0
    max_iterations = 100  # Limit for long runs

    # Convert the function string to a lambda function
    try:
        func = eval(f"lambda x: {func_str}")
    except Exception as e:
        messagebox.showerror("Function Error", f"Invalid function: {e}")
        return

    # Prepare the graph
    x = np.linspace(a, b, 500)
    y = [func(xi) for xi in x]

    ax.clear()  # Clear previous plots
    ax.plot(x, y, label="Function f(x)", color="blue")  # Plot the function curve

    # Adding titles and labels
    ax.set_title("ORMIZ: Dichotomy Method for Unconstrained Minimization")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    # Info text to display on the graph
    info_text = ax.text(0.5, 0.9, "", transform=ax.transAxes, ha="center", va="center", fontsize=10)

    while (b - a) > epsilon:
        if stop_flag:  # Stop condition
            break

        m = (a + b) / 2
        x1 = m - delta
        x2 = m + delta

        # Dichotomy decision
        if func(x1) < func(x2):
            b = x2
        else:
            a = x1

        iter_data.append((a, b, m))

        # Update the graph
        ax.axvline(x=a, color='r', linestyle='--', alpha=0.5, label="Left boundary a")  # Update left boundary
        ax.axvline(x=b, color='g', linestyle='--', alpha=0.5, label="Right boundary b")  # Update right boundary
        ax.scatter(m, func(m), color='black', label="Current midpoint")  # Mark the current midpoint

        # Update info text on the graph
        info_text.set_text(f"Current a: {a:.6f}, b: {b:.6f}, X*: {m:.6f}")

        plt.pause(0.1)

        # Check periodically to update the GUI and avoid freezing
        root.update_idletasks()

        iteration_count += 1
        if iteration_count % 100 == 0:
            root.update_idletasks()  # Allow the GUI to update

        if iteration_count > max_iterations:
            messagebox.showwarning("ORMIZ: Warning",
                                   "The number of iterations is very high. Consider increasing epsilon or reducing the interval.")
            stop_flag = True
            break

    ax.legend()  # Add legend to the graph
    return (a + b) / 2, iter_data


# Function to start the minimization
def start_minimization():
    global stop_flag
    stop_flag = False  # Reset stop flag

    try:
        # Get input values
        a = float(entry_a.get())  # Lower bound
        b = float(entry_b.get())  # Upper bound
        epsilon = float(entry_epsilon.get())  # Precision
        func_str = entry_function.get()  # Function to minimize (as string)

        # Validating input
        if a >= b:
            messagebox.showerror("Input Error", "Lower bound 'a' must be less than upper bound 'b'.")
            return
        if epsilon <= 0:
            messagebox.showerror("Input Error", "Epsilon must be a positive number.")
            return

        fig, ax = plt.subplots()  # Create a figure for the plot

        # Run the dichotomy method with live updates
        result, iterations = dichotomy_method(a, b, epsilon, func_str, ax)

        # Show the final result
        if stop_flag:
            messagebox.showinfo("ORMIZ: Result", f"Process stopped early. Approximate minimum: x = {result:.6f}")
        else:
            messagebox.showinfo("ORMIZ: Result", f"The approximate minimum is at x = {result:.6f}")

    except Exception as e:
        messagebox.showerror("ORMIZ: Error", f"Error during minimization: {e}")


# Function to stop the minimization
def stop_minimization():
    global stop_flag
    stop_flag = True


# GUI with Tkinter
root = tk.Tk()
root.title("ORMIZ: Dichotomy Minimization")

# Instructions for the user
instructions = (
    "Enter the lower bound (a), upper bound (b),\n"
    "precision (epsilon), and the function to minimize."
)
tk.Label(root, text=instructions).grid(row=0, column=0, columnspan=2)

# Entry for the lower bound a
tk.Label(root, text="Lower bound a:").grid(row=1, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=1, column=1)

# Entry for the upper bound b
tk.Label(root, text="Upper bound b:").grid(row=2, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=2, column=1)

# Entry for the precision epsilon
tk.Label(root, text="Precision epsilon:").grid(row=3, column=0)
entry_epsilon = tk.Entry(root)
entry_epsilon.grid(row=3, column=1)

# Entry for the function to minimize
tk.Label(root, text="Function to minimize (in terms of x):").grid(row=4, column=0)
entry_function = tk.Entry(root)
entry_function.grid(row=4, column=1)
entry_function.insert(0, "x**2 + 3*x + 3")  # Default function

# Button to start minimization
start_button = tk.Button(root, text="Start Minimization", command=start_minimization)
start_button.grid(row=5, column=0, columnspan=2)

# Button to stop the process
stop_button = tk.Button(root, text="Stop", command=stop_minimization)
stop_button.grid(row=6, column=0, columnspan=2)

root.mainloop()
