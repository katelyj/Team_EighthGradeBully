# STUYTINERARY

**Team EighthGradeBully:** Kate Ly Johnston, Winston Venderbush, Patrick Chan, Maddie Ostergaard

*softdev pd9 -- final project*


# DESCRIPTION

Our project is a revamped version of Mr. Brooks’s bell schedule application, but more aesthetically pleasing, and with user functionality, such as personal schedule overlay, bell warnings, and A/B days.

Check the bell schedule, whether it's an A or B day, log in and customize your home schedule to see which classes you have next... and more!

# HOW TO USE LOCALLY

0. Open a terminal and make sure git and virtualenv are installed

1. Clone this repository.

```
$ git clone https://github.com/katelyj/Team_EighthGradeBully.git
```

2. Enter the repository, and run the flask app:

  *If never used before:*

```
  $ virtualenv softdev
  $ source softdev/bin/activate
  $ cd Team_EighthGradeBully/stuytinerary
  $ pip install requirements.txt
  $ python __init__.py
```

  *If already used:*

  ```
  $ cd Team_EighthGradeBully/stuytinerary
  $ python __init__.py
  ```

3. Open up a browser, and navigate to <localhost:5000>

# Features In Development

- Support for special schedules (available in beta version)
- Logging
- Robustification

# Future Plans

- Display User Schedule Info
