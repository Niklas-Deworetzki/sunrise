# Sunrise - Python command line tool

Sunrise is a small command line tool written in Python.
Its task is to calculate sunrise and sunset times for any given position on earth and any given date.

## Getting started

Dependencies for this tool are managed via [Pipenv](https://github.com/pypa/pipenv), which is required for an easy install.

When using Pipenv, all you need to do for start using this tool, is clone the repository and install the dependencies via Pipenv.

```bash
git clone git@github.com:Niklas-Deworetzki/sunrise.git
cd sunrise
pipenv install
```

If you don't want to use Pipenv or can't use it, make sure to install the [Astral Python Library](https://pypi.org/project/astral/), which is the only dependency for this tool.

## Usage

The usage for this tool should be pretty straight forward.
All you have to do, is pass the latitude and longitude of your position as parameters.

```bash
./sunrise.py -lat 52.52437 -lon 13.41053
```

The output will be something like the following:

> Sunrise: 07:16
> Sunset: 16:24


### Improving accuracy

If you notice, that the times for sunrise and sunset are a little of from what you actually experience, it may help to pass your elevation to this tool.
Depending on how high you are above sea level, you might see mor of the sun before it goes below the horizon.
Consequently the duration of days increase with higher elevation.
An elevation is passed via the `--elevation` parameter (short `-e`) and might change the times you see by a few minutes.

Additionally you can specify an offset for sunrise and sunset times.
This is done via the `--offset` parameter (short `-o`), which accepts an integer.
The given offset is the time in minutes, the sunrise will be delayed and sunset will be advanced for internal calculations.

Specifiying an offset can be used to let other programs react to the output of this tool.
If this tool is for example used to control a light depending on the day and night cycle, it could be desired to switch the light on a few minutes before the sun actually passes the horizon.
In this case these minutes could be passed as a positive offset for this parameter.


### Pass other dates

Sometimes you might want to know sunrise and sunset times for another day than today.
This can be achieved by passing another date as parameter for this tool.
Dates are passed via the `--date` parameter (short `-d`) and have to be provided in the *yyyy-mm-dd* format


### Relative output times

By default this tool will output the absolute times for sunrise and sunset for the current day.
If you want to know, how long you have to wait for the sun to touch the horizon again, you can use the `--time` flag (short `-t`).
In this mode the minutes left to the next sunrise or sunset will be printed.

> Minutes till sunrise: 515

> Minutes till sunset: 83

Depending on whether its day- or nighttime it will print "sunrise" or "sunset" along with the time its away.

**Note:** You can't use this flag together with a custom date.
Since dates passed to this tool don't have a time attached to them, it would be impossible to say, whether its day or night at the specified date.


### Query the day-night-cycle

This tool can be asked to output whether its currently day- or nighttime.
It is considered *day* when the current time lies between the calculated times for *sunrise* and *sunset*.
In this case, an additional line stating "day" will be printed.
Otherwise this tool will output "night"

**Note:** You can't use this flag together with a custom date.
Since dates passed to this tool don't have a time attached to them, it would be impossible to say, whether its day or night at the specified date.


### Timezones

To output the local sunrise and sunset times, you may need to specify your local timezone.
This can be passed via the `--timezone` parameter.
Timezones are specified as a string.

To view a complete list of available timeszones, you can pass the `--list-timezones` flag to this program.
It will print out all available timezones (matching an optional filter) and halt the execution afterwards.


## Exit Codes

The exit code of this program can be used to determine whether its day- or nighttime.

|        Event       | Exit Code |
|:------------------:|:---------:|
| Daytime            |     0     |
| Nighttime          |     1     |
| Custom date\*      |     0     |
| Usage Error        |     2     |

\* Custom dates can be passed using the `--date` parameter.


