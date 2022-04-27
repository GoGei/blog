$(document).ready(function () {
    let url = new URL(document.location.href);
    if (!url.searchParams.has('tab')){
        url.searchParams.set('tab', 'posts');
    }
    window.history.pushState(null, '', url.toString());
})