# IMPORT STUFF!!

# python standard libraries
import hashlib, random, json, os, time, urllib, threading, datetime, urllib2

# flask
import flask
from flaskext.mail import Mail, Message

# pymongo
import pymongo
from pymongo.objectid import ObjectId

# database fixture thing that yang told me to make
import saveStuff

# config variables, to make moving to production easier
import config

# opentok
from lib import OpenTokSDK


##############################################################################
# GLOBAL VARIABLES & CONFIG

USERPIC_FOLDER = 'static/uploads/userpics'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'gif'])

TESTER_CODE = "cooking is awesome"

# for sending cooking reminder emails
checkForReminderTimeInterval = 10 # 5min

emailSenderInfo = ("Hotpot", "hey@letsgohotpot.com")

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
db = connection[config.DB_NAME]


##############################################################################
# TEMPLATE RENDERING

# custom render_template function that also adds a boolean "isLoggedIn" to let template know whether user is logged in
def render_template(template, **kwargs):
	# decide if i'm logged in or not
	if 'userId' in flask.session:
		isLoggedIn = True
		
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
		userInfo = {
			'name' : user['name'],
			'userpic' : user['userpic'],
			'_id' : str(user['_id'])
		}
		
		if 'lastname' in user:
			userInfo['lastname'] = user['lastname']
			
		if 'location' in user:
			userInfo['location'] = user['location']
		
		# if user's logged in, also grab the # of new invites they have, if any
		newInvites = list(db.invitations.find({'inviteeIds' : flask.session['userId']}))
		
		alertNumber = len(newInvites)
		
		for invite in newInvites:
			if 'replies' in invite:
				for reply in invite['replies']:
					if reply['userId'] == flask.session['userId']:
						alertNumber = alertNumber-1
		
		return flask.render_template(template, isLoggedIn=isLoggedIn, user=userInfo, alertNumber=alertNumber, BASE_URL=config.BASE_URL, **kwargs)
	else:
		isLoggedIn = False
		return flask.render_template(template, isLoggedIn=isLoggedIn, BASE_URL=config.BASE_URL, **kwargs)

@app.template_filter()
def jsDatetimeLocaleFormat(tstamp, fmt, tzname=False):
	return """<script type="text/javascript">document.write(formatDatetimeLocale(%d, "%s") %s)</script>""" % (
		tstamp, fmt, ("""+ ' ' + TZ_NAME""" if tzname else '')
	)


def naiveLocalDatetimeForUser(tstamp, userInfo):
	return datetime.datetime.utcfromtimestamp(tstamp) - datetime.timedelta(minutes=userInfo.get('tzoffset', 0))


##############################################################################
# INTRO PAGE

@app.route('/')
def index():
	if 'userId' in flask.session:
		return flask.redirect(flask.url_for('home'))
		
	return render_template('index.html')
	

##############################################################################
# FAW PAGE

@app.route('/faq')
def faq():
		
	return render_template('faq.html')
	

##############################################################################
# LOGGED IN HOME

@app.route('/home')
def home():

	if 'userId' not in flask.session:
		return flask.redirect(flask.url_for('index'));
	
	newMeal = db.meals.find_one({'slug' : 'GarlicCuminVinaigretteEggplant'})
	
	# grab both the sent and received invitations that have been accepted
	invitations = grabAllInvitationsFor(flask.session['userId'])
	
	futureHotpots = filterUpcoming(invitations)
	
	# grab other info for upcoming Hotpots!
	for hotpot in futureHotpots:
		grabInvitationInfo(hotpot)
	
	return render_template('home.html', newMeal=newMeal, hotpots=futureHotpots)


##############################################################################
# PEOPLE PAGE

@app.route('/people')
def people():
	return render_template('people.html')


##############################################################################
# INVITE CODES


@app.route('/checkTesterCode', methods=['POST'])
def checkTesterCode():
	data = flask.request.form
	
	registrationFormHTML = flask.render_template('registrationForm.html')
	
	if data['code'] == TESTER_CODE:
		return registrationFormHTML
		
	else:
		return """wrong code"""


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
	
	print data
	
	userDocument = db.users.find_one({'email' : data['email'], 'password' : data['password']})
	
	print userDocument
	
	if userDocument is not None:
		print 'user found'
		# log the user in by setting a session variable
		flask.session['userId'] = str(userDocument['_id'])

		# get timezone info from form and store it in the database
		tzinfo = data.get('tzinfo', '').split()
		if len(tzinfo) and tzinfo[0].isdigit():
			userDocument['tzoffset'] = int(tzinfo[0])
			if len(tzinfo) == 2 and len(tzinfo[1]) == 3: # e.g. EST, PDT
				userDocument['tzname'] = tzinfo[1]
			db.users.save(userDocument)

		# redirect to the place you were gonna go... if there were such a place
		if 'redirectURL' in data:
			return flask.redirect(data['redirectURL'])
		# otherwise just drop them on their homepage
		else:
			flask.flash("Logged in. Welcome!")
			return flask.redirect(flask.url_for('home'))
	else:
		flask.flash("Login info was incorrect.")
		
		# return people to the page they tried to login from
		return flask.redirect(flask.request.referrer)
			


