import sys

if sys.argv[1] == "LIVE":

	BASE_URL = 'http://letsgohotpot.com'
	LOCAL_URL = 'http://localhost:8888'
	PORT_NUMBER = 8888
	SOCKETS_PORT_NUMBER = 8889
	
elif sys.argv[1] == "TEST":
	
	BASE_URL = 'http://test.letsgohotpot.com'
	LOCAL_URL = 'http://localhost:7777'
	PORT_NUMBER = 7777
	SOCKETS_PORT_NUMBER = 7778