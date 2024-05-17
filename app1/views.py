from django.shortcuts import redirect, render
from urllib.parse import unquote
from django.shortcuts import redirect
# from app1.email_utils import send_email
from .models import * 
from django.core import serializers
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login as auth_login
import json
from django.utils import timezone
from django.http import HttpResponseBadRequest
from django.urls import reverse
from decimal import Decimal
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
import datetime
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.db.models import Avg
import requests
import random
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime
from django.urls import reverse_lazy

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        otp = random.randint(100000, 999999)
        otp_str = str(otp).zfill(6)[:6]  # ensure OTP is between 4 to 6 digits
        mobile_no = request.POST.get('mobile_no')
        if UserProfile.objects.filter(mobile_no=mobile_no).exists():
        
            messages(request, 'Mobile Number Taken')
            return JsonResponse({'error':'Mobile Number Exists'})
        else:
            auth_key = '362abe918aa57dcf'
            sid = '11723'
            EID = '1001263168181693318'
            dltid = '1707170574553241572'
            company = ' GROWMORE INTERNATIONAL LIMITED'
            url = f"https://api.authkey.io/request?authkey={auth_key}&mobile={mobile_no}&country_code=91&sid={sid}&otp={otp}"
            response = requests.get(url)
            response_data = response.json() 
            otp_save_database = OTPVerification.objects.create(mobile_no=mobile_no,otp=otp_str)
            otp_save_database.save()
            # Implement the logic to send OTP using the provided auth_key and mobile_no
            expiration_time = timezone.now() - timezone.timedelta(minutes=5)
            OTPVerification.objects.filter(created_at__lte=expiration_time).delete()
            response_data = {
                'status': 'success',
                'message': 'OTP sent successfully.'
            }
    
            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@csrf_exempt
def resend_otp(request):
    if request.method == 'POST':
        otp = random.randint(100000, 999999)
        otp_str = str(otp).zfill(6)[:6]  # ensure OTP is between 4 to 6 digits
        mobile_no = request.POST.get('mobile_no')
        if User.objects.filter(mobile=mobile_no).exists():
        
            messages(request, 'Mobile Number Taken')
            return JsonResponse({'error':'Mobile Number Exists'})
        else:
            auth_key = '02e59807d3c6ce8d'
            sid = '11723'
            EID = '1001263168181693318'
            dltid = '1707170574553241572'
            company = ' GROWMORE INTERNATIONAL LIMITED'
            url = f"https://api.authkey.io/request?authkey={auth_key}&mobile={mobile_no}&country_code=91&sid={sid}&name=amitesh&OTP={otp}"
            response = requests.get(url)
            response_data = response.json()
            try:
                delete = OTPVerification.objects.all().delete()
                otp_save_database = OTPVerification.objects.create(mobile_no=mobile_no,otp=otp_str)
                otp_save_database.save()
            except:
                otp_save_database = OTPVerification.objects.create(mobile_no=mobile_no,otp=otp_str)
                otp_save_database.save()
            response_data = {
                'status': 'success',
                'message': 'OTP sent successfully.'
            }
    
            return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def verify_otp(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        print('251', mobile_no)
        user_otp = request.POST.get('otp')
        print('253', user_otp)
        # Retrieve the OTP from the database based on the phone number
        try:
            otp_verification = OTPVerification.objects.get(mobile_no=mobile_no)
            stored_otp = otp_verification.otp
            if user_otp == stored_otp:
                # OTP is valid
                return JsonResponse({'status': 'success', 'message': 'OTP verified successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'}, status=400)
        except OTPVerification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Phone number not found.'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Create your views here.
# Create your views here.
def index(request):
    homeBannerData = HomeBanner.objects.all()
    # cart, created = Cart.objects.get_or_create(user=request.user)
    # Fetch products based on categories
    all_products = Product.objects.filter(b2b=False)
    purses = Product.objects.filter(b2b=False, category='Purse')
    belts = Product.objects.filter(b2b=False, category='Belt')
    combos = Product.objects.filter(b2b=False, category='Combo')
    new_arrival_products = Product.objects.filter(b2b=False, new_arrival=True)
    # Fetch average ratings for each product
    purse_ratings = ReviewRating.objects.filter(product_id__in=purses).aggregate(Avg('rating'))
    belt_ratings = ReviewRating.objects.filter(product_id__in=belts).aggregate(Avg('rating'))
    combo_ratings = ReviewRating.objects.filter(product_id__in=combos).aggregate(Avg('rating'))


    sideofferbar = Sideofferbar.objects.all()
    sideofferbar1 = Sideofferbar1.objects.all()
    sideofferbar2 = Sideofferbar2.objects.all()

    cart_items = []
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    
    else: 
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)

    context = {
        'homeBannerData': homeBannerData,
        'purses': purses,
        'belts': belts,
        'combos': combos,
        'products': all_products,
        'new_arrival_products':new_arrival_products,
        'sideofferbar': sideofferbar,
        'sideofferbar1': sideofferbar1,
        'sideofferbar2': sideofferbar2,
        'purse_avg_rating': purse_ratings['rating__avg'] if purse_ratings['rating__avg'] is not None else 0,
        'belt_avg_rating': belt_ratings['rating__avg'] if belt_ratings['rating__avg'] is not None else 0,
        'combo_avg_rating': combo_ratings['rating__avg'] if combo_ratings['rating__avg'] is not None else 0,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'index.html', context)
    
def maintenance(request):
    return render(request, 'error_page.html')

def contact_us(request):
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            subject = request.POST.get('subject') 
            message = request.POST.get('con_message')

            # Save form data to the database
            contact_entry = ContactUs(fname=fname, lname=lname, email=email, subject=subject, message=message)
            contact_entry.save()

            # You can add additional logic here, such as sending email notifications

            # Add a success message
            messages.success(request, 'Your message has been sent successfully!')

            # Redirect to the same page
            return redirect('contact-us')
        else:
            # messages.error(request, 'Your message has failed!Please try again')

            wishlist_items = []
            cart_items = []
            total_cost = 0
    
            if request.user.is_authenticated:
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
                wishlist_items = Wishlist.objects.filter(user=request.user)
                total_cost = sum(cart_item.total_cost for cart_item in cart_items)
            else:
                cart_items_data = request.session.get('guest_cart', [])
                wishlist_items_data = request.session.get('guest_wishlist', [])
                wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]
    
                for item_data in cart_items_data:
                    product = get_object_or_404(Product, id=item_data['product_id'])
                    quantity = item_data['quantity']
                    total_cost += product.discounted_price * quantity
                    cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
                    cart_items.append(cart_item)
                    
            total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    
            context = {
                'cart_items': cart_items,
                'total_cost': total_cost,
                'wishlist_items': wishlist_items,
                'wishlist_items_count': len(wishlist_items),
            }

        return render(request, 'contact-us.html', context) 
        
