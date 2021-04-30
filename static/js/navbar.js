// requires jquery
// adapted from getskeleton.com

(function( navbar, $, undefined ) {
    let navOffsetTop;
    let button = document.getElementById("back-to-top");

    $(document).ready(function init() {
        $(window).scroll(onScroll);
        $(window).resize(onResize);
    });

    $(window).on("load", () => {
        $('a[href^="#"]').on('click', smoothScroll);
        onResize();
    })

    function onResize(e) {
        $('body').removeClass('has-docked-nav');
        navOffsetTop = $('.navbar').offset().top;
        onScroll();
    }

    function onScroll(e) {
        if(navOffsetTop < $(window).scrollTop() && !$('body').hasClass('has-docked-nav')) {
          $('body').addClass('has-docked-nav');
        }

        if(navOffsetTop > $(window).scrollTop() && $('body').hasClass('has-docked-nav')) {
          $('body').removeClass('has-docked-nav');
        }
    }

    function smoothScroll(e) {
        e.preventDefault();

        let target = this.hash;
        let scrollOff = $(target).offset().top
        let navHeight = $('.navbar').outerHeight();
        console.log(navHeight)

        if(!$('body').hasClass('has-docked-nav')) {
            scrollOff = scrollOff > navOffsetTop ? scrollOff - navHeight : scrollOff;
        } else {
            scrollOff = scrollOff < navOffsetTop ? scrollOff + navHeight : scrollOff;
        }
    //        console.log(scrollOff)

        $('html, body').animate({
            scrollTop: scrollOff
        }, 500, function () {
            $(target).focus();
            if ($(target).is(":focus")) { // Checking if the target was focused
              return false;
            } else {
              $(target).attr('tabindex','-1'); // Adding tabindex for elements not focusable
              $(target).focus(); // Set focus again
            };
        });
    }

    navbar.scrollToTop = function () {
        console.log("scroll to top")
        $('html, body').animate({
            scrollTop: $('html').offset().top
        }, 500, function () {
            // TODO: reset focus
        })
    }
} (window.navbar = window.navbar || {}, jQuery));
