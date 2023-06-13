import pandas as pd

cities = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv',
              'chicago_mini': 'chicago_mini.csv' }

#month series
months = pd.Series(['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december'], index=[1,2,3,4,5,6,7,8,9,10,11,12])

#weekday series
weekdays = pd.Series(['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'], index=[0,1,2,3,4,5,6])

# Yes or No possibilities array
yes = ['yes', 'y']   

def load_data(city, month, day):
    print("Input values: City:{}, Month:{}, Day:{}".format(city, month, day))

    # Load data file into a dataframe
    df = pd.read_csv("data/"+cities[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour_of_the_day'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':        
        #find index for month
        month = months[months == month].index[0]
    
        # Filter by month and create new data frame
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week and create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df
    
#df = load_data('chicago', 'march', 'friday')

# Main function
def main():

    print('Hello! This is an interactive user terminal. Please feel free to provide the input requested to explore US bikeshare data!')

    _continue = 'yes'
    while _continue.lower() in yes:
        # Get user input for city (chicago, new york city, washington)
        city_number = input("Enter city details(Numeric value 1-3): \n 1. Washington \n 2. New York City \n 3. Chicago \n 3. Sample \n")
        
        if city_number == "1":
            city = "washington"
        elif city_number == "2":
            city = "new york city"
        elif  city_number == "3":
            city = "chicago"
        elif  city_number == "4":
            city = "chicago_mini"
        else:
            print("Invalid input. Please enter a valid city number(1-3) and try again \n")
            continue
        
        # Get user input for month 1-12
        month_number = input("Enter month number(1-12): Any other values considered as 'All' months \n")
        
        if month_number.isdigit() and int(month_number) in months.index:
            month = months[int(month_number)]
        else:
            month = "all"

        # Get user input for day of week 0-6
        weekday_number = input("Enter week days(0-6): Any other values considered as 'Any' days \n")
        
        
        if weekday_number.isdigit() and int(weekday_number) in weekdays.index:
            week = weekdays[int(weekday_number)]
        else:
            week = "all"

        #print city, month and week
        print("City: {} \n Month: {} \n Week: {}".format(city.title(), month.title(), week.title()))
        

        # Load data
        df = load_data(city, month, week)

        # Validate empty data frame
        if df.empty:
            print("No data available for the selected filter. Please try again with different filter values\n")
            continue

        # 1. Display statistics on the most frequent times of travel
        time_stats(df)

        # 2. Display statistics on the most popular stations and trip
        station_stats(df)

        # 3. Display statistics on the total and average trip duration
        trip_duration_stats(df)

        # 4. Display statistics on bikeshare users
        user_stats(df, city)

        # 5. Display raw data
        display_data(df)

        _continue = input("Would you like to see details for another city? Enter Yes/Y or No/N\n")

        if _continue.lower() not in yes:
            print("Thank you for using the interactive user terminal. Pleae visit again!\n")
            break

def time_stats(df):
    print("Most common month: ", df['month'].mode()[0])
    print("Most common day of week: ", df['day_of_week'].mode()[0])
    print("Most common start hour: ", df['Start Time'].dt.hour.mode()[0])
    print("Most common start minute of the hour: ", df['Start Time'].dt.minute.mode()[0])

def station_stats(df):
    print("Most common start station: ", df['Start Station'].mode()[0])
    print("Most common end station: ", df['End Station'].mode()[0])
    print("Most common trip from start to end: ", (df['Start Station'] + " to " + df['End Station']).mode()[0])

def trip_duration_stats(df):
    print("Total travel time: ", df['Trip Duration'].sum())
    print("Average travel time: ", df['Trip Duration'].mean())

def user_stats(df, city):
    print("User type count: \n", df['User Type'].value_counts())
    if city != "washington":
        print("Count of each Gender: \n", df['Gender'].value_counts())
        #earliest, most recent, most common year of birth
        print("Earliest year of birth: ", df['Birth Year'].min())

def display_data(df):
    # local variables
    _display_raw_data = 'yes'

    pageNumber = 1
    pageSize = 5

    list_df = [df[i:i+pageSize] for i in range(0,df.shape[0],pageSize)]

    list_df_size = len(list_df)

    while _display_raw_data.lower() in yes:

        _start = (pageSize*pageNumber-pageSize)+1
        _end = pageSize*pageNumber
        _last = df.shape[0]
        
        if _end > _last:
            _end = _last  # to display the last page number when the end of the list is reached  

        print("Displaying raw data for {}-{} rows of {}".format(_start, _end, _last))
        
        print(list_df[pageNumber-1])
        pageNumber += 1
        
        if pageNumber <= list_df_size:
            _display_raw_data = input("There are additional data to display. Would you like to see additional raw data? Enter Yes/Y or No/N.\n")
        else:
            print("No more raw data to display.")
            break

        if _display_raw_data.lower() not in yes or _end == _last:
            break

        #if pageNumber > list_df_size and list_df_size > 1:
         #   print("No more raw data to display.")
          #  break
        

#invoke main function
if __name__ == "__main__":
    main()