@app.route('/logout')
def logout():
	flask.session.pop('userId', None)
	flask.session.pop('email', None)
	
	flask.flash("logged out")
	return flask.redirect(flask.url_for('index'))


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
		'password' : data['password'],
		'userpic' : 'placeholder.png'
	})
	
	# log the user in by setting a variable in the session object
	# (i've decided to use the stringified ObjectId to identify the user everywhere, including in sessions & the front end)
	flask.session['userId'] = str(userId)
	
	flask.flash("welcome")
	return flask.redirect(flask.url_for('home'))


##############################################################################
# USER ACCOUNT SETTINGS

@app.route('/accountinfo')
def showMyStuff():
	
	if 'userId' in flask.session:
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})

	return render_template('account.html', userEmail=user['email'])


@app.route('/updateAccountInfo', methods=['POST'])
def updateAccountInfo():
	data = flask.request.form
	
	emailWasChanged = False
	passwordWasChanged = False
	
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	if data['email'] != user['email']:
		user['email'] = data['email']
		emailWasChanged = True
	
	if data['password'] != '':
		user['password'] = data['password']
		passwordWasChanged = True
	
	if emailWasChanged and passwordWasChanged:
		flask.flash('Email and password have been updated.')
	elif emailWasChanged:
		flask.flash('Email has been updated.')
	elif passwordWasChanged:
		flask.flash('Password has been updated.')
	else:
		flask.flash('No changes were made.')
	
	db.users.save(user);
	
	return flask.redirect(flask.url_for('showMyStuff'))
	


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

	return render_template('profile.html', isMyProfile=isMyProfile)


@app.route('/editProfile')
def showEditProfileForm():
	
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	return render_template('editProfile.html')


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
		
		print "got file and named it " + userpicFilename
		
		# delete older user pic, if it's around (only if its not the placeholder)
		if user['userpic'] != 'placeholder.png':
			try:
				os.remove(os.path.join(USERPIC_FOLDER, user['userpic']))
				print "baleted"
			except:
				print "oh. i guess that file didn't exist after all. oh well."
		
		# save to the right folder on the server
		userpic.save(os.path.join(USERPIC_FOLDER, userpicFilename))
		print "saved the file"
		
		# update database so we now know there's a picture for this user
		user['userpic'] = userpicFilename
		
	db.users.save(user)	
	
	flask.flash("Changes to your profile were saved.")
	return flask.redirect('/home')
	
	
	
##############################################################################
# MEALS!

@app.route('/meals')
def showMeals():
	
	featuredMeal = db.meals.find_one({'_id' : ObjectId('4f3352569685aa28d5000008')})
	meals = list(db.meals.find())
	
	return render_template('meals.html', featured=featuredMeal, meals=meals)


@app.route('/meals/<slug>')
def showMeal(slug):
	
	meal = db.meals.find_one({ 'slug' : slug })
	
	return render_template( 'meal.html', meal=meal )


##############################################################################
# CREATING A COOKING ROOM

@app.route('/createRoom')
def showCreateRoomForm():
	
	meals = list(db.meals.find())

	return render_template('createRoom.html', meals=meals);


##############################################################################
# INVITING SOMEONE TO COOK

@app.route('/invite')
def showBlankInviteForm():
	
	meal = flask.request.args.get('meal', 'LemonGarlicKalePasta')
	
	meals = list(db.meals.find())
	meal = db.meals.find_one({ 'slug' : meal })
	
	return render_template('invite.html', meals=meals, meal=meal)

# used by AJAX request when picking a recipe for the invitation
@app.route('/loadMealInformation')
def loadMealInformation():

	slug = flask.request.args.get('slug', '')
	
	meal = db.meals.find_one({'slug' : slug})
	
	mealInfo = {
		'title' : meal['title'],
		'shortDescription' : meal['shortDescription'],
		'ingredients' : meal['ingredients'],
		'slug' : meal['slug']
	}
	
	return json.dumps(mealInfo)

