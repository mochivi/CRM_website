from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, UserGroup

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="", 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }
        ), 
    )
    first_name = forms.CharField(
        label="", 
         widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }
        )
    )
    last_name = forms.CharField(
        label="", 
        max_length=50, 
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "First Name",
            "class": "form-control"
            }),
        label = ""
    )
    last_name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Last Name",
            "class": "form-control"
            }),
        label = ""
    )
    email = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Email",
            "class": "form-control"
            }),
        label = ""
    )
    phone = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Phone",
            "class": "form-control"
            }),
        label = ""
    )
    adress = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Address",
            "class": "form-control"
            }),
        label = ""
    )
    city = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "City",
            "class": "form-control"
            }),
        label = ""
    )
    state = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "State",
            "class": "form-control"
            }),
        label = ""
    )
    country = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Country",
            "class": "form-control"
            }),
        label = ""
    )
    zipcode = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Zipcode",
            "class": "form-control"
            }),
        label = ""
    )

    class Meta:
        model = Record
        exclude = ("user",)

class AddGroupForm(forms.ModelForm):
    name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(attrs={
            "placeholder": "Group Name",
            "class": "form-control",
            "max_length": "50"
            }),
        label = "Name"
    )
    description = forms.CharField(
        required=True, 
        widget=forms.widgets.Textarea(attrs={
            "placeholder": "Description",
            "class": "form-control",
            "max_length": "255"
            }),
        label = "Description"
    )
    members = forms.CharField(
        required=False,
        widget = forms.SelectMultiple(attrs={
            'class': 'form-control',
            'multiple': 'multiple'
            }),
        label="Members"
    )
    records = forms.CharField(
        required=False,
        widget = forms.SelectMultiple(attrs={
            'class': 'form-control',
            'multiple': 'multiple'
            }),
        label="Records"
    )
    admin = forms.CharField(
        required=False,
        widget = forms.SelectMultiple(attrs={
            'class': 'form-control',
            'multiple': 'multiple'
            }),
        label="Admin"
    )
    visibility = forms.ChoiceField(
        required=True,
        choices=['Public', 'Private'],
        label="Visibility"
    )

    def __init__(self, *args, **kwargs): #curent_user to arguments maybe
        self.user = kwargs.pop("user", None)
        
        super().__init__(*args, **kwargs)
        
        self.fields['visibility'].choices = self.Meta.model.VISIBILITY_CHOICES
        
        self.fields['members'].queryset = User.objects.all()
        self.fields['admin'].queryset = User.objects.all()
        
        if self.user is not None:
            self.fields['records'].queryset = Record.objects.filter(creator=self.user)
        
        # self.instance.admin = current_user
        # self.instance.members.set([current_user])
    
    def save(self, commit=True):
        user_group = super().save(commit=False)

        if self.user:
            if not user_group.admin:
                user_group.admin = self.user

            if commit:
                user_group.save()
            
            if not user_group.members.exists():
                user_group.members.set([self.user])
        
        return user_group

    def clean(self):
        cd = super().clean()

        members = cd.get("members")
        admin = cd.get("admin")

        if not members:
            members = [self.user]
        if not admin:
            admin = self.user

        cd["members"] = members
        cd["admin"] = admin
        
        return cd


    class Meta:
        model = UserGroup
        fields = '__all__'