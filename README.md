# github_gist_api

<h2>Overview</h2>
This is a web application created in Python, using Django. It allows users to view public GitHub gists.

<h2>Functionality</h2>
* Allows users to list the public gists of GitHub users by entering their username
* For each gist:
    * Display tags indicating the type of the files contained in the gist
    * Display the 3 most recent users who have forked the gist
    * Display the names of the files contained in the gist.
      By clicking on a file name, the content of the file will be shown

<h3>Additional features and optimizations</h3>
* The gists can be filtered by the tags so that only the gists that contain a certain file type are shown
* While viewing the latest users that have forked a gist,
  clicking a fork user's username will display the gists of the clicked user
* Taking into account that a gist can be forked by a great number of people,
  an optimization has been made in order to reduce the time needed for the web application to load
    * The requests needed in order to retrieve the fork users are only made when asked for
    * The web application user asks for a gist's fork users by clicking the ``Latest Forks`` button

<h3>Further developments and optimizations</h3>
The web application can be developed and optimized further
* Apply pagination when displaying the gists of a user and
  request from the GitHub API only those gists that are part of the current page
* Integrate authentication with the GitHub account into the web application
  in order to raise the number of requests that a user can make.
  An unauthenticated user is limited to only 60 requests per hour
* Add the possibility to search for a specific gist

<h3>Dependencies</h3>
> pip install django

> pip install requests