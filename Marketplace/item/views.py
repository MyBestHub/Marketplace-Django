from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.contrib.auth.decorators import login_required #For Django to require that we are login to access: def new(request)
from .forms import NewItemForm, EditItemForm
from django.db.models import Q  #Q make it easier to search in multiple fields

def items(request):      #1st step to creating the browser search 
    query= request.GET.get('query', '')
    category_id = request.GET.get('category', 0) #when I click on the categories under the search bar, it will direct me to the specified category
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items= items.filter(Q(name__icontains=query) | Q(description__icontains=query)) #if the name in search bar countain the query for name or description ,it will process.
        
    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:5]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required   #redirected to login page, if you visit this without being logged in
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
        
    else:
        form = NewItemForm()

    return render(request,'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')

def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
        
    else:
        form = EditItemForm(instance=item)      #put an instance inside so form isnt empty when we visit the page

    return render(request,'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })
