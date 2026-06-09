from django.shortcuts import render
from .models  import journalEntry
from django .contrib.auth.decorators import login_required
 
@login_required
def entry_list(request);
    entries=journalEntry.objects.filter(user=request.user)
    return render(request,'entry_list.html',{'entries': entries})