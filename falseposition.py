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

def regula_falsi_method(user_equation, a, b, relative_error):
    if f(a, user_equation) * f(b, user_equation) >= 0:
        messagebox.showerror("Error", "Regula Falsi method fails.")
        return
    
    # Initialize iteration counter
    iterations = 0
    
    # Initial approximation
    c = a
    
    result_text.delete(1.0, tk.END)  # Clear previous results
    result_text.insert(tk.END, "Iteration\t\t|\t   a\t\t|\t   b\t\t|\t   Root\t\t|\tRelative Error(%)\n")
    result_text.insert(tk.END, "-"*85 + "\n")
    
    while (b - a) >= relative_error:
        # Calculate the next approximation using Regula Falsi method
        c = (a * f(b, user_equation) - b * f(a, user_equation)) / (f(b, user_equation) - f(a, user_equation))
        
        # Check if the root is found
        if f(c, user_equation) == 0.0:
            break
        
        # Calculate the relative error
        relative_error_c = abs((c - a) / c) * 100 if iterations > 0 else 0
        
        # Decide the side to repeat the steps
        if f(c, user_equation) * f(a, user_equation) < 0:
            b = c
        else:
            a = c
        
        # Print iteration details with values rounded to 4 decimal places
        result_text.insert(tk.END, f"{iterations}\t\t|\t{a:.4f}\t\t|\t{b:.4f}\t\t|\t{c:.4f}\t\t|\t{relative_error_c:.4f}%\n")
        
        # Increment iteration counter
        iterations += 1
    
    result_text.insert(tk.END, f"\nRoot is: {c:.4f}\nRelative Error: {relative_error_c:.4f}%")

def run_regula_falsi():
    user_equation = equation_entry.get()
    lower = float(lower_entry.get())
    upper = float(upper_entry.get())
    
    # Remove percentage sign and convert to float
    error_str = error_entry.get().replace('%', '')
    error = float(error_str) / 100
    
    regula_falsi_method(user_equation, lower, upper, error)

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
root.title("Regula Falsi Method App")
root.geometry('1200x800')

# Equation input
equation_frame = tk.Frame(root)
equation_frame.pack(pady=10)

equation_label = tk.Label(equation_frame, text="Equation:")
equation_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
equation_entry = tk.Entry(equation_frame, width=50, font=("Arial", 12))
equation_entry.grid(row=0, column=1, padx=10, pady=5)

# Lower bound input
lower_frame = tk.Frame(root)
lower_frame.pack(pady=5)

lower_label = tk.Label(lower_frame, text="Lower bound: (a)")
lower_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
lower_entry = tk.Entry(lower_frame, width=10, font=("Arial", 12))
lower_entry.grid(row=0, column=1, padx=10, pady=5)

# Upper bound input
upper_label = tk.Label(lower_frame, text="Upper bound: (b)")
upper_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
upper_entry = tk.Entry(lower_frame, width=10, font=("Arial", 12))
upper_entry.grid(row=0, column=3, padx=10, pady=5)

# Relative error input
error_label = tk.Label(lower_frame, text="Relative error (%):")
error_label.grid(row=0, column=4, padx=10, pady=5, sticky="e")
error_entry = tk.Entry(lower_frame, width=10, font=("Arial", 12))
error_entry.grid(row=0, column=5, padx=10, pady=5)

# Power input
power_entry = tk.Entry(lower_frame, width=10, font=("Arial", 12))

# Buttons for calculator functionality
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5)

trig_buttons = ['sin', 'cos', 'tan']
exp_button = 'exp'
squared_button = '^2'
real_numbers_1 = ['0', '1', '2', '3', '4']
real_numbers_2 = ['5', '6', '7', '8', '9', '.', '+', '-', '*', '/']

row_index = 0
column_index = 0
for trig in trig_buttons:
    button = tk.Button(buttons_frame, text=trig, command=lambda t=trig: add_to_focus(t), width=5, font=("Arial", 12))
    button.grid(row=row_index, column=column_index, padx=5, pady=5)
    column_index += 1

button = tk.Button(buttons_frame, text=exp_button, command=lambda e=exp_button: add_to_focus(e), width=5, font=("Arial", 12))
button.grid(row=row_index, column=column_index, padx=5, pady=5)
column_index += 1

button = tk.Button(buttons_frame, text=squared_button, command=lambda s=squared_button: add_to_focus(s), width=5, font=("Arial", 12))
button.grid(row=row_index, column=column_index, padx=5, pady=5)
column_index += 1

row_index += 1
column_index = 0

for num in real_numbers_1:
    button = tk.Button(buttons_frame, text=num, command=lambda n=num: add_to_focus(n), width=5, font=("Arial", 12))
    button.grid(row=row_index, column=column_index, padx=5, pady=5)
    column_index += 1

row_index += 1
column_index = 0

for num in real_numbers_2:
    button = tk.Button(buttons_frame, text=num, command=lambda n=num: add_to_focus(n), width=5, font=("Arial", 12))
    button.grid(row=row_index, column=column_index, padx=5, pady=5)
    column_index += 1
    if column_index % 5 == 0:
        row_index += 1
        column_index = 0

# Additional buttons
x_button = tk.Button(buttons_frame, text="x", command=lambda: add_to_focus('x'), width=5, font=("Arial", 12))
x_button.grid(row=row_index, column=0, padx=5, pady=5)

delete_button = tk.Button(buttons_frame, text="Delete", command=delete_last, width=5, font=("Arial", 12))
delete_button.grid(row=row_index, column=1, padx=5, pady=5)

# Parentheses buttons
open_parentheses_button = tk.Button(buttons_frame, text="(", command=lambda: add_to_focus("("), width=5, font=("Arial", 12))
open_parentheses_button.grid(row=row_index, column=2, padx=5, pady=5)

close_parentheses_button = tk.Button(buttons_frame, text=")", command=lambda: add_to_focus(")"), width=5, font=("Arial", 12))
close_parentheses_button.grid(row=row_index, column=3, padx=5, pady=5)

# Raise to power button
raise_to_power_button = tk.Button(buttons_frame, text="Raise to", command=raise_to_power, width=8, font=("Arial", 10))
raise_to_power_button.grid(row=row_index, column=4, padx=5, pady=5)

# Button to clear all fields
clear_all_button = tk.Button(buttons_frame, text="Clear All", command=clear_all, width=8, font=("Arial", 10))
clear_all_button.grid(row=row_index, column=5, padx=5, pady=5)

# Button to run the regula falsi method
run_button = tk.Button(root, text="Run Regula Falsi Method", command=run_regula_falsi, width=30, font=("Arial", 14))
run_button.pack(pady=10)

# Separator line
separator_line = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator_line.pack(fill=tk.X, padx=10, pady=5)

# Text widget to display results with increased width
result_text = tk.Text(root, height=20, width=150, font=("Arial", 12))  # Increased width
result_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Start the main event loop
root.mainloop()
