const set_city = function(id){
    parag = document.getElementsByClassName("p_city")[id];
    parag.innerText = `Temperature: fetching... Humidity: fetching...`;
    fetch_weather(id).then(response => {
        //parag.innerText = response.current;
        parag.innerText = `Temperature: ${response.current.temperature_2m} ${response.current_units.temperature_2m} Humidity: ${response.current.relative_humidity_2m} ${response.current_units.relative_humidity_2m}`;
    })    
}

const fetch_weather = function(id){
    var current_weather = fetch(cities_list[Object.keys(cities_list)[id]])
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response error');
            }
            return response.json();
        })
        .catch(error => console.error('Fetch error:', error));
    return current_weather;
}

const populate_cities_container = function(cities_list){
    let city_lines = [];
    for (let i = 0; i < Object.keys(cities_list).length; i++) {
        city_lines[i] = document.createElement("div");
        city_lines[i].className = "l_city";
        let button = document.createElement("button");
        button.className = "b_city"
        button.textContent = Object.keys(cities_list)[i];
        button.addEventListener("click", function(){ set_city(i); }, false); // Passing parameters to an attached function requires wrapping it in an anonymous function
        city_lines[i].appendChild(button);
        let parag = document.createElement("p");
        parag.className = "p_city"
        const text_node = document.createTextNode("...");
        parag.appendChild(text_node);
        city_lines[i].appendChild(parag);
        document.getElementById("cont_weather").appendChild(city_lines[i]);
}
}