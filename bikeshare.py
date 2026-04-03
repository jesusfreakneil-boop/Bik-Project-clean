import time
import pandas as pd
import os

# Mapping of city names to CSV files
CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day to filter by, or "all"
    """
    print("Hello! Let's explore some US bikeshare data!")

    # Get user input for city
    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid city. Please choose from Chicago, New York City, or Washington.")

    # Get user input for month
    while True:
        month = input("Enter month (January to June) or 'all': ").strip().lower()
        if month in MONTHS:
            break
        print("Invalid month. Please try again.")

    # Get user input for day of week
    
    while True:
        day = input("Enter day of week or 'all': ").strip().lower()
        if day in DAYS:
            break
        print("Invalid day. Please try again.")

    print('-' * 40)
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
    
    file_path = CITY_DATA[city]
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file for {city.title()} not found: {file_path}")

    df = pd.read_csv(file_path)

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays stats on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    print(f"Most common month: {df['month'].mode()[0]}")
    
    # display the most common day of week
    print(f"Most common day of week: {df['day_of_week'].mode()[0]}")
    
    # display the most common start hour
    print(f"Most common start hour: {df['Start Time'].dt.hour.mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def station_stats(df):
    """Displays stats on the most popular stations and trip."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    print(f"Most common start station: {df['Start Station'].mode()[0]}")
    
    # display most commonly used end station
    print(f"Most common end station: {df['End Station'].mode()[0]}")
    
    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    print(f"Most common trip: {df['trip'].mode()[0]}")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def trip_duration_stats(df):
    """Displays stats on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    print(f"Total travel time: {df['Trip Duration'].sum():,.0f} seconds")
    
    # display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean():.2f} seconds")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)


def user_stats(df):
    """Displays stats on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df.columns:
        print("Counts of user types:")
        print(df['User Type'].value_counts())
    else:
        print("User Type data not available.")

    # Display counts of gender
    if 'Gender' in df.columns:
        print("\nCounts of gender:")
        print(df['Gender'].value_counts())
    else:
        print("\nGender data not available.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print(f"\nEarliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
    else:
        print("\nBirth Year data not available.")

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    start_loc = 0
    while True:
        view_data = input("\nWould you like to see 5 rows of raw data? Enter yes or no: ").strip().lower()
        if view_data != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(df):
            print("\nNo more data to display.")
            break
            

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # New feature: display raw data
            display_raw_data(df)
            
            
            restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
            if restart != 'yes':
                print("Goodbye!")
                break
        except FileNotFoundError as e:
            print(e)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    main()