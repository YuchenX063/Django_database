from django.db import models

class Church(models.Model):
    instID = models.CharField(max_length=255)
    year = models.IntegerField()
    church_type = models.CharField(max_length=255)
    instName = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    instNote = models.CharField(max_length=255)
    placeName = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    state_orig = models.CharField(max_length=255)
    city_reg = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    attendingInstID = models.CharField(max_length=255)
    memberType = models.CharField(max_length=255)
    member = models.CharField(max_length=255)
    affiliated = models.CharField(max_length=255)

    class Meta:
        unique_together = (('instID', 'year'),)

    def __str__(self):
        return self.instName

class Small_Church(models.Model):
    instID = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    church_type = models.CharField(max_length=255)
    instName = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    instNote = models.CharField(max_length=255)
    placeName = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    state_orig = models.CharField(max_length=255)
    city_reg = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    attendingInstID = models.CharField(max_length=255)
    attendingChurch = models.CharField(max_length=255)
    attendingChurchFrequency = models.CharField(max_length=255)

    class Meta:
        unique_together = (('instID', 'year'),)

    def __str__(self):
        return self.instName

class Person(models.Model):
    persID = models.CharField(max_length=255)
    year = models.IntegerField()
    persTitle = models.CharField(max_length=255)
    persName = models.CharField(max_length=255)
    persSuffix = models.CharField(max_length=255)
    persNote = models.CharField(max_length=255)

    class Meta:
        unique_together = (('persID', 'year'),)

    def __str__(self):
        return self.persName

class Church_Person(models.Model):
    instID = models.CharField(max_length=255)
    persID = models.CharField(max_length=255)
    year_church = models.IntegerField()
    year_person = models.IntegerField()
    persTitle = models.CharField(max_length=255)
    persName = models.CharField(max_length=255)

    class Meta:
        unique_together = (('instID', 'persID', 'year_church', 'year_person'),)

    person_church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='persons')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_churches')

class Church_Church(models.Model):
    instID = models.CharField(max_length=255) #the id of church
    attendingInstID = models.CharField(max_length=255) #the id of small church
    year_church = models.IntegerField()
    year_small_church = models.IntegerField()

    class Meta:
        unique_together = (('instID', 'attendingInstID', 'year_church', 'year_small_church'),)

    church = models.ForeignKey(Church, on_delete=models.CASCADE, related_name='small_churches')
    small_church = models.ForeignKey(Small_Church, on_delete=models.CASCADE, related_name='churches')