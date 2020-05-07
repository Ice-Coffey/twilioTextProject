from geopy.distance import geodesic
from geopy.distance import great_circle 
import datetime
import argparse
import logging


#returns the logger string for a late order that was sent
def text_late_sent(order_id, message, phone):
	return '''Order number "{}" is scheduled to arrive late. 
				The following message "{}" was sent to the number "{}".
				'''.format(order_id, message, phone)


#returns the logger string for a late order that was not sent
def text_late_error(order_id, message, phone, error):
	return '''Order number "{}" is scheduled to arrive late. 
				The following message "{}" could NOT be sent to the number "{}" for the following reason:
				{}'''.format(order_id, message, phone, error)


#returns the logger string for an on time order
def text_on_time(order_id):
	return 'On time to order number "{}". No message sent.'.format(order_id)


#initializes the logger
def init_logger(filename='textLog.log'):
	logging.basicConfig(filename=filename,level=logging.INFO)
	return logging.getLogger()


"""parses command line arguments
pickup are pickup coordinates of the order. ie (57.00000,57.00000)
dropoff are dropoff coordinates of the client. ie (57.00000,57.00000)
time is local time in the format "month/day/year-time(timezone)" (ie 1/1/19-11:11:11(-0800))
speed is an int that is interpreted as km/h. ie, 60 is 60 km/h
fromphone is a phone number in the format "+CountrycodeAreacodeNumber" that you wish to send from (ie +15555555555)
tophone is a phone number in the format "+CountrycodeAreacodeNumber" that you wish to send to (ie +15555555555)
message is any string that you wish to send to the customer if late
orderid is the int that is tied to the order number"""

def process_args():
    parser = argparse.ArgumentParser(description="""
    This script is going to send text messages if there is a late delivery. 
    """)
    parser.add_argument("pickup", help="pickup coordinates")
    parser.add_argument("dropoff", help="dropoff coordinates")
    parser.add_argument("time", help="dropoff time")
    parser.add_argument("speed", help="expected average speed to location")
    parser.add_argument("fromphone", help="phone number the text comes from")
    parser.add_argument("tophone", help="phone number the text goes to")
    parser.add_argument("message", help="the message sent to the phone")
    parser.add_argument("orderid", help="the id of the order")

    args = parser.parse_args()

    PICKUP = str_to_tuple(args.pickup)
    DROPOFF = str_to_tuple(args.dropoff)
    TIME = str_to_datetime(args.time)
    SPEED = float(args.speed)
    FROMPHONE = args.fromphone
    TOPHONE = args.tophone
    MESSAGE = args.message
    ORDERID = args.orderid

    return {
        'PICKUP':PICKUP,
        'DROPOFF':DROPOFF,
        'TIME':TIME,
        'SPEED':SPEED,
        'FROMPHONE':FROMPHONE,
        'TOPHONE':TOPHONE,
        'MESSAGE':MESSAGE,
        'ORDERID':ORDERID
    }

#converts a string to datetime
def str_to_datetime(string, fmt='%m/%d/%y-%H:%M:%S(%z)'):
	return datetime.datetime.strptime(string, fmt)


#converts string in format "(object1,object2,...,objectn)" to tuple
def str_to_tuple(string):
	string = string.strip('(').strip(')')
	return tuple(string.split())


#calculates seconds since epoch
def time_since_epoch(dt):
	epoch = str_to_datetime('1/1/1970-00:00:00(-0000)', fmt='%m/%d/%Y-%H:%M:%S(%z)')
	return (dt - epoch).total_seconds()


#city_1 and city_2 are the coordinates of each
#sphere dictates whether we assume earth is a perfect sphere
def distance_between(city_1, city_2, sphere=False):
	if(sphere):
		return great_circle(city_1, city_2).km
	return geodesic(city_1, city_2).km

#calculates driving time in seconds
def drive_time(distance, speed):
	return distance/speed*3600

#determines if the driver will be late given delivery time, current time, and driving time
def late(delivery_datetime_utc, driving_time):
	expected_time = time_since_epoch(delivery_datetime_utc)
	current_time = time_since_epoch(datetime.datetime.now(tz=datetime.timezone.utc))
	actual_time = current_time+driving_time
	return actual_time > expected_time
