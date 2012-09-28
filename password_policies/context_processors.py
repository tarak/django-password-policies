from password_policies.models import PasswordHistory


def password_status(request):
    """
Adds a variable determining the state of a user's password
to the context if the user has authenticated:

* ``password_change_required``
    Determines if the user needs to change his/her password.

    Set to ``True`` if the user has to change his/her password,
    ``False`` otherwise.

"""
    d = {}
    if request.user.is_authenticated():
        if not '_password_policies_change_required' in request.session:
            r = PasswordHistory.objects.change_required(request.user)
        else:
            r = request.session['_password_policies_change_required']
        d['password_change_required'] = r
    return d
