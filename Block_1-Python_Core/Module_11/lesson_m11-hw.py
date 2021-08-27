from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):
    contact_counter = 0

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
            self.contact_counter += 1
        else:
            self.data[record.name.value].add_additionally(record.contacts)

    def change_record(self, ex_record, new_record):
        self.data[ex_record.name.value].change(ex_record, new_record)

    def show_phone(self, name):
        return self.data[name]

    def delete_record(self, record):
        self.data.pop(record.name.value)
        self.contact_counter -= 1

    def iterator(self, item):
        counter = 0
        result = []
        for val in self.data.values():
            result.append(str(val).replace("[", "")
                          .replace("]", ""))
            counter += 1
            if counter == item:
                break
        return result

    def __str__(self):
        result = f"All {self.contact_counter} contacts in Address book:\n"
        for val in self.data.values():
            result += str(val).replace("[", "") \
                          .replace("]", "") + "\n"
        return result


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __repr__(self):
        return f"{self.value.title()}"


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @staticmethod
    def contact_value(value: str):
        try:
            name, contact = value.split(" ")
            if not value.startswith(" ") and contact[1:].isdigit() and len(contact[1:]) == 12 or len(contact) == 10:
                record = Record(Name(name), contacts=[contact])
                address_book.add_record(record)
                print(f"{name.title()}`s contact information {contact} added to Address book.")
            elif not value.startswith(" ") and not contact.isdigit() and contact.count("@", 0, -1) == 1:
                record = Record(Name(name), contacts=[contact])
                address_book.add_record(record)
                print(f"{name.title()}`s contact information {contact} added to Address book.")
            else:
                print("Wrong input name or contact information! Check, please.")
                print(f"<< {contact} >>")
        except ValueError or TypeError or AttributeError:
            print("Wrong input name or contact information! Check, please.")

    def __repr__(self):
        return self.value


class Record:
    def __init__(self, name, contacts=None, birthday=None):
        self.name = name
        self.birthday = birthday
        if contacts is None:
            self.contacts = []
        else:
            self.contacts = contacts

    def add(self, contacts):
        self.contacts.append(contacts)

    def add_additionally(self, contacts):
        self.contacts.extend(contacts)

    def change(self, ex_contact, new_contact):
        index = 0
        for name, contact in enumerate(self.contacts):
            if str(contact) == str(ex_contact):
                index = name
                break
        self.contacts[index] = new_contact

    @staticmethod
    def days_to_birthday(birthday):
        try:
            current_date = datetime.now()
            month, day, year = re.findall('\d+', birthday)
            if current_date.month > int(month):
                days = datetime(year=current_date.year, month=current_date.month, day=current_date.day) - \
                       datetime(year=current_date.year + 1, month=int(month), day=int(day))
                age = int(current_date.year) - int(year)
                print(f"In {str(days.days).removeprefix('-')} days there will be a birthday and turn {age + 1} age.")
            else:
                days = datetime(year=current_date.year, month=current_date.month, day=current_date.day) - \
                       datetime(year=current_date.year, month=int(month), day=int(day))
                age = int(current_date.year) - int(year)
                print(f"In {str(days.days).removeprefix('-')} days there will be a birthday and turn {age} age.")
        except ValueError or TypeError:
            print("Wrong input birthday date! Check, please.")

    def __repr__(self):
        return f"{self.name}: {str(self.contacts).replace('[', '').replace(']', '')}"


class BirthDay(Field):
    def __init__(self, value):
        self.value = value

    @staticmethod
    def birthday_value(value: str):
        try:
            name = value.split(" ")[0]
            birthday_date = re.findall('\d+', value)
            if len(birthday_date) == 3:
                if 0 < int(birthday_date[0]) <= 31:
                    if 0 < int(birthday_date[1]) <= 12:
                        if len(birthday_date[2]) == 4:
                            record = Record(Name(name), [BirthDay(str(value.split(" ")[1:])
                                                                  .replace(' ', '-')
                                                                  .replace(',', ''))])
                            address_book.add_record(record)
                            print(f"{name.title()}`s birthday added to Address book.")
        except ValueError or TypeError:
            print("Wrong input birthday date! Check, please.")

    def __repr__(self):
        return self.value


address_book = AddressBook()


