"""
March 08, 2023
--------------
This file contains the time class
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations


class Time:
    """
    This class holds the time.
    """
    hours: int
    minutes: int

    def __init__(self, hours: int, minutes: int) -> None:
        self.hours = hours
        self.minutes = minutes

    def __gt__(self, other: Time) -> bool:
        """
        >>> t1 = Time(1, 10)
        >>> t2 = Time(3, 10)
        >>> t2 > t1
        True
        """
        if self.hours > other.hours:
            return True
        elif self.hours == other.hours and self.minutes > other.minutes:
            return True
        else:
            return False

    def __ge__(self, other: Time) -> bool:
        """
        >>> t1 = Time(1, 10)
        >>> t2 = Time(1, 10)
        >>> t2 >= t1
        True
        """
        if self.__gt__(other) or self.__eq__(other):
            return True
        return False

    def __le__(self, other: Time) -> bool:
        """
        >>> t1 = Time(10, 10)
        >>> t2 = Time(3, 10)
        >>> t2 <= t1
        True
        """
        if self.__lt__(other) or self.__eq__(other):
            return True
        return False

    def __lt__(self, other: Time) -> bool:
        """
        >>> t1 = Time(10, 10)
        >>> t2 = Time(3, 10)
        >>> t2 < t1
        True
        """
        if self.hours < other.hours:
            return True
        elif self.hours == other.hours and self.minutes < other.minutes:
            return True
        else:
            return False

    def __eq__(self, other: Time) -> bool:
        """
        >>> t1 = Time(10, 10)
        >>> t2 = Time(10, 10)
        >>> t2 == t1
        True
        """
        if self.hours == other.hours and self.minutes == other.minutes:
            return True
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
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
