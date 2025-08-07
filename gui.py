import os
import subprocess
import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

SCRIPT_PATH = Path(__file__).parent / "scripts" / "user_ops.sh"

def run_script(args):
    if not SCRIPT_PATH.exists():
        return False, f"Script not found: {SCRIPT_PATH}"
    try:
        result = subprocess.run([str(SCRIPT_PATH)] + args, check=True, text=True, capture_output=True)
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

# ---- GUI Functions ----
def add_user():
    user = simpledialog.askstring("Add User", "Enter username:")
    if user:
        show(run_script(["add_user", user]))

def remove_user():
    user = simpledialog.askstring("Remove User", "Enter username:")
    if user:
        show(run_script(["remove_user", user]))

def add_group():
    group = simpledialog.askstring("Add Group", "Enter group name:")
    if group:
        show(run_script(["add_group", group]))

def remove_group():
    group = simpledialog.askstring("Remove Group", "Enter group name:")
    if group:
        show(run_script(["remove_group", group]))

def list_users():
    success, output = run_script(["list_users"])
    show((success, output))

def list_groups():
    success, output = run_script(["list_groups"])
    show((success, output))

def change_password():
    user = simpledialog.askstring("Change Password", "Enter username:")
    password = simpledialog.askstring("Change Password", "Enter new password:", show="*")
    if user and password:
        show(run_script(["change_password", user, password]))

def add_user_to_group():
    user = simpledialog.askstring("Add to Group", "Enter username:")
    group = simpledialog.askstring("Add to Group", "Enter group name:")
    if user and group:
        show(run_script(["add_user_to_group", user, group]))

def chmod():
    perm = simpledialog.askstring("chmod", "Enter permission code (e.g. 755):")
    path = simpledialog.askstring("chmod", "Enter file/directory path:")
    if perm and path:
        show(run_script(["chmod", perm, path]))

def chown():
    owner = simpledialog.askstring("chown", "Enter new owner (e.g. user or user:group):")
    path = simpledialog.askstring("chown", "Enter file/directory path:")
    if owner and path:
        show(run_script(["chown", owner, path]))

def show(result):
    success, output = result
    messagebox.showinfo("Result", output if success else f"Error: {output}")

# ---- Main Window ----
def main():
    root = tk.Tk()
    root.title("User & Permissions Manager")
    root.attributes('-fullscreen', True)


    options = [
        ("Add User", add_user),
        ("Remove User", remove_user),
        ("Add Group", add_group),
        ("Remove Group", remove_group),
        ("List Users", list_users),
        ("List Groups", list_groups),
        ("Change Password", change_password),
        ("Add User to Group", add_user_to_group),
        ("Set Permissions (chmod)", chmod),
        ("Change Owner (chown)", chown),
        ("Exit", root.destroy)
    ]

    for label, func in options:
        tk.Button(root, text=label, command=func, width=30).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

