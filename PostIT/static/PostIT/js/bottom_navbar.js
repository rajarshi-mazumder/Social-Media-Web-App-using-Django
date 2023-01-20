var is_right_sidebar_displayed = false;
window.onload = function () {

    HideRightSidebar();
    $('.profile-img-navbar').click(ToggleRightSidebar)
    $('.sidebar_right_blocker').click(ToggleRightSidebar);

    $('.add-post-submenu').hide();
    $('.profile-submenu').hide();
}
function ToggleRightSidebar() {
    if (is_right_sidebar_displayed) {
        HideRightSidebar();
        is_right_sidebar_displayed = false;
    }
    else {
        ShowRightSidebar();
        is_right_sidebar_displayed = true;
    }
    console.log("Sidbar toggle!!", is_right_sidebar_displayed)
}
function HideRightSidebar() {
    $('.sidebar-right-mobile').hide();
    $('.sidebar_right_blocker').hide();
    console.log(" HideRightSidebar!!", is_right_sidebar_displayed)

}
function ShowRightSidebar() {
    $('.sidebar-right-mobile').show();
    $('.sidebar_right_blocker').show();
    console.log(" ShowRightSidebar!!", is_right_sidebar_displayed)

}