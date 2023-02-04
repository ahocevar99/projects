import requests;
from PIL import Image
import json

def mainMenu(): 
    print ("MAIN MENU: ")
    print ("1: users; 2: carts; 3: products")
    text = input ("\nenter the number: ")

    if text == "1":
        getData("users")
    if text == "2":
        getData("carts")
    if text == "3":
        getData("products")
    else: 
        print ("\nUnknown input.\n")
        mainMenu()

def getData (resource):
    def findById():
        getId = input ("enter id: ")
        dataFound = requests.get ('https://dummyjson.com/{}/{}'.format(resource, getId))
        if dataFound.status_code == 404: print (("{} with id '{}' not found. ").format(resource[0:-1],getId)), findById()
        else: 
            dataFound = dataFound.json()
            if resource == "users": r = "USER"
            elif resource == "products": r = "PRODUCT"
            elif resource == "carts": r = "CART" 
            print (("\n{} with id: '{}'").format(r,getId))
            for param in dataFound:
                print ('{}: {}'.format(param, dataFound[param]))
            print ("\n")
        dataMenu(resource)
    def getAllData():
        dataFound = requests.get ('https://dummyjson.com/{}'.format (resource))
        dataFound = dataFound.json()
        if dataFound['total'] == 0:
            print ("\nNo data found. \n")
        else:
            dataFound = dataFound[resource]
            if resource == "users":
                print ('\nALL USERS: \n')
                for i in dataFound:
                    print ('{}: {} {}, {}, age: {}'.format(i['id'], i['firstName'], i['lastName'], i['gender'], i['age']))
            elif resource == "products":
                print ('\nALL PRODUCTS: \n')
                for i in dataFound:
                    print ('{}: {}, {}, price: {}'.format(i['id'], i['title'], i['description'], i['price']))
            elif resource == "carts":
                print ('\nALL CARTS')
                for i in dataFound:
                    print ('{}: discounted total: {}, userId: {}, quantity: {}'.format(i['id'], i['discountedTotal'], i['userId'], i['totalQuantity']))
        dataMenu(resource)
    def saveDataImage():
        getId = input ("Enter the id: ")
        dataFound = requests.get('https://dummyjson.com/{}/{}'.format(resource, getId))
        if dataFound.status_code == 404: print (("{} with id '{}' not found. ").format(resource[0:-1], getId)), saveDataImage()
        else: 
            dataFound = dataFound.json()
            if resource == "users": imgUrl = dataFound['image']
            elif resource == "products": imgUrl = dataFound['images'] 
            index = 0
            if resource == "users":
                img = Image.open(requests.get(imgUrl, stream = True).raw)
                index=+1
                img.save(("{} {}.png").format(dataFound['firstName'], dataFound['lastName']))
            elif resource == "products":
                for image in imgUrl:
                    img = Image.open(requests.get(image, stream = True).raw)
                    index += 1
                    img.save(("{} {}.png").format(dataFound['title'], index))
            print (("{} image(s) saved\n").format(index)), dataMenu(resource) 
    def searchDataWithParams():
        if resource == "users":
            print ("\nFIND USER by KEY and VALUE\n")
            key = input ("enter key: ")
            value = input ("enter value: ")
            dataFound = requests.get('https://dummyjson.com/users/filter?key={}&value={}'.format(key,value))
            dataFound = dataFound.json()
            dataFound = dataFound['users']
            print ("\n{} USERS FOUND: ".format(len (dataFound)))
            for i in dataFound:
                print ('{} {}, {} = {}, id = {}'.format(i['firstName'], i['lastName'], key, i['{}'.format(key)], i['id']))
            dataMenu(resource)
        elif resource == "products":
            print ("\nsearch by CATEGORIES: \n")
            categories = requests.get ('https://dummyjson.com/products/categories')
            categories = categories.json()
            index = 0
            for cat in categories:
                offset = 20 - len(cat)
                print (cat, end =" "+' '*offset)
                index+=1
                if index % 4==0: print ("\n")
            category = input ("Enter a category: ")
            dataFound = requests.get ('https://dummyjson.com/products/category/{}'. format(category))
            dataFound = dataFound.json()
            dataFound = dataFound['products']
            print ("\n{} PRODUCTS FOUND: ".format(len (dataFound)))
            for product in dataFound:
                print ('{}, price: {}, category: {}, id = {}'.format(product['title'], product['price'], product['category'], product['id']))
            dataMenu(resource)
    def addData():
        if resource == "users":
            print ("\nADD user\n")
            firstName = input("first name: ")
            lastName = input ("last name: ")
            age = input ("age: ")
            addedData = {"firstName": "{}".format(firstName.capitalize()),
                        "lastName": "{}".format(lastName.capitalize()),
                        "age": "{}".format(age)}
            dataAdd = requests.post ('https://dummyjson.com/users/add', data = addedData)
            print ("\nUser ADDED: ")
            print (dataAdd.json())
            dataMenu(resource)
        elif resource == "products":
            print ("\nADD product\n")
            title = input("title: ")
            description = input ("description: ")
            price = input ("price: ")
            addedData = {"title": "{}".format(title.capitalize()),
                        "description": "{}".format(description.capitalize()),
                        "price": "{}".format(price)}
            dataAdd = requests.post ('https://dummyjson.com/products/add', data = addedData)
            print ("\nProduct ADDED: ")
            print (dataAdd.json())
            dataMenu(resource)
    def updateData():
        print ("\nUPDATE {}\n".format ("user" if resource == "users" else "product"))
        getId = input ("id of a{}: ".format("n user" if resource == "users" else " product"))
        key = input ("key: ")
        value = input ("value: ")
        dataUpdate = requests.put ('https://dummyjson.com/{}/{}'.format (resource, getId), data = {'{}'.format(key): '{}'.format(value)})
        print ("\n{} UPDATED: ".format("User" if resource == "users" else "Product"))
        print (dataUpdate.json())
        dataMenu(resource)
    def deleteData():
        print ("\nDELETE {}\n".format ("user" if resource == "users" else "product"))
        getId = input ("id of a{}: ".format("n user" if resource == "users" else " product"))
        deletedData = requests.delete ('https://dummyjson.com/{}/{}'.format (resource, getId))
        deletedData = deletedData.json()
        if (deletedData['isDeleted'] == True):
            print ("\n{} with id: '{}' DELETED on {}". format (("User" if resource == "users" else "Product"), getId, deletedData['deletedOn']))
        dataMenu(resource)
    def dataMenu(resource):
        print ("\n{} MENU: ".format(resource.upper()))
        print ("1: find {} by id".format(resource[0:-1]))
        print ("2: get all {}".format(resource))
        print ("3: save image(s) of a{}".format("n " + resource[0:-1] if resource == "users" else " "+resource[0:-1]))
        print ("4: search {} with parametres".format(resource))
        print ("5: add {}".format(resource[0:-1]))
        print ("6: update {}".format(resource[0:-1]))
        print ("7: delete {}".format(resource[0:-1]))
        print ("-1: back to main menu")
        inp = input ("\nenter the number: ")
        if inp == "1": findById()
        elif inp == "2": getAllData()
        elif inp == "3": saveDataImage()
        elif inp == "4": searchDataWithParams()
        elif inp == "5": addData()
        elif inp == "6": updateData()
        elif inp == "7": deleteData()
        elif inp == "-1": print ("\n"), mainMenu()
        else: print ("\nunknown command"), dataMenu(resource)
    dataMenu(resource)   
mainMenu()
