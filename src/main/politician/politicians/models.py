from django.db import models

# Create your models here.
class Politician(models.Model):
        name = models.CharField(max_length=100)
        gov_link = models.CharField(max_length=1000, blank=True)
        campaign_link = models.CharField(max_length=1000, blank=True)
        email = models.CharField(max_length=100, blank=True, null=True)
        phone = models.CharField(max_length=15, blank=True, null=True)
        address = models.CharField(max_length=1000, blank=True, null=True)
        party = models.CharField(max_length=25, null=True)
        date_elected = models.CharField(max_length=4,null=True)
        biography = models.CharField(max_length=10000, null=True)
        district = models.CharField(max_length=100, null=True)
        title = models.CharField(max_length=100, null=True, blank=True)

class City(models.Model):
        name = models.CharField(max_length=100, null=True, blank=True)
        state = models.CharField(max_length=25, null=True, blank=True)
        politician = models.ForeignKey(Politician, on_delete=models.CASCADE)

#Department model
class Department(models.Model):
        name = models.CharField(max_length=100, null=True, blank=True)
        url = models.CharField(max_length=1000, null=True, blank=True)
        phone = models.CharField(max_length=13, null=True, blank=True)
        city = models.ForeignKey(City, on_delete=models.CASCADE)

#To be chucked.
# class Office(models.Model):
#         office_id = models.AutoField(primary_key=True)
#         name = models.CharField(max_length=100, null=True, blank=True)
#         role = models.CharField(max_length=100, null=True, blank=True)
#         politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    
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