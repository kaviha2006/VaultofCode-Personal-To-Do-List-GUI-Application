import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "tasks.json"

# ---------------- File Handling ----------------

def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)

# ---------------- Task Operations ----------------

def add_task():
    title = title_entry.get().strip()
    description = desc_entry.get().strip()
    category = category_var.get()

    if not title or not description:
        messagebox.showwarning("Input Error", "Please enter title and description")
        return

    task = {
        "title": title,
        "description": description,
        "category": category,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    refresh_tasks()

    title_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)

def mark_completed():
    if not task_list.curselection():
        messagebox.showwarning("Select Task", "Please select a task")
        return

    index = task_list.curselection()[0]
    tasks[index]["completed"] = True
    save_tasks()
    refresh_tasks()

def delete_task():
    if not task_list.curselection():
        messagebox.showwarning("Select Task", "Please select a task")
        return

    index = task_list.curselection()[0]
    tasks.pop(index)
    save_tasks()
    refresh_tasks()

def refresh_tasks():
    task_list.delete(0, tk.END)
    for task in tasks:
        status = "✔ Done" if task["completed"] else "⏳ Pending"
        task_list.insert(
            tk.END,
            f"{status}  |  {task['title']}  ({task['category']})"
        )

# ---------------- GUI Setup ----------------

tasks = load_tasks()

root = tk.Tk()
root.title("Personal To-Do List")
root.geometry("520x600")
root.configure(bg="#f4f6f8")
root.resizable(False, False)

# Header
header = tk.Label(
    root,
    text="📝 Personal To-Do List",
    font=("Segoe UI", 20, "bold"),
    bg="#4f46e5",
    fg="white",
    pady=12
)
header.pack(fill="x")

# Main Card
card = tk.Frame(root, bg="white", padx=20, pady=20)
card.pack(padx=20, pady=20, fill="both", expand=True)

# Title Input
tk.Label(card, text="Task Title", font=("Segoe UI", 11), bg="white").pack(anchor="w")
title_entry = tk.Entry(card, font=("Segoe UI", 11))
title_entry.pack(fill="x", pady=6)

# Description Input
tk.Label(card, text="Description", font=("Segoe UI", 11), bg="white").pack(anchor="w")
desc_entry = tk.Entry(card, font=("Segoe UI", 11))
desc_entry.pack(fill="x", pady=6)

# Category Dropdown
tk.Label(card, text="Category", font=("Segoe UI", 11), bg="white").pack(anchor="w")
category_var = tk.StringVar(value="Work")
category_menu = tk.OptionMenu(card, category_var, "Work", "Personal", "Urgent")
category_menu.config(font=("Segoe UI", 10))
category_menu.pack(fill="x", pady=6)

# Buttons
btn_frame = tk.Frame(card, bg="white")
btn_frame.pack(pady=10)

tk.Button(
    btn_frame, text="Add Task", command=add_task,
    bg="#4f46e5", fg="white", font=("Segoe UI", 10),
    width=14
).grid(row=0, column=0, padx=6)

tk.Button(
    btn_frame, text="Mark Completed", command=mark_completed,
    bg="#16a34a", fg="white", font=("Segoe UI", 10),
    width=14
).grid(row=0, column=1, padx=6)

tk.Button(
    btn_frame, text="Delete Task", command=delete_task,
    bg="#dc2626", fg="white", font=("Segoe UI", 10),
    width=14
).grid(row=0, column=2, padx=6)

# Task List
tk.Label(card, text="Your Tasks", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", pady=(20, 5))

task_list = tk.Listbox(
    card,
    font=("Segoe UI", 11),
    height=10,
    selectbackground="#e0e7ff"
)
task_list.pack(fill="both", expand=True)

refresh_tasks()
root.mainloop()
