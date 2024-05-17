/*--------------------------------------------------
Template Name: Raavin;
Description: Raavin - Responsive E-Commerce HTML Template;
Template URI:;
Author Name:HasTech;
Author URI:;
Version: 1.0.3;
Note: main.js, All Default Scripting Languages For This Theme Included In This File.
-----------------------------------------------------
    CSS INDEX
    ================
    1. Newsletter Popup
    02. Counter Js
    03. Meanmenu
    04. WOW
    05. Full Screen Menu Active
    06. Main Slider
    07. Banner Slider
    08. New Product Slider
    09. Testimonials Slider
    10. Featured Product Slider
    11. Blog Slider
    12. Featured Product-2 (Home style 2)
    13. New Product-2 (Home style 2)
    14. New Product 3 (Home Style 3)
    15. Scroll Up
    16. Isotop
    17. New Product 3 (Home Style 3)
    18. Select Plugin
    19. Zoom Product Venobox
    20. Product Details
    21. Star Rating Js
    22. Product Details
    23. FAQ Accordion
    24. Toggle Function Active
    25. Modal Menu Active
    26. Price Slider Active

-----------------------------------------------------------------------------------*/
(function ($) {
	"use Strict";
/*--------------------------
1. Newsletter Popup
---------------------------*/
setTimeout(function () {
    $('.popup_wrapper').css({
        "opacity": "1",
        "visibility": "visible"
    });
    $('.popup_off').on('click', function () {
        $(".popup_wrapper").fadeOut(500);
    })
}, 2500);
/*----------------------------------------*/
/* 02. Counter Js
/*----------------------------------------*/
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });
/*----------------------------------------*/
/* 03. Meanmenu
/*----------------------------------------*/
    jQuery('.mobile-menu nav').meanmenu({
        meanScreenWidth: "991"
    });
/*----------------------------------------*/
/* 04. WOW
/*----------------------------------------*/
    new WOW().init();
/*----------------------------------------*/
/* 05. Full Screen Menu Active
/*----------------------------------------*/
    function fullScreenmenu() {
        var menuTrigger = $('.menu-icon button'),
            endTriggermenu = $('button.menu-close'),
            container = $('.full-screen-menu-area');
        
        menuTrigger.on('click', function() {
            container.addClass('inside');
        });
        
        endTriggermenu.on('click', function() {
            container.removeClass('inside');
        });
        
    };
    fullScreenmenu();
/*----------------------------------------*/
/* 06. Main Slider
/*----------------------------------------*/
    $(".slider-active").owlCarousel({
        loop: true,
        margin: 0,
        nav: true,
        autoplay: true,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        items: 1,
        autoplayTimeout: 5000,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        dots: true,
        autoHeight: true,
        lazyLoad: true,
    });
/*----------------------------------------*/
/* 07. Banner Slider
/*----------------------------------------*/
    $('.banner-active').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        stagePadding:0,
        margin:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            480: {
                items: 2,
            },
            768: {
                items: 2,
            },
            992: {
                items: 3,
            }
        }
    });
/*----------------------------------------*/
/* 08. New Product Slider
/*----------------------------------------*/
    $('.new-product-active').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            768: {
                items: 2,
            },
            992: {
                items: 3,
            },
            1200: {
                items: 4
            }
        }
    });
/*----------------------------------------*/
/* 09. Testimonials Slider
/*----------------------------------------*/
    $('.testimonials-active').owlCarousel({
        loop: true,
        nav: false,
        margin: 15,
        dots: true,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: false,
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 1,
            },
            1000: {
                items: 1
            }
        }
    });
/*----------------------------------------*/
/* 10. Featured Product Slider
/*----------------------------------------*/
    $('.featured-pro-active').owlCarousel({
        loop: true,
        nav: true,
        margin: 30,
        dots: false,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            480: {
                items: 2,
            },
            768: {
                items: 3,
            },
            992: {
                items: 4,
            },
            1200: {
                items: 6
            }
        }
    });
