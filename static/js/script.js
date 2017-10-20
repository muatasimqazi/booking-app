var events;

function my_script(e) {
  events = e; // from the database
  console.log(events);
}

$(document).ready(function() {
  $('.modal').modal();
  $('select').material_select();
  $('.button-collapse').sideNav({
    menuWidth: 300, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true, // Choose whether you can drag to open on touch screens,
  });

  $(".ui-draggable").draggable();

  $('.timepicker').pickatime({
    default: 'now', // Set default time: 'now', '1:30AM', '16:30'
    fromnow: 0, // set default time to * milliseconds from now (using with default = 'now')
    twelvehour: false, // Use AM/PM or 24-hour format
    donetext: 'OK', // text for done-button
    cleartext: 'Clear', // text for clear-button
    canceltext: 'Cancel', // Text for cancel-button
    autoclose: false, // automatic close timepicker
    ampmclickable: true, // make AM PM clickable
    aftershow: function() {} //Function for after opening timepicker
  });


  $('#calendar').fullCalendar({
    // put your options and callbacks here
    weekends: false, // will hide Saturdays and Sundays
    defaultView: 'month',
    header: {
      left: 'prev,next today myCustomButton',
      center: 'title',
      right: 'agendaDay,agendaWeek,month,listDay'
    },
    columnFormat: 'ddd',
    displayEventEnd: true,
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

    eventRender: function(event, element) {
      element.attr('href', '#event-modal');
      element.addClass('modal-trigger');
      element.click(function() {

        $("#event-content").html(
          '<h5>' + event.title + '</h5>' +
          '<p>' + moment(event.start).format('MMM Do h:mm A') + '</p>'
        );
      });
    },

    events: events,

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

  });

});
