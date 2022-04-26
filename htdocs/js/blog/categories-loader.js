$(document).ready(function () {
    console.log('Load categories');
    let $categoriesContainer = $('#categories-container');
    let categoriesUrl = $categoriesContainer.data('categories-url');

    $.ajax({
        type: 'GET',
        url: categoriesUrl,
        data: {'ordering': 'position'},
        success: function (data) {
            let categories = JSON.stringify(data.results);
            let renderUrl = $categoriesContainer.data('categories-render-url');

            $.ajax({
                type: 'GET',
                url: renderUrl,
                data: {'categories': categories},
                success: function (result) {
                    $categoriesContainer.append(result.content);
                },
            })
        }
    });

    updatePageHeader();
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


$('#categories-container').on('click', 'li', function () {
    let categorySlug = $(this).data('category-slug');
    let url = new URL(document.location.href);
    url.searchParams.set('category', categorySlug);
    window.history.pushState(null, '', url.toString());
});


function updatePageHeader(element=null) {
    let $categoryNameHeader = $('#category-name');

    let slug;
    if (!element) {
        let url = new URL(window.location.href);
        slug = url.searchParams.get('category');
    } else {
        slug = element.data('category-slug');
    }

    getNameOfCategoryBySlug(slug, function (name) {
        $categoryNameHeader.html(name);
    })

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
