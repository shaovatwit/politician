from django.db import models

# Create your models here.
class Politician(models.Model):
        politician_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        gov_link = models.CharField(max_length=1000, blank=True)
        campaign_link = models.CharField(max_length=1000, blank=True)
        email = models.CharField(max_length=100, blank=True, null=True)
        phone = models.CharField(max_length=15, blank=True, null=True)
        address = models.CharField(max_length=100, blank=True, null=True)
        party = models.CharField(max_length=25, null=True)
        date_elected = models.DateField(null=True)
        biography = models.CharField(max_length=10000, null=True)
        district = models.CharField(max_length=100, null=True)

class City(models.Model):
        city_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        state = models.CharField(max_length=25)
        politician = models.ForeignKey(Politician, on_delete=models.CASCADE)

#Department model
class Department(models.Model):
        department_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        url = models.CharField(max_length=1000)
        city = models.ForeignKey(City, on_delete=models.CASCADE)

class Office(models.Model):
        office_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        role = models.CharField(max_length=100)
        politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    
# #To be chucked.
# class Issue(models.Model):
#         issue_id = models.AutoField(primary_key=True)
#         name = models.CharField(max_length=100)
#         copy = models.CharField(max_length=100)
#         politician = models.ForeignKey(Politician, on_delete=models.CASCADE)

# #To be chucked.
# class Committee(models.Model):
#         committee_id = models.AutoField(primary_key=True)
#         name = models.CharField(max_length=100)
#         chair = models.CharField(max_length=100)
#         groups_overseen = models.CharField(max_length=100)
#         committee_web = models.CharField(max_length=100, blank=True)
#         politician = models.ForeignKey(Politician, on_delete=models.CASCADE)