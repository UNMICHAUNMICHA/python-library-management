import tkinter as tk
from tkinter import messagebox, font
from tkinter import ttk

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

    def __str__(self):
        return f"{self.title} by {self.author}"

class User:
    def __init__(self, name):
        self.name = name
        self.checked_out_books = []

    def __str__(self):
        return self.name

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.populate_initial_books()

    def populate_initial_books(self):
        initial_books = [
            ("The Great Gatsby", "F. Scott", "0001"),
            ("To Kill a Mockingbird", "Harper", "0002"),
            ("1984", "George Orwell", "0003"),
            ("Pride and Prejudice", "Jane Austen", "0004"),
            ("The Catcher in the Rye", "J.D.", "0005"),
        ]
        for title, author, isbn in initial_books:
            self.add_book(title, author, isbn)

    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books[isbn] = book
        return f"Added book: {book}"

    def add_user(self, name):
        user = User(name)
        self.users[name] = user
        return f"Added user: {user}"

    def search_books(self, query):
        results = []
        for book in self.books.values():
            if query.lower() in book.title.lower() or query.lower() in book.author.lower():
                results.append(book)
        return results

    def checkout_book(self, user, isbn):
        if isbn not in self.books:
            return "Book not found."
        book = self.books[isbn]
        if book.checked_out:
            return "Book is already checked out."
        user.checked_out_books.append(book)
        book.checked_out = True
        return f"{user} has checked out {book}."

    def return_book(self, user, isbn):
        if isbn not in self.books:
            return "Book not found."
        book = self.books[isbn]
        if book not in user.checked_out_books:
            return f"{user} does not have this book checked out."
        user.checked_out_books.remove(book)
        book.checked_out = False
        return f"{user} has returned {book}."

    def display_checked_out_books(self, user):
        return [str(book) for book in user.checked_out_books]

class LibraryApp:
    def __init__(self, master):
        self.master = master
        self.library = Library()
        self.master.title("Library Management System")
        self.master.configure(bg="#D3D3D3")  # สีพื้นหลังเทา

        self.custom_font = font.Font(family="Helvetica", size=12)

        # Frame สำหรับการแสดงผล
        self.display_frame = tk.Frame(master, bg="#D3D3D3")
        self.display_frame.pack(pady=10)

        self.display = tk.Text(self.display_frame, height=15, width=50, font=self.custom_font, bg="white", fg="black")  # เปลี่ยนพื้นหลังเป็นขาว
        self.display.pack(padx=10, pady=10)

        # Frame สำหรับการกรอกข้อมูล
        self.entry_frame = tk.Frame(master, bg="#D3D3D3")
        self.entry_frame.pack(pady=10)

        self.entry = tk.Entry(self.entry_frame, width=50, font=self.custom_font)
        self.entry.pack(padx=10, pady=5)

        # Frame สำหรับปุ่ม
        self.button_frame = tk.Frame(master, bg="#D3D3D3")
        self.button_frame.pack(pady=10)

        # สร้างปุ่มด้วย ttk.Button
        self.create_button("Add Book", self.add_book)
        self.create_button("Add User", self.add_user)
        self.create_button("Search Books", self.search_books)
        self.create_button("Checkout Book", self.checkout_book)
        self.create_button("Return Book", self.return_book)
        self.create_button("Display Checked Out", self.display_checked_out_books)
        self.create_button("Display All Books", self.display_all_books)

        self.update_display("Welcome to the Library Management System!")

    def create_button(self, text, command):
        button = ttk.Button(self.button_frame, text=text, command=command)
        button.pack(pady=5, padx=10, fill=tk.X)
        style = ttk.Style()
        style.configure("TButton", borderwidth=5, relief="flat", padding=10, background="white", foreground="black")
        style.map("TButton", background=[("active", "white")])  # เปลี่ยนสีเมื่อกดปุ่ม

    def add_book(self):
        data = self.entry.get().split(',')
        if len(data) == 3:
            title, author, isbn = data
            message = self.library.add_book(title.strip(), author.strip(), isbn.strip())
            self.show_message("Success", message)
            self.entry.delete(0, tk.END)
        else:
            self.show_message("Error", "Please enter title, author, and ISBN separated by commas.")

    def add_user(self):
        name = self.entry.get()
        if name:
            message = self.library.add_user(name.strip())
            self.show_message("Success", message)
            self.entry.delete(0, tk.END)
        else:
            self.show_message("Error", "Please enter a user name.")

    def search_books(self):
        query = self.entry.get()
        results = self.library.search_books(query)
        if results:
            self.update_display("Search results:\n" + "\n".join(str(book) for book in results))
        else:
            self.update_display("No matching books found.")

    def checkout_book(self):
        data = self.entry.get().split(',')
        if len(data) == 2:
            user_name, isbn = data
            user = self.library.users.get(user_name.strip())
            if user:
                message = self.library.checkout_book(user, isbn.strip())
                self.show_message("Success", message)
            else:
                self.show_message("Error", "User not found.")
        else:
            self.show_message("Error", "Please enter user name and ISBN separated by commas.")

    def return_book(self):
        data = self.entry.get().split(',')
        if len(data) == 2:
            user_name, isbn = data
            user = self.library.users.get(user_name.strip())
            if user:
                message = self.library.return_book(user, isbn.strip())
                self.show_message("Success", message)
            else:
                self.show_message("Error", "User not found.")
        else:
            self.show_message("Error", "Please enter user name and ISBN separated by commas.")

    def display_checked_out_books(self):
        user_name = self.entry.get()
        user = self.library.users.get(user_name.strip())
        if user:
            books = self.library.display_checked_out_books(user)
            if books:
                self.update_display(f"{user} has checked out the following books:\n" + "\n".join(books))
            else:
                self.update_display(f"{user} has no books checked out.")
        else:
            self.show_message("Error", "User not found.")

    def display_all_books(self):
        if self.library.books:
            books_info = "\n".join(f"ชื่อหนังสือ: {book.title}, ผู้แต่ง: {book.author}, ISBN: {book.isbn}" for book in self.library.books.values())
            self.update_display("รายการหนังสือทั้งหมด:\n" + books_info)
        else:
            self.update_display("ไม่มีหนังสือในห้องสมุด.")

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def update_display(self, message):
        self.display.delete(1.0, tk.END)
        help_message = (
            "วิธีการกรอกข้อมูล:\n"
            "1. Add Book: ชื่อหนังสือ, ผู้แต่ง, รหัส\n"
            "2. Add User: ชื่อผู้ใช้\n"
            "3. Search Books: ชื่อหนังสือหรือผู้แต่ง\n"
            "4. Checkout Book: ชื่อผู้ใช้, รหัส\n"
            "5. Return Book: ชื่อผู้ใช้, รหัส\n"
            "6. Display Check Out: ชื่อผู้ใช้\n"
            "7. Display All Book: กดปุ่ม 'Display All Books'\n\n"
        )
        self.display.insert(tk.END, help_message + message)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
