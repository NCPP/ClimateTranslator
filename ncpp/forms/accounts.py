from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import CharField, BooleanField, PasswordInput
import re

# list of invalid characters in text fields
INVALID_CHARS = "[<>&#%{}\[\]\$]"
INVALID_USERNAME_CHARS = "[^a-zA-Z0-9_\-\+\@\.]"

class UserForm(ModelForm):
    
    # override User form fields to make them required
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    username = CharField(required=True)
    email = CharField(required=True)
    password = CharField(required=True, widget=PasswordInput())
    
    # additional fields not in User
    confirm_password = CharField(required=True, widget=PasswordInput())
    subscribed = BooleanField(required=False)
    
    class Meta:
        model = User
        # define fields to be used, so to exclude last_login and date_joined
        fields = ('first_name', 'last_name', 'username', 'email', 'password',
                  'subscribed','confirm_password')
        
    # override form clean() method to execute custom validation on fields, 
    # including combined validation on multiple fields
    def clean(self):
        
        # invoke superclass cleaning method
        super(UserForm, self).clean()        
        cleaned_data = self.cleaned_data
                        
        # validate 'password', 'confirm_password' fields
        validate_password(self)
        
        # validate 'username' field
        validate_username(self)
                
        # validate all other fields against injection attacks
        for field in ['first_name','last_name', 'email']: 
            try:
                validate_field(self, field, cleaned_data[field])
            except KeyError: # field not set (validation occurs later)
                pass
        
        return cleaned_data

# method to validate the fields 'password" and 'confirm_password'
def validate_password(form):
    
        cleaned_data = form.cleaned_data
        
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password:
            if len(password) < 6:
                form._errors["password"] = form.error_class(["'Password' must contain at least 6 characters."])
            if password != confirm_password:
                form._errors["confirm_password"] = form.error_class(["'Password' and 'Confirm Password' must match."])

# method to validate the field 'username'
def validate_username(form):
    
        cleaned_data = form.cleaned_data
    
        username = cleaned_data.get("username")
        if username:
            if len(username) < 5:
                form._errors["username"] = form.error_class(["'Username' must contain at least 5 characters."])
            elif len(username) >30:
                form._errors["username"] = form.error_class(["'Username' must not exceed 30 characters."])
            elif re.search(INVALID_USERNAME_CHARS, username):
                form._errors["username"] = form.error_class(["'Username' can only contain letters, digits and @/./+/-/_"])
                
            # perform case-insensitive lookup of username, compare with id from form instance
            if User.objects.filter(username__iexact=username).exists():
                form._errors["username"] = form.error_class(["Username already taken in database"])
                
# method to validate a generic field against bad characters
def validate_field(form, field_name, field_value):
    
    if field_value:
        if re.search(INVALID_CHARS, field_value):
            form._errors[field_name] = form.error_class(["'%s' contains invalid characters." % field_name])