(function($) {
    "use strict";

    // Preloader (if the #preloader div exists)
    $(window).on('load', function() {
        if ($('#preloader').length) {
            $('#preloader').delay(100).fadeOut('slow', function() {
                $(this).remove();
            });
        }
    });

    // Back to top button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function() {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    // Initiate the wowjs animation library
    new WOW().init();

    // Header scroll class
    $(window).scroll(function() {
        if ($(this).scrollTop() > 5) {
            $('#header').addClass('header-scrolled');
        } else {
            $('#header').removeClass('header-scrolled');
        }
    });

    if ($(window).scrollTop() > 100) {
        $('#header').addClass('header-scrolled');
    }

    // Smooth scroll for the navigation and links with .scrollto classes
    // $('.main-nav a, .mobile-nav a, .scrollto').on('click', function() {
    //   if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
    //     var target = $(this.hash);
    //     if (target.length) {
    //       var top_space = 0;

    //       if ($('#header').length) {
    //         top_space = $('#header').outerHeight();

    //         if (! $('#header').hasClass('header-scrolled')) {
    //           top_space = top_space - 40;
    //         }
    //       }

    //       $('html, body').animate({
    //         scrollTop: target.offset().top - top_space
    //       }, 1500, 'easeInOutExpo');

    //       if ($(this).parents('.main-nav, .mobile-nav').length) {
    //         $('.main-nav .active, .mobile-nav .active').removeClass('active');
    //         $(this).closest('li').addClass('active');
    //       }

    //       if ($('body').hasClass('mobile-nav-active')) {
    //         $('body').removeClass('mobile-nav-active');
    //         $('.mobile-nav-toggle i').toggleClass('fa-times fa-bars');
    //         $('.mobile-nav-overly').fadeOut();
    //       }
    //       return false;
    //     }
    //   }
    // });

    // Navigation active state on scroll
    var nav_sections = $('section');
    var main_nav = $('.main-nav, .mobile-nav');
    var main_nav_height = $('#header').outerHeight();

    $(window).on('scroll', function() {
        var cur_pos = $(this).scrollTop();

        nav_sections.each(function() {
            var top = $(this).offset().top - main_nav_height,
                bottom = top + $(this).outerHeight();

            if (cur_pos >= top && cur_pos <= bottom) {
                main_nav.find('li').removeClass('active');
                main_nav.find('a[href="#' + $(this).attr('id') + '"]').parent('li').addClass('active');
            }
        });
    });
})(jQuery);

//check mcq score
$('#myform').on('submit', function(e) {
    e.preventDefault();
    var sum = 0;
    var lastQues = 0;
    for (var i = 1; i <= 9; i++) {
        var ques = document.getElementsByName("ques" + i);
        for (var y = 0; y < ques.length; y++) {
            if (ques[y].checked) {
                sum = Number(sum) + Number(ques[y].value);
                if (i == 9)
                    lastQues = Number(ques[y].value)
            }
        }
    }

    if (sum > 17 || lastQues > 0) {
        window.location.href = "http://localhost:8000/desc";
        return false;
    } else {
        window.location.href = "http://localhost:8000/result?result=happy";
        return false;

    }
})

$('#myform2').on('submit', function(e) {
    e.preventDefault();
    //This API call sends the answers to the question to the server and receives a value back 
    var dataAttribute = new FormData();
        
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/api/descriptive",
        dataType: "text",
        contentType: "application/json",
        data: dataAttribute,
        success: function(response) {
            var i = response.verdict; //check variable in which verdict is coming
            //Based on the value, the app either navigates to the happy or sad result page
            window.location.href = "http://localhost:8000/result?result=" + i;
            return false;
        },
        error: function(error) {
            alert("something went wrong");
            return false;
        }
    });


})