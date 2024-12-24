from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import re  

def home(request):
    return render(request, 'game/home.html')

from .models import GameSession
from django.utils.timezone import now

from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import GameSession

import random
import copy


a = [0, 2, 4]
b = [2, 4]

def init():
    
    table_x = []
    table = []
    for j in range(4):
        for i in range(4):
            x = random.choice(a)
            table_x.append(x)
        table.append(table_x)
        table_x = []
    return table

def scan(table, k):    
    coord = []
    for i in range(4):
        for j in range(4):
            if table[i][j] == k:
                coord.append([i, j])
    return coord


def random_generate(table):
    coord = scan(table, 0)
    i = random.choice(coord)
    nbr = random.choice(b)
    table[i[0]][i[1]] = nbr
    return table


def compare_list(list1, list2):
    for i in range(4):
        for j in range(4):
            if list1[i][j] != list2[i][j]:
                return False
    return True


def lose(table):
    temp = copy.deepcopy(table)
    scan0 = scan(temp, 0)
    table1 = right(temp)
    table1 = left(temp)
    table1 = top(temp)
    table1 = bottom(temp)
    scan1 = compare_list(temp, table1)
    if scan1 and len(scan0) == 0:
        return "lose"
    return "non_lose"


def right(table):
    for x in range(4):
        for i in range(4):
            for j in reversed(range(1, 4)):
                if table[i][j] == 0:
                    table[i][j] = table[i][j - 1]
                    table[i][j - 1] = 0
    for i in range(4):
        init_range = 4
        for j in reversed(range(1, init_range)):
            if table[i][j] == table[i][j - 1]:
                init_range = j
                table[i][j] = table[i][j - 1] * 2
                table[i][j - 1] = 0
    for x in range(4):
        for i in range(4):
            for j in reversed(range(1, 4)):
                if table[i][j] == 0:
                    table[i][j] = table[i][j - 1]
                    table[i][j - 1] = 0
    return table

def left(table):
    for x in range(4):
        for i in range(4):
            for j in range(3):
                if table[i][j] == 0:
                    table[i][j] = table[i][j + 1]
                    table[i][j + 1] = 0
    for i in range(4):
        init_range = 0
        for j in range(init_range, 3):
            if table[i][j] == table[i][j + 1]:
                init_range = j + 1
                table[i][j] = table[i][j + 1] * 2
                table[i][j + 1] = 0
    for x in range(4):
        for i in range(4):
            for j in range(3):
                if table[i][j] == 0:
                    table[i][j] = table[i][j + 1]
                    table[i][j + 1] = 0
    return table

def top(table):
 
    init_range = 0
    for k in range(4):
        for x in range(4):
            for i in range(3):
                for j in range(4):
                    if table[i][j] == 0:
                        table[i][j] = table[i + 1][j]
                        table[i + 1][j] = 0
        for x in range(4):
            for i in range(init_range, 3):
                for j in range(4):
                    if table[i][j] == table[i + 1][j]:
                        init_range = i + 1
                        table[i][j] = table[i + 1][j] * 2
                        table[i + 1][j] = 0
    return table

def bottom(table):
 
    init_range = 4
    for k in range(4):
        for x in range(4):
            for i in reversed(range(1, 4)):
                for j in range(4):
                    if table[i][j] == 0:
                        table[i][j] = table[i - 1][j]
                        table[i - 1][j] = 0
        for x in range(4):
            for i in reversed(range(1, init_range)):
                for j in range(4):
                    if table[i][j] == table[i - 1][j]:
                        init_range = i
                        table[i][j] = table[i - 1][j] * 2
                        table[i - 1][j] = 0
    return table