@app.route('/sendInvitation', methods=['POST'])
def sendInvitation():
	data = flask.request.form
	
	user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
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
		"message" : data['message'],
		"tzoffset": 300,
		"tzname": "EST"
	}
	# get timezone info from form and store it in the database
	tzinfo = data.get('tzinfo', '').split()
	if len(tzinfo) and tzinfo[0].isdigit():
		newInvitation['tzoffset'] = int(tzinfo[0])
		if len(tzinfo) == 2 and len(tzinfo[1]) == 3: # e.g. EST, PDT
			newInvitation['tzname'] = tzinfo[1]

	# insert into database
	db.invitations.insert(newInvitation)
	
	# add some extra info that's needed by the email template, but which we don't need stored in the database
	# NOTE: assuming for now there is only one friend! (even though the document has an array for 'friendIds')
	newInvitation['hostName'] = user['name']
	newInvitation['inviteeName'] = data['inviteeName']
	newInvitation['inviteeId'] = inviteeId
	
	# other stuff that's needed by the template
	meal = db.meals.find_one({'slug' : newInvitation['meal']})
	
	# compose email to send
	email = Message(user['name'] + " invites you to cook!", recipients=[data['inviteeEmail']], sender=emailSenderInfo)
	# TODO: if recipient has an account, translate to their TZ
	invitationMessage = render_template('email/invitation.html', meal=meal, invitation=newInvitation)
	email.html = invitationMessage
	mail.send(email)
	
	return render_template('inviteSent.html', invitationMessage=invitationMessage, invitation=newInvitation)


@app.route('/sendSimpleInvitation', methods=['POST'])
def sendInvitation():
	data = flask.request.form
	
	print data['message']
	
	invitation = {
		'message' : data['message'],
		'inviteeName' : data['inviteeName']
	}
	
	if 'yourName' in data:
		newUserInfo = {
			'name' : data['yourName'],
			'email' : data['yourEmail']
		}
		
		emailSenderInfo = (data['yourName'], data['yourEmail'])
	else:
		newUserInfo = {}
		user = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
		emailSenderInfo = (user['name'], user['email'])
		
	
	if data['meal'] != '':
		meal = db.meals.find_one({'slug' : data['meal']})
		
		mealInfo = {
			'title' : meal['title'],
			'shortDescription' : meal['shortDescription'],
			'slug' : meal['slug']
		}
	else:
		mealInfo = 'none'
	
	# compose email to send
	email = Message("Let's cook on Hotpot", recipients=[data['inviteeEmail']], sender=emailSenderInfo)
	# TODO: if recipient has an account, translate to their TZ
	invitationMessage = render_template('email/invitationSimple.html', meal=mealInfo, invitation=invitation)
	email.html = invitationMessage
	mail.send(email)
	
	return render_template('inviteSimpleSent.html', invitationMessage=invitationMessage, invitation=invitation, newUserInfo=newUserInfo)


##############################################################################
# REPLYING TO AN INVITATION

