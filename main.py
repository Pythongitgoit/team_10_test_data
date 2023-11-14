from datetime import datetime
import pickle
import atexit
import os
import objects
import sorter_folder
from test_data import add_test_contacts, add_test_notes


def save_data(address_book, notes):
    with open("address_book.pkl", "wb") as address_book_file:
        pickle.dump(address_book, address_book_file)
    with open("notes.pkl", "wb") as notes_file:
        pickle.dump(notes, notes_file)


def load_data():
    address_book = objects.AddressBook()
    notes = objects.Notes()

    if os.path.exists("address_book.pkl"):
        with open("address_book.pkl", "rb") as address_book_file:
            address_book = pickle.load(address_book_file)

    if os.path.exists("notes.pkl"):
        with open("notes.pkl", "rb") as notes_file:
            notes = pickle.load(notes_file)

    return address_book, notes


def help_func():
    help_text = "Available commands:\n\n"

    commands = {
        "add": "Додати контакт: Ця команда дозволяє вам додати новий контакт до адресної книги. Ви вводите ім'я, номер телефону, електронну пошту (за бажанням), адресу (якщо є) та дату народження (за бажанням) для нового контакту.",
        "search": "Пошук контакту: Ця команда дозволяє вам знайти контакти за ключовим словом. Ви вводите ключове слово, і програма виводить контакти, які містять це слово в імені, телефоні, електронній пошті або адресі.",
        "delete": "Видалити контакт: Ця команда дозволяє вам видалити контакт з адресної книги. Ви вводите ім'я контакту, який потрібно видалити.",
        "add note": "Додати нотатку: Ця команда дозволяє вам додати нову нотатку до своїх нотаток. Ви вводите текст нотатки та теги (якщо є).",
        "search note": "Пошук нотатки: Ця команда дозволяє вам знайти нотатки за ключовим словом. Ви вводите ключове слово, і програма виводить нотатки, які містять це слово в тексті.",
        "sort": "Сортування нотаток за тегами: Ця команда сортує ваші нотатки за тегами. Ви вводите тег, і програма виводить всі нотатки з цим тегом, впорядковані за ним.",
        "sort folder": "Ця команда сортує файли в папці за розширеннями, видаляє пусті папки",
        "hello": "Вивести привітання: Ця команда виводить привітання від бота.",
        "close": "Завершити роботу: Ця команда завершує роботу програми та виводить прощання.",
        "clear": "Видалення данних: Ця команда видаляє всі збережені данні в нотатках та адресної книзі.",
        "change": "Редагування контакту: Ця команда дозволяє змінити будь-яке поле контакту.",
        "all": "Вивід всіх наявних контактів: ця команда виводить список всіх контактів",
        "all notes": "Вивід всіх наявних нотатків: ця команда виводить список всіх нотаток",
        "change note": "Редагування нотатків: ця команда дозволяж редагувати нотатки і теги.",
        "help": "Список всіх команд",
    }

    for command, description in commands.items():
        help_text += f"{command}: {description}\n\n"

    print(help_text)


def add_contact(address_book):
    while True:
        name = input("Enter the contact's name: ")
        while True:
            try:
                name = objects.Name(name)
                break
            except ValueError as e:
                print(f"Error: {e}")
                name = input("Enter the contact's name: ")

        phone = input("Enter the contact's phone: ")
        while True:
            try:
                if phone:
                    phone = objects.Phone(phone)
                break
            except ValueError as e:
                print(f"Error: {e}")
                phone = input("Enter the contact's phone: ")

        email = input(
            "Enter the contact's email (if available, otherwise press Enter): "
        )
        while True:
            try:
                if email:
                    email = objects.Email(email)
                break
            except ValueError as e:
                print(f"Error: {e}")
                email = input("Enter the contact's email: ")

        address = input(
            "Enter the contact's address (if available, format input - city street house, otherwise press Enter): "
        )
        while True:
            try:
                if address:
                    new_address = address.split()
                    city, street, house = new_address
                    address = objects.Address(city, street, house)
                break
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
                address = input("Enter the contact's address: ")

        birthday = input("Enter the birthday (if available, otherwise press Enter): ")
        while True:
            try:
                if birthday:
                    birthday = datetime.strptime(birthday, "%Y-%m-%d")
                break
            except (ValueError, IndexError) as e:
                print(f"Error: {e}")
                birthday = input("Enter the birthday: ")

        contact = objects.Record(name.name, birthday)
        if phone:
            contact.add_phone(phone.phone)
        if email:
            contact.add_email(email.email)
        if address:
            city, street, house = address.city, address.street, address.house
            contact.add_address(city, street, house)
        address_book.add_record(contact)
        print(f"New contact, {name.name} successfully added")
        break


