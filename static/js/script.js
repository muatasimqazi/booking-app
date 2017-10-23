$(document).ready(function() {
  $('.modal').modal({
    opacity: .2,
    background: 'red'
  });
  $('.modal').css({
    'max-height': '100%',
    'background': 'white'
  });
  $('select').material_select();
  $('.button-collapse').sideNav({
    menuWidth: 300, // Default is 300
    edge: 'left', // Choose the horizontal origin
    closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
    draggable: true, // Choose whether you can drag to open on touch screens,
  });


  $('#external-events .fc-event').each(function() {
    $(this).data('event', {
      title: $.trim($(this).text()),
      stick: true,
      overlap: false
    });

    $(this).draggable({
      zIndex: 999,
      revert: true,
      revertDuration: 0
    });
  });

  $('#calendar').fullCalendar({
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
    backgroundColor: 'blue',
    eventConstraint: {
      // start: '09:00', // a start time (10am in this example)
      // end: '17:00', // an end time (5pm in this example)
      dow: [1, 2, 3, 4, 5]
      // days of week. an array of zero-based day of week integers (0=Sunday)
      // (Monday-Thursday in this example)
    },
    droppable: true,
    drop: function(date, e, ui, resourceId) {
      console.log(resourceId.start);
      $('#new-event').modal('open');
      $('#event_title').val(e.target.textContent);
      $("label[for='event_title']").empty();
      $('#event-date').val(date.format());
    },

    eventRender: function(event, element) {
      element.attr('href', '#event-info');
      element.addClass('modal-trigger');
      element.click(function() {
        var moment1 = moment('2013-09-02');
        var moment2 = moment('2013-09-09');
        $.fullCalendar.formatRange(moment1, moment2, 'MM D YYYY');
        $('#event-info-title').text(event.title);
        $('#event-info-date').html("<span class='black-text'>" + event.start.format('dddd, MMMM D') + '</span><br><small>' + event.start.format('h:mm a') + ' – ' + event.end.format('h:mm a') + '</small>');
        console.log(event);
        $('#event-info').modal('open');
      });
    },

    events: {
      url: $SCRIPT_ROOT + '/_get_events',
      cache: true,

    },
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
