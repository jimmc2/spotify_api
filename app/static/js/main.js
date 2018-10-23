var myData = {
  artist:'',
  tracks:[],
  featuredArtists:[],
  next:'start',
  fullD:[]
}
$(document).ready(function () {
  // setup the button click
$("#ArtistForm").submit(function(event) {
    event.preventDefault();
    document.getElementById("theButton").disabled = true;
    console.log(document.querySelector('#Artist').value)
    query(document.querySelector('#Artist').value,myData.token)
    console.log('query')
    document.getElementById("theButton").disabled = false;
    return false
  })
})


function query(artist, token){
  let headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + window.myData.token
  }
  myData.artist=''
  myData.tracks=[]
  myData.featuredArtists=[]
  var myNode = document.querySelector("#tbody");
  while (myNode.firstChild) {
    myNode.removeChild(myNode.firstChild);
}
  featureSongs(artist, headers);
  dupes();
  cleanSongs();
  displayArtists();
  doWork();
}

function jsonRequest(url, head){
  $.ajax({
    async:false,
    url: url,
    success: function(d)
        {
          console.log('success')
          myData.fullD = d
          let featureTracks = [];
          if(myData.artist == ''){
            let artist = d.tracks.items[0].artists[0].id
            myData.artist = artist}
          for(let song = 0;song<d.tracks.items.length;song++){
            if (d.tracks.items[song].artists.length>1 && d.tracks.items[song].artists[0].id == myData.artist){
              featureTracks.push(d.tracks.items[song]);
            };
          };
          myData.next = d.tracks.next
          myData.tracks.push.apply(myData.tracks, featureTracks)},
    error:function(_, text, error){console.log(text);console.log(error);console.log('error')},
    headers: head
  });
}

function featureSongs(artist, head) {
    let url = "https://api.spotify.com/v1/search?type=track&q=artist:"+ artist + "&limit=50"
    let header = head
    jsonRequest(url,header)
    while (window.myData.next){
      jsonRequest(window.myData.next, header)
    }
}
function dupes(){
  let tracks_to_remove = new Set([])
  for(let i = 0; i<myData.tracks.length;i++){
     if(tracks_to_remove.has(i)){}
     else {
       for(let j = 0; j<myData.tracks.length;j++){
         if(i == j){}
         else if(myData.tracks[i].name == myData.tracks[j].name){
          tracks_to_remove.add(j)
          console.log(i,' & ', j)
         }
       } 
     }
  }
  tracks_to_remove_array = Array.from(tracks_to_remove)
  tracks_to_remove_array.sort(function(a, b){return b-a})
  for(let index=0; index< tracks_to_remove_array.length;index++){
    console.log('removing', myData.tracks[tracks_to_remove_array[index]].name)
    myData.tracks.splice(tracks_to_remove_array[index],1)
    console.log('removed: ', tracks_to_remove_array[index])
  }
}
function cleanSongs(){
  for(let i = 0; i <myData.tracks.length; i++){
    let songName = myData.tracks[i].name
    let track = myData.tracks[i]
    for(let j = 0;j<myData.tracks[i].artists.length;j++){
      let artist = track.artists[j]
      if(artist.id == myData.artist){}
      else if(artist.name in myData.featuredArtists){
        myData.featuredArtists[artist.name].songs.push(songName)
        myData.featuredArtists[artist.name].count++
      }
      else{
        myData.featuredArtists[artist.name]= {};
        myData.featuredArtists[artist.name].name= artist.name;
        myData.featuredArtists[artist.name].songs = [songName];
        myData.featuredArtists[artist.name].count = 1;
      }
    }
  }
}
function displayArtists(){
  var tbody = document.querySelector('#tbody')
  for(let i = 0; i<Object.keys(myData.featuredArtists).length;i++){
    var trow = document.createElement("tr")
    var tname = document.createElement("td")
    var nodeName = document.createTextNode(myData.featuredArtists[Object.keys(myData.featuredArtists)[i]].name)
    tname.appendChild(nodeName)
    var tsongs = document.createElement("td")
    var nodeSongs = document.createTextNode(myData.featuredArtists[Object.keys(myData.featuredArtists)[i]].songs)
    tsongs.appendChild(nodeSongs)
    var tcount = document.createElement("td")
    var nodeCount = document.createTextNode(myData.featuredArtists[Object.keys(myData.featuredArtists)[i]].count)
    tcount.appendChild(nodeCount)
    trow.appendChild(tname)
    trow.appendChild(tsongs)
    trow.appendChild(tcount)
    tbody.appendChild(trow)
  }
}

function doWork() {
  // ajax the JSON to the server
  $.ajax({
    type: "POST",
    url: "/receiver",
    data: JSON.stringify(myData),
    success: function(){ console.log("success")},
    dataType: "json",
    contentType: "application/json"
  });
  
  // stop link reloading the page
event.preventDefault();
}