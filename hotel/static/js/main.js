$(document).on('click', 'td button.accept', function (e) {
    e.preventDefault()
    var _booking = $(this).attr("value")
    var _csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: window.location,
        headers: {
            'X-CSRFToken': _csrf
        },
        data: {
            'action': 'accept',
            'booking': _booking,
        },
        success: function () {
            $('#tr-row-'+_booking).remove();
        },
        error: function () {
            console.log('error')
        }
    })
})

$(document).on('click', 'td button.decline', function (e) {
    e.preventDefault()
    var _booking = $(this).attr("value")
    var _csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: window.location,
        headers: {
            'X-CSRFToken': _csrf
        },
        data: {
            'action': 'decline',
            'booking': _booking,
        },
        success: function () {
            $('#tr-row-'+_booking).remove();
        },
        error: function () {
            console.log('error')
        }
    })
})

$(document).on('click', 'td button.cancel', function (e) {
    e.preventDefault()
    var _booking = $(this).attr("value")
    var _csrf = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
        type: "POST",
        url: window.location,
        headers: {
            'X-CSRFToken': _csrf
        },
        data: {
            'action': 'cancel',
            'booking': _booking,
        },
        success: function () {
            $('#tr-row-'+_booking).remove();
        },
        error: function () {
            console.log('error')
        }
    })
})
