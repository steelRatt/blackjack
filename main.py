# Blackjack
import random

MAX_SCORE = 21
player_cards = {}
cpu_cards = {}


def initialise_deck():
    """Initialise the deck for a new game"""

    # Dictionary for the cards in a deck
    suit = {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 10,
        "Queen": 10,
        "King": 10,
        "Ace": 11  # Defaults to 11, will be able to change to 1 if needed later
    }

    pack = {
        "Clubs": suit.copy(),
        "Diamonds": suit.copy(),
        "Hearts": suit.copy(),
        "Spades": suit.copy()
    }
    return pack.copy()


deck = initialise_deck()


def get_random_card(is_cpu):
    """Removes a random card from the deck to give to the player or CPU"""

    suit = random.choice(list(deck.keys()))  # Randomly picks a suit
    card_name = random.choice(list(deck[suit].keys()))  # Randomly picks a card from the chosen suit
    card_value = deck[suit].pop(card_name)  # Sets value and removes card from deck

    # If all cards from a suit have been removed, delete the suit to prevent choosing this suit again
    if not deck[suit]:
        del deck[suit]

    # If card for player is Ace, choose between value 1 or 11
    if card_name == "Ace" and not is_cpu:
        print(f"Your card is {card_name} of {suit}.")
        card_value = int(input("Would you like value to be 1 or 11? "))

    # Update player or CPU card dictionary
    # E.g. {('King', 'Diamonds'): 10, ('9', 'Clubs'): 9}
    card = (card_name, suit)
    if is_cpu:
        cpu_cards[card] = card_value
    else:
        player_cards[card] = card_value


def blackjack(cards):
    """Checks if player or CPU have a blackjack (11 and 10)"""

    if 11 in cards.values():
        if 10 in cards.values():
            return True


# If player's hand exceeds 21, they are bust and lose
# If CPU busts, player wins by default
# If player or CPU gets a Blackjack (Ace and 10 point card) they automatically win
# If both player and CPU have Blackjack, it's a draw

def calculate_winner(player_score, player_blackjack, cpu_score, cpu_blackjack):
    """Takes final player and CPU score and determines winner of current game"""

    if player_score == MAX_SCORE:
        if cpu_score == MAX_SCORE:
            if player_blackjack and cpu_blackjack:
                return "Player and dealer have Blackjack! Draw!\n"
            else:
                return "Player and dealer have 21! Draw!\n"
        else:
            return "You have 21! You win!\n"
    elif cpu_score == MAX_SCORE:
        if player_score > MAX_SCORE:
            return "Dealer has 21! You went over. You lose.\n"
        else:
            return f"Dealer has 21! You were {MAX_SCORE - player_score} away. You lose.\n"
    elif cpu_score > MAX_SCORE:
        return "Dealer is bust. You win!\n"
    elif player_score > MAX_SCORE:
        return f"You are bust! You were over by {player_score - MAX_SCORE}. You lose.\n"
    elif player_score < MAX_SCORE and cpu_score < MAX_SCORE:
        if player_score > cpu_score:
            return "You were closer to 21. You win!\n"
        elif cpu_score > player_score:
            return "Dealer is closer to 21. You lose!\n"
        else:
            return "Draw!\n"


def play():
    """The main blackjack game"""

    global deck  # Ensure the global variable deck is being used here
    deck = initialise_deck()  # Replenish the deck for the start of a new game

    # Clear player and CPU cards for start of game
    player_cards.clear()
    cpu_cards.clear()

    # Assign cards
    get_random_card(False)
    get_random_card(False)
    get_random_card(True)
    get_random_card(True)

    player_blackjack = blackjack(player_cards)
    cpu_blackjack = blackjack(cpu_cards)

    # Display player's initial 2 cards
    print(f"\nYour cards:")
    print("\n".join([f"{name} of {suit}" for name, suit in player_cards.keys()]))
    if player_blackjack:
        print("\nBLACKJACK!\n")
    print(f"\nPlayer score: {sum(player_cards.values())}\n-------------------------------")

    # Only show CPU's first card and not second
    print(f"Dealer's cards:")
    print("".join([f"{name} of {suit}" for name, suit in cpu_cards.keys()][0]))
    print("Hidden")
    print(f"\nDealer score: ")
    print("".join([f"{score}" for score in cpu_cards.values()][0]))
    print("-------------------------------")

    # Hit
    if not player_blackjack:
        if input("Hit? (yes/no): ").lower() == "yes":
            get_random_card(False)

    # Display player cards
    print(f"\nYour cards:")
    print("\n".join([f"{name} of {suit}" for name, suit in player_cards.keys()]))
    print(f"\nPlayer score: {sum(player_cards.values())}\n-------------------------------")

    # CPU must continue to hit until its hand value reaches 17 or higher
    while sum(cpu_cards.values()) < 17:
        get_random_card(True)

    # Display dealer cards
    print(f"\nDealer's cards:")
    print("\n".join([f"{name} of {suit}" for name, suit in cpu_cards.keys()]))
    if cpu_blackjack:
        print("\nBLACKJACK!\n")
    print(f"\nDealer score: {sum(cpu_cards.values())}\n-------------------------------")

    # Calculate winner
    return calculate_winner(sum(player_cards.values()), player_blackjack, sum(cpu_cards.values()), cpu_blackjack)


def game_loop():
    """Allows the user to continuously play another game after their current game ends"""

    is_continue = "yes"
    while is_continue == "yes":
        print(play())
        is_continue = input("Do you want to play another game? (yes/no): ").lower()


game_loop()