def login(request):
    cart_items = []
    wishlist_items = []

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if 'guest_cart' in request.session:
                    guest_cart_items_data = request.session.get('guest_cart', [])
                    for item_data in guest_cart_items_data:
                        product = get_object_or_404(Product, id=item_data.get('product_id'))
                        quantity = item_data.get('quantity')
                        total_cost = product.discounted_price * quantity
                        cart, created = Cart.objects.get_or_create(user=request.user)
                        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                        if not created:
                            cart_item.quantity += quantity
                            cart_item.total_cost += total_cost
                        else:
                            cart_item.quantity = quantity
                            cart_item.total_cost = total_cost
                        cart_item.save()

                    del request.session['guest_cart']
                    return redirect('place_order')
                else:
                    # If no session data, redirect to index
                    return redirect('index')
            else:
                # User authentication failed
                messages.error(request, "Invalid username or password")

        except Exception as e:
            # Handle any unexpected exceptions
            messages.error(request, f"An error occurred: {str(e)}")

    else:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            # Pass the cart_items to the context to display them in the template
        else:
            wishlist_items_data = request.session.get('guest_wishlist', [])
            wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

    context = {
        'cart_items': cart_items,  # Pass the cart_items to the context
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }

    return render(request, 'login-register.html', context)

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('accounts/login/')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dob = request.POST.get('dob')
            mobile_no = request.POST.get('mobile_no')
            gender = request.POST.get('gender')
            if User.objects.filter(email=username).exists():
                messages.info(request, 'This Email is Already Taken {} ! Please Register With Another Email'.format(username))
                return redirect('register')
            
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=username,
            )
            profile = UserProfile.objects.create(
                user=user,
                dob=dob,
                mobile_no=mobile_no,
                gender=gender
            )
            messages.success(request, f'{first_name} was successfully registered!')
            return redirect('accounts/login/')  # Assuming you have a named URL pattern for login page
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('register')  # Redirect back to registration page
    else:
        return render(request, 'login-register.html')
        