@app.route('/reply/<id>')
def showReplyForm(id):
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	inviteeId = flask.request.args.get('invitee', '')
	
	# first check if this person has already replied to this invite
	if 'replies' in invitation:
		loggedInName = ""
	
		for reply in invitation['replies']:
			if reply['userId'] == inviteeId:
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
	
	host = db.users.find_one({'_id' : ObjectId(invitation['hostId'])})
	hostInfo = {
		'name' : host['name'],
		'userpic' : host['userpic']
	}
			
	return render_template('reply.html', show=show, invitation=invitation, meal=meal, inviteeId=inviteeId, host=hostInfo, loggedInName=loggedInName)


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
		'password' : data['password'],
		'userpic' : 'placeholder.png'
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
		"message" : data['message']
	}
	
	# include extra info only if available
	if data['mainReply'] == "maybe":
		if data['altTimes'] != "":
			replyInfo["altTimes"] = data['altTimes']
		
		if data['altMeals'] != "":
			replyInfo["altMeals"] = data['altMeals']
	
	# if there aren't any replies stored yet, make an array to store them!
	if 'replies' not in invitation:
		# print 'no replies yet'
		invitation['replies'] = []
		
		invitation['replies'].append(replyInfo)
	
	# else, there are replies! so check if there already is one from this user for this invitation
	# TODO: there is a little inconsistency here... when accessing the RSVP form,
	# it won't let you reply if you already did,
	# but the code below also handles the case in which you overwrite an existing reply.
	# ...must fix someday..........
	
	else:
		replyFoundAt = -1
		
		# search for invitee's own reply, if it exists
		for (index, reply) in enumerate(invitation['replies']):
			if reply['userId'] == flask.session['userId']:
				replyFoundAt = index
		
		# this means invitee's own reply was found
		# in that case, instead of creating a new entry, we should overwrite it
		if replyFoundAt != -1:
			# overwriting reply
			invitation['replies'][replyFoundAt] = replyInfo
		else:
			# appending reply
			invitation['replies'].append(replyInfo)
	
	# set status of invitation
	# TODO: this logic needs to be fixed major big time for multiple invitees,
	# because if a second person replies, it will just overwrite the status of the first person
	# Right now it works fine for just one invitee...
	if replyInfo['mainReply'] == "yes":
		invitation['status'] = "accepted"
		
		# also, set a flag in the database to indicate that the cooking's happening.
		# [insert Carrie voice: "It's HAPPENING!"
		invitation['itsHappening'] = True
		
	elif replyInfo['mainReply'] == 'maybe':
		invitation['status'] = 'changeNeeded'
		
	elif replyInfo['mainReply'] == 'no':
		invitation['status'] = 'declined'
	
	
	# store updated invitation entry back in database
	db.invitations.save(invitation)
	
	# grab host email address
	hostEmail = db.users.find_one({'_id' : ObjectId(invitation['hostId'])})['email']
	
	# grab invitee info
	invitee = db.users.find_one({'_id' : ObjectId(flask.session['userId'])})
	
	inviteeInfo = {
		'name' : invitee['name'],
		'userpic' : invitee['userpic'],
		'email' : invitee['email']
	}
	
	if 'lastname' in invitee:
		inviteeInfo['lastname'] = invitee['lastname']
	
	# grab meal info
	meal = db.meals.find_one({'slug' : invitation['meal']})
	
	mealInfo = {
		'_id' : str(meal['_id']),
		'title' : meal['title'],
		'ingredients' : meal['ingredients'],
		'slug' : meal['slug']
	}
	
	# grab invitation info
	invitationInfo = {
		'_id' : invitation['_id'],
		'readableDate' : invitation['readableDate'],
		'readableTime' : invitation['readableTime']
	}
	
	# compose and send email back to host
	# email = Message("Hotpot RSVP", recipients=[hostEmail], sender=emailSenderInfo)
	replyMessage = render_template('email/replyToHost.html', reply=replyInfo, invitee=inviteeInfo, invitation=invitationInfo, meal=mealInfo)
	#email.html = replyMessage
	#mail.send(email)
	
	host = db.users.find_one({'_id' : ObjectId(invitation['hostId'])})
		
	hostInfo = {
		'name' : host['name'],
		'userpic' : host['userpic']
	}
	
	# if reply was a yes...
	if replyInfo['mainReply'] == "yes":
		# also send the invitee a confirmation
		invitee = db.users.find_one({'_id' : ObjectId(replyInfo['userId'])})
		inviteeEmail = invitee['email']

		# calculate the cooking time in the invitee's locale
		localDt = naiveLocalDatetimeForUser(invitation['datetime'], invitee)

		# make a copy so we can modify it for the invitee
		confirmationInfo = dict(invitationInfo)
		confirmationInfo['readableDate'] = localDt.strftime("%A, %B %d, %Y")
		readableTime = localDt.strftime("%l:%M %p").strip()
		if invitee.get('tzname'):
			readableTime += ' ' + invitee['tzname']
		confirmationInfo['readableTime'] = readableTime

		email = Message("Hotpot RSVP Confirmation", recipients=[inviteeEmail], sender=emailSenderInfo)
		email.html = render_template('email/RSVPConfirmation.html', reply=replyInfo, host=hostInfo, invitation=invitationInfo, meal=mealInfo)
		mail.send(email)
		
		# check whether this invitation is for something happening on the same day.
		# if so, send out a "reminder" email for today (b/c the reminder emails contain the link to the room)
		currentTime = time.time();
		
		# TODO: this is a VERY naive implementation whereby we consider something 'same day' if it's less than 12 hrs from now
		# obviously this wouldn't make sense if we sent the invite at 9pm for 8am the next day...
		# but since i haven't figured out time zones yet, this will have to do for now.
		if invitation['datetime'] <= currentTime+43200:
			print "oh we're cooking on the same day? cool."
			if 'reminderSent' not in invitation:
				invitation['reminderSent'] = True
				db.invitations.save(invitation)
				
				print "calling send cooking reminder"
				
				# have to set a timer to make a request on a separate thread, or else we get a request timeout
				def sendCookingReminderAfterWaitingOneSecond():
					urllib2.urlopen(config.LOCAL_URL + '/sendCookingReminder?invitationId=' + str(invitation['_id']) + '&today=yes').read()
				timer = threading.Timer(1, sendCookingReminderAfterWaitingOneSecond)
				timer.start()
	
	return render_template('replySent.html', replyMessage=replyMessage, host=hostInfo, invitation=invitation)


