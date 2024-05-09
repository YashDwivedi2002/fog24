# Complete project details at https://RandomNerdTutorials.com

from machine import Pin
from time import sleep
import dht 
import network
import urequests

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)  # create station interface
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.active(True)
        wlan.connect(ssid, password)  # connect to an AP
        while not wlan.isconnected():
            pass
    print('Connected to WiFi:', wlan.ifconfig())

def send_data_to_server(data, url = "http://192.168.171.252:8000/api/sensor"):
    headers = {'Content-Type': 'application/json'}
    try:
        response = urequests.post(url, json=data, headers=headers)
        print('Server response:', response.text)
    except Exception as e:
        print('Error sending data to server:', e)

# Replace 'your_wifi_ssid' and 'your_wifi_password' with your actual WiFi credentials
wifi_ssid = 'Yash'
wifi_password = 'Yash@124'
url = "http://192.168.171.252:8000/api/sensor"

connect_to_wifi(wifi_ssid, wifi_password)

sensor = dht.DHT22(Pin(14))
#sensor = dht.DHT11(Pin(14))

while True:
  try:
    sleep(10)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
    send_data_to_server({
      'sensor': 2,
      'temperature': temp ,
      'temperaturef':temp_f ,
      'humidity': hum ,
    })
  except OSError as e:
    print('Failed to read sensor.')