/*----------------------------------------*/
/* 11. Blog Slider
/*----------------------------------------*/
    $('.blog-active').owlCarousel({
        loop: true,
        nav: true,
        margin: 30,
        dots: false,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: false,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            992: {
                items: 3
            }
        }
    });
/*----------------------------------------*/
/* 12. Featured Product-2 (Home style 2)
/*----------------------------------------*/
    $('.featured-pro-active-2').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 0,
        slideBy:3,
        URLhashListener:false,
        prevArrow: '<span class="prev"></span>',
        nextArrow: '<span  class="next"></span>',
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 2
            },
            1000: {
                items: 2
            },
            1200: {
                items: 2
            }
        }
    });
/*----------------------------------------*/
/* 13. New Product-2 (Home style 2)
/*----------------------------------------*/
    $('.new-pro-active-2').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 0,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        prevArrow: '<span class="prev"></span>',
        nextArrow: '<span  class="next"></span>',
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            600: {
                items: 2,
            },
            1000: {
                items: 2
            }
        }
    });
/*----------------------------------------*/
/* 14. New Product 3 (Home Style 3)
/*----------------------------------------*/
    $('.product-tab-active').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 0,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            992: {
                items: 3
            },
            1000: {
                items: 4
            }
        }
    });
/*----------------------------------------*/
/* 10. Featured Product Slider
/*----------------------------------------*/
    $('.random-pro-active').owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        margin: 0,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        autoplayTimeout: 5000,
        lazyLoad: true,
        responsive: {
            0: {
                items: 1,
            },
            576: {
                items: 2,
            },
            768: {
                items: 3,
            },
            992: {
                items: 4,
            },
            1200: {
                items: 6
            }
        }
    });
/*----------------------------------------*/
/* 15. Scroll Up
/*----------------------------------------*/
   $.scrollUp({
    scrollText: '<i class="fa fa-arrow-up"></i>',
    easingType: 'linear',
    scrollSpeed: 900,
   });
/*----------------------------------------*/
/* 16. Isotop
/*----------------------------------------*/
    var isotopFilter = $('.isotop-filter');
    var isotopGrid = $('.isotop-grid');
    var isotopGridMasonry = $('.isotop-grid-masonry');
    var isotopGridItem = '.isotop-item';
    /*-- Images Loaded --*/
    isotopGrid.imagesLoaded(function () {
        /*-- Filter List --*/
        isotopFilter.on('click', 'button', function () {
            isotopFilter.find('button').removeClass('active');
            $(this).addClass('active');
            var filterValue = $(this).attr('data-filter');
            isotopGrid.isotope({ filter: filterValue });
        });
        /*-- Filter Grid Layout FitRows --*/
        isotopGrid.isotope({
            itemSelector: isotopGridItem,
            layoutMode: 'fitRows',
            masonry: {
                columnWidth: 1,
            }
        });
        /*-- Filter Grid Layout Masonary --*/
        isotopGridMasonry.isotope({
            itemSelector: isotopGridItem,
            layoutMode: 'masonry',
            masonry: {
                columnWidth: 1,
            }
        });
    });
/*----------------------------------------*/
/* 17. New Product 3 (Home Style 3)
/*----------------------------------------*/
    $('.popular-pro-active').owlCarousel({
        loop: true,
        nav: true,
        margin: 30,
        dots: false,
        stagePadding:0,
        slideBy:3,
        URLhashListener:false,
        navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
        autoplay: true,
        responsive: {
            0: {
                items: 1,
            },
            600: {
                items: 2,
            },
            1000: {
                items: 4
            }
        }
    });
/*----------------------------------------*/
/* 18. Select Plugin
/*----------------------------------------*/
$(document).ready(function() {
    $('.nice-select').niceSelect();
});
/*----------------------------------------*/
/* 19. Zoom Product Venobox
/*----------------------------------------*/
    $('.venobox').venobox({
        spinner:'wave',
        spinColor:'#cb9a00',
    });
