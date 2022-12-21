from replit import db
from random import randint
from flask import request
import os

class ecard (object):

    def __init__(self):
        pass




			
    # Making the number for the key in db
    def makeKey(self):

        # Creating the random 6 character number
        # zfill fills the number (less than 6 digits) with zeroes in front of it
        k = str(randint(0,100000)).zfill(6)

        # checks to make sure there is no repeat
        check = db.prefix(k) # prefix method returns nothing if the number is unique

        # if check is not nothing, keep making numbers until it is nothing
        while len(check) != 0:
            k = str(randint(0,100000)).zfill(6)
            check = db.prefix(k)

        # Setting the key to an empty string to get the key into the db
        db[k] = ""

        return k



	
    def createCard(self):

        ## FOR THE IMAGE:
        # gets the image file from the form
        image = request.files["image"]

        # gets the type of image (png,jpeg etc.) by taking the image's actual filename and splitting it at the "." and taking the last item (the extension)
        extension = image.filename.split(".")[-1]

        # make a name for the image
        k = self.makeKey()

        # the filename is now the url.extension eg. "123456.jpg"
        fn = k + "." + extension


        # operating system module - handles files and folders
        # - if "static/images" folder does not exist, make directory (mkdir) "static/images"
        if not os.path.exists("static/images"):
        	os.mkdir("static/images")

        # save image in that folder
        image.save("static/images/" + fn)

        ## FOR THE TEXT:
        # Save the text as a key value pair in the database with the same key as the image's url and the values from the form


        db[k] = {
        	"bgcolour": request.form["bgcolour"],
        	"textcolour": request.form["textcolour"],
        	"body": request.form["body"],
        	# "sender_email": request.form["sender_email"],
        	# "password": request.form["sender_email_password"],
        	# "receiver_email": request.form["receiver_email"],
        	# "receiver_name": request.form["receiver_name"]
        }

        return fn