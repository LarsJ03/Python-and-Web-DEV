import pytest
from API import blackjack


@pytest.fixture(scope='session')
def create_4_cards():
    return blackjack.Cards([('2', 'C'), ('4', 'S'), ('3', 'H'), ('5', 'D')])


def test_cards_init(create_4_cards):
    assert create_4_cards.rank_suit == [('2', 'C'), ('4', 'S'), ('3', 'H'), ('5', 'D')]


def test_rank_cards(create_4_cards):
    create_4_cards.rank_cards()
    assert create_4_cards.rank_suit == [('2', 'C'), ('3', 'H'), ('4', 'S'), ('5', 'D')]


def test_sort_suit(create_4_cards):
    create_4_cards.sort_suit()
    assert create_4_cards.rank_suit == [('2', 'C'), ('5', 'D'), ('3', 'H'), ('4', 'S')]


def test_add_card():
    cards = blackjack.Cards([('2', 'C'), ('4', 'S')])
    new_card = blackjack.Cards([('5', 'H')])
    cards.add_card(new_card)
    assert cards.rank_suit == [('2', 'C'), ('4', 'S'), ('5', 'H')]


def test_deck_init():
    deck = blackjack.Deck()
    assert len(deck.rank_suit) == 52  # A new deck should have 52 cards


def test_deck_shuffle():
    deck = blackjack.Deck()
    before_shuffle = deck.rank_suit.copy()
    deck.shuffle()
    after_shuffle = deck.rank_suit
    assert before_shuffle != after_shuffle  # The order should change after shuffle
    assert sorted(before_shuffle) == sorted(after_shuffle)  # The cards remain the same, only order changes


def test_deal_cards():
    deck = blackjack.Deck()
    deck.shuffle()  # Shuffle the deck before dealing
    dealt_cards = deck.deal_cards(5)
    assert len(dealt_cards) == 5  # Should deal 5 cards
    assert len(deck.rank_suit) == 52 - 5


@pytest.fixture(scope='session')
def create_hand():
    return blackjack.Hand()


@pytest.fixture(scope='module')
def new_deck():
    return blackjack.Deck()


@pytest.fixture(scope='module')
def empty_hand():
    return blackjack.Hand()


def test_hand_initial_empty(empty_hand):
    assert len(empty_hand.rank_suit) == 0, "Hand should be initialized empty."


def test_add_card_to_hand(empty_hand):
    empty_hand.add_card(('A', 'S'))
    assert len(empty_hand.rank_suit) == 1, "Hand should have one card after adding."
    assert empty_hand.rank_suit[0] == ('A', 'S'), "The Ace of Spades should be in the hand."


def test_calculate_score_with_various_cards(empty_hand):
    # Reset hand to empty
    empty_hand.rank_suit = []

    # Add a combination of cards to the hand
    cards_to_add = [('J', 'H'), ('A', 'S'), ('3', 'D')]
    for card in cards_to_add:
        empty_hand.add_card(card)

    # Test the score
    assert empty_hand.calculate_score() == 14, "Hand with J, A, and 3 should have a score of 14."


def test_hand_score_with_multiple_aces(empty_hand):
    # Reset hand to empty
    empty_hand.rank_suit = []

    # Add multiple aces to the hand
    cards_to_add = [('A', 'S'), ('A', 'H')]
    for card in cards_to_add:
        empty_hand.add_card(card)

    # Test the score
    assert empty_hand.calculate_score() == 12, "Hand with two Aces should have a score of 12."


def test_deal_cards_from_deck_to_hand(new_deck, empty_hand):
    empty_hand.clear_hand()  # Ensure the hand is empty before the test
    new_deck.reset_deck()  # Ensure the deck is full and shuffled before the test

    card = new_deck.deal_cards(1)[0]
    empty_hand.add_card(card)

    # Assert that a card has been added to the hand from the deck
    assert len(empty_hand.rank_suit) == 1, "Hand should have one card after dealing from deck."
    # Assert that the deck has one less card
    assert len(new_deck.rank_suit) == 51, "Deck should have 51 cards after one card has been dealt."


# Fixture to create a new game
@pytest.fixture
def new_game():
    game = blackjack.BlackjackGame()
    return game


# Test that the game initializes correctly with a shuffled deck and empty hands
def test_game_initialization(new_game):
    assert len(new_game.deck.rank_suit) == 52, "Deck should have 52 cards at the start."
    assert len(new_game.player_hand.rank_suit) == 0, "Player hand should be empty at the start."
    assert len(new_game.dealer_hand.rank_suit) == 0, "Dealer hand should be empty at the start."


