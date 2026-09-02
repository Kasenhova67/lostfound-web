from django.shortcuts import render, redirect
from lost.models import itemlost, itemfound
from users.models import itemfoundfull, itemlostfull
from .forms import lostform, foundform
from users.forms import lostfullform, foundfullform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import Profile
from django.core.paginator import Paginator
from django.db.models import Q


def lost_view(request, *args, **kwargs):
    queryset = itemlost.objects.all()
    
    # Поиск
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(product_title__icontains=query) |
            Q(place__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Фильтр по дате
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    # Фильтр по месту
    place = request.GET.get('place', '').strip()
    if place:
        queryset = queryset.filter(place__icontains=place)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-date')
    valid_sort_fields = ['date', '-date', 'product_title', '-product_title']
    if sort_by in valid_sort_fields:
        queryset = queryset.order_by(sort_by)
    
    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    objpic = Profile.objects.all()
    
    context = {
        'object': paginator.get_page(page),
        'objectpic': objpic,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'place': place,
        'sort_by': sort_by,
    }
    return render(request, "lostlist.html", context)


@login_required
def lost_enter(request, *args, **kwargs):
    if request.method == 'POST':
        dict1 = request.POST.copy()
        dict1['username'] = request.user.username
        form = lostform(dict1 or None)
        if form.is_valid():
            formfull = lostfullform(dict1 or None)
            formfull.save()
            form.save()
            messages.success(request, 'Your form has been posted successfully!')
            return redirect('home')
    else:
        form = lostform()
    context = {'form': form}
    return render(request, "lost.html", context)


def found_enter(request, *args, **kwargs):
    if request.method == 'POST':
        dict2 = request.POST.copy()
        dict2['username'] = request.user.username
        form1 = foundform(dict2 or None)
        if form1.is_valid():
            formfull1 = foundfullform(dict2 or None)
            formfull1.save()
            form1.save()
            messages.success(request, 'Your form has been posted successfully!')
            return redirect('home')
    else:
        form1 = foundform()
    context = {'form1': form1}
    return render(request, "found.html", context)


def found_view(request, *args, **kwargs):
    queryset = itemfound.objects.all()
    
    # Поиск
    query = request.GET.get('q', '').strip()
    if query:
        queryset = queryset.filter(
            Q(product_title__icontains=query) |
            Q(place__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Фильтр по дате
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    if date_from:
        queryset = queryset.filter(date__gte=date_from)
    if date_to:
        queryset = queryset.filter(date__lte=date_to)
    
    # Фильтр по месту
    place = request.GET.get('place', '').strip()
    if place:
        queryset = queryset.filter(place__icontains=place)
    
    # Сортировка
    sort_by = request.GET.get('sort', '-date')
    valid_sort_fields = ['date', '-date', 'product_title', '-product_title']
    if sort_by in valid_sort_fields:
        queryset = queryset.order_by(sort_by)
    
    paginator = Paginator(queryset, 6)
    page = request.GET.get('page')
    objpic = Profile.objects.all()
    
    context = {
        'object': paginator.get_page(page),
        'objectpic': objpic,
        'query': query,
        'date_from': date_from,
        'date_to': date_to,
        'place': place,
        'sort_by': sort_by,
    }
    return render(request, "foundlist.html", context)