@login_required()
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        user = request.user

        # Check if the current password is correct
        if not check_password(current_password, user.password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('change_password')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')

        # Update the user's password
        user.set_password(new_password)
        user.save()

        # Update session auth hash to prevent logout
        update_session_auth_hash(request, user)

        # Send password change notification email using Elastic Email API
        try:
            elastic_email_api_key = '9D81D5E90EC6535C2D6D72C010D2E4CAF86D3B2112B26EBD387A23224FE81215496FEA61E5FED33206906025A9ED5293'
            elastic_email_template_id_or_name = 'https://app.elasticemail.com/marketing/templates/new?shareIdentifier=f2_wZazRMAqZUzNFhrC4uw2'  # Replace with the actual ID or name of your template
            elastic_email_url = 'https://api.elasticemail.com/v2/email/send'
            subject = 'Password Change Notification'
            body = 'Your password has been successfully changed. If you did not make this change, please contact us immediately.'
            to_address = user.email

            data = {
                'apikey': elastic_email_api_key,
                'to': to_address,
                'subject': subject,
                'body': body,
                'template': elastic_email_template_id_or_name,
            }

            response = requests.post(elastic_email_url, data=data)
            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                print("Password change notification email sent successfully")
            else:
                print(f"Failed to send password change notification email. Status code: {response.status_code}, Error: {response.text}")

        except Exception as e:
            print("An error occurred while sending the password change notification email:", e)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')  

    messages.error(request, 'Something Went Wrong!')
    return redirect('profile')


def forgot_password(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('phoneNumber')
        user_otp = request.POST.get('otp')
        try:
            otp_verification = OTPVerification.objects.get(mobile_no=mobile_no)
            stored_otp = otp_verification.otp
            if user_otp == stored_otp:
                return redirect('reset_password')
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'}, status=400)
        except OTPVerification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Phone number not found.'}, status=400)
    else:
        return render(request, 'forgot_password.html')

def post_detail(request):
    comments = Comment.objects.all()

    if request.method == 'POST':
        if 'comment' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            text = request.POST.get('comment')
            
            if name and email and text:
                Comment.objects.create(name=name, email=email, text=text, created_at=timezone.now())

                # Redirect to the same page after posting comment
                return redirect('post_detail')
        elif 'reply' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            text = request.POST.get('text')
            comment_id = request.POST.get('comment_id')

            if name and email and text and comment_id:
                parent_comment = Comment.objects.get(id=comment_id)
                Reply.objects.create(comment=parent_comment, name=name, email=email, text=text, created_at=timezone.now())

                # Redirect to the same page after posting reply
                return redirect('post_detail')

    return render(request, 'post_detail.html', {'comments': comments})

def Verify_Number(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        user = UserProfile.objects.filter(mobile_no = mobile_no)
        if user:
            otp = random.randint(100000, 999999)
            print(otp,"462")
            otp_str = str(otp).zfill(6)[:6]
            print(otp_str,"464")
            auth_key = '362abe918aa57dcf'
            sid = '11723'
            EID = '1001263168181693318'
            dltid = '1707170574553241572'
            company = ' GROWMORE INTERNATIONAL LIMITED'
            url = f"https://api.authkey.io/request?authkey={auth_key}&mobile={mobile_no}&country_code=91&sid={sid}&otp={otp}"
            response = requests.get(url)
            response_data = response.json()
            print("1285",mobile_no)
            print("1286",otp)
            try:
                delete_otp = OTPVerificationForgotPassword.objects.all().delete()
                otp_entry = OTPVerificationForgotPassword.objects.create(mobile_no=mobile_no,otp=otp_str)
                otp_entry.otp = otp
                otp_entry.save()

                expiration_time = timezone.now() - timezone.timedelta(minutes=5)
                OTPVerificationForgotPassword.objects.filter(created_at__lte=expiration_time).delete()
            except OTPVerification.DoesNotExist:
                otp_entry = OTPVerificationForgotPassword.objects.create(mobile_no=mobile_no, otp=otp_str)
                otp_entry.save()

                expiration_time = timezone.now() - timezone.timedelta(minutes=5)
                OTPVerificationForgotPassword.objects.filter(created_at__lte=expiration_time).delete()
            check=True
            response_data = {
                'check': check,
                'status': 'success',
                'message': 'Number verify successfully.'
            }
            return JsonResponse(response_data)
        else:
            check=False
            response_data = {
                'check': check,
                'status': 'Error',
                'message': 'Sorry your number is not Register'
            }
            return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def forgot_verify_otp(request):
    if request.method == 'POST':
        mobile_no = request.POST.get('mobile_no')
        print('1315', mobile_no)
        user_otp = request.POST.get('otp')
        print('1317', user_otp)
        print(mobile_no)
        print(user_otp)
        otp_verification = OTPVerificationForgotPassword.objects.get(mobile_no=mobile_no)
        print("1314",otp_verification)
        stored_otp = otp_verification.otp
        print('1319', stored_otp)
        try:
            if user_otp == stored_otp:
                print("1317",stored_otp)
                check=True
                url = f"https://growmore.in/reset_password/{mobile_no}"
                response_data = {
                'check': check,
                'status': 'success',
                'url':url
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'}, status=400)
        except OTPVerification.DoesNotExist:
            print("1328",stored_otp)
            return JsonResponse({'status': 'error', 'message': 'Phone number not found.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Something Went Wrong.'}, status=400)
  
def reset_password(request,number):
    if request.method == 'POST':
        comf_password = request.POST.get('confirm_password')
        new_password = request.POST.get('new_password')
        user_profile = UserProfile.objects.get(mobile_no=number)
        user_email = user_profile.user.username
        context = {'useremail':user_email,'number':number, }
        if new_password == comf_password:
            user_profile.user.set_password(new_password)
            user_profile.save()
            update_session_auth_hash(request, user_profile)
            messages.success(request, 'Success message: Your operation was successful!')
        else:
            messages.error(request, f'Error message: your Password not match')
        return render(request, 'reset-password.html', context)
    else:    
        print(number)
        user_profile = UserProfile.objects.get(mobile_no=number)
        user_email = user_profile.user.username
        context = {'useremail':user_email,'number':number, }
        return render(request, 'reset-password.html', context)

def combo(request, category=None, subcategory=None):
    # Fetch products based on categories
    combo = Product.objects.filter(category='Combo')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []

    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(b2b=False,category='Belt')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.all() 

    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'combo': combo,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        # 'product': product
    }
    return render(request, 'product.html', context)


from django.db.models import Q

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = ReviewRating.objects.filter(product=product)
    size_34 = Product.objects.filter(size_34=True)
    size_36 = Product.objects.filter(size_36=True)
    size_38 = Product.objects.filter(size_38=True)
    size_40 = Product.objects.filter(size_40=True)
    size_42 = Product.objects.filter(size_42=True)
    size_44 = Product.objects.filter(size_44=True)
    sizes = []
    if size_34:
        sizes.append('34')
    if size_36:
        sizes.append('36')
    if size_38:
        sizes.append('38')
    if size_40:
        sizes.append('40')
    if size_42:
        sizes.append('42')
    if size_44:
        sizes.append('44')

    # Determine related products based on the category of the current product
    related_products = Product.objects.filter(b2b=False, category=product.category).exclude(id=product_id)[:2]

    # Fetch existing cart items and wishlist items
    cart_items = []
    wishlist_items = []
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    
    context = {
        'product': product,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'reviews': reviews,
        'sizes':sizes,
        'related_products': related_products,
    }

    return render(request, 'product-details.html', context)

def submit_review(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        name = request.POST.get('name')
        email = request.POST.get('email')
        product_id = request.POST.get('product_id')

        if rating and review_text and name and email and product_id:
            product_id = int(product_id)
            user = request.user

            review_rating = ReviewRating.objects.create(
                product_id=product_id,
                user=user,
                title="Review Title",  # You can customize this or retrieve it from the form
                review=review_text,
                rating=rating,
                name=name,
                email=email,
            )

            review_rating.save()
            return redirect(reverse('product-details', kwargs={'product_id': product_id}))

    # Redirect to the product details page if the form submission fails
    return redirect(reverse('product-details', kwargs={'product_id': product_id}))

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from the form
    previous_url = request.META.get('HTTP_REFERER')
    if request.user.is_authenticated:
        # For authenticated users, handle the cart as usual
        cart, created = Cart.objects.get_or_create(user=request.user)
        # Save the cart before creating CartItem
        if created:
            cart.save()
        # Refresh the cart to get the updated instance with the primary key
        cart.refresh_from_db()
        # Save the cart again after updating the total cost
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        messages.success(request, f"{quantity} items added to your cart.")
        return redirect(previous_url)
    else:
        # For non-authenticated users (guests), handle the guest cart using sessions
        guest_cart = request.session.get('guest_cart', [])
        # Check if the product is already in the guest cart
        product_exists = any(item['product_id'] == product_id for item in guest_cart)
        if not product_exists:
            guest_cart.append({'product_id': product_id, 'quantity': quantity})
            request.session['guest_cart'] = guest_cart
            messages.success(request, f"{quantity} item(s) added to your cart.")
        else:
            messages.info(request, "Item is already in your cart.")
        return redirect(previous_url)


def shopping_cart(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
        total_cost = sum(cart_item.total_cost for cart_item in cart_items)
        context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        }

        return render(request, 'shopping-cart.html', context)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

        total_cost = sum(cart_item.total_cost for cart_item in cart_items)

        context = {
            'cart_items': cart_items,
            'total_cost': total_cost,
            'wishlist_items': wishlist_items,
            'wishlist_items_count': len(wishlist_items),
        }
        
        return render(request, 'shopping-cart.html', context)


def product_filter(request):
    # Get the sorting, filtering, and any other parameters from the URL
    sort_by = request.GET.get('sort', 'default')  # Default sorting, you can change this
    category = request.GET.get('category', 'all')
    # Add more parameters as needed

    # Retrieve all products initially
    all_products = Product.objects.all()

    # Apply filtering based on the category
    if category != 'all':
        all_products = all_products.filter(category=category)

    # Apply sorting based on the selected option
    if sort_by == 'price:asc':
        all_products = all_products.order_by('selling_price')
    elif sort_by == 'price:desc':
        all_products = all_products.order_by('-selling_price')

    # Add more filtering conditions as needed

    context = {
        'all_products': all_products,
    }

    return render(request, 'product.html', context)

def update_cart(request, cart_item_id, new_quantity):
    # Assuming you have a CartItem model with a 'quantity' field
    if request.user.is_authenticated:
        print("191",cart_item_id)
        print("192",)
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f"{new_quantity} item(s) added to your cart.")
        response_data = {'message': 'Quantity updated successfully'}
        return JsonResponse(response_data)
    else:
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        cart_items = []

        # Create CartItem objects
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

        for cart_item in cart_items:
            if cart_item.product.id == cart_item_id:
                cart_item.quantity = new_quantity
                cart_item.total_cost = cart_item.product.discounted_price * new_quantity

        # Update the session with the modified cart_items_data
        request.session['guest_cart'] = [{'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items]

        # Recalculate total_cost
        total_cost = sum(cart_item.total_cost for cart_item in cart_items)

        messages.success(request, f"{new_quantity} item(s) added to your cart.")
        response_data = {'message': 'Quantity updated successfully'}
        return JsonResponse(response_data)
       
        
def update_cart_2(request, new_quantity):
        cart_items_data = request.session.get('guest_cart', [])
        # wishlist_items_data = request.session.get('guest_wishlist', [])
        # wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        # guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = new_quantity
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

        total_cost = sum(cart_item.total_cost for cart_item in cart_items)
        messages.success(request, f"{new_quantity} item(s) added to your cart.")
        response_data = {'message': 'Quantity updated successfully'}
        return JsonResponse(response_data)

def delete_cart_item(request, product_id):
    if request.user.is_authenticated:
        # For authenticated users
        cart_item = get_object_or_404(CartItem, cart__user=request.user, product__id=product_id)
        cart_item.delete()
    else:
        # For non-authenticated users (guests)
        cart_items = request.session.get('guest_cart', [])

        for i, item in enumerate(cart_items):
            if item['product_id'] == product_id:
                del cart_items[i]
                break

        request.session['guest_cart'] = cart_items  # Fix the session variable name

    messages.success(request, "Item removed from your cart.")
    return redirect('shopping_cart')  

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    previous_url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        # For authenticated users, add the product to the wishlist
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    else:
        # For non-authenticated users, handle the wishlist using sessions
        wishlist_items = request.session.get('guest_wishlist', [])
        product_exists = any(item['product_id'] == product_id for item in wishlist_items)

        if not product_exists:
            wishlist_items.append({'product_id': product_id})
            request.session['guest_wishlist'] = wishlist_items
            
    # Redirect the user back to the previous URL
    return redirect(previous_url)



# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     previous_url = request.META.get('HTTP_REFERER')

#     if request.user.is_authenticated:
#         # For authenticated users, add the product to the wishlist
#         wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
#     else:
#         # For non-authenticated users, handle the wishlist using sessions
#         wishlist_items = request.session.get('guest_wishlist', [])
#         product_exists = any(item['product_id'] == product_id for item in wishlist_items)

#         if not product_exists:
#             wishlist_items.append({'product_id': product_id})
#             request.session['guest_wishlist'] = wishlist_items
            
#     return redirect('previous_url')


def wishlist(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }

    return render(request, 'wishlist.html', context)

def remove_from_wishlist(request, wishlist_item_id):
    if request.user.is_authenticated:
        # For authenticated users, remove the wishlist item from the database
        wishlist_item = get_object_or_404(Wishlist, id=wishlist_item_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, "Item removed from your wishlist.")
    else:
        # For non-authenticated users, remove the item from the session-based wishlist
        wishlist_items = request.session.get('guest_wishlist', [])
        wishlist_items = [item for item in wishlist_items if item['product_id'] != wishlist_item_id]
        request.session['guest_wishlist'] = wishlist_items
        messages.success(request, "Item removed from your wishlist.")

    return redirect('wishlist')

def shop_left_sidebar(request):
    # Fetch products based on categories
    all_products = Product.objects.all()
    # purses = Product.objects.filter(category='Purse')
    # belts = Product.objects.filter(category='Belt')
    # combos = Product.objects.filter(category='Combo')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'products': all_products,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        # 'product': product
    }
    return render(request, 'product.html', context)

def shop_left_sidebar(request, category=None, subcategory=None):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(category='Belt')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.all()
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  # Changed 'product' to 'products'
    }
    return render(request, 'product.html', context)

from django.db.models import Q

def under_799(request):
    # Fetch products based on categories
    all_products = Product.objects.all().filter(Q(discounted_price__lt=799) | Q(discounted_price__isnull=True))
    
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'products': all_products,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'under_799.html', context)

def product_short_under_799(request):
    # Fetch products based on categories
    all_products = Product.objects.all().filter(Q(discounted_price__lt=799) | Q(discounted_price__isnull=True))
    
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        all_products = all_products.order_by('discounted_price')
    elif sort_by == 'price_desc':
        all_products = all_products.order_by('-discounted_price')
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'products': all_products,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'product.html', context)
    
def product_belts(request):
    # Fetch products based on categories
    belts = Product.objects.filter(b2b=False, category='Belt')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'products': belts,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        # 'product': product
    }
    return render(request, 'belts.html', context)

