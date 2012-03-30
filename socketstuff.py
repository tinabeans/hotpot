# this program handles incoming socket connections (which are different from HTTP)
# it is the intervening layer between the socket.io javascript client (front end) and Flask, because Flask only handles HTTP requests

# there are 3 required handlers: on_open, on_message, and on_close.

import tornado.web
import tornado.ioloop
import tornado.websocket
import tornado.httpclient
import tornadio
import json

tornado.websocket.WebSocketHandler.allow_draft76 = lambda self:True

# keep tabs on all the client-side connections that exist so we can iterate through them later when sending out messages
# it will be a dictionary where the keys are roomIds, pointing to lists of sockets in that room
allTheSockets = {}

# the one required class for using socket
class SocketHandler(tornadio.SocketConnection):
	# runs when a new connection is opened by the client
	def on_open(self, request, **kwargs):
		print "allo from", self
	
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
		if messageJSON['type'] == 'socket connect':
			print "got socket connection message"
			roomId = messageJSON['roomId']
			
			# carry along the roomId so we know how which array to remove it from later, when disconnecting
			self.roomId = roomId
		
			if roomId in allTheSockets:
				allTheSockets[roomId].append(self)
			else:
				allTheSockets[roomId] = [self]
				
			print str(allTheSockets)
		
		else:
			# and now for handling all the other types of socket messages...
			
			# NOTES FOR A TINA:
			# tornado can make an http request! just like how AJAX does it. whoa, it's http turtles all the way down
			# here it acts like the client and makes a request to Flask the regular way, like through a browser window
			# and then on the Flask end, we set up an @route thingy to handle the request
			
			# have to create a request object. the body is just the data being sent from the front end as a socket message
			request = tornado.httpclient.HTTPRequest(url="http://localhost:7777/socketMessageHandler", method="POST", headers={'Content-Type':'application/json'}, body=message)
			
			# then actually execute the request
			# when the response comes back containing stuff Flask wants to send back out to the front-end,
			# call handle_response to actually do the sending (second argument is callback)
			httpClient.fetch(request, self.handle_response)
	
	def on_close(self):
		print "seeyah"
		
		try:
			# tidy up our handy list of currently open sockets...
			allTheSockets[self.roomId].remove(self)
		except:
			pass


# boilerplate stuff to get tornado up and running
application = tornado.web.Application([ tornadio.get_router(SocketHandler).route() ])
application.listen(7778) # this is the port i chose for tornado to talk to the client on
httpClient = tornado.httpclient.AsyncHTTPClient()

globalLoop = tornado.ioloop.IOLoop.instance()
globalLoop.start()