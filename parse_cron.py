#!/opt/homebrew/bin/python3

'''
Usage: ./main.py '* * * * * /usr/bin/ls'
Assumptions:
- All months have 30 days
- Command doesn't have spaces
'''

from exceptions import CronParseException
import re
import schedule

ONLY_DIGITS_RE = re.compile(r'^\d{1,2}$')
ASTRICK_INTERVAL_RE = re.compile(r'\*\/\d{1,2}$')
RANGE_INTERVAL_RE = re.compile(r'^\d{1,2}\-\d{1,2}\/\d{1,2}$')
ONLY_RANGE_RE = re.compile(r'^\d{1,2}\-\d{1,2}$')
ASTRICK_RE = re.compile(r'^\*$')
COMMA_SEP_RE = re.compile(r'^(\d{1,2}\,)+\d{1,2}$')

TIME_FIELD_LIMIT = {
	'minute': [0,59],
	'hour': [0,23],
	'day_of_month': [1,30],
	'month': [1,12],
	'day_of_week': [0,6]
}

def get_schedule(cron_type, time_field, cron):

	schedule = []

	min_range = TIME_FIELD_LIMIT[time_field][0]
	max_range = TIME_FIELD_LIMIT[time_field][1]

	if cron_type == 'ONLY_DIGITS':
		num = int(cron)
		if num < min_range or num > max_range:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')
		schedule = [num]

	elif cron_type == 'ASTRICK_INTERVAL':
		interval = int(cron.split('/')[1])
		if interval > max_range:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')
		num = min_range
		while num <= max_range:
			schedule.append(num)
			num += interval

	elif cron_type == 'RANGE_INTERVAL':
		min_num = int(cron.split('-')[0])
		max_num = int(cron.split('-')[1].split('/')[0])
		interval = int(cron.split('/')[1])
		if min_num > max_num or min_num < min_range or max_num > max_range:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')
		num = min_num
		while num <= max_num:
			schedule.append(num)
			num += interval

	elif cron_type == 'ONLY_RANGE':
		min_num = int(cron.split('-')[0])
		max_num = int(cron.split('-')[1])
		if min_num > max_num or min_num < min_range or max_num > max_range:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')
		num = min_num
		while num <= max_num:
			schedule.append(num)
			num += 1

	elif cron_type == 'ASTRICK':
		num = min_range
		while num <= max_range:
			schedule.append(num)
			num += 1

	elif cron_type == 'COMMA_SEP':
		nums = list(map(int, cron.split(',')))
		if sorted(nums) != nums:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')

		min_num = nums[0]
		max_num = nums[-1]
		if min_num < min_range or max_num > max_range:
			raise ValueError(f'Invalid cron for {time_field}: {cron}')

		schedule += list(map(int, cron.split(',')))

	return schedule

def parse_cronstring(cronstring):
	cron_parts = list(map(lambda s: s.strip(), cronstring.split(' ')))

	# if len(cron_parts) != 6:
	# 	raise ValueError('Invalid cronstring')

	## TODO: compile once and use
	all_patterns = [ ONLY_DIGITS_RE, ASTRICK_INTERVAL_RE, RANGE_INTERVAL_RE, ONLY_RANGE_RE, ASTRICK_RE, COMMA_SEP_RE ]
	pattern_names = [ 'ONLY_DIGITS', 'ASTRICK_INTERVAL', 'RANGE_INTERVAL', 'ONLY_RANGE', 'ASTRICK', 'COMMA_SEP' ]

	time_fields = ['minute', 'hour', 'day_of_month', 'month', 'day_of_week']

	all_schedule = {}

	for time_field, cron in zip(time_fields, cron_parts[:5]):
		for pattern_name, pattern in zip(pattern_names, all_patterns):
			match = pattern.match(cron)
			if match:
				# print({'pattern': pattern, 'cron_type': pattern_name, 'cron': cron, 'time_field': time_field, 'match': match.group(), 'pattern_name': pattern_name})
				schedule = get_schedule(pattern_name, time_field, cron)
				all_schedule[time_field] = schedule
				break
		else:
			raise CronParseException(f'No match for time_field {time_field}, cron: {cron}')

		all_schedule['COMMAND'] = ' '.join(cron_parts[5:])

	return all_schedule

def print_schedule(schedule):
	for key, value in schedule.items():
		print(f'{key}\t{value}')
	


