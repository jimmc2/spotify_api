query = (artist) => {
    json_request = ()=> {}
    feature_songs = (artist) => {
        let feature_songs = []
        let url = "https://api.spotify.com/v1/search?type=track&q=artist:"+ str(artist) + "&limit=50"
        let search_json = json_request(url, headers)
    for (let i=0; i < search_json['tracks']['items'].length; i++) {
        let item = search_json['tracks']['items'][i]
        if (item['artists'].length >1 ){
            feature_songs.push(item)
            }
        }
    while (search_json['tracks']['next']){
        url = search_json['tracks']['next']
        search_json = json_request(url, headers)
        for (let j = 0; j < search_json['tracks']['items'].length; j++){
            item = search_json['tracks']['items'][j]
            if (item['artists'].length>1){
                feature_songs.push(item)
                }
            }
        }
    return feature_songs
    }
}