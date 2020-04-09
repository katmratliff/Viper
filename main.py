# Default template for XBee MicroPython projects

import urequests
import umqtt
import uftp
import remotemanager
import hdc1080
import ds1621
import socket
from machine import UART
import time
from machine import I2C
import usocket

# socket notes
'''
# Import the socket module.  
# This allows the creation/use of socket objects.
 
import usocket
# Create a TCP socket that can communicate over the internet.
socketObject = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
# Create a "request" string, which is how we "ask" the web server for data.
request = "GET /ks/test.html HTTP/1.1\r\nHost: www.micropython.org\r\n\r\n"
# Connect the socket object to the web server
socketObject.connect(("www.micropython.org", 80))
# Send the "GET" request to the MicroPython web server.  
# A "GET" request asks the server for the web page data.
bytessent = socketObject.send(request)
print("\r\nSent %d byte GET request to the web server." % bytessent)
 
print("Printing first 3 lines of server's response: \r\n")
# Single lines can be read from the socket, 
# useful for separating headers or
# reading other data line-by-line.
# Use the "readline" call to do this.  
# Calling it a few times will show the
# first few lines from the server's response.
socketObject.readline()
socketObject.readline()
socketObject.readline()
# The first 3 lines of the server's response 
# will be received and output to the terminal.
 
print("\nPrinting the remainder of the server's response: \n")
# Use a "standard" receive call, "recv", 
# to receive a specified number of
# bytes from the server, or as many bytes as are available.
# Receive and output the remainder of the page data.
socketObject.recv(512)
 
# Close the socket's current connection now that we are finished.
socketObject.close()
print("Socket closed.")
 

'''
# Set up HTTP COMMS with VIPER


'''VIPER - CAP via HTTPS - Notes:

----------------------------------------
HTTPS = HTTP over TLS/SSL
TLS - Transport Layer Security
 -rVIPER requires v1.2
HTTP Basic Auth
 -HTTP Authorization header
 -"Basic" scheme
 -base64-encoded bytes of "[username]:[password]"
 -e.g., "Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l"
Content-Length header required
 -size of message body (i.e. CAP XML), in bytes
CAP XML in request body'''
'''
POST /CAP/post HTTP/1.1
Host: viper.response.epa.gov
Authorization: Basic QWxhZGRpbjpPcGVuU2VzYW1l
Content-Length: 547
Connection: Keep-Alive

 Our Authentication: Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh

<?xml version="1.0" encoding="utf-16"?>
<alert xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
       xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>281005951_634498074648864996</identifier>
<sender>My Device</sender>
<sent>2011-08-19T15:31:08-04:00</sent>>
<source>Acme Particulate Monitor,APM S/N 123456,0,0</source>
<info>
  <headline>ConcRT;0.001;mg/m3;Green;ConcHr;0;mg/m3;Green;</headline>
  <area>
    <circle>38.904722, -77.016389 0</circle>
  </area>
</info>
</alert>

This ^^ is all the body
'''

uart = UART(1, 115200)
data = 0


def read_serial():
    host = "Placeholder"  # this will be the Viper URL
    if uart.any() > 0:
        post = uart.read(uart.any())
        http_post(host, post)
    time.sleep(5)


'''
HTTP example
FORMAT TO USE % s 'POST /CAP/post HTTP/1.1\r\nHost: %s\r\n\r\n' % host, 'utf16'
 
post = bytes('POST /CAP/post HTTP/1.1\r\nHost: viper.response.epa.gov\r\nAuthorization: '
                     'Basic Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh\r\nContent-Length: 547\r\nConnection: '
                     'Keep-Alive\r\n<?xml version="1.0" encoding="utf-16"?>
<alert xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
       xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>281005951_634498074648864996</identifier>
<sender>My Device</sender>
<sent>2011-08-19T15:31:08-04:00</sent>>
<source>Acme Particulate Monitor,APM S/N 123456,0,0</source>
<info>
  <headline>ConcRT;0.001;mg/m3;Green;ConcHr;0;mg/m3;Green;</headline>
  <area>
    <circle>38.904722, -77.016389 0</circle>
  </area>
</info>
</alert>\r\n', 'utf16')

<?xml version="1.0" encoding="utf-16"?>
<alert xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:xsd="http://www.w3.org/2001/XMLSchema"
       xmlns="urn:oasis:names:tc:emergency:cap:1.1">
<identifier>281005951_634498074648864996</identifier>
<sender>My Device</sender>
<sent>2011-08-19T15:31:08-04:00</sent>>
<source>Acme Particulate Monitor,APM S/N 123456,0,0</source>
<info>
  <headline>ConcRT;0.001;mg/m3;Green;ConcHr;0;mg/m3;Green;</headline>
  <area>
    <circle>38.904722, -77.016389 0</circle>
  </area>
</info>
</alert>
                     
'''


