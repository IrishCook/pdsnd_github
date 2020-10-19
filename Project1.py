import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }
months = ['January', 'February', 'March', 'April', 'May', 'June']
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    Given_Inputs_OK=False

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while Given_Inputs_OK==False:
        city=input('Please, select a city out of Chicago, New York City and Washington: ').title()
        if city in ['Chicago', 'New York City', 'Washington']:
            Given_Inputs_OK=True
        else:
            print('Let\'s try this again. Incorrect inputs detected \n')

    Given_Inputs_OK=False
    # get user input for month (all, january, february, ... , june)
    while Given_Inputs_OK==False:
        month=input('Please, select a month (available data January to June). If you want data for all months, please give input "all": ').title()
        if month in months or month=='All':
            Given_Inputs_OK=True
        else:
            print('Let\'s try this again. Incorrect inputs detected \n')
    Given_Inputs_OK=False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while Given_Inputs_OK==False:
        day=input('Please, select a day. If you want data for all days, please give input "all": ').title()
        if day in days or day=='All':
            Given_Inputs_OK=True
        else:
            print('Let\'s try this again. Incorrect inputs detected \n')
    Given_Inputs_OK=False

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
    #Selecting the correct dataset file
    df = pd.read_csv(CITY_DATA[city])

    #Selecting the correct dates and setting up the dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    #filtering the DataFrame
    if month!='All':
        month = months.index(month) + 1
        df = df[df['month'] == month]
        print(df)
    if day!= 'All':
        df = df[df['day'] == day]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\n The most popular month in the selection was %s ." % months[df['month'].mode()[0]-1])

    # display the most common day of week
    print("\n The most popular day in the selection was %s ." % df['day'].mode()[0])

    # display the most common start hour
    print("\n The most popular hour in the selection was %s ." % df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\n The most popular start station in the selection was %s ." % df['Start Station'].mode()[0])

    # display most commonly used end station
    print("\n The most popular end station in the selection was %s ." % df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['trip']=df['Start Station'] + ' to ' + df['End Station']
    print("\n The most popular trip in the selection was %s ." % df['trip'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['travel time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    # display total travel time
    print("\n The total travel time in the selection was %s ." % df['travel time'].sum())

    # display mean travel time
    print("\n The mean travel time in the selection was %s ." % df['travel time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    
    Displays statistics on bikeshare users.
    Available gender and age data are not available for all cities. Exception handling required.
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\n The breakdown of the users in the selection was \n%s." % df['User Type'].value_counts())

    # Display counts of gender
    try:
        print("\n The users per gender in the selection were \n %s :Females \n %s :Males ." % (df[df['Gender'] == 'Female']['Gender'].value_counts(),df[df['Gender'] == 'Male']['Gender'].value_counts()))
    except:
        print('\n There is no Gender info in the dataset \n')

    # Display earliest, most recent, and most common year of birth
    try:
        print("\n The oldest users are from year: %s \n The youngest users are from year: %s \n The most common user birth year is: %s \n " % (int(df['Birth Year'].min()),int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0])))
    except:
        print('\n There is no Age info in the dataset \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays only 5 lines per user request"""
    
    view_display = input('\nWould you like to view 5 rows of individual trip data? Enter y for yes.\n')
    start=0
    while start!=len(df) and view_display=='y':
        try:
            print(df.iloc[start:start+4])
            start += 5
            view_display= input("Do you wish to continue?: ").lower()
        except:
            print(df.iloc[start:])
    return

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes if desired, otherwise press any key to exit.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
