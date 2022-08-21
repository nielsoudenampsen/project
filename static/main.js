$(document).ready(function(){
    $(".favorite_button").click(function(){
        let favorites = document.getElementsByClassName("favorite_button");
        let itemid = $(this).closest(".card").attr("id")
        
        
        for (let i = 0; i < favorites.length; i++) {
            let clickedid = favorites[i].getAttribute('data-arg1')
            if(itemid == clickedid){
                console.log(itemid)
                $.ajax({
                        
                    type : 'POST',
                    url : "/favorite/" + favorites[i].getAttribute('data-arg1'),
                    contentType: 'application/json;charset=UTF-8',
                    data : JSON.stringify({'favorite_id': favorites[i].getAttribute("data-arg1"),
                            'favorite_img': favorites[i].getAttribute("data-arg2"),
                            'favorite_name': favorites[i].getAttribute("data-arg3"),
                            'favorite_description': favorites[i].getAttribute("data-arg4")
                        }),
                  });
                if(favorites[i].style.fill == "grey"){
                    favorites[i].style.fill = "yellow";
                }
                else{
                    favorites[i].style.fill = "grey";
                }
            }
          }
        

        
     
    });
  });

$(document).ready(function(){
    $(".update-button").click(function(){
        location.reload();
        return false;
    });
    
});