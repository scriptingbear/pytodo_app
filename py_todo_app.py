#PyToDo App
'''
You are asked to design an App to keep track of students’ TODOs and Classes.
To do this, you will need to analyze the classes needed for the app and the
attributes and methods of each class. Please indicate the possible attributes
and, if possible, the possible values) and add a brief description of the
functionality of the methods (base your answer on the details provided by the client).

This is the description provided by the client:
The user will be able to create a TODO and assign a description, due date,
and priority. Optionally, the user can assign a classroom and a class to the
TODO if it is related to academic activities.

TODOs can be classified as: Personal, Academic, Work, or Leisure.

The three possible priorities are: Urgent, Intermediate, and Optional.

TODOs should be removed when the user indicates that it was completed.

Additionally, the app should include a tracker of the classes that the student is taking at a college or high school.

Each class has a class code, a professor, a start time, end time, and classroom assigned.

'''
#Use enums for more readable code and to reduce typos
from enum import Enum
import os
import sys
from dateutil.parser import parse
from datetime import datetime

class Priority(Enum):
	URGENT = 3
	INTERMEDIATE = 2
	OPTIONAL = 1

class Classification(Enum):
        PERSONAL = 1
        ACADEMIC = 2
        WORK = 3
        LEISURE = 4

class MenuOption(Enum):
        ADD = 0
        EDIT = 1
        DELETE = 2
        VIEW_INCOMPLETE = 3
        VIEW_COMPLETED = 4
        VIEW_ALL = 5
        VIEW_CLASSES = 6
        DELETE_ALL = 7
        SAVE = 8
        RESTORE = 9
        QUIT = 10
        

class ViewOption(Enum):
        INCOMPLETE = 1
        COMPLETED = 2
        ALL = 3

class ToDo:

        def __init__(self, description=None, due_date=None, priority=None, classification=None, classroom=None, subject=None):
                #Create dictionary from formal parameters and their values
                #Eliminates having to write lots of individual assignments
                args = locals()
                for arg, value in args.items():
                        setattr(self, "_" + arg, value)

        @property
        def description(self):
                return self._description

        @description.setter
        def description(self, value):
                if value:
                        self._description = value

        @property
        def due_date(self):
                return self._due_date

        @due_date.setter
        def due_date(self, value):
                try:
                        value = parse(value)
                        self._due_date = value
                except ValueError:
                        print(f"Could not parse \"{value}\" as a date.")    

        @property
        def priority(self):
                return self._priority

        @priority.setter
        def priority(self, value):
                try:
                        if isinstance(value, str):
                                if value.isnumeric():
                                        value = int(value)

                        priority = Priority(value)
                        self._priority = value
                except:
                        print(f"\"{value}\" is not a valid value for the priority property.")

        @property
        def classification(self):
                return self._classification

        @classification.setter
        def classification(self, value):
                try:
                        if isinstance(value, str):
                                if value.isnumeric():
                                        value = int(value)

                        classification = Classification(value)
                        self._classification = value
                except:
                        print(f"\"{value}\" is not a valid value for the classification property.")

        @property
        def classroom(self):
                return self._classroom

        @classroom.setter
        def classroom(self, value):
                if value:
                        self._classroom = value

        @property
        def subject(self):
                return self._subject

        @subject.setter
        def subject(self, value):
                if value:
                        self._subject = value
                          