def http_post(host, body):
    s = socket.socket()
    try:
        s.connect((host, 443))
        # post = bytes('POST /CAP/post HTTP/1.1\r\nHost: viper.response.epa.gov\r\nAuthorization: '
        #             'Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh\r\nContent-Length: %s\r\nConnection: '
        #             'Keep-Alive\r\n\r\n', 'utf8')
        post = bytes(body)
        print("Requesting from host")
        s.send(post)
        while True:
            print(str(s.recv(500), 'utf8'), end='')
    finally:
        s.close()


def http_test():
    st = socket.socket()
    try:
        st.connect(("https://viper.response.epa.gov/CAP/post", 443))
        post = bytes('POST /CAP/post HTTP/1.1\r\nHost: viper.response.epa.gov\r\nAuthorization: '
                     'Basic Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh\r\nContent-Length: 547\r\nConnection: '
                     'Keep-Alive\r\n'
                     '<?xml version="1.0" encoding="utf-16"?>'
                     '<alert xmlns: xsi = "http://www.w3.org/2001/XMLSchema-instance"'
                     'xmlns: xsd = "http://www.w3.org/2001/XMLSchema"'
                     'xmlns = "urn:oasis:names:tc:emergency:cap:1.1">'
                     '<identifier> 281005951_634498074648864996 </identifier '
                     '<sender> EPA_WET_BOARD </sender>'
                     '<sent>2011-08-19T15:31:08-04:00</sent>>'
                     '<source>Acme Particulate Monitor,APM S/N 123456,0,0</source>'
                     '<info>'
                     '<headline> ConcRT;0.001;mg/m3;Green;ConcHr;0;mg/m3;Green;</headline>'
                     '<area>'
                     '<circle>38.904722, -77.016389 0</circle>'
                     '</area>'
                     '</info>'
                     '</alert>\r\n\r\n')
        st.send(post)
    finally:
        st.close()


def ssend():
    print("\n Starting Response \n")
    post = bytes('<?xml version="1.0" encoding="utf-8"?>\n'
                 '<alert xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
                 'xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n'
                 'xmlns="urn:oasis:names:tc:emergency:cap:1.1">\n'
                 '<identifier>281005951_634498074648864996</identifier>\n'
                 '<sender>EPA_WET_BOARD</sender>\n'
                 '<sent>2011-08-19T15:31:08-04:00</sent>\n'
                 '<source>Acme Particulate Monitor,APM S/N 123456,0,0</source>\n'
                 '<info>\n'
                 '<headline>ConcRT;0.001;mg/m3;Green;ConcHr;0;mg/m3;Green;</headline>\n'
                 '<area>\n'
                 '<circle>38.904722, -77.016389 0</circle>\n'
                 '</area>\n'
                 '</info>\n'
                 '</alert>\n', 'utf-8')
    socketObject = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    socketObject.connect(("remote.ertviper.org", 8038))
    print(" Sending \n")
    socketObject.send(post)
    print(socketObject.readline())

    print("Printing the remainder of the server's response: \n")
    # Use a "standard" receive call, "recv",
    # to receive a specified number of
    # bytes from the server, or as many bytes as are available.
    # Receive and output the remainder of the page data.
    socketObject.close()
    print("Socket closed.")

i2c = I2C(1, freq=400000)  # I2c Module


def i2c_read():
    global i2c
    data_i2c = i2c.readfrom(40, 4)
    data_i2c = int.from_bytes(data_i2c, byteorder='big')
    return data_i2c


while True:
    ssend()
    # http_test()
    time.sleep(500)
