const form = document.querySelector(".top-banner form");
const input = document.querySelector(".top-banner input");
const msg = document.querySelector(".top-banner .msg");
const list = document.querySelector(".ajax-section .cities");
const apiKey = "95f9c30fc9fb4dc296a194754241606";

form.addEventListener("submit", e => {
  e.preventDefault();
  let inputVal = input.value.trim();

  // Check if the city is already displayed
  const listItems = list.querySelectorAll(".ajax-section .city");
  const listItemsArray = Array.from(listItems);

  if (listItemsArray.length > 0) {
    const filteredArray = listItemsArray.filter(el => {
      let content = "";
      // Check if inputVal includes a country code
      if (inputVal.includes(",")) {
        // If country code is invalid, use only the city name
        if (inputVal.split(",")[1].length > 2) {
          inputVal = inputVal.split(",")[0];
        }
        content = el.querySelector(".city-name").dataset.name.toLowerCase();
      } else {
        content = el.querySelector(".city-name span").textContent.toLowerCase();
      }
      return content == inputVal.toLowerCase();
    });

    if (filteredArray.length > 0) {
      msg.textContent = `You already know the weather for ${
        filteredArray[0].querySelector(".city-name span").textContent
      } ...otherwise be more specific by providing the country code as well 😉`;
      form.reset();
      input.focus();
      return;
    }
  }

  // Fetch weather data from WeatherAPI
  const url = `https://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${inputVal}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        msg.textContent = "Please search for a valid city 😩";
        return;
      }
      
      const { location, current } = data;
      const { name, country } = location;
      const { temp_c, condition, wind_kph, humidity } = current;
      const icon = condition.icon;

      const li = document.createElement("li");
      li.classList.add("city");
      const markup = `
        <h2 class="city-name" data-name="${name},${country}">
          <span>${name}</span>
          <sup>${country}</sup>
        </h2>
        <div class="city-temp">${Math.round(temp_c)}<sup>°C</sup></div>
        <figure>
          <img class="city-icon" src="${icon}" alt="${condition.text}">
          <figcaption>${condition.text}</figcaption>
        </figure>
        <div class="city-wind">Wind: ${wind_kph} kph</div>
        <div class="city-humidity">Humidity: ${humidity}%</div>
      `;
      li.innerHTML = markup;
      list.appendChild(li);
    })
    .catch(() => {
      msg.textContent = "Please search for a valid city 😩";
    });

  msg.textContent = "";
  form.reset();
  input.focus();
});
