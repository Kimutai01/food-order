from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    fooditem = models.ForeignKey('menu.FoodItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user
    
class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2,verbose_name='Tax Percentage (%)')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Taxes"
    
    def __str__(self):
        return self.tax_type
        
    