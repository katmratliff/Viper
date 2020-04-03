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
data = 

def read_serial():
    if uart.any() > 0:
        read_text = uart.read(uart.any())
        # uart.write(bytearray(read_text))
    time.sleep(0.1)


'''

post = bytes('POST /CAP/post HTTP/1.1\r\nHost: viper.response.epa.gov\r\nAuthorization: '
                     'Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh\r\nContent-Length: 547\r\nConnection: '
                     'Keep-Alive\r\n\r\n', 'utf8')
                     FORMAT TO USE % s 'POST /CAP/post HTTP/1.1\r\nHost: %s\r\n\r\n' % host, 'utf16'
                     
'''


def http_post(url):
    scheme, _, host, path = url.split('/', 3)
    s = socket.socket()
    try:
        s.connect((host, 443))
        post = bytes('POST /CAP/post HTTP/1.1\r\nHost: viper.response.epa.gov\r\nAuthorization: '
                     'Y29sbGllci5qYW1lc0BlcGEuZ292OldldGJvYXJkdGVhbTEh\r\nContent-Length: %s\r\nConnection: '
                     'Keep-Alive\r\n\r\n', 'utf8')
        print("Requesting /%s from host %s\n" % (path, host))
        s.send(post)
        while True:
            print(str(s.recv(500), 'utf8'), end='')
    finally:
        s.close()


i2c = I2C(1, freq=400000)  # I2c Module


def i2c_read():
    global i2c
    data_i2c = i2c.readfrom(40, 4)
    data_i2c = int.from_bytes(data_i2c, byteorder='big')
    return data_i2c


while True:
    time.sleep(0.1)
