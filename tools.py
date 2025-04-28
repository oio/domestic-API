""" 
The set of tools accessible to the LLM in order to create better responses.
"""

import datetime

def now():
	"""
	Get the current date and time

	Args:
		None

	Returns:
		str: The current date and time in ISO format
	"""
	return datetime.datetime.now().isoformat()

def iso_to_datetime(iso_string):
	"""
	Convert an ISO formatted string to a datetime object

	Args:
		iso_string (str): The ISO formatted string to convert	

	Returns:
		datetime: The datetime object
	"""
	return datetime.datetime.fromisoformat(iso_string)

def datetime_to_iso(datetime_object):
	"""
	Convert a datetime object to an ISO formatted string

	Args:
		datetime_object (datetime): The datetime object to convert

	Returns:
		str: The ISO formatted string
	"""
	return datetime_object.isoformat()

