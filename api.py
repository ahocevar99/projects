import requests;
from PIL import Image

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
            print (("\nDATA with id: '{}'").format(getId))
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
    def dataMenu(resource):
        print ("\n{} MENU: ".format(resource.upper()))
        print ("1: find {} by id".format(resource[0:-1]))
        print ("2: get all {}".format(resource))
        print ("3: save image(s) of an {}".format(resource[0:-1]))
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
        elif inp == "-1": print ("\n"), mainMenu()
        else: print ("\nunknown command"), dataMenu()
    dataMenu(resource)   
mainMenu()
