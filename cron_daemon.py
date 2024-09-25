from datetime import datetime
import subprocess
import time

def run_command_on_schedule(schedule):
	now = datetime.now()
	[minute, hour, day, month, weekday] = [now.minute, now.hour, now.day, now.month, now.weekday()]
	checks = [minute in schedule['minute'], hour in schedule['hour'], day in schedule['day_of_month'], month in schedule['month'], weekday in schedule['day_of_week']]
	if all(checks):
		print(f'Executing command \'{schedule['COMMAND']}\' at {now}')
		subprocess.run([schedule['COMMAND']], shell=True)
	else:
		print('Not time to run command')

def run_daemon(schedule):
	while True:
		run_command_on_schedule(schedule)
		time.sleep(60)
	
def get_next_n_occurances(n, schedule):
	now = datetime.now()
	[minute, hour, day, month, weekday] = [now.minute, now.hour, now.day, now.month, now.weekday()]
	print(f'Current time: {now}')
	# 34, 40, 46, 52, 58, 04
	# 23-09-2024 00:45:00
	m = 0
	next_minute = None
	while schedule['minute'][m] <= len(schedule['minute']):
		if schedule['minute'][m] >= minute:
			next_minute = schedule['minute'][m]
			break
		m += 1
	else:
		next_minute = schedule['minute'][0]

	print(next_minute)
	