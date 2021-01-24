import PetApi from "/static/helper.js";

let petApi = new PetApi();
let type = $("#data").data("type");
let location = $("#data").data("location");
let page = $("#data").data("page");

if (page === 1) $(".prev").hide();
if (page > 1) $(".prev").show();

start();

async function start() {
  let pets = await petApi.getPets(type, location, page);
  let types = await petApi.getTypes();
  types = types.types.map((t) => {
    return { name: t.name, link: t._links.self.href };
  });
  console.log(pets);
  if (pets.status === 400) window.location = "/";
  let pagination = pets.pagination;
  if (page === pagination.total_pages) $(".next").hide();
  console.log(pets);
  createPetList(pets.animals);
  createPetTypes(types);
  createPageNums(pagination);
}

function createPageNums(pagination) {
  let $pageNums = $("#page-name");
  console.log($pageNums);
  for (let i = 1; i < pagination.total_pages; i++) {
    $pageNums.append(
      `<option data-page="${i}"> page ${i}/${pagination.total_pages}</option>`
    );
  }
  $pageNums.prop("selectedIndex", pagination.current_page - 1);
}

function createPetTypes(types) {
  let $list = $(".pet-types");

  for (let t of types) {
    let link = t.link.slice(10);
    $list.append(`<option data-link="${link}">${t.name}</option>`);
  }
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
    if (photo) {
      $newPet.find(".fa-paw").hide();
    }
    if (p.distance != null) {
      let distance = Math.round(p.distance * 10) / 10;
      $newPet.find(".distance").text(`${distance} miles away`);
    }

    $("#pet-list").append($newPet);
  }
}

function queryBuild() {
  let qType = $("#type").find("option:selected").data("link");
  if (!qType && type !== "None") qType = type;
  let qLocation = $("#location").val() || location;
  let query = "?";

  if (qType && qLocation) query += `type=${qType}&location=${qLocation}`;
  else if (qType) query += `type=${qType}`;
  else if (qLocation) query += `location=${qLocation}`;
  console.log(query, qLocation, qType);
  return query;
}

$("#search-sumbit").on("click", async function (e) {
  e.preventDefault();
  window.location = queryBuild();
});

$("#page-name").on("change", async function (e) {
  e.preventDefault();
  let page = $("#page-name").find("option:selected").data("page");
  let query = queryBuild();
  query += `&page=${page}`;
  console.log(query);
  window.location = query;
});

$(".prev").on("click", async function (e) {
  e.preventDefault();
  let query = queryBuild();
  query += `&page=${page - 1}`;
  console.log(query);
  window.location = query;
});

$(".next").on("click", async function (e) {
  e.preventDefault();
  let query = queryBuild();
  query += `&page=${page + 1}`;
  console.log(query);
  window.location = query;
});
