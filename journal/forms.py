from django import forms
from .models import journalEntry

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = journalEntry
        fields = ['title', 'content','gratitude', 'tomorrow_goal','notes']