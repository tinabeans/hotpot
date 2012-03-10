# IMPORT STUFF!!

# python standard libraries
import hashlib, random, json, os

# nice 3rd party stuff
import flask
from flaskext.mail import Mail, Message
import pymongo
from pymongo.objectid import ObjectId

# used to put stuff in the db
import saveStuff


##############################################################################
# GLOBAL VARIABLES & CONFIG

USERPIC_FOLDER = 'static/uploads/userpics'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])


# creating new Flask instance
app = flask.Flask(__name__)
app.config.from_pyfile('config.cfg')


# start up mail object to send messages via SMTP
mail = Mail(app)

# really secret secret key! used for Flask sessions...
app.secret_key = '''nTi!"2Oq#j2WdnUsQziTn52y8xGfZl:"MH*H|`yVClNLA4UG'GIvq1qc%Gk}vu<'''


##############################################################################
# DB SETUP

# open database connection!
connection = pymongo.Connection()
db = connection.hotpot


##############################################################################
# HOMEPAGE

@app.route('/')
def index():
	return render_template('home.html')


##############################################################################
# INVITE CODES (NOT NEEDED)
'''
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
'''


##############################################################################
# LOGIN

@app.route('/login')
def showLogin():
	return render_template('login.html')


@app.route('/loginAction', methods=['POST'])
def login():
	data = flask.request.form
	
	userDocument = db.users.find_one({'email' : data['email'], 'password' : data['password']})
	
	if userDocument is not None:
		flask.session['userId'] = str(userDocument['_id'])
	
		flask.flash("Logged in. Welcome!")
		return flask.redirect(flask.url_for('index'))
	else:
		flask.flash("Login info was incorrect.")
		return flask.redirect(flask.url_for('showLogin'))


@app.route('/logout')
def logout():
	flask.session.pop('userId', None)
	flask.session.pop('email', None)
	
	flask.flash("logged out")
	return flask.redirect(flask.url_for('index'))


# custom render_template function that also adds a boolean "isLoggedIn" to let template know whether user is logged in
def render_template(template, **kwargs):
	# decide if i'm logged in or not
	if 'userId' in flask.session:
		isLoggedIn = True
	else:
		isLoggedIn = False
	
	return flask.render_template(template, isLoggedIn=isLoggedIn, **kwargs)


##############################################################################
# REGISTRATION

@app.route('/register')
def showRegistration():
	return render_template('registration.html')

@app.route('/registerAction', methods=['POST'])
def register():
	data = flask.request.form
	
	# create the user's db entry; it returns an ObjectId we can use to log the user in
	userId = db.users.insert({
		'email' : data['email'],
		'name' : data['name'],
		'password' : data['password']
	})
	
	# log the user in by setting a variable in the session object
	# (i've decided to use the stringified ObjectId to identify the user everywhere, including in sessions & the front end)
	flask.session['userId'] = str(userId)
	
	flask.flash("""Welcome to Hotpot!""")
	return flask.redirect(flask.url_for('showEditProfileForm'))



##############################################################################
# USER ACCOUNT SETTINGS

@app.route('/accountinfo')
def showMyStuff():
	
	if 'userId' in flask.session:
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})

	return render_template('account.html')



##############################################################################
# USER PROFILE


