import sqlite3
from datetime import datetime

# Connect Database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()


# Create Tables
def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        author TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issues(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        issue_date TEXT,
        return_date TEXT
    )
    """)

    conn.commit()


# Add Book
def add_book():

    name = input("Book Name: ")
    author = input("Author Name: ")

    cursor.execute("""
    INSERT INTO books(name,author,status)
    VALUES(?,?,?)
    """, (name, author, "Available"))

    conn.commit()

    print("Book Added ✅")


# View Books
def view_books():

    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()

    if not data:
        print("No Books Found ❌")
        return

    print("\nBooks List:")

    for b in data:
        print(f"ID:{b[0]} | {b[1]} | {b[2]} | {b[3]}")


# Add Member
def add_member():

    name = input("Member Name: ")
    phone = input("Phone: ")

    cursor.execute("""
    INSERT INTO members(name,phone)
    VALUES(?,?)
    """, (name, phone))

    conn.commit()

    print("Member Added ✅")


# View Members
def view_members():

    cursor.execute("SELECT * FROM members")
    data = cursor.fetchall()

    if not data:
        print("No Members ❌")
        return

    print("\nMembers List:")

    for m in data:
        print(f"ID:{m[0]} | {m[1]} | {m[2]}")


# Issue Book
def issue_book():

    book_id = input("Book ID: ")
    member_id = input("Member ID: ")

    cursor.execute("""
    SELECT status FROM books WHERE id=?
    """, (book_id,))

    book = cursor.fetchone()

    if not book:
        print("Book Not Found ❌")
        return

    if book[0] == "Issued":
        print("Book Already Issued ❌")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    INSERT INTO issues(book_id,member_id,issue_date)
    VALUES(?,?,?)
    """, (book_id, member_id, date))

    cursor.execute("""
    UPDATE books SET status="Issued" WHERE id=?
    """, (book_id,))

    conn.commit()

    print("Book Issued ✅")


# Return Book
def return_book():

    book_id = input("Book ID: ")

    cursor.execute("""
    SELECT * FROM issues
    WHERE book_id=? AND return_date IS NULL
    """, (book_id,))

    issue = cursor.fetchone()

    if not issue:
        print("No Issue Record Found ❌")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
    UPDATE issues SET return_date=?
    WHERE id=?
    """, (date, issue[0]))

    cursor.execute("""
    UPDATE books SET status="Available"
    WHERE id=?
    """, (book_id,))

    conn.commit()

    print("Book Returned ✅")


# Issue History
def issue_history():

    cursor.execute("""
    SELECT b.name, m.name, i.issue_date, i.return_date
    FROM issues i
    JOIN books b ON i.book_id=b.id
    JOIN members m ON i.member_id=m.id
    """)

    data = cursor.fetchall()

    if not data:
        print("No Records ❌")
        return

    print("\nIssue History:")

    for row in data:

        ret = row[3] if row[3] else "Not Returned"

        print(f"Book:{row[0]} | Member:{row[1]} | Issue:{row[2]} | Return:{ret}")


# Main Menu
def main():

    create_tables()

    while True:

        print("\n====== LIBTRACK – Library Manager ======")
        print("1. Add Book")
        print("2. View Books")
        print("3. Add Member")
        print("4. View Members")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Issue History")
        print("8. Exit")

        choice = input("Choose (1-8): ")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            add_member()

        elif choice == "4":
            view_members()

        elif choice == "5":
            issue_book()

        elif choice == "6":
            return_book()

        elif choice == "7":
            issue_history()

        elif choice == "8":
            print("Thank You ❤️")
            break

        else:
            print("Wrong Choice ❌")


# Start Program
if __name__ == "__main__":
    main()