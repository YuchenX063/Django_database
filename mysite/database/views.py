from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Church, Person, Church_Person, Small_Church, Church_Church
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    church_name = request.GET.get('church_name')
    person_name = request.GET.get('person_name')
    place_name = request.GET.get('place_name')
    
    church_list = Church.objects.all()
    person_list = Person.objects.all()
    
    if church_name and not person_name and not place_name:
        church_list = church_list.filter(instName__icontains=church_name)
        related_persons = Church_Person.objects.filter(person_church__instName__icontains=church_name).values_list('person', flat=True)
        person_list = Person.objects.filter(id__in=related_persons)
        # person_church -- the related churches according to the Church_Person model
    
    if person_name and not church_name and not place_name:
        person_list = person_list.filter(persName__icontains=person_name)
        related_churches = Church_Person.objects.filter(person__persName__icontains=person_name).values_list('person_church', flat=True)
        church_list = Church.objects.filter(id__in=related_churches)
    
    if place_name and not church_name and not person_name:
        church_list = church_list.filter(city_reg__icontains=place_name)
        related_persons = Church_Person.objects.filter(person_church__city_reg__icontains=place_name).values_list('person', flat=True)
        person_list = Person.objects.filter(id__in=related_persons)

    if church_name and place_name:
        church_list = church_list.filter(instName__icontains=church_name, city_reg__icontains=place_name)
        related_persons = Church_Person.objects.filter(person_church__instName__icontains=church_name, person_church__city_reg__icontains=place_name).values_list('person', flat=True)
        person_list = Person.objects.filter(id__in=related_persons)

    if church_name and person_name:
        church_person_list = Church_Person.objects.filter(person_church__instName__icontains=church_name, person__persName__icontains=person_name)
        church_ids = church_person_list.values_list('person_church__id', flat=True)
        person_ids = church_person_list.values_list('person__id', flat=True)
        church_list = church_list.filter(id__in=church_ids)
        person_list = person_list.filter(id__in=person_ids)
    
    if place_name and person_name:
        church_person_list = Church_Person.objects.filter(person_church__city_reg__icontains=place_name, person__persName__icontains=person_name)
        church_ids = church_person_list.values_list('person_church__id', flat=True)
        person_ids = church_person_list.values_list('person__id', flat=True)
        church_list = church_list.filter(id__in=church_ids)
        person_list = person_list.filter(id__in=person_ids)
    
    if church_name and place_name and person_name:
        church_person_list = Church_Person.objects.filter(person_church__instName__icontains=church_name, person__persName__icontains=person_name, person_church__city_reg__icontains=place_name)
        church_ids = church_person_list.values_list('person_church__id', flat=True)
        person_ids = church_person_list.values_list('person__id', flat=True)
        church_list = church_list.filter(id__in=church_ids)
        person_list = person_list.filter(id__in=person_ids)

    church_list = church_list.order_by('instID', 'year')
    person_list = person_list.order_by('persID', 'year')

    church_paginator = Paginator(church_list, 10)  # Show 10 churches per page
    person_paginator = Paginator(person_list, 10)  # Show 10 persons per page
    
    church_page_number = request.GET.get('church_page')
    person_page_number = request.GET.get('person_page')
    
    church_page_obj = church_paginator.get_page(church_page_number)
    person_page_obj = person_paginator.get_page(person_page_number)
    
    return render(request, 'database/index.html', {
        'church_page_obj': church_page_obj,
        'person_page_obj': person_page_obj,
        'church_name': church_name,
        'person_name': person_name,
        'place_name': place_name
    })

'''def church_detail(request, instID, year): #query a church by instID and year
    try:
        church = Church.objects.get(instID=instID, year=year)
        related_persons = Church_Person.objects.filter(person_church=church)
        attending_small_churches = Church_Church.objects.filter(instID=church.instID, year_church=church.year)
        return render(request, 'database/church.html', {
            'church': church,
            'related_persons': related_persons,
            'attending_small_churches': attending_small_churches
        })
    except Church.DoesNotExist:
        try:
            small_church = Small_Church.objects.get(instID=instID, year=year)
            related_persons = Church_Person.objects.filter(person_church=small_church)
            attending_church_name = None
            if small_church.attendingInstID:
                try:
                    attending_church = Church.objects.get(instID=small_church.attendingInstID, year=year)
                    attending_church_name = attending_church.instName
                except Church.DoesNotExist:
                    attending_church_name = "Unknown"
            return render(request, 'database/small_church.html', {
                'church': small_church,
                'related_persons': related_persons,
                'attending_church_name': attending_church_name
            })
        except Small_Church.DoesNotExist:
            return render(request, 'database/does_not_exist.html', {'instID': instID, 'year': year})'''

def church_detail(request, instID, year): #query a church by instID and year
    church = Church.objects.filter(instID=instID, year=year).first()
    if church:
        related_persons = Church_Person.objects.filter(person_church=church)
        attending_small_churches = Church_Church.objects.filter(instID=church.instID, year_church=church.year)
        attending_small_churches_details = []
        for attending in attending_small_churches:
            try:
                small_church = Small_Church.objects.get(instID=attending.attendingInstID, year=attending.year_small_church)
                attending_small_churches_details.append({
                    'instID': small_church.instID,
                    'year': small_church.year,
                    'instName': small_church.instName
                })
            except Small_Church.DoesNotExist:
                continue
        return render(request, 'database/church.html', {
            'church': church,
            'related_persons': related_persons,
            'attending_small_churches': attending_small_churches_details
        })
    else:
        try:
            small_church = Small_Church.objects.get(instID=instID, year=year)
            #related_persons = Church_Person.objects.filter(person_church=small_church)
            related_persons = []
            attending_church_name = None
            if small_church.attendingInstID:
                try:
                    attending_church = Church.objects.get(instID=small_church.attendingInstID, year=year)
                    attending_church_name = attending_church.instName
                except Church.DoesNotExist:
                    attending_church_name = "Unknown"
            return render(request, 'database/small_church.html', {
                'church': small_church,
                'related_persons': related_persons,
                'attending_church_name': attending_church_name
            })
        except Small_Church.DoesNotExist:
            return render(request, 'database/does_not_exist.html', {'instID': instID, 'year': year})

def person_detail(request, persID, year): #query a person by persID and year
    person = get_object_or_404(Person, persID=persID, year=year)
    related_churches = Church_Person.objects.filter(person=person)
    return render(request, 'database/person.html', {'person': person, 'related_churches': related_churches})

def church_list(request, instName, year):
    churches = Church.objects.filter(instName=instName, year=year)
    small_churches = Small_Church.objects.filter(instName=instName, year=year)
    
    # Add attending church information to small churches
    for small_church in small_churches:
        if small_church.attendingInstID:
            try:
                attending_church = Church.objects.get(instID=small_church.attendingInstID, year=year)
                small_church.attending_church_name = attending_church.instName
                small_church.attending_church_link = attending_church
            except Church.DoesNotExist:
                small_church.attending_church_name = "Unknown"
                small_church.attending_church_link = None
        else:
            small_church.attending_church_name = None
            small_church.attending_church_link = None

    return render(request, 'database/church_list.html', {'churches': churches, 'small_churches': small_churches, 'instName': instName, 'year': year})

def person_list(request, persName, year):
    persons = Person.objects.filter(persName=persName, year=year)
    return render(request, 'database/person_list.html', {'persons': persons, 'persName': persName, 'year': year})

