# Hotzone
Software engineering course project

## Description 
This is a pilot web application that aims to assist the Centre for Health Protection with data management and contact tracing for COVID-19 cases.

### Jira link

https://hotzone.atlassian.net/

### App link

https://hotzoneteamg.herokuapp.com/

## Current limitations

* Using Django built-in forms for creating a new entries, might not be easy to customise in case of extra needs from client
* Choosing multiple locations in a scroll box for creating a case record: might be hard to look for the right matches if the list is long
* The "select location" in the add case form is not that user friendly, since it only displays coordinates as options, which may be very hard to remember on a case by case basis

### Release 1

- [x] Get GeoData with location search API


### Release 2

- [x] Authentication
- [x] Selection of location in case of multiple matches
- [x] Create and view confirmed case records
- [x] Create and view virus records
- [x] Create and view patient records

### Release 3

- [x] Simple clustering

