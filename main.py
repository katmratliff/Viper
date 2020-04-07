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
example
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


i2c = I2C(1, freq=400000)  # I2c Module


def i2c_read():
    global i2c
    data_i2c = i2c.readfrom(40, 4)
    data_i2c = int.from_bytes(data_i2c, byteorder='big')
    return data_i2c


while True:
    time.sleep(0.1)
