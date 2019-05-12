import time
import calendar
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please enter "chicago" or "new_york_city" or "washington".')
    validinput = False
    city = ""
    while validinput == False:
        city = input("enter city").lower()
        if city == "chicago" or city == "new_york_city" or city == "washington":
            validinput = True
        else:
            print("Invalid command.")

    # TO DO: get user input for month (all, january, february, ... , june)
    print('Please enter "01" for January, "02" for February, etc. for the first 6 months, or "first 6 months" if you want all of the first 6 months.')
    month = ""
    validinput = False
    while validinput == False:
        month = input("enter month").lower()
        if month == "first 6 months" or month == "01" or month == "02" or month == "03" or month == "04" or month == "05" or month == "06":
            validinput = True
        else:
            print("Invalid command.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please enter "monday" or "tuesday" or "wednesday" or "thursday" or "friday" or "saturday" or "sunday" or "full week" if you want the every day of the week.')
    day = ""
    validinput = False
    while validinput == False:
        day = input("enter day").lower()
        if day == "full week" or day == "monday" or day == "tuesday" or day == "wednesday" or day == "thursday" or day == "friday" or day == "saturday" or day == "sunday":
            validinput = True
        else:
            print("Invalid command.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    hours = []
    months = []
    days = []
    df = pd.read_csv(city + ".csv", parse_dates = ['Start Time', 'End Time'], date_parser = pd.core.tools.datetimes.to_datetime)
    for index, row in df.iterrows():
        months.append(row["Start Time"].month)
        hours.append(row["Start Time"].hour)
        day_of_week = calendar.day_name[row["Start Time"].weekday()].lower()
        days.append(day_of_week)
    df['hour'] = hours
    df['month'] = months
    df['day'] = days
    query = ''
    if month != '*':
        query = query + "month=='{}'".format(month)
    if day != '*':
        if query != '':
            query = query + '&'
        query = query + "day=='{}'".format(day)
    if query != '':
        df = df.query(query)
    print(df)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode().values[0]
    print('The most common month people used the service was {}.'.format(calendar.month_abbr[most_common_month]))

    # TO DO: display the most common day of week
    most_common_weekday = df['day'].mode()
    print('The most common day of the week people used the service was {} (hour is in military time).'.format(most_common_weekday))

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()
    print('The most common start hour when people used the service was {}.'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_used_start_station = df['Start Station'].mode()
    print('The most commonly used start station is: \n{}'.format(most_used_start_station))

    # TO DO: display most commonly used end station
    most_used_end_station = df['End Station'].mode()
    print('The most commonly used end station is: \n{}'.format(most_used_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    combo_stations = df.groupby(['Start Station', 'End Station'])
    most_common_station_combo = {}
    number_of_combos = -1
    for name, group in combo_stations:
        if len(group.values) > number_of_combos:
            most_common_station_combo = name
            number_of_combos = len(group.values)

    print('The most frequent combination of start station and end station trip is {} with {} trips.'.format(most_common_station_combo, number_of_combos))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    trip_duration = df['Trip Duration'].agg(['sum'])
    trip_duration = trip_duration.values[0]
    total_travel_time = datetime.timedelta(seconds=int(trip_duration))
    print('The total travel time is: \n{}'.format(total_travel_time))

    # TO DO: display mean travel time
    trip_duration = df['Trip Duration'].agg(['mean'])
    trip_duration = trip_duration.values[0]
    average_travel_time = datetime.timedelta(seconds=int(trip_duration))
    print('The average travel time is: \n{}'.format(average_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df["User Type"].value_counts()
    print('The counts for user types are: \n{}'.format(user_type))


    # TO DO: Display counts of gender
    gender_type = None
    try:
        gender_type = df["Gender"].value_counts()
        print('The counts for each gender is: \n{}'.format(gender_type))
    except KeyError:
        print("Gender is not available for this city.")

    # TO DO: Display earliest, most recent, and most common year of birth
    birth_year_years = None
    birth_year_mode = None
    try:
        birth_year_years = df['Birth Year'].agg(['min', 'max'])
        birth_year_mode = df['Birth Year'].mode()
        print('The earliest year of birth and the most recent years of birth, respetively, are: \n{}'.format(birth_year_years))
        print('The most common year of birth is: \n{}'.format(birth_year_mode))
    except KeyError:
        print("Birth year is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        restart = input('\nWould you display stats? Enter yes or no.\n')
        if restart.lower() == 'yes':
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        view_data = input('\nWould you like to view the data? Enter yes or no.\n')
        if view_data.lower() == 'yes':
            index = 0
            while True:
                print(df[index:index+5])
                restart = input('\nWould you like to read 5 more rows? Enter yes or no.\n')
                if restart.lower() == 'yes':
                    index=index+5
                else:
                    break



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