##############################################################################
# VIEWING INVITATIONS

def grabMealInfo(slug):
	meal = db.meals.find_one({'slug' : slug})
	mealInfo = {
		'title' : meal['title'],
		'slug' : meal['slug']
	}
	
	return mealInfo



def grabUserInfo(inviteeId):
	
	if '@' not in inviteeId:
		invitee = db.users.find_one({'_id' : ObjectId(inviteeId)})
	
		inviteeInfo = {
			'name' : invitee['name'],
			'_id' : str(invitee['_id'])
		}
		
		if 'userpic' in invitee:
			inviteeInfo['userpic'] = invitee['userpic']
		else:
			inviteeInfo['userpic'] = 'placeholder.png'
	# for people who were not actually signed up yet
	else:
		inviteeInfo = {
			'name' : inviteeId,
			'_id' : None,
			'userpic' : 'placeholder.png'
		}
		
	return inviteeInfo


	
def grabInvitationInfo(invitation):
	# start a new blank array to hold invitee details
	invitation['inviteesInfo'] = []
	
	for inviteeId in invitation['inviteeIds']:
		# skip if inviteeId is blank
		if inviteeId == "":
			continue
		
		inviteeInfo = grabUserInfo(inviteeId)
		invitation['inviteesInfo'].append(inviteeInfo)
		
	# no longer need the array of inviteeIds! 'coz we have better infos now :)
	invitation.pop('inviteeIds', None)
	
	# include host info for received invitations
	hostInfo = grabUserInfo(invitation['hostId'])
	invitation['host'] = hostInfo
	
	# get meal info
	invitation['meal'] = grabMealInfo(invitation['meal'])
	
	return invitation



def grabAllInvitationsFor(userId):
	
	return list(db.invitations.find({'hostId' : userId, 'itsHappening' : True })) + list(db.invitations.find({'inviteeIds' : userId, 'itsHappening' : True }))


def filterUpcoming(invitations):
	
	# filter out the ones that are in the past
	futureHotpots = []
	
	for invitation in invitations:
		if invitation['datetime'] >= time.time(): # current time
			futureHotpots.append(invitation)
		
	return futureHotpots
	
	

@app.route('/invitations/')
def showInvitations():

	if 'userId' not in flask.session:
		flask.flash('Log in to view invitations.')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/invitations/'}))
	
	# grab all the sent invitations
	invitationsSent = list(db.invitations.find({'hostId' : flask.session['userId']}))
	
	# add invitee and meal info for sent invitations
	for invitation in invitationsSent:
		grabInvitationInfo(invitation)
		
	# grab all the received invitations too
	invitationsReceived = list(db.invitations.find({'inviteeIds' : flask.session['userId']}))
	
	# add invitee and meal info for received invitations
	for invitation in invitationsReceived:
		grabInvitationInfo(invitation)
	
	# grab number of future hotpots
	numberOfUpcoming = len(filterUpcoming(invitationsSent)) + len(filterUpcoming(invitationsReceived))
	
	return render_template('invitations.html', invitationsSent=invitationsSent, invitationsReceived=invitationsReceived, numberOfUpcoming=numberOfUpcoming)


@app.route('/invitations/upcoming')
def showUpcoming():
	
	if 'userId' not in flask.session:
		flask.flash('Log in to view upcoming Hotpots.')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/invitations/upcoming'}))
		
	# grab both the sent and received invitations that have been accepted
	invitations = grabAllInvitationsFor(flask.session['userId'])
	
	futureHotpots = filterUpcoming(invitations)
	
	# grab other info for upcoming Hotpots!
	for hotpot in futureHotpots:
		grabInvitationInfo(hotpot)
	
	# get number of invitations sent and received
	numberOfInvitationsSent = len(list(db.invitations.find({'hostId' : flask.session['userId']})))
	numberOfInvitationsReceived = len(list(db.invitations.find({'inviteeIds' : flask.session['userId']})))
	
	return render_template('upcoming.html', hotpots=futureHotpots, numberOfInvitationsSent=numberOfInvitationsSent, numberOfInvitationsReceived=numberOfInvitationsReceived)


