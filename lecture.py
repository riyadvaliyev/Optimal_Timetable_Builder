"""
March 08, 2023
--------------
This file contains the lecture class, which will contain information on lecture time and location.
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from session import Session
from time_h import Time


class Lecture:
    """
    A class that represents a lecture section. Includes all classes (their times and locations) for that lecture
    section.

    Instance Attributes:
        - sessions: a list of sessions that must be taken in this lecture section.
        - lect_code: Combine the course code with the lecture code. This will be the identifier for the lecture
        (Example: "csc111 lec101")
    """
    lect_code: str
    sessions: list[Session]

    def __init__(self, lect_code: str, sessions: list[Session]) -> None:
        """
        Initialize a lecture with a list of sessions

        Test initialization:
        >>> s1 = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        >>> s2 = Session(time=(Time(1, 15), Time(20, 30)), day="TUES", location="THAT PLACE")
        >>> lecture = Lecture("Lect_code", [s1, s2])
        >>> lecture.sessions[0].day
        'MON'
        """
        self.sessions = sessions
        self.lect_code = lect_code

    def conflict(self, other: Lecture) -> bool:
        """
        Return if this lecture section conflicts with another lecture section.

        >>> s1 = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        >>> s2 = Session(time=(Time(1, 15), Time(20, 30)), day="TUES", location="THAT PLACE")
        >>> lecture1 = Lecture("LECT_CODE", [s1, s2])
        >>> s3 = Session(time=(Time(1, 15), Time(2, 30)), day="MON", location="THIS PLACE")
        >>> s4 = Session(time=(Time(1, 15), Time(20, 30)), day="TUES", location="THAT PLACE")
        >>> lecture2 = Lecture("LECT_CODE", [s3, s4])
        >>> lecture1.conflict(lecture2)
        True
        >>> s5 = Session(time=(Time(1, 15), Time(2, 30)), day="THU", location="THIS PLACE")
        >>> s6 = Session(time=(Time(1, 15), Time(20, 30)), day="FRI", location="THAT PLACE")
        >>> lecture3 = Lecture("LECT_CODE", [s5, s6])
        >>> lecture3.conflict(lecture1)
        False
        """
        for i in range(len(self.sessions)):
            for c in range(len(other.sessions)):
                if self.sessions[i].conflict(other.sessions[c]):
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

    # NOTE: Python TA will mark an error because time_h isn't used, but it is required for doctest purposes.
    python_ta.check_all(config={
        'extra-imports': ['session', 'time_h'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
