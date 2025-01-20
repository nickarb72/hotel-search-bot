from config_data import config


api_host = "booking-com15.p.rapidapi.com"

url = f"https://{api_host}/api/v1/hotels/"

headers = {
	"x-rapidapi-key": config.RAPID_API_KEY,
	"x-rapidapi-host": api_host
}


