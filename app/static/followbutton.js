function toggle_following(username) {
    let state = get_follow_state();
    let follow_count = $('#follow-count');

    $.ajax({
        type: "POST",
        url: "/follow",
        data: JSON.stringify({
            username: username,
            state: !state
        }),
        contentType: "application/json; charset=utf-8;",
        dataType: "json",
        success: function() {
            console.log(`Set following user '${username}' to ${!state}`);
            if(state == 0){
                follow_count.text(Number(follow_count.text()) + 1);
                toggle_button_style(state);
                return;
            }
            follow_count.text(Number(follow_count.text()) - 1);
            toggle_button_style(state)
        }
    });
}

function get_follow_state() {
    if ($('#follow-btn').hasClass("btn-following")){
        return 1;
    }
    return 0;
}

function toggle_button_style(state) {
    btn = $('#follow-btn');

    if (state==0) {
        btn.text("Following");
        btn.removeClass("btn-notfollowing");
        btn.addClass("btn-following");
        return;
    }

    btn.text("Follow");
    btn.removeClass("btn-following");
    btn.addClass("btn-notfollowing");
}