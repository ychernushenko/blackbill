$(function() {
    $('#mainCreateA').click(function() {
 
        $.ajax({
            url: '/mainCreateA',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});