function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        // 'sessionid': getCookie('sessionid'),
    },
});


$(".go-to-the-top").click(function () {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

$(".phone-number").inputmask("mask", { "mask": "+380(99)-999-9999" });
