# IMPORT STUFF!!

# python standard libraries
import hashlib, random, json, os, time, urllib

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
	redirectURL = flask.request.args.get('redirectURL', '')
	
	if redirectURL != '':
		return render_template('login.html', redirectURL=redirectURL)
	else:
		return render_template('login.html')


@app.route('/loginAction', methods=['POST'])
def login():
	data = flask.request.form
	
	userDocument = db.users.find_one({'email' : data['email'], 'password' : data['password']})
	
	if userDocument is not None:
		# log the user in by setting a session variable
		flask.session['userId'] = str(userDocument['_id'])
		
		# redirect to the place you were gonna go... if there were such a place
		if 'redirectURL' in data:
			return flask.redirect(data['redirectURL'])
		else:
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
	
	# check if email addr is already registered
	if db.users.find_one({'email' : data['email']}) is not None:
		flask.flash('Looks like that email address is already registered. Try logging in instead!')
		return flask.redirect('login')
	
	# create the user's db entry; it returns an ObjectId we can use to log the user in
	userId = db.users.insert({
		'name' : data['name'],
		'lastname' : data['lastname'],
		'email' : data['email'],
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
	user['name'] = data['name']
	user['lastname'] = data['lastname']
	user['location'] = data['location']
	
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
# MEALS!

@app.route('/meals')
def showMeals():
	
	featuredMeal = db.meals.find_one()
	meals = list(db.meals.find())
	
	return render_template('meals.html', featured=featuredMeal, meals=meals)


@app.route('/meals/<slug>')
def showMeal(slug):
	
	meal = db.meals.find_one({ 'slug' : slug })
	
	return render_template( 'meal.html', meal=meal )


##############################################################################
# INVITING SOMEONE TO COOK

@app.route('/invite/<meal>')
def showInviteForm(meal):
	
	meal = db.meals.find_one({ 'slug' : meal })
	
	if 'userId' not in flask.session:
		return flask.redirect('/login')
	else:
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
		return render_template('invite.html', meal=meal, user=user )
	

@app.route('/sendInvitation', methods=['POST'])
def sendInvitation():
	data = flask.request.form
	
	# look up whether invited friend already exists as a user
	invitee = db.users.find_one({'email' : data['inviteeEmail']})
	
	# if user exists, then use their ID code as identifier; otherwise use their name + email address
	# NOTE: throughout the system, lack of userId indicates that user is not registered
	if invitee is not None:
		inviteeId = str(invitee['_id'])
	else:
		inviteeId = data['inviteeEmail']
	
	# construct new invitation document based on incoming form data and info above
	newInvitation = {
		"status" : "new",
		"hostId" : flask.session['userId'],
		"inviteeIds" : [inviteeId], # this is an array!
		"datetime" : int(data['datetime']),
		"sendDate" : time.time(),
		"meal" : data['meal'],
		"readableTime": data['readableTime'],
		"readableDate": data['readableDate'],
		"message" : data['message']
	}
	
	# insert into database
	db.invitations.insert(newInvitation)
	
	# add some extra info that's needed by the email template, but which we don't need stored in the database
	# NOTE: assuming for now there is only one friend! (even though the document has an array for 'friendIds')
	newInvitation['hostName'] = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})['name']
	newInvitation['inviteeName'] = data['inviteeName']
	newInvitation['inviteeId'] = inviteeId
	
	# other stuff that's needed by the template
	meal = db.meals.find_one({'slug' : newInvitation['meal']})
	
	# compose email to send
	email = Message("Hotpot Invitation Test", recipients=[data['inviteeEmail']])
	email.html = render_template('email/invitation.html', meal=meal, invitation=newInvitation)
	mail.send(email)
	
	return render_template('email/invitation.html', meal=meal, invitation=newInvitation)


##############################################################################
# REPLYING TO AN INVITATION

