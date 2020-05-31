import PetApi from "/static/helper.js";

let petApi = new PetApi();

start();

async function start() {
  let $currPets = $("#curr-pet-list > .pet");
  fillPetList($currPets);
  let $pastPets = $("#past-pet-list > .pet");
  fillPetList($pastPets);
}

async function fillPetList($petlist) {
  for (let elem of $petlist) {
    let id = $(elem).data("id");
    let data = await petApi.getPet(id);
    let avg = data.rating;
    let pet = data.animal;
    // console.log(data, avg);
    fillPet(elem, pet, avg);
  }
}

function fillPet(elem, p, avg) {
  let photo = p.photos[0] ? p.photos[0].medium : "";
  let $pet = $(".pet");
  let $elem = $(elem);
  $elem.data("id", p.id);
  $elem.find(".pet-name").text(p.name);
  $elem.find(".avg").text(avg);

  $elem.find(".pet-img").attr("src", photo);
  let $ratingElem = $elem.find(".rating");
  let rating = $ratingElem.data("rating");
  // console.log($ratingElem, rating);
  fillStars($ratingElem, rating);
}

$(".rating i").click(async function (e) {
  let rating = $(this).index() + 1;
  let obj = {
    rating: rating,
  };
  let id = $(this).closest(".pet").data("bookid");
  let resp = await axios.post(`booking/${id}/rating`, obj);
  // console.log(resp);

  let $ratingElem = $(this).parent(".rating");
  fillStars($ratingElem, rating);
});

function fillStars($ratingElem, rating) {
  let $stars = $ratingElem.children();
  $stars.removeClass("text-warning");
  for (let i = 0; i < rating; i++) {
    $stars.eq(i).addClass("text-warning");
  }
}
