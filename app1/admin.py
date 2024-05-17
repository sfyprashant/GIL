from django.contrib import admin
from .models import *


admin.site.register(UserProfile)
admin.site.register(HomeBanner)


admin.site.register(Sideofferbar)
admin.site.register(Sideofferbar1)
admin.site.register(Sideofferbar2)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(old_CartItem)
admin.site.register(AboutUs)
admin.site.register(AboutBanner)
admin.site.register(Counter)
admin.site.register(Customer)
admin.site.register(Skill)
admin.site.register(Order)
admin.site.register(PaymentMethod)
admin.site.register(Payment)
admin.site.register(ReviewRating)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Wishlist)
admin.site.register(ContactUs)
admin.site.register(OTPVerification)
admin.site.register(OTPVerificationForgotPassword)
admin.site.register(Cancellation)
# Register your models here.


admin.site.site_header = "Growmore Admin"
admin.site.index_title = "Welcome to Growmore Administartion"
admin.site.site_title = "Growmore"


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category','subcategory', 'selling_price', 'availability', 'desc')
    list_filter = ('category', 'availability', 'b2b', 'subcategory')
    search_fields = ['product_name', 'category', 'subcategory','desc']

admin.site.register(Product, ProductAdmin)