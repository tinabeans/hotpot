# IMPORT STUFF!!

# python standard libraries
import hashlib, random, json

# nice 3rd party stuff
import flask
from flaskext.mail import Mail, Message
import pymongo
from pymongo.objectid import ObjectId

# used to put stuff in the db
import saveStuff

# creating new Flask instance
app = flask.Flask(__name__)
app.config.from_pyfile('config.cfg')

# start up mail object to send messages via SMTP
mail = Mail(app)

# really secret secret key! used for Flask sessions...
app.secret_key = '''nTi!"2Oq#j2WdnUsQziTn52y8xGfZl:"MH*H|`yVClNLA4UG'GIvq1qc%Gk}vu<'''

# open database connection!
connection = pymongo.Connection()
db = connection.hotpot

codes = db.inviteCodes
users = db.users
snippets = db.snippets
recipes = db.recipes

@app.route('/')
def index():
	return flask.render_template('home.html')

@app.route('/generateCode')
def showGenerateCodeForm():
	return flask.render_template('generateCode.html')

@app.route('/newCode', methods=['POST'])
def generateCode():
	requestData = flask.request.form
	
	# generate a random "code"
	code = random.randint(100000,999999)
	
	while codes.find_one({ 'code' : code }) is not None:
		code = random.randint(100000,999999)
	
	newDocument = {
		'name' : requestData['name'],
		'email' : requestData['email'],
		'code' : code,
		'redeemed' : False
	}
	
	print newDocument
	
	codes.insert(newDocument)
	
	return flask.render_template('newCode.html', data = newDocument)

@app.route('/redeemCode')
def showRedeemCodeForm():
	return flask.render_template('redeemCode.html')
	
@app.route('/checkCode', methods=['POST'])
def checkCode():
	code = flask.request.form['code']
	
	if code.isdigit():
		code = int(code)
		
		codeDocument = codes.find_one({ 'code' : code })
		
		print codeDocument
		
		if codeDocument is not None:
			codes.update(
				{ 'code' : code },
				{ '$set' : { 'redeemed' : True }}
			)
			
			return flask.render_template('newAccount.html', data=codeDocument)
	
	return 'code not found'
	
@app.route('/saveProfile', methods=['POST'])
def saveProfile():
	data = flask.request.form
	
	# insert/update entries in users db
	# is there some magical fast way to do this?
	# users.update({ '
	
	# do some fancy ajax?
	return "okiedoke"

@app.route('/profile', methods=['POST', 'GET'])
def viewProfile():
	data = flask.request.form
			
	return flask.render_template('profile.html', data=data)


##############################################################################
# REGISTRATION

@app.route('/register')
def showRegistration():
	return flask.render_template('registration.html')

@app.route('/registerAction', methods=['POST'])
def register():
	data = flask.request.form
	
	# create the user's db entry
	users.insert({
		'email' : data['email'],
		'name' : data['name'],
		'password' : data['password']
	})
	
	# be nice and log the user in too
	flask.session['email'] = data['email']
		
	return "okay you're registered!"


##############################################################################
# LOGIN

@app.route('/login')
def showLogin():
	return flask.render_template('login.html')


@app.route('/loginAction', methods=['POST'])
def login():
	data = flask.request.form
	
	userDocument = users.find_one({'email' : data['email'], 'password' : data['password']})
	
	if userDocument is not None:
		flask.session['email'] = data['email']
	
		return 'omg you logged in!'
	else:
		return 'login info is wrongfaced'


@app.route('/logout')
def logout():
	flask.session.pop('email', None)
	return "omg you logged out!"


##############################################################################
# RECIPE

@app.route('/meals/<recipe>')
def showRecipe(recipe):
	
	recipe = db.recipes.find_one({ 'slug' : recipe })
	
	return flask.render_template( 'recipe.html', recipe=recipe )


##############################################################################
# INVITE

@app.route('/invite/<recipe>')
def showInviteForm(recipe):
	
	recipe = db.recipes.find_one({ 'slug' : recipe })
	
	if 'email' not in flask.session:
		return flask.redirect('/login')
	else:
		user = db.users.find_one({'email' : flask.session['email']})
		return flask.render_template('invite.html', recipe=recipe, user=user )


@app.route('/inviteEmail/<recipe>')
def sendEmail(recipe):
	
	recipe = db.recipes.find_one({ 'slug' : recipe })
	
	return flask.render_template('inviteEmail.html', recipe=recipe)

@app.route('/sendInvite', methods=['POST'])
def sendInvite():
	
	# put incoming values in a dictionary
	newInvite = {}
	for key in ['to', 'from', 'message', 'recipe', 'datetime', 'friendName', 'fromName', 'readableDate', 'readableTime']:
		newInvite[key] = flask.request.form[key]
	
	# store new invite dictionary in database
	newInvite['status'] = "new"
	newInvite['datetime'] = int(newInvite['datetime']) # convert from string to int
	db.invites.insert(newInvite)
	
	# retrieve recipe based on slug
	recipe = db.recipes.find_one({'slug' : newInvite['recipe']})
	
	# compose email to send
	msg = Message("Hotpot Invite Test", recipients=[newInvite['to']])
	msg.body = "test..."
	msg.html = flask.render_template('inviteEmail.html', recipe=recipe, invite=newInvite)
	mail.send(msg)

	return flask.render_template('inviteEmail.html', recipe=recipe, invite=newInvite)


