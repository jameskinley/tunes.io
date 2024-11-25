let tracks = [];

function set_song(id) {
    console.log(`clicked id: ${id}`);
    $('#search-results').hide();

    let track = tracks.find(t => t.track_external_id == id);

    if(!track) return;

    $('#track_id').val(id);
    $('#song-artwork').attr('src', track.artwork);
    $('#song-title').text(track.title);
    $('#song-album-artist').text(`${track.album} • ${track.artist}`);

    $('#post-preview').removeClass('d-none');
    $('#post-preview').addClass('d-flex');

    $('#post-description').removeClass('d-none');
    $('#post-description').addClass('d-block');

    $('#post-submit').removeClass('d-none');
    $('#post-submit').addClass('d-flex');
    $('#post-submit').find('button').removeAttr('disabled');
}

function get_html(response) {
    let html = '';
    response.forEach(track => {
        html += `
            <a id="${track.track_external_id}" class="d-flex border search-panel" onclick="set_song(this.id)">
                <img class="search-artwork" src="${track.artwork}" alt="Artwork" width="75px" height="75px">
                <div class="d-block">
                    <strong>${track.title}</strong>
                    <p class="overflow-wrap">${track.album} &#x2022; ${track.artist}</p>
                </div>
            </a>`;
    });
    return html;
}

function populate_results(response) {
    tracks = response;
    $('#search-results').html(get_html(response))
    $('#search-results').show();
}

function search_request(query) {
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
}

$(document).ready(function() {
    $('#search-input-submit').click(function() {
        let query = $('#search-input').val();
        search_request(query);
    });

    $('#search-input').keyup(function() {
        let query = $('#search-input').val();
        search_request(query);
    });

    //Close when we click off
    $(document).click(function(event) { 
        if (!$(event.target).closest('#search-results').length && !$(event.target).is('#search-input')) { 
            $('#search-results').hide(); } });
});