def product_wallets(request):
    # Fetch products based on categories
    wallets = Product.objects.filter(category='Belt')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'products': belts,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        # 'product': product
    }
    return render(request, 'belts.html', context)


def belts(request, category=None, subcategory=None):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(b2b=False , category='Belt')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.all()
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  # Changed 'product' to 'products'
    }
    return render(request, 'belts.html', context)

def wallets(request, category=None, subcategory=None):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(b2b=False , category='Purse')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.all()
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  # Changed 'product' to 'products'
    }
    return render(request, 'wallets.html', context)

def corporate_gift(request, category=None, subcategory=None):
    # Fetch products based on categories
    combos = Product.objects.filter(b2b=False, category='Combo')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'combos': combos,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        # 'product': product
    }
    return render(request, 'corporate_gift.html', context)

# def wallets(request, category=None, subcategory=None):
#     wishlist_items = []
#     cart_items = []

#     try:
#         if subcategory:
#             subcategory = unquote(subcategory)
#             print(subcategory)
#     except Exception as e:
#         print(f"Error decoding subcategory: {e}")
    
#     if category:
#         all_products = Product.objects.filter(category=category)
        
#         if subcategory:
#             all_products = all_products.filter(subcategory=subcategory)
#     else:
#         all_products = Product.objects.filter(category="Purse")
        
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_items = CartItem.objects.filter(cart=cart)
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#     else:
#         cart_items_data = request.session.get('guest_cart', [])
#         wishlist_items_data = request.session.get('guest_wishlist', [])
#         wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

#         for item_data in cart_items_data:
#             product = get_object_or_404(Product, id=item_data['product_id'])
#             quantity = item_data['quantity']
#             total_cost = product.discounted_price * quantity
#             cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
#             cart_items.append(cart_item)

#     total_cost = sum(cart_item.total_cost for cart_item in cart_items) if cart_items else 0

#     context = {
#         'cart_items': cart_items,
#         'total_cost': total_cost,
#         'wishlist_items': wishlist_items,
#         'wishlist_items_count': len(wishlist_items),
#         'products': all_products
#     }
#     return render(request, 'wallets.html', context)

# def corporate_gift(request, category=None, subcategory=None):
#     # Fetch products based on categories
#     combos = Product.objects.filter(b2b=False, category='Combo')
#     # product = get_object_or_404(Product)
#     wishlist_items = []
#     cart_items = []
#     if request.user.is_authenticated:
#         # For authenticated users, retrieve the user's cart and cart items
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         cart_items = CartItem.objects.filter(cart=cart)
#         wishlist_items = Wishlist.objects.filter(user=request.user)
#     else:
#         # For non-authenticated users (guests), retrieve the guest cart items from the session
#         cart_items_data = request.session.get('guest_cart', [])
#         wishlist_items_data = request.session.get('guest_wishlist', [])
#         wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

#         guest_cart_items_data = request.session.get('guest_cart', [])
        
#         for item_data in cart_items_data:
#             product = get_object_or_404(Product, id=item_data['product_id'])
#             quantity = item_data['quantity']
#             total_cost = product.discounted_price * quantity
#             cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
#             cart_items.append(cart_item)

#     total_cost = sum(cart_item.total_cost for cart_item in cart_items)
#     context = {
#         'combos': combos,
#         'cart_items': cart_items,
#         'total_cost': total_cost,
#         'wishlist_items': wishlist_items,
#         'wishlist_items_count': len(wishlist_items),
#         # 'product': product
#     }
#     return render(request, 'corporate_gift.html', context)

def B2B(request, category=None, subcategory=None):
    # Fetch products based on categories
    
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass

    all_products = Product.objects.filter(b2b=True)  # Filter B2B products
    
    if category:
        # Filter products based on the selected category
        all_products = all_products.filter(category=category)

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.filter(b2b=True)  # Filter B2B products
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'product': all_products
    }
    return render(request, 'b2b.html', context)  

    

def B2B_belts(request, category=None, subcategory=None):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    all_products = Product.objects.filter(b2b=True, category='Belt')  # Filter B2B belts
    
    if subcategory:
        # Filter products based on subcategory
        all_products = all_products.filter(subcategory=subcategory)
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products
    }
    return render(request, 'b2b_belts.html', context)

def B2B_belts_2(request):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    category=None
    subcategory=None
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(b2b=True, category='Belt')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.filter(category='Belt')
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  # Changed 'product' to 'products'
    }
    return render(request, 'b2b_belts.html', context)



def B2B_wallets(request, category=None, subcategory=None):
    # Fetch products based on categories
    wishlist_items = []
    cart_items = []
    
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    
    if category:
        # Filter products based on the selected category
        all_products = Product.objects.filter(category='Purse')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            all_products = all_products.filter(subcategory=subcategory)
    else:
        all_products = Product.objects.all()
        
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  # Changed 'product' to 'products'
    }
    return render(request, 'b2b_wallets.html', context)
    
def B2B_corporate(request, category=None, subcategory=None):
    # Fetch products based on categories
    all_products = Product.objects.filter(b2b=True, category='Combo')
    # product = get_object_or_404(Product)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'products': all_products  
    }
    return render(request, 'b2b_corporate.html', context)

def product_short(request):
    products = Product.objects.all()
    
    # Filtering logic
    if category:
        products = products.filter(category=category)
    
    if subcategory:
        products = products.filter(subcategory=subcategory)
    
    # Sorting logic
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        products = products.order_by('discounted_price')
    elif sort_by == 'price_desc':
        products = products.order_by('-discounted_price')
    
    context = {
        'products': products
    }
    return render(request, 'product.html', context)


def product_short_belts(request, category=None, subcategory=None):
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass

    if category:
        # Filter products based on the selected category
        belts = Product.objects.filter(b2b=False, category='Belt')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            belts = belts.filter(b2b=False, subcategory=subcategory)
    else:
        belts = Product.objects.filter(b2b=False)

    # Sorting logic
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        belts = belts.order_by('discounted_price')
    elif sort_by == 'price_desc':
        belts = belts.order_by('-discounted_price')
    
    context = {
        'products': belts
    }
    return render(request, 'belts.html', context)


