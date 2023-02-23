pip install pika requests paho-mqtt


#NWS Connection via AMQP
#all messages
python recieve_nws.py collection.#

#messages for tac_opmet_reports collection
python recieve_nws.py collection.tac_opmet_reports


#UKMO connection via MQTT
python recieve_ukmo.py
