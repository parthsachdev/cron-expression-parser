from exceptions import CronParseException
from parse_cron import parse_cronstring, print_schedule
from argparse import ArgumentParser
from cron_daemon import run_command_on_schedule, run_daemon, get_next_n_occurances

def main():
	parser = ArgumentParser()
	parser.add_argument('cronstring', type=str)
	cronstring = parser.parse_args().cronstring
	try:
		schedule = parse_cronstring(cronstring)
		# print_schedule(schedule)
		# run_command_on_schedule(schedule)
		# run_daemon(schedule)
		get_next_n_occurances(5, schedule)

	except CronParseException as err:
		print('Error: ', err)

if __name__ == '__main__':
	main()