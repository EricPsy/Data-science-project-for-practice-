#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago','new york city','washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    input_message_c = 'write the name of the city to analyze:'
    input_message_m = 'write the name of the month to filter:'
    input_message_d = 'write the name of the days to filter:'
    
    error_message_c = 'There is something wrong with inputs.Please choose cities from chicago, new york city or washington!'
    error_message_md = 'There is something wrong! Check your inputs and writhe again'
    
    def input_check(v_list, input_message, error_message):
        while True:
            v = input(input_message)
            if v.lower() not in v_list:
                print(error_message)
            else:
                break
        return v
    city = input_check(cities, input_message_c, error_message_c)
    month = input_check(months, input_message_m, error_message_md)
    day = input_check(days, input_message_d, error_message_md)
   

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1   # index(a): look for the index number of a in object months
        df = df[df['month'] == month]

    # filter by daye of week if applicable
    if day != 'all':
        df = df[df['day'] == day.title()]
    return df.dropna(axis=0)



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # TO DO: display the most common month
    most_month = df['month'].mode()[0]  #results was number, not the name of month
    print('The most traveled month was :', most_month)

    # TO DO: display the most common day of week
    most_day = df['day'].mode()[0]
    print('The most traveled day of week was :' , most_day) #result was the name

    # TO DO: display the most common start hour
    most_hour = df['hour'].mode()[0]
    print('The most traveled hour was :' , most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_ss = df['Start Station'].mode()[0]
    print('The most commonly used start station was :', popular_ss)

    # TO DO: display most commonly used end station
    popular_es = df['End Station'].mode()[0]
    print('The most commonly used end station was :', popular_es)

    # TO DO: display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " ---> " + df['End Station']
    popular_com = df['combination'].mode()[0]
    print('The most frequent combination of start station and end station trip was :', popular_com)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # duration's attritute is Timedelta
    df['duration'] = (df['End Time'] - df['Start Time'])/np.timedelta64(1,'s')
    #ps:或者用trip duration数据也可以
    mean_duration_min = df['duration'].mean() / 60
    sum_duration = df['duration'].sum() / 3600

    # TO DO: display mean travel time
    print('Mean travel time was %.1f minutes.' % mean_duration_min)
    print('Total travel time of our custom was %.1f hours.' % sum_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user type:\n',user_types)
    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('counts of gender:\n',user_gender)
        # TO DO: Display earliest, most recent, and most common year of birth
        max_year = df['Birth Year'].max()
        min_year = df['Birth Year'].min()
        most_year = df['Birth Year'].mode()[0]
        print('oldest custom born in %d' % min_year)   #smaller number was older
        print('youngest custom born in %d' % max_year)
        print('most common year of birth: %d' % most_year)
    except KeyError:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



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

#当文件作为模块导入时，不执行main()；当.py文件被直接执行时，运行main()
if __name__ == "__main__":
	main()
