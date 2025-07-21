var upadateBtns=document.getElementsByClassName('update-cart')

for(var i = 0;i<upadateBtns.length;i++ ){
    upadateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action = this.dataset.action
        console.log('projectId:',productId,'action:',action)
    
        console.log('USER:',user)
        if(user === 'AnonymousUser'){
            alert("Please login");
            window.location.href = "/login/";
                    
        }else{
            updateUserOrder(productId,action)
        }
    })
        

}


function updateUserOrder(productId,action){
    console.log('User is logged in, sending, data...')
    var url ='/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken' : csrftoken,
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })  
    .then((response)=>{
        return response.json()
    })
        .then((data)=>{
            console.log('data:',data)
            location.reload()
    })


}