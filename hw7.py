"""
INTRO
"""
from functools import reduce


class Plant:
    """
    A representation of a plant. Implements a constructor with defaulting values(except one),
     a represent overload and 2 more methods:
    # get_maintenance_cost.
    # purchase_decision.
    """
    def __init__(self, name: str,
                 aesthetics: int = 1,
                 water_consumption_month: int = 1,
                 average_month_yield: int = 1,
                 seasonal: bool = False):
        """
        Initializes an instance of Plant.
        :param name: (str) the name of the plant.
        :param aesthetics: (int) the level of aesthetics the plant is valued at.
        :param water_consumption_month: (int) the plant's monthly consumption of water amount
        :param average_month_yield: (int) the value the plant creates every month
        :param seasonal: (bool) whether the plant is year-round (True) plantation or only 6 months (False).
        """
        self.name = name
        self.aesthetics = aesthetics
        self.water_consumption_month = water_consumption_month
        self.average_month_yield = average_month_yield
        self.seasonal = seasonal

    def get_maintenance_cost(self, func1):
        """
        Invokes the given argument as a function with the instance itself (self) as input argument.
        :param func1: a function object.
        :return:
        """
        return func1(self)

    def purchase_decision(self, func1, func2):
        """
        Invokes the first given argument as a function with two inputs (by order):
         the instance itself, and the result of the second argument invoked as a function with the instance
         itself (self) as input argument.
        :param func1: a function object.
        :param func2: a function object.
        :return:
        """
        return func1(self, func2(self))

    def __repr__(self):
        """
        overloads the python object __repr__ method.
        :return: str
        """
        return "name={}".format(self.name)


class GardenManager:
    """
    A representation of a garden management system. Implements a constructor with no defaulting values,
     a represent overload and 1 more methods:
     # action.
    """
    def __init__(self, plants_in_garden: list):
        """
        Initializes an instance of GardenManager.
        :param plants_in_garden: a list of the plants which are in the garden.
        """
        self.plants_in_garden = plants_in_garden

    def action(self, func1):
        """
        Invokes the given argument as a function with the instance itself (self) as input argument.
        :param func1: a function object.
        :return:
        """
        return func1(self)

    def __repr__(self):
        """
        overloads the python object __repr__ method.
        :return: str
        """
        return "Number of plants = {0}".format(len(self.plants_in_garden))
#

"""
PART A - Lambda functions
"""

# Q1
get_cost_lmbd = lambda x: x.water_consumption_month  # returns plant's water_consumption_month.

# Q2
get_yearly_cost_lmbd = lambda x: x.water_consumption_month * 6 if x.seasonal else x.water_consumption_month * 12  # checks if plant is seasonal (consumpts water for 6 or 12 months).

# Q3
worth_investing_lmbd = lambda x: True if x.average_month_yield > x.water_consumption_month else False  # checks if average_month_yield is greater than water_consumption_month.

# Q4
declare_purchase_lmbd = lambda x, y: '{}:yes'.format(x.name) if y or (not y and x.aesthetics >= x.water_consumption_month) else '{}:no'.format(x.name)  # checks if y is True or y is False + aesthetics is greater than or equal to water_consumption_month.

# Q5
get_plants_names_lmbd = lambda x: sorted([flower.name for flower in x.plants_in_garden])  # returns sorted list of the names of the plants.

"""
PART B - High order functions
"""

# Q1 -
def retrospect(garden_manager):
    return list(map(lambda x:x.name, filter(worth_investing_lmbd, garden_manager.plants_in_garden)))  # filters plants of list by operate worth_investing_lmbd on each one.

# Q2 -
def get_total_yearly_cost(garden_manager):
    if not garden_manager.plants_in_garden:  # in case list is empty.
        return 0  # no plants means no cost.
    return reduce(lambda x, y: x + y, map(get_yearly_cost_lmbd, garden_manager.plants_in_garden))  # sums all plant's yearly cost.

# Q3 -
def get_aesthetics(garden_manager):
    return list(map(lambda x:x.aesthetics, garden_manager.plants_in_garden))  # runs over all plants and returns list of aesthetics.

"""
PART C - University gate
"""
class Student:  # help class for managing queue of students.
    def __init__(self, student_id, priority_id_holder):
        self.student_id = student_id  # unique for each student.
        self.priority_id_holder = priority_id_holder  # True if students has the card, False otherwise.

class GateLine:
    def __init__(self, max_capacity=5):
        self.max_capacity = max_capacity  # maximum number of people can wait in the queue.
        self.queue = []  # implementation of a queue using a list.

    def new_in_line(self, student_id, priority_id_holder):
        if len(self.queue) < self.max_capacity:  # checks if queue is not full.
            self.queue.insert(0, Student(student_id, priority_id_holder))  # if not, the student can join the queue.
        else:  # if queue is full.
            if priority_id_holder:  # checks if student has priority card.
                counter = 0  # initials a counter.
                while len(self.queue) >= self.max_capacity and counter < len(self.queue):  # runs as long as queue is full and counter can point students on the queue (not out of range).
                    if not self.queue[counter].priority_id_holder:  # checks if student dont have priority card.
                        self.queue.pop(counter)  # if he doesn't he is getting out of the queue.
                    else:
                        counter += 1  # if student has a priority card, we keep search for other students with no priority.
                self.queue.insert(0, Student(student_id, priority_id_holder))  # now it's possible to add the student to the queue (other students expelled or all of the queue are priorities).

    def open_gate(self):
        if not self.queue:  # in case queue has no students (empty).
            return None  # no one has entered the university.
        for i in range(len(self.queue) - 1, -1, -1):  # runs over the queue from the beginning to the end.
            if self.queue[i].priority_id_holder:  # checks if student has a priority card.
                return self.queue.pop(len(self.queue)-1).student_id  # if so, pops him out of the queue and returns his ID.
        return self.queue.pop(len(self.queue) - 1).student_id  # if no priority card holders are in the queue, pops the first student on the queue and returns his ID.

    def is_empty(self):
        return len(self.queue) == 0  # returns whether queue is 0 long or not.

    def show_who_is_in_line(self):
        result = []  # list we gonna fill first with ID's of students with priority and then with ID's of students with no priority and return it.
        for i in range(len(self.queue) - 1, -1, -1):  # runs over the queue from the beginning to the end to search for priority card holders.
            if self.queue[i].priority_id_holder:  # checks if student has a priority card.
                result.append(self.queue[i].student_id)  # inserts his ID to the result list.
        for i in range(len(self.queue) - 1, -1, -1):  # runs over the queue from the beginning to the end to search for students with no priority card.
            if not self.queue[i].priority_id_holder:  # checks if student doesn't have a priority card.
                result.append(self.queue[i].student_id)  # inserts his ID to the result list.
        return result  # returns list of ID's