@app.route('/invitations/<id>')
def showInvitation(id):

	if 'userId' not in flask.session:
		flask.flash('Log in to view invitations.')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/invitations/' + id}))
	
	# TODO: check if this invite belongs to the person who's logged in
	
	invitation = db.invitations.find_one({'_id' : ObjectId(id)})
	
	invitation = grabInvitationInfo(invitation)
	
	# reorganize the invitation dict so that it's easier for the template to display who's replied and who hasn't
	for invitee in invitation['inviteesInfo']:
		try:
			for reply in invitation['replies']:
				if invitee['_id'] == reply['userId']:
					invitee['reply'] = reply
			invitation.pop('replies', None)
		except:
			"oh dang. guess nobody replied yet."
	
	# get number of invitations sent and received
	numberOfInvitationsSent = len(list(db.invitations.find({'hostId' : flask.session['userId']})))
	numberOfInvitationsReceived = len(list(db.invitations.find({'inviteeIds' : flask.session['userId']})))
	
	# determine whether this was sent or received by the currently logged-in user
	if invitation['host']['_id'] == flask.session['userId']:
		invitationType = "sent"
	else:
		invitationType = "received"
	
	return render_template('invitation.html', invitation=invitation, numberOfInvitationsSent=numberOfInvitationsSent, numberOfInvitationsReceived=numberOfInvitationsReceived, invitationType=invitationType)
	


##############################################################################
# SENDING A COOKING REMINDER

# check at short intervals whether it's time to send out reminder emails yet
def checkWhetherItsTimeToSendOutReminderEmails():

	print "checking whether it's time to send out reminder emails"

	# loop through all invitations that are happening
	for invitation in db.invitations.find({'itsHappening' : True}):
		invitationUpdated = False

		if not invitation.get('hostReminderSent'):
			if checkReminderSentForUser(invitation, invitation['hostId']):
				invitation['hostReminderSent'] = True
				invitationUpdated = True

		for attendee in invitation['replies']:
			if attendee['mainReply'] == 'yes' and not attendee.get('reminderSent'):
				if checkReminderSentForUser(invitation, attendee['userId']):
					attendee['reminderSent'] = True
					invitationUpdated = True

		if invitationUpdated:
			db.invitations.save(invitation)

	# repeat
	timer = threading.Timer(checkForReminderTimeInterval, checkWhetherItsTimeToSendOutReminderEmails)
	timer.daemon = True
	timer.start()


def checkReminderSentForUser(invitation, userId):
	"""Checks whether a user should've been reminder-emailed about an invitation,
	   and if so, make an HTTP request to send that email. This works for both
	   hosts and invitees. Returns True if an email was sent.
	"""
	userInfo = db.users.find_one({'_id': ObjectId(userId)})

	dt = naiveLocalDatetimeForUser(invitation['datetime'], userInfo)
	hoursBefore = 18 + dt.hour
	if dt.hour < 4: # count 12am-4am as previous day
		hoursBefore += 24
	secondsBefore = (hoursBefore * 60 + dt.minute) * 60

	timeRemaining = invitation['datetime'] - time.time()
	if timeRemaining < secondsBefore:
		query = urllib.urlencode({'invitationId': invitation['_id'], 'userId': userId,
		                          'isToday': ('yes' if timeRemaining < 86000 else 'no')})
		def sendRequestToSendReminder():
			urllib2.urlopen(config.LOCAL_URL + '/sendCookingReminder?' + query).read()

		timer = threading.Timer(0.5, sendRequestToSendReminder)
		timer.start()
		return True