def product_short_wallets(request, category=None, subcategory=None):
    # Filter products for the 'Purse' category
    # purses = Product.objects.filter(category='Purse')
    try:
        input_string = subcategory
        subcategory = unquote(input_string)
        print(subcategory)
    except:
        pass
    if category:
        # Filter products based on the selected category
        purses = Product.objects.filter(category='Purse')  # Change 'belt' to 'Belt'

        if subcategory:
            # Filter products based on both category and subcategory
            purses = all_products.filter(subcategory=subcategory)
    else:
        purses = Product.objects.all()
    # Sorting logic
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'price_asc':
        purses = purses.order_by('discounted_price')
    elif sort_by == 'price_desc':
        purses = purses.order_by('-discounted_price')
    
    context = {
        'products': purses
    }
    return render(request, 'wallets.html', context)


def range_filter(request):
    if request.method == 'POST':
        price_range = request.POST.get('price')

        # Split the string to extract the minimum and maximum values
        min_price_str, max_price_str = price_range.split(' - ')

        # Remove the currency symbol and convert the strings to integers
        min_price = int(min_price_str.replace('₹', ''))
        max_price = int(max_price_str.replace('₹', ''))

        purses = Product.objects.filter(selling_price__range=(min_price, max_price), category='Purse')
        belts = Product.objects.filter(selling_price__range=(min_price, max_price), category='Belt')
        combos = Product.objects.filter(selling_price__range=(min_price, max_price), category='Combo')
        filtered_data = Product.objects.filter(selling_price__range=(min_price, max_price))


        # print(purses)
        # print(belts)
        # print(combos)
        # print(filtered_data)

        cart_items = []
        wishlist_items = []

        if request.user.is_authenticated:
            # For authenticated users, retrieve the user's cart and cart items
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            wishlist_items = Wishlist.objects.filter(user=request.user)
            
        guest_cart_items_data = request.session.get('guest_cart', [])
        for item_data in guest_cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            # cart_items.append(cart_item)
            wishlist_items_data = request.session.get('guest_wishlist', [])
            wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        # wishlist_items_data = request.session.get('guest_wishlist', [])
        # wishlist_items.extend(get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data)

        context = {
            'purses': purses,
            'belts': belts,
            'combos': combos,
            'cart_items': cart_items,
            'wishlist_items': wishlist_items,
            'wishlist_items_count': len(wishlist_items),
        }  

        return render(request, 'product.html', context)  
        
@login_required(login_url='accounts/login/')
def checkout(request):
    cart_user = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart_user)

    user_order = request.user
    cart_items_data = []

    for item_data in cart_items:
        product = get_object_or_404(Product, id=item_data.product_id)
        quantity = item_data.quantity
        total_cost = product.discounted_price * quantity
        cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
        cart_items_data.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items_data)
    
    saved_address = Order.objects.filter(user=request.user).first()
    ship_to_different_address = saved_address.ship_to_different_address if saved_address else False

    billing_info = {
        'name': saved_address.name if saved_address else '',
        'gender': saved_address.gender if saved_address else '',
        'country': saved_address.country if saved_address else '',
        'locality': saved_address.locality if saved_address else '',
        'city': saved_address.city if saved_address else '',
        'state': saved_address.state if saved_address else '',
        'zipcode': saved_address.zipcode if saved_address else '',
        'mobile_no': saved_address.mobile_no if saved_address else '',
    }

    shipping_info = {
        'ship_to_different_address': ship_to_different_address,
        'ship_country': request.POST.get('ship_country') if ship_to_different_address else billing_info['country'],
        'ship_name': request.POST.get('ship_name') if ship_to_different_address else billing_info['name'],
        'ship_gender': request.POST.get('ship_gender') if ship_to_different_address else billing_info['gender'],
        'ship_address': request.POST.get('ship_address') if ship_to_different_address else billing_info['locality'],
        'ship_town': request.POST.get('ship_town') if ship_to_different_address else billing_info['city'],
        'ship_state': request.POST.get('ship_state') if ship_to_different_address else billing_info['state'],
        'ship_zip': request.POST.get('ship_zip') if ship_to_different_address else billing_info['zipcode'],
        'ship_mobile_no': request.POST.get('ship_mobile_no') if ship_to_different_address else billing_info['mobile_no'],
    }
    

    razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    currency = 'INR'
    amount = total_cost * 100
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='1'))
    razorpay_order_id = razorpay_order['id']
    context = {
        'cart_items': cart_items_data,
        'amount': amount,
        'total_cost': total_cost,
        'user_order':user_order,
        'currency':currency,
        'razorpay_order_id':razorpay_order_id,
        'billing_info': billing_info,
        'shipping_info': shipping_info
    }
    return render(request, 'checkout.html', context)

from django.http import JsonResponse

def place_order(request):
    if request.method == 'POST':
        try:
            # Extract billing information
            billing_info = {
                'username': request.user.username,
                'name': request.POST.get('name', ''),
                'gender': request.POST.get('gender', ''),
                'country': request.POST.get('country', ''),
                'locality': request.POST.get('locality', ''),
                'city': request.POST.get('city', ''),
                'state': request.POST.get('state', ''),
                'zipcode': request.POST.get('zipcode', ''),
                'mobile_no': request.POST.get('mobile_no', ''),
            }

            # Extract shipping information
            ship_to_different_address = request.POST.get('ship_to_different_address', False)
            shipping_info = {
                'ship_to_different_address': ship_to_different_address,
                'ship_country': request.POST.get('ship_country') if ship_to_different_address else billing_info['country'],
                'ship_name': request.POST.get('ship_name') if ship_to_different_address else billing_info['name'],
                'ship_gender': request.POST.get('ship_gender') if ship_to_different_address else billing_info['gender'],
                'ship_address': request.POST.get('ship_address') if ship_to_different_address else billing_info['locality'],
                'ship_town': request.POST.get('ship_town') if ship_to_different_address else billing_info['city'],
                'ship_state': request.POST.get('ship_state') if ship_to_different_address else billing_info['state'],
                'ship_zip': request.POST.get('ship_zip') if ship_to_different_address else billing_info['zipcode'],
                'ship_mobile_no': request.POST.get('ship_mobile_no') if ship_to_different_address else billing_info['mobile_no'],
            }
            
            saved_address = Order.objects.filter(user=request.user).first()

            if saved_address:
                billing_info.update({
                    'name': saved_address.name,
                    'gender': saved_address.gender,
                    'country': saved_address.country,
                    'locality': saved_address.locality,
                    'city': saved_address.city,
                    'state': saved_address.state,
                    'zipcode': saved_address.zipcode,
                    'mobile_no': saved_address.mobile_no,
                })

                if ship_to_different_address:
                    shipping_info = {
                        'ship_name': saved_address.name,
                        'ship_gender': saved_address.gender,
                        'ship_country': saved_address.country,
                        'ship_address': saved_address.locality,
                        'ship_town': saved_address.city,
                        'ship_state': saved_address.state,
                        'ship_zip': saved_address.zipcode,
                        'ship_mobile_no': saved_address.mobile_no,
                    }


            # Get quantity and total_cost from the form
            quantity = request.POST.get('quantity', 0)
            total_cost = request.POST.get('total_cost', 0)
            order_id = request.POST.get('order_id', 0)

            

            cart_user = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart_user)

            user_order = request.user
            cart_items_data = []
            CustomerOrder = []
            totle_quantity = 0
            for item_data in cart_items:
                product = get_object_or_404(Product, id=item_data.product_id)
                quantity = item_data.quantity
                total_cost = product.discounted_price * quantity
                cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
                cart_items_data.append(cart_item)
                totle_quantity =+ item_data.quantity

            total_cost = sum(cart_item.total_cost for cart_item in cart_items_data)
            total_quantity = sum(cart_item.quantity for cart_item in cart_items_data)
            
                        # Create the order
            razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            currency = 'INR'
            amount = total_cost * 100
            razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='1'))
            razorpay_order_id = razorpay_order['id']
            
            order = Order.objects.create(
                product=product,
                user=request.user,
                **billing_info,
                **shipping_info,
                quantity=total_quantity,
                total_cost=total_cost,
                order_notes=request.POST.get('order_notes', ''),
                order_id=razorpay_order_id,
            )

            order.save()
            for i in cart_items:
                i.Order = order
                i.save()

            
            context = {
                'cart_items': cart_items_data,
                'amount': amount,
                'total_cost': total_cost,
                'user_order':user_order,
                'currency':currency,
                'razorpay_order_id':razorpay_order_id,
                'saved_address': saved_address,
                # 'customer_order': customer_order
            }
            return render(request, 'payment.html',context)
        
        except Product.DoesNotExist:
                # Handle the case where a product does not exist
            messages.error(request, 'Invalid product ID')
            return render(request, 'error_page.html', {'error_message': 'Invalid product ID'})
        except Exception as e:
            # Handle other potential exceptions
            messages.error(request, f'Error placing order: {str(e)}')
            return render(request, 'error_page.html', {'error_message': str(e)})
    else:
        return render(request, 'checkout.html')
        
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
@login_required(login_url='accounts/login/')
@csrf_exempt
def payment(request):
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        print('Received amount:', amount)

        razorpay_order = razorpay_client.order.create({'amount': amount, 'currency': 'INR'})
        razorpay_order_id = razorpay_order['id']

        context = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'currency': 'INR',
            'callback_url': '/success/',  # Update to your appropriate callback URL
        }
       
        return JsonResponse({'message': 'Payment successful!', 'context': context})
    else:
        return render(request, 'payment.html')

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required

