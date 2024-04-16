import random

RANK = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
SUIT = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
PLAYER = 'Player'
DEALER = 'Dealer'

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self._get_value(rank)
    
    def to_dict(self):
        return {"rank": self.rank, "suit": self.suit}

    def _get_value(self, rank):
        if rank in ['Jack', 'Queen', 'King']:
            return 10
        elif rank == 'Ace':
            return 11
        else:
            return int(rank)

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()
    
    def to_dict(self):
        return [card.to_dict() for card in self.cards]
    
    @classmethod
    def from_dict(cls, data):
        deck = cls()
        deck.cards = [Card(rank=card_data['rank'], suit=card_data['suit']) for card_data in data]
        return deck

    def reset(self):
        self.cards = [Card(rank, suit) for suit in SUIT for rank in RANK]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def to_dict(self):
        return {"hand": [hand.to_dict() for hand in self.hand], "value": self.get_hand_value()}
    
    @classmethod
    def from_dict(cls, data, name):
        player = cls(name)
        player.hand = [Card(rank=card_data['rank'], suit=card_data['suit']) for card_data in data["hand"]]
        return player

    def add_to_hand(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        value = sum(card.value for card in self.hand)
        for card in self.hand:
            if card.rank == 'Ace' and value > 21:
                value -= 10
        return value
    
    def reset_hand(self):
        self.hand = []


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player(PLAYER)
        self.dealer = Player(DEALER)
        self.result = None
        self.is_player_done = False
        self.score = 0

    def to_dict(self):
        return {
            'deck': self.deck.to_dict(),
            'player': self.player.to_dict(),
            'dealer': self.dealer.to_dict(),
            'result': self.result,
            'is_player_done': self.is_player_done,
            'score': self.score
        }
    
    @classmethod
    def from_dict(cls, data):
        game = cls()
        game.deck = Deck.from_dict(data["deck"])
        game.player = Player.from_dict(data["player"], PLAYER)
        game.dealer = Player.from_dict(data["dealer"], DEALER)
        game.score = data["score"]
        return game

    def start(self):
        self.deal_hands()
        self.check_blackjack()

    def play_again(self):
        self.is_player_done = False
        self.player.reset_hand()
        self.dealer.reset_hand()
        if len(self.deck.cards) < 15:
            self.deck.reset()

        self.deal_hands()
        self.check_blackjack()

    def deal_hands(self):
        self.player.add_to_hand(self.deck.draw())
        self.dealer.add_to_hand(self.deck.draw())
        self.player.add_to_hand(self.deck.draw())
        self.dealer.add_to_hand(self.deck.draw())

    def check_blackjack(self):
        if self.player.get_hand_value() == 21:
            self.is_player_done = True
            self.result = "Blackjack!"
            self.score += 15

    def draw_cards(self):
        self.player.add_to_hand(self.deck.draw())
        if self.player.get_hand_value() > 21:
            self.is_player_done = True
            self.result = "You bust!"
            self.score -= 10

    def end_game(self):
        self.is_player_done = True
        while self.dealer.get_hand_value() < 17:
            self.dealer.add_to_hand(self.deck.draw())

        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        if player_value > 21 or (dealer_value <= 21 and dealer_value > player_value):
            self.result = "Dealer wins!"
            self.score -= 10
        elif dealer_value > 21 or player_value > dealer_value:
            self.result = "Player wins!"
            self.score += 10
        else:
            self.result = "It's a tie!"

        