# called by checkForUpcomingCooking() above if the cooking is within the next 48 hours
@app.route('/sendCookingReminder')
def sendCookingReminder():
	print "sending cooking reminder"
	
	invitationId = flask.request.args.get('invitationId')
	userId = flask.request.args.get('userId')
	isToday = flask.request.args.get('isToday', 'no')

	if not invitationId:
		return "invitation not found"
	if not userId:
		return "user not found"
	
	invitation = db.invitations.find_one({'_id' : ObjectId(invitationId)})
	userInfo = db.users.find_one({'_id': ObjectId(userId)})
	
	localDt = naiveLocalDatetimeForUser(invitation['datetime'], userInfo)
	readableDate = localDt.strftime("%A, %B %d, %Y")
	readableTime = localDt.strftime("%l:%M %p").strip()
	if userInfo.get('tzname'):
		readableTime += ' ' + userInfo['tzname']

	invitation['readableDate'] = readableDate
	invitation['readableTime'] = readableTime

	# grab a list of all attendees
	attendeeIds = [invitation['hostId']] + [reply['userId'] for reply in invitation['replies']
	                                                        if reply['mainReply'] == 'yes']
	attendees = [db.users.find_one({'_id': ObjectId(aId)}) for aId in attendeeIds]
	
	# grab recipe ingredients to send along
	mealInfo = db.meals.find_one({'slug' : invitation['meal']})
	
	# compose and send email to the user
	email = Message("Get Ready to Cook!", recipients=[userInfo['email']], sender=emailSenderInfo)
		
	message = render_template('email/reminder.html', invitation=invitation, attendees=attendees, meal=mealInfo, recipient=userInfo, isToday=isToday)
	email.html = message
		
	print message
		
	mail.send(email)
	
	return "reminder email sent!"



##############################################################################
# HOTPOT ROOM


@app.route('/getready/<id>')
def showDressingRoom(id):
	
	# generate an opentok session and token to send to the user
	opentok_sdk = OpenTokSDK.OpenTokSDK(config.api_key, config.api_secret)
	session = opentok_sdk.create_session()
	token = opentok_sdk.generate_token(session.session_id)
	
	return render_template('dressingRoom.html', roomId=id, token=token, sessionId=session.session_id)

# takes a meal dictionary and inserts notes into the appropriate step
def insertNotesIntoSteps(meal, notes):
	
	for step in meal['steps']:
	
		notesToInsert = []
		currentStepId = step['id']
		
		# the for-loop below is for grabbing just the foodNotes related to this step
		for note in notes:
			
			if note['stepId'] != currentStepId:
				continue # this skips the rest of the stuff in the loop and starts the next iteration
			
			# get the note author's name from their id
			noteAuthor = db.users.find_one({'_id' : ObjectId(note['userId'])})
			
			# grab just the info we wamt to send to the template
			noteInfo = {
				'timestamp' : note['timestamp'],
				'type' : note['type'],
				'_id' : str(note['_id']),
				'content' : note['content'],
				'noteAuthor' : {
					'name' : noteAuthor['name'],
					'userpic' : noteAuthor['userpic']
				}
			}
			
			# if it's a stamp, add in some additional info...
			if note['type'] == 'stamp':
				stampInfo = db.stamps.find_one({'slug' : note['content']})
				
				noteInfo['content'] = {
					'stampName' : stampInfo['name'],
					'stampSlug' : stampInfo['slug']
				}
			
			notesToInsert.append(noteInfo)
			
		
		if len(notesToInsert) != 0:
			step['notes'] = notesToInsert
		
	return meal

@app.route('/rooms/<invitationId>')
def showRoom(invitationId):
	# if the user's not logged in, redirect them to the login page
	if 'userId' not in flask.session:
		flask.flash('Log in to start cooking!')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/rooms/' + invitationId}))
	
	# if logged in, then show the room
	else:
		
		# this is to prevent people from seeing a server error if for some reason the URL is wrong
		try:
			roomInfo = db.invitations.find_one({'_id' : ObjectId(invitationId)})
			assert roomInfo is not None
		except:
			return "room not found. oops. quick, go back before you get eaten by a grue!"
		
		# grab the meal info (for displaying recipe steps, etc.)
		meal = db.meals.find_one({'slug' : roomInfo['meal']})
		
		# grab all the notes related to this room
		notesInThisRoom = list(db.notes.find({'invitationId' : invitationId}))
		
		# ...and insert them into the recipe object at the appropriate step, one step at a time
		meal = insertNotesIntoSteps(meal, notesInThisRoom)
		if len(meal['title']) > 35:
			truncatedTitle = meal['title'][0:35]
			shortTitle = truncatedTitle[0:truncatedTitle.rfind(' ')] + '...'
			meal['shortTitle'] = shortTitle
		
		# truncate the meal name if it's too long
		
		# grab all the stamps too
		stamps = list(db.stamps.find())
		
		# grab info of all attendees
		attendees = []
		attendees.append(grabUserInfo(roomInfo['hostId']))
		
		for inviteeId in roomInfo['inviteeIds']:
			attendees.append(grabUserInfo(inviteeId))
		
		return render_template('room.html', meal=meal, invitationId=invitationId, stamps=stamps, attendees=attendees, socketsPortNumber=config.SOCKETS_PORT_NUMBER)


