"""
March 08, 2023
--------------
This file contains the session class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from time_h import Time


class Session:
    """
    A class that represents a single lecture session.

    Instance Attributes:
        - day: which day of the week does this lecture take place
        - start_time: at what time does this lecture start
        - end_time: at what time does this lecture end
        - location: the address where the lecture will take place
    """
    start_time: Time
    end_time: Time
    day: str
    location: str

    def __init__(self, time: tuple[Time, Time], day: str, location: str) -> None:
        """
        Initialize a session. The first element of the time tuple is the start time and
        the second element is the end time.

        >>> session = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        >>> session.day
        'MON'
        """
        self.start_time = time[0]
        self.end_time = time[1]
        self.day = day
        self.location = location

    def conflict(self, other: Session) -> bool:
        """
        Return if this session conflicts with another session. This happens when one session's hours overlap the other
        session's hours.

        >>> s1 = Session((Time(1, 40), Time(4, 20)), "MON", "Mining Building")
        >>> s2 = Session((Time(3, 0), Time(6, 0)), "MON", "Mining Building")
        >>> s1.conflict(s2)
        True
        >>> s3 = Session((Time(4, 30), Time(6, 0)), "MON", "Mining Building")
        >>> s1.conflict(s3)
        False
        >>> s1 = Session((Time(9, 0), Time(10, 0)), "MON", "Mining Building")
        >>> s2 = Session((Time(9, 0), Time(11, 0)), "MON", "Jord")
        >>> s1.conflict(s2)
        True
        >>> s1 = Session((Time(9, 0), Time(10, 0)), "MON", "Mining Building")
        >>> s2 = Session((Time(10, 0), Time(11, 0)), "MON", "Jord")
        >>> s1.conflict(s2)
        False
        """
        if self.day == other.day and self.start_time < other.end_time and self.end_time > other.start_time:
            return True
        return False

    def adjacent(self, other: Session) -> bool:
        """
        Return if this session is directly adjacent to the other session (when this session ends, the other starts, or
        when this session starts is the end of the other session)

        >>> s1 = Session((Time(1, 40), Time(4, 20)), "MON", "Mining Building")
        >>> s2 = Session((Time(4, 20), Time(5, 20)), "MON", "Mining Building")
        >>> s1.adjacent(s2)
        True
        >>> s2.adjacent(s1)
        True
        """
        if self.day == other.day and (self.end_time == other.start_time or self.start_time == other.end_time):
            return True
        return False

    def time_check(self, compare: str) -> bool:
        """
        Compare is a string in the form xy :00 - rz :00 where y and r may or may not be 0. Given the start and end time
        of the session, this function aims to tell us if the time is the same as the string or if the string is
        contained in the range between the start and end time.

        Precondition:
        - the time difference between xy: 00 and rz: 00 is 1 hour
        """

        compare_again = str.split(compare)

        if self.start_time.hours <= int(compare_again[0]) and self.end_time.hours >= int(compare_again[3]):
            return True
        else:
            return False


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['time_h'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
