"""MBULELO PANI, Class 2"""

import mysql.connector  # importing the connector module

# create connection to database
db = mysql.connector.connect(port="3306", host="localhost", user="mbulelo", password="1234",
                             database="lifechoicesonline")
# creating instance cursor for executing sql statements
cursor = db.cursor()


# Function to handle logging in
def login():
    cursor.execute("select * from users")  # Select data from the tables 'users'
    result = cursor.fetchall()  # Fetch all the rows
    # User enters his/her details, including date and time
    fullname = input("Enter your fullnames: ")
    password = str(input("Enter password: "))
    date = str(input("Enter date(yyyy-mm-dd): "))
    time = str(input("Enter time(hh:mm:ss): "))

    a = False
    for x in result:
        # if fullname and password are found in the table 'users'...
        if fullname in x and password in x:
            # ..then then a is true
            a = True
            # and if a is true, execute the following
            cursor.execute("insert into new_userlog(fullname, date, login_time) values(%s, %s, %s)",
                           (fullname, date, time))
    if a:
        # print out this message after successful login
        print("Succesfully logged in.")
    else:
        # user directed to reception if login fails
        print("Unknown user. Contact reception.")


# Function to handle the logging out
def logout():
    cursor.execute("select * from new_userlog")  # Selects the data from new_userlog
    res = cursor.fetchall()  # Fetches the rows in the table 'new_userlog'
    # user enters fullname and time of logging out
    fullname = input("Enter your fullnames: ")
    date = str(input("Enter today's date(yyyy-mm-dd): "))
    logout_time = str(input("Enter current time(hh:mm:ss): "))

    log = False
    for x in res:
        if fullname in x:  # if fullname is found in the 'table' new_userlog', then..
            log = True  # the user did login
            # if user did login, then insert his/her details and logout time in logout table
            cursor.execute("insert into user_logout(fullname, date, logout_time) values(%s, %s, %s)", (fullname,date, logout_time))
    if log:
        # prints out the following if logout was successful
        print("success")
    else:
        print("You weren't logged in.")  # if user wasnt logged in


# Function to handle registration
def register():
    cursor.execute("select * from users")           # select the data from 'users'
    res = cursor.fetchall()                         # fetch all the rows
    fullname = input("Enter fullname: ")            # user enter fullname
    username = input("Create a username: ")         #   "  creates a new username
    pswd = str(input("Create a password"))          #   "  creates a new pasword
    reg = False
    for x in res:
        # if username is not found the 'users' table
        if username not in x:
            reg = True      # ...then reg is not registered
    if reg:
        # if reg is true, execute the following
        cursor.execute("insert into users(full_name, username, password, registration_date) value(%s, %s, %s, NOW())",
                       (fullname, username, pswd))
    else:
        # if username is found in table, print the following
        print("Oops, try another username.")
def view_userlog():

    cursor.execute("select * from new_userlog")
    users = cursor.fetchall()
    for x in users:
        print("Logged in users:")
        print(x)  # print list of users
    cursor.execute("select * from user_logout")
    users = cursor.fetchall()
    for x in users:
        print("Logged out users"
              ":")
        print(x)  # print list of users

# main menu screen
def menu():
    print("Welcome to Lifechoices")
    # options listed
    opt = int(input("1.Login \t2.Logout \t3.Register \t4.Admin \t5.View logged users"))
    # call the relevant function based on user input
    if opt == 1:
        login()
    elif opt == 2:
        logout()
    elif opt == 3:
        register()

    elif opt == 4:
        # logging in as admin
        admin_login = False
        # while not logged in as admin
        while not admin_login:
            # Select the users from mysql.user
            cursor.execute("select user from mysql.user")
            admins = cursor.fetchall()
            # enters username and password
            username = input("Enter username: ")
            password = input("Enter password: ")

            admin = False
            for x in admins:
                if username in x:
                    # if the username is found on mysql.user, login succeeds
                    admin = True
                    print("Welcome admin.")
            while admin:
                # if admin logged in, call the admin_logged function
                admin_logged()
            else:
                # is username not found, display following message
                print("Something went wrong.")
    elif opt == 5:
        view_userlog()

# function to handle admin activity
def admin_logged():
    # options for the admin
    opt = int(input("1.Create a user \t2. View registered users  \t.3. Grant privileges \n4.Quit "))
    if opt == 1:
        # option to add user, data from mysql.user selected, and all rows fetched
        cursor.execute("select host, user from mysql.user")
        users = cursor.fetchall()
        # admin enters the details
        fullname = input("Enter fullname: ")
        username = input("Create a username: ")
        password = input("Create a password: ")

        user = False
        for x in users:
            if username in x:       # if user is found in mysql.user
                user = True         # ...then user already exists
        # if user doesn't exist
        if not user:        # if user doesn't exist
            try:
                # execute the following
                cursor.execute("CREATE USER '%s'@'localhost' IDENTIFIED BY '%s'" % (username, password))
            except Exception:
                print("Failed")
        else:
            # display the following if operation fails
            print("Failed to add user.")

    elif opt == 2:      # option to view users
        # select from mysql.user
        cursor.execute("select host, user from mysql.user")
        users = cursor.fetchall()
        for x in users:
            print("All the users:")
            print(x) # print list of users
    elif opt == 3:      # option to grant users privileges
        # select from mysql.user
        cursor.execute("select host, user from mysql.user")
        users = cursor.fetchall()
        # admin enters relevant user details
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = False
        for x in users:
            if username in x:       # if username found on mysql.user
                user = True         # then the user exists
        if user:
            # if user exist, do grant
            cursor.execute("GRANT CREATE, SELECT ON *.* TO '%s'@'localhost' IDENTIFIED BY '%s'" % (username, password))
        else:
            # display following if operation fails
            print("Failed")
    elif opt == 4:
        menu()      # return to main screen


menu()
db.commit()
