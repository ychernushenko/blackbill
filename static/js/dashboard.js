$(function() {
    $('#dashboardCreateA').click(function() {
 
        $.ajax({
            url: '/dashboardCreateA',
            type: 'POST',
            success: function(response) {
                console.log(response);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            },
            error: function(error) {
                console.log(error);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            }
        });
    });
});

$(function() {
    $('#dashboardCreateB').click(function() {
 
        $.ajax({
            url: '/dashboardCreateB',
            type: 'POST',
            success: function(response) {
                console.log(response);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            },
            error: function(error) {
                console.log(error);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            }
        });
    });
});

$(function() {
    $('#dashboardCreateC').click(function() {
 
        $.ajax({
            url: '/dashboardCreateC',
            type: 'POST',
            success: function(response) {
                console.log(response);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            },
            error: function(error) {
                console.log(error);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            }
        });
    });
});

$(function() {
    $('#dashboardCreateD').click(function() {
 
        $.ajax({
            url: '/dashboardCreateD',
            type: 'POST',
            success: function(response) {
                console.log(response);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            },
            error: function(error) {
                console.log(error);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            }
        });
    });
});


$(function() {
    $('#showStatus').click(function() {
 
        $.ajax({
            url: '/showStatus',
            type: 'POST',
            success: function(response) {
                console.log(response);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            },
            error: function(error) {
                console.log(error);
                $( "#outputLog" ).prepend("<p>" + JSON.stringify(response) + "</p>");
            }
        });
    });
});
