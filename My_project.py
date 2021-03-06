import time
import pandas as pd
import numpy as np

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to filter by? New York City, Chicago or Washington?\n").lower()
        if city not in ('chicago', 'new york city', 'washington'): # We use tuple because the elements are related to each other.
            print("\nPlease, Enter a valid Input from Choices in question.\n")
            continue
        else:
            break

        # get user input for month (all, january, february, ... , june)
    while True:
        month = input("\nDo you want to filter by a specific month? you can choose: January, February, March, April, May, June or choose 'all' if you do not have any preference?\n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("\nPlease, Enter a valid Input from Choices in question.\n")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nAnother filter by day if you want, you can chosse: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or choose 'all' if you do not have any preference?\n").lower()
        if day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print("\nPlease, Enter a valid Input from Choices in question.\n")
            continue
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column dtype to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    
    # Create a new column for the month.
    df['month'] = df['Start Time'].dt.month
    
    
    # Create a new column for the day.
    df['Day'] = df['Start Time'].dt.day_name()
   

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month = df['month'].mode()[0]
    print("Most Popular Month: ", pop_month)

    # display the most common day of week
    pop_day = df['Day'].mode()[0]
    print("Most Popular Day: ", pop_day)

    # display the most common start hour
     # Create a new column for the hour.
    df['Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Hour'].mode()[0]
    print("Most Popular Hour: ", pop_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("Most frequent Start Station: ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("Most frequent End Station: ", end_station)
    # display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print("\nThe most frequent combination of trips are from {}.".format(combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total Travel Time: ', total_travel_time/86400, "in Days")

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Total Travel Time: ', mean_travel_time/60 ,'in Minutes')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('User Type Counts: ', user_types_count)

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('Gender Counts: ', gender_count)
    except KeyError:
        print('Gender_types: No data available for this month.')
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = df['Birth Year'].min()
        print('Earliest Year: ', earliest_year)
    except KeyError:
        print('Earliest Year: No data available for this month.')

    try:
      most_recent_year = df['Birth Year'].max()
      print('Most Recent Year:', most_recent_year)
    except KeyError:
      print("Most Recent Year:No data available for this month.")

    try:
      most_common_year = df['Birth Year'].mode()[0]
      print('Most Common Year:', most_common_year)
    except KeyError:
      print("Most Common Year:No data available for this month.")
      
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
	
def display_data(df):
    
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1    # use index values for rows

    print('\n Would you like to see some raw data from the current dataset?')
    while True:
        raw_data = input('      (y or n):  ')
        if raw_data.lower() == 'y':
            print('\n    Displaying rows {} to {}:'.format(rows_start + 1, rows_end + 1))

            print('\n', df.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print_line('.')
            print('\nWould you like to see the next {} rows?'.format(show_rows))
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
