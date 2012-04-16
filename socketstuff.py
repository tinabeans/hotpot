############################################################################################
# WHAT'S GOING ON HERE?

# This file handles incoming socket connections (which are different from HTTP)
# It is the intervening layer between the socket.io javascript client (front end) and Flask, because Flask can't do sockets
# Also we're using it to initiate OpenTok sessions for each room and handle connections to them.
# Whew. I think I get that...

############################################################################################

# import tornado stuff
import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpclient
import tornadio

# opentok
from lib import OpenTokSDK

# utils
import json

# config variables, to make moving to production easier
import config


##############################################################################
# SETUP AND VARS AND STUFF

# keep tabs on all the client-side connections that exist so we can iterate through them later when sending out messages
# it will be a dictionary where the keys are roomIds, pointing to lists of sockets in that room
allTheSockets = {}

# ditto for openTok sessions
openTokSessions = {}

# OpenTok setup
opentok_sdk = OpenTokSDK.OpenTokSDK(config.api_key, config.api_secret)

# no comment.
tornado.websocket.WebSocketHandler.allow_draft76 = lambda self:True



##############################################################################
# LET'S HANDLE SOME SOCKET STUFF! YAY!

# the one required class for using sockets with Tornadio (note the i)
# there are 3 required handlers: on_open, on_message, and on_close.

class SocketHandler(tornadio.SocketConnection):
	# runs when a new connection is opened by the client
	def on_open(self, request, **kwargs):
		print "new socket connection from", self
	
	# called inside on_message, sends message back to the front-end(s) which will then decide what to do with it
	def handle_response(self, response):
	
		# in case Tornado is rebooted and the front end attempts to reconnect, it will throw an error
		# because self doesn't have a roomId anymore (the front end only sends it once)
		# so we prevent an error by putting it in a try/except thingy
		try:
			for socket in allTheSockets[self.roomId]:
				print "socket to send a message to: " + str(socket)
				socket.send(response.body)
		except:
			pass

	# called when a client sends a message
	def on_message(self, message):
		print "got message from front end: " + message
		
		# nice to have
		if type(message) is unicode:
			message = message.encode('utf-8')
		
		# JSONify the message so we can work with it... 'coz it's a string
		messageJSON = json.loads(message)
		
		# only one type of message is processed here; the rest is processed Flask via an HTTP request below
		# this is needed to remember which connections go with which cooking rooms,
		# so messages don't get sent back out to the wrong rooms
		if messageJSON['type'] == "Here I am!":
			print "someone is in the room!"
			roomId = messageJSON['roomId']
			
			# carry along the roomId so we know how which array to remove it from later, when disconnecting
			self.roomId = roomId
			
			# if this is the first person in the room, then start an entry in allTheSockets to keep track of who is in this room
			if roomId not in allTheSockets:
				allTheSockets[roomId] = [self]
				
				# also create an openTok session for this room
				session_address = "74.66.13.93" # TODO: make this grab the IP of the connected user dynamically
				session_properties = {
					'p2p.preference' : "enabled"
				}
				openTokSessions[roomId] = opentok_sdk.create_session(session_address, session_properties)
				
			# otherwise add this person to the existing entry
			else:
				allTheSockets[roomId].append(self)
			
			# create an openTok token for this person and send it back to the front end
			token = opentok_sdk.generate_token(openTokSessions[roomId].session_id)
			
			dataToSendBack = {
				'type' : 'openTok token',
				'data' : {
					'token' : token,
					'sessionId' : openTokSessions[roomId].session_id
				}
			}
			self.send(json.dumps(dataToSendBack))
		
		else:
			# and now for handling all the other types of socket messages...
			
			# NOTES FOR A TINA:
			# tornado can make an http request! just like how AJAX does it. whoa, it's http turtles all the way down
			# here it acts like the client and makes a request to Flask the regular way, like through a browser window
			# and then on the Flask end, we set up an @route thingy to handle the request
			
			# have to create a request object. the body is just the data being sent from the front end as a socket message
			request = tornado.httpclient.HTTPRequest(url=config.LOCAL_URL + "/socketMessageHandler", method="POST", headers={'Content-Type':'application/json'}, body=message)
			
			# then actually execute the request
			# when the response comes back containing stuff Flask wants to send back out to the front-end,
			# call handle_response to actually do the sending (second argument is callback)
			httpClient.fetch(request, self.handle_response)
	
	def on_close(self):
		print "seeyah"
		
		try:
			# tidy up our handy list of currently open sockets...
			allTheSockets[self.roomId].remove(self)
			
			# if the last person just left, remove the room from our handy dictionary
			if len(allTheSockets[self.roomId]) == 0:
				allTheSockets.pop(self.roomId)
				
				# also close and remove openTok session for this room
				# TODO
		except:
			pass


# boilerplate stuff to get tornado up and running
application = tornado.web.Application([ tornadio.get_router(SocketHandler).route() ])
application.listen(config.SOCKETS_PORT_NUMBER) # this is the port i chose for tornado to talk to the client on
httpClient = tornado.httpclient.AsyncHTTPClient()

globalLoop = tornado.ioloop.IOLoop.instance()
globalLoop.start()