import PetApi from "/static/helper.js";

let petApi = new PetApi();
start();

async function start() {
  let type = $("#data").data("type");
  let location = $("#data").data("location");
  await petApi.getToken();
  let pets = await petApi.getPets(type, location);
  createPetList(pets);
}

function createPetList(pets) {
  $("#pet-list").empty();
  let $pet = $("#pet-clone > .pet");

  for (let p of pets) {
    let photo = p.photos[0] ? p.photos[0].medium : "";
    let $newPet = $pet.clone();
    $newPet.find(".card-img-top").attr("href", `/pet/${p.id}`);
    $newPet.find(".pet-name").text(p.name);
    $newPet.find(".pet-img").attr("src", photo);
    if (p.distance != null) {
      let distance = Math.round(p.distance * 10) / 10;
      $newPet.find(".distance").text(`${distance} miles away`);
    }

    $("#pet-list").append($newPet);
  }
}

// $("#search-sumbit").on("click", async function (e) {
//   e.preventDefault();
//   let type = $("#type").val();
//   let location = $("#location").val();
//   let pets = await petApi.getPets(type, location);
//   createPetList(pets);

//   let query = "?";
//   query += `type=${type}`;
//   if (location) query += `&location=${location}`;
//   window.history.pushState(null, null, query);
// });

$("#search-sumbit").on("click", async function (e) {
  e.preventDefault();
  let type = $("#type").val();
  let location = $("#location").val();
  let query = "?";
  if (type && location) query += `type=${type}&location=${location}`;
  else if (type) query += `type=${type}`;
  else if (location) query += `location=${location}`;
  window.location = query;
});
