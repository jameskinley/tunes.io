function toggle_liked(id) {
    let element = $(id).find("img");

    if(element.attr("src") == "/static/heart.svg"){
        element.attr("src", "/static/heart-fill.svg");
        return;
    }

    element.attr("src", "/static/heart.svg");
}