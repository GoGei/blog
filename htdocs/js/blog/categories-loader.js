$(document).ready(function () {
    console.log('Load categories');
    let $categoriesContainer = $('#categories-container');
    let categoriesUrl = $categoriesContainer.data('categories-url');

    $.ajax({
        type: 'GET',
        url: categoriesUrl,
        dataType: "json",
        success: function (data) {
            $.map(data.results, function (category, i) {
                $categoriesContainer.append(`<li data-category-id="${category.id}" 
                                                data-category-name="${category.name}" 
                                                data-category-slug="${category.slug}">
                                                <a href="#">${category.short_name}</a></li>`)
            })
        }
    });

    updatePageHeader();
});


$('#categories-container').on('click', 'li', function () {
    updateUrlParams($(this));
    updatePageHeader($(this));
    loadCategoryPosts($(this));
});


function updateUrlParams(element) {
    let categorySlug = element.data('category-slug');
    let url = new URL(document.location.href);
    url.searchParams.set('category', categorySlug);
    window.history.pushState(null, '', url.toString());
}


function updatePageHeader(element=null) {
    let $categoryNameHeader = $('#category-name');

    let slug;
    if (!element) {
        let url = new URL(window.location.href);
        slug = url.searchParams.get('category');
    } else {
        slug = element.data('category-slug');
    }

    getNameOfCategoryBySlug(slug, function (name) {$categoryNameHeader.html(name);})

}

function getNameOfCategoryBySlug(slug, callback){
    let categoryUrl = $('#category-name').data('category-name-url');
    let name = 'Posts';
    if (slug) {
        $.get(
            categoryUrl, {'slug': slug}
        ).done(function (response) {
            if (response.name) {
                name = response.name;
                callback(name);
            }
        });
    } else {
        callback(name);
    }
}


function loadCategoryPosts(element) {
    let $container = element.parent();
    let postsUrl = $container.data('posts-url');

    let filterData = {'category': element.data('category-id')};
    $.ajax({
        type: 'GET',
        url: postsUrl,
        data: filterData,
        success: function (data) {
            console.log(data);
            $.map(data.results, function (post, i) {
                // console.log(post);
            })
        }
    })
}