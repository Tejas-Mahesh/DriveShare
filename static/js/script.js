// =========================
// Back To Top Button
// =========================

const backToTop = document.getElementById("backToTop");

if (backToTop) {

    window.addEventListener("scroll", () => {

        if (window.scrollY > 400) {
            backToTop.classList.add("show");
        } else {
            backToTop.classList.remove("show");
        }

    });

    backToTop.addEventListener("click", () => {

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    });

}


// =========================
// Loader
// =========================

window.addEventListener("load", function () {

    const loader = document.getElementById("loader");

    if (loader) {

        setTimeout(function () {

            loader.classList.add("loader-hidden");

        }, 1800);

    }

});


// =========================
// Mobile Menu
// =========================

const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.getElementById("nav-links");

if (menuToggle && navLinks) {

    menuToggle.addEventListener("click", function () {

        menuToggle.classList.toggle("active");
        navLinks.classList.toggle("active");

    });

}


// =========================
// Navbar Scroll Effect
// =========================

window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".navbar");

    if (!navbar) return;

    if (window.scrollY > 80) {

        navbar.classList.add("scrolled");

    } else {

        navbar.classList.remove("scrolled");

    }

});


// =========================
// Dashboard / Home Counters
// =========================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    const target = Number(counter.dataset.target);

    let current = 0;

    const increment = target / 100;

    function updateCounter() {

        if (current < target) {

            current += increment;

            counter.innerText = Math.ceil(current);

            requestAnimationFrame(updateCounter);

        } else {

            if (target === 49) {

                counter.innerText = "4.9★";

            } else {

                counter.innerText = target + "+";

            }

        }

    }

    updateCounter();

});