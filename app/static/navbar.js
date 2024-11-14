let icons =
    [
        {
            id: "#nav-btn-home",
            active: "/static/home-fill.svg",
            inactive: "/static/home.svg"
        },
        {
            id: "#nav-btn-profile",
            active: "/static/person-fill.svg",
            inactive: "/static/person.svg"
        },
        {
            id: "#nav-btn-settings",
            active: "/static/gear-fill.svg",
            inactive: "/static/gear.svg"
        }
    ];

function setInactiveIcons() {
    icons.forEach(icon => {
        $(icon.id).find("img").attr("src", icon.inactive);
    });
}
$(document).ready(function () {
    $(".navbar-item").click(function () {
        setInactiveIcons();
        let curr = `#${$(this).attr('id')}`;
        $(this).find("img").attr("src", icons.find(icon => icon.id == curr).active);
    });
});