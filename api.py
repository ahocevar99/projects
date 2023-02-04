import requests;
from PIL import Image

def mainMenu(): 
    print ("MAIN MENU: ")
    print ("1: users; 2: carts; 3: products")
    text = input ("\nenter the number: ")

    if text == "1":
        usersFunction()
    else: 
        print ("\nUnknown input.\n")
        mainMenu()

def usersFunction ():
    def findUser():
        getId = input ("enter id of a user: ")
        usersFound = requests.get ('https://dummyjson.com/users/{}'.format(getId))
        if usersFound.status_code == 404: print (("User with id '{}' not found. ").format(getId)), findUser()
        else: 
            usersFound = usersFound.json()
            print (("\nUSER with id: '{}'").format(getId))
            for param in usersFound:
                print ('{}: {}'.format(param, usersFound[param]))
            print ("\n")
        usersMenu()
    def getAllUsers():
        usersFound = requests.get ('https://dummyjson.com/users')
        usersFound = usersFound.json()
        if usersFound['total'] == 0:
            print ("\nNo users found. \n")
        else:
            usersFound = usersFound['users']
            print ('\nALL USERS: \n')
            for i in usersFound:
                print ('{}: {} {}, {}, age: {}'.format(i['id'], i['firstName'], i['lastName'], i['gender'], i['age']))
        usersMenu()
    def saveImageUser():
        getId = input ("Type user's ID to save his/her image: ")
        usersFound = requests.get('https://dummyjson.com/users/{}'.format(getId))
        if usersFound.status_code == 404: print (("User with id '{}' not found. ").format(getId)), saveImageUser()
        else: 
            usersFound = usersFound.json()
            imgUrl = usersFound['image'] or ""
            if imgUrl == "": print ("no image found"),  saveImageUser()
            img = Image.open(requests.get(imgUrl, stream = True).raw)
            img.save(("{} {}.png").format(usersFound['firstName'], usersFound['lastName']))
            print ("image saved\n"), usersMenu() 
    def searchUsersWithParams():
        return -1
    def usersMenu():
        print ("\nUSERS MENU: ")
        print ("1: find user by id")
        print ("2: get all users")
        print ("3: save image of an user")
        print ("4: search users with parametres")
        print ("5: add user")
        print ("6: update user")
        print ("7: delete user")
        print ("-1: back to main menu")
        inp = input ("\nenter the number: ")
        if inp == "1": findUser()
        elif inp == "2": getAllUsers()
        elif inp == "3": saveImageUser()
        elif inp == "4": searchUsersWithParams()
        elif inp == "-1": print ("\n"), mainMenu()
        else: print ("\nunknown command"), usersMenu()
    usersMenu()   
mainMenu()
