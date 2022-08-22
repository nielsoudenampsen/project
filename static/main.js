// sends post request with ajax, so the page is not reloaded with every button click
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

  //updates the favorites list when the button is pressed
$(document).ready(function(){
    $(".update-button").click(function(){
        location.reload();
        return false;
    });
    
});


// DEBUG only, automaticly login
$(document).ready(function(){

    username_login = document.getElementById("username_login").setAttribute("value","n")
    password_login = document.getElementById("password_login").setAttribute("value","1")
    
    let path = window.location.pathname
    if(path == '/login' || path == '/logout' ) {
        document.login.submit();
    } 
});