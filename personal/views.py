from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_screen_view(request):
	context = {}
	return render(request, "personal/home.html", context)