@app.route('/reply/<id>')
def showReplyForm(id):
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	inviteeId = flask.request.args.get('invitee', '')
	
	# first check if this person has already replied to this invite
	if 'replies' in invitation:
		for reply in invitation['replies']:
			if reply['friendId'] == inviteeId:
				show = 'replied'
	
	# if person is not logged in, determine if they're an existing user or not
	elif 'userId' not in flask.session:
		loggedInName = ""
	
		# not an existing user based on their email address; prompt them to register OR login
		# (could be registered under different email address)
		if '@' in inviteeId:
			show = 'registration' # used by template to determine what to show
		else:
			flask.flash("""Please log in to reply.""")
			show = 'login'
		
		# TODO: still need to go through the checks below once person IS logged in, for max fool-proof-ness
		
	# if someone is logged in already, check if they are logged in as the right person
	else:
		loggedInName = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})['name']
	
		# same person, different email?
		if '@' in inviteeId:
			show = 'confirm'
		
		# oops, the person you logged in as doesn't match the intended invitee
		elif inviteeId != flask.session['userId']:
			show = 'wrongperson'
			
		else:
			show = 'reply'
		
	meal = db.meals.find_one({'slug' : invitation['meal']})
	hostName = db.users.find_one({'_id' : ObjectId(invitation['hostId'])})['name']
			
	return render_template('reply.html', show=show, invitation=invitation, meal=meal, inviteeId=inviteeId, hostName=hostName, loggedInName=loggedInName)


@app.route('/loginToReply', methods=['POST'])
def loginToReply():
	data = flask.request.form
	
	userDocument = db.users.find_one({'email' : data['email'], 'password' : data['password']})
	
	if userDocument is not None:
		flask.session['userId'] = str(userDocument['_id'])
		return flask.redirect('/reply/' + data['invitationId'] + '?invitee=' + data['inviteeId'])
	else:
		flask.flash("Login info was incorrect.")
		return flask.redirect('/reply/' + data['invitationId'] + '?invitee=' + data['inviteeId'])


@app.route('/logoutToReply')
def logoutToReply():
	invitationId = flask.request.args.get('invitationId', '')
	inviteeId = flask.request.args.get('inviteeId', '')
	
	# logout current person
	flask.session.pop('userId', None)
	
	return flask.redirect('/reply/' + invitationId + '?invitee=' + inviteeId)


@app.route('/continueToReply')
def continueToReply():
	invitationId = flask.request.args.get('invitationId', '')
	inviteeId = flask.request.args.get('inviteeId', '')
	
	# replace the email address in the database with this person's userId
	invitation = db.invitations.find_one({'_id' : ObjectId(invitationId)})
	
	for (index, invitee) in enumerate(invitation['inviteeIds']):
		if invitee == inviteeId:
			invitation['inviteeIds'][index] = flask.session['userId']
			
	db.invitations.save(invitation)
	
	return flask.redirect('/reply/' + invitationId + '?invitee=' + flask.session['userId'])
	

@app.route('/registerToReply', methods=['POST'])
def registerToReply():
	data = flask.request.form
	invitationId = data['invitationId']
	inviteeId = data['inviteeId']
	
	# create the user's db entry
	userId = db.users.insert({
		'email' : data['email'],
		'name' : data['name'],
		'password' : data['password']
	})
	
	# log the user in
	flask.session['userId'] = str(userId)
	
	# replace email addr in invitation db entry with newly created userId
	invitation = db.invitations.find_one({'_id' : ObjectId(invitationId)})
	
	for (index, invitee) in enumerate(invitation['inviteeIds']):
		if invitee == inviteeId:
			invitation['inviteeIds'][index] = flask.session['userId']
			
	db.invitations.save(invitation)
	
	
	return flask.redirect('/reply/' + invitationId + '?invitee=' + flask.session['userId'])

@app.route('/sendReply', methods=['POST'])
def sendReply():
	data = flask.request.form
	
	invitation = db.invitations.find_one({'_id' : ObjectId(data['id'])})
	
	# grab all the form data and stuff it into a dictionary
	replyInfo = {
		"userId" : flask.session['userId'],
		"mainReply" : data['mainReply'],
		"message" : data['message'],
		"altTimes" : data['altTimes'],
		"altMeals" : data['altMeals']
	}
	
	# if there aren't any replies stored yet, make an array to store them!
	if 'replies' not in invitation:
		invitation['replies'] = []
		
		invitation['replies'].append(replyInfo)
	
	# else, there are replies! so check if there already is one from this user for this invitation
	else:
		replyFoundAt = -1
	
		for (index, reply) in enumerate(invitation['reply']):
			if reply['userId'] == flask.session['userId']:
				replyFoundAt = index
		
		if replyFoundAt != -1:
			print 'overwriting reply'
			invitation['replies'][replyFoundAt] = replyInfo
		else:
			print 'appending reply'
			invitation['replies'].append(replyInfo)
	
	
	# store updated invitation entry back in database
	db.invitations.save(invitation)
	
	# grab host email address
	hostEmail = db.users.find_one({'_id' : ObjectId(invitation['hostId'])})['email']
	
	# grab invitee name
	inviteeName = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})['name']
	
	# compose and send email
	email = Message("Hotpot Invitation RSVP", recipients=[hostEmail])
	email.html = render_template('email/replyToHost.html', reply=replyInfo, inviteeName=inviteeName)
	mail.send(email)
	
	
	return render_template('email/replyToHost.html', reply=replyInfo, inviteeName=inviteeName)


