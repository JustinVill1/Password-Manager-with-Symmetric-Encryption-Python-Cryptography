from cryptography.fernet import Fernet
import json

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    #function that is creating the key to decrypt encryption
    def createKey(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    #function that is looking up key and reading the key from its file
    def loadKey(self, path):
        with open(path,'rb') as f:
            self.key = f.read()

    #function that is creating the password file where the passwords are going to be stored
    def createPasswordFile(self,path,initialVal=None):
        self.password_file = path
        open(path, 'a').close()


        if initialVal is not None:
            for key, value in initialVal.items(): 
                self.addPassword(key,value)
                
    #function that takes you to encrytped password file decrypts them
    def loadPasswordFile(self,path):
        self.password_file = path

        with open(path,'r') as f:
            for line in f:
                site, encrypted = line.strip().split(":", 1)
                decrypted = Fernet(self.key).decrypt(encrypted.encode()).decode()
                self.password_dict[site] = json.loads(decrypted)

    #Adds a password and then encrypts it
    def addPassword(self,site,credentials):
        self.password_dict[site] = credentials

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(json.dumps(credentials).encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    # Checks to see if password i want is in the password file
    def getPassword(self,site):
        creds = self.password_dict.get(site)
        if creds is None:
            return "Site not found."
        return f"Username: {creds['Username']}, Password: {creds['Password']}"
    
def main():
    password = {
        "Amazon" : {"Username" : "JohnDoe", "Password" : "JohnDoe123"},
    }

    pm = PasswordManager()


    print("""What do you want to do? 
        1. Create a new key
        2. Load an existing key
        3. Create a new Password File
        4. Load existing password file
        5. Add a new password
        6. get a password
        7. quit
        """)

    done = False

    while not done: 
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter Path: ")
            pm.createKey(path)              #calls to create a new key
        elif choice == "2":
            path = input("Enter path")
            pm.loadKey(path)                #calls to load an existing key
        elif choice == "3":
            path = input("Enter Path: ")
            pm.createPasswordFile(path,password)            #calls to create a new password file and creates a path there
        elif choice == "4":
            path = input("Enter Path: ")
            pm.loadPasswordFile(path)                       #calls to load an existing password file 
        elif choice == "5":
            site = input("Enter the site: ")
            username = input("Enter the username: ")
            pwd = input("Enter the password: ")
            pm.addPassword(site, {"Username": username, "Password": pwd})           #calls to add the given password and username into the password file
        elif choice == "6":
            site = input("What site do you want: ")
            print(f"The information for {site} is {pm.getPassword(site)}")          #gets the username and password from the site entered by user
        elif choice == "7":
            done = True
            print("Bye")
        else:
            print("Invalid Choice!")

if __name__ == "__main__":
    main()