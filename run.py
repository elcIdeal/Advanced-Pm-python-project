import sqlite3
import time

conn = sqlite3.connect("lost_and_found.db")
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    location TEXT,
    date_found TEXT,
    claimed INTEGER DEFAULT 0,
    points INTEGER DEFAULT 10,
    timestamp INTEGER
)''')
conn.commit()


def add_item():
    name = input("Enter item name:")
    category = input("Enter category:")
    location = input("Where found:")
    date_found = input("Date of discovery (YYYY-MM-DD): ")
    timestamp = int(time.time())
    c.execute("INSERT INTO items (name, category, location, date_found, timestamp) VALUES (?, ?, ?, ?, ?)",
              (name, category, location, date_found, timestamp))
    conn.commit()
    print("Item added! You got 10 points!\n")


def search_items():
    search = input("Enter a title, category or location: ")
    c.execute("SELECT * FROM items WHERE (name LIKE ? OR category LIKE ? OR location LIKE ?) AND claimed = 0",
              ('%' + search + '%', '%' + search + '%', '%' + search + '%'))
    results = c.fetchall()
    if results:
        for item in results:
            print(f"[{item[0]}] {item[1]} | {item[2]} | {item[3]} | Найден: {item[4]}")
    else:
        print(" Nothing found!\n")


def view_unclaimed():
    c.execute("SELECT * FROM items WHERE claimed = 0")
    results = c.fetchall()
    if results:
        for item in results:
            print(f"[{item[0]}] {item[1]} | {item[2]} | {item[3]} | Найден: {item[4]}")
    else:
        print("There are no uncollected items!\n")


def claim_item():
    item_id = input("Enter the ID of the item you want to pick up:")
    c.execute("UPDATE items SET claimed = 1 WHERE id = ? AND claimed = 0", (item_id,))
    if c.rowcount:
        conn.commit()
        print(" Item successfully collected!\n")
    else:
        print(" The item has already been taken or the ID is incorrect!\n")


def check_auction():
    current_time = int(time.time())
    threshold = 7 * 24 * 60 * 60  # 7 дней в секундах
    c.execute("SELECT * FROM items WHERE claimed = 0 AND (timestamp + ?) < ?", (threshold, current_time))
    results = c.fetchall()
    if results:
        print("⏳These items have been listed for over 7 days and are now in auction mode:")
        for item in results:
            print(f"[{item[0]}] {item[1]} | {item[2]} | {item[3]} | Найден: {item[4]}")
    else:
        print("There are no items in the auction.\n")


def main():
    while True:
        print("\nМеню:")
        print("1. Add found item (+10 points)")
        print("2. Find item")
        print("3. Show all uncollected items")
        print("4. Pick up item")
        print("5. Check auction items")
        print("6. Log out")
        choice = input("Select action: ")

        if choice == "1":
            add_item()
        elif choice == "2":
            search_items()
        elif choice == "3":
            view_unclaimed()
        elif choice == "4":
            claim_item()
        elif choice == "5":
            check_auction()
        elif choice == "6":
            break
        else:
            print("Invalid input!\n")


if __name__ == "__main__":
    main()
    conn.close()