def success(request):
    # try:
        # Get the values from the URL parameters
        razorpay_payment_id = request.GET.get('razorpay_payment_id')
        razorpay_order_id = request.GET.get('razorpay_order_id')
        razorpay_signature = request.GET.get('razorpay_signature')

        # Fetch payment details from Razorpay
        razorpay_payment = razorpay_client.payment.fetch(razorpay_payment_id)

        # Save the payment data to the Payment model
        if razorpay_payment['status']=='captured':
            payment = Payment.objects.create(
                razorpay_payment_id=razorpay_payment_id,
                amount=razorpay_payment['amount'],
                currency=razorpay_payment['currency'],
                status="Paid"
            )
            print('razorpay_order_id',razorpay_order_id)
        order = Order.objects.get(order_id=razorpay_order_id)
        order.payment = payment
        order.checkpayment_id = razorpay_payment_id
        order.save()
        amount_cut= razorpay_payment['amount'] / 100
        # Retrieve the payment data and pass it to the template for display
        cart_user = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart_user)
        for product_list in cart_items:
           old_list= old_CartItem.objects.create(
               cart=product_list.cart,
               product=product_list.product,
               quantity=product_list.quantity,
               total_cost=product_list.total_cost,
               order=product_list.Order
           )
           old_list.save()
        cart_items.delete()
        
        payment_data = {
            'payment_id': payment.id,
            'razorpay_payment_id': payment.razorpay_payment_id, 
            'amount': amount_cut,
            'currency': payment.currency,
            'status': payment.status,
        }
        return render(request, 'paymentsuccess.html', {'payment_data': payment_data})

    # except Exception as e:
    #     # Handle exceptions appropriately
    #     return render(request, 'paymentfail.html',)

    # except PaymentMethod.DoesNotExist:
    #     error_message = 'Selected payment method does not exist.'
    #     return render(request, 'error_page.html', {'error_message': error_message})
    # except Exception as e:
    #     error_message = f'Error in success: {str(e)}'
    #     return render(request, 'error_page.html', {'error_message': error_message})


@login_required
def profile(request):
    cart_items = []
    wishlist_items = []
    order_data = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
        
    guest_cart_items_data = request.session.get('guest_cart', [])
    for item_data in guest_cart_items_data:
        product = get_object_or_404(Product, id=item_data['product_id'])
        quantity = item_data['quantity']
        total_cost = product.discounted_price * quantity
        cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
        # cart_items.append(cart_item)
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]
        
    user_profile = UserProfile.objects.get(user=request.user)

    # Get user orders with related product information
    orders = Order.objects.filter(user=request.user).select_related('product')

    # Extract billing and shipping addresses from orders
    addresses = [
        {
            'billing': {
                'name': order.name,
                'gender': order.gender,
                'country': order.country,
                'locality': order.locality,
                'city': order.city,
                'state': order.state,
                'zipcode': order.zipcode,
                'mobile_no': order.mobile_no,
            },
            'shipping': {
                'name': order.ship_name,
                'gender': order.ship_gender,
                'country': order.ship_country,
                'address': order.ship_address,
                'town': order.ship_town,
                'state': order.ship_state,
                'zipcode': order.ship_zip,
                'mobile_no': order.ship_mobile_no,
            },
        }
        for order in orders
    ] 
    
    
    order_details = [
        
        {
            'order_id': order.order_id,
            'product_name': order.product.product_name if order.product else "Product Name not available",
            'product_url': order.product.prod_image if order.product else "Product IMAGE not available",
            'quantity': order.quantity,
            'status': order.payment.status,
            'total_cost': order.total_cost,
            'ship_address': order.ship_address,
            'ship_town': order.ship_town,
            'ship_state': order.ship_state,
            'ship_zip': order.ship_zip,
        }
        for order in orders
    ]
    
    payment_history = [
        {
            'payment_id': order.payment.razorpay_payment_id if order.payment else "Payment ID not available",
            'amount': order.payment.amount if order.payment else "Amount not available",
            'currency': order.payment.currency if order.payment else "Currency not available",
            'payment_status': order.payment.status if order.payment and order.payment.status else "Payment Status not available",
        }
        for order in orders
    ]
    
    old_cart_items = old_CartItem.objects.filter(order__in=orders)
    Cancel = Cancellation.objects.filter(user=request.user)
    
    check_url = False
    
    context = {
        'user_profile': user_profile,
        'oldcart': old_cart_items,
        'addresses': addresses,
        'order_details': order_details,
        'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
        'payment_history': payment_history,
        'Cancel':Cancel,
        'check_url':check_url,
    }

    return render(request, 'profile.html', context)


from datetime import datetime

