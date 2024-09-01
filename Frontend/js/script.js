'use strict';

/**
 * navbar toggle
 */

const overlay = document.querySelector("[data-overlay]");
const navOpenBtn = document.querySelector("[data-nav-open-btn]");
const navbar = document.querySelector("[data-navbar]");
const navCloseBtn = document.querySelector("[data-nav-close-btn]");
const navLinks = document.querySelectorAll("[data-nav-link]");

const navElemArr = [navOpenBtn, navCloseBtn, overlay];

const navToggleEvent = function (elem) {
  for (let i = 0; i < elem.length; i++) {
    elem[i].addEventListener("click", function () {
      navbar.classList.toggle("active");
      overlay.classList.toggle("active");
    });
  }
}

navToggleEvent(navElemArr);
navToggleEvent(navLinks);



/**
 * header sticky & go to top
 */

const header = document.querySelector("[data-header]");
const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {

  if (window.scrollY >= 200) {
    header.classList.add("active");
    goTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    goTopBtn.classList.remove("active");
  }

});



// async function fetchRatings() {
//     try {
//         const response = await fetch('http://localhost:5000/api/ratings'); // Adjust URL as needed
//         if (!response.ok) throw new Error('Network response was not ok.');
//         const data = await response.json();
//         return data;
//     } catch (error) {
//         console.error('Error fetching ratings:', error);
//         return [];
//     }
// }

// async function renderChart() {
//     const ratingsData = await fetchRatings();
//     const labels = [];
//     const data = [];
//     for (let i = 1; i <= 5; i++) {
//         const rating = ratingsData.find(r => r._id === i);
//         labels.push(i);
//         data.push(rating ? rating.count : 0);
//     }

//     const ctx = document.getElementById('ratingsChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: labels,
//             datasets: [{
//                 label: 'Number of Ratings',
//                 data: data,
//                 backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// }

// document.addEventListener('DOMContentLoaded', renderChart);