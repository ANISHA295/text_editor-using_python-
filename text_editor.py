import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font, ttk
import os

class AdvancedTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Text Editor")
        self.file_path = None
        
        # Set default font
        self.current_font = ("Arial", 12)
        
        # Create main text area
        self.text_area = tk.Text(root, undo=True, font=self.current_font, wrap="word")
        self.text_area.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)
        
        # Adding Scrollbar
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)
        
        # Creating a Menu Bar
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit, accelerator="Ctrl+Q")
        
        # Edit Menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        edit_menu.add_command(label="Undo", command=lambda: self.text_area.event_generate("<<Undo>>"), accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=lambda: self.text_area.event_generate("<<Redo>>"), accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find & Replace", command=self.find_replace, accelerator="Ctrl+F")
        
        # Font Menu
        font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Font", menu=font_menu)
        font_menu.add_command(label="Change Font", command=self.change_font)
        
        # Theme Menu
        theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Theme", menu=theme_menu)
        theme_menu.add_command(label="Light Mode", command=lambda: self.change_theme("light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.change_theme("dark"))
        
        # Status Bar
        self.status_bar = tk.Label(root, text="Words: 0 | Characters: 0", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_area.bind("<KeyRelease>", self.update_status)

        # Keyboard Shortcuts
        root.bind("<Control-n>", lambda event: self.new_file())
        root.bind("<Control-o>", lambda event: self.open_file())
        root.bind("<Control-s>", lambda event: self.save_file())
        root.bind("<Control-Shift-S>", lambda event: self.save_as())
        root.bind("<Control-q>", lambda event: root.quit())
        root.bind("<Control-f>", lambda event: self.find_replace())

        self.auto_save_enabled = True
        self.auto_save()

    def new_file(self):
        """Create a new file."""
        if messagebox.askyesno("New File", "Do you want to save changes before creating a new file?"):
            self.save_file()
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Untitled - Advanced Text Editor")

    def open_file(self):
        """Open an existing file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.root.title(os.path.basename(self.file_path) + " - Advanced Text Editor")
            self.update_status()

    def save_file(self):
        """Save the current file."""
        if not self.file_path:
            self.save_as()
        else:
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Save", "File saved successfully.")

    def save_as(self):
        """Save the file with a new name."""
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.file_path:
            self.save_file()

    def find_replace(self):
        """Find and replace functionality."""
        find_window = tk.Toplevel(self.root)
        find_window.title("Find & Replace")
        find_window.geometry("300x150")

        tk.Label(find_window, text="Find:").pack()
        find_entry = tk.Entry(find_window, width=30)
        find_entry.pack()

        tk.Label(find_window, text="Replace:").pack()
        replace_entry = tk.Entry(find_window, width=30)
        replace_entry.pack()

        def replace_text():
            find_text = find_entry.get()
            replace_text = replace_entry.get()
            content = self.text_area.get(1.0, tk.END)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content.replace(find_text, replace_text))

        tk.Button(find_window, text="Replace", command=replace_text).pack()

    def change_font(self):
        """Change the font of the text."""
        font_name = simpledialog.askstring("Font", "Enter Font Name (e.g., Arial):")
        font_size = simpledialog.askinteger("Size", "Enter Font Size:", minvalue=8, maxvalue=50)
        if font_name and font_size:
            self.current_font = (font_name, font_size)
            self.text_area.config(font=self.current_font)

    def change_theme(self, mode):
        """Switch between light and dark modes."""
        if mode == "dark":
            self.text_area.config(bg="black", fg="white", insertbackground="white")
        else:
            self.text_area.config(bg="white", fg="black", insertbackground="black")

    def update_status(self, event=None):
        """Update word and character count."""
        text_content = self.text_area.get(1.0, tk.END)
        words = len(text_content.split())
        chars = len(text_content) - 1  # Exclude final newline
        self.status_bar.config(text=f"Words: {words} | Characters: {chars}")

    def auto_save(self):
        """Automatically save file every 30 seconds."""
        if self.auto_save_enabled and self.file_path:
            self.save_file()
        self.root.after(30000, self.auto_save)  # Every 30 seconds

if __name__ == "__main__":
    root = tk.Tk()
    editor = AdvancedTextEditor(root)
    root.geometry("800x600")
    root.mainloop()