##############################################################################
# ROOM

@app.route('/<recipe>/room/<roomId>')
def showRoom(recipe, roomId):
	# check to see if the person's logged in
	if 'email' not in flask.session:
		return flask.render_template('login.html') 
	else:
		room = db.rooms.find_one({'_id' : ObjectId(roomId)})
		recipe = recipes.find_one({'slug' : recipe})
		
		# grab all the foodNotes related to this room
		foodNotesInThisRoom = list(db.foodNotes.find({'roomId' : ObjectId(roomId)}))
		
		# and insert them into the recipe object
		for step in recipe['steps']:
		
			snippetsToInsert = []
			stepId = step['id'];
			
			# the for-loop below is for grabbing just the foodNotes related to this step
			
			# crazy Python list comprehension magic to grab only the foodnotes related to this room & step
			# the first 'note' represents what gets returned by the filtered list
			# the second 'note' represents the list item that is being 'comprehended' (in this case filtered by the if)
			# I hope these comments still make sense in 2 weeks
			for foodNote in (note for note in foodNotesInThisRoom if note['stepId'] == stepId):
				snippet = {}
				snippet['type'] = 'foodNote'
				
				userInfo = db.users.find_one({'email' : foodNote['userId']})
				snippet['username'] = userInfo['name']
				snippet['_id'] = foodNote['_id']
				snippet['text'] = foodNote['text']
				
				snippetsToInsert.append(snippet)
			
			step['snippets'] = snippetsToInsert
		
		# grab all the badges too
		badges = list(db.badges.find())
			
		return flask.render_template('room.html', recipe=recipe, userId=flask.session['email'], roomId=roomId, badges=badges )


def postFoodnote():
	data = flask.request.json
	
	# put together the new user note to send to the database!
	newUserNote = {
		"user_id": flask.session['email'], # users are uniquely identified by their email
		"recipe_id": ObjectId(data['recipe_id']),
		"snippet_id": ObjectId(data['snippet_id']),
		"text": data['text']
	}
	
	# now insert the data, and store the id
	newUserNoteId = userNotes.insert(newUserNote);
	
	# now put together some data to send back to the template...
	
	# get user name based on email
	userInfo = users.find_one({ 'email' : flask.session['email'] })
	
	# HEEEEEEEEEEEEEEEEEEEEELLLLLLLLLLLPPPPPPPPPPPPPPPPPPPPPPP SINGLE QUOTES!!?
	dataForResponse = {
		'noteId' : str(newUserNoteId),
		'username' : str(userInfo['name'])
	}
	
	return str(dataForResponse)


##############################################################################
# SOCKET.IO ENDPOINT for IN-ROOM COMMUNICATIONINGS

@app.route('/socketMessageHandler', methods=['POST'])
def doStuffWithStuffFromTornado():
	requestJSON = flask.request.json
	data = requestJSON['data']
	
	userInfo = None
	# if message is coming from a user, get user database entry based on userId
	if 'userId' in requestJSON:
		userInfo = users.find_one({ 'email' : requestJSON['userId'] })
	
	# do different things depending on what the socket message says...
	if requestJSON['type'] == 'foodNote':
	
		# put together the new user note to store in the database!
		newFoodNote = {
			"userId": requestJSON['userId'], # users are uniquely identified by their email
			"roomId": ObjectId(data['roomId']),
			"stepId": data['stepId'],
			"text": data['text']
		}
		
		# now insert the data, and store the id
		newFoodNoteId = db.foodNotes.insert(newFoodNote);
		
		# now put together some data to send back to the template...
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				"stepId": data['stepId'],
				'noteId' : str(newFoodNoteId),
				'username' : userInfo['name'],
				"text": data['text']
			}
		}
	
	elif requestJSON['type'] == 'chat':
		
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				'userId' : userInfo['name'],
				'chatMessage' : data['chatMessage']
			}
		}
		
	elif requestJSON['type'] == 'recipeStep':
		
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				'username' : userInfo['name'],
				'stepNumber' : data['stepNumber'],
				'userId' : requestJSON['userId']
			}
		}
	
	elif requestJSON['type'] == 'focus':
		
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				'username' : userInfo['name'],
				'userId' : requestJSON['userId'],
				'focus' : data['focus']
			}
		}
				
	# use json.dumps() instead of str() because on the other end we need a well-formatted JSON string with double-quotes
	print dataForResponse
	return json.dumps(dataForResponse)


##############################################################################
# UTILS for a Tina

@app.route('/saveStuff')
def saveStuffFunction():
	saveStuff.start(db)
	return "database being populated. omgscary"
	


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True)