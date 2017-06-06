# STUYTINERARY

**Team EighthGradeBully:** Kate Ly Johnston, Winston Venderbush, Patrick Chan, Maddie Ostergaard

*softdev pd9 -- final project*


# DESCRIPTION

Our project is a revamped version of Mr. Brooks’s bell schedule application, but more aesthetically pleasing, and with user functionality, such as personal schedule overlay, bell warnings, and A/B days.

Check the bell schedule, whether it's an A or B day, log in and customize your home schedule to see which classes you have next... and more!

# HOW TO USE ON TERMINAL

1. Clone this repository.

```
$ git clone <https link... found above!>
```

2. If never run before:

- CD into 'dev_utils'
- Run the following command to initialize the database:
  ```
$ python populate_schedule_database.py
  ```

3. Enter the repository, and run the flask app:

  *If never used before:*

  ```
  $ pip install docs/requirements.txt
  $ python app.py
  ```

  *If already used:*

  ```
  $ python app.py
  ```

4. Go to the app, view the schedule, make an account... anything you want!

# Features In Development
- Display User Schedule Info
- Custom Schedules / No Schedule Error Handling
- Logging
- Robustification
