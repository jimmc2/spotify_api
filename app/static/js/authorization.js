auth_request = (event) =>{
    event.preventDefault()
    console.log('entered')
    var request = new XMLHttpRequest();
    request.onreadystatechange= function () {
        console.log(request)
        console.log('did it')
    }
    let clientid = 'b1517d3939f347839da7391dcf5d6e86'
    let client_secret = '5f386d680a02483a94f5bd88bd68bee3' 
    request.open("POST", "https://accounts.spotify.com/api/token", true);
    request.setRequestHeader("Authorization", "Basic: "+ btoa(clientid+':'+client_secret));
    request.setRequestHeader("Access-Control-Allow-Origin", true);
    request.send("grant_type=client_credentials");
}

$.ajax({
    url: "https://api.spotify.com/v1/search?type=track&q=artist:chance%20the%20rapper&limit=50",
    type: "GET",
    headers: {
        'Authorization': "Bearer BQDVvRy6kL9alEU666LFb9dkRbUSR4BkazZDieMCw9lDnSrQlu0e-HjuOXN6-xeyNUWf2zzTSbLdvpbYnIw",
            'Accept': "application/json",
            'Content-Type': "application/json"},
    success: function (result) {
        window.resu = result
        console.log(result)
        },
    error: function (error) {
          console.log(damn)  
        }

});