##############################################################################
# SOCKET.IO ENDPOINT for IN-ROOM COMMUNICATIONINGS

@app.route('/socketMessageHandler', methods=['POST'])
def doStuffWithStuffFromTornado():
	print flask.request.json

	requestJSON = flask.request.json
	data = requestJSON['data']
	
	userInfo = None
	
	# if message is coming from a user, get user database entry based on userId
	if 'userId' in requestJSON:
		userInfo = db.users.find_one({ '_id' : ObjectId(requestJSON['userId']) })
	
	# do different things depending on what the socket message says...
	if requestJSON['type'] == 'note':
		
		# put together the new user note to store in the database!
		newNote = {
			'type' : data['type'],
			"userId": requestJSON['userId'],
			"invitationId": data['invitationId'],
			"stepId": data['stepId'],
			"content": data['content'],
			"timestamp" : data['timestamp']
		}
		
		# insert the new note into the database, and store the id in a variable for use later
		newNoteId = db.notes.insert(newNote);
		
		# put together socket response containing info needed by the template...
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				'type' : data['type'],
				'stepId': data['stepId'],
				'noteId' : str(newNoteId),
				'content': data['content'],
				'timestamp' : data['timestamp'],
				'noteAuthor' : {
					'name' : userInfo['name'],
					'userpic' : userInfo['userpic']
				}
			}
		}
		
		# if it's a stamp, add in some additional info...
		if data['type'] == 'stamp':
			stampInfo = db.stamps.find_one({'slug' : data['content']})
		
			dataForResponse['data']['content'] = {
				'stampName' : stampInfo['name'],
				'stampSlug' : stampInfo['slug']
			}
		
		print dataForResponse
			
	
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
	# print requestJSON
	# print dataForResponse
	return json.dumps(dataForResponse)


##############################################################################
# COOKING HISTORY

@app.route('/history/')
def showHistory():

	if 'userId' not in flask.session:
		flask.flash('Log in to view history.')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/history/'}))
	
	# need to find all invitations where hostId or one of the inviteeIds matches the current logged-in user
	allHotpots = list(db.invitations.find({'hostId' : flask.session['userId'], 'itsHappening' : True})) + list(db.invitations.find({'inviteeIds' : flask.session['userId'], 'itsHappening' : True}))
	
	pastHotpots = []
	
	# loop through and find ones which occurred in the past
	for hotpot in allHotpots:
		if hotpot['datetime'] < time.time():
			pastHotpot = grabInvitationInfo(hotpot)
			pastHotpots.append(pastHotpot)
	
	# just send the ones from the past to the template
	return render_template('history.html', hotpots=pastHotpots)


@app.route('/history/<id>')
def showSingleHistory(id):
	
	if 'userId' not in flask.session:
		flask.flash('Log in to view history.')
		return flask.redirect('login?' + urllib.urlencode({'redirectURL' : '/history/' + id}))
		
	# TODO: check if this history belongs to the person who's logged in
	
	hotpot = grabInvitationInfo(db.invitations.find_one({'_id' : ObjectId(id)}))
	
	# grab meal info
	meal = db.meals.find_one({'slug' : hotpot['meal']['slug']})
	
	# grab notes related to this hotpot
	notes = list(db.notes.find({'invitationId' : str(hotpot['_id'])}))
	
	# stuff notes into the meals dict at the appropriate steps
	meal = insertNotesIntoSteps(meal, notes)
	
	return render_template('historySingle.html', hotpot=hotpot, meal=meal)


##############################################################################
# UTILS for a Tina

@app.route('/saveStuff')
def saveStuffFunction():
	saveStuff.start(db)
	return "database being populated. omgscary"
	

##############################################################################
# INITIALIZATIONINGS

@app.before_first_request
def initialize():
	# start checking for time to send out reminder emails a few moments after the server starts
	# the delay is to give the server some time to boot up..?
	print "initializing check function"
	timer = threading.Timer(5, checkWhetherItsTimeToSendOutReminderEmails)
	timer.daemon = True
	timer.start()

def sendFirstRequestToStartTheInitializationFunctionYeah():
	urllib2.urlopen(config.LOCAL_URL + '/').read()

if __name__ == '__main__':
	
	timer = threading.Timer(1, sendFirstRequestToStartTheInitializationFunctionYeah)
	timer.start()
	
	app.run(host='0.0.0.0', port=config.PORT_NUMBER, debug=True)
