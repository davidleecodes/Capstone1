import PetApi from "/static/helper.js";

let petApi = new PetApi();

start();

async function start() {
  let id = $(".pet").data("id");
  console.log("id", id);
  let data = await petApi.getPet(id);
  let pet = data.animal;
  createPet(pet);
}

function createPet(p) {
  let photo = p.photos[0] ? p.photos[0].medium : "";
  let $pet = $(".pet");
  $pet.data("id", p.id);
  $pet.find(".pet-img").attr("src", photo);
  $pet.find(".pet-name").text(p.name);
  $pet.find(".pet-breed").text(p.breeds.primary);
  $pet.find(".pet-gender").text(p.gender);
  $pet.find(".pet-city").text(p.contact.address.city);
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
