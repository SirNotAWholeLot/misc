// This really should be a database-like file containing city names and corresponding API links, but I haven't figured out how to do that properly yet
//import cities_list from './cities_list.json' assert {type : 'json'}; // Reading from a local file seems much more difficult in JS
var cities_list = {
    "Rome": "https://api.open-meteo.com/v1/forecast?latitude=41.8919&longitude=12.5113&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day&forecast_days=1",
    "Paris": "https://api.open-meteo.com/v1/forecast?latitude=48.8534&longitude=2.3488&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day&forecast_days=1"
};//*/
