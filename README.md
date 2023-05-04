This is the final CAB collaborative project for Group 4 (Elliot Topper, Shannon Joseph, Spandana Bondalapati).

## Creating the Database

To create and populate the database, ensure psql is installed on the machine.

To create the database to be used for the project, define the schema and populate the database using:

```
$ ./createdb.sh
```

## Running the Application

To run the web application, [python3](https://www.python.org/) must be installed on the system.
For example, using apt (if installed):

```
$ sudo apt install python3
```

Once python3 is installed, necessary libraries ([flask](https://flask.palletsprojects.com/en/2.2.x/), [psycopg2](https://pypi.org/project/psycopg2/), and [python-dotenv](https://pypi.org/project/python-dotenv/)) can be automatically installed in the Python environment using:

```
$ app/install.sh
```

Additionally, `.env` should be edited to contain the username and password of some user who has read permissions on the entire `sustainability` database. This may include the root psql user for the system.

&nbsp;

Once all system requirements are met, start the flask server using

```
$ python3 app/app.py
```

This will run the web application - it should now be available at https://127.0.0.1:5000.

This application provides comparative EV and Greenhouse Gas metrics for municipalities across the state, allowing municipalities to see their progress in greenhouse gas emissions over the past few years, especially in comparison to others around them. Ideally, this will promote more sustainable practices across the state.

Sample images of the GUI:

<img width="500" alt="main_map" src="https://user-images.githubusercontent.com/91216718/234443109-bcd688c0-1e7c-41f0-92db-34ba3be9bf87.png">

<img width="500" alt="county_emissions" src="https://user-images.githubusercontent.com/91216718/234489908-69c29a08-3b4c-473c-9e0a-9857c8cbcc73.png">

<img width="500" alt="Screen Shot 2023-04-29 at 6 53 42 PM" src="https://user-images.githubusercontent.com/91216718/235327297-c168c7ed-4707-4a5a-9cdb-e97ab92b36e7.png">

