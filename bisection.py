import tkinter as tk
from tkinter import messagebox
import math
import re

def f(x, user_equation):
    # Replace the operators to handle expressions like "sin(x)3"
    user_equation = re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', user_equation)
    user_equation = re.sub(r'([a-zA-Z])(\d+)', r'\1*\2', user_equation)
    user_equation = user_equation.replace('^', '**')  # Replace ^ with ** for exponentiation
    # Define your function here
    return eval(user_equation.replace('x', str(x)), {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'exp': math.exp, 'sqrt': math.sqrt})

def bisection_method(user_equation, a, b, relative_error):
    if f(a, user_equation) * f(b, user_equation) >= 0:
        messagebox.showerror("Error", "Bisection method fails.")
        return
    
    # Initialize iteration counter
    iterations = 0
    
    # Initial approximation
    c = a
    
    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.END, "Iteration\t a\t\t\t b\t\t\t c\t\t\t f(c)\n")
    
    while (b - a) >= relative_error:
        # Find the midpoint
        c = (a + b) / 2
        
        # Check if the root is found
        if f(c, user_equation) == 0.0:
            break
        
        # Decide the side to repeat the steps
        if f(c, user_equation) * f(a, user_equation) < 0:
            b = c
        else:
            a = c
        
        # Print iteration details with values rounded to 4 decimal places
        result_text.insert(tk.END, f"{iterations}\t\t {a:.4f}\t\t {b:.4f}\t\t {c:.4f}\t\t {f(c, user_equation):.4f}\n")
        
        # Increment iteration counter
        iterations += 1
    
    result_text.insert(tk.END, f"\nRoot is: {c:.4f}\nIterations: {iterations}")

def run_bisection():
    user_equation = equation_entry.get()
    lower = float(lower_entry.get())
    upper = float(upper_entry.get())
    
    # Remove percentage sign and convert to float
    error_str = error_entry.get().replace('%', '')
    error = float(error_str) / 100
    
    bisection_method(user_equation, lower, upper, error)

def add_to_focus(symbol):
    focus = root.focus_get()
    if focus == equation_entry or focus == lower_entry or focus == upper_entry or focus == error_entry or focus == power_entry:
        focus.insert(tk.END, symbol)
    else:
        equation_entry.focus_set()
        equation_entry.insert(tk.END, symbol)

def delete_last():
    focus = root.focus_get()
    if focus == equation_entry or focus == lower_entry or focus == upper_entry or focus == error_entry or focus == power_entry:
        focus.delete(len(focus.get()) - 1)

def add_parentheses(parentheses):
    add_to_focus(parentheses)

def raise_to_power():
    power = power_entry.get()
    add_to_focus(f"^{power}")

def clear_all():
    equation_entry.delete(0, tk.END)
    lower_entry.delete(0, tk.END)
    upper_entry.delete(0, tk.END)
    error_entry.delete(0, tk.END)
    power_entry.delete(0, tk.END)
    result_text.delete(1.0, tk.END)

# Create the main window
root = tk.Tk()
root.title("Bisection Method App")

# Equation input
equation_frame = tk.Frame(root)
equation_frame.grid(row=0, column=0, columnspan=6, padx=10, pady=5, sticky="ew")

equation_label = tk.Label(equation_frame, text="Equation:")
equation_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
equation_entry = tk.Entry(equation_frame)
equation_entry.grid(row=0, column=1, columnspan=4, padx=10, pady=5, sticky="ew")

# Lower bound input
lower_frame = tk.Frame(root)
lower_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

lower_label = tk.Label(lower_frame, text="Lower bound:")
lower_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
lower_entry = tk.Entry(lower_frame)
lower_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

# Upper bound input
upper_label = tk.Label(lower_frame, text="Upper bound:")
upper_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
upper_entry = tk.Entry(lower_frame)
upper_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

# Relative error input
error_label = tk.Label(lower_frame, text="Relative error (%):")
error_label.grid(row=0, column=4, padx=10, pady=5, sticky="e")
error_entry = tk.Entry(lower_frame)
error_entry.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

# Power input
power_label = tk.Label(lower_frame, text="Raise to power:")
power_label.grid(row=0, column=6, padx=10, pady=5, sticky="e")
power_entry = tk.Entry(lower_frame)
power_entry.grid(row=0, column=7, padx=10, pady=5, sticky="ew")

# Buttons for calculator functionality
buttons_frame = tk.Frame(root)
buttons_frame.grid(row=2, column=0, columnspan=6, padx=10, pady=5, sticky="ew")

trig_buttons = ['sin', 'cos', 'tan']
exp_button = 'exp'
squared_button = '^2'
real_numbers = [str(i) for i in range(10)] + ['.', '+', '-', '*', '/']

row_index = 0
column_index = 0
for trig in trig_buttons:
    button = tk.Button(buttons_frame, text=trig, command=lambda t=trig: add_to_focus(t))
    button.grid(row=row_index, column=column_index, padx=5, pady=5)
    column_index += 1

button = tk.Button(buttons_frame, text=exp_button, command=lambda e=exp_button: add_to_focus(e))
button.grid(row=row_index, column=column_index, padx=5, pady=5)
column_index += 1

button = tk.Button(buttons_frame, text=squared_button, command=lambda s=squared_button: add_to_focus(s))
button.grid(row=row_index, column=column_index, padx=5, pady=5)
column_index += 1

for num in real_numbers:
    button = tk.Button(buttons_frame, text=num, command=lambda n=num: add_to_focus(n))
    button.grid(row=row_index, column=column_index, padx=5, pady=5)
    column_index += 1
    if column_index % 5 == 0:
        row_index += 1
        column_index = 0

# Additional buttons
x_button = tk.Button(buttons_frame, text="x", command=lambda: add_to_focus('x'))
x_button.grid(row=row_index, column=0, padx=5, pady=5)

delete_button = tk.Button(buttons_frame, text="Delete", command=delete_last)
delete_button.grid(row=row_index, column=1, padx=5, pady=5)

# Parentheses buttons
open_parentheses_button = tk.Button(buttons_frame, text="(", command=lambda: add_to_focus("("))
open_parentheses_button.grid(row=row_index, column=2, padx=5, pady=5)

close_parentheses_button = tk.Button(buttons_frame, text=")", command=lambda: add_to_focus(")"))
close_parentheses_button.grid(row=row_index, column=3, padx=5, pady=5)

# Raise to power button
raise_to_power_button = tk.Button(buttons_frame, text="Raise to", command=raise_to_power)
raise_to_power_button.grid(row=row_index, column=4, padx=5, pady=5)

# Button to clear all fields
clear_all_button = tk.Button(buttons_frame, text="Clear All", command=clear_all)
clear_all_button.grid(row=row_index, column=5, padx=5, pady=5)

# Button to run the bisection method
run_button = tk.Button(root, text="Run Bisection Method", command=run_bisection)
run_button.grid(row=3, column=0, columnspan=6, padx=10, pady=5, sticky="ew")

# Text widget to display results with increased width
result_text = tk.Text(root, height=20, width=100)  # Increased width
result_text.grid(row=4, column=0, columnspan=6, padx=10, pady=5, sticky="nsew")

# Configure row and column weights to make the text widget expandable
for i in range(5):
    root.grid_rowconfigure(i, weight=1)
for i in range(6):
    root.grid_columnconfigure(i, weight=1)

# Start the main event loop
root.mainloop()
