import time
import pandas as pd
import numpy as np
from datetime import timedelta
from tabulate import tabulate

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

    # Get City from user to determine file to process
    city = None

    while city != 'None':
        city = input('Enter a city to analyze the data. (Chicago, New York City or Washington): ')
        city = city.lower()
        city = CITY_DATA.get(city)

        if city == None:
            print('\nNot a valid city. Please enter a valid city.\n')
        else:
            break

    #Get Month from user to determine Month filter

    while True:
        try:
            month = input('Enter a month to filter by or \'ALL\' to not filter any data. (Jan, Feb, Mar, Apr, May, Jun): ' )
            month = month.lower()
            months = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
            month = months.index(month)
            if month == 0:
                month = 'all'

            break
        #trap for keyboard interupt to exit program without processing data
        except KeyboardInterrupt:
            print('\n')
            raise SystemExit
        except:
            print('\nNot a valid month. Please enter a valid month.\n')

    #Get day of the week from user to determine Day filter
    day = None
    days = { 'all': 'all',
             'mon': 'Monday',
             'tue': 'Tuesday',
             'wed': 'Wednesday',
             'thu': 'Thursday',
             'fri': 'Friday',
             'sat': 'Saturday',
             'sun': 'Sunday'}

    while day != 'None':
        day = input('Enter the day of the week to filter or \'All\' to not filter any data. (Mon, Tue, Wed, Thu, Fri, Sat, Sun): ' )
        day = day.lower()
        day = days.get(day)

        if day == None:
            print('\nNot a valid day. Please enter a valid day.\n')
        else:
            break

    print('\nData File: {} - Month Filter: {} - Day Filter: {}'.format(city, month, day))

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
    # load data file into a dataframe
    df = pd.read_csv(city)

    # convert Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculate most common month and convert to a month name
    common_month_name = df['Start Time'].dt.month_name().mode()[0]
    print('Most common month:', common_month_name)

    # Calculate most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day:', common_day)

    # Calculate the most common hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print('Most common hour: ', common_hour)

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculate most common starting station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station:', common_start_station)

    # Calculate most common ending station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station:', common_end_station)

    # Calculate most frequent trip stations
    common_trip = (df['Start Station'] + ' and ' + df['End Station']).mode()[0]
    print('Most common trip stations:', common_trip)

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate total travel time
    total_travel_time = timedelta(seconds=int(df['Trip Duration'].sum()))
    print('Total travel time (Days, H:M:S):', total_travel_time)

    # Calculate average trip duration
    trip_average = int(df['Trip Duration'].mean())
    print('Average trip duration (H:M:S): {}'.format(timedelta(seconds=trip_average)))


    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculate counts for types of users
    count_type = df.groupby(['User Type'])['User Type'].count()
    print('\nTypes of user counts:', count_type)

    # Calculate counts for gender
    try:
        count_gender = df.groupby(['Gender'])['Gender'].count()
        print('\nGender counts:', count_gender)
    except KeyError:
        print('\nData not available for Gender.')

    # Calculate earliest, latest and most common birth year
    try:
        birth_early = int(df['Birth Year'].min())
        print('\nEarliest birth year:', birth_early)

        birth_recent = int(df['Birth Year'].max())
        print('Latest birth year:', birth_recent)

        birth_common = int(df['Birth Year'].mode()[0])
        print('Most common birth year:', birth_common)

    except KeyError:
        print('\nData not available for Birth Year.')

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def display_file(df):
    """Displays file."""
    """
    Displays raw data from the chosen file 5 lines at a time.

    Args:
        (str) city - name of the csv file to display the raw data
    """

    print('\nDisplay raw data...\n')
    start_time = time.time()

    # open file and display 5 records at a time
    i=5
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers="keys"))
        i+=5

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_file(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
