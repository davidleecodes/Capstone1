import PetApi from "/static/helper.js";

let petApi = new PetApi();

start();

async function start() {
  let id = $(".pet").data("id");
  console.log("id", id);
  let data = await petApi.getPet(id);
  let pet = data.animal;
  createPet(pet);
  console.log(data);
  console.log(data.animal.description);
}

function createPet(p) {
  let photo = p.photos[0] ? p.photos[0].medium : "";
  let $pet = $(".pet");
  $pet.data("id", p.id);
  $pet.find(".pet-img").attr("src", photo);
  if (photo) {
    $pet.find(".fa-paw").hide();
  } else {
    $pet.find(".pet-img").hide();
  }

  $pet.find(".pet-name").text(p.name);
  $pet.find(".pet-breed").text(p.breeds.primary);
  $pet.find(".pet-city").text(p.contact.address.city);

  $pet.find(".pet-age").text(p.age);
  $pet.find(".pet-gender").text(p.gender);
  $pet.find(".pet-size").text(p.size);
  let $about = $pet.find(".about");
  Object.entries(p.attributes).forEach(([obj, val]) => {
    console.log(obj, val);
    obj = obj.replace("_", "-");
    if (val) {
      $about.append(`<span class="mx-2">${obj}</span>`);
    }
  });

  $pet.find(".pet-description").text(p.description);
}

let dates = $("#book_form").data("booked") || [];
let $start = $('input[name="start_date"]');
let $end = $('input[name="end_date"]');
let today = new Date().toISOString().slice(0, 10);

addDatePicker($start);
addDatePicker($end);

function addDatePicker($elem) {
  $elem.attr("type", "");
  $elem.datepicker({
    dateFormat: "yy-mm-dd",
    minDate: today,
    beforeShowDay: function (date) {
      var string = jQuery.datepicker.formatDate("yy-mm-dd", date);
      return [dates.indexOf(string) == -1];
    },
  });
}
