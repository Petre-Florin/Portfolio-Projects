import config as cfg
import os
import json as js
import bcrypt

def main():
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            js.dump({"users": []}, f)

    while True:
        data,users=cfg.get_users()
        name= input("Enter your name: ")
        found=False
        for user in users:
            if name == user["name"]:
                found=True
                break

        if found == False:
            password = input("Enter your password: ")
            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            current_user = cfg.User(name, hashed_pw, False , None)
            new_user={"name":current_user.name,"password":current_user.password,"locked":current_user.locked,"vault":current_user.user_vault}
            data["users"].append(new_user)
            cfg.write_file(data)
            print(f"User {name} created successfully.")

        else:
            print(f"Welcome back, {name}.")
            for user in data["users"]:
                if name == user["name"]:
                    current_user=cfg.User(user["name"],user["password"],user["locked"],user["vault"])

        if current_user.check_password():
            current_user.vault_actions()
        else:
            print("Access denied. Please try again later.")
            continue

main()