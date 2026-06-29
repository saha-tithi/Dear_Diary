from django.shortcuts import render, redirect,get_object_or_404
from .models  import journalEntry
from django .contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from .forms import JournalEntryForm
from django.db.models import Q
from datetime import date



 
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

    

def create_entry(request):
    if request.method == "POST":
        form = JournalEntryForm(request.POST)
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
        entry.mood = request.POST.get('mood') 
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
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form': form})


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

def entry_detail(request,id):
    entry=get_object_or_404(journalEntry,id=id,user=request.user)
    return render(request,'entry_detail.html',{'entry':entry})

@login_required
def toggle_favorite(request,id):
    entry=get_object_or_404(journalEntry,id=id,user=request.user)
    entry.is_favorite= not entry.is_favorite
    entry.save()
    return redirect('entry_list')