'''
BlackJack Game using terminal

'''
import random

ranks = ["Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace"]
suits = ["Hearts", "Diamonds", "Clubs", "Spade"]
values ={"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six":6, "Seven": 7, "Eight": 8, "Nine": 9, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}


class Deck:
    '''
    Deck is list of cards
    '''
    def __init__(self):
        self.cards = []
        for i in suits:
            for j in ranks:
                self.cards.append(Card(i, j))

    def __str__(self):
        s = "The cards inside the decks are:\n"
        for i in self.cards:
            s = s + str(i) + "\n"
        return s

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()


class Card:
    '''
    Card is a single card
    '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit

    def value(self):
        return values[self.rank]

class Hand:
    '''
    Hand is the hand that holds the card
    '''
    def __init__(self):
        self.total = 0
        self.cards =[]
        self.ace = 0
        self.game_on = True

    def add_card(self, card):
        self.cards.append(card)
        self.total += card.value()
        if card.rank =='Ace':
            self.ace +=1
        
        if self.total >21 and self.ace >0:
            self.ace -=1
            self.total -=10
    
    def stop(self):
        self.game_on = False

class Player:
    '''
    Player is human player who holds the chips and the cards
    '''
    def __init__(self, hand, chips, name):
        self.hand = hand
        self.chips = chips
        self.name = name
    
    def clear_card(self):
        self.hand = Hand()

class Chips:
    '''
    Chips are the money to bet
    '''
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def set_bet(self, bet):
        self.bet = bet

    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def show_some(player, dealer):
    print('\n---------------------------')
    print(f"These are the player {player.name}'s cards:")
    print('---------------------------')
    for i in player.hand.cards:
        print(i)
    print('\n---------------------------')
    print("This is the dealer's first card:")
    print('---------------------------')
    print(dealer.cards[0])
    print()

def show_all(player, dealer):
    print('\n---------------------------')
    print(f"These are the player {player.name}'s cards:")
    print('---------------------------')
    for i in player.hand.cards:
        print(i)
    print('\n---------------------------')
    print("These are the dealer's card:")
    print('---------------------------')
    for i in dealer.cards:
        print(i)
    print()

def ask_num_of_player():
    while True:
        try:
            n = int(input("Please enter the number of players: "))
        except ValueError:
            print("Please enter an integer.")
        else:
            return n

def ask_for_bet(chips):
    while True:
        try:
            b = int(input("Please enter your bet: "))
        except ValueError:
            print("Please enter integer amount.")
            continue
        else:
            if b>chips.total:
                print(f"The amount could not be bigger your current chips {chips.total}")
                continue
            else:
                chips.bet = b
                break


def hit_or_stand():
    while True:
        p_input = input("Do you want to hit or stand? 'h' for hit and 's' for stand: ")
        if p_input not in ['h', 's']:
            print("Your input is incorrect")
            continue
        else:
            return p_input
    
def player_wins(player):
    print(player.name + " wins the game against dealer")
    player.hand.game_on=False
    player.chips.win_bet()

def dealer_wins(player):
    print("Dealer wins the game against "+ player.name)
    player.chips.lose_bet()

def player_busts(player):
    print(player.name + " busts")
    player.hand.game_on=False
    player.chips.lose_bet()

def dealer_busts(player):
    print("Dealer busts")
    player.chips.win_bet()

def player_lose(player):
    print("Dealer wins the game against "+ player.name)
    player.chips.lose_bet()

def dealer_lose(player):
    print(player.name + " wins the game against dealer")
    player.chips.win_bet()

def player_draw(player):
    print(player.name + " draws")


def ask_for_bet_from_players(players):
    for p in players:
        print("Player "+ p.name)
        ask_for_bet(p.chips)

def clear_players_card(players):
    for p in players:
        p.clear_card()

def distribute_two_cards_to_everyone(players, dealer, deck):
    for p in players:
        p.hand.add_card(deck.deal())
        p.hand.add_card(deck.deal())
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

def check_win_or_bust(player):
    if player.hand.total == 21:
        player_wins(player)
        return True
    elif player.hand.total >21:
        player_busts(player)
        return True
    else:
        return False

def start_game():
    players = []
    n = ask_num_of_player()
    for i in range(0, n):
        name = input(f"Please enter payler {i+1}'s name: ")
        players.append(Player(Hand(), Chips(), name))

    while True:
        clear_players_card(players)
        ask_for_bet_from_players(players)
        
        d = Deck()
        d.shuffle()

        dealer = Hand()

        distribute_two_cards_to_everyone(players, dealer, d)

        
        for p in players:
            print(f"This is player {p.name}'s turn")
            show_some(p, dealer)

            while True:
                if check_win_or_bust(p):
                    break
                else:
                    h = hit_or_stand()
                    if h=='h':
                        p.hand.add_card(d.deal())
                        show_some(p, dealer)
                        continue
                    if h=='s':
                        break

        active_player = list(filter(lambda p: p.hand.game_on, players))
        if len(active_player)>0:
            while True:
                dealer.add_card(d.deal())
                if dealer.total>=17:
                    break
                else:
                    continue
            for p in active_player:
                show_all(p, dealer)
            if dealer.total == 21:
                for p in active_player:
                    dealer_wins(p)
            elif dealer.total >21:
                for p in active_player:
                    dealer_busts(p)
            else:
                for p in active_player:
                    if p.hand.total > dealer.total:
                        player_wins(p)
                    elif p.hand.total < dealer.total:
                        player_lose(p)
                    else:
                        player_draw(p)

        for p in players:
            print(f"Player {p.name} chips total is {p.chips.total}")

        again = input("\nDo you want to play again? if yes, please type 'y': ")
        if again == 'y':
            continue
        else:
            break

if __name__ == '__main__':
    start_game()














