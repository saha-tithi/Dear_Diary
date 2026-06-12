from django.shortcuts import render, redirect,get_object_or_404
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

@login_required
def edit_entry(request,id):
    entry=get_object_or_404(journalEntry,id=id,user=request.user)
    if request.method=="POST":
        entry.title=request.POST.get('title')
        entry.content=request.POST.get('content')
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


