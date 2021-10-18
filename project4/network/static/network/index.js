$(document).ready(
    () => {
        $('.edit_post').slideUp();
        console.clear();
    }
)

drop_edit_textarea = (id) => {
    target = "#edit" + String(id);
    $(target).slideToggle();
};

send_update = (id) => {
    target = "#edit" + String(id) + ' ' + 'textarea';
    new_msg = $(target).val();
    fetch(
            "/post/" + String(id), {
                method: 'PUT',
                body: JSON.stringify({
                    msg: new_msg
                })
            })
        .then(response => response.json())
        .then(post => {
            target = '#' + String(id) + ' ' + '.card-text';
            $(target).text(post.msg);
            target = "#edit" + String(id);
            $(target).slideUp();
        });
    console.clear()

}

like_post = (id) => {
    target = '#opinion' + String(id);
    $(target).remove();
    fetch(
            "/post/" + String(id), {
                method: 'PUT',
                body: JSON.stringify({
                    like: true
                })
            })
        .then(response => response.json())
        .then(post => {
            target = '#likes' + String(id);
            $(target).text(post.likes);
        });
    console.clear()
};
dislike_post = (id) => {
    target = '#opinion' + String(id);
    $(target).remove();
    fetch(
            "/post/" + String(id), {
                method: 'PUT',
                body: JSON.stringify({
                    dislike: true
                })
            })
        .then(response => response.json())
        .then(post => {
            target = '#dislikes' + String(id);
            $(target).text(post.dislikes);
        });
    console.clear()

}