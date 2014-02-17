from ncpp.forms import UserForm, UsernameReminderForm
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from ncpp.notification import notify, sendEmail
from django.contrib.auth.models import User

# view that handles user registration
def user_add(request):

    # GET
    if (request.method=='GET'):
        
        # FIXME
        #form = UserForm( initial={ 'first_name':'Test', 
        #                           'last_name':'User',
        #                           'email':'test.user@test.com',
        #                           'username':'Tester123',
        #                           'password':'',
        #                           'confirm_password:':'' }) 
        form = UserForm() # empty form with no data
        return render_to_response('ncpp/accounts/user_form.html', {'form': form }, context_instance=RequestContext(request))
        
    # POST
    else:
        
        form = UserForm(request.POST) # form with bounded data
        
        if form.is_valid():
            
            # create a user from the form but don't save it to the database yet because the password is not encoded
            user = form.save(commit=False)
            # must reset the password through the special method that encodes it correctly
            user.set_password(form.cleaned_data['password'])
            # save user to database
            user.save()
            
            # subscription to mailing list ?
            subscribed = form.cleaned_data['subscribed']
            
            # notify site administrators
            notifyAdminsOfUserRegistration(user, subscribed)
            
            
            # redirect to login page with special message
            message = 'Thank you for creating an account. You can now login.'
            return HttpResponseRedirect(reverse('login')+"?message=%s" % message)
        
        else:
            print "Form is invalid: %s" % form.errors
            return render_to_response('ncpp/accounts/user_form.html', {'form': form }, context_instance=RequestContext(request))
        
def username_reminder(request):
    
    if (request.method=='GET'):
        form = UsernameReminderForm()
        return render_to_response('ncpp/accounts/username_reminder.html', {'form':form }, context_instance=RequestContext(request))
    
    else:
        form = UsernameReminderForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            
            # look up username
            users = User.objects.filter(email__iexact=email)
            
            if len(users)>0:
                
                # send email with username(s) to user
                subject = "Username Reminder"
                message = ""
                for user in users:
                    message +=  "Your username is: %s\n"  % user.username
                notify(user, subject, message)

                # redirect to login page with special message
                message = 'Your username has been emailed to the address you provided. Please check your email box.'
                return HttpResponseRedirect(reverse('login')+"?message=%s" % message)

            # user not found
            else:            
                return render_to_response('ncpp/accounts/username_reminder.html', 
                                          {'form':form, 'message':'This email address cannot be found' }, context_instance=RequestContext(request))
            
        else:
            print "Form is invalid: %s" % form.errors
            return render_to_response('ncpp/accounts/username_reminder.html', {'form':form }, context_instance=RequestContext(request))

# function to notify the site administrators of a new user registration
def notifyAdminsOfUserRegistration(user, subscribed):
    
    subject = 'New User Registration'
    message = 'User %s has created a new account' % user.get_full_name()   
    
    # user attributes
    message += "\nFirst Name: %s" % user.first_name
    message += "\nLast Name: %s" % user.last_name
    message += "\nUser Name: %s" % user.username
    message += "\nEmail: %s" % user.email
    message += "\nSubscribe to OCG email list? %s" % subscribed
    
    for admin in getSiteAdministrators():
        notify(admin, subject, message)

# function to return the site administrators (aka web masters) for this site
def getSiteAdministrators():
    return User.objects.filter(is_staff=True)
