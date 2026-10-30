"use strict";

(function ($) {

  /* ===============================
     Mobile Menu
  =============================== */
  $('.menu-click').on('click', function () {
    $('.openmobile-menu').addClass('active-mobile-menu');
    $('.rt-mobile-menu-overlay').addClass('active');
  });

  $('.rt-mobile-menu-close, .rt-mobile-menu-overlay').on('click', function () {
    $('.openmobile-menu').removeClass('active-mobile-menu');
    $('.rt-mobile-menu-overlay').removeClass('active');
  });

  /* ===============================
     Accordion
  =============================== */
  $('.accrodain-button').on('click', function () {

    const parent = $(this).parent();

    if (parent.hasClass('open')) {

      parent.removeClass('open');
      parent.find('.content').slideUp(250);

    } else {

      $('.accrodains li').removeClass('open');
      $('.accrodains .content').slideUp(250);

      parent.addClass('open');
      parent.find('.content').slideDown(250);

    }
  });

  /* ===============================
     Sticky Header
  =============================== */
  const header = $('.rt-sticky');

  $(window).on('scroll', function () {

    if ($(window).scrollTop() > 100) {

      header.addClass('rt-sticky-active');

    } else {

      header.removeClass('rt-sticky-active');

    }
  });

  /* ===============================
     Isotope Blog Filter
  =============================== */
  if ($('.grids').length) {

    $('.grids').imagesLoaded(function () {

      const $grid = $('.grids').isotope({
        itemSelector: '.grid-item',
        percentPosition: true
      });

      $('.filter-list').on('click', 'li', function () {

        $('.filter-list li').removeClass('active');
        $(this).addClass('active');

        const filterValue = $(this).attr('data-filter');

        $grid.isotope({
          filter: filterValue
        });

      });

    });
  }

})(jQuery);