def game_view(request):
    
    if 'board' not in request.session:
        request.session['board'] = init()
        request.session['score'] = 0
        request.session['best_score'] = 0
        request.session['has_won'] = False

    board = request.session['board']
    score = request.session['score']
    best_score = request.session['best_score']
    has_won = request.session.get('has_won', False)
    message = ""

    if request.method == 'POST':
        if 'restart' in request.POST:
          
            request.session['board'] = init()
            request.session['score'] = 0
            request.session['has_won'] = False
            return render(request, 'game/index.html', {
                'board': request.session['board'],
                'score': 0,
                'best_score': best_score,
                'message': ""
            })

       
        move = request.POST.get('move')
        old_board = [row[:] for row in board]

        if move == 'right':
            board = right(board)
        elif move == 'left':
            board = left(board)
        elif move == 'top':
            board = top(board)
        elif move == 'bottom':
            board = bottom(board)

        if old_board != board:
            board = random_generate(board)
            score = sum(sum(row) for row in board)
            if score > best_score:
                best_score = score
                request.session['best_score'] = best_score
            request.session['score'] = score
        else:
            message = "Invalid move!"

        if not has_won and any(2048 in row for row in board):
            message = "You Win!"
            request.session['has_won'] = True
            if request.user.is_authenticated:
                GameSession.objects.create(user=request.user, timestamp=now(), score=score, best_score=best_score, status="win")

  
        if lose(board) == "lose" and message != "You Win!":
            message = "Game Over!"
            if request.user.is_authenticated:
                GameSession.objects.create(user=request.user, timestamp=now(), score=score, best_score=best_score, status="loss")

        request.session['board'] = board


    return render(request, 'game/index.html', {
        'board': board,
        'score': score,
        'best_score': best_score,
        'message': message
    })

from django.contrib.auth.decorators import login_required
from .models import GameSession

@login_required
def dashboard_view(request):
    game_sessions = GameSession.objects.filter(user=request.user).order_by('-timestamp')
    game_count = game_sessions.count()
    return render(request, 'game/dashboard.html', {
        'game_sessions': game_sessions,
        'game_count': game_count
    })
    
    
from django.shortcuts import render
from .models import GameSession
from django.db.models import Max

def leaderboard_view(request):
   
    search_query = request.GET.get('search', '')
    
   
    sort_order = request.GET.get('sort', 'desc')  

   
    leaderboard = GameSession.objects.values('user__username') \
                                      .annotate(best_score=Max('best_score')) \
                                      .order_by('-best_score' if sort_order == 'desc' else 'best_score')

    if search_query:
       
        leaderboard = leaderboard.filter(user__username__icontains=search_query)

    leaderboard_data = []
    rank = 1
    for entry in leaderboard:
        game_session = GameSession.objects.filter(
            user__username=entry['user__username'], 
            best_score=entry['best_score']
        ).first()

        leaderboard_data.append({
            'rank': rank,
            'username': entry['user__username'],
            'best_score': entry['best_score'],
            'timestamp': game_session.timestamp if game_session else None
        })
        rank += 1

    return render(request, 'game/leaderboard.html', {
        'leaderboard_data': leaderboard_data,
        'search_query': search_query,
        'sort_order': sort_order
    })


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if not username or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('register')
        
        if len(username) < 3:
            messages.error(request, "Username must be at least 3 characters long.")
            return redirect('register')
        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Invalid email format.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, 'game/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        
        if not username or not password:
            messages.error(request, "Both username and password are required.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'game/login.html')

@login_required
def profile_view(request):
    return render(request, 'game/profile.html')

@login_required
def update_view(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()

        if not username or not email:
            messages.error(request, "All fields are required.")
            return redirect('update')

        user = request.user
        if user.username != username and User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('update')

        if user.email != email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('update')
        
        user.username = username
        user.email = email
        user.save()
        
        messages.success(request, "Account details updated successfully.")
        return redirect('profile')

    return render(request, 'game/update.html')

@login_required
def delete_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Account deleted successfully.")
        return redirect('home')
    return render(request, 'game/delete.html')

def logout_view(request):
    logout(request)
    return redirect('home')
