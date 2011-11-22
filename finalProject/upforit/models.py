from django.db import models
from django.contrib.auth.models import User

categories = (('Appetizers', 'Appetizers'), ('Breads', 'Breads'), ('Soups', 'Soups'),
    ('Casseroles', 'Casseroles'), ('Entrees', 'Entrees'), ('Desserts', 'Desserts'),
    ('Beverages', 'Beverages'))

class Recipe(models.Model):
	category = models.CharField(max_length = 20, choices = categories, default ='student')
	title = models.CharField(max_length=50)
	preparation = models.TextField(max_length=5000, blank=True)
	serving = models.TextField(max_length=5000, blank=True)
	notes = models.TextField(max_length=5000, blank=True)
	creator = models.ForeignKey(User)
	update = models.DateTimeField()
	#card = models.ImageField(upload_to='images/cards', blank=True)
	
	def __unicode__(self):
		return u'%s' % self.title

class Ingredient(models.Model):
    item = models.TextField(max_length=200, blank=True)
    quantity = models.CharField(max_length=10, blank=True)
    measurement_type = models.CharField(max_length=15, blank=True)
    recipe = models.ForeignKey(Recipe)
    
    def __unicode__(self):
        return u'%s' % (self.quantity + " " + self.measurement_type + " " + self.item)
        
