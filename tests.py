from parse_cron import parse_cronstring
from exceptions import CronParseException

def test_happy_cron_case():
	cron = '*/15 0 1,7 * 1-5 /usr/bin/find'
	schedule = parse_cronstring(cron)
	assert schedule['minute'] == [0, 15, 30, 45]
	assert schedule['hour'] == [0]
	assert schedule['day_of_month'] == [1, 7]
	assert schedule['month'] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	assert schedule['day_of_week'] == [1, 2, 3, 4, 5]
	assert schedule['COMMAND'] == '/usr/bin/find'

def test_invalid_cron():
	cron = '*15 0 1,15 * 1-5 /usr/bin/find'
	try:
		schedule = parse_cronstring(cron)
	except CronParseException as e:
		assert str(e) == 'No match for time_field minute, cron: *15'