##############################################################################
# VIEWING INVITATIONS

@app.route('/invitations')
def showInvitations():
	
	invitationsSent = list(db.invitations.find({'hostId' : flask.session['userId']}))
	
	# fetch and include full invitee info for template
	for invitation in invitationsSent:
		
		invitation['inviteesInfo'] = []
		
		for inviteeId in invitation['inviteeIds']:
			if '@' not in inviteeId:
				invitee = db.users.find_one({'_id' : ObjectId(inviteeId)})
			
				inviteeInfo = {
					'name' : invitee['name'],
					'_id' : str(invitee['_id'])
				}
				
				if 'userpic' in invitee:
					inviteeInfo['userpic'] = invitee['userpic']
			
			else:
				inviteeInfo = {
					'name' : inviteeId,
					'_id' : None
				}
			
			invitation['inviteesInfo'].append(inviteeInfo)
		
		invitation.pop('inviteeIds', None)
	
	# TODO: invitationsReceived = list(db.invitations.find({'hostId' : flask.session['userId']}))
	
	return render_template('invitations.html', invitations=invitationsSent)


@app.route('/invitations/<id>')
def showInvitation(id):
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	
	# fetch and include full invitee info for template	
	invitation['inviteesInfo'] = []
	
	for inviteeId in invitation['inviteeIds']:
		if '@' not in inviteeId:
			invitee = db.users.find_one({'_id' : ObjectId(inviteeId)})
		
			inviteeInfo = {
				'name' : invitee['name'],
				'_id' : str(invitee['_id'])
			}
			
			if 'userpic' in invitee:
				inviteeInfo['userpic'] = invitee['userpic']
		
		else:
			inviteeInfo = {
				'name' : inviteeId,
				'_id' : None
			}
		
		invitation['inviteesInfo'].append(inviteeInfo)
	
	invitation.pop('inviteeIds', None)
	
	return render_template('invitation.html', invitation=invitation)


##############################################################################
# HOTPOT ROOM

@app.route('/rooms/<inviteId>')
def showRoom(inviteId):
	# if the user's not logged in, redirect them to the login page
	if 'userId' not in flask.session:
		flask.flash('Log in to start cooking!')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/rooms/' + roomId}))
	
	# if logged in, then show the room
	else:
		
		# this is to prevent people from seeing a server error if for some reason the URL is wrong
		try:
			roomInfo = db.invitations.find_one({'_id' : ObjectId(inviteId)})
			assert roomInfo is not None
		except:
			return "room not found. oops. quick, go back before you get eaten by a grue!"
		
		# grab the meal info (for displaying recipe steps, etc.)
		meal = db.meals.find_one({'slug' : roomInfo['meal']})
		
		# grab all the foodNotes related to this room
		notesInThisRoom = list(db.notes.find({'inviteId' : inviteId}))
		
		# and insert them into the recipe object at the appropriate step
		for step in meal['steps']:
		
			notesToInsert = []
			currentStepId = step['id'];
			
			# the for-loop below is for grabbing just the foodNotes related to this step
			for note in notesInThisRoom:
				
				if note['stepId'] != currentStepId:
					continue # this skips the rest of the stuff in the loop and starts the next iteration
				
				noteAuthor = db.users.find_one({'_id' : ObjectId(note['userId'])})
				
				noteInfo = {
					'type' : note['type'],
					'_id' : str(note['_id']),
					'content' : note['content'],
					
				}
				noteInfo['type'] = 'note'
				
				
				snippet['username'] = userInfo['name']
				
				snippetsToInsert.append(snippet)
			
			step['snippets'] = snippetsToInsert
		
		# grab all the badges too
		badges = list(db.badges.find())
		
		return render_template('room.html', meal=meal, userId=flask.session['userId'], inviteId=inviteId, badges=badges )


def postFoodnote():
	data = flask.request.json
	
	# put together the new user note to send to the database!
	newUserNote = {
		"user_id": flask.session['userId'],
		"meal_id": ObjectId(data['meal_id']),
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
		
	elif requestJSON['type'] == 'change step':
		
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