from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from django.contrib.auth.decorators import login_required #For Django to require that we are login to access: def new(request)
from .forms import NewItemForm

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