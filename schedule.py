"""
March 12, 2023
--------------
This file contains the schedule class, which will be used by schedule_builder
--------------
Authors: Richard, Hussain, Riyad, Hannah
"""

from __future__ import annotations
from lecture import Lecture
from timetable import Timetable

DEFAULT_LECTURE = Lecture('', [])


class Schedule:
    """
    A tree that holds many possible schedules. This is a recursive class that will store one course at each
    level.

    Instance Attributes:
        - root_lecture: the lecture at this level of the schedule
        - subtrees: the possible branching paths from this schedule. It maps the lecture code of the subtree's root
        lecture to the subtree.
    """
    root_lecture: Lecture
    subtrees: dict[str, Schedule]

    def __init__(self, root_lecture: Lecture) -> None:
        """
        Initializes a schedule with only a root lecture and empty subtrees.
        """
        self.root_lecture = root_lecture
        self.subtrees = {}

    def add_course(self, lectures: list[Lecture]) -> None:
        """
        Add a lecture to the schedule class. How this function will work is that it will first recurse down until it
        finds a leaf node. As it recurses down the tree, if it finds that any of the lectures in the list conflict with
        the root_lecture, it will remove that lecture from the list. This is to prevent the creation of schedules
        where lectures conflict with one another. Once it reaches the bottom leaf, it will then add all remaining
        lectures as their own recursive schedules.

        Implementation Notes:
        - If root_lecture is None, return
        - Make a copy of list lectures
        - If root_lecture conflicts with a lecture in lectures, remove that lecture from the copied list
        - Recurse into subtrees and add_course with copied list
        - Once there are no subtrees (you are at a leaf) then, add new schedules with their roots being the lectures.
        """
        # Create a copy of 'lectures', with only lectures that do not have conflicts with current lecture
        lectures_copy = []
        for lecture in lectures:
            #  For each lecture,if it does not have a conflict, add it to the new list
            if not lecture.conflict(self.root_lecture):
                lectures_copy.append(lecture)

        # Base Case (We are at a leaf)
        # Here, add each lecture in lecture list as a subtree. (Basically adding the course as a level of the tree)
        if len(self.subtrees) == 0:
            for lecture in lectures_copy:
                self.subtrees[lecture.lect_code] = Schedule(lecture)

        else:
            # Otherwise, recurse into the subtrees
            for subtree in self.subtrees:
                if len(lectures_copy) != 0:
                    # Recursively call add_course into the subtrees, with the new list of lectures,
                    # if the list is non-empty
                    self.subtrees[subtree].add_course(lectures_copy)

    def get_valid_paths(self, courses_count: int) -> list[list[str]]:
        """
        Return all valid paths within the schedule. Courses_count tells us how many lectures we need to collect before
        concluding our search for the path. If a path ends before reaching the course count, it will be disguarded as
        it is invalid.

        Implementation Notes:
        - if the path does not have the correct number of courses, do not add it to the list.
        - otherwise, add the lecture code (string) of the lectures to the list
        - for each new path, add a new list
        """
        paths = self._helper_get_paths(courses_count, 0)
        for i in range(len(paths) - 1, 0, -1):
            if len(paths[i]) < courses_count:
                paths.pop(i)
        return paths

    def _helper_get_paths(self, depth_to_reach: int, curr_depth: int) -> list[list[str]]:
        """
        Helper method to recursively return all valid paths of at a certain depth of the schedule. This is a recursive
        function.

        Base Case: we've reached the depth that we want to in the tree, and will return the root lecture code.
        Recursive Case: we still need to decend further. Gather all the paths of the subtrees of this node into a
        list, then add the root lecture code to the front of each list.
        """
        # Base case
        if curr_depth == depth_to_reach:
            return [[self.root_lecture.lect_code]]
        # Else (Recursive case)
        paths = []
        for i in self.subtrees:
            # self.subtrees[i] refers to the schedule below this one in the recursive tree
            returned_list = self.subtrees[i]._helper_get_paths(depth_to_reach, curr_depth + 1)

            # Note, this is for the case that we are on the starting lecture (default lect)
            # We do not want to include the starting lecture in our returned list.
            if curr_depth != 0:
                for path in returned_list:
                    path.insert(0, self.root_lecture.lect_code)
            paths.extend(returned_list)

        return paths

    def get_best_timetable(self, course_count: int, exclusion_days: set[str],
                           start_end_times: tuple[int, int]) -> Timetable:
        """
        Given the number of courses, exclusion days and start end times, construct the most optimal timetable. This
        function will get all possible paths and get the score for each path. It will then take the path with the best
        score, convert it to a timetable, and return it.

        course_count: the number of courses that the timetable will contain
        exclusion_days: a set of the weekdays when the student would not like to have classes
        start_end_times: a tuple containing at which hour the student would like to start and stop classes
        """
        valid_paths = self.get_valid_paths(course_count)

        best_timetable = None
        best_score = None

        for path in valid_paths:
            timetable = self.get_timetable(path)
            # Use the timetable function that returns a score.
            score = timetable.get_score(exclusion_days, start_end_times)

            # Find the best score
            if best_score is None or score > best_score:
                best_timetable = timetable
                best_score = score

        return best_timetable

    def get_timetable(self, path: list[str]) -> Timetable:
        """
        Given a path through the tree, construct a timetable and return it. In order to construct the timetable,
        get each root_lecture on the way down the path and store it in a list. Timetables can be created if a
        list of lectures are inputted.

        If the path is not valid, then raise a value error.
        """
        path_copy = path.copy()
        # to save on runtime, reverse the path so that the helper function can pop at constant runtime.
        path_copy.reverse()
        lectures = self._get_list_lectures_in_path(path_copy)
        return Timetable(lectures)

    def _get_list_lectures_in_path(self, path: list[str]) -> list[Lecture]:
        """
        A helper method that recurses and gets all the sessions in a schedule. This is a recursive method.

        Base Case: the inputted path list is empty, meaning you've collected all the neccessary lectures. Return the
        root lecture if it is not the DEFAULT_LECTURE.
        Recursive Case: get the last element of path and recurse into subtrees, following that path. Return a list
        of the lectures that you collect. If the root_lecture is not the DEFAULT_LECTURE, add it to the list.
        """
        if len(path) == 0:
            if len(self.root_lecture.sessions) > 0:
                return [self.root_lecture]
            else:
                return []
        else:
            lectures = []
            next_lect = path.pop()
            lectures.extend(self.subtrees[next_lect]._get_list_lectures_in_path(path))

            if len(self.root_lecture.sessions) > 0:
                lectures.append(self.root_lecture)

            return lectures


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['lecture', 'timetable'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
