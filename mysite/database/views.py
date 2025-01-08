from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Church, Person, Church_Person, Small_Church, Church_Church

# Create your views here.

def index(request):
    return render(request, 'database/index.html')

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

