"""
March 29, 2023
--------------
This file contains the get_travel_time method which'll be used to get the amount of time it takes to walk betwen
two places.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""
import datetime
import googlemaps
API_KEY = 'AIzaSyDmhjbDyLYlW-2OQyvcLt0qjOYKDozhUt8'
gmaps = googlemaps.Client(key=API_KEY)


def get_travel_time(start_location: str, end_location: str) -> int:
    """
    Return the time taken to travel between two addresses in minutes
    """
    try:
        direction = gmaps.directions(start_location, end_location, mode="walking",
                                     departure_time=datetime.datetime.now())
        time = direction[0]['legs'][0]['duration']['value']

        return time // 60
    # The google maps cannot detect certain locations, and so we will return a default
    # value for those locations
    except (googlemaps.exceptions.ApiError, IndexError):
        return 10


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['googlemaps', 'datetime'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
