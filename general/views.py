from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from registration.backends.default.views import RegistrationView


@login_required
def dashboard(request):
    
    context = {
        "is_dashboard": True,
        "active_menu": "dashboard",
        "title": "Dashboard",      
    }

    return render(request, "base.html", context)


class SkipEmailVerificationRegistrationView(RegistrationView):

    def register(self, form):
        user = form.save(commit=False)
        user.is_active = True  # Set the user as active without email verification
        user.save()

        return user

