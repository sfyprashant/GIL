from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.utils import timezone

User = get_user_model()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #Foreignkey with the User model
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True, null=True)
    
    def __str__(self):
        return self.user.username  # Return the username as a string representation of the profile

# Create your models here.
AVAILABILITY_CHOICES = (
    ('In Stock', 'In Stock'),
    ('Not Available ', 'Not Available In Stock'),
)

CATEGORY_CHOICES = (
    ('Purse', 'Purse'),
    ('Belt', 'Belt'),
    ('Combo', 'Combo'),
)
SUBCATEGORY_CHOICES = (
    ('All Belts', 'All Belts'),
    ('Signature Belts', 'Signature Belts'),
    # ('Reversible Belts', 'Reversible Belts'),
    ('Casual Belts', 'Casual Belts'),
    ('Semi Formal', 'Semi Formal'),
    ('Ladies Belt', 'Ladies Belt'),
    ('Formal Belts', 'Formal Belts'),
    ('Wallets', 'Wallets'),
    ('Accessories', 'Accessories'),
    ('Corporate Gifts', 'Corporate Gifts'),
    ('Under799', 'Under799')
)

class Product(models.Model):
    product_name = models.CharField(max_length=500)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, null=True)
    Brand = models.CharField(max_length=20, blank=True, null=True)
    selling_price = models.IntegerField()
    discounted_price = models.IntegerField()
    desc = models.CharField(max_length=2000)
    pub_date = models.DateField()
    pub_time = models.TimeField()
    prod_image = models.ImageField(upload_to='productimg')
    prod_image1 = models.ImageField(upload_to='productimg', blank=True, null=True)
    prod_image2 = models.ImageField(upload_to='productimg', blank=True, null=True)
    prod_image3 = models.ImageField(upload_to='productimg', blank=True, null=True)
    prod_image_detail = models.ImageField(upload_to='productimgdetail')
    availability = models.CharField(choices=AVAILABILITY_CHOICES, max_length=20)
    condition = models.CharField(max_length=20)
    rating = models.IntegerField(blank=True, null=True)
    prod_tag = models.ImageField(upload_to='tag')
    new_arrival = models.BooleanField(default=False)
    b2b = models.BooleanField(default=False)
    size_34 = models.BooleanField(default=False)
    size_36 = models.BooleanField(default=False)
    size_38 = models.BooleanField(default=False)
    size_40 = models.BooleanField(default=False)
    size_42 = models.BooleanField(default=False)
    size_44 = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product_name)

    # def image_tag(self):
    #     return mark_safe('<img src="%s" width="50" height="50" />' % (self.prod_image.url))

# Sidebar one

class Sideofferbar(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    sideofferbar = models.ImageField(upload_to='offerimg')

    def __str__(self):
        return str(self.title)

# Sidebar two

class Sideofferbar1(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    sideofferbar = models.ImageField(upload_to='offerimg1')

    def __str__(self):
        return str(self.title)

# Sidebar three

class Sideofferbar2(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    sideofferbar = models.ImageField(upload_to='offerimg2')

    def __str__(self):
        return str(self.title)

# Sidebar three

class Sideofferbar3(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    sideofferbar = models.ImageField(upload_to='offerimg2')

    def __str__(self):
        return str(self.title)

class ContactUs(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.IntegerField()  # Assuming you want to store ratings as integers
    name = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Wishlist'

STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab','Punjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal'),
    ('Chandigarh','Chandigarh'),
    ('Dadra & Nagar Haveli and Daman & Diu','Dadra & Nagar Haveli and Daman & Diu'),
    ('Delhi','Delhi'),
    ('Jammu and Kashmir','Jammu and Kashmir'),
    ('Lakshadweep','Lakshadweep'),
    ('Puducherry','Puducherry'),
    ('Ladakh','Ladakh'),
)

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.user.username} - {self.method_name}"

class Payment(models.Model):
    razorpay_payment_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.razorpay_payment_id} - {self.amount} - {self.status}"

STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    )



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    
    # Billing information
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    # email_verified = models.BooleanField(default=False)
    # mobile_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    country = models.CharField(max_length=255, default='Unknown')
    locality = models.CharField(max_length=255)
    city = models.CharField(max_length=255) 
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    mobile_no = models.CharField(max_length=20)
    # create_account = models.BooleanField(default=False)
    
    # Shipping information
    ship_to_different_address = models.BooleanField(default=False)
    ship_country = models.CharField(max_length=255)
    ship_name = models.CharField(max_length=255)
    ship_gender = models.CharField(max_length=10)
    ship_address = models.CharField(max_length=255)
    ship_town = models.CharField(max_length=255)
    ship_state = models.CharField(max_length=255)
    ship_zip = models.CharField(max_length=20)
    ship_mobile_no = models.CharField(max_length=20)
    
    # Order details
    order_notes = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=50, unique=True)
    checkpayment_id = models.CharField(max_length=50, null=True,blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"

        
    # def __str__(self):
    #     return f"Order {self.id} - {self.user.username} - {self.product.product_name}"

    @property
    def get_total(self):
        total = self.product.discounted_price * self.quantity
        return total


class Cart(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - Cart"


class CartItem(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_total_cost(self):
        return self.quantity * self.product.discounted_price

    def save(self, *args, **kwargs):
        self.total_cost = self.get_total_cost()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.product} in {self.cart}"

class old_CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def get_total_cost(self):
        return self.quantity * self.product.discounted_price

    def save(self, *args, **kwargs):
        self.total_cost = self.get_total_cost()
        super().save(*args, **kwargs)


    def _str_(self):
        return f"{self.product} in {self. Cart}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name
    

# Home Page Banner

class HomeBanner(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    offertag = models.CharField(max_length=70)
    homebannerimg = models.ImageField(upload_to='Homebanner')
    headerimg = models.ImageField(upload_to='HeaderImg')

    def __str__(self):
        return str(self.title)
    

class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='about_us_images/')
    description = models.TextField()

class AboutBanner(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    aboutbannerimg = models.ImageField(upload_to='aboutbanner')

    def __str__(self):
        return str(self.title)
  
  
class Counter(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='counter_icons/')
    label = models.CharField(max_length=255)
    count = models.PositiveIntegerField()

class Skill(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    percentage = models.PositiveIntegerField()

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

CANCEL_CHOICES = (
        ('Pending', 'Pending'),
        ('Accept', 'Accept'),
        ('Reject', 'Reject')
    )

class Cancellation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    old_cart = models.ForeignKey(old_CartItem, on_delete=models.CASCADE)
    request_massage = models.TextField(max_length=100, blank=True)
    comment = models.TextField(max_length=200, blank=True)
    cancel_check = models.CharField(max_length=20, choices=CANCEL_CHOICES, default='pending')
    test = models.TextField(max_length=500,null=True, blank=True)







class OTPVerification(models.Model):
    mobile_no = models.CharField(max_length=15)
    otp = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now,null=True,blank=True)
    
class OTPVerificationForgotPassword(models.Model):
    mobile_no = models.CharField(max_length=15)
    otp = models.CharField(max_length=8)
    created_at = models.DateTimeField(default=timezone.now,null=True,blank=True)

  