def main():
    print("Command Line Interface")
    while True:
        user_ans = input("Address book bot\n>>").lower()
        user_ans_a = user_ans.split(" ")
        for i in user_ans_a:
            if i == "hello":
                print("Hello!\nHow can I help you?")
            if i == "add" and user_ans != "add birthday":
                add_command()
            if i == "change":
                change_command()
            if i == "phone":
                phone_command()
            if i == "delete":
                delete_command()
            if i == "help" or i == "reference":
                help_command()
        if user_ans == "add birthday":
            add_birthday_command()
        if user_ans == "show part":
            show_part_command()
        if user_ans == "show all":
            print(address_book)
        if len(user_ans) == 0:
            print("Empty input!\nDo you want to read reference for Address book bot?\n"
                  "Enter <<help>> or <<reference>>")
        if user_ans == "good bye" or user_ans == "close" or user_ans == "exit":
            print("Good bye!\nHope see you soon!")
            break


def add_command():
    user_input = input("Give me name and contact information to add, please\n"
                       "(between name and contact information must be space)\n>>").lower()
    Phone.contact_value(value=user_input)


def add_birthday_command():
    user_input = input("Give me name and birthday to add, please\n"
                       "(between name month (digit) day (digit) year (4 digit) must be space)\n>>").lower()
    BirthDay.birthday_value(value=user_input)
    Record.days_to_birthday(birthday=user_input)


def change_command():
    user_input = input("Give me name, old and new contact information to change, please\n"
                       "(between name, old and new contact information must de space)\n>>").lower()
    try:
        name, ex_contact, new_contact = user_input.split(" ")
        ex_record = Record(Name(name), [Phone(ex_contact)])
        new_record = Record(Name(name), [Phone(new_contact)])
        address_book.change_record(ex_record, new_record)
        print(f"{name.title()}`s contact information changed on {new_contact}.")
    except ValueError or TypeError:
        print("Wrong input name or contact information! Check, please.")


def phone_command():
    user_info = input("Enter only name, please\n>>").lower()
    print(f"{address_book.show_phone(user_info)}")


def show_part_command():
    print(f"Address book include {address_book.contact_counter} contacts.")
    if address_book.contact_counter != 0:
        user_input = input("Give me a certain quantity of contacts (digit) to show, please\n>>")
        for part in address_book.iterator(int(user_input)):
            print(part)


def delete_command():
    user_input = input("Are you sure?\nIf <<YES>>\nGive me name to delete all contact information, please\n"
                       "If <<NO>>\nEnter <<No>>\n>>").lower()
    for i in user_input.split():
        if i == "no":
            continue
        else:
            name = user_input
            record = Record(Name(name))
            address_book.delete_record(record)
        print(f"{user_input.title()} was successfully deleted form Address Book.")


def help_command():
    """
    =====================================================
                 CLI - Command Line Interface
                       Address book bot
    =====================================================

    Address book bot has a commands:
    1. "add" - for add name and contact information to
    Address book, write "add" and enter command, then
    bot ask you contact details enter it;

    2. "add birthday" - for add birthday of contact in
    Address book, write "add birthday" and enter command,
    then bot ask you details enter it;

    3. "phone" - for get contact information, write
    "phone" and enter command, then bot ask you details
    enter it;

    4. "change" - for change contact information, write
    "change" and enter command, then bot ask you details
    enter it;

    5. "show part" - for show a certain part of contacts
    in Address book, write "show part" and enter command,
    then bot ask you details enter it;

    6. "show all" - for show all contacts in Address
    book, write "show all" and enter command;

    7. "delete" - for delete name and contact information
    in Address book, write "delete" and enter command,
    then bot ask you details enter it;

    8. "help", "reference" - for ask reference how to
    use bot write "help" or "reference" and enter the
    command;

    9. "hello" - for check Address book bot condition
    write "hello" and enter command;

    10. "close", "exit", "good bye" - for finish work with
    Address book bot, write one of "close", "exit" or
    "good bye" and enter command, then you will exit from
    Command Line Interface.

    Pleasant use!

    """
    print(help_command.__doc__)


if __name__ == "__main__":
    main()

