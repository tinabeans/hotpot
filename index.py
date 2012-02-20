# IMPORT STUFF!!

# python standard libraries
import hashlib, random, json

# nice 3rd party stuff
import flask
import pymongo
from pymongo.objectid import ObjectId

# used to put stuff in the db
import saveStuff

# creating new Flask instance
app = flask.Flask(__name__)

# really secret secret key! used for Flask sessions...
app.secret_key = '''nTi!"2Oq#j2WdnUsQziTn52y8xGfZl:"MH*H|`yVClNLA4UG'GIvq1qc%Gk}vu<'''

# open database connection!
connection = pymongo.Connection()
db = connection.hotpot

codes = db.inviteCodes
users = db.users
userNotes = db.userNotes
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
# ROOM

@app.route('/<recipe>/room/<id>')
def showRoom(recipe, id):
	# check to see if the person's logged in
	if 'email' not in flask.session:
		return flask.render_template('login.html') 
	else:
		room = db.rooms.find_one({'_id' : ObjectId(id)})
		print str(room)
		recipe = recipes.find_one({'slug' : recipe})
		
		for step in recipe['steps']:
			snippetsToInsert = []
			
			#so im looping through the steps, then im looping through the snippets in the steps, then if the snippet is a foodnote, query the database for a list of notes that match the snippet id, then loop through that to determine which ones are relevant to the users in the current room, and finally send that to the template
			
			for snippetId in step.get('snippets', []): # get is a magical fail-safe method for checking if a key exists!
				snippet = snippets.find_one({'_id' : snippetId })
				
				# also find snippet responses
				if (snippet['type'] == 'foodnote'):
					
					notes = []
					
					# iterate through all the notes for a particular snippet
					for userNote in userNotes.find({'snippet_id' : snippetId}):
						
						# match the notes against each user of the room
						for userEmail in room['users']:
							
							# if there's a match, then add that snippet to a dictionary
							if userNote['user_id'] == userEmail:
								notes.append({
									'text' : userNote['text'],
									'name' : users.find_one({'email' : userNote['user_id']})['name']
								})
								
					# saves dictionary to send to template
					snippet['notes'] = notes
				
				snippetsToInsert.append(snippet)
			
			step['snippets'] = snippetsToInsert
			
			print recipe
		
		return flask.render_template('room.html', recipe=recipe, user_id=flask.session['email'])


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
	
	if requestJSON['type'] == 'userNote':
	
		# put together the new user note to store in the database!
		newUserNote = {
			"user_id": requestJSON['userId'], # users are uniquely identified by their email
			"recipe_id": ObjectId(data['recipe_id']),
			"snippet_id": ObjectId(data['snippet_id']),
			"text": data['text']
		}
		
		# now insert the data, and store the id
		newUserNoteId = userNotes.insert(newUserNote);
		
		# now put together some data to send back to the template...
		dataForResponse = {
			'type' : requestJSON['type'],
			'data' : {
				"snippetId": data['snippet_id'],
				'noteId' : str(newUserNoteId),
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