from django.shortcuts import render, redirect
from .models import Cat
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form
        })

def add_feeding(request, cat_id):
    # grab the form data
    form = FeedingForm(request.POST)
    #check if the form submitted is valid
    if form.is_valid():
        new_feeding = form.save(commit=False)

        # if the form is good, then we would create new record in our feeding table
        new_feeding.cat_id = cat_id
        new_feeding.save()

    #if its bad, just send them back to the same page
    #if its good , send them to the cat detail page
    return redirect('cat-detail', cat_id=cat_id)


# CBVs
class CatCreate(CreateView):
    model = Cat
    fields = '__all__'
    success_url = '/cats/'

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'