"use strict";

$(document).ready(function() {
    var swiper = new Swiper('.swiper-main');
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: 7000,
      values: [ 300, 1800 ]
    });
});