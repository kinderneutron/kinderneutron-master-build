const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");

inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});
index1 =1;
function moveSlider() {
 
  //let index = this.dataset.value;
  index1 = (index1 +1)
  if(index1==4)
  {
    index1=1
  }
  let currentImage = document.querySelector(`.img-${index1}`);
   images.forEach((img) => img.classList.remove("show"));
   currentImage.classList.add("show");

 colours = ['#d35858','#fedb2a','#040401']
 
  bullets.forEach((bull) => bull.classList.remove("active"));
  //this.classList.add("active");
  
  document.getElementsByTagName('main')[0].style.backgroundColor = colours[index1-1]

}

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});

setInterval(moveSlider, 3000);
