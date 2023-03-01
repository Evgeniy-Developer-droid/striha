
let btn_add = document.getElementById("add-upload");
let uploads_data = document.getElementById('uploads_array')

Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

btn_add.addEventListener("click", function(e){
    let block = document.createElement('div')
    block.className = "upload-card c-card"
    block.innerHTML = `<input type="file" accept="image/*" class="input-upload" style="display: none;">
    <div class="logo upload-btn"><i class="mdi mdi-upload"></i></div>`.trim()
    btn_add.parentElement.before(block)
})

document.addEventListener("click", function(e){
    const target = e.target.closest(".upload-btn"); // Or any other selector.

    if(target){
        target.parentElement.querySelectorAll('input')[0].click()
    }
})

document.addEventListener("click", function(e){
    const target = e.target.closest(".delete-btn"); // Or any other selector.

    if(target){
        let formdata = new FormData();
        formdata.append("id", parseInt(target.getAttribute("data-pk")));
        fetch(urls.request_media_delete_url, {
            method: "POST",
            body: formdata
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            let uploads = JSON.parse(uploads_data.value);
            uploads.remove(parseInt(target.getAttribute("data-pk")))
            uploads_data.value = JSON.stringify(uploads);
            target.parentElement.remove();
        })
        .catch((error)=> console.log(error));
        
    }
})

document.addEventListener("change", function(e){
    const target = e.target.closest(".input-upload"); // Or any other selector.

    if(target){
        if(target.files.lenght !== 0){
            const file = target.files[0];
            let formdata = new FormData();
            formdata.append("file", file, file.name);
            fetch(urls.request_media_upload_url, {
                method: "POST",
                body: formdata
            })
            .then((response) => response.json())
            .then((data) => {
                if ("file" in data){
                    target.parentElement.style.backgroundImage = `url('${data.file}')`;
                    let change_logo_to_delete = target.parentElement.querySelectorAll(".upload-btn")[0];
                    let uploads = JSON.parse(uploads_data.value);
                    uploads.push(data.id);
                    
                    target.parentElement.className = "delete-upload-card c-card";
                    change_logo_to_delete.className = "logo delete-btn";
                    change_logo_to_delete.setAttribute("data-pk", data.id);
                    change_logo_to_delete.innerHTML = `<i class="mdi mdi-delete-forever"></i>`.trim();
                    uploads_data.value = JSON.stringify(uploads);
                }
            })
            .catch((error)=> console.log(error));
        }
    }
})