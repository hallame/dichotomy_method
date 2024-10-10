import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import time

# Global variable for the "Stop" button
stop_flag = False


# Dichotomy method for minimization with stop option
def dichotomy_method(a, b, epsilon, func):
    global stop_flag
    delta = 1e-4 * (b - a)  # Set delta to a small value relative to the interval
    iter_data = []

    while (b - a) > epsilon:
        if stop_flag:  # If the process is stopped, exit the loop
            break
        m = (a + b) / 2
        x1 = m - delta
        x2 = m + delta
        if func(x1) < func(x2):
            b = x2
        else:
            a = x1
        iter_data.append((a, b, m))  # Store iteration data for plotting
    return (a + b) / 2, iter_data


# Function to dynamically evaluate the user-entered function
def eval_func(expr):
    def func(x):
        return eval(expr, {"x": x, "np": np})  # Allow use of numpy functions in the expression

    return func


# Function to check if the function is likely unimodal
def check_unimodality(a, b, func):
    x_vals = np.linspace(a, b, 100)  # 100 points between a and b
    f_vals = np.array([func(x) for x in x_vals])

    # Check for a single minimum (detect the index where the minimum occurs)
    min_index = np.argmin(f_vals)

    # If the function decreases before the minimum and increases after it, it's likely unimodal
    if np.all(np.diff(f_vals[:min_index]) < 0) and np.all(np.diff(f_vals[min_index:]) > 0):
        return True
    else:
        return False


# Function to warn if the number of iterations could be high
def warn_if_many_iterations(a, b, epsilon):
    iterations_estimate = np.log2((b - a) / epsilon)
    if iterations_estimate > 50:
        return messagebox.askyesno(
            "Warning",
            f"The estimated number of iterations is {int(iterations_estimate)}. "
            "This may take a long time. Do you want to continue?"
        )
    return True


# Function to start the minimization process
def start_minimization():
    global stop_flag
    stop_flag = False  # Reset stop flag

    try:
        a = float(entry_a.get())  # Get lower bound
        b = float(entry_b.get())  # Get upper bound
        epsilon = float(entry_epsilon.get())  # Get precision
        func_expr = entry_function.get()  # Get the function expression
        func = eval_func(func_expr)  # Create a callable function

        # Check if the function is unimodal
        if not check_unimodality(a, b, func):
            response = messagebox.askyesno("Warning",
                                           "The function does not appear to be unimodal. Do you want to proceed anyway?")
            if not response:
                return

        # Warn the user if the number of iterations could be large
        if not warn_if_many_iterations(a, b, epsilon):
            return

        result, iterations = dichotomy_method(a, b, epsilon, func)  # Run the method

        # Plot the function and minimization process with animated steps
        plot_function_and_iterations(a, b, func, iterations, result)

    except Exception as e:
        messagebox.showerror("Error", f"Error during minimization: {e}")


# Function to stop the minimization
def stop_minimization():
    global stop_flag
    stop_flag = True  # Trigger the stop of the process


# Function to plot the function and the minimization process with animation
def plot_function_and_iterations(a, b, func, iterations, result):
    x = np.linspace(a, b, 500)
    y = [func(xi) for xi in x]

    plt.ion()  # Enable interactive mode
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Function")

    # Plot the intervals for each iteration, with a slight delay to simulate animation
    for i, (ai, bi, mi) in enumerate(iterations):
        if stop_flag:
            break  # Stop plotting if minimization is stopped

        # Plot the lines and midpoint, without excessive annotation
        ax.axvline(x=ai, color='r', linestyle='--', alpha=0.5)
        ax.axvline(x=bi, color='g', linestyle='--', alpha=0.5)
        ax.scatter(mi, func(mi), color='black')

        ax.set_title(f"Iteration {i + 1}: Interval [{ai:.6f}, {bi:.6f}]")
        plt.pause(0.5)  # Pause for 0.5 seconds to simulate a slower update
        plt.draw()

    # Final annotation of the result
    ax.scatter(result, func(result), color='blue', s=100, label=f"Approx. Minimum x = {result:.6f}")
    ax.set_title(f"Final Result: Approx. Minimum at x = {result:.6f}")
    ax.legend()
    plt.ioff()  # Turn off interactive mode
    plt.show()


# GUI with Tkinter
root = tk.Tk()
root.title("Dichotomy Minimization")

# Entry for the lower bound a
tk.Label(root, text="Lower bound a:").grid(row=0, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=0, column=1)

# Entry for the upper bound b
tk.Label(root, text="Upper bound b:").grid(row=1, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=1, column=1)

# Entry for the precision epsilon
tk.Label(root, text="Precision epsilon:").grid(row=2, column=0)
entry_epsilon = tk.Entry(root)
entry_epsilon.grid(row=2, column=1)

# Entry for the function to minimize
tk.Label(root, text="Function f(x):").grid(row=3, column=0)
entry_function = tk.Entry(root)
entry_function.grid(row=3, column=1)
entry_function.insert(0, "(x-2)**2 + 1")  # Default function provided earlier

# Button to start the minimization
start_button = tk.Button(root, text="Start Minimization", command=start_minimization)
start_button.grid(row=4, column=0, columnspan=2)

# Button to stop the minimization
stop_button = tk.Button(root, text="Stop", command=stop_minimization)
stop_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
