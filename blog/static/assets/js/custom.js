document.addEventListener('DOMContentLoaded', function () {


const imageSlider = new Swiper('.testimonial-image-slider', {

loop:true,

speed:700,

effect:'fade',

fadeEffect:{
crossFade:true
},

allowTouchMove:false

});



const textSlider = new Swiper('.testimonial-text-slider', {

loop:true,

speed:700,

autoHeight:true,


navigation:{

nextEl:'.testimonial-next',

prevEl:'.testimonial-prev'

}

});



imageSlider.controller.control = textSlider;

textSlider.controller.control = imageSlider;



});