def update_account(request):
    if request.method == 'POST':
        # Retrieve data from the request
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        mobile = request.POST.get('mobile', '')
        dob = request.POST.get('dob', '')
        gender = request.POST.get('gender', '')

        # Update user profile data
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.username = email
        request.user.mobile = mobile
        request.user.save()

        try:
            dob = datetime.strptime(dob, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use the format "Month Day, Year" (e.g., "April 23, 2023").')
            return redirect('profile')

        # Update additional profile data if needed
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.mobile_no = mobile
        profile.dob = dob
        profile.gender = gender
        profile.save()

        messages.success(request, 'Account updated successfully!')
        return redirect('profile')  # Redirect to account settings or any other desired page

    messages.error(request, 'Something Went Wrong!')
    return redirect('profile')
    
# @login_required
def edit_address(request):
    orders = Order.objects.filter(user=request.user)

    if not orders.exists():
        # Handle the case where no orders are found for the user
        messages.error(request, 'No order found for the user.')
        return redirect('profile')  # or another desired page

    order = orders.first()  # Assuming you want to use the first order if there are multiple

    if request.method == 'POST':
        # Process the form submission
        order.country = request.POST.get('country', '')
        order.locality = request.POST.get('locality', '')
        order.city = request.POST.get('city', '')
        order.state = request.POST.get('state', '')
        order.zipcode = request.POST.get('zipcode', '')

        order.ship_country = request.POST.get('ship_country', '')
        order.ship_address = request.POST.get('ship_address', '')
        order.ship_town = request.POST.get('ship_town', '')
        order.ship_state = request.POST.get('ship_state', '')
        order.ship_zip = request.POST.get('ship_zip', '')

        order.save()
        messages.success(request, 'Addresses updated successfully.')
        return redirect('profile')

    context = {
        'order': order,
    }

    return render(request, 'profile.html', context)


def about_us(request):
    about_us_data = AboutUs.objects.first()
    aboutBannerData = AboutBanner.objects.all()
    counters = Counter.objects.filter(about_us=about_us_data)
    skills = Skill.objects.filter(about_us=about_us_data)
    # cart, created = Cart.objects.get_or_create(user=request.user)
    # cart_items = CartItem.objects.filter(cart=cart)
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'aboutBannerData': aboutBannerData,
        'about_us_data': about_us_data,
        'counters': counters,
        'skills': skills,
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'aboutus.html', context)

def blog(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'blog.html', context)

def blog1(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'blog-details.html', context)

def blog2(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'blog-details2.html', context)

def blog3(request):
    cart_items = []
    wishlist_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
        
    guest_cart_items_data = request.session.get('guest_cart', [])
    for item_data in guest_cart_items_data:
        product = get_object_or_404(Product, id=item_data['product_id'])
        quantity = item_data['quantity']
        total_cost = product.discounted_price * quantity
        cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
        # cart_items.append(cart_item)
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]


    context = {
         'cart_items': cart_items,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'blog-details3.html', context)

def services(request):
    return render(request, 'services.html')

def faq(request):
    return render(request, 'faq.html')

def error(request):

    return render(request, '404.html')



def cancellation_request(request,ID):
    if request.method == 'POST':
        old_cart = old_CartItem.objects.get(id=ID)
        order = old_cart.order
        check_class= Cancellation.objects.filter(old_cart=old_cart)
        if check_class:
            messages.success(request, 'Request Already Send successfully!')
            return redirect('profile')
        else:
            reason = request.POST.get('reason')
            comment = request.POST.get('comment')
            cancel = Cancellation.objects.create(user=request.user,order=order, old_cart=old_cart,request_massage=reason,comment=comment)
            messages.success(request, 'Request Send successfully!')
            return redirect('profile')
    else:
        old_cart = old_CartItem.objects.get(id=ID)
        context={
            'old_cart':old_cart,
        }
        return render(request,"cancel-request.html",context)


def show_order(request):
    if request.method == 'POST':
        orderid = request.POST.get('order_id')
        orders = Order.objects.get(order_id=orderid)
        oldcart = old_CartItem.objects.filter(order=orders)
        
        oldcart_list = []
        
        for oldorder in oldcart:
            # Extracting data for each oldcart item
            product_id = oldorder.product.id
            product_name = oldorder.product.product_name
            product_image = oldorder.product.prod_image.url  # Assuming prod_image is an ImageField
            oldcart_id = oldorder.id
            oldcart_quantity = oldorder.quantity
            oldcart_amount = oldorder.total_cost
            
            # Creating a dictionary for each oldcart item
            oldcart_item = {
                'product_id': product_id,
                'product_name': product_name,
                'product_image': product_image,
                'oldcart_id': oldcart_id,
                'oldcart_quantity': oldcart_quantity,
                'oldcart_amount': oldcart_amount
            }
            
            # Appending the dictionary to the list
            oldcart_list.append(oldcart_item)
        check_url = True
        # oldcart_json = serializers.serialize('json', oldcart)
        return JsonResponse({'message': 'Order status updated successfully', 'oldcart': oldcart_list,'check_url':check_url})
  
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def videos(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'vdo.html', context)



################################################ ADMIN PANEL CODES ################################################ 

def signin_admin(request):
    if request.method == 'POST':
        ip_email = request.POST.get('email')
        ip_password = request.POST.get('password')
        user = authenticate(username=ip_email, password=ip_password)
        if user is not None:
            if user.is_superuser:
                auth_login(request, user)  # Correct usage of login() functio
                return redirect('admin-dashboard')  # Redirect superuser to admin dashboard
            else:
                context = {
                    'msg': 'You are not authorized to access the admin panel.'
                }
                return render(request, 'adminpanel/sign-in.html', context)
        else:
            if User.objects.filter(username=ip_email).exists():
                # Incorrect password
                context = {
                    'msg': 'Incorrect password!'
                }
                return render(request, 'adminpanel/sign-in.html', context)
            else:
                # User does not exist
                context = {
                    'msg': 'User does not exist!'
                }
                return render(request, 'adminpanel/sign-in.html', context)
    else:
        context = {
                    'msg': 'Invalid request!'
                }
        return render(request, 'adminpanel/sign-in.html',context)

@login_required(login_url=reverse_lazy('signin'))
def admin_dashboard(request):
    num_items = 20
    total_users = User.objects.filter(is_staff=False)
    user_count = total_users.count()
    total_product = Product.objects.all().count()
    total_orders = Order.objects.all().count()
    total_review = ReviewRating.objects.all().count()
    latest_users = User.objects.all().order_by('-date_joined')
    latest_order_items = old_CartItem.objects.all().order_by('-id')[:num_items]
    latest_product = Product.objects.all().order_by('-id')[:num_items]
    user_profiles = []
    for user in latest_users:
        profile = UserProfile.objects.filter(user=user).first()
        user_profiles.append({'user': profile,})
    
    context={
        'latest_product':latest_product,
        'latest_order_items':latest_order_items,
        'latest_user':user_profiles,
        'total_users':user_count,
        'total_product':total_product,
        'total_orders':total_orders,
        'total_review':total_review,
    }
    return render(request, 'adminpanel/index.html',context)

@login_required(login_url=reverse_lazy('signin'))
def product_list(request):
    product = Product.objects.all()
    context={
        'product':product,
    }
    return render(request,"adminpanel/product-list.html",context)

@login_required(login_url=reverse_lazy('signin'))
def add_product(request):
    
    return render(request,"adminpanel/product-add.html")

@login_required(login_url=reverse_lazy('signin'))
def save_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        categories = request.POST.get('categories')
        subcategories = request.POST.get('subcategories')
        barnd = request.POST.get('barnd')
        description = request.POST.get('description')
        img1 = request.FILES.get('img1')
        img2 = request.FILES.get('img2')
        imgdec = request.FILES.get('imgdec')
        selling_price = request.POST.get('selling_price')
        discounted_price = request.POST.get('discounted_price')
        # quantity = request.POST.get('quantity')
        availability = request.POST.get('availability')
        B2b = request.POST.get('B2B')
        condition = request.POST.get('condition')
        # ratingimg = request.POST.get('ratingimg')
        tagimg = request.FILES.get('tagimg')
        current_date = timezone.now().date()
        current_time = timezone.now().time()
        size34 = request.POST.get('size34')
        size36 = request.POST.get('size36')
        size38 = request.POST.get('size38')
        size40 = request.POST.get('size40')
        size42 = request.POST.get('size42')
        size44 = request.POST.get('size44')
        if size34 is None:
            size34 = False
        if size36 is None:
            size36 = False
        if size38 is None:
            size38 = False
        if size40 is None:
            size40 = False
        if size42 is None:
            size42 = False
        if size44 is None:
            size44 = False
            
        product =Product.objects.create(
            product_name=product_name,
            category=categories,
            subcategory=subcategories,
            Brand=barnd,
            selling_price=selling_price,
            discounted_price=discounted_price,
            desc=description,
            prod_image=img1,
            prod_image1=img2,
            prod_image_detail=imgdec,
            # quantity=quantity,b2b
            availability=availability,
            b2b=B2b,
            condition=condition,
            # rating=ratingimg,
            size_34=size34,
            size_36=size36,
            size_38=size38,
            size_40=size40,
            size_42=size42,
            size_44=size44,
            prod_tag=tagimg,
            pub_time=current_time,
            pub_date=current_date
        )
        try:
            # Attempt to save the product
            product.save()
            # If successful, send a success message
            messages.success(request, 'Product saved successfully!')
        except Exception as e:
            # If an error occurs during saving, send an error message
            messages.error(request, f'Failed to save product: {str(e)}')
        return redirect('product-list') 
    else:
        return render(request,"adminpanel/product-add.html")

