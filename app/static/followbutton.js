function set_follow(btn_id, state, username_source, username_dest) {

    let follow_count = $(`#${username}-count`);

    $.ajax({
        type: "POST",
        url: "/follow",
        data: JSON.stringify({
            post_id: id,
            state: state
        }),
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function() {
            console.log(`Set following user '${username}' to ${state}`);
            if(state == 1){
                follow_count.text(Number(follow_count.text()) + 1);
                return;
            }
            follow_count.text(Number(follow_count.text()) - 1);
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