jQuery(document).ready(function ($) {


    
    let check_status = setInterval(()=>{
        let key = $("#key").val();
        fetch(urls.contract_check_status+"?key="+key, {
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