from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.templatetags.static import static
from django.views.static import serve

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),

    # path('',views.maintenance,name='maintenance'),
    path('',views.index,name='index'),
    path('home',views.index,name='index'),
    path('contact-us',views.contact_us,name='contact-us'),
    path('accounts/login/',views.login,name='accounts/login/'),
    path('register',views.register,name='register'),
    path('product', views.shop_left_sidebar, name='product'),
    path('product_short/', views.product_short, name='product_short'),
    path('product_short/<str:category>/', views.product_short, name='product_category'),
    path('products/<str:category>/<str:subcategory>/', views.product_short, name='product_subcategory'),
    path('product-short-belts', views.product_short_belts, name='product-short-belts'),
    path('product-short-wallets', views.product_short_wallets, name='product-short-wallets'),
    path('product/<str:category>/', views.shop_left_sidebar, name='product'),
    path('product/<str:category>/<str:subcategory>/', views.shop_left_sidebar, name='product'),
    path('product-belts', views.product_belts, name='product-belts'),
    path('belts', views.belts, name='belts'),
    path('belts/<str:category>/<str:subcategory>/', views.belts, name='belts'),
    path('combo', views.combo, name='combo'),
    path('combo<str:category>/<str:subcategory>/', views.combo, name='combo'),
    path('wallets', views.wallets, name='wallets'),
    path('wallets/<str:category>/<str:subcategory>/', views.wallets, name='wallets'),
    path('accessories/<str:category>/<str:subcategory>/', views.wallets, name='accessories'),
    path('corporate-gift', views.corporate_gift, name='corporate-gift'),
    path('corporate-gift/<str:category>/<str:subcategory>/', views.corporate_gift, name='corporate-gift'),
    # path('corporate-gift/<str:category>/<str:subcategory>/', views.corporate_gift, name='corporate-gift'),
    path('product-details/<int:product_id>/', views.product_details, name='product-details'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    # path('shopping-cart/<int:product_id>/', views.shopping_cart, name='shopping_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('remove-from-wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('delete_cart_item/<int:product_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('update-cart/<int:cart_item_id>/<int:new_quantity>/', views.update_cart, name='update-cart'),
    path('update-cart-2/<int:new_quantity>/', views.update_cart_2, name='update-cart-2'),
    # path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('checkout/',  views.checkout, name='checkout'),
    path('about_us', views.about_us, name='about_us'),
    path('services', views.services, name='services'),
    path('blog', views.blog, name='blog'),
    path('blog1', views.blog1, name='blog1'),
    path('blog2', views.blog2, name='blog2'),
    path('blog3', views.blog3, name='blog3'),
    path('post_detail/', views.post_detail, name='post_detail'),
    path('faq', views.faq, name='faq'),
    path('error', views.error, name='error'),
    path('logout', views.logout, name='logout'),
    # path('razorpay_confirm_payment/', views.razorpay_confirm_payment, name='razorpay_confirm_payment'),
    # path('payment', views.payment, name='payment'),
    # path('paymenthandler', views.paymenthandler, name='paymenthandler'),
    path('profile', views.profile, name='profile'),
    path('update_account', views.update_account, name='update_account'),
    path('edit_address/', views.edit_address, name='edit_address'),
    path('change_password', views.change_password, name='change_password'),
    path('product_filter', views.product_filter, name='product_filter'),
    path('accounts/login/verify-mobile', views.send_otp),
    path('accounts/login/verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp', views.resend_otp, name='resend-otp'),
    path('success/', views.success, name='success'),
    path('forgot_password', views.forgot_password, name='forgot_password'),#shivani
    path('reset_password/<str:number>', views.reset_password, name='reset_password'),#shivani
    path('verify-number', views.Verify_Number, name='verify-number'),
    path('for-verify-otp', views.forgot_verify_otp, name='for-verify-otp'),
    path('filter', views.range_filter, name='filter'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('B2B/', views.B2B, name='B2B'),
    path('B2B/<str:category>/<str:subcategory>/', views.B2B, name='b2b_filtered'),
    path('B2B-Belts/', views.B2B_belts_2, name='B2B-Belts'),
    path('b2b-belts/<str:category>/<str:subcategory>/', views.B2B_belts, name='b2b-belts'),
    path('B2B-Wallets/', views.B2B_wallets, name='B2B-Wallets'),
    path('b2b-wallets/<str:category>/<str:subcategory>/', views.B2B_wallets, name='b2b-wallets'),
    path('b2b-corporate-gift/', views.B2B_corporate, name='b2b-corporate-gift'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('term_policy/', views.term_policy, name='term_policy'),
    path('refund_policy/', views.refund_policy, name='refund_policy'),
    path('shipping_policy/', views.shipping_policy, name='shipping_policy'),
    path('cancellation-request/<str:ID>/', views.cancellation_request, name='cancellation-request'),
    path('show-order', views.show_order, name='show-order'),
    path('under799', views.under_799, name='under799'),
    path('videos', views.videos, name='videos'),
    path('product-short-under799', views.product_short_under_799, name='product-short-under799'),

    
    
    ###################### ADMIN PANEL CODES ###################### 

   
    path('signin', views.signin_admin, name='signin'),
    path('signout', views.signout_admin, name='signout'),
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('product-list', views.product_list, name='product-list'),
    path('product-list-filter/<str:Category>', views.product_list_filter, name='product-list-filter'),
    path('add-product', views.add_product, name='add-product'),
    path('save-product', views.save_product, name='save-product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
    path('update-product/<int:pk>/', views.update_product, name='update-product'),
    path('user-list', views.user_list, name='user-list'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete-user'),
    path('order-list', views.order_list, name='order-list'),
    path('update-order/<int:pk>/', views.update_order, name='update-order'),
    path('review-list', views.review_list, name='review-list'),
    path('delete-review/<int:pk>/', views.delete_review, name='delete-review'),
    path('status', views.status_update, name='status'),
    path('cancel-request', views.cancel_request, name='cancel-request'),
    path('cancel-status2', views.cancel_status_update, name='cancel-status2'),
    path('all-order/<int:pk>/', views.all_order, name='all-order'),
    path('payment-list', views.payment_list, name='payment-list'),
    path('payment-order/<int:pk>/', views.payment_order, name='payment-order'),

    
    
]