@login_required(login_url=reverse_lazy('signin'))
def delete_product(request,pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Product Delete successfully!')
    return redirect('product-list')

def update_product(request, pk):
    if request.method == 'POST':
        # Process form data
        product = get_object_or_404(Product, id=pk)
        product_name = request.POST.get('product_name')
        categories = request.POST.get('categories')
        sub_categories = request.POST.get('sub_categories')
        barnd = request.POST.get('barnd')
        description = request.POST.get('description')
        selling_price = request.POST.get('selling_price')
        discounted_price = request.POST.get('discounted_price')
        quantity = request.POST.get('quantity')
        availability = request.POST.get('availability')
        condition = request.POST.get('condition')
        ratingimg = request.FILES.get('ratingimg')
        tagimg = request.FILES.get('tagimg')

        # Check if img1, img2, and imgdec are in request.FILES
        if 'img1' in request.FILES:
            product.prod_image = request.FILES['img1']
        if 'img2' in request.FILES:
            product.prod_image1 = request.FILES['img2']
        if 'imgdec' in request.FILES:
            product.prod_image_detail = request.FILES['imgdec']

        # Update other fields
        product.product_name = product_name
        product.category = categories
        product.subcategory = sub_categories
        product.Brand = barnd
        product.desc = description
        product.selling_price = selling_price
        product.discounted_price = discounted_price
        product.in_stock = quantity
        product.availability = availability
        product.condition = condition
        
        # Update rating image if provided
        if ratingimg:
            product.rating = ratingimg
        
        # Update tag image if provided
        if tagimg:
            product.prod_tag = tagimg

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product-list')
    else:
        # Render form for GET request
        product = get_object_or_404(Product, id=pk)
        context = {'product': product}
        return render(request, "adminpanel/product-update.html", context)

@login_required(login_url=reverse_lazy('signin'))
def user_list(request):
    users = UserProfile.objects.all()
    context={
        'users':users,
    }
    return render(request,"adminpanel/user-list.html",context)

@login_required(login_url=reverse_lazy('signin'))
def delete_user(request,pk):
    try:
        # Retrieve the UserProfile instance by ID
        user_profile = UserProfile.objects.get(id=pk)
        
        # Delete both the User and UserProfile instances
        user_profile.user.delete()  # This will delete the associated User
        user_profile.delete()  # This will delete the UserProfile
        
        messages.success(request, 'User Delete successfully!')
        return redirect('user-list')
    except UserProfile.DoesNotExist:
        messages.success(request, 'User does not exist')
        return redirect('user-list')

@login_required(login_url=reverse_lazy('signin'))
def order_list(request):
    order = Order.objects.all()
    context={
        'order':order,
    }
    return render(request,"adminpanel/new-order.html",context)

@login_required(login_url=reverse_lazy('signin'))
def update_order(request,pk):
    order = get_object_or_404(Order, pk=pk)
    print("orderghjkjhgfghjkjhghjk",order)
    context={
        'order':order,
    }
    return render(request,"adminpanel/order-detail.html",context)

@login_required(login_url=reverse_lazy('signin'))
def signout_admin(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('signin')

@login_required(login_url=reverse_lazy('signin'))
def review_list(request):
    review = ReviewRating.objects.all()
    context={'review':review,}
    return render(request,"adminpanel/review-list.html",context)

@login_required(login_url=reverse_lazy('signin'))
def delete_review(request,pk):
    review = get_object_or_404(ReviewRating, pk=pk)
    review.delete()
    messages.success(request, 'Review Delete successfully!')
    return redirect('review-list')

@login_required(login_url=reverse_lazy('signin'))
def status_update(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return JsonResponse({'message': 'Order status updated successfully'})
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
  
@login_required(login_url=reverse_lazy('signin'))  
def privacy_policy(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'privacy.html', context)

def term_policy(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'terms.html', context)

def refund_policy(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'refund.html', context)

def shipping_policy(request):
    wishlist_items = []
    cart_items = []
    if request.user.is_authenticated:
        # For authenticated users, retrieve the user's cart and cart items
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # For non-authenticated users (guests), retrieve the guest cart items from the session
        cart_items_data = request.session.get('guest_cart', [])
        wishlist_items_data = request.session.get('guest_wishlist', [])
        wishlist_items = [get_object_or_404(Product, id=item['product_id']) for item in wishlist_items_data]

        guest_cart_items_data = request.session.get('guest_cart', [])
        
        for item_data in cart_items_data:
            product = get_object_or_404(Product, id=item_data['product_id'])
            quantity = item_data['quantity']
            total_cost = product.discounted_price * quantity
            cart_item = CartItem(product=product, quantity=quantity, total_cost=total_cost)
            cart_items.append(cart_item)

    total_cost = sum(cart_item.total_cost for cart_item in cart_items)


    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'wishlist_items': wishlist_items,
        'wishlist_items_count': len(wishlist_items),
    }
    return render(request, 'shipping.html', context)

def cancel_request(request):
    order = Cancellation.objects.all()
    context={
        'order':order,
    }
    return render(request,"adminpanel/order-cancel-request.html",context)

@login_required(login_url=reverse_lazy('signin'))
def cancel_status_update(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        print('order_id',order_id)
        print('new_status',new_status)
        order = Cancellation.objects.get(id=order_id)
        order.cancel_check = new_status
        order.save()
        return JsonResponse({'message': 'Order status updated successfully'})
        # except Order.DoesNotExist:
        #     return JsonResponse({'error': 'Order not found'}, status=404)
        # except Exception as e:
        #     return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
   
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@login_required(login_url=reverse_lazy('signin'))   
def all_order(request,pk):
    order = Order.objects.get(id = pk)
    order_details = old_CartItem.objects.filter(order = order)
    context={
        'order_details':order_details,
    }
    return render(request,"adminpanel/all-order-details.html",context)


@login_required(login_url=reverse_lazy('signin'))
def payment_list(request):
    payment = Payment.objects.all()
    context={
        'payment':payment,
    }
    return render(request,"adminpanel/payment-list.html",context)

@login_required(login_url=reverse_lazy('signin'))
def payment_order(request,pk):
    payment_obj = Payment.objects.get(id = pk)
    order = Order.objects.get(payment = payment_obj)
    order_details = old_CartItem.objects.filter(order = order)
    context={
        'order_details':order_details,
    }
    return render(request,"adminpanel/all-order-details.html",context)

def product_list_filter(request, Category):
    # Fetch products based on categories
    all_products = Product.objects.filter(category=Category)  # Filter B2B belts
    context={
        'product':all_products,
    }
    return render(request,"adminpanel/product-list.html",context)









