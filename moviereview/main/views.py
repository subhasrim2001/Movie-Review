from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg
# Create your views here - main logic
#function based views

def home(request):
    query = request.GET.get("title")
    allMovies = None
    if query:
        allMovies = Movie.objects.filter(name__icontains=query)
    else:
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
    reviews = Review.objects.filter(movie=id).order_by("-comment")
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)
   
    context = {
        "movie": movie,
        "reviews": reviews,
        "average": average
    }
    return render(request, 'main/details.html', context)
#add movies to the 
def add_movies(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
        #if not admin
        else:
            return redirect("main:home")
    #if not auth - login
    else:
        return redirect("accounts:login")
#edit movie
def edit_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
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
         #if not admin
        else:
            return redirect("main:home")
    #if not auth - login
    else:
        return redirect("accounts:login")
#delete movies
def delete_movies(request, id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            #get the movie
            movie = Movie.objects.get(id=id)
            #delete the movie
            movie.delete()
            return redirect("main:home")
             #if not admin
        else:
            return redirect("main:home")
    #if not auth - login
    else:
        return redirect("accounts:login")
#add reviews
def add_review(request, id):
    if request.user.is_authenticated:
        movie = Movie.objects.get(id=id)
        if request.method == "POST":
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST["comment"]
                data.rating = request.POST["rating"]
                data.user = request.user
                data.movie = movie
                data.save()
                return redirect("main:detail", id)
        else:
            form = ReviewForm()
        return render(request, 'main/details.html', {"form": form})
    else:
        return redirect("accounts:login")
#edit reviews
def edit_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        #movie
        movie = Movie.objects.get(id=movie_id)
        #review
        review = Review.objects.get(movie=movie, id=review_id)
        #check if review is made by logged in user
        if request.user == review.user:
            #grant permission to edit
            if request.method == "POST":
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = "Out of range. Please select rating from 0 to 10."
                        return render(request, 'main/editreview.html', {"error" : error, "form": form})
                    else:
                        data.save()
                        return redirect("main:detail", movie_id)
            else:
                form = ReviewForm(instance=review)
            return render(request, 'main/editreview.html', {"form": form})
        else:
            return redirect("main:detail", movie_id)
    else:
        return redirect("accounts:login")
#delete reviews
def delete_review(request, movie_id, review_id):
    if request.user.is_authenticated:
        #movie
        movie = Movie.objects.get(id=movie_id)
        #review
        review = Review.objects.get(movie=movie, id=review_id)
        #check if review is made by logged in user
        if request.user == review.user:
            #grant permission to delete review
            review.delete()
        return redirect("main:detail", movie_id)
    else:
        return redirect("accounts:login")

