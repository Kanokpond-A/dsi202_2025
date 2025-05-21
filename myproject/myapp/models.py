from django.db import models
from django.contrib.auth.models import User

class Tree(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class PlantingLocation(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserPlanting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    location = models.ForeignKey(PlantingLocation, on_delete=models.CASCADE)
    planting_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} planted {self.tree.name} at {self.location.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} on {self.notification_date.date()}"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(PlantingLocation, on_delete=models.SET_NULL, null=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ เพิ่มตรงนี้
    address = models.TextField(blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

# class NewsArticle(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     image_url = models.URLField()
#     article_url = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
    
class OrderItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20)  # 'tree' or 'equipment'
    item_id = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} x {self.quantity}"
    
class TreeOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verifying', 'Verifying'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed_at = models.DateTimeField(auto_now_add=True)

    location = models.ForeignKey(PlantingLocation, on_delete=models.SET_NULL, null=True, blank=True)
    slip = models.ImageField(upload_to='slips/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.tree.name} (x{self.quantity})"