# Test the initial dealing of the game
def test_start_game_deals_correctly(new_game):
    new_game.start_game()
    assert len(new_game.player_hand.rank_suit) == 2, "Player should have 2 cards after starting the game."
    assert len(new_game.dealer_hand.rank_suit) == 2, "Dealer should have 2 cards after starting the game."
    assert len(
        new_game.deck.rank_suit) == 52 - 4, "Deck should have 48 cards after dealing 2 cards to player and dealer."


# Mocking the deck to control the outcome for testing the check_winner method
class MockDeck(blackjack.Deck):
    def __init__(self, cards):
        super().__init__()
        self.rank_suit = cards  # Override the shuffled deck with a predefined set of cards


# Test the check_winner method when the player wins
def test_check_winner_player_wins():
    # Mock the deck with a set of cards that ensures the player wins
    mock_cards = [('10', 'H'), ('7', 'D'), ('8', 'S'), ('5', 'C')] * 2  # Player gets 17, Dealer gets 13
    game = blackjack.BlackjackGame()
    game.deck = MockDeck(mock_cards)
    game.start_game()
    assert game.check_winner() == "Player wins!", "Player should win with a score of 17 against dealer's 13."


# Test the check_winner method when the dealer wins
def test_check_winner_dealer_wins():
    # Mock the deck with a set of cards that ensures the dealer wins
    mock_cards = [('10', 'H'), ('7', 'D'), ('8', 'S'), ('10', 'C')] * 2  # Player gets 17, Dealer gets 18
    game = blackjack.BlackjackGame()
    game.deck = MockDeck(mock_cards)
    game.start_game()
    assert game.check_winner() == "Dealer wins!", "Dealer should win with a score of 18 against player's 17."


# Test the check_winner method when it's a tie
def test_check_winner_tie():
    # Mock the deck with a set of cards that ensures a tie
    mock_cards = [('10', 'H'), ('7', 'D'), ('10', 'S'), ('7', 'C')] * 2  # Both player and dealer get 17
    game = blackjack.BlackjackGame()
    game.deck = MockDeck(mock_cards)
    game.start_game()
    assert game.check_winner() == "It's a tie!", "It should be a tie with both scores at 17."


def test_deck_unique_cards():
    deck = blackjack.Deck()
    assert len(set(deck.rank_suit)) == 52, "Deck should contain 52 unique cards"


def test_hand_clear_hand(create_hand):
    create_hand.add_card(('2', 'H'))
    create_hand.clear_hand()
    assert len(create_hand.rank_suit) == 0, "Hand should be empty after clear_hand method"


def test_immediate_blackjack(new_game):
    # Mock a deck to test immediate blackjack
    mock_cards = [('A', 'S'), ('10', 'H'), ('K', 'D'), ('3', 'C')] + [('2', 'H'), ('3', 'D')] * 24
    new_game.deck = MockDeck(mock_cards)
    new_game.start_game()
    assert new_game.player_hand.calculate_score() == 21 or new_game.dealer_hand.calculate_score() == 21, "Immediate blackjack should be detected"


def test_player_busting(new_game):
    # Mock a deck to test player busting
    mock_cards = [('10', 'H'), ('6', 'D'), ('7', 'S')] + [('2', 'H'), ('3', 'D')] * 24
    new_game.deck = MockDeck(mock_cards)
    new_game.start_game()
    new_game.player_hand.add_card(('8', 'C'))  # This should cause the player to bust
    assert new_game.player_hand.calculate_score() > 21, "Player should bust with score over 21"

# Test the dealer behavior when the player has a higher score than the dealer's 17+
def test_dealer_hits_past_seventeen():
    # Mock the deck with a set of cards where the dealer must hit past 17 to try to beat the player
    # Player gets 19, Dealer initially gets 17 but must hit to try to beat the player
    mock_cards = [('10', 'H'), ('9', 'D'), ('7', 'S'), ('10', 'C'), ('5', 'H')] + [('2', 'H'), ('3', 'D')] * 23
    game = blackjack.BlackjackGame()
    game.deck = MockDeck(mock_cards)
    game.start_game()
    game.dealer_plays()

    player_score = game.player_hand.calculate_score()
    dealer_score = game.dealer_hand.calculate_score()

    assert dealer_score >= 17 and dealer_score > player_score, "Dealer should hit past 17 to try to beat the player"
