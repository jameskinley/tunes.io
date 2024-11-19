function set_like(id, state, element) {
    $.ajax({
        type: "POST",
        url: "/like",
        data: JSON.stringify({
            post_id: id,
            state: state
        }),
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function() {
            console.log(`Updated like for post ${id} to ${state}`);
            if(state == 1){
                element.attr("src", "/static/heart-fill.svg");
                return;
            }
            element.attr("src", "/static/heart.svg");
        }
    });
}

function is_liked(element) {
    return element.attr("src") == "/static/heart.svg";
}

function toggle_liked(id) {
    let element = $(`#${id}`).find("img");

    if(is_liked(element)){
        set_like(id, 1, element);
        return;
    }

    set_like(id, 0, element);
}