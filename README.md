# Cron Expression Parser

Steps to run the CLI tool:
1. In your Linux/Unix machine, clone and cd into the project directory.
1. Make sure you have python3 installed.
1. [Optional] Make the shebang at the top of script as per the path of python in your system and make the script executable.
`chmod +x main.py`, then you can run it as `./main.py <cron_string>`
1. Run the script with the cron string as 1st argument. Here are some of the examples:

- `python3 main.py '2 */3 2-30/4 * 0,2,4 find'`
- `python3 main.py '* */3 1 * 0,1 find'`
- `python3 main.py '*/15 0 1,15 * 1-5 /usr/bin/find'`

You'll see relevant errors when the cron string is invalid, such as when numbers are out of bound for a certain time field. Some assumptions that are made and are not handled in the error scenarios:
- All months have 30 days
- Command doesn't have spaces


# Changes to make
- implement cyclic order for ranges. Suppose if the days are supported as 2-5 and return 2,3,4,5 then if I give 5-2 that should yield me 5,6,7,1,2. 