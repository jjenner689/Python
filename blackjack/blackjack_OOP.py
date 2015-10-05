'''

BlackJack Game
'''

import random

class Card:

    SUITS = ('c','s','h','d')
    RANKS = ('2','3','4','5','6','7','8','9','10','J','Q','K','A')
    SCORES = {'2': 2, '3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10,'A':11}
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.score = self.calc_score()

    def calc_score(self):
        return Card.SCORES[self.rank]

    def __str__(self):
        return '%s%s' % (self.rank, self.suit)

class Hand:

    def __init__(self):
        self.cards = []

    def give_card(self):
        card = self.cards.pop()
        return card

    def receive_card(self, card):
        self.cards.append(card)

    def ace_count(self):
        count = 0
        for card in self.cards:
            if card.rank == 'A':
                count += 1
        return count

    def total(self):
        total = self.account_for_ace(sum([x.calc_score() for x in self.cards]))

        if total > 21:
            return None
        else:
            return total

    def account_for_ace(self, total):
        for ace in range(self.ace_count()):
            if total > 21:
                total -= 10
        return total


    def discard_hand(self):
        self.cards = []

    def __str__(self):
        rep = ''
        for card in self.cards:
            rep += '%s  ' % str(card)
        return rep

class Deck(Hand):

    def __init__(self):
        self.populate()
        self.shuffle()
   
    def populate(self):

        self.cards = [Card(suit,rank) for suit in Card.SUITS for rank in Card.RANKS]
        
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, player):
        for i in range(2):
            player.hand.receive_card(self.give_card())


class Player:

    def __init__(self, name):
        self.hand = Hand()
        self.name = name.title()

    def show_hand(self):
        return str(self.hand)

    def take_turn(self):
        answer = ''
        options = ('s', 't')
        while answer not in options:
            answer = raw_input('\nPress s to stick or t to twist > ')
        return answer

    def is_bust(self):
        return self.hand.total() == None

class Dealer(Player):

    def __init__(self):
        self.hand = Hand()
        self.name = 'Dealer'

    def take_turn(self):
        total = self.hand.total()
        if total >= 17:
            return 's'
        else:
            return 't'

class Game:

    def __init__(self):

        self.deck = Deck()

    def run(self):
        self.set_players()
        self.interface()

    def set_players(self):

        num = ''
        while num not in [str(x) for x in range(9)]:
            num = raw_input('Enter the number of players (1-8) > ')
        self.players = [Player(raw_input('Enter the name for player %s > ' % (i+1))) for i in range(int(num))]
        self.dealer = Dealer()
        

    def interface(self):
        answer = ''
        options = {'q': self.quit, 'p': self.play}
        while answer not in options:
            answer = raw_input('\nPress q to quit, or p to play > ')
        options[answer]()

    def play(self):
        self.check_deck()
        self.do_rounds()
        self.interface()

    def do_rounds(self):
        for player in self.players:
            players = [player, self.dealer]
            self.deal(players)
            self.round(players)
            self.compute_winner(players)
            self.clear_hands(players)

    def clear_hands(self, players):
        for player in players:
            player.hand.discard_hand()

    def round(self, players):
        options = {'s': self.stick, 't': self.twist}
        for player in players:
            answer = ''

            while answer != 's':
                self.display_hands(player)
                answer = player.take_turn()
                options[answer](player)

                # print player.hand.total()

                if player.is_bust():
                    self.display_hands(player)
                    print '\nBust!!!!'
                    return

    def compute_winner(self, players):
        scores = [[player.hand.total(), player.name] for player in players]
        scores.sort()
        winners = self.find_winner(scores)
        self.print_scores(scores, winners)
        
    def print_scores(self, scores, winners):
        print ''
        for score in scores:
            if score[0] == None:
                score[0] = 'BUST'
            print '%s   %s' % (score[1], score[0])
        if len(winners) == 1:
            print '\n%s wins!!!!!' % winners[0]
        else:
            print '\n%s tie!!!!!!' % ', '.join(winners)

    def find_winner(self, scores):
        max_ = max([score for score in scores])
        winners = [score[1] for score in scores if score[0] == max_[0]]
        return winners

    def stick(self, player):
        print '\n%s sticks...' % player.name

    def twist(self, player):
        print '\n%s twists...' % player.name
        player.hand.receive_card(self.deck.give_card())

    def display_hands(self, player):
        print '\n%s: %s' % (player.name, player.show_hand())

    def deal(self, players):
        for player in players:
            self.deck.deal(player)

    def check_deck(self):
        if len(self.deck.cards) < 10:
            self.deck.populate()
            self.deck.shuffle()

    def quit(self):
        print '\nBye bye.......'



game = Game()
game.run()
















    
