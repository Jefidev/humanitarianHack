import json
import base64
import os
from random import randint,choice
import datetime


def random_list_user():
    path_image = "./resources/face/"
    images = os.listdir(path_image)

    list_psw = ["psw","cpi","coco"]
    list_sq = ["papa","dobby","TheBest"]

    names = ["Genin","Fink","Georis"]
    firstnames = ["Simon","Jerome","Francois"]

    users = []

    for i in range(0,len(images)) :

        if(images[i].split(".")[-1] == "jpg"):
            user = {
                "identifications":{},
                "parameters":{
                    "general_info":{}
                }
            }

            identification = {}


            sourceFile = path_image+images[i]
            print(sourceFile)

            imageSource = open(sourceFile,'rb')
            encoded_img_b64 = base64.b64decode(imageSource.read())

            identification["image"] = encoded_img_b64
            identification["psw"] = list_psw[i]
            identification["sq"] = list_sq[i]

            user["identifications"] = identification

            general_info = {}

            general_info["name"] = choice(names)
            general_info["firstname"] = choice(firstnames)

            general_info["birthdate"]  = datetime.date(randint(1980,2010), randint(1,12),randint(1,28))

            user["parameters"]["general_info"] = general_info

            users.append(user)

    return users



        

