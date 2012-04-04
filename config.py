import sys

api_key = "6303111"
api_secret = "45b94b30d4f5554ad7445950c13e8d78e099e92e"

if sys.argv[1] == "LIVE":

	BASE_URL = 'http://letsgohotpot.com'
	LOCAL_URL = 'http://localhost:8888'
	PORT_NUMBER = 8888
	SOCKETS_PORT_NUMBER = 8889
	DB_NAME = "hotpot_live"
	
elif sys.argv[1] == "TEST":
	
	BASE_URL = 'http://test.letsgohotpot.com'
	LOCAL_URL = 'http://localhost:7777'
	PORT_NUMBER = 7777
	SOCKETS_PORT_NUMBER = 7778
	DB_NAME = "hotpot"