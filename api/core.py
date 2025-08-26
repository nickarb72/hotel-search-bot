from loader import bot_settings

api_host = "booking-com15.p.rapidapi.com"

url = f"https://{api_host}/api/v1/hotels/"

rapid_api_key = bot_settings.RAPID_API_KEY.get_secret_value()

headers = {
	"x-rapidapi-key": rapid_api_key,
	"x-rapidapi-host": api_host
}


