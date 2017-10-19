$(document).ready(function() {
  // the "href" attribute of the modal trigger must specify the modal ID that wants to be triggered
  $('.modal').modal();

  $('.button-collapse').sideNav({
    menuWidth: 300, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true, // Choose whether you can drag to open on touch screens,
  });

$( ".ui-draggable" ).draggable();

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
        weekends: false, // will hide Saturdays and Sundays
          defaultView: 'agendaDay',
          header: {
            left: 'prev,next today myCustomButton',
            center: 'title',
            right: 'agendaDay,agendaWeek,month,listDay'
          },
          columnFormat: 'ddd',
          displayEventEnd: true,
          // durationEditable: true,
          editable: true,
          eventStartEditable: true,
          eventOverlap: false,
          eventConstraint: {
            start: '09:00', // a start time (10am in this example)
            end: '15:00', // an end time (5pm in this example)
            dow: [1, 2, 3, 4, 5]
    // days of week. an array of zero-based day of week integers (0=Sunday)
    // (Monday-Thursday in this example)
},

eventRender: function (event, element) {
       element.attr('href', '#event-modal');
       element.addClass('modal-trigger');
       element.click(function() {

           $("#event-content").html(
              '<h5>' + event.title + '</h5>' +
              '<p>' + moment(event.start).format('MMM Do h:mm A') + '</p>'
           );
       });
   },
eventDrop: function(event, delta, revertFunc) {

        alert(event.title + " was dropped on " + event.start.format());

        if (!confirm("Are you sure about this change?")) {
            revertFunc();
        }

    },
    events: [
            {
                title  : 'Furnace Repair',
                start: '2017-10-18T10:00:00',
                end: '2017-10-18T11:00:00'

            },
            {
                title  : 'event2',
                start  : '2017-10-19T09:00:00',
                end    : '2017-10-19T10:00:00',
            }

        ],


  //       businessHours: [{
  //   dow: [0, 1, 2, 3, 4, 5, 6], // Maybe not 0,6? Sunday,Saturday
  //   start: '08:00',
  //   end: '12:00'
  // }, {
  //   dow: [0, 1, 2, 3, 4, 5, 6], // Maybe not 0,6? Sunday,Saturday
  //   start: '13:00',
  //   end: '18:00'
  // }],


  viewRender: function(view, element) {
    if (view.name.substr(0, 6) === 'agenda') {
      $(element).find('div.fc-slats table tr[data-time]').filter(function() {
        var _t = $(this).data('time');
        /* find times not in the ranges we want */
        return ((_t >= '08:00' && _t <= '18:00')) === false;
      }).each(function() {
        $(this).hide(); /* hide the rows */
      });
    }
  }

    })

    // $('#calendar').fullCalendar('next');
});
