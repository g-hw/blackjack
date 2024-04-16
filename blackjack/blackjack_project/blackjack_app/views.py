from django.shortcuts import render
from .blackjack_logic import BlackjackGame

def index(request):
    return render(request, 'index.html')

def start_game(request):
    game = BlackjackGame()
    game.start()
    request.session['game'] = game.to_dict()

    return render(request, 'play.html', game.to_dict())

def draw_card(request):
    game_data = request.session.get('game')
    if game_data:
        game = BlackjackGame().from_dict(game_data)
        game.draw_cards()
        request.session['game'] = game.to_dict()

        return render(request, 'play.html', game.to_dict())

    
def stand(request):
    game_data = request.session.get('game')
    if game_data:
        game = BlackjackGame().from_dict(game_data)
        game.end_game()
        request.session['game'] = game.to_dict()

        return render(request, 'play.html', game.to_dict())


def play_again(request):
    game_data = request.session.get('game')
    if game_data:
        game = BlackjackGame().from_dict(game_data)
        game.play_again()
        request.session['game'] = game.to_dict()

        return render(request, 'play.html', game.to_dict())
