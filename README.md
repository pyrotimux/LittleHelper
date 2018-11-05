# LittleHelper
Test project to retrieve movies and tv shows from flask rest api. In order to gather the dataset required, I used the titles retrieved from wikidata and queried the rest of the info needed from omdb using their api. This script lives under scraper folder to semi-automate this procedure.


### Getting Started

The current version of the API lives at ```http://35.235.66.151/```.

examples: ```http://35.235.66.151/show/841```  ```http://35.235.66.151/movie/1```  

```http://35.235.66.151/search?query=the&page=5&limit=35```

To run this project, you will need docker installed. Once project is cloned then go into the folder and run ```docker-compose up``` which will bring up both containers.

#### Containers

| Containers | What it does |
| ------------- | -------------|
| ```lhdb``` | mysql db container.
| ```lhapp``` | flask app that host the application.

#### Endpoints

| Endpoint | What it does |
| ------------- | -------------|
| ```/movie/${id}``` | when given the appropriate id, will yield the movie matching that identifier.
| ```/show/${id}``` | when given the appropriate id, will yield the show matching that identifier.
| ```/search``` | when given a query, will yield any movies or shows matching that title.

#### Supported Request Args

| Args | What it does | Endpoint |
| ------------- | -------------| -------------|
| ```page``` | page number to retrieve. | all
| ```limit``` | number of items in one page. | all
| ```query``` | title of the movie or show. | search only

<body id="basics"></body>