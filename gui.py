import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
import subprocess
from pathlib import Path

SCRIPT_PATH = Path("/root/project3/scripts/user_ops.sh")

def run_script(args, input_text=None):
    try:
        result = subprocess.run(
            [str(SCRIPT_PATH)] + args,
            input=input_text,
            check=True,
            text=True,
            capture_output=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def show(result):
    success, message = result
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def add_user():
    user = simpledialog.askstring("Input", "Enter username:")
    if user:
        show(run_script(["add_user", user]))

def delete_user():
    user = simpledialog.askstring("Input", "Enter username to delete:")
    if user:
        show(run_script(["remove_user", user]))

def change_password():
    user = simpledialog.askstring("Input", "Enter username:")
    if not user:
        return
    password = simpledialog.askstring("Input", "Enter new password:", show="*")
    if password:
        show(run_script(["change_password", user], input_text=password))

def add_group():
    group = simpledialog.askstring("Input", "Enter group name:")
    if group:
        show(run_script(["add_group", group]))

def delete_group():
    group = simpledialog.askstring("Input", "Enter group name to delete:")
    if group:
        show(run_script(["remove_group", group]))

def add_user_to_group():
    user = simpledialog.askstring("Input", "Enter username:")
    group = simpledialog.askstring("Input", "Enter group name:")
    if user and group:
        show(run_script(["add_user_to_group", user, group]))

def change_permissions():
    filepath = simpledialog.askstring("Input", "Enter permissions (e.g. 755):")
    permissions = simpledialog.askstring("Input", "Enter full path to file:")
    if filepath and permissions:
        show(run_script(["chmod", filepath, permissions]))

def list_users(root):
    success, output = run_script(["list_users"])
    if success:
        show_scrolled_output("List of Users", output, root)
    else:
        messagebox.showerror("Error", output)

def list_groups(root):
    success, output = run_script(["list_groups"])
    if success:
        show_scrolled_output("List of Groups", output, root)
    else:
        messagebox.showerror("Error", output)

def show_scrolled_output(title, content, root):
    top = tk.Toplevel(root)
    top.title(title)
    text_area = scrolledtext.ScrolledText(top, wrap=tk.WORD, width=80, height=30)
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10)

def main():
    root = tk.Tk()
    root.title("User & Permissions Manager")
    root.attributes('-fullscreen', True)

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # GUI elements
    tk.Label(scrollable_frame, text="User & Permissions Manager", font=("Arial", 24)).pack(pady=10)

    tk.Label(scrollable_frame, text="User Management", font=("Arial", 16)).pack(pady=5)
    tk.Button(scrollable_frame, text="Add User", command=add_user).pack(pady=3)
    tk.Button(scrollable_frame, text="Delete User", command=delete_user).pack(pady=3)
    tk.Button(scrollable_frame, text="Change User Password", command=change_password).pack(pady=3)

    tk.Label(scrollable_frame, text="Group Management", font=("Arial", 16)).pack(pady=5)
    tk.Button(scrollable_frame, text="Add Group", command=add_group).pack(pady=3)
    tk.Button(scrollable_frame, text="Delete Group", command=delete_group).pack(pady=3)
    tk.Button(scrollable_frame, text="Add User to Group", command=add_user_to_group).pack(pady=3)

    tk.Label(scrollable_frame, text="Permissions", font=("Arial", 16)).pack(pady=5)
    tk.Button(scrollable_frame, text="Change File Permissions", command=change_permissions).pack(pady=3)

    tk.Label(scrollable_frame, text="View Info", font=("Arial", 16)).pack(pady=5)
    tk.Button(scrollable_frame, text="List Users", command=lambda: list_users(root)).pack(pady=3)
    tk.Button(scrollable_frame, text="List Groups", command=lambda: list_groups(root)).pack(pady=3)

    # Exit button (always at bottom)
    tk.Button(scrollable_frame, text="Exit", command=root.destroy, bg="red", fg="white").pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

