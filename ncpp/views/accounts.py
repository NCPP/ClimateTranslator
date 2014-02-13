from ncpp.forms import UserForm
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

def user_add(request):

    # GET
    if (request.method=='GET'):
        
        # FIXME
        form = UserForm( initial={ 'first_name':'Luca', 
                                   'last_name':'Cinquini',
                                   'email':'luca.cinquini@jpl.nasa.gov',
                                   'username':'luca123',
                                   'password':'',
                                   'confirm_password:':'' }) # empty form with no data
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
            print 'Created user=%s' % user.get_full_name()
            
            # redirect to login page with special message
            message = 'Thank you for creating an account. You can now login.'
            return HttpResponseRedirect(reverse('login')+"?message=%s" % message)

        
        else:
            print "Form is invalid: %s" % form.errors
            return render_to_response('ncpp/accounts/user_form.html', {'form': form }, context_instance=RequestContext(request))

