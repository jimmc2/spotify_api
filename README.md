# SpotifyAPI Artist Feature Search

Project used to find common collaborators of a user's favorite artist and give the opportunity to listen to the songs. 

## What's inside

App runs a post request to Spotify to gain temporary access to query the api. The front-end runs artist AJAX requests based on user searches and then sends another AJAX to a python receiver route to submit to the database.

### To-Do List

* Add function to query artist genres for a genre pairing capability where a user can select two genres and fitting songs would appear
* Multi-Artist search: Find songs done by two artists
* back-end queries to retrieve full artist and song objects for advanced calculations
* host it