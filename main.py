# Imports
from replit import db
from random import randint
from flask import Flask, request, redirect, jsonify
import os


# Making your app an object of the Flask class
app = Flask(__name__, static_folder="static", static_url_path="/static")


# Making the number for the key in db
def makeKey():

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



# The route() function of the Flask class tells the application which URL should call the associated function
# @app.route(rule, options)
# rule = the url binding with the function
# options = a list of parameters
# whatever function comes after this line is bounded to the rule and will execute when page is run

@app.route("/")
def give_homepage():
	return redirect("/home")

@app.route("/home") 
def homepage(): 
	return app.send_static_file('homepage.html')




@app.route("/form")
def give_form():
	return app.send_static_file("index.html")




# Handling file upload in Flask needs an HTML form with its enctype attribute set to ‘multipart/form-data’, posting the file to a URL. The URL handler fetches file from request.files[] and saves it to the desired location.

# after user fills out form 
@app.route("/create_card", methods=["POST"])
def create_card():

  ## FOR THE IMAGE:
  # gets the image file from the form
  image = request.files["image"]

  # gets the type of image (png,jpeg etc.) by taking the image's actual filename and splitting it at the "." and taking the last item (the extension)
  extension = image.filename.split(".")[-1]

  # make a name for the image
  k = makeKey()

  # the filename is now the url.extension eg. "123456.jpg"
  filename = k + "." + extension


	# operating system module - handles files and folders
	# - if "static/images" folder does not exist, make directory (mkdir) "static/images" 
  if not os.path.exists("static/images"):
	  os.mkdir("static/images")

	# save image in that folder
  image.save("static/images/" + filename)

  ## FOR THE TEXT:
  # Save the text as a key value pair in the database with the same key as the image's url and the values from the form
  db[k] = {
    "bgcolour": request.form["bgcolour"],
	  "textcolour": request.form["textcolour"],
    "body": request.form["body"]
  }

  return redirect("/card?img=" + filename)
	

# Give the user the card
@app.route("/card")
def card():
  return app.send_static_file("cardpage.html")


# Get the info from the database 
@app.route("/card/<string:card_id>")
def get_info(card_id):
  return jsonify(dict(db[card_id]))

  
# The run method of the Flask class runs the application on the local server
# app.run(host, port, debug, options)

# host = hostname to listen on (default is 127.0.0.1 = localhost) (0.0.0.0 to have it available externally)
# port = defaults to 5000
# debug = default set to false (if a change in code happens, you have to restart the application manually, debug = True enables debug support: automatically reloads to update changes)

if __name__ == '__main__':
  app.run(host="0.0.0.0")