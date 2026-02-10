class Book:
    def __init__(self, book_id, title, author, isbn, price, status="Available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.status = status

    def __str__(self):
        return f"ID: {self.book_id}, {self.title} by {self.author} [{self.status}]"


class User:
    def __init__(self, user_id, name, email, phone):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []

    def __str__(self):
        return f"ID: {self.user_id}, {self.name} ({self.email})"


class Transaction:
    def __init__(self, trans_id, user_id, book_id, issue_date, return_date=None, fine=0):
        self.trans_id = trans_id
        self.user_id = user_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.return_date = return_date
        self.fine = fine


class LibraryManagementSystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.transactions = []
        self.next_book_id = 1
        self.next_user_id = 1
        self.next_trans_id = 1

    # ADMIN OPERATIONS
    def add_book(self, title, author, isbn, price):
        book = Book(self.next_book_id, title, author, isbn, price)
        self.books.append(book)
        self.next_book_id += 1
        print(f"✅ Book '{title}' added successfully!")

    def register_user(self, name, email, phone):
        user = User(self.next_user_id, name, email, phone)
        self.users.append(user)
        self.next_user_id += 1
        print(f"✅ User '{name}' registered!")

    def list_all_books(self):
        if not self.books:
            print("📚 No books available")
            return
        print("\n📚 ALL BOOKS:")
        for book in self.books:
            print(book)

    def list_users(self):
        if not self.users:
            print("👥 No users registered")
            return
        print("\n👥 ALL USERS:")
        for user in self.users:
            print(user)

    # USER OPERATIONS
    def search_book(self, title_or_author):
        results = [b for b in self.books if title_or_author.lower() in
                   (b.title.lower() or b.author.lower())]
        if results:
            print(f"\n🔍 SEARCH RESULTS for '{title_or_author}':")
            for book in results:
                print(book)
        else:
            print("❌ No books found")

    def issue_book(self, user_id, book_id):
        user = next((u for u in self.users if u.user_id == user_id), None)
        book = next((b for b in self.books if b.book_id == book_id), None)

        if not user or not book:
            print("❌ Invalid User ID or Book ID")
            return

        if book.status != "Available":
            print("❌ Book not available")
            return

        # Create transaction
        trans = Transaction(self.next_trans_id, user_id, book_id, "2026-01-29")
        self.transactions.append(trans)
        self.next_trans_id += 1

        book.status = "Issued"
        user.borrowed_books.append(book_id)

        print(f"✅ Book issued to {user.name}")

    def return_book(self, trans_id):
        trans = next((t for t in self.transactions if t.trans_id == trans_id), None)
        if not trans:
            print("❌ Invalid Transaction ID")
            return

        book = next((b for b in self.books if b.book_id == trans.book_id), None)
        if not book:
            print("❌ Book not found")
            return

        book.status = "Available"
        trans.return_date = "2026-02-05"
        trans.fine = 5.0  # Example fine

        # Remove from user's borrowed list
        user = next(u for u in self.users if u.user_id == trans.user_id)
        if trans.book_id in user.borrowed_books:
            user.borrowed_books.remove(trans.book_id)

        print(f"✅ Book returned. Fine: ${trans.fine}")

    def show_user_books(self, user_id):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if not user:
            print("❌ User not found")
            return

        print(f"\n📖 Books borrowed by {user.name}:")
        for book_id in user.borrowed_books:
            book = next(b for b in self.books if b.book_id == book_id)
            print(f"  - {book}")

    # DISPLAY MENU
    def display_menu(self):
        print("\n" + "=" * 50)
        print("🏛️  LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1.  📚 Add Book")
        print("2.  👥 Register User")
        print("3.  📋 List All Books")
        print("4.  📋 List All Users")
        print("5.  🔍 Search Book")
        print("6.  📤 Issue Book")
        print("7.  📥 Return Book")
        print("8.  📖 View User Books")
        print("0.  ❌ Exit")
        print("=" * 50)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter choice (0-8): ").strip()

            if choice == '1':
                title = input("Book Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                price = float(input("Price: "))
                self.add_book(title, author, isbn, price)

            elif choice == '2':
                name = input("User Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                self.register_user(name, email, phone)

            elif choice == '3':
                self.list_all_books()

            elif choice == '4':
                self.list_users()

            elif choice == '5':
                search_term = input("Search by title/author: ")
                self.search_book(search_term)

            elif choice == '6':
                user_id = int(input("User ID: "))
                book_id = int(input("Book ID: "))
                self.issue_book(user_id, book_id)

            elif choice == '7':
                trans_id = int(input("Transaction ID: "))
                self.return_book(trans_id)

            elif choice == '8':
                user_id = int(input("User ID: "))
                self.show_user_books(user_id)

            elif choice == '0':
                print("👋 Thank you for using Library Management System!")
                break

            else:
                print("❌ Invalid choice!")

            input("\nPress Enter to continue...")


# RUN THE SYSTEM
if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run()
