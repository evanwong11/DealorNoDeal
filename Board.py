import random
import math
from collections import namedtuple


Case = namedtuple('Case', ['number', 'amount', 'in_play'])
# number = case number (int),
# amount = money value the case holds (double or int),
# in_play = whether the case is on the board (bool)


class DONDError(Exception):
    """
    raised when error to game occurs
    """
    pass


class Board:

    def __init__(self):
        self.turn = 1  # the turn in the game
        self.player_case = 0  # which case number the player has
        self._percentage = 1.05  # used to multiply the bank offer, increases each turn
        self.cases = []  # holds all of the cases in the game
        self._money = [0.01, 1, 5, 10, 25, 50, 75, 100,
                       200, 300, 400, 500, 750, 1000,
                       5000, 10000, 25000, 50000, 75000,
                       100000, 200000, 300000, 400000,
                       500000, 750000, 1000000]  # holds the values left on the board

    def set_up_board(self):
        """
        Randomizes money into the cases and add them to the board
        :return: none
        """
        random.shuffle(self._money)  # randomizes the order of the money
        for num in range(1, 27):  # 26 cases to be made and added to the board
            case = Case(num, self._money[num - 1], True)
            self.cases.append(case)
        self._money.sort()  # set the money back in order for printing purposes and hide the shuffled order

    def banker(self) -> int:
        """
        averages amount left on the board and returns that value
        :return: int
        """
        average = math.floor((sum(self._money) // len(self._money)) * self._percentage)
        #  get the average of money left on the board and multiply by the increasing percentage
        self._percentage += 0.05  # increases the percentage for the next turn
        return int(average)

    def valid_case(self, case_num) -> bool:
        """
        checks to see if case is in play, between 1 - 26 (inclusive)
        :param case_num:
        :return: bool
        """
        return 0 < case_num < 27 and self.cases[case_num - 1].in_play

    def remove_case(self, case_num):
        """
        remove cases from the board
        changes the case's in_play to false
        :param case_num: int
        :return: none
        """
        if self.valid_case(case_num):  # checks to see if case chosen is valid else raises an error
            self._money.remove(self.cases[case_num - 1].amount)  # remove the money from the board
            self.cases[case_num - 1] = self.cases[case_num - 1]._replace(in_play=False)  # sets the case to not in_play
        else:
            raise DONDError

    def pick_player_case(self, case_num):
        """
        player chooses a case
        :param case_num: int
        :return: none
        """
        if self.valid_case(case_num):  # checks to see if case chosen is valid else raises an error
            self.player_case = case_num  # assigns the case number chosen
            self.cases[case_num - 1] = self.cases[case_num - 1]._replace(in_play=False)  # sets case to not in_play
        else:
            raise DONDError

    def last_play_switch(self):
        """
        player wants to switch cases to the final case
        :return: none
        """
        for case in self.cases:  # searches for last case in play
            if case.in_play:
                self.player_case = case.number  # switches the player's case
                return

    def print_cases(self):
        """
        prints to output remaining cases
        :return: none
        """
        for case in self.cases:
            if case.in_play:
                print(case.number, end=' ')
        print()

    def print_money_on_board(self):
        """
        prints to output remaining money left
        :return: none
        """
        print(*self._money, sep=' ')
