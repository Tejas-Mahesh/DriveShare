const hero = document.querySelector(".hero");

const images = [

"/static/images/hero1.jpg",

"/static/images/hero2.jpg",

"/static/images/hero3.jpg",

];

let current = 0;

function changeBackground(){

hero.style.backgroundImage =

`linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.55)),url(${images[current]})`;

current++;

if(current===images.length){

current=0;

}

}

changeBackground();

setInterval(changeBackground,4000);