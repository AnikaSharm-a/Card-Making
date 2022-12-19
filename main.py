# Imports
from replit import db
from random import randint
from flask import Flask, request, redirect, jsonify, render_template
from jinja2 import Template
import imgkit
import os
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.utils import formataddr
# from email.mime.multipart import MIMEMultipart 
# from email.mime.base import MIMEBase  
# from email import encoders  


# to run before server startup:
os.system("install-pkg wkhtmltopdf")


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

	return redirect("/card?img=" + fn)
	


	
# Give the user the card
@app.route("/card")
def card():
  return app.send_static_file("cardpage.html")



	
# Get the info from the database 
@app.route("/card/<string:card_id>")
def get_info(card_id):
  return jsonify(dict(db[card_id]))





# For jinja to make a card using the data from user
def build_card_html(values):
	
  template_text = open("static/cardpage_template.html").read()
  template = Template(template_text)
		
  html = template.render(**values)
	
  return html
  


	

# From the imgkit url
@app.route("/card_static/<string:card_fn>")
def card_static(card_fn):

	# key for values in db
  card_id = card_fn.split(".")[0]
  values = db[card_id]

	# adding the image filename into the values dictionary
  values["imgSource"] = "/static/images/" + card_fn

  # bcol = values["bgcolour"]
  # tcol = values["textcolour"]
  # body = values["body"]
  # img = values["imgSource"]

  html = build_card_html(values)
	
	# returning the card image file
  return html




	
# From the download button in cardpage
@app.route("/card_image/<string:card_fn>")
def card_image(card_fn):
	# converts urls to image files
  imgkit.from_url("https://card-making.sharmaanika.repl.co/card_static/" + card_fn, "static/dist/card_" + card_fn)
	
	# sends user the file
  return app.send_static_file("dist/card_" + card_fn)


	



# @app.route("/sendemail/<string:card_fn>")
# def sendemail(card_fn):
# 	# converts urls to image files
# 	imgkit.from_url("https://card-making.sharmaanika.repl.co/card_static/" + fn, "static/dist/card_" + fn)
	
# 	# User configuration

# 	# Change following fields to input from user
	
# 	sender_email = "sender_email" 
# 	sender_name = "sender_name"
# 	password = "sender_email_password"
# 	receiver_emails = ["receiver_email"]
# 	receiver_names = ["receiver_name"]

# 	# Email body
# 	##email_html = open('email.html')
# 	##email_body = email_html.read()

# 	email_body = "This email is sent by ....."

# 	filename = "dist/card_" + card_fn

	
# 	for receiver_email, receiver_name in zip(receiver_emails, receiver_names):
# 		print("Sending the email...")
# 		# Configurating user's info
# 		msg = MIMEMultipart()
# 		msg['To'] = formataddr((receiver_name, receiver_email))
# 		msg['From'] = formataddr((sender_name, sender_email))
# 		msg['Subject'] = 'Hello, my friend ' + receiver_name

# 		msg.attach(MIMEText(email_body, 'html'))

		
		
# 		try:
# 			# Open PDF file in binary mode
# 			with open(filename, "rb") as attachment:
# 				part = MIMEBase("application", "octet-stream")
# 				part.set_payload(attachment.read())

# 			# Encode file in ASCII characters to send by email
# 			encoders.encode_base64(part)

# 			# Add header as key/value pair to attachment part
# 			part.add_header(
# 				"Content-Disposition",
# 				f"attachment; filename= {filename}",
# 			)

# 			msg.attach(part)

		
		
# 		except Exception as e:
# 			print(f'Oh no! We didn\'t find the attachment!\n{e}')
# 			break

		
		
# 		try:
# 			# Creating a SMTP session | use 587 with TLS, 465 SSL and 25
# 			server = smtplib.SMTP('smtp.gmail.com', 587)
			
# 			# Encrypts the email
# 			context = ssl.create_default_context()
# 			server.starttls(context=context)
			
# 			# We log in into our Google account
# 			server.login(sender_email, password)
			
# 			# Sending email from sender, to receiver with the email body
# 			server.sendmail(sender_email, receiver_email, msg.as_string())
			
# 			print('Email sent!')
		
		
# 		except Exception as e:
# 			print(f'Oh no! Something bad happened!\n{e}')
# 			break
		
		
# 		finally:
# 			print('Closing the server...')
# 			server.quit()
	
	
	
# 	return render_template('index.html')




# The run method of the Flask class runs the application on the local server
# app.run(host, port, debug, options)

# host = hostname to listen on (default is 127.0.0.1 = localhost) (0.0.0.0 to have it available externally)
# port = defaults to 5000
# debug = default set to false (if a change in code happens, you have to restart the application manually, debug = True enables debug support: automatically reloads to update changes)

if __name__ == '__main__':
  app.run(host="0.0.0.0")