import flask
from lib import OpenTokSDK

# OpenTok setup
api_key = "6303111"
api_secret = "45b94b30d4f5554ad7445950c13e8d78e099e92e"
session_address = "68.175.75.213"

opentok_sdk = OpenTokSDK.OpenTokSDK(api_key, api_secret)

session_properties = {
	OpenTokSDK.SessionProperties.p2p_preference: "enabled"
}

session = opentok_sdk.create_session(session_address, session_properties)
token = opentok_sdk.generate_token(session.session_id)


#create a new Flask object
app = flask.Flask(__name__)


# used to pass OpenTok setup info to template
content = {
	'apiKey' : session.session_id,
	'sessionId' : session.session_id,
	'token' : token
}

@app.route('/p2ptest')
def p2pTest():
	return flask.render_template('_test_p2p.html', content=content)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777, debug=True)