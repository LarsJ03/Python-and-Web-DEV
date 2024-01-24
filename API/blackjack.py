import random


# Create a {Cards} class that holds multiple cards (not single card). Standard playing cards have a rank
# (ace, two through ten, jack, queen and king) and suit (clubs, diamonds, hearts, spades).
# This class should output (print) the cards contained in this object.
# The class should have a  method to rank the cards (by rank) and (another method) to sort by suit.
# Possible values for rank are '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'.
# Possible values for suit are 'C', 'D', 'H', 'S'.
class Cards:
    """
        Represents a collection of playing cards. Each card is represented as a tuple with a rank and a suit.

        Attributes:
            rank_suit (list of tuples): The list of cards as (rank, suit) tuples.
            rank_order (dict): A dictionary mapping card ranks to their corresponding order value.
            suit_order (dict): A dictionary mapping card suits to their corresponding order value.
        """

    def __init__(self, rank_suit):
        """
                Initialize the Cards instance with a list of (rank, suit) tuples.

                Args:
                    rank_suit (list of tuples): The initial cards in the collection.
                """
        # rank_suit is a list of tuples
        self.rank_suit = rank_suit
        # orderings to be used in the rank and suit methods
        rank_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suit_list = ['C', 'D', 'H', 'S']
        self.rank_order = {rank: i for i, rank in enumerate(rank_list)}
        self.suit_order = {suit: i for i, suit in enumerate(suit_list)}

    def rank_cards(self):
        """Sort the cards in the collection by rank"""
        self.rank_suit.sort(key=lambda x: self.rank_order[x[0]])
        print('Cards ranked by rank: ', self.rank_suit)

    def sort_suit(self):
        """Sort the cards in the collection by suit"""
        self.rank_suit.sort(key=lambda x: self.suit_order[x[1]])
        print('Cards sorted by suit: ', self.rank_suit)

    def add_card(self, card):
        """Add a card to the collection

        Args:
            card (Cards): A Cards instance representing the cards to be added.
        """
        self.rank_suit.extend(card.rank_suit)

    def __str__(self):
        return f"Cards({self.rank_suit!r})"


class Deck(Cards):
    """
        Represents a standard deck of 52 playing cards, inheriting from the Cards class.
        Provides functionality to shuffle the deck and deal cards from it.
        """

    def __init__(self):
        rank_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suit_list = ['C', 'D', 'H', 'S']
        rank_suit = [(rank, suit) for suit in suit_list for rank in rank_list]
        super().__init__(rank_suit)

    def shuffle(self):
        """Shuffle the deck of cards in place."""
        random.shuffle(self.rank_suit)
        print('Deck shuffled.')

    def deal_cards(self, number=1):
        """
                Deal a number of cards from the deck.

                Args:
                    number (int): The number of cards to deal. Defaults to 1.

                Returns:
                    list of tuples: The list of dealt cards.
                """
        # Deal the specified number of cards
        dealt_cards = self.rank_suit[:number]
        self.rank_suit = self.rank_suit[number:]
        return dealt_cards

    def reset_deck(self):
        """Resets the deck to a full deck of cards and shuffles."""
        rank_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suit_list = ['C', 'D', 'H', 'S']
        self.rank_suit = [(rank, suit) for suit in suit_list for rank in rank_list]
        self.shuffle()


class Hand(Cards):
    """
    Represents a hand of playing cards in a game. Inherits from Cards class.
    A Hand can add cards and calculate scores based on game rules.
    """

    def __init__(self):
        super().__init__(rank_suit=[])  # Initialize with an empty list of cards.

    def calculate_score(self):
        """
        Calculate the score of the hand. In Blackjack, the score is the sum of card values with
        Ace being 1 or 11 points, face cards being 10 points, and other cards being their pip value.

        Returns:
            int: The score of the hand.
        """
        score = 0
        aces = 0
        for rank, _ in self.rank_suit:
            if rank in 'JQK':
                score += 10
            elif rank == 'A':
                aces += 1
            else:
                score += int(rank)

        # Add aces, considering them as 1 point or 11 points to maximize the score without busting.
        for _ in range(aces):
            score += 11 if score + 11 <= 21 else 1

        return score

    def add_card(self, card):
        """
        Adds a card to the hand. The card should be a tuple containing the rank and suit.

        Args:
            card (tuple): The card to add to the hand, represented as (rank, suit).
        """
        if isinstance(card, tuple) and len(card) == 2:
            self.rank_suit.append(card)
        else:
            raise ValueError("Invalid card format. Must be a tuple of (rank, suit).")

    def clear_hand(self):
        """Clears all cards from the hand."""
        self.rank_suit = []


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.deck.shuffle()

    def start_game(self):
        # Initial deal (2 cards each)
        self.player_hand.add_card(self.deck.deal_cards(1)[0])
        self.player_hand.add_card(self.deck.deal_cards(1)[0])
        self.dealer_hand.add_card(self.deck.deal_cards(1)[0])
        self.dealer_hand.add_card(self.deck.deal_cards(1)[0])

        print("Player's hand:", self.player_hand)
        print("Dealer's hand:", self.dealer_hand)

    def dealer_plays(self):
        player_score = self.player_hand.calculate_score()
        while True:
            dealer_score = self.dealer_hand.calculate_score()
            # Dealer hits if score is less than 17, or if dealer is trailing player's score (above 17)
            if dealer_score < 17 or (dealer_score < player_score and player_score <= 21):
                self.dealer_hand.add_card(self.deck.deal_cards(1)[0])
            else:
                break

    def check_winner(self):
        # Assuming dealer plays after the player has stood
        self.dealer_plays()

        player_score = self.player_hand.calculate_score()
        dealer_score = self.dealer_hand.calculate_score()

        print(f"Player's score: {player_score} with {self.player_hand}")
        print(f"Dealer's score: {dealer_score} with {self.dealer_hand}")
        if player_score == 21 and dealer_score == 21:
            return "Player and dealer have blackjack so its a tie!"
        elif player_score == 21:
            return "Player wins with a blackjack!"
        elif dealer_score == 21:
            return "Dealer wins with a blackjack!"
        if player_score > 21:
            return "Dealer wins!"
        elif dealer_score > 21:
            return "Player wins!"
        elif player_score > dealer_score:
            return "Player wins!"
        elif player_score < dealer_score:
            return "Dealer wins!"
        else:
            return "It's a tie!"
