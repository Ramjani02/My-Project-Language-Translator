from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from deep_translator import GoogleTranslator

# =========================
# LANGUAGE LIST
# =========================
LANGUAGES = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-CN': 'Chinese',
    'ar': 'Arabic',
}

# =========================
# TEMP CHAT MEMORY (for demo)
# =========================
chat_memory = []


# =========================
# AUTH VIEWS
# =========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('translate')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'app/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'app/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# TRANSLATE PAGE
# =========================
@login_required(login_url='login')
def translate_view(request):
    translated_text = ""

    if request.method == 'POST':
        text = request.POST.get('text')
        source = request.POST.get('source')
        target = request.POST.get('target')

        translated_text = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

    return render(request, 'app/translate.html', {
        'translated_text': translated_text,
        'languages': LANGUAGES
    })


# =========================
# CHAT TRANSLATOR (RAMU ↔ SOMU)
# =========================
@login_required(login_url='login')
def chat_view(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        text = request.POST.get('text')
        source = request.POST.get('source')

        # Decide target language automatically
        target = 'ta' if sender == 'A' else 'en'

        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        chat_memory.append({
            'sender': sender,
            'text': translated
        })

    return render(request, 'app/chat.html', { 
        'languages': LANGUAGES,
        'chat': chat_memory
    })
