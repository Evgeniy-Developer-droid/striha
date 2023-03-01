jQuery(document).ready(function ($) {

    let newSubTenantsCount = 0;

    function fadeAnimation(prev, next, t=1000) {
        $("#"+prev).fadeOut();
        $("#"+prev).removeClass("active");
        let tm = setTimeout(()=>{
            $("#"+next).fadeIn();
            $("#"+next).addClass("active");
            clearTimeout(tm);
        }, t)
    }

    function newInputBlockSubTenant() {
        return `<div class="sub_tenant border border-top-0 border-secondary p-3 mt-3 sb">
        <div class="row">
            <div class="form-group col-md-12 col-xl-6">
                <input type="text" class="form-control" name="sub_${newSubTenantsCount}_fn" placeholder="First name" aria-label="first_name">
            </div>
            <div class="form-group col-md-12 col-xl-6">
                <input type="text" class="form-control" name="sub_${newSubTenantsCount}_ln" placeholder="Last name" aria-label="last_name">
            </div>
            <div class="form-group col-12">
                <input type="email" class="form-control" name="sub_${newSubTenantsCount}_em" placeholder="Email" aria-label="email">
            </div>
        </div>
    </div>`
    }

    function getMediaImageHtml(url) {
        return `<div class="item">
            <img src="${url}" alt="">
        </div>`
    }

    function getInfoPointHtml(label, icon) {
        return `<div class="preview-item border-bottom">
        <div class="preview-item-content d-flex flex-grow">
          <div class="flex-grow">
            <div class="d-flex justify-content-between">
              <p class="preview-subject">${label}</p>
              ${icon}
            </div>
          </div>
        </div>
      </div>`
    }

    $("#add-subtenant").on('click', function(e) {
        e.preventDefault();
        $("#enter_main_info_step .sub-tenants-wrap .sb:last").before(newInputBlockSubTenant());
        newSubTenantsCount += 1;
    })

    $("#re_cancel_contract").on('click', function(e) {
        e.preventDefault();
        window.location.reload();
    })
    
    $("#token_get").on('click', function(e) {
        let token = $("#token_input").val();
        let formdata = new FormData();
        formdata.append("token", token);
        fetch(urls.re_data_url, {
            method: "POST",
            body: formdata
        })
        .then((response) => response.json())
        .then((data) => {
            if("error" in data){
                $('.new-contract-alert').text(data.error);
                $('.new-contract-alert').fadeIn();
                let tm = setTimeout(()=>{
                    $('.new-contract-alert').fadeOut();
                    $('.new-contract-alert').text("");
                    clearTimeout(tm);
                }, 3000)
            } else {
                $("#new_contract_price_month").text("UAN "+data.price_month);
                $("#new_contract_price_security").text("UAN "+data.price_security);
                $("#re_token_input").val(data.share_token);
                $("#re_description").text(data.description);

                if (data.type_real_estate === "house") {
                    $("#re_info").append(getInfoPointHtml("Type", '<span class="text-primary"><i class="mdi mdi-home-variant"></i> <b>House</b></span>'))
                } else if (data.type_real_estate === "appartment"){
                    $("#re_info").append(getInfoPointHtml("Type", '<span class="text-info"><i class="mdi mdi-home-modern"></i> <b>Appartment</b></span>'))
                }else{
                    $("#re_info").append(getInfoPointHtml("Type", '<span class="text-warning"><i class="mdi mdi-hotel"></i> <b>Single Room</b></span>'))
                }

                if(data.smokers_allowed){
                    $("#re_info").append(getInfoPointHtml("Smokers allowed", '<span class="text-success"><i class="mdi mdi-check-circle"></i></span>'))
                } else{
                    $("#re_info").append(getInfoPointHtml("Smokers allowed", '<span class="text-danger"><i class="mdi mdi-close-circle"></i></span>'))
                }

                if(data.children_allowed){
                    $("#re_info").append(getInfoPointHtml("Children allowed", '<span class="text-success"><i class="mdi mdi-check-circle"></i></span>'))
                } else{
                    $("#re_info").append(getInfoPointHtml("Children allowed", '<span class="text-danger"><i class="mdi mdi-close-circle"></i></span>'))
                }

                if(data.students_allowed){
                    $("#re_info").append(getInfoPointHtml("Students allowed", '<span class="text-success"><i class="mdi mdi-check-circle"></i></span>'))
                } else{
                    $("#re_info").append(getInfoPointHtml("Students allowed", '<span class="text-danger"><i class="mdi mdi-close-circle"></i></span>'))
                }

                if(data.animals_allowed){
                    $("#re_info").append(getInfoPointHtml("Animalsaccordion allowed", '<span class="text-success"><i class="mdi mdi-check-circle"></i></span>'))
                } else{
                    $("#re_info").append(getInfoPointHtml("Animals allowed", '<span class="text-danger"><i class="mdi mdi-close-circle"></i></span>'))
                }

                $(".accordion").fadeIn();

                let media_images_html = "";
                for(let i = 0; i < data.media.length; i++){
                    media_images_html += getMediaImageHtml(data.media[i].file);
                }
                $(".owl-carousel").html(media_images_html);
                $("#media-no-data").removeClass("active");
                $('#owl-carousel-basic').owlCarousel({
                    loop: true,
                    margin: 10,
                    dots: false,
                    nav: true,
                    autoplay: true,
                    autoplayTimeout: 4500,
                    navText: ["<i class='mdi mdi-chevron-left'></i>", "<i class='mdi mdi-chevron-right'></i>"],
                    responsive: {
                      0: {
                        items: 1
                      },
                      600: {
                        items: 1
                      },
                      1000: {
                        items: 1
                      }
                    }
                  });

                fadeAnimation("token_step", "enter_main_info_step");
            }
        })
    })

});