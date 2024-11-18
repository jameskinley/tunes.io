function get_html(response) {
    let html = '';
    response.forEach(track => {
        html += `
            <div class="d-flex">
                <img class="search-artwork" src="${track.artwork}" alt="Artwork" width="75px" height="75px">
                <div class="d-block">
                    <strong>${track.title}</strong>
                    <p>${track.album}&#x2022;${track.artist}</p>
                </div>
            </div>`;
    });
    return html;
}

function populate_results(response) {
    $('#search-results').html(get_html(response))
    $('#search-results').show();
}

$(document).ready(function() {
    $('#search-input-submit').click(function() {
        let query = $('#search-input').val();
        $.ajax({
            type: "POST",
            url: "/search",
            data: JSON.stringify({
                query: query
            }),
            contentType: "application/json; charset=utf-8;",
            dataType: "json",
            success: function(response) {
                console.log(`Got the following tracks: ${response}`);
                populate_results(response);
            }
        });
    });
});