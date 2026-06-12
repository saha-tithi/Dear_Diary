from django.shortcuts import render, redirect
from .models  import journalEntry
from django .contrib.auth.decorators import login_required
 
@login_required
def entry_list(request):
    entries=journalEntry.objects.filter(user=request.user)
    return render(request,'entry_list.html',{'entries': entries})

def create_entry(request):
    if request.method == "POST":
        title=request.POST.get('title')
        content=request.POST.get('content')
        
        journalEntry.objects.create(user=request.user,title=title,content=content)
        return redirect('entry_list')
    return render(request,'create_entry.html')

