$(document).ready(function () {
    regSliderSelector = ".mainSlider"
    if ($("div").is(regSliderSelector)) {
        $(regSliderSelector).slick({
            touchThreshold: 10,
            slidesToShow: 1,
            variableWidth: true,
            responsive: [
                {
                    breakpoint: 2000,
                    settings: {
                        slidesToShow: 3,
                        infinite: true,
                        centerMode: false,
                    }
                },
                {
                    breakpoint: 800,
                    settings: {
                        slidesToShow: 2,
                        infinite: true,
                        centerMode: false,
                    }
                },
                {
                    breakpoint: 600,
                    settings: {
                        slidesToShow: 1,
                        infinite: true,
                        centerMode: true,
                    }
                },
            ]
        });
    }

});

$(document).ready(function () {
    regSliderSelector = ".listSample__slider"
    if ($("div").is(regSliderSelector)) {
        $(regSliderSelector).slick({
            slidesToShow: 2,
            slidesToScroll: 2,
            swipeToSlide: false,
            speed: 300,
            easing: 'linear',
            centerMode: false,
            variableWidth: true,
            pauseOnFocus: false,
            focusOnSelect: false,
            edgeFriction: 0,
            draggable: true,
            infinite: false,
            initialSlide: 0,
            touchThreshold: 10,
            waitForAnimate: false,
        });
    }
});

$(document).ready(function () {
    regSliderSelector = ".sport__slider"
    if ($("div").is(regSliderSelector)) {
        $(regSliderSelector).slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            swipeToSlide: false,
            //useTransform: true,
            speed: 300,
            easing: 'linear',
            centerMode: false,
            //centerPadding: '80px',
            variableWidth: true,
            //mobileFirst: true,
            pauseOnFocus: false,
            focusOnSelect: false,
            edgeFriction: 0,
            //centerMode: true,
            //infinite: true,
            draggable: true,
            //lazyLoad: "progressive",
            infinite: false,
            //speed: 300,
            initialSlide: 0,
            touchThreshold: 10,
            waitForAnimate: false,
        });
    }
});

$(document).ready(function () {
    regSliderSelector = ".shows__slider"
    if ($("div").is(regSliderSelector)) {
        $(regSliderSelector).slick({
            slidesToShow: 2,
            centerMode: true,
            infinite: true,
            initialSlide: 1,
            touchThreshold: 10,
        });
    }
});
$(document).ready(function () {
    regSliderSelector = ".listseason__slider"
    if ($("div").is(regSliderSelector)) {
        $(regSliderSelector).slick({
            slidesToShow: 2,
            slidesToScroll: 2,
            swipeToSlide: false,
            //useTransform: true,
            speed: 300,
            easing: 'linear',
            centerMode: false,
            //centerPadding: '80px',
            variableWidth: true,
            //mobileFirst: true,
            pauseOnFocus: false,
            focusOnSelect: false,
            edgeFriction: 0,
            //centerMode: true,
            //infinite: true,
            draggable: true,
            //lazyLoad: "progressive",
            infinite: false,
            //speed: 300,
            initialSlide: 0,
            touchThreshold: 10,
            waitForAnimate: false,
        });
    }
});





let search_open = document.getElementById("search-open")
let search_close = document.getElementById("search-close")
let search = document.getElementById("search")
let footer = document.getElementById("footer")

if (search_open) {
    search_open.addEventListener("click", (event) => {
        search.classList.toggle("search-acitve")
        let search_input = document.getElementById("search-input")
        let search_first = document.getElementById("search-first")
        search_first.click()
        search_input.focus()
        search.scrollTo(0, 0);
    })
}