def show_contacts(address_book):
    if not address_book.data:
        print("Address book is empty.")
    else:
        for name, records in address_book.data.items():
            for record in records:
                contact_info = f"Contact name: {record.name.value},"
                if record.emails and record.emails is not None:
                    contact_info += (
                        f" Email: {', '.join(email.value for email in record.emails)},"
                    )
                else:
                    contact_info += " Email: N/A,"
                if record.phones and record.phones is not None:
                    contact_info += (
                        f" Phone: {', '.join(phone.value for phone in record.phones)},"
                    )
                else:
                    contact_info += " Phone: N/A,"
                if record.addresses and record.addresses is not None:
                    contact_info += f" Address: {', '.join(str(address) for address in record.addresses)},"
                else:
                    contact_info += " Address: N/A,"
                if record.birthday and record.birthday.birthday is not None:
                    contact_info += (
                        f" Birthday: {record.birthday.birthday.strftime('%Y-%m-%d')}"
                    )
                else:
                    contact_info += " Birthday: N/A"
                print(contact_info)


def show_notes(notes):
    if not notes.notes:
        print("No notes available.")
    else:
        print("List of all notes:")
        for index, note in enumerate(notes.notes, start=1):
            print(f"{index}. Text: {note.text}")
            if note.tags:
                print(f"   Tags: {', '.join(note.tags)}")
            else:
                print("   Tags: N/A")


