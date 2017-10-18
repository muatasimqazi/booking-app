$(document).ready(function() {
  // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
  $('.modal').modal();

  $('.button-collapse').sideNav({
    menuWidth: 300, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true, // Choose whether you can drag to open on touch screens,
  });


$('.datepicker').addClass('picker--focused picker--opened');

  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    ariaHidden: true,
    closeOnSelect: false // Close upon selecting a date,
  });
  $('.picker').addClass('pickers');


  $('#calendar').fullCalendar({
        // put your options and callbacks here
        weekends: false // will hide Saturdays and Sundays
    })
});
