$(document).ready(function () {
    console.log('Load categories');
    let $categoriesContainer = $('#categories-container');
    let categoriesUrl = $categoriesContainer.data('categories-url');

    $.ajax({
        type: 'GET',
        url: categoriesUrl,
        dataType: "json",
        success: function (data) {
            $.map(data.results, function (category) {
                $categoriesContainer.append(`<li class="category-row" 
                                                data-category-id="${category.id}" 
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
    loadPosts('', true);
});


$('#categories-search').on('keyup', function (){
    let value = this.value;
    let categories = $('.category-row');
    $.map(categories, function (category){
        let element = $(category)
        let currentName = element.data('category-name');
        if (currentName.toLowerCase().includes(value.toLowerCase())){
            element.show();
        } else {
            element.hide();
        }
    });
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
                callback(response.name);
            }
        });
    } else {
        callback(name);
    }
}


function getIdOfCategoryBySlug(slug, callback){
    let categoryUrl = $('#category-name').data('category-id-url');
    let name = 'Posts';
    if (slug) {
        $.get(
            categoryUrl, {'slug': slug}
        ).done(function (response) {
            if (response.id) {
                callback(response.id);
            }
        });
    } else {
        callback(name);
    }
}
