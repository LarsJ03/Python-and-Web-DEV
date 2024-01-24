from flask import Flask, render_template, request, redirect, flash, session, url_for
from API.users import Users  # Import the Users class
from API.blackjack import BlackjackGame

application = Flask(__name__)
application.secret_key = 'ISkjdSd657Sd65Sdjhjsdaowd'


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('my_account'))

    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        if Users.authenticate_user(username_or_email, password):
            session['username'] = Users.get_username_from_email(
                username_or_email) if '@' in username_or_email else username_or_email
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


def is_logged_in():
    return 'username' in session


@application.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect('/my_account')

    if request.method == 'POST':
        user_data = {
            "email": request.form['email'],
            "username": request.form['username'],
            "password": request.form['password']  # In real applications, hash this password
        }

        response, status_code = Users.create_user(user_data)

        if status_code == 201:  # Successful creation
            session['username'] = user_data['username']  # Auto login after registration
            flash('Account created and logged in successfully', 'success')
            return redirect('/')
        else:
            flash('Registration failed', 'error')
            return redirect('/register')

    return render_template('register.html')


@application.route('/my_account')
def my_account():
    if not is_logged_in():
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Render the my-account page template
    return render_template('my_account.html')


@application.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))  # Redirect to login page or home page


@application.route('/game')
def game():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('game.html')  # Page with a "Start Game" button


@application.route('/game/start', methods=['POST'])
def start_game():
    if not is_logged_in():
        return redirect(url_for('login'))
    game = BlackjackGame()
    game.start_game()
    session['player_hand'] = game.player_hand.rank_suit
    session['dealer_hand'] = game.dealer_hand.rank_suit
    session['deck'] = game.deck.rank_suit  # Store the remaining deck
    return redirect(url_for('playing'))


@application.route('/game/playing', methods=['GET', 'POST'])
def playing():
    if not is_logged_in():
        return redirect(url_for('login'))
    if 'player_hand' not in session or 'dealer_hand' not in session or 'deck' not in session:
        return redirect(url_for('game'))

    # Reconstruct game state from session
    game = BlackjackGame()
    game.player_hand.rank_suit = session['player_hand']
    game.dealer_hand.rank_suit = session['dealer_hand']
    game.deck.rank_suit = session['deck']

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'hit':
            # Player chooses to hit (get another card)
            game.player_hand.add_card(game.deck.deal_cards(1)[0])
            session['player_hand'] = game.player_hand.rank_suit
            session['deck'] = game.deck.rank_suit  # Update the deck in the session
            player_score = game.player_hand.calculate_score()
            if player_score > 21:

                # Player busts, set the game result and end the game
                session['game_result'] = "Player busts! Dealer wins!"
                return redirect(url_for('game_result'))
            elif player_score == 21:
                # Check for player blackjack or tie
                print('blackjack!')
                session['game_result'] = game.check_winner()
                return redirect(url_for('game_result'))
        elif action == 'stand':
            # Player stands, dealer plays, and check the winner
            game.check_winner()
            # Update the dealer's hand in the session
            session['dealer_hand'] = game.dealer_hand.rank_suit
            session['game_result'] = game.check_winner()
            return redirect(url_for('game_result'))

    # Convert card tuples to image paths for both player and dealer hands
    player_hand_images = [get_card_image(card) for card in session['player_hand']]
    dealer_hand_images = [get_card_image(card) for card in session['dealer_hand']]

    return render_template('playing.html', player_hand=player_hand_images, dealer_hand=dealer_hand_images)


@application.route('/game/result')
def game_result():
    if not is_logged_in():
        return redirect(url_for('login'))
    # If there is no game result in session, redirect to start page
    if 'game_result' not in session or 'player_hand' not in session or 'dealer_hand' not in session:
        return redirect(url_for('game'))

    # Retrieve the result and hands from the session
    result_game = session.pop('game_result', None)
    player_hand_tuples = session.pop('player_hand', None)
    dealer_hand_tuples = session.pop('dealer_hand', None)

    # Convert card tuples to image paths for both player and dealer hands
    player_hand_images = [get_card_image(card) for card in player_hand_tuples]
    dealer_hand_images = [get_card_image(card) for card in dealer_hand_tuples]

    # Render the result page with the winner and the card images
    return render_template('result.html', game_result=result_game, player_hand=player_hand_images,
                           dealer_hand=dealer_hand_images)


def get_card_image(card):
    rank, suit = card
    # Convert rank and suit to match file names
    suit_map = {'S': 'spades', 'H': 'hearts', 'D': 'diamonds', 'C': 'clubs'}
    rank_map = {
        '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
        '8': '8', '9': '9', '10': '10', 'J': 'jack', 'Q': 'queen',
        'K': 'king', 'A': 'ace'
    }
    file_name = f"{rank_map[rank]}_of_{suit_map[suit]}.png"  # Example: 'ace_of_spades.png'
    return url_for('static', filename=f'cards/{file_name}')


if __name__ == '__main__':
    application.run(debug=True)