def isFileExtensionAllowed(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/profile/<id>')
def showMyProfile(id):
	
	if id == "me":
		id = flask.session['userId']
		
	if id == flask.session['userId']:
		isMyProfile = True
	else:
		isMyProfile = False
	
	if 'userId' in flask.session:
		user = db.users.find_one({'_id' : ObjectId(id)})

	return render_template('profile.html', user=user, isMyProfile=isMyProfile)


@app.route('/editProfile')
def showEditProfileForm():
	
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	return render_template('editProfile.html', user=user)


@app.route('/saveProfile', methods=['POST'])
def updateMyProfile():
	
	# load incoming request data into some convenient variables
	data = flask.request.form
	userpic = flask.request.files['userpic']
	
	# get existing user data
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	# update form fields with new info
	db.users.update({'_id' : ObjectId(flask.session['userId'])}, {'$set' : { 'name' : data['name'] } })
	db.users.update({'_id' : ObjectId(flask.session['userId'])}, {'$set' : { 'location' : data['location'] } })
	
	# upload the userpic, if any
	if userpic and isFileExtensionAllowed(userpic.filename):
		# rename the file after the user's ID + a random number
		# random num is to prevent caching & displaying the old pic when uploading a new pic w/ same extension
		userpicFilename = str(user['_id']) + '_' + str(random.random()) + '.' + userpic.filename.rsplit('.', 1)[1]
		
		# delete older user pic, if it's around
		try:
			os.remove(os.path.join(USERPIC_FOLDER, user['userpic']))
			print "baleted"
		except:
			print "oh. i guess that file didn't exist after all. oh well."
		
		# save to the right folder on the server
		userpic.save(os.path.join(USERPIC_FOLDER, userpicFilename))
		
		# update database so we now know there's a picture for this user
		db.users.update({'_id' : ObjectId(flask.session['userId'])}, {'$set' : { 'userpic' : userpicFilename } })
		
	# retrieve updated user data
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	
	flask.flash("Changes saved.")
	return flask.redirect('/profile/me')
	
	
	
##############################################################################
# MENUS!

@app.route('/menus')
def showMenus():
	
	featuredMenu = db.recipes.find_one()
	menus = list(db.recipes.find())
	
	return render_template('menus.html', featured=featuredMenu, menus=menus)


@app.route('/menus/<slug>')
def showRecipe(slug):
	
	recipe = db.recipes.find_one({ 'slug' : slug })
	
	return render_template( 'recipe.html', recipe=recipe )


##############################################################################
# INVITATIONS

@app.route('/invite/<recipe>')
def showInviteForm(recipe):
	
	recipe = db.recipes.find_one({ 'slug' : recipe })
	
	if 'userId' not in flask.session:
		return flask.redirect('/login')
	else:
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
		return render_template('invite.html', recipe=recipe, user=user )


@app.route('/viewInvitation/<recipe>')
def sendEmail(recipe):
	recipe = db.recipes.find_one({ 'slug' : recipe })
	invitation = db.invitations.find_one();
	
	return render_template('email/invitation.html', recipe=recipe, invitation=invitation)
	

@app.route('/sendInvitation', methods=['POST'])
def sendInvitation():
	
	# put incoming values in a dictionary
	newInvitation = {}
	for key in ['to', 'from', 'message', 'recipe', 'datetime', 'friendName', 'fromName', 'readableTime', 'readableDate']:
		newInvitation[key] = flask.request.form[key]
	
	# store new invitation dictionary in database
	newInvitation['status'] = "new"
	newInvitation['datetime'] = int(newInvitation['datetime']) # convert from string to int
	db.invitations.insert(newInvitation)
	
	# retrieve recipe based on slug
	recipe = db.recipes.find_one({'slug' : newInvitation['recipe']})
	
	# compose email to send
	email = Message("Hotpot Invitation Test", recipients=[newInvitation['to']])
	email.html = render_template('email/invitation.html', recipe=recipe, invitation=newInvitation)
	mail.send(email)

	return render_template('email/invitation.html', recipe=recipe, invitation=newInvitation)


##############################################################################
# REPLY

@app.route('/reply/<id>')
def showReplyForm(id):
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	
	# does the respondant already have an account?
	respondant = db.users.find_one({ 'email' : invitation['to']})
	if respondant is None:
		return render_template('registration.html')
	
	# ok so that user has an account, but are they logged in?
	elif 'userId' not in flask.session:
		return render_template('login.html')
		
	# ok they are logged in, but somehow did they login as the right person?
	elif str(respondant['_id']) != flask.session['userId']:
		return """hmm... that invitation is for %s %s. <a href="/logout">logout</a> and try again.""" % (flask.session['userId'], str(respondant['_id']))
	
	# wait, check if the invitation has already been replied to
	elif 'reply' in invitation:
		return """you already replied to that. <a href="/invitations/%s">see your response here</a>""" % invitation['_id']
	
	# ok! looks like the user can actually respond to the invitation now.
	else:
		recipe = db.recipes.find_one({'slug' : invitation['recipe']})
		
		return render_template('reply.html', invitation=invitation, showLogin=showLogin, recipe=recipe)

@app.route('/sendReply', methods=['POST'])
def sendReply():
	data = flask.request.form
	
	invitation = db.invitations.find_one({'_id' : ObjectId(data['id'])})
	
	# compose and send email
	email = Message("Hotpot Invitation RSVP", recipients=[invitation['from']])
	email.html = render_template('email/replyToHost.html', reply=data)
	mail.send(email)
	
	# store reply in database
	reply = {
		"mainReply" : data['mainReply'],
		"message" : data['message'],
		"altTimes" : data['altTimes'],
		"altMeals" : data['altMeals']
	}
	
	db.invitations.update({ '_id' : ObjectId(data['id']) }, {'$set' : { 'reply' : reply }})
	
	return render_template('email/replyToHost.html', reply=data, invitation=invitation)


@app.route('/invitations')
def showInvitations():
	
	# grab email address of logged in user
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	invitations = list(db.invitations.find({'from' : user['email']}))
	
	print db.invitations.find_one({'from' : user['email']})
	
	return render_template('invitations.html', invitations=invitations)


@app.route('/invitations/<id>')
def showInvitation(id):
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	
	user = db.users.find_one({'email' : flask.session['email']})
	userInfoForTemplate = {
		'name' : user['name'],
		'email' : user['email']
	}
	
	return render_template('invitation.html', invitation=invitation, user=userInfoForTemplate)


##############################################################################
# ROOM

@app.route('/<recipe>/room/<roomId>')
def showRoom(recipe, roomId):
	# check to see if the person's logged in
	if 'userId' not in flask.session:
		return render_template('login.html') 
	else:
		room = db.rooms.find_one({'_id' : ObjectId(roomId)})
		recipe = db.recipes.find_one({'slug' : recipe})
		
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
				
				userInfo = db.users.find_one({'_id' : ObjectId(foodNote['userId'])})
				snippet['username'] = userInfo['name']
				snippet['_id'] = foodNote['_id']
				snippet['text'] = foodNote['text']
				
				snippetsToInsert.append(snippet)
			
			step['snippets'] = snippetsToInsert
		
		# grab all the badges too
		badges = list(db.badges.find())
			
		return render_template('room.html', recipe=recipe, userId=flask.session['userId'], roomId=roomId, badges=badges )


def postFoodnote():
	data = flask.request.json
	
	# put together the new user note to send to the database!
	newUserNote = {
		"user_id": flask.session['userId'],
		"recipe_id": ObjectId(data['recipe_id']),
		"snippet_id": ObjectId(data['snippet_id']),
		"text": data['text']
	}
	
	# now insert the data, and store the id
	newUserNoteId = userNotes.insert(newUserNote);
	
	# now put together some data to send back to the template...
	userInfo = db.users.find_one({ '_id' : ObjectId(flask.session['userId']) })
	
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
		userInfo = db.users.find_one({ '_id' : ObjectId(requestJSON['userId']) })
	
	# do different things depending on what the socket message says...
	if requestJSON['type'] == 'foodNote':
	
		# put together the new user note to store in the database!
		newFoodNote = {
			"userId": requestJSON['userId'],
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