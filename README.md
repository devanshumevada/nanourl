## NanoURL

[NanoURL](http://nanourl.xyz "NanoURL") is a service that creates shorter aliases for lengthy URLs.


------------

#### Technical Specifications
1. Based on: **Flask (Python)**
2. Email Api: **SendGrid**
3. Deployed On: **Heroku**
4. Database: **MongoDB**
5. Caching: **MemCachier**

------------

#### Api Routes and usage
1. **/api/links - GET**: Returns all shorted URLs and related metadata for a particular user
2. **/api/link - POST**: Short a long URL. Json data with the format {"url":URL_TO_BE_SHORTED} needs to be passed within the request body
3. **/api/link?short_code=SHORT_CODE - GET**: Returns the metadata of a short url
4. **/api/link?short_code=SHORT_CODE - DELETE**:
Deletes the short url from the database

**All the API routes mentioned above need 'Authorization':AUTH_TOKEN in the header. Auth token can be obtained from a user's account dashboard**

