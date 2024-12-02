from django.shortcuts import render, redirect
from .models import Cat, Toy
from .forms import FeedingForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic import DetailView, ListView

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cat_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {'cats': cats})

def cat_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    # toys = Toy.objects.all()
    toys_cat_doesnt_have = Toy.objects.exclude(id__in = cat.toys.all().values_list('id'))
    feeding_form = FeedingForm()
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'toys': toys_cat_doesnt_have
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
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/cats/'

class CatUpdate(UpdateView):
    model = Cat
    # Let's disallow the renaming of a cat by excluding the name field!
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'

# TOYS
class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyDetail(DetailView):
    model = Toy

class ToyList(ListView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'


    # Note that you can pass a toy's id instead of the whole object
def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', cat_id=cat_id)

def remove_toy(request, cat_id, toy_id):
    # Look up the cat
    cat = Cat.objects.get(id=cat_id)
    # Look up the toy
    toy = Toy.objects.get(id=toy_id)
    # Remove the toy from the cat
    cat.toys.remove(toy)
    return redirect('cat-detail', cat_id=cat.id)