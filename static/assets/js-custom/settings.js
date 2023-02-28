jQuery(document).ready(function ($) {
    

    $('#avatar-input').change(function(e){
        let file = $('#avatar-input')[0].files[0];
        let crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
        if(file){
            let formdata = new FormData();
            formdata.append('avatar', file, file.name);
            fetch(urls.change_avatar_url, {
                method: "POST",
                // headers:{"X-CSRFToken": crf_token},
                body: formdata
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                $(".image-avatar-change").css("background-image", `url('${data.avatar}')`)
            })
            .catch((error)=> console.log(error));
        }
    })


})