/*----------------------------------------*/
/* 20. Product Details
/*----------------------------------------*/
$('.porduct-details-active').owlCarousel({
    loop: true,
    nav: true,
    margin: 30,
    dots: false,
    stagePadding:0,
    slideBy:3,
    URLhashListener:false,
    navText: [" <i class='fa fa-angle-left'></i>"," <i class='fa fa-angle-right'></i>"],
    autoplay: true,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 2,
        },
        1000: {
            items: 4
        }
    }
});
/*----------------------------------------*/
/* 21. Star Rating Js
/*----------------------------------------*/
    $(function() {
          $('.star-rating').barrating({
            theme: 'fontawesome-stars'
          });
       });
/*----------------------------------------*/
/* 22. Product Details
/*----------------------------------------*/
$('.blog-2-active').owlCarousel({
    loop: true,
    nav: true,
    margin: 30,
    dots: true,
    stagePadding:0,
    slideBy:3,
    URLhashListener:false,
    navText: [" <i class='fa fa-caret-left'></i>"," <i class='fa fa-caret-right'></i>"],
    autoplay: true,
    responsive: {
        0: {
            items: 1,
        },
        600: {
            items: 1,
        },
        1000: {
            items: 1
        }
    }
});
/*----------------------------------------*/
/* 23. FAQ Accordion
/*----------------------------------------*/
  $('.card-header a').on('click', function() {
    $('.card').removeClass('actives');
    $(this).parents('.card').addClass('actives');
  });
/*----------------------------------------*/
/* 24. Toggle Function Active
/*----------------------------------------*/ 
// showlogin toggle
  $('#showlogin').on('click', function() {
      $('#checkout-login').slideToggle(900);
  });
// showlogin toggle
  $('#showcoupon').on('click', function() {
      $('#checkout_coupon').slideToggle(900);
  });
// showlogin toggle
  $('#cbox').on('click', function() {
      $('#cbox-info').slideToggle(900);
  });

// showlogin toggle
  $('#ship-box').on('click', function() {
      $('#ship-box-info').slideToggle(1000);
  });
/*----------------------------------------*/
/* 25. Modal Menu Active
/*----------------------------------------*/
$('.single-slide-menu').owlCarousel({
      smartSpeed: 1000,
      nav: false,
      responsive: {
          0: {
              items: 3
          },
          450: {
              items: 3
          },
          768: {
              items: 4
          },
          1000: {
              items: 4
          },
          1200: {
              items: 4
          }
      }
  });
$('.modal').on('shown.bs.modal', function (e) {
  $('.single-slide-menu').resize();
})
  
$('.single-slide-menu a').on('click',function(e){
e.preventDefault();

var $href = $(this).attr('href');

$('.single-slide-menu a').removeClass('active');
$(this).addClass('active');

$('.product-details-large .tab-pane').removeClass('active show');
$('.product-details-large '+ $href ).addClass('active show');

})
/*----------------------------------------*/
/* 26. Price Slider Active
/*----------------------------------------*/
var sliderrange = $('#slider-range');
var amountprice = $('#amount');
$(function() {
    sliderrange.slider({
        range: true,
        min: 0,
        max: 10000,
        values: [0, 10000],
        slide: function(event, ui) {
            amountprice.val("₹" + ui.values[0] + " - ₹" + ui.values[1]);
        }    
    });
    amountprice.val("₹" + sliderrange.slider("values", 0) +
        " - ₹" + sliderrange.slider("values", 1));
});
/*----------------------------------------*/
/* 28. Sticky Menu Activation
/*----------------------------------------*/
$(window).on('scroll',function() {
    if ($(this).scrollTop() > 300) {
        $('.header-sticky').addClass("sticky");
    } else {
        $('.header-sticky').removeClass("sticky");
    }
});
})(jQuery);