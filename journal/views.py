from django.shortcuts import render, redirect,get_object_or_404
from .models  import journalEntry, MOOD_EMOJIS
from django .contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from .forms import JournalEntryForm
from django.db.models import Q
from datetime import date
import json
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import calendar
from datetime import datetime
from django.db.models import Count
from django.utils import timezone
from .models import Profile


 
@login_required
def entry_list(request):
    query = request.GET.get('q')
    selected_date = request.GET.get('date')
    favorites=request.GET.get('favorites')
    show_favorites=request.GET.get('favorites')
    entries = journalEntry.objects.filter( user=request.user )
    if query: 
        entries = entries.filter( title__icontains=query )
    if selected_date: 
        entries = entries.filter( created_at__date=selected_date )
    if favorites:
        entries=entries.filter(is_favorite=True)
    return render( request, 'entry_list.html', { 'entries': entries, 'query': query,'selected_date': selected_date,'favorites':favorites,'show_favorites':show_favorites,'today':date.today()} )

    






@login_required
def create_entry(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST,request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('entry_list')
    else:
        form = JournalEntryForm()

    return render(request, 'create_entry.html', {'form': form})

@login_required
def edit_entry(request, id):
    entry = get_object_or_404(journalEntry,id=id,user=request.user)
    if request.method == "POST":
        entry.title = request.POST.get('title')
        entry.content = request.POST.get('content')
        entry.gratitude = request.POST.get('gratitude')
        entry.tomorrow_goal = request.POST.get('tomorrow_goal')
        entry.notes = request.POST.get('notes')
        entry.memory_song = request.POST.get('memory_song')
        entry.mood = request.POST.get('mood') 
        if request.FILES.get("image"):
         entry.image = request.FILES["image"]
        entry.save()
        return redirect('entry_list')
    return render(request,'edit_entry.html',{'entry': entry})


@login_required
def delete_entry(request, id):

    entry=get_object_or_404(journalEntry,id=id,user=request.user)
    if request.method=="POST":
        
        entry.delete()
        return redirect('entry_list')
    return render(request,'delete_entry.html',{'entry': entry})
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            print(form.errors)  # 🔥 ADD THIS

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})
'''def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form': form})'''


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)   # <-- This was missing
            return redirect('entry_list')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
def log_out(request):
    if request.method=="POST":
        logout(request)
    return redirect('login')

@login_required
def entry_detail(request, id):

    entry = get_object_or_404(
        journalEntry,
        id=id,
        user=request.user
    )

    spotify_embed_url = None

    if entry.memory_song:

        spotify_embed_url = entry.memory_song.replace(
            "open.spotify.com/track/",
            "open.spotify.com/embed/track/"
        )

        # Remove any query parameters like ?si=...
        spotify_embed_url = spotify_embed_url.split("?")[0]

    return render(
        request,
        "entry_detail.html",
        {
            "entry": entry,
            "spotify_embed_url": spotify_embed_url
        }
    )
@login_required
def toggle_favorite(request,id):
    entry=get_object_or_404(journalEntry,id=id,user=request.user)
    entry.is_favorite= not entry.is_favorite
    entry.save()
    return redirect('entry_list')

@login_required
def get_weather(request):
    if request.method == "POST":

       
        data = json.loads(request.body)
        lat = data.get("latitude")
        lon = data.get("longitude")

       
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={settings.WEATHER_API_KEY}"
        )
        res = requests.get(url)
        weather_data = res.json()

        weather = weather_data["weather"][0]["main"]
        
        
        weather_labels = {
            "Clear": "Sunny",
            "Clouds": "Cloudy",
            "Rain": "Rainy",
            "Drizzle": "Drizzling",
            "Thunderstorm": "Stormy",
            "Snow": "Snowy",
            "Mist": "Misty",
            "Fog": "Foggy",
            "Haze": "Hazy",
            "Smoke": "Smoky",
            "Dust": "Dusty",
            "Sand": "Sandy",
            "Ash": "Ashy",
            "Squall": "Windy",
            "Tornado": "Tornado",
        }

        
        weather_icons = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
            "Smoke": "🌫️",
            "Dust": "🌪️",
            "Sand": "🌪️",
            "Ash": "🌋",
            "Squall": "💨",
            "Tornado": "🌪️",
        }

        
        
        label = weather_labels.get(weather, weather)
        emoji = weather_icons.get(weather, "🌤️")

        weather_display = f"{label}{emoji}"   # 👉 Sunny☀️
       
       
        
        
        return JsonResponse({
            "weather": weather_display
        })





@login_required
def calendar_view(request):

    today = datetime.today()

    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))

    cal = calendar.monthcalendar(year, month)

    entries = journalEntry.objects.filter(
        user=request.user,
        created_at__year=year,
        created_at__month=month
    )

    entry_days = {}

    for entry in entries:

        day = entry.created_at.day

        if day not in entry_days:
            entry_days[day] = []

        entry_days[day].append(entry)

    # Previous month
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    # Next month
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    calendar_icon = "📖"
    context = {

        "calendar": cal,

        "month": calendar.month_name[month],
        "month_number": month,
        "year": year,

        "entry_days": entry_days,
        "calendar_icon": calendar_icon,

        "today_day": today.day,
        "today_month": today.month,
        "today_year": today.year,

        "prev_month": prev_month,
        "prev_year": prev_year,

        "next_month": next_month,
        "next_year": next_year,

    }

    return render(request, "calendar.html", context)


@login_required
def entries_by_date(request, year, month, day):

    entries = journalEntry.objects.filter(
        user=request.user,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day
    )

    return render(
        request,
        "entries_by_date.html",
        {
            "entries": entries,
            "selected_date": date(year, month, day),
        },
    )

@login_required
def statistics(request):

    entries = journalEntry.objects.filter(user=request.user)

    total_entries = entries.count()

    favorites = entries.filter(is_favorite=True).count()

    current_month = timezone.now().month
    current_year = timezone.now().year

    this_month = entries.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).count()

    mood_stats = (
        entries
        .values("mood")
        .annotate(total=Count("mood"))
        .order_by("-total")
    )

    most_used_mood = mood_stats[0] if mood_stats else None
    if most_used_mood:
        most_used_mood["emoji"] = MOOD_EMOJIS.get(
        most_used_mood["mood"],
        "😐")
    recent_entries = entries.order_by("-created_at")[:7]
    recent_entries = list(reversed(recent_entries))

    mood_values = {
    "angry": 1,
    "sad": 2,
    "tired": 3,
    "neutral": 4,
    "calm": 5,
    "excited": 6,
    "happy": 7,}

    chart_labels = []
    chart_data = []
    chart_emojis = []

    for entry in recent_entries:

       chart_labels.append(entry.created_at.strftime("%d"))

       chart_data.append(mood_values.get(entry.mood, 4))
       chart_emojis.append(entry.mood_emoji)
    

    context = {

        "total_entries": total_entries,
        "favorites": favorites,
        "this_month": this_month,
        "most_used_mood": most_used_mood,
       
        "chart_labels": chart_labels,
        "chart_data": chart_data,
        "chart_emojis": chart_emojis,
        

    }

    return render( request,"statistics.html",context)

@login_required
def change_theme(request, theme):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    profile.theme = theme
    profile.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))