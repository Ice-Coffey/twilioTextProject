import os
from twilio.rest import Client
import utils

#initialize logger
logger = utils.init_logger()


#sends a message from twilio api
#message is the message sent. 
#phone_to is the number the text is sent to, format: "+1555555555"
#phone_from are the number the text is sent from, format: "+1555555555"

def send_message(message, phone_to, phone_from):
	account_sid = os.environ['twilioID']
	auth_token = os.environ['twilioAuth']
	client = Client(account_sid, auth_token)
	message = client.messages.create(
	         body=message,
	         from_=phone_from,
	         to=phone_to
	     )


#message handling for when there is a delay.
#also logs result of sent message with information

def delayed(message, to_phone, from_phone, order_id):
	try:
		send_message(
			message,
			to_phone,
			from_phone
		)

		logger.info(
			utils.text_late_sent(
				order_id, 
				message, 
				to_phone
			)
		)

	except Exception as e:
		logger.error(
			utils.text_late_error(
				order_id,
				message, 
				to_phone, 
				e
			)
		)


#Logs result when message sent to phone successfully

def timely(order_id):
	logger.info(
		utils.text_on_time(
			order_id
		)
	)