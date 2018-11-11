import Board


def print_board(board):
    """
    prints the cases and money on the board
    :param board: Board
    :return: none
    """
    print("Cases Available:")
    board.print_cases()
    print("Money Left on the Board:")
    board.print_money_on_board()
    if board.player_case != 0:
        print("Player's Case: {}\n".format(board.player_case))


def initial_setup(board):
    """
    sets up the board and player chooses a case
    raises error if player fails to enter an int
    :param board: Board
    :return: none
    """
    try:
        print("Let's Play Deal or No Deal!\n")
        board.set_up_board()  # sets up the cases and the money is shuffled
        print_board(board)  # displays cases left and money left
        board.pick_player_case(int(input("\nPick a Case to Hold onto (1 - 26): ")))  # player chooses a case to hold
        print()
    except ValueError:
        raise ValueError


def choose_cases(board):
    """
    player chooses cases to remove from the board
    shows amount the case had that was removed
    raises an error if player fails to enter an int
    :param board: Board
    :return: none
    """
    try:
        picks = {1: 6,  # first turn 6 choices
                 2: 5,  # second turn 5 choices
                 3: 4,  # third turn 4 choices
                 4: 3,  # fourth turn 3 choices
                 5: 2,  # fifth turn 2 choices
                 6: 1,  # sixth turn 1 choice
                 7: 1,  # seventh turn 1 choice
                 8: 1,  # eighth turn 1 choice
                 9: 1}  # ninth turn 1 choice
        for i in range(picks[board.turn]):  # chooses how many choices a player has based on the turn
            print_board(board)  # displays case and money left on the board
            print("You have {} more Choices!\n".format(picks[board.turn] - i))
            case_num = int(input("Choose a Case to reveal: "))  # chooses a case to be removed
            board.remove_case(case_num)  # removes the case from the board and the money value
            print("\nCase #{} had ${}\n".format(case_num, board.cases[case_num - 1].amount))
    except ValueError:
        raise ValueError


def bank_offer(board) -> bool:
    """
    Player makes a deal or no deal
    :param board: Board
    :return: bool
    """
    choice = ""
    print_board(board)  # displays the cases and money left on the board
    offer = board.banker()  # calculate average money left on the board to be offered
    print("The Banker Offer is: ${}".format(offer))
    while choice != "deal" and choice != "no deal":  # player accepts or declines bank offer
        choice = input("Deal or No Deal: ").lower()
    print()
    if choice == "deal":  # player takes the money and ends the game
        print("Congratulations on Earning ${}".format(offer))
        return True
    elif choice == "no deal":  # player declines and the game keeps on going
        board.turn += 1
        return False


def last_round(board):
    """
    Player may choose to switch cases or keep their case
    :param board: Board
    :return: none
    """
    choice = ""
    print("Here are the Remaining Cases on the Board.")
    print_board(board)  # displays remaining money and cases left on the board
    while choice != "y" and choice != "n":  # player can switch case or keep case chosen in the beginning
        choice = input("Would you like to switch your case? (y or n): ").lower()
    if choice == "y":  # player switches case with the remaining one on the board
        board.last_play_switch()
    print("Congratulations you won ${}".format(board.cases[board.player_case - 1].amount))


def main():
    """
    runs the game
    :return: none
    """
    board = Board.Board()
    end_game = False  # used to see if player accepted the bank offer thus ending the game
    initial_setup(board)
    while board.turn != 10 and not end_game:  # turn 10 is last possible turn with one remaining case left
        choose_cases(board)  # player chooses cases to remove from the board
        end_game = bank_offer(board)  # player either accepts or decline offer
    if board.turn == 10 and not end_game:
        last_round(board)  # player can switch cases to the final one on the board
    print("Thanks for Playing Deal or No Deal!")


if __name__ == '__main__':
    main()
