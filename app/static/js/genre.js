
    let genre1 = document.querySelector('#genre1')
    genre1.selectedIndex=-1;
    let genre2 = document.querySelector('#genre2')
    genre1.onchange = function(){
        genre = genre1.value
        fetch('/genres/'+genre).then(function(response){
            response.json().then(function(data){
                let optionHTML = ''
                for (let gen of data.genres){
                    optionHTML += '<option value="'+gen[0]+'">'+gen[1]+'</option>';
                }
                genre2.innerHTML=optionHTML
                genre2.selectedIndex = -1;
            })
        })
    }