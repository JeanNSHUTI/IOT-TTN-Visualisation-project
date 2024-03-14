import paho.mqtt.client as mqtt
import json
import csv
import DataProcessing

AppID="jss-test@ttn"
Password="NNSXS.R34EEF32IOVMYTQ4WFPAG7SQ6NBHWCP2M3YPQGI.IIWETZAFGU2C3HXO7AX6YJDU6IXAZY4JLYMUCKN3OB72A6VOWEZA"

prev_hum_resistance_arduino = prev_hum_resistance_nucleo = 0


def getDataFromPayload(payload):
    dateTime = payload['received_at']
    date = dateTime.split('T')[0] #Recupère la date
    time = dateTime.split('T')[1].split('.')[0][:5] #Récupère l'heure
    Data = payload['uplink_message']['decoded_payload']['payload'] #Récupère toutes les données
    Temperature = Data.split('T')[0]
    Vib = Data.split('T')[1].split('V')[0]
    Hum = Data.split('T')[1].split('V')[1].split('H')[0]
    Lum = Data.split('T')[1].split('V')[1].split('H')[1].split('L')[0]
    Device = payload['end_device_ids']['device_id']
    if (Device == "eui-a8610a323334650a"):
        Device = "Arduino"
        prev_hum_resistance_arduino = Hum
    else:
        Device = "Nucleo"
        prev_hum_resistance_nucleo = Hum
    return date,time,Device,Temperature,Lum,Hum,Vib


def writeLine(payload):
    date, time, device, temp, lum, hum, vib = getDataFromPayload(payload)
    if device == 'Arduino':
        with open('IOTArduinoData.csv','a', newline="") as fichiercsv:
            writer=csv.writer(fichiercsv)
            if int(hum) == 0:
                hum = prev_hum_resistance_arduino
            hum_resistance = DataProcessing.calculate_hum_resistance(hum)
            lum_percentage = DataProcessing.calculate_lum(lum)
            temp = DataProcessing.calculate_temperature(temp)
            writer.writerow([date,time,device,round(temp),DataProcessing.calculate_rh_value(temp,hum_resistance),vib,lum_percentage])
    else:
        with open('IOTNucleoData.csv','a', newline="") as fichiercsv:
            writer=csv.writer(fichiercsv)
            if int(hum) == 0:
                hum = prev_hum_resistance_nucleo
            hum_resistance = DataProcessing.calculate_hum_resistance(hum)
            lum_percentage = DataProcessing.calculate_lum(lum)
            temp = DataProcessing.calculate_temperature(temp)
            writer.writerow([date,time,device,round(temp),DataProcessing.calculate_rh_value(temp,hum_resistance),vib,lum_percentage])


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('v3/+/devices/+/up')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Receiving data")
    payload = json.loads(msg.payload.decode('utf-8'))
    #print(payload)
    #print(payload['uplink_message']['decoded_payload']['payload']) ##Récupere la temp
    writeLine(payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(AppID,Password)
 
client.connect('eu1.cloud.thethings.network', 1883, 60)

run = True
while run:
    client.loop()
