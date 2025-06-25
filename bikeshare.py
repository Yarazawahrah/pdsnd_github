# Refactored by Yara Alzawahrah – June 2025
# Minor code improvements and documentation
import time
import pandas as pd
import numpy as np

# Fix: Use a non-interactive backend to avoid GUI errors
import matplotlib
matplotlib.use('Agg')  # This prevents the display error
import matplotlib.pyplot as plt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input("\nWhich city would you like to analyze? (Chicago, New York City, Washington)\n").strip().lower()
        if city in cities:
            break
        else:
            print("\nPlease enter a valid city name.")

    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'none']
        month = input("\nWhich month would you like to consider? (January, February, March, April, May, June)? Type 'None' for no month filter\n").strip().lower()
        if month in months:
            break
        else:
            print("\nPlease enter a valid month.")

    while True:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'none']
        day = input("\nWhich day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)? Type 'None' for no day filter\n").strip().lower()
        if day in days:
            break
        else:
            print("\nPlease enter a valid day.")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'none':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'none':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df, month, day):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if month == 'none':
        pop_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        pop_month = months[pop_month - 1]
        print("The most popular month is", pop_month)

    if day == 'none':
        pop_day = df['day_of_week'].mode()[0]
        print("The most popular day is", pop_day.title())

    df['Start Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Start Hour'].mode()[0]
    print("The most popular start hour is {}:00 hrs".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    pop_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(pop_start_station))

    pop_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(pop_end_station))

    df['combination'] = df['Start Station'] + " to " + df['End Station']
    pop_com = df['combination'].mode()[0]
    print("The most frequent combination of start and end station is {} ".format(pop_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour, minute, second))

    average_duration = round(df['Trip Duration'].mean())
    m, sec = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print("The average trip duration: {} hour(s) {} minute(s) {} second(s)".format(h, m, sec))
    else:
        print("The average trip duration: {} minute(s) {} second(s)".format(m, sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df, city):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_counts = df['User Type'].value_counts().to_dict()
    print("The user types are:\n", user_counts)

    if city in ['chicago', 'new york city']:
        gender_counts = df['Gender'].value_counts().to_dict()
        print("\nThe counts of each gender are:\n", gender_counts)

        earliest = int(df['Birth Year'].min())
        print("\nThe oldest user is born in the year", earliest)
        most_recent = int(df['Birth Year'].max())
        print("The youngest user is born in the year", most_recent)
        common = int(df['Birth Year'].mode()[0])
        print("Most users are born in the year", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def plot_popular_times(df, city):
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]

    plt.figure(figsize=(10, 6))
    plt.hist(df['hour'], bins=24, range=(0, 24), color='skyblue', edgecolor='black')
    plt.axvline(pop_hour, color='red', linestyle='dashed', linewidth=1)
    plt.title(f'Trips by Hour in {city.title()}')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Trips')
    plt.grid(True)

    # Save the figure to file instead of showing it
    filename = f'{city}_trips_by_hour.png'
    plt.savefig(filename)
    plt.close()
    print(f"\nPlot saved as '{filename}'. You can open it to view the trip distribution.")

    # Prompt to show raw data
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nDo you wish to view the raw data?")
        print("Accepted responses: yes or no")
        rdata = input().lower()
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("Input does not seem to match any of the accepted responses.")
            print("\nRestarting...\n")

    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
        if rdata == "yes":
            print(df[counter:counter + 5])
        elif rdata != "yes":
            break

    print('-' * 80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        plot_popular_times(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
    
