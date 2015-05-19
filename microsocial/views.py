from django.contrib.auth.decorators import login_required
from django.http import request
from django.shortcuts import redirect

@login_required()
def main(requests):
    return redirect('profile', person_id=requests.user.pk, permanent=False)
