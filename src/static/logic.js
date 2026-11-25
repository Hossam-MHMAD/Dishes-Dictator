
// template design 
document.documentElement.classList.add("js");
var links = document.getElementById("links"), menu = document.getElementById("menu");
menu.addEventListener("click", function () {
  var open = links.classList.toggle("open");
  menu.setAttribute("aria-expanded", open);
});
links.addEventListener("click", function (e) { if (e.target.tagName === "A") { links.classList.remove("open"); menu.setAttribute("aria-expanded", false); } });

var els = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
  }, { threshold: .15 });
  els.forEach(function (el) { io.observe(el); });
} else { els.forEach(function (el) { el.classList.add("in"); }); }

// The week resets at the start of this weekday (0 = Sunday ... 6 = Saturday).
var RESET_DAY = 0;
function tick() {
  var now = new Date();
  var next = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  var add = (RESET_DAY - now.getDay() + 7) % 7;
  next.setDate(next.getDate() + (add === 0 ? 7 : add));
  var s = Math.max(0, Math.floor((next - now) / 1000));
  document.getElementById("d").textContent = Math.floor(s / 86400);
  document.getElementById("h").textContent = Math.floor(s % 86400 / 3600);
  document.getElementById("m").textContent = Math.floor(s % 3600 / 60);
}
tick(); setInterval(tick, 30000);

// APIs 
const APIs = {
  leader_board: "/api/leader-board",
  current_dictator: "/api/week_dictator"
}

// landing page setup
async function get_current_dictator() {
  const response = await fetch(APIs.current_dictator)
  const data = await response.json()

  return data
}

async function get_leader_board() {
  const response = await fetch(APIs.leader_board)
  const data = await response.json()

  return data
}

async function init_landing_page() {
  // Dictator Card
  const dic_card_container = document.querySelector(".throne")
  const dictator_name = dic_card_container.querySelector("h2")
  const points = dic_card_container.querySelector(".pts")

  const current_dictator_data = await get_current_dictator()

  dictator_name.textContent = current_dictator_data.week_dictator || "-------"
  points.textContent = `with ${current_dictator_data.winning_points || "0"} winning points`

  // Leader Board
  const leader_board_container = document.querySelector("#board").querySelector("ol")

  const leader_board_data = await get_leader_board()

  leader_board_container.innerHTML = ""

  leader_board_data.forEach(cleaner => {
    const row = `
      <li><span>${cleaner.name}</span><b>${cleaner.points} pts</b></li>
    `
    leader_board_container.innerHTML += row
  })
}

if (document.querySelector(".landing_page")) {
  init_landing_page()
}

