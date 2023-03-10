jQuery(document).ready( function ($) {
    
    $(".copy-btn").click(function(){
        $('.copied').fadeIn();
        setTimeout(()=>{
            $('.copied').fadeOut();
        }, 2000)
    })

})