from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    # create encryption key and write to file
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    # load existing encryption key from file
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    # create new password file to add new passwords
    def create_password_file(self, path, initial_values=None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    # load existing password file and decrypt contents
    def load_password_file(self, path):
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    # add new password to dictionary and save to password file
    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                # one for each line
                f.write(site + ":" + encrypted.decode() + "\n")

    def get_password(self, site):
        return self.password_dict[site]

def main():
    # initial passwords
    password = {
        "email": "email_pass",
        "youtube": "youtube_pass",
        "tiktok": "tiktok_pass"
    }

    pm = PasswordManager()

    print("""What do you want to do?
          (1) Create a new key
          (2) Load an existing key
          (3) Create new password file
          (4) Load existing password file
          (5) Add new password
          (6) Get a password
          (q) Quit program
          """)
    
    done = False
    
    while not done:
        choice = input("Enter your choice: ")

        match choice:

            # create new key
            case "1":
                path = input("Enter path for new key: ")
                pm.create_key(path)

            # load existing key
            case "2":
                path = input("Enter path for existing key: ")
                pm.load_key(path)
            
            # create new password file
            case "3":
                path = input("Enter path for new password file: ")
                pm.create_password_file(path, password)
            
            # load existing password file
            case "4":
                path = input("Enter path for existing password file: ")
                pm.load_password_file(path)

            # add new password
            case "5":
                site = input("Enter the new site: ")
                password = input("Enter the new password: ")
                pm.add_password(site, password)

            # retrieve password
            case "6":
                site = input("What site password do you want? ")
                print("Password for " + site + " is " + pm.get_password(site))
            
            #quit
            case "q":
                done = True
                print("Thanks for using the password manager.")

            # choice validation
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main()