def change_contact(address_book, contact_name):
    found_contacts = address_book.find_contact(contact_name)

    if not found_contacts:
        print(f"Contact '{contact_name}' not found.")
        return

    if len(found_contacts) > 1:
        print("Found multiple contacts:")
        for i, contact in enumerate(found_contacts):
            print(f"{i + 1}. {contact.name.value}")
        while True:
            choice = input("Enter the number of the contact you want to change: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(found_contacts):
                    contact = found_contacts[choice]
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
    else:
        contact = found_contacts[0]

    if contact.name:
        contact_info = f"Contact found: Contact name: {contact.name.value},"
    else:
        contact_info = "Contact found: Contact name: N/A,"

    if contact.emails and contact.emails is not None:
        contact_info += f" Email: {', '.join(email.value for email in contact.emails)},"
    else:
        contact_info += " Email: N/A,"

    if contact.phones and contact.phones is not None:
        phone_values = [phone.value for phone in contact.phones]
        contact_info += f" Phone: {', '.join(phone_values)},"
    else:
        contact_info += " Phone: N/A,"

    if contact.addresses and contact.addresses is not None:
        contact_info += f" Address: {', '.join(map(str, contact.addresses))}"
    else:
        contact_info += " Address: N/A,"

    if contact.birthday and contact.birthday.birthday is not None:
        contact_info += f" Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}"
    else:
        contact_info += " Birthday: N/A"

    print(contact_info)

    while True:
        field_to_change = input(
            "Enter the field you want to change (name, phone, email, address, birthday) or 'cancel' to exit: "
        ).lower()

        if field_to_change == "cancel" or field_to_change in "cancel":
            print("Change canceled.")
            break
        if field_to_change == "name" or field_to_change in "name":
            new_name = input("Enter the new name: ")
            contact.name.value = new_name
            print(f"Contact name changed to {new_name}")
            break
        elif field_to_change == "phone" or field_to_change in "phone":
            if contact.phones:
                old_phone = input("Enter the old phone number: ")
            else:
                old_phone = None

            new_phone = input("Enter the new phone number: ")

            if new_phone:
                try:
                    new_phone_object = objects.Phone(new_phone)

                    if old_phone:
                        contact.remove_phone(old_phone)
                        contact.add_phone(new_phone)
                        print(f"Phone number changed from {old_phone} to {new_phone}")
                    else:
                        contact.add_phone(new_phone)
                        print(f"Phone number {new_phone} added")
                    break
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("New phone number cannot be empty.")
        elif field_to_change == "email" or field_to_change in "email":
            if contact.emails:
                old_email = input("Enter the old email address: ")
            else:
                old_email = None

            new_email = input("Enter the new email address: ")

            if new_email:
                try:
                    new_email_object = objects.Email(new_email)

                    if old_email:
                        contact.emails = [
                            email
                            for email in contact.emails
                            if email.value != old_email
                        ]
                        contact.add_email(new_email)
                        print(f"Email address changed from {old_email} to {new_email}")
                    else:
                        contact.add_email(new_email)
                        print(f"Email address {new_email} added")
                    break
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("New email address cannot be empty.")
        elif field_to_change == "address" or field_to_change in "address":
            if contact.addresses:
                old_address = input(
                    "Enter the old address (format: city street house): "
                )
            else:
                old_address = None

            new_address = input("Enter the new address (format: city street house): ")

            if new_address:
                try:
                    new_address_parts = new_address.split()
                    if len(new_address_parts) == 3:
                        new_city, new_street, new_house = new_address_parts
                        if old_address:
                            old_address_parts = old_address.split()
                            if len(old_address_parts) == 3:
                                old_city, old_street, old_house = old_address_parts
                                contact.addresses = [
                                    address
                                    for address in contact.addresses
                                    if address.city != old_city
                                    or address.street != old_street
                                    or address.house != old_house
                                ]
                                contact.add_address(new_city, new_street, new_house)
                                print(
                                    f"Address changed from {old_address} to {new_address}"
                                )
                            else:
                                print("Invalid old address format.")
                        else:
                            contact.add_address(new_city, new_street, new_house)
                            print(f"Address {new_address} added")
                        break
                    else:
                        print("Invalid new address format.")
                except (ValueError, IndexError) as e:
                    print(f"Error: {e}")
            else:
                print("New address cannot be empty.")
        elif field_to_change == "birthday" or field_to_change in "birthday":
            new_birthday = input("Enter the new birthday (format: YYYY-MM-DD): ")
            if new_birthday:
                try:
                    new_birthday = datetime.strptime(new_birthday, "%Y-%m-%d")
                    contact.birthday.birthday = new_birthday
                    print(f"Birthday changed to {new_birthday.strftime('%Y-%m-%d')}")
                except ValueError:
                    print("Invalid date format.")
            else:
                contact.birthday = None
                print("Birthday cleared.")
            break
        else:
            print("Invalid field to change.")


def change_note(notes, note_text):
    found_notes = []
    for note in notes.notes:
        if note_text.lower() in note.text.lower():
            found_notes.append(note)

    if not found_notes:
        print(f"Note with text '{note_text}' not found.")
        return

    if len(found_notes) > 1:
        print("Found multiple notes:")
        for i, note in enumerate(found_notes):
            print(f"{i + 1}. {note.text}")
        while True:
            choice = input("Enter the number of the note you want to change: ")
            try:
                choice = int(choice) - 1
                if 0 <= choice < len(found_notes):
                    note = found_notes[choice]
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
    else:
        note = found_notes[0]

    print(f"Note found: Text: {note.text}, Tags: {', '.join(note.tags)}")

    while True:
        field_to_change = input(
            "Enter the field you want to change (text, tags): "
        ).lower()

        if field_to_change == "text":
            new_text = input("Enter the new text for the note: ")
            note.text = new_text
            print(f"Note text changed to '{new_text}'")
            break
        elif field_to_change == "tags":
            new_tags = input("Enter the new tags (comma-separated): ").split(",")
            note.tags = new_tags
            print(f"Tags updated to: {', '.join(new_tags)}")
            break
        else:
            print("Invalid field to change.")


def search_contact(address_book):
    query = input("Enter the search keyword: ")
    found_contacts = address_book.find_contact(query)
    if found_contacts:
        print("Found contacts:")
        for contact in found_contacts:
            contact_info = f"Name: {contact.name.value}"
            if contact.emails and contact.emails is not None:
                contact_info += (
                    f", Email: {', '.join(email.value for email in contact.emails)}"
                )
            else:
                contact_info += f", Email: N/A"
            if contact.phones and contact.phones is not None:
                contact_info += (
                    f", Phone: {', '.join(phone.value for phone in contact.phones)}"
                )
            else:
                contact_info += f", Phone: N/A"
            if contact.addresses and contact.addresses is not None:
                contact_info += f", Address: {', '.join(str(address) for address in contact.addresses)}"
            else:
                contact_info += f", Address: N/A"
            if contact.birthday and contact.birthday.birthday is not None:
                contact_info += (
                    f", Birthday: {contact.birthday.birthday.strftime('%Y-%m-%d')}"
                )
            else:
                contact_info += f", Birthday: N/A"
            print(contact_info)
    else:
        print("Contacts not found.")


def delete_contact(address_book, name):
    if name in address_book.data:
        address_book.delete(name)
        print(f"Contact '{name}' deleted.")
    else:
        print("Contact not found.")


def add_note(notes):
    text = input("Enter note text: ")
    tags = input("Enter tags (comma-separated): ").split(",")
    note = objects.Note(text, tags)
    notes.add_note(note)


def search_note(notes):
    keyword = input("Enter a keyword to search for: ")
    tag_search = input("Do you want to search by tag (yes or no)? ").lower()

    found_notes = []
    for note in notes.notes:
        if keyword.lower() in note.text.lower() and (
            not tag_search or tag_search == "no" or tag_search == "n"
        ):
            found_notes.append(note)
        elif tag_search and tag_search in ["yes", "y"] and keyword.lower() in note.tags:
            found_notes.append(note)

    if found_notes:
        print("Found notes:")
        for note in found_notes:
            print(f"Note text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
    else:
        print("Notes not found.")


def sort_notes_by_tags(notes):
    tag = input("Enter a tag for sorting: ")
    sorted_notes = notes.sort_notes_by_tags(tag)
    if sorted_notes:
        print(f"Sorted notes by tag '{tag}':")
        for note in sorted_notes:
            print(f"Note text: {note.text}")
            print(f"Tags: {', '.join(note.tags)}")
    else:
        print(f"No notes with the tag '{tag}' found.")


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format."

    return inner


def hello():
    return f"Welcome to assist bot"


def clear_data(address_book, notes):
    confirmation = input(
        "Are you sure you want to clear all data? (yes or no): "
    ).lower()
    if confirmation == "yes" or confirmation == "y":
        address_book.clear()
        notes.clear()
        print("All data has been cleared.")
    else:
        print("Clearing data canceled.")


COMMANDS = {"add": add_contact, "search": search_contact, "delete": delete_contact}


def process_command(command, address_book):
    if command in COMMANDS:
        COMMANDS[command](address_book)
    else:
        print("Invalid command")


@user_error
def main():
    address_book, notes = load_data()
    atexit.register(save_data, address_book, notes)

    # ******добавити сюди********************
    print("Adding test contacts...")
    add_test_contacts(address_book)
    print("Adding test notes...")
    add_test_notes(notes)

    # ***************************

    print("Welcome to assist bot")
    print('If you need list of commands, write "help" and press ENTER.')
    while True:
        user_input = input("Enter a command: ")
        if user_input == "hello":
            print("Hello how can i help you")

        elif user_input == "close":
            print("Good bye")
            break
        elif user_input == "delete":
            name = input("Enter the contact's name to delete: ")
            delete_contact(address_book, name)
        elif user_input == "add note":
            add_note(notes)
        elif user_input == "search note":
            search_note(notes)
        elif user_input == "sort":
            sort_notes_by_tags(notes)
        elif user_input == "help":
            help_func()
        elif user_input == "clear":
            clear_data(address_book, notes)
        elif user_input == "change":
            contact_name = input("Enter a keyword to find a contact: ")
            change_contact(address_book, contact_name)
        elif user_input == "all":
            show_contacts(address_book)
        elif user_input == "change note":
            note_text = input("Enter the text of the note you want to change: ")
            change_note(notes, note_text)
        elif user_input == "all notes":
            show_notes(notes)
        elif user_input == "sort folder":
            folder_path = input("Enter the path to the folder you want to sort: ")
            sorter_folder.sort_files(folder_path)
        else:
            process_command(user_input, address_book)


if __name__ == "__main__":
    main()
