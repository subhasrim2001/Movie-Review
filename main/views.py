from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here - main logic
#function based views

def home(request):
    allMovies = Movie.objects.all() #select * from movie
    #print(allMovies)
    context = {
        "movies": allMovies,
    }
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, 'main/index.html', context)
#detail page
def detail(request, id):
    movie = Movie.objects.get(id=id) #select * from movie where id=id
    context = {
        "movie": movie
    }
    return render(request, 'main/details.html', context)
#add movies to the 
def add_movies(request):
    if request.method == "POST":
        form = MovieForm(request.POST or None)
        #check if form is valid
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:home")
    else:
        form = MovieForm()
    return render(request, 'main/addmovies.html', {"form": form, "controller": "Add Movies"})
#edit movie
def edit_movies(request, id):
    #get movies via id
    movie = Movie.objects.get(id=id)
    #form check
    if request.method == "POST":
        form = MovieForm(request.POST or None, instance=movie)
        #check if form is valid
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect("main:detail", id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'main/addmovies.html', {"form": form, "controller": "Edit Movies"})
#delete movies
def delete_movies(request, id):
    #get the movie
    movie = Movie.objects.get(id=id)
    #delete the movie
    movie.delete()
    return redirect("main:home")