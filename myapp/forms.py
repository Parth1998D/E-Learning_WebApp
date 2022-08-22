from django import forms
from myapp.models import Order, Student, PasswordReset


class InterestForm(forms.Form):
    CHOICES = [(1, 'Yes'),
               (0, 'No')]

    interested = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    levels = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Additional Comments")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['course', 'levels', 'order_date']
        widgets = {
            'order_date': forms.SelectDateWidget
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password', 'school',
                  'city', 'interested_in', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'interested_in': forms.CheckboxSelectMultiple,
        }


class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = PasswordReset
        fields = ('username',)
        widget = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
