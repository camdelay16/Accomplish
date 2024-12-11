from django import forms
from .models import Subtask

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['subtask_name', 'due_date', 'priority', 'note']
        widgets = {
            'due_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }
