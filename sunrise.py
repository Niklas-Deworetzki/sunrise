#! /usr/bin/env python3

from datetime import *
from astral import Location, AstralError

import argparse
import sys
import pytz


class ArgumentParser(argparse.ArgumentParser):
    """Custom argparse.ArgumentParser class exits with exit code 2 on usage errors and does not show help.
    """
    def error(self, message):
        self.exit(2, 'Error: %s\n' % message)

class ListTimezonesAction(argparse.Action):
    """Custom argparse.Action class to display timezones
    """
    def __call__(self, parser, namespace, filter, option_string=''):
        for tz in pytz.all_timezones:
            if filter in tz:
                print(tz)

        sys.exit(2) # Don't use the exit codes for Day and Night

def parse():
    """Parses the command line parameters and returns parse result.
    """
    parser = ArgumentParser(
        add_help=False,
        description='Calculate the sunrise and sunset times for any given day.',
        epilog='Unless a custom date is supplied, this programs exit code represents the state of the day-night-cycle. '
            + 'During day the exit code will be 0 and during night it will be 1.'
    )

    if parser._optionals is not None and parser._optionals.title is not None:
        parser._optionals.title = 'Program arguments:'

    parser.add_argument('--help', '-h', action='help',
        help='Shows this message and exits.')

    parser.add_argument('--latitude', '-lat', type=float, metavar='<deg>',
        help='Latitude in degrees.')
    parser.add_argument('--longitude', '-lon', type=float, metavar='<deg>',
        help='Longitude in degrees.')

    parser.add_argument('--elevation', '-e', type=float, default=0, metavar='<elevation>',
        help='Elevation in meters.')

    parser.add_argument('--date', '-d', metavar='<yyyy-mm-dd>', default=None,
        help='Optional parameter to calculate sunrise and sunset times for another date. '
            + 'If this parameter is omitted, the current date is used.')
    parser.add_argument('--offset', '-o', type=int, default=0, metavar='<min>',
        help='Optional parameter to shorten the duration of the day by changing the times of sunrise and sunset. '
            + 'If this parameter has a positive value, sunrise time is delayed by the given amount of minutes '
            + 'and sunset time is advanced by the same mount of minutes. '
            + 'Alternatively a negative value can be passed as this parameter to increase the duration of the day.')


    parser.add_argument('--state', '-s', action='store_true',
        help='When set, the program displays an additional line of output reading "Day" or "Night" depending on whether its daytime or nighttime. '
            + 'This flag can NOT be used when another date is passed.')
    parser.add_argument('--time', '-t', action='store_true',
        help='When set, the program will display the time in minutes left to the next event. '
            + 'The next event may be either "Sunrise" or "Sunset".')

    parser.add_argument('--timezone', metavar='<timezone>',
        help='Sets the timezone for which the time should be displayed. '
            + 'The timezone must be supplied as a string. '
            + 'If no timezone is given "Europe/Berlin" is used as a default.'
            + 'A complete list of possible values can be displayed by using the "list-timezones" parameter.')

    parser.add_argument('--list-timezones', metavar='<filter>', const='', nargs='?',
        action=ListTimezonesAction,
        help='Shows a list of all possible timezones and exits. '
            + 'You can pass a string to filter timezones for only those, which contain the filter-string.')


    return parser.parse_args()


def usageError(msg):
    """Displays give message to the user and exits the program 
    with an exit code of 2 representing an user error."""
    print(msg)
    sys.exit(2)

def isDay(time, sunrise, sunset, offset=0):
    """Returns True if its currently day according to this functions parameters.
    If the first parameter lies between sunrise and sunset its considered day.
    If the first parameter lies before sunrise or after sunset its considered night.
    An additional offset parameter may be supplied to delay the time of sunrise and
    advance the time of sunset.

    Parameters:
    time    - The datetime to check if its day or night
    sunrise - The datetime representing sunrise
    sunset  - The datetime representing sunset
    offset  - an optional integer to increase nights duration.
    """
    return (time - offset) >= sunrise and (time + offset) <= sunset

def validateTimezone(state, location):
    """Uses the parsed command line state and the astral Location
    to validate given timezone parameters.
    """
    location.timezone = 'Europe/Berlin'
    if state.timezone is not None:
        try:
            # Setting the timezone fails with an invalid timezone string.
            location.timezone = state.timezone
        except ValueError:
            print('Unable to set timezone "%s" (using default "%s")' % (state.timezone, location.timezone),
                file=sys.stderr)

def validateDate(state, location):
    """Uses the parsed command line state and the astral Location
    to validate given date parameters.
    """
    if state.date is None:
        state.date = datetime.now(location.tzinfo)
    else:
        if state.state: # Illegal combination of flags requested
            usageError('Illegal combination of "--date" and "--state".')

        parts = state.date.split('-')

        if not len(parts) is 3: # Date is not in format yyyy-mm-dd
            usageError('The date parameter should be supplied as YYYY-MM-DD.')

        try:
            state.date = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
        except ValueError as e:
            usageError('Error: ' + str(e))

def main():
    state = parse()
    if state.latitude is None or state.longitude is None:
        usageError('Error: the following arguments are required: --latitude, --longitude')

    location = Location()

    validateTimezone(state, location)
    validateDate(state, location)

    state.offset = timedelta(minutes=state.offset)

    location.latitude = state.latitude
    location.longitude = state.longitude
    location.elevation = state.elevation

    sun = location.sun()
    sunset = sun['sunset']
    sunrise = sun['sunrise']

    # Check if its currently day if possible
    day = isDay(state.date, sunrise, sunset, offset=state.offset) if state.date.tzinfo is not None else True

    if state.state: # Show current state
        print('Day' if day else 'Night')


    if not state.time: # Don't show relative times
        print(sunrise.strftime('Sunrise: %H:%M'))
        print(sunset.strftime('Sunset: %H:%M'))
    elif day:
        diff = sunset - state.date - state.offset
        if diff.total_seconds() < 0:
            diff += timedelta(minutes=24 * 60)
        print('Minutes till sunset: %02d' % (diff.total_seconds() // 60))
    else:
        diff = sunrise - state.date + state.offset
        if diff.total_seconds() < 0:
            diff += timedelta(minutes=24 * 60)
        print('Minutes till sunrise: %02d' % (diff.total_seconds() // 60))

    sys.exit(not day)


if __name__ == '__main__':
    main()
