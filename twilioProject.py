import utils
import messages

"""main program, takes in command args in this order:
pickup coordinates of food
dropoff coordinates of food
dropoff time of food
average expected speed to destination in km/h
phone that late texts will be sent from
phone that late texts will be sent to
message sent to customer if the driver is late
id of the order

sends text if order will be late,
always logs the result"""

def main():
	args = utils.process_args()
	distance = utils.distance_between(args['PICKUP'], args['DROPOFF']) #in km
	time_take = utils.drive_time(distance,args['SPEED'])
	isLate = utils.late(args['TIME'], time_take)

	if(isLate):
		messages.delayed(
			args['MESSAGE'],
			args['TOPHONE'],
			args['FROMPHONE'],
			args['ORDERID']
		)

	else:
		messages.timely(args['ORDERID'])

if __name__ == '__main__':
	main()