(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    // Add event listener to the sidebar-toggler
    $('.sidebar-toggler').click(function () {
        // Toggle the open class on both sidebar and content
        $('.sidebar, .content').toggleClass("open");
        return false;
    });

    // Sidebar Toggler (Added)
    // Remove the 'open' class when the page loads
    $('.sidebar, .content').removeClass("open");

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });

    // Rest of the code remains the same...
})(jQuery);
