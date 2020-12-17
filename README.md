# News-service
This project is backend service developed to provide NEWS APIs and database access for front-end applications.   
This service is hosted in heroku and actively integrated with the [front-end news repository](https://github.com/vinay-raghava/news-app) which is hosted in netlify.  
You can find the live website [here](https://vinay-news-app.netlify.app/).  

Note: This service internally uses [open NEWS API](https://newsapi.org/) to get the latest news.

## Development server
- Open command prompt, create virtual environment using `python3 -m venv <path to new virtual environment>` and activate virtual environment.
- Run `pip install -r requirements.txt`
- Set the environment variables `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`.
- Go to https://newsapi.org/ and get the API key according to your requirement and set `NEWS_API_KEY` to your key.
- Run `run.py` file and you can find the server hosted on `http://localhost:5000/`. 
