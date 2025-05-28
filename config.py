import json as js
import bcrypt
class User:
    def __init__(self,name,password,locked,user_vault):
        self.name = name
        self.password = password
        self.locked = locked
        self.user_vault = user_vault if user_vault is not None else []
    
    def lock(self):
        self.locked = True
        print(f"{self.name} is now locked.")

    def change_pass(self):
        if self.check_password():
            password = input("Enter your new password: ")
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            data,users=get_users()
            for user in users:
                if self.name == user["name"]:
                    user["password"] = hashed_pw
                    self.password = hashed_pw
                    write_file(data)
    def check_password(self):
        while self.locked:
                print(f"User {self.name} is locked. Please unlock to continue.")
                action = input("Do you want to unlock? (yes/no): ").strip().lower()
                if action == 'yes':
                    if self.unlock():
                        print(f"User {self.name} is now unlocked.")
                        return True
                elif action == 'no':
                    print("Exiting the program.")
                    return False
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        attempts = 3
        while attempts > 0:
            entered = input("Please enter your password: ")
            if bcrypt.checkpw(entered.encode(), self.password.encode()):
                print("Password is correct.")
                return True
            else:
                print("Incorrect password.")
                attempts -= 1
            if attempts == 0:
                print("Too many incorrect attempts. User is now locked.")
                self.lock()
                return False
            else:
                print(f"You have {attempts} attempts left.")

    def unlock(self):
        password = input("Enter your password to unlock: ")
        if password == self.password:
            self.locked = False
            return True
        else:
            print("Incorrect password. User remains locked.")
            return False
    
    def add_pass(self):
        password = input("Enter a password to add to the vault: ")
        data,users=get_users()
        for user in users:
            if self.name == user["name"]:
                if not password in user["vault"]:
                    user["vault"].append(password)
                    self.user_vault.append(password)
                    write_file(data)
                    print("Password added to vault")
                else:
                    print("Password already in vault")

    def remove_pass(self):
        password = input("Enter a password to remove from the vault: ")
        data,users=get_users()
        for user in users:
            if self.name == user["name"]:
                if password in user["vault"]:
                    user["vault"].remove(password)
                    self.user_vault.remove(password)
                    write_file(data)
                    print("Password removed from vault")
                else:
                    print("Password not found in vault")

    def view_pass(self):
        data,users=get_users()
        for user in users:
            if self.name == user["name"]:
                for password in user["vault"]:
                    print(f"- {password}")

    def vault_actions(self):
        while True:
            action = input("What would you like to do? (add/remove/view/pass/exit): ").strip().lower()
            if action == 'add' or action == "1":
                self.add_pass()
            elif action == 'remove' or action == "2":
                self.remove_pass()
            elif action == 'view' or action == "3":
                self.view_pass()
            elif action == "pass" or action == "4":
                self.change_pass()
            elif action == 'exit' or action == "5":
                print("Exiting the vault.")
                break
            else:
                print("Invalid action. Please try again.")

def get_data():
    with open("users.json","r") as f:
        data = js.load(f)
        return data

def get_users():
    with open("users.json","r") as f:
        data = js.load(f)
        return data,data["users"]

def write_file(data):
    with open("users.json","w") as f:
        js.dump(data,f,indent=4)