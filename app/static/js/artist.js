
    let artist1 = document.querySelector('#artist1')
    artist1.selectedIndex=-1;
    let artist2 = document.querySelector('#artist2')
    let results = document.querySelector('#results')
    artist1.onchange = function(){
        results.innerHTML = ''
        let artist = artist1.value
        console.log(artist)
        artist2.innerHTML =''
        fetch('/artists/'+artist).then(function(response){
            response.json().then(function(data){
                let optionHTML = ''
                for (let art of data.artists){
                    optionHTML += '<option value="'+art[0]+'">'+art[1]+'</option>';
                }
                artist2.innerHTML=optionHTML
                artist2.selectedIndex = -1;
            })
        })
    }
    artist2.onchange = function(){
        artist1v = artist1.value
        artist2v = artist2.value
        fetch('/artists/'+artist1v+'_'+artist2v).then(function(response){
            let optionHTML = ''
            response.json().then(function(data){
                for (let j =0;j<data.songs.length;j++){
                optionHTML += '<div id="'+j+'" class = "song container"><div class="songname">'+ data.songs[j].name +'</div><div class = "artists">'
                    for (let i =0;i<data.songs[j].artists.length;i++){ 
                        optionHTML += '<div class="artist row">' // open artist div
                        if(data.songs[j].artists[i].image){
                            optionHTML += '<div class="image"><img src="'+ data.songs[j].artists[i].image +'"></div>'} // artist info row
                        else{ optionHTML += '<div class="image"><img src="'+ 'https://via.placeholder.com/100x100?text=?' +'"></div>'}
                        optionHTML += '<div class="artistname">'+ data.songs[j].artists[i].name +'</div>' // artist info row
                        optionHTML += '</div>' //close artist div
                        
                    }
                    optionHTML += '</div></div>'
                }
            results.innerHTML=optionHTML
            })
        
        })
    }