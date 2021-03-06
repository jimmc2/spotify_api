var myData = {
  artist:'',
  tracks:[],
  featuredArtists:[],
  next:'start',
  fullD:[]
}

var targetUrl;
var currentlyMakingRequest;
var allRequestsCompleted;
var intervalId;

$(document).ready(function () {
  // setup the button click
  $("#ArtistForm").submit(function(event) {
      event.preventDefault();
      var button = $("#theButton");
      var artist = $("#Artist");
      var progress = $("#searchProgress");
      $("#theButton").prop("disabled", "disabled");
      $("#Artist").prop("disabled", "disabled");
      $("#searchProgress").show();

      query(artist.val())
      return false
    })
})


function query(artist){
  
  let headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + window.myData.token
  }
  myData.artist=''
  myData.tracks=[]
  myData.featuredArtists=[]
  $("#tbody").empty();

  let url = "https://api.spotify.com/v1/search?type=track&q=artist:"+ artist + "&limit=50"

  allRequestsCompleted = false;
  currentlyMakingRequest = false;
  targetUrl = url;

  intervalId = window.setInterval(() =>{
    if(!currentlyMakingRequest && !allRequestsCompleted){

      currentlyMakingRequest = true;
      jsonRequest(targetUrl,headers)
    }
    if(allRequestsCompleted){
      window.clearInterval(intervalId);
    }
  }, 100);
}

function jsonRequest(url, head){

  $.ajax({
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
          myData.next = d.tracks.next;
          myData.tracks.push.apply(myData.tracks, featureTracks);
          if(!myData.next){
            allRequestsCompleted = true;
            dupes();
            cleanSongs();
            displayArtists();
            doWork();
            
            $("#theButton").removeAttr("disabled");
            $("#Artist").removeAttr("disabled");
            $("#searchProgress").hide();
          } else{
            targetUrl = myData.next;
          }
          currentlyMakingRequest = false;
        
        },
    error:function(_, text, error){console.log(text);console.log(error);console.log('error')},
    headers: head
  });
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