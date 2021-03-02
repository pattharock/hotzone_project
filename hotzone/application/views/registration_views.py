from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from ..forms import CreateUserForm

def registerPage(request):
  form = CreateUserForm()

  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()

      return redirect('application:login_page')
  
  context = {'form' : form}
  return render(request, 'register.html', context)