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
    allUsers = requests.get ('https://dummyjson.com/users').json()
    allProducts = requests.get ('https://dummyjson.com/products').json()
    allCarts = requests.get ('https://dummyjson.com/carts').json()
    def findById():
        getId = input ("enter id: ")
        if (getId == ""): findById()
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
        if (getId == ""): saveDataImage()
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
    def getUserCarts():
        getId = input ("Enter the id of an user: ")
        if (getId == ""): getUserCarts()
        dataFound = requests.get('https://dummyjson.com/carts/user/{}'.format(getId))
        dataFound = dataFound.json()
        dataFound = dataFound['carts']
        print ("\n{} CART{} FOUND: ".format(len (dataFound), "S" if len(dataFound) > 1 else ""))
        for i in dataFound:
            print ("{} product{} in this cart: ".format(i['totalProducts'], "" if i['totalProducts'] == 1 else "s"))
            for product in i['products']:
                print (product)
            print ("total quantity: {}".format(i['totalQuantity']))
            print("total: {}".format(i['total']))
            print("discounted total: {}".format(i['discountedTotal']))
        dataMenu(resource)
    def searchDataWithParams():
        if resource == "users":
            print ("\nFIND USER by KEY and VALUE\n")
            key = input ("enter key: ")
            value = input ("enter value: ")
            dataFound = requests.get('https://dummyjson.com/users/filter?key={}&value={}'.format(key,value))
            dataFound = dataFound.json()
            dataFound = dataFound['users']
            print ("\n{} USER{} FOUND: ".format(len (dataFound), "S" if len(dataFound) > 1 else ""))
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
            print ("\n{} PRODUCT{} FOUND: ".format(len (dataFound), "S" if len(dataFound) > 1 else ""))
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
        elif resource == "carts":
            print ("\nADD cart\n")
            userIdCart = input ("this cart is from the user with id: ")
            if int(userIdCart) not in range (1, allUsers['total']):
                print ("user with id '{}' not found.".format (userIdCart))
                addData()
            products = []
            while (1): 
                productId = input ("product id: ")
                if productId == "": continue
                if (productId == "-1"): break
                if (int(productId) not in range (1, allProducts['total'])):
                    print ("product with id '{}' not found.".format (productId))
                    continue
                productQuantity = input ("quantity: ")
                if productQuantity == "":
                    continue
                current = {"id": "{}".format(productId),
                            "quantity": "{}".format(productQuantity)}
                products.append(current)
            addedData = {"userId": "{}".format(userIdCart),
                         "products": "{}".format(products)}
            #print (addedData)
            dataAdd = requests.post('https://dummyjson.com/carts/add', data = addedData)
            #print ("\nCart ADDED: ")
            print ("Not working properly ...")
            print (dataAdd.json())
            dataMenu(resource)

    def updateData():
        if (resource == "carts"):
            print ("\nUPDATE cart\n")
            getId = input ("id of a cart: ")
            if (getId == "" or int(getId) not in range (1, allCarts['total'])): updateData()
            cartProductId = input("id of a product in a cart: ")
            cartQuantity = input ("set quantity to: ")
            dataToArr = {"merge": "true", "products": [{"id": "{}".format(cartProductId),
                          "quantity": "{}".format(cartQuantity)}]}
            dataUpdate = requests.put('https://dummyjson.com/carts/{}'.format(getId), data = dataToArr)
            #print ("\nCart UPDATED: ")
            print ("Not working properly ...")
            print (dataUpdate.json())
        else:
            print ("\nUPDATE {}\n".format ("user" if resource == "users" else "product"))
            getId = input ("id of a{}: ".format("n user" if resource == "users" else " product"))
            if (getId==""): updateData()
            key = input ("key: ")
            value = input ("value: ")
            dataUpdate = requests.put ('https://dummyjson.com/{}/{}'.format (resource, getId), data = {'{}'.format(key): '{}'.format(value)})
            print ("\n{} UPDATED: ".format("User" if resource == "users" else "Product"))
            print (dataUpdate.json())
        dataMenu(resource)
    def deleteData():
        if resource == "users": r = "user"
        elif resource == "products": r = "product"
        elif resource == "carts": r = "cart" 
        print ("\nDELETE {}\n".format (r))
        getId = input ("id of a{}: ".format("n "+r if r =="user" else " "+r))
        if (getId == ""): deleteData()
        if (resource == "users" and int(getId) not in range(1, allUsers['total'])): print ("User with id '{}' not found".format(getId)), deleteData()
        if (resource == "products" and int(getId) not in range(1, allProducts['total'])): print ("Product this id '{}' not found".format(getId)), deleteData()
        if (resource == "carts" and int(getId) not in range(1, allCarts['total'])): print ("Cart with id '{}' not found".format(getId)), deleteData()
        deletedData = requests.delete ('https://dummyjson.com/{}/{}'.format (resource, getId))
        deletedData = deletedData.json()
        if (deletedData['isDeleted'] == True):
            print ("\n{} with id: '{}' DELETED on {}". format ((r.capitalize()), getId, deletedData['deletedOn']))
        dataMenu(resource)
    
    def dataMenu(resource):
        if resource == "carts":
            print ('\nCARTS MENU: ')
            print ("1: find cart by id")
            print ("2: get all carts")
            print ("3: get carts of a user")
            print ("4: add cart")
            print ("5: update cart")
            print ("6: delete cart")
            print ("-1: back to main menu")
            inp = input ("\nenter the number: ")
            if inp == "1": findById()
            elif inp == "2": getAllData()
            elif inp == "3": getUserCarts()
            elif inp == "4": addData()
            elif inp == "5": updateData()
            elif inp == "6": deleteData()
            elif inp == "-1": print ("\n"), mainMenu()
            else: print ("\nunknown command"), dataMenu(resource)
        else:
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