######################################################################################
# from collections import UserDict
# from datetime import datetime
# import re
#
#
# class AddressBook(UserDict):
#     contact_counter = 0
#
#     def add_record(self, record):
#         if record.name.value not in self.data:
#             self.data[record.name.value] = record
#             self.contact_counter += 1
#         else:
#             self.data[record.name.value].add_additionally(record.contacts)
#
#     def change_record(self, ex_record, new_record):
#         self.data[ex_record.name.value].change(ex_record, new_record)
#
#     def show_phone(self, name):
#         return self.data[name]
#
#     def delete_record(self, record):
#         self.data.pop(record.name.value)
#         self.contact_counter -= 1
#
#     def iterator(self, item):
#         counter = 0
#         result = []
#         for val in self.data.values():
#             result.append(str(val).replace("[", "")
#                                   .replace("]", ""))
#             counter += 1
#             if counter == item:
#                 break
#         return result
#
#     def __str__(self):
#         result = f"All {self.contact_counter} contacts in Address book:\n"
#         for val in self.data.values():
#             result += str(val).replace("[", "")\
#                               .replace("]", "") + "\n"
#         return result
#
#
# class Field:
#     def __init__(self, value):
#         self.__value = value
#
#     @property
#     def value(self):
#         return self.__value
#
#     @value.setter
#     def value(self, value):
#         self.__value = value
#
#     def __str__(self):
#         return f"{self.value.title()}"
#
#
# class Name(Field):
#     pass
#
#
# class Phone(Field):
#     def __init__(self, value):
#         super().__init__(value)
#         self.contacts = ""
#
#     @Field.value.setter
#     def value(self, value: str):
#         name, contact = value.split(" ")
#         try:
#             if not value.startswith(" ") and contact[1:].isdigit() and len(contact[1:]) <= 12 or len(contact) == 10:
#                 self.contacts += contact
#             elif not value.startswith(" ") and not contact.isdigit() and contact.count("@", 0, -1) == 1:
#                 self.contacts += contact
#         except AttributeError or ValueError or TypeError:
#             print("Wrong input name or contact information! Check, please.")
#
#     def __repr__(self):
#         return self.value
#
#
# class Record:
#     def __init__(self, name, contacts=None, birthday=None):
#         self.name = name
#         self.birthday = birthday
#         if contacts is None:
#             self.contacts = []
#         else:
#             self.contacts = contacts
#
#     def add(self, contacts):
#         self.contacts.appends(contacts)
#
#     def add_additionally(self, contacts):
#         self.contacts.extend(contacts)
#
#     def change(self, ex_contact, new_contact):
#         index = 0
#         for name, contact in enumerate(self.contacts):
#             if str(contact) == str(ex_contact):
#                 index = name
#                 break
#         self.contacts[index] = new_contact
#
#     def days_to_birthday(self):
#         try:
#             current_date = datetime.now()
#             month, day, year = re.findall('\d+', self.birthday)
#             if current_date.month > int(month):
#                 days = datetime(year=current_date.year, month=current_date.month, day=current_date.day) - \
#                        datetime(year=current_date.year + 1, month=int(month), day=int(day))
#                 age = int(current_date.year) - int(year)
#                 return f"In {str(days.days).removeprefix('-')} days there will be a birthday and turn {age + 1} age."
#             else:
#                 days = datetime(year=current_date.year, month=current_date.month, day=current_date.day) - \
#                        datetime(year=current_date.year, month=int(month), day=int(day))
#                 age = int(current_date.year) - int(year)
#                 return f"In {str(days.days).removeprefix('-')} days there will be a birthday and turn {age} age."
#         except ValueError or TypeError:
#             print("Wrong input birthday date! Check, please.")
#
#     def __repr__(self):
#         return f"{self.name}: {str(self.contacts).replace('[', '').replace(']', '')}"
#
#
# class BirthDay(Field):
#     def __init__(self, value):
#         super().__init__(value)
#
#     @Field.value.setter
#     def value(self, value: str):
#         try:
#             birthday_date = re.findall('\d+', value)
#             if len(birthday_date) == 3:
#                 if 0 < int(birthday_date[0]) <= 31:
#                     if 0 < int(birthday_date[1]) <= 12:
#                         if len(birthday_date[2]) == 4:
#                             self.__value = value
#         except ValueError or TypeError:
#             print("Wrong input birthday date! Check, please.")
#
#     def __repr__(self):
#         return self.value
#
#
# address_book = AddressBook()
#
#
# def main():
#     print("Command Line Interface")
#     while True:
#         user_ans = input("Address book bot\n>>").lower()
#         user_ans_a = user_ans.split(" ")
#         for i in user_ans_a:
#             if i == "hello":
#                 print("Hello!\nHow can I help you?")
#             if i == "add" and user_ans != "add birthday":
#                 add_command()
#             if i == "change":
#                 change_command()
#             if i == "phone":
#                 phone_command()
#             if i == "delete":
#                 delete_command()
#             if i == "help" or i == "reference":
#                 help_command()
#         if user_ans == "add birthday":
#             add_birthday_command()
#         if user_ans == "show part":
#             show_part_command()
#         if user_ans == "show all":
#             print(address_book)
#         if len(user_ans) == 0:
#             print("Empty input!\nDo you want to read reference for Address book bot?\n"
#                   "Enter <<help>> or <<reference>>")
#         if user_ans == "good bye" or user_ans == "close" or user_ans == "exit":
#             print("Good bye!\nHope see you soon!")
#             break
#
#
# def add_command():
#     user_input = input("Give me name and contact information to add, please\n"
#                        "(between name and contact information must be space)\n>>").lower()
#     name, contact = user_input.split(" ")
#     record = Record(Name(name), [Phone(contact)])
#     address_book.add_record(record)
#     print(f"{name.title()}`s contact information {contact} added to Address book.")
#
#
# def add_birthday_command():
#     user_input = input("Give me name and birthday to add, please\n"
#                        "(between name month (digit) day (digit) year (4 digit) must be space)\n>>").lower()
#     name = user_input.split(" ")[0]
#     record = Record(Name(name), birthday=user_input)
# #    birthday = Record(Name(name), Field(value=user_input))
#     birthday = Record(Name(name), [BirthDay(str(user_input.split(" ")[1:]).replace(' ', '-').replace(',', ''))])
#     address_book.add_record(birthday)
#     print(f"{name.title()}`s birthday added to Address book.")
#     print(Record.days_to_birthday(record))
#
#
# def change_command():
#     user_input = input("Give me name, old and new contact information to change, please\n"
#                        "(between name, old and new contact information must de space)\n>>").lower()
#     name, ex_contact, new_contact = user_input.split(" ")
#     ex_record = Record(Name(name), [Phone(ex_contact)])
#     new_record = Record(Name(name), [Phone(new_contact)])
#     address_book.change_record(ex_record, new_record)
#     print(f"{name.title()}`s contact information changed on {new_contact}.")
#
#
# def phone_command():
#     user_info = input("Enter only name, please\n>>").lower()
#     print(f"{address_book.show_phone(user_info)}")
#
#
# def show_part_command():
#     print(f"Address book include {address_book.contact_counter} contacts.")
#     if address_book.contact_counter != 0:
#         user_input = input("Give me a certain quantity of contacts (digit) to show, please\n>>")
#         for part in address_book.iterator(int(user_input)):
#             print(part)
#
#
# def delete_command():
#     user_input = input("Are you sure?\nIf <<YES>>\nGive me name to delete all contact information, please\n"
#                        "If <<NO>>\nEnter <<No>>\n>>").lower()
#     for i in user_input.split():
#         if i == "no":
#             continue
#         else:
#             name = user_input
#             record = Record(Name(name))
#             address_book.delete_record(record)
#         print(f"{user_input.title()} was successfully deleted form Address Book.")
#
#
# def help_command():
#     """
#     =====================================================
#                  CLI - Command Line Interface
#                        Address book bot
#     =====================================================
#
#     Address book bot has a commands:
#     1. "add" - for add name and contact information to
#     Address book, write "add" and enter command, then
#     bot ask you contact details enter it;
#
#     2. "add birthday" - for add birthday of contact in
#     Address book, write "add birthday" and enter command,
#     then bot ask you details enter it;
#
#     3. "phone" - for get contact information, write
#     "phone" and enter command, then bot ask you details
#     enter it;
#
#     4. "change" - for change contact information, write
#     "change" and enter command, then bot ask you details
#     enter it;
#
#     5. "show part" - for show a certain part of contacts
#     in Address book, write "show part" and enter command,
#     then bot ask you details enter it;
#
#     6. "show all" - for show all contacts in Address
#     book, write "show all" and enter command;
#
#     7. "delete" - for delete name and contact information
#     in Address book, write "delete" and enter command,
#     then bot ask you details enter it;
#
#     8. "help", "reference" - for ask reference how to
#     use bot write "help" or "reference" and enter the
#     command;
#
#     9. "hello" - for check Address book bot condition
#     write "hello" and enter command;
#
#     10. "close", "exit", "good bye" - for finish work with
#     Address book bot, write one of "close", "exit" or
#     "good bye" and enter command, then you will exit from
#     Command Line Interface.
#
#     Pleasant use!
#
#     """
#     print(help_command.__doc__)
#
#
# if __name__ == "__main__":
#     main()