class Manager:
        todo_list = []
        database_file = "C:\\Users\\win2m\\Documents\\Programming Documentation\\" \
                        "Python Documentation\\Udemy\Python OOP - Python Object Oriented Programming For Beginners\\" \
                        "Object OrientedAnalysis And Design\\" \
                        "todo_database.txt"


        menu = {}
        todo_properties = ["description", "due_date", "priority", "classification", "classroom", "subject"]

        def __init__(self):
                print("Welcome to PyToDo!")
                self.read_data()
                self.display_menu()


        def display_menu(self):
                while True:
                        print(self.build_menu())
                        choice = input("Select an option: ")
                        if (not choice) or (not choice.isnumeric()):
                                print("invalid selection. Try again")
                                continue
                        else:
                                try:
                                        choice = int(choice)
                                        #Cast as MenuOption to access the dictionary
                                        choice = MenuOption(choice)
                                except:
                                        print("Invalid selection. Try again.")
                                        continue

                        #Invoke the method associated with the selected option
                        #Optionally provide arguments, if present
                        args = None
                        menu_data = Manager.menu[choice]
                        proc = menu_data[1]
                        if len(menu_data) == 3:
                                args = menu_data[2]
                        if args:
                                getattr(Manager, proc)(self, args)
                        else:
                                getattr(Manager, proc)(self)



        def build_menu(self):
                #App menu constructed from dictionary with the following structure:
                #key: MenuOption<enum>
                #value: [<text to display>, <name of proc to invoke>, <optional argument(s)>]
                Manager.menu.clear()
                menu_option_data = [["Add TODO", "add_todo"],
                                    ["Edit TODO", "edit_todo"],
                                    ["Delete TODO", "delete_todo"],
                                    ["View Incomplete TODOs", "view_todos", ViewOption.INCOMPLETE],
                                    ["View Completed TODOs", "view_todos", ViewOption.COMPLETED],
                                    ["View All TODOs", "view_todos", ViewOption.ALL],
                                    ["View Classes", "view_classes"],
                                    ["Delete All TODOs", "delete_all_todos"],
                                    ["Save Data", "write_data"],
                                    ["Restore Data", "read_data"],
                                    ["Quit", "quit_app"]]
                Manager.menu = {option: menu_option_data[option.value] for option in MenuOption}
                menu_text = "-----MAIN MENU-----\n"
                for item, data in Manager.menu.items():
                        menu_text += f"{item.value}. - {menu_option_data[item.value][0]}\n"

                return menu_text

                
        def get_enum_choices(self, enum_name):
                if not enum_name:
                        return None

                enum_name = enum_name.capitalize()
                if not enum_name in ["Priority", "Classification"]:
                        return None
                
                enum_choices = []
                if enum_name == "Priority":
                        my_enum = Priority
                elif enum_name == "Classification":
                        my_enum = Classification
                
                for item in my_enum:
                        enum_choices.append(f"{item.value}-{item.name}")

                enum_choices = "{" + ",".join(enum_choices) + "}"
                return enum_choices



        def input_todo_properties(self):
                todo_data = {}
                enum_values = {"Priority": [1, 2, 3], "Classification": [1, 2, 3, 4]}
                for prop in Manager.todo_properties:
                        prompt = f"{prop.capitalize()}"
                        enum_choices = self.get_enum_choices(prop)
                        if enum_choices:
                                prompt += "\n" + enum_choices
                                valid_choices = enum_values[prop.capitalize()]
                                value = input(prompt + ": ")
                                if value.isnumeric() and int(value) in valid_choices:
                                        todo_data[prop] = value
                                else:
                                        print(f"\"{value}\" is not a valid option.")
                                        
                        else:
                                value = input(prompt + ": ")
                                if value:
                                        todo_data[prop] = value

                return todo_data

        def display_todo_properties(self, todo):
                todo_info = ""
                for prop in Manager.todo_properties:
                        todo_info += f"{prop.capitalize()}: {getattr(todo, prop)}\n"
                        
                print(todo_info)

        def select_todo(self):
                self.view_todos(ViewOption.ALL)
                choice = input("Select ToDo from the list: ")
                
                if not choice:
                        return None
                try:
                        choice = int(choice)
                except:
                        print(f"\"{choice}\" is not a number.")
                        return None

                if not (0 <= choice < len(Manager.todo_list)):
                        print(f"\"{choice}\" is not a valid selection.")
                        return None
                else:
                        return choice
                

        def add_todo(self):
                #Prompt user for ToDo item properties
                todo_data = self.input_todo_properties()

                if not todo_data:
                        print("Invalid or insufficient data provided. Cannot create a ToDo item.")
                        return

                #Create empty ToDo item and then set its attributes
                todo = ToDo()
                for prop, value in todo_data.items():
                        setattr(todo, prop, value)
                
                Manager.todo_list.append(todo)
                print(f"ToDo item \"{todo.description}\" as been added.")
                
        def edit_todo(self):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return
                
                choice = self.select_todo()
                if choice == None:
                        return

                #Display selected ToDo item properties and prompt user for inputs
                todo = Manager.todo_list[choice]
                self.display_todo_properties(todo)
                mark_complete = input("Mark this ToDo item complete? (Y/N)")
                if mark_complete.upper() == "Y":
                        setattr(todo, "Completed", True)
                        Manager.todo_list[choice] = todo
                        print(f"ToDo item \"{todo.description}\" has been marked completed.")
                        return

                #Prompt user for ToDo item properties
                try:
                        todo_data = self.input_todo_properties()
                        for prop, value in todo_data.items():
                                setattr(todo, prop, value)
                        
                        Manager.todo_list[choice] = todo
                        print(f"ToDo item \"{todo.description}\" has been updated.")
                except:
                        print("Could not edit Todo item.")
                

        def delete_todo(self):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return
                
                choice = self.select_todo()
                if choice == None:
                        return

                #Display selected ToDo item properties and prompt to confirm deletion
                todo = Manager.todo_list[choice]
                self.display_todo_properties(todo)
                ok_to_delete = input("Delete this ToDo item now? (Y/N)")
                if (not ok_to_delete) or (ok_to_delete.upper() == "N"):
                        print("Operation canceled. ToDos was not deleted.")
                        return
                        
                del Manager.todo_list[choice]
                print(f"ToDo item \"{todo.description}\" has been marked completed.")
                

        def view_todos(self, view_option):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return
                
                menu_text = "ToDo List\n"
                for index, todo in enumerate(Manager.todo_list):
                        if (view_option == ViewOption.ALL) or \
                           (view_option == ViewOption.COMPLETED and hasattr(todo, "Completed")) \
                           or(view_option == ViewOption.INCOMPLETE and not hasattr(todo, "Completed")):
                                menu_text += f"{index}. - {todo.description}\n"
                
                print(menu_text)
                

        def view_classes(self):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return

                subjects = []
                menu_text = "Classes\n"
                #Sort subjects (classes) alphabetically
                for index, todo in enumerate(Manager.todo_list):
                       if hasattr(todo, "subject"):
                               subjects.append(todo.subject)

                if not subjects:
                        print("No ToDos have associated classes.")
                        return
                
                subjects.sort()
                menu_text += "\n".join(subjects)      
                print(menu_text)
                

        def delete_all_todos(self):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return
                
                ok_to_delete = input("Are you sure you want to delete ALL ToDos now? (Y/N)")
                if (not ok_to_delete) or (ok_to_delete.upper() == "N"):
                        print("Operation canceled. No ToDos were deleted.")
                        return
                
                Manager.todo_list.clear()
                print("All ToDos have been deleted.")
                

        def quit_app(self):
                print("PyToDo says \"Ciao!\"")
                sys.exit()


        def write_data(self):
                if not Manager.todo_list:
                        print("No ToDo items have been created.")
                        return
                
                #If todo_database.txt file doesn't exists, create it.
                #Store records delimited by pipe ("|") character
                with open(Manager.database_file, 'w') as f:
                        for todo in Manager.todo_list:
                                todo_data = []
                                for prop in Manager.todo_properties:
                                        value = getattr(todo, prop)
                                        if isinstance(value, datetime):
                                                #Convert date to string representation
                                                value = value.strftime("%m/%d/%Y")
                                        elif isinstance(value, (Priority, Classification)):
                                                #value is an enum member, so coerce to an int
                                                value = int(value)
                                                
                                        todo_data.append(f"{prop}:{value}")
                                        
                                line = '|'.join(todo_data)
                                f.write(line + "\n")         

                print("PyToDo database file has been updated")
                

        def read_data(self):
                #Update class attribute todo_list with contents of
                #todo_database.txt file, whose records are in this format:
                #<prop>:<value>|,...
                if not os.path.isfile(Manager.database_file):
                        raise FileNotFoundError(f"PyToDo database file {Manager.database_file} not found.")

                #If file is empty, don't update todo_list[]
                file_stats = os.stat(Manager.database_file)
                if file_stats.st_size == 0:
                    return

                with open(Manager.database_file, 'r') as f:
                        file_data = list(f)
                        f.close()

                #Build todo objects from the data in each line
                Manager.todo_list.clear()
                for line in file_data:
                        todo = ToDo()
                        #Remove EOL character(s)
                        line = line.rstrip()
                        todo_attrs = line.split("|")
                        for todo_attr in todo_attrs:
                                prop, value = todo_attr.split(":")
                                setattr(todo, prop, value)
                        Manager.todo_list.append(todo)

                print("Records have been imported from PyToDo database file.")


    
#Test Code
manager = Manager()

	
