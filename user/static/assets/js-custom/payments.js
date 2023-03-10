jQuery(document).ready( function ($) {
    
    $('.pay-btn-info').click(function(){
        $('.payment-preview').fadeIn();
    });

    $('.payment-preview').click(function(){
        $('.payment-preview').fadeOut();
    });
    $('.close-btn-pay').click(function(){
        $('.payment-preview').fadeOut();
    });

})