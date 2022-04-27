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


$('#categories-search').on('keyup', function () {
    let value = this.value;
    let categories = $('.category-row');
    $.map(categories, function (category) {
        let element = $(category)
        let currentName = element.data('category-name');
        if (currentName.toLowerCase().includes(value.toLowerCase())) {
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


function updatePageHeader(element = null) {
    let $categoryNameHeader = $('#category-name');

    let slug;
    if (!element) {
        let url = new URL(window.location.href);
        slug = url.searchParams.get('category');
    } else {
        slug = element.data('category-slug');
    }

    let name = getNameOfCategoryBySlug(slug);
    $categoryNameHeader.html(name);
}


function getNameOfCategoryBySlug(slug) {
    let categoryData = getCategoryBySlugData(slug);
    return categoryData?.name || 'Posts';
}


function getIdOfCategoryBySlug(slug) {
    let categoryData = getCategoryBySlugData(slug);
    return categoryData?.id || 0;
}

function getCategoryBySlugData(slug){
    let categoryUrl = $('#category-name').data('category-get-by-slug-url');
    let categoryData = {};
    if (slug) {
        $.ajax({
            type: 'GET',
            async: false,
            url: categoryUrl,
            data: {'slug': slug},
            success: function (response) {
                if (response.category) {
                    categoryData = response.category
                }
            }
        });
    }

    return categoryData
}

