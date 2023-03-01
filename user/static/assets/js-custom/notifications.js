jQuery(document).ready(function ($) {
    
    const get_html = (title, body) => {
        return `<div class="dropdown-divider"></div>
        <a class="dropdown-item preview-item">
          <div class="preview-thumbnail">
            <div class="preview-icon bg-dark rounded-circle">
              <i class="mdi mdi-bell text-success"></i>
            </div>
          </div>
          <div class="preview-item-content">
            <p class="preview-subject mb-1">${title}</p>
            <p class="text-muted ellipsis mb-0"> ${body} </p>
          </div>
        </a>`
    }


    setInterval(()=>{

        fetch(urls.get_new_notification_url, {
            method: "GET"
        })
        .then((response) => response.json())
        .then((data) => {
            if(data.length > 0){
                $('#notificationDropdown').html('<i class="mdi mdi-bell"></i><span class="count bg-danger"></span>')
            }else{
                $('#notificationDropdown').html('<i class="mdi mdi-bell"></i>')
            }
            $('#notification-wrap-preview').empty();
            data.forEach(item => {
                $('#notification-wrap-preview').append(get_html(item.title, item.body))
            });
        })
        .catch((error)=> console.log(error));

    }, 3000)

})