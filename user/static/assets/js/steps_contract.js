jQuery(document).ready(function ($) {


    
    let check_status = setInterval(()=>{
        fetch(urls.contract_check_status, {
            method: "GET",
        })
        .then((response) => response.json())
        .then((data) => {
            if("status" in data){
                if(data.status !== $("#now_status").val()){
                    window.location.reload();
                }
            }
        })
    }, 3000)

});