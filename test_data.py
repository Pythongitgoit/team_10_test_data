# добавити в main.py
# from test_data import add_test_contacts, add_test_notes

# добавити у функцію у файл main.py
# def main():
#     address_book, notes = load_data()
#     atexit.register(save_data, address_book, notes)

# ******добавити сюди********************
# print("Adding test contacts...")
# add_test_contacts(address_book)
# print("Adding test notes...")
# add_test_notes(notes)

# ***************************
# print("Welcome to assist bot")


from datetime import datetime
import objects


def add_test_contacts(address_book):
    test_contact1 = objects.Record("John Doe", datetime(1990, 1, 1))
    test_contact1.add_phone("1234567890")
    test_contact1.add_email("john@example.com")
    test_contact1.add_address("City", "Street", "123")

    test_contact2 = objects.Record("Alice Smith", datetime(1985, 5, 15))
    test_contact2.add_phone("9876543210")
    test_contact2.add_email("alice@example.com")
    test_contact2.add_address("Town", "Avenue", "456")

    test_contact3 = objects.Record("Bob Johnson", datetime(1978, 8, 20))
    test_contact3.add_phone("5551234567")
    test_contact3.add_email("bob@example.com")
    test_contact3.add_address("Village", "Lane", "789")

    test_contact4 = objects.Record("Eva Davis", datetime(1992, 3, 10))
    test_contact4.add_phone("1112223333")
    test_contact4.add_email("eva@example.com")
    test_contact4.add_address("Suburb", "Park", "101")

    test_contact5 = objects.Record("Michael Brown", datetime(1980, 6, 25))
    test_contact5.add_phone("9998887777")
    test_contact5.add_email("michael@example.com")
    test_contact5.add_address("Rural", "Meadow", "505")

    test_contact6 = objects.Record("Sophie White", datetime(1995, 11, 5))
    test_contact6.add_phone("4445556666")
    test_contact6.add_email("sophie@example.com")
    test_contact6.add_address("Island", "Beach", "222")

    for contact in [
        test_contact1,
        test_contact2,
        test_contact3,
        test_contact4,
        test_contact5,
        test_contact6,
    ]:
        if not any(
            existing_contact.name.value.lower() == contact.name.value.lower()
            for existing_contact in address_book.data.get(contact.name.value, [])
        ):
            address_book.add_record(contact)


def add_test_notes(notes):
    test_notes = [
        objects.Note("Meeting at 2 PM", ["work", "meeting"]),
        objects.Note("Grocery shopping", ["personal", "shopping"]),
        objects.Note("Code review", ["work", "development"]),
        objects.Note("Book club meeting", ["personal", "reading"]),
        objects.Note("Project deadline", ["work", "deadline"]),
        objects.Note("Yoga class", ["personal", "fitness"]),
        objects.Note("Shopping list", ["personal", "shopping"]),
    ]

    for note in test_notes:
        if note not in notes.notes:
            notes.add_note(note)
