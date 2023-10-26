document.addEventListener("DOMContentLoaded", () => {
    let s1 = document.getElementById('scroll-sticky');
    let s2 = document.getElementById('scroll-main-table');

    if (s1 && s2) {

    function select_scroll_1(e) { s2.scrollLeft = s1.scrollLeft; }
    function select_scroll_2(e) { s1.scrollLeft = s2.scrollLeft; }

    s1.onscroll = function(e) {
        select_scroll_1();
    }
    s2.onscroll = function(e) {
        select_scroll_2();
    }
}
});

