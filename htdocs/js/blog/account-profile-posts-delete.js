$(document).on('click', '.delete-post', function (){
    console.log('Confirm delete post');
    if(confirm("Do you want to delete this post?")){
        let current = $(this);
        $.ajax({
            type: 'DELETE',
            url: current.data('post-delete-url'),
        })
    }
    else{
        return false;
    }
})