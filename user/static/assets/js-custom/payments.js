jQuery(document).ready( function ($) {

    const renderModal = (data) => {
      let button_link = "";
      if("pay_url" in data){
        button_link = `<div class="row mb-3">
        <div class="col-12 d-flex">
          <a href="${data['pay_url']}" class="btn btn-primary w-100">Сплатити</a>
        </div>
      </div>`
      }
      return `<div class="row mb-3">
        <span class="desc col-12">Платіж</span>
        <div class="col-12 d-flex">
          <h4 style="margin: 0;">${data['amount']}</h4>
          <span style="margin-left: 15px;" class="status text-primary">${data['status']}</span>
        </div>
      </div>
      <div class="row mb-3">
        <span class="desc col-12">Дата</span>
        <p class="col-12" style="margin: 0;">${data['created']}</p>
      </div>
      <div class="row mb-3">
        <span class="desc col-12">${data['role']}</span>
        <div class="profile-pic col-12 d-flex">
          <div class="count-indicator">
            <img class="img-xs rounded-circle " src="${data['avatar']}" alt="">
          </div>
          <div class="profile-name" style="margin-left: 15px;">
            <h5 class="mb-0 font-weight-normal">${data['full_name']}</h5>
            <span style="font-size: 15px; color: rgb(100, 100, 224);">${data['email']}</span>
          </div>
        </div>
      </div>
      <div class="row mb-3">
        <span class="desc col-12">Метод платежу</span>
        <div class="col-12 d-flex align-items-center">
          <img src="${data['sender_card_type_svg']}" alt="">
          <p style="margin: 0 15px;">${data['card']}</p>
        </div>
      </div>
      <div class="row mb-3">
        <span class="desc col-12">Вид платежу</span>
        <div class="col-12 d-flex">
          <p>${data['mode']}</p>
        </div>
      </div>
      <div class="row mb-3">
        <span class="desc col-12">Опис</span>
        <div class="col-12 d-flex">
          <p>${data['description']}</p>
        </div>
      </div>${button_link}`;
    }
    
    $('.pay-btn-info').click(function(){
        let key = $(this).data('key');
        fetch(url_get_payment_data+"?key="+key, {
            method: "GET"
        })
        .then((response) => response.json())
        .then((data) => {
            $('#payment-modal').append(renderModal(data));
            setTimeout(()=>{
                $('.payment-preview').fadeIn();
            }, 200)
        })
        .catch((error)=> console.log(error));
    });

    $('.payment-preview').click(function(){
        $('.payment-preview').fadeOut();
        setTimeout(()=>{
            $('#payment-modal').empty();
        }, 1000)
    });
    $('.close-btn-pay').click(function(){
        $('.payment-preview').fadeOut();
        setTimeout(()=>{
            $('#payment-modal').empty();
        }, 1000)
    });

})