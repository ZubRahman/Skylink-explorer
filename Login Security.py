def hashdata(password):
    import random
    dict = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
    newpassword = ""
    for x in range(len(password)):
        newpassword += random.choice(dict)
    try:
        file = open("data.txt", "a")
        file2 = open("Uncrypted data.txt", "a")
        try:
            file.write("\n" + newpassword)
            file2.write("\n" + password)
        except:
            print("something went wrong")
        finally:
            file.close()
            file2.close()
    except:
        print("something went wrong")

# example:
hashdata("hello world")