$(document).ready(function () {
    regSliderSelector = ".main-slider"
    if ($("div").is(regSliderSelector)) {
        var bigSlider = new Swiper(regSliderSelector, {
            slidesPerView: "auto",
            spaceBetween: 12,
            centeredSlides: true,
            loop: true,
            observeParents: true,
            observeSlideChildren: true,
            observer: true,
            autoplay: {
                delay: 5500,
                disableOnInteraction: false,
            },

            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
        });
    }
})
$(document).ready(function () {
    regSliderSelector = ".line-slider"
    if ($("div").is(regSliderSelector)) {
        var lineSlider = new Swiper(regSliderSelector, {
            slidesPerView: "auto",
            freeModeSticky: true,
            slideToClickedSlide: true,
            shortSwipes: false,
            effect: "slide",
            grabCursor: true,
            velocityRatio: 0.2,
            spaceBetween: 12,
            centeredSlides: false,
            freeMode: true,
            observeParents: true,
            observeSlideChildren: true,
            observer: true,
        });
    }
})
$(document).ready(function () {
    regSliderSelector = ".sport-slider"
    if ($("div").is(regSliderSelector)) {
        var sportSlider = new Swiper(regSliderSelector, {
            slidesPerView: "auto",
            autoHeight: true,
            slideToClickedSlide: true,
            shortSwipes: false,
            effect: "slide",
            grabCursor: true,
            freeModeSticky: true,
            velocityRatio: 0.2,
            spaceBetween: 12,
            centeredSlides: false,
            freeMode: true,
            loop: true
        });
    }
})


String.prototype.fmt = function (hash) {
    var string = this, key;
    for (key in hash) string = string.replace(new RegExp('\\{' + key + '\\}', 'gm'), hash[key]);
    return string
}
//menu
$(document).ready(function () {
    checkIsAvailable = ".header__menu"
    if ($("div").is(checkIsAvailable)) {
        let burger = document.getElementById("burger")
        let menu = document.getElementById("menu")
        let menu_content = document.getElementById("menu-content")

        burger.addEventListener("click", (event) => {
            menu.classList.toggle("menu-active")
            setTimeout(() => {
                menu_content.classList.toggle("menu__content-active")
            }, 0);
            document.body.style.maxHeight = menu.offsetHeight + 400 + "px"
            document.body.style.overflowY = "hidden"

            // $(document).mouseup(function (e) { // событие клика по веб-документу
            //     var div = $(".header__menu_content"); // тут указываем ID элемента
            //     if (!div.is(e.target) // если клик был не по нашему блоку
            //         && div.has(e.target).length === 0) { // и не по его дочерним элементам
            //         menu.classList.toggle("menu-active")
            //         menu_content.classList.toggle("menu__content-active")
            //         document.body.style.overflowY = "visible"
            //     }
            // });

        })


        menu.addEventListener("click", (event) => {
            if (event.target != menu_content) {
                menu.classList.toggle("menu-active")
                menu_content.classList.toggle("menu__content-active")
                document.body.style.overflowY = "visible"
            }
        })
    }
})

//filter-popup
$(document).ready(function () {
    checkIsAvailable = ".filter-popup"
    if ($("div").is(checkIsAvailable)) {
        const slidersArray = {
            "years": [1970, 2021],
            "ratings": [1, 10]
        }
        $(function () {
            $("#slider-range").slider({
                range: true,
                min: 1960,
                max: 2021,
                values: [1970, 2021],
                slide: function (event, ui) {
                    $("#amount").val(ui.values[0] + " - " + ui.values[1]);
                    slidersArray["years"] = [ui.values[0], ui.values[1]]
                }
            });
            $("#amount").val($("#slider-range").slider("values", 0) +
                " - " + $("#slider-range").slider("values", 1));
        });
        $(function () {
            $("#rating").slider({
                range: true,
                min: 1,
                max: 10,
                values: [1, 10],
                slide: function (event, ui) {
                    $("#rating-amount").val(ui.values[0] + " - " + ui.values[1]);
                    slidersArray["ratings"] = [ui.values[0], ui.values[1]]
                }
            });
            $("#rating-amount").val($("#rating").slider("values", 0) +
                " - " + $("#rating").slider("values", 1));
        });

        let popups = document.querySelectorAll(".filters__item_popup")

        for (let i = 0; i < popups.length; i++) {
            popups[i].addEventListener("click", (event) => {
                let popup = document.querySelector(`[data-filterpopup="${popups[i].getAttribute('data-popupid')}"]`)
                let search_input = popup.querySelector('.filter-popup__input-query')
                searchQueryToDb(search_input.value)
                let popupItemsGroup = popup.querySelector('.filter-popup__group')

                search_input.addEventListener('keyup', (event) => {
                    searchQueryToDb(search_input.value)
                })

                function searchQueryToDb(q) {
                    let csrf = popup.querySelector('input[name="csrfmiddlewaretoken"]').value
                    request = $.ajax({
                        url: `/${currLocale}/filter.json`,
                        type: "post",
                        data: {
                            "csrfmiddlewaretoken": csrf,
                            "q": q,
                            "id": popups[i].getAttribute('data-popupid')
                        }
                    })
                    let template = ` \
                    <div class="filter-popup__item" onclick="checkbyclick(this);" data-popupitemid="{id}"> \
                        <input type="checkbox" class="filter-popup__item_checkbox " name="Action"> \
                        <span>{name}</span> \
                    </div> \
                    `
                    request.done(function (response, textStatus, jqXHR) {
                        if (response.length > 0) {
                            response = JSON.parse(response)
                            returnHTML = ''
                            response.forEach(element => {
                                returnHTML += template.fmt({id: element.id || "", name: element.name || ""})
                            })
                            popupItemsGroup.innerHTML = returnHTML
                        }
                    })
                }

                let popupCloseBtn = popup.querySelector('.filter-popup_close')
                let popupChooseBtn = popup.querySelector('.filter-popup__btn')
                //open-popup
                popup.classList.add("filter-popup-active")
                let allitem = popup.querySelectorAll('.filter-popup__item')[0]
                if (popup.getAttribute('data-filterpopup') != 1) {
                    allitem.classList.add("filter-popup__item-active")
                }
                // let сitems = document.querySelectorAll('.filter-popup__item')
                // console.log(сitems)
                // сitems[0].classList.add('filter-popup__item-active')
                //close-popup
                popupCloseBtn.addEventListener('click', (event) => {
                    popup.classList.remove("filter-popup-active")
                })
                popupChooseBtn.addEventListener('click', (event) => {
                    chooseInPopup(popups[i].getAttribute('data-popupid'), popup)
                })


            })
        }

        function chooseInPopup(id, popup) {
            filterPopupContent = document.querySelector(`[data-popupid="${id}"]`).querySelector('.filters__item_options')
            activeElements = popup.querySelectorAll('.filter-popup__item-active')
            if (activeElements[0] == undefined) {
                let items = popup.querySelectorAll('.filter-popup__item')
                items[0].classList.add('filter-popup__item-active')
            }
            activeElements = popup.querySelectorAll('.filter-popup__item-active')
            finalHTML = []
            for (let i = 0; i < activeElements.length; i++) {
                finalHTML.push(`<span class="filter-popup__options_item" data-filterpopupitemname="${activeElements[i].getAttribute('data-popupitemid')}">${activeElements[i].querySelector('span').innerHTML}</span>`)
            }
            filterPopupContent.innerHTML = finalHTML.join(', ')
            popup.classList.remove("filter-popup-active")
        }

        let filterShowBtn = document.querySelector(".button-to-submit")
        let sendForm = document.querySelector(".send-form")
        filterShowBtn.addEventListener('click', (event) => {
            finalArray = {
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0,
            }
            for (let i = 0; i < popups.length; i++) {
                let popupElements = popups[i].querySelectorAll('.filter-popup__options_item')
                let popupId = popups[i].getAttribute('data-popupid')
                checkOfAll = false
                localList = []
                for (let element of popupElements) {
                    elementId = element.getAttribute('data-filterpopupitemname')
                    if (elementId == "0") {
                        checkOfAll = true
                    } else {
                        localList.push(parseInt(elementId))
                    }
                }
                if (!checkOfAll) {
                    finalArray[popupId] = localList
                }
            }

            // console.log(finalArray)
            // sendForm
            sendForm.innerHTML += ` \
                <input type="hidden" name="1" value="${finalArray['1']}"> \
                <input type="hidden" name="2" value="${finalArray['2']}"> \
                <input type="hidden" name="3" value="${finalArray['3']}"> \
                <input type="hidden" name="4" value="${finalArray['4']}"> \ 
                <input type="hidden" name="5" value="${slidersArray.years}"> \
                <input type="hidden" name="6" value="${slidersArray.ratings}"> \
            `
            sendForm.submit()

        })

    }
})

function checkbyclick(elem) {
    let popup = document.querySelector('.filter-popup-active')
    let allitem = popup.querySelectorAll('.filter-popup__item')[0]
    let items = document.querySelectorAll('.filter-popup__item')
    if (elem.getAttribute('data-popupitemid') == 0) {
        if (!elem.classList.contains("filter-popup__item-active")) {
            for (let i = 1; i < items.length; i++) {
                items[i].classList.remove("filter-popup__item-active")
            }
            allitem.classList.add("filter-popup__item-active")
        } else {

        }
    } else {
        if (popup.getAttribute('data-filterpopup') != 1) {
            allitem.classList.remove("filter-popup__item-active")
            elem.classList.toggle("filter-popup__item-active")
            if (popup.querySelectorAll('.filter-popup__item-active')[0] == undefined) {
                allitem.classList.add('filter-popup__item-active')
            }
        } else {
            let allActive = popup.querySelectorAll('.filter-popup__item-active')
            for (let i = 0; i < allActive.length; i++) {
                console.log(allActive)
                allActive[i].classList.remove('filter-popup__item-active')
            }
            elem.classList.toggle('filter-popup__item-active')
        }

    }
}

$(document).ready(function () {
    checkIsAvailable = ".serie-card"
    orCheck = ".movie-card"
    if ($("main").is(checkIsAvailable) || $("main").is(orCheck)) {
        let read = document.getElementById('read-more')
        let text = document.getElementById('text')

        read.addEventListener("click", (event) => {
            text.style.maxHeight = "none";
            text.style.marginBottom = "10px"
            read.style.display = "none"
        })
    }
})

$(document).ready(function () {
    checkIsAvailable = ".serie-card"

    if ($("main").is(checkIsAvailable)) {
        var seasonSlider = new Swiper('.seas-slider', {
            slidesPerView: "auto",
            spaceBetween: 30,
            centeredSlides: false,
            loop: false,
            freeModeSticky: true,
            freeMode: true,
        })

        let tabs = document.querySelectorAll('.seasslide')
        for (let i = 0; i < tabs.length; i++) {
            tabs[i].addEventListener('click', (event) => {
                for (let j = 0; j < tabs.length; j++) {
                    tabs[j].classList.remove("seasslide_active")
                    let season_episodes = document.querySelector(`div.seasons-episodes[data-tabseasid="${tabs[j].getAttribute('data-seasid')}"]`)
                    season_episodes.classList.remove("season-episodes_active")
                }
                tabs[i].classList.toggle("seasslide_active")
                let season_num = tabs[i].getAttribute('data-seasid')
                let season_episodes = document.querySelector(`div.seasons-episodes[data-tabseasid="${season_num}"]`)
                season_episodes.classList.add('season-episodes_active')

            })
        }
    }
})

$(document).ready(function () {

})

$(document).ready(function () {

})

//popup
$(document).ready(function () {
    checkIsAvailable = ".header__app"
    if ($("button").is(checkIsAvailable)) {
        let popup = document.getElementById('popup')
        let popup_open = document.getElementsByClassName("popup__open")

        let popup_close

        for (let i = 0; i < popup_open.length; i++) {
            popup_open[i].addEventListener("click", (event) => {
                popup.classList.toggle("popup-acitve")
                popup_close = document.getElementById("popup-close")
                popup_close.addEventListener("click", (event) => {
                    popup.classList.remove("popup-acitve")
                })
            })
        }
    }
})

//search

function openSearch() {
    let search = document.getElementById("search")
    let search_input = document.getElementById("search-input")
    let footer = document.querySelector('.footer')
    search.classList.toggle("search-acitve")
    if (footer) {
        footer.classList.toggle('footer_hidden')
    }
    document.body.classList.toggle('locked_ovf')
    let search_first = document.getElementById("search-first")
    if (search.classList.contains('search-acitve')) {
        setTimeout(() => {
            try {
                AndroidFunction.setBottomNavVisibility(false)
            } catch (e) {
            }
        }, 200)
        search_input.focus()
        search_first.click()
        search.scrollTo(0, 0);
    } else {
        try {
            AndroidFunction.setBottomNavVisibility(true)
        } catch (e) {
        }
    }


}

$(document).ready(function () {
    checkIsAvailable = ".search"
    if ($("div").is(checkIsAvailable)) {
        // SEARCH
        let search_open = document.getElementById("search-open")
        let search_close = document.getElementById("search-close")
        let search = document.getElementById("search")
        let search_input = document.getElementById("search-input")
        let footer = document.getElementById("footer")
        if ($("button").is("#search-open")) {
            search_open.addEventListener("click", (event) => {
                openSearch()
            })
        }

        //LIVE-SEARCH
        function getCurrentTab() {
            return document.querySelector('.search__tab_active')
        }

        function getCurrentTabID() {
            return getCurrentTab().getAttribute('data-tabid')
        }

        function getSearchQuery() {
            return search_input.value
        }

        var checkInputEmpty = function checkInputEmpty() {
            if (getSearchQuery() == '') {
                return false
            }
            return true

        }

        function searchQueryToDb(tab, q) {
            let csrf = $('input[name="csrfmiddlewaretoken"]').val()
            request = $.ajax({
                url: `/${currLocale}/live-search.json`,
                type: "post",
                data: {
                    "csrfmiddlewaretoken": csrf,
                    "q": q,
                    "tab": tab
                }
            })
            request.done(function (response, textStatus, jqXHR) {
                if (response.length > 0) {
                    response = JSON.parse(response)
                    let template = ` \
                        <a href="/{page_url}/{id}" class="search__item"> \
                            <div class="search__item_img"> \
                                <img src="{poster}" alt=""> \ 
                            </div> \
                            <div class="search__item_text"> \
                                <div class="search__item_name">{name}</div> \
                                <div class="search__item_decription"> \
                                    <div class="search__item_year">{year}</div> \
                                    <div class="search__item_decor"></div> \
                                    <div class="search__item_genres">{genres}</div> \
                                </div> \
                            </div> \
                            <div class="search__item_rating">{rating}</div> \
                        </a> \
                    `
                    returnHTML = ''

                    function get_page_url() {
                        switch (parseInt(getCurrentTabID())) {
                            case 1:
                                return "movie";
                            case 2:
                                return "serie";
                            case 3:
                                return "sport";
                            case 4:
                                return "channel";
                            case 5:
                                return "tv-show";
                        }
                    }

                    response.forEach(element => {
                        returnHTML += template.fmt({
                            id: element.id || "",
                            poster: element.poster || "",
                            name: element.name || "",
                            year: element.year || "",
                            genres: element.genres || "",
                            rating: element.rating.toFixed(1) || "",
                            page_url: get_page_url()
                        })
                    })
                    getCurrentTab().innerHTML = returnHTML
                }
            })
        }

        search_input.addEventListener('keyup', (event) => {
            if (checkInputEmpty()) {
                searchQueryToDb(getCurrentTabID(), getSearchQuery())
            }
        })
        let tabs = document.getElementsByClassName('search__menu_item');
        for (let i = 0; i < tabs.length; i++) {
            tabs[i].addEventListener('click', (event) => {
                for (let j = 0; j < tabs.length; j++) {
                    tabs[j].classList.remove("search__menu_item-active")
                    tab_container = document.getElementById(`search${tabs[j].getAttribute('data-tab')}`)
                    tab_container.classList.remove('search__tab_active')
                }
                tabs[i].classList.add("search__menu_item-active")
                tab_container = document.getElementById(`search${tabs[i].getAttribute('data-tab')}`)
                tab_container.classList.add('search__tab_active')
                if (checkInputEmpty()) {
                    searchQueryToDb(tab_container.getAttribute('data-tabid'), getSearchQuery())
                }
            })
        }
    }
})
$(document).ready(function () {


    checkIsAvailable = ".profile-sl"
    if ($("div").is(checkIsAvailable)) {
        let request = getUrlVars()
        let tabs = document.querySelectorAll('.profslide')
        let tabs_content = document.querySelectorAll('.seasons-episodes')
        let current_slide = 0
        if (request.tab) {
            let tab = document.querySelector(`div.profslide[data-seasid="${request.tab}"]`)
            let tab_content = document.querySelector(`div.seasons-episodes[data-tabseasid="${request.tab}"]`)
            if (tab && tab_content) {
                for (let i = 0; i < tabs.length; i++) {
                    tabs[i].classList.remove('profslide_active')
                    tabs_content[i].classList.remove('season-episodes_active')
                }
                tab.classList.add('profslide_active')
                tab_content.classList.add('season-episodes_active')
                current_slide = parseInt(request.tab) - 1
            }


        }

        var seasonSlider = new Swiper('.profile-slider', {
            slidesPerView: "auto",
            spaceBetween: 22,
            centeredSlides: false,
            loop: false,
            freeModeSticky: true,
            freeMode: true,
        })
        for (let i = 0; i < tabs.length; i++) {

            tabs[i].addEventListener('click', (event) => {
                for (let j = 0; j < tabs.length; j++) {
                    tabs[j].classList.remove("profslide_active")
                    let season_episodes = document.querySelector(`div.seasons-episodes[data-tabseasid="${tabs[j].getAttribute('data-seasid')}"]`)
                    season_episodes.classList.remove("season-episodes_active")
                }
                tabs[i].classList.toggle("profslide_active")
                let season_num = tabs[i].getAttribute('data-seasid')
                let season_episodes = document.querySelector(`div.seasons-episodes[data-tabseasid="${season_num}"]`)
                season_episodes.classList.add('season-episodes_active')

            })
        }
    }
})

window.onload = function () {
    // document.body.classList.add('loaded_hiding');
    window.setTimeout(function () {
        prl = document.querySelector('.loading')
        prl.classList.add('loaded')
        document.body.classList.add('loaded');
    }, 500);
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
        function (m, key, value) {
            vars[key] = value;
        });
    return vars;
}

function createShareUrl(url) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/createShareUrl`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "url": url,
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        console.log(response)
    })
}

function shareEl(params) {
    let popupShare = document.querySelector('.share-popup')
    let popupShareMsgs = popupShare.querySelector('.share-popup__msgs')
    let popupShareInput = popupShare.querySelector('.share-copy__input')
    let copyBtn = popupShare.querySelector('.share-copy__btn')
    let popupShareBg = popupShare.querySelector('.share-popup__background')
    let name = params.getAttribute('data-elname')
    let url = "http://webapp.zola.cx" + params.getAttribute('data-elurl')
    if (!itsapp) {
        url = window.location.protocol + "//" + window.location.host + params.getAttribute('data-elurl')
    }

    try {
        if (u_profile) {
            url = url + `?ref=${u_id}`
            createShareUrl(url)
        }
    } catch (e) {

    }
    let resultHTML = ''
    let templates = [
        `\
        <a class="resp-sharing-button__link" \
           href="https://facebook.com/sharer/sharer.php?u={url}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--facebook resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M18.77 7.46H14.5v-1.9c0-.9.6-1.1 1-1.1h3V.5h-4.33C10.24.5 9.5 3.44 9.5 5.32v2.15h-3v4h3v12h5v-12h3.85l.42-4z"/> \
                    </svg> \
                </div> \
            </div> \
        </a>\
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://twitter.com/intent/tweet/?text=ZolaTV - {name}&amp;url={url}" \
           target="_blank" \
           rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--twitter resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M23.44 4.83c-.8.37-1.5.38-2.22.02.93-.56.98-.96 1.32-2.02-.88.52-1.86.9-2.9 1.1-.82-.88-2-1.43-3.3-1.43-2.5 0-4.55 2.04-4.55 4.54 0 .36.03.7.1 1.04-3.77-.2-7.12-2-9.36-4.75-.4.67-.6 1.45-.6 2.3 0 1.56.8 2.95 2 3.77-.74-.03-1.44-.23-2.05-.57v.06c0 2.2 1.56 4.03 3.64 4.44-.67.2-1.37.2-2.06.08.58 1.8 2.26 3.12 4.25 3.16C5.78 18.1 3.37 18.74 1 18.46c2 1.3 4.4 2.04 6.97 2.04 8.35 0 12.92-6.92 12.92-12.93 0-.2 0-.4-.02-.6.9-.63 1.96-1.22 2.56-2.14z"/> \
                    </svg> \  
                </div>\
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://www.tumblr.com/widgets/share/tool?posttype=link&amp;title=ZolaTV - {name}&amp;caption=ZolaTV - {name}&amp;content={url}&amp;canonicalUrl={url}&amp;shareSource=tumblr_share_button" \
           target="_blank" rel="noopener" aria-label=""> \ 
            <div class="resp-sharing-button resp-sharing-button--tumblr resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \ 
                        <path d="M13.5.5v5h5v4h-5V15c0 5 3.5 4.4 6 2.8v4.4c-6.7 3.2-12 0-12-4.2V9.5h-3V6.7c1-.3 2.2-.7 3-1.3.5-.5 1-1.2 1.4-2 .3-.7.6-1.7.7-3h3.8z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="mailto:?subject=ZolaTV - {name}&amp;body={url}" \
           target="_self" \
           rel="noopener" aria-label=""> \ 
            <div class="resp-sharing-button resp-sharing-button--email resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \ 
                        <path d="M22 4H2C.9 4 0 4.9 0 6v12c0 1.1.9 2 2 2h20c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zM7.25 14.43l-3.5 2c-.08.05-.17.07-.25.07-.17 0-.34-.1-.43-.25-.14-.24-.06-.55.18-.68l3.5-2c.24-.14.55-.06.68.18.14.24.06.55-.18.68zm4.75.07c-.1 0-.2-.03-.27-.08l-8.5-5.5c-.23-.15-.3-.46-.15-.7.15-.22.46-.3.7-.14L12 13.4l8.23-5.32c.23-.15.54-.08.7.15.14.23.07.54-.16.7l-8.5 5.5c-.08.04-.17.07-.27.07zm8.93 1.75c-.1.16-.26.25-.43.25-.08 0-.17-.02-.25-.07l-3.5-2c-.24-.13-.32-.44-.18-.68s.44-.32.68-.18l3.5 2c.24.13.32.44.18.68z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://pinterest.com/pin/create/button/?url={url}&amp;media={url}&amp;description=ZolaTV - {name}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--pinterest resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M12.14.5C5.86.5 2.7 5 2.7 8.75c0 2.27.86 4.3 2.7 5.05.3.12.57 0 .66-.33l.27-1.06c.1-.32.06-.44-.2-.73-.52-.62-.86-1.44-.86-2.6 0-3.33 2.5-6.32 6.5-6.32 3.55 0 5.5 2.17 5.5 5.07 0 3.8-1.7 7.02-4.2 7.02-1.37 0-2.4-1.14-2.07-2.54.4-1.68 1.16-3.48 1.16-4.7 0-1.07-.58-1.98-1.78-1.98-1.4 0-2.55 1.47-2.55 3.42 0 1.25.43 2.1.43 2.1l-1.7 7.2c-.5 2.13-.08 4.75-.04 5 .02.17.22.2.3.1.14-.18 1.82-2.26 2.4-4.33.16-.58.93-3.63.93-3.63.45.88 1.8 1.65 3.22 1.65 4.25 0 7.13-3.87 7.13-9.05C20.5 4.15 17.18.5 12.14.5z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://www.linkedin.com/shareArticle?mini=true&amp;url={url}&amp;title=ZolaTV - {name}&amp;summary=ZolaTV - {name}&amp;source={url}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--linkedin resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M6.5 21.5h-5v-13h5v13zM4 6.5C2.5 6.5 1.5 5.3 1.5 4s1-2.4 2.5-2.4c1.6 0 2.5 1 2.6 2.5 0 1.4-1 2.5-2.6 2.5zm11.5 6c-1 0-2 1-2 2v7h-5v-13h5V10s1.6-1.5 4-1.5c3 0 5 2.2 5 6.3v6.7h-5v-7c0-1-1-2-2-2z"/> \
                    </svg> \ 
                </div> \ 
            </div> \ 
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://reddit.com/submit/?url={url}&amp;resubmit=true&amp;title=ZolaTV - {name}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--reddit resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M24 11.5c0-1.65-1.35-3-3-3-.96 0-1.86.48-2.42 1.24-1.64-1-3.75-1.64-6.07-1.72.08-1.1.4-3.05 1.52-3.7.72-.4 1.73-.24 3 .5C17.2 6.3 18.46 7.5 20 7.5c1.65 0 3-1.35 3-3s-1.35-3-3-3c-1.38 0-2.54.94-2.88 2.22-1.43-.72-2.64-.8-3.6-.25-1.64.94-1.95 3.47-2 4.55-2.33.08-4.45.7-6.1 1.72C4.86 8.98 3.96 8.5 3 8.5c-1.65 0-3 1.35-3 3 0 1.32.84 2.44 2.05 2.84-.03.22-.05.44-.05.66 0 3.86 4.5 7 10 7s10-3.14 10-7c0-.22-.02-.44-.05-.66 1.2-.4 2.05-1.54 2.05-2.84zM2.3 13.37C1.5 13.07 1 12.35 1 11.5c0-1.1.9-2 2-2 .64 0 1.22.32 1.6.82-1.1.85-1.92 1.9-2.3 3.05zm3.7.13c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9.8 4.8c-1.08.63-2.42.96-3.8.96-1.4 0-2.74-.34-3.8-.95-.24-.13-.32-.44-.2-.68.15-.24.46-.32.7-.18 1.83 1.06 4.76 1.06 6.6 0 .23-.13.53-.05.67.2.14.23.06.54-.18.67zm.2-2.8c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm5.7-2.13c-.38-1.16-1.2-2.2-2.3-3.05.38-.5.97-.82 1.6-.82 1.1 0 2 .9 2 2 0 .84-.53 1.57-1.3 1.87z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://www.xing.com/app/user?op=share;url={url};title=ZolaTV - {name}" \
           target="_blank" \
           rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--xing resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M10.2 9.7l-3-5.4C7.2 4 7 4 6.8 4h-5c-.3 0-.4 0-.5.2v.5L4 10 .4 16v.5c0 .2.2.3.4.3h5c.3 0 .4 0 .5-.2l4-6.6v-.5zM24 .2l-.5-.2H18s-.2 0-.3.3l-8 14v.4l5.2 9c0 .2 0 .3.3.3h5.4s.3 0 .4-.2c.2-.2.2-.4 0-.5l-5-8.8L24 .7V.2z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="whatsapp://send?text=ZolaTV - {name}%20{url}" \
           target="_blank" \ 
           rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--whatsapp resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M20.1 3.9C17.9 1.7 15 .5 12 .5 5.8.5.7 5.6.7 11.9c0 2 .5 3.9 1.5 5.6L.6 23.4l6-1.6c1.6.9 3.5 1.3 5.4 1.3 6.3 0 11.4-5.1 11.4-11.4-.1-2.8-1.2-5.7-3.3-7.8zM12 21.4c-1.7 0-3.3-.5-4.8-1.3l-.4-.2-3.5 1 1-3.4L4 17c-1-1.5-1.4-3.2-1.4-5.1 0-5.2 4.2-9.4 9.4-9.4 2.5 0 4.9 1 6.7 2.8 1.8 1.8 2.8 4.2 2.8 6.7-.1 5.2-4.3 9.4-9.5 9.4zm5.1-7.1c-.3-.1-1.7-.9-1.9-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.1-.2.2-.3.2-.6.1s-1.2-.5-2.3-1.4c-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6s.3-.3.4-.5c.2-.1.3-.3.4-.5.1-.2 0-.4 0-.5C10 9 9.3 7.6 9 7c-.1-.4-.4-.3-.5-.3h-.6s-.4.1-.7.3c-.3.3-1 1-1 2.4s1 2.8 1.1 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.6.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.3-.3-.4-.6-.5z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://news.ycombinator.com/submitlink?u={name}&amp;t=ZolaTV - {name}" \
           target="_blank" \
           rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--hackernews resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 140"> \
                        <path fill-rule="evenodd" \
                              d="M60.94 82.314L17 0h20.08l25.85 52.093c.397.927.86 1.888 1.39 2.883.53.994.995 2.02 1.393 3.08.265.4.463.764.596 1.095.13.334.262.63.395.898.662 1.325 1.26 2.618 1.79 3.877.53 1.26.993 2.42 1.39 3.48 1.06-2.254 2.22-4.673 3.48-7.258 1.26-2.585 2.552-5.27 3.877-8.052L103.49 0h18.69L77.84 83.308v53.087h-16.9v-54.08z"></path> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="http://vk.com/share.php?title=ZolaTV - {name}&amp;url={url}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--vk resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \ 
                        <path d="M21.547 7h-3.29a.743.743 0 0 0-.655.392s-1.312 2.416-1.734 3.23C14.734 12.813 14 12.126 14 11.11V7.603A1.104 1.104 0 0 0 12.896 6.5h-2.474a1.982 1.982 0 0 0-1.75.813s1.255-.204 1.255 1.49c0 .42.022 1.626.04 2.64a.73.73 0 0 1-1.272.503 21.54 21.54 0 0 1-2.498-4.543.693.693 0 0 0-.63-.403h-2.99a.508.508 0 0 0-.48.685C3.005 10.175 6.918 18 11.38 18h1.878a.742.742 0 0 0 .742-.742v-1.135a.73.73 0 0 1 1.23-.53l2.247 2.112a1.09 1.09 0 0 0 .746.295h2.953c1.424 0 1.424-.988.647-1.753-.546-.538-2.518-2.617-2.518-2.617a1.02 1.02 0 0 1-.078-1.323c.637-.84 1.68-2.212 2.122-2.8.603-.804 1.697-2.507.197-2.507z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `,
        ` \
        <a class="resp-sharing-button__link" \
           href="https://telegram.me/share/url?text=ZolaTV - {name}&amp;url={url}" \
           target="_blank" rel="noopener" aria-label=""> \
            <div class="resp-sharing-button resp-sharing-button--telegram resp-sharing-button--small"> \
                <div aria-hidden="true" class="resp-sharing-button__icon resp-sharing-button__icon--solid"> \
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"> \
                        <path d="M.707 8.475C.275 8.64 0 9.508 0 9.508s.284.867.718 1.03l5.09 1.897 1.986 6.38a1.102 1.102 0 0 0 1.75.527l2.96-2.41a.405.405 0 0 1 .494-.013l5.34 3.87a1.1 1.1 0 0 0 1.046.135 1.1 1.1 0 0 0 .682-.803l3.91-18.795A1.102 1.102 0 0 0 22.5.075L.706 8.475z"/> \
                    </svg> \
                </div> \
            </div> \
        </a> \
        `
    ]
    document.body.style.overflowY = "hidden"
    popupShareInput.value = url
    templates.forEach((value => {
        resultHTML += value.fmt({
            name: name,
            url: url
        })
    }))
    popupShareMsgs.innerHTML = resultHTML
    popupShare.classList.add('share-popup_active')
    copyBtn.addEventListener('click', (event) => {
        popupShareInput.focus()
        popupShareInput.select()
        try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
        } catch (err) {
        }
    })
    popupShareBg.addEventListener('click', (event) => {
        popupShare.classList.remove('share-popup_active')
        document.body.style.overflowY = "visible"
        popupShareMsgs.innerHTML = ''
    })

}

function removeFromHistory(params, classname) {
    let type = params.getAttribute('data-type')
    let elid = params.getAttribute('data-elid')
    let popups = document.querySelector('.popups')
    let template = ` \
         <div class="popup-rm popup-rm_active"> \
            <div class="popup-rm__content"> \ 
                <div class="popup-rm__text"> \
                    {text} \
                </div> \
                <div class="popup-rm__btns"> \
                    <button onclick="{onyes}">Yes</button> \
                    <button onclick="{onno}">No, keep it</button> \
                </div> \
            </div> \
            <div class="popup-rm__background"> \
            </div> \
        </div> \
    `
    popups.innerHTML = template.fmt({
        text: "Remove<br/>from Watch list?",
        onyes: `removeFromHistoryHandler('${type}','${elid}');`,
        onno: "closePopup('popup-rm');"
    })
    document.body.style.overflowY = "hidden"
}

function removeFromHistoryHandler(type, id) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/remove-from-hl`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "type": type,
            "id": id
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
            window.location.reload();
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        }
    })
}

function removeFromWl(params, classname) {
    let type = params.getAttribute('data-type')
    let elid = params.getAttribute('data-elid')
    let popups = document.querySelector('.popups')
    let template = ` \
         <div class="popup-rm popup-rm_active"> \
            <div class="popup-rm__content"> \ 
                <div class="popup-rm__text"> \
                    {text} \
                </div> \
                <div class="popup-rm__btns"> \
                    <button onclick="{onyes}">Yes</button> \
                    <button onclick="{onno}">No, keep it</button> \
                </div> \
            </div> \
            <div class="popup-rm__background"> \
            </div> \
        </div> \
    `
    popups.innerHTML = template.fmt({
        text: "Remove<br/>from Watch list?",
        onyes: `removeFromWlHandler('${type}','${elid}');`,
        onno: "closePPopup('.popup-rm');"
    })
    document.body.style.overflowY = "hidden"
}

function closePPopup(classname) {
    let popups = document.querySelector('.popups')
    popups.innerHTML = ''
    document.body.style.overflowY = "visible"
}

function removeFromWlHandler(type, id) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/remove-from-wl`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "type": type,
            "id": id
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
            window.location.reload();
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        }
    })
}

function AddToChannelsBtn(params) {
    let id = params.getAttribute('data=chid')
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/add-to-channels`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "id": id
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        }
    })
}


function openGenres(id) {
    let popup = document.querySelector(`.filter-popup_page[data-popuptype="1"]`)
    let popupItems = popup.querySelectorAll('.filter-popup__item')
    popup.classList.add('filter-popup_page_active')
    document.body.style.overflowY = "hidden"

    function removeAll(popup, type) {
        let allItem = popup.querySelector('.filter-popup__item[data-itemid="0"]')
        let activeClass = 'filter-popup__item-active'
        switch (type) {
            case "rm":
                allItem.classList.remove(activeClass);
                break;
            case "ad":
                allItem.classList.add(activeClass);
                break;

        }

    }

    function removeAllItems() {
        popupItems.forEach((item => {
            item.classList.remove('filter-popup__item-active')
        }))
    }

    function countAllitems() {
        let allitems = popup.querySelectorAll('.filter-popup__item-active')
        return allitems.length
    }

    popupItems.forEach((item => {
        item.addEventListener('click', (event) => {
            let itemid = item.getAttribute('data-itemid')
            if (itemid == "0") {
                removeAllItems()
                removeAll(popup, 'ad')

            } else {
                removeAll(popup, 'rm')
                console.log(item)
                item.classList.toggle('filter-popup__item-active')
                if (countAllitems() < 1) {
                    removeAll(popup, 'ad')
                }
            }
        })
    }))
    let form = document.querySelector('.form__page_popup')
    let btn = popup.querySelector('.filter-popup__btn')
    btn.addEventListener('click', (event) => {
        let items = popup.querySelectorAll('.filter-popup__item-active')
        let finalArray = []
        items.forEach((item => {
            finalArray.push(item.getAttribute('data-itemid'))
        }))

        form.innerHTML += ` \
                <input type="hidden" name="1" value="${id}"> \
                <input type="hidden" name="2" value="${finalArray.join(',')}"> \
                <input type="hidden" name="3" value="0"> \
                <input type="hidden" name="4" value="0"> \ 
                <input type="hidden" name="5" value="1970,2021"> \
                <input type="hidden" name="6" value="1,10"> \
            `
        if (id == '3') {
            form.innerHTML += ` \
            <input type="hidden" name="7" value="${finalArray.join(',')}"> \
        `
        }
        form.submit()
    })

    // 1: 6
    // 2: 3,9,21
    // 3: 0
    // 4: 0
    // 5: 1970,2021
    // 6: 1,10


}

function openLang(id) {
    let popup = document.querySelector(`.filter-popup_page[data-popuptype="2"]`)
    let popupItems = popup.querySelectorAll('.filter-popup__item')
    popup.classList.add('filter-popup_page_active')
    document.body.style.overflowY = "hidden"

    function removeAll(popup, type) {
        let allItem = popup.querySelector('.filter-popup__item[data-itemid="0"]')
        let activeClass = 'filter-popup__item-active'
        switch (type) {
            case "rm":
                allItem.classList.remove(activeClass);
                break;
            case "ad":
                allItem.classList.add(activeClass);
                break;

        }

    }

    function removeAllItems() {
        popupItems.forEach((item => {
            item.classList.remove('filter-popup__item-active')
        }))
    }

    function countAllitems() {
        let allitems = popup.querySelectorAll('.filter-popup__item-active')
        return allitems.length
    }

    popupItems.forEach((item => {
        item.addEventListener('click', (event) => {
            let itemid = item.getAttribute('data-itemid')
            if (itemid == "0") {
                removeAllItems()
                removeAll(popup, 'ad')

            } else {
                removeAll(popup, 'rm')
                console.log(item)
                item.classList.toggle('filter-popup__item-active')
                if (countAllitems() < 1) {
                    removeAll(popup, 'ad')
                }
            }
        })
    }))
    let form = document.querySelector('.form__page_popup')
    let btn = popup.querySelector('.filter-popup__btn')
    btn.addEventListener('click', (event) => {
        let items = popup.querySelectorAll('.filter-popup__item-active')
        let finalArray = []
        items.forEach((item => {
            finalArray.push(item.getAttribute('data-itemid'))
        }))
        form.innerHTML += ` \
                <input type="hidden" name="1" value="${id}"> \
                <input type="hidden" name="2" value="0"> \
                <input type="hidden" name="3" value="0"> \
                <input type="hidden" name="4" value="${finalArray.join(',')}"> \ 
                <input type="hidden" name="5" value="1970,2021"> \
                <input type="hidden" name="6" value="1,10"> \
            `
        form.submit()
    })

    // 1: 6
    // 2: 3,9,21
    // 3: 0
    // 4: 0
    // 5: 1970,2021
    // 6: 1,10


}

function closePopup(classname) {
    let popup = document.querySelector('.' + classname)
    popup.classList.toggle("popup-rm_active")
    document.body.style.overflowY = "visible"
}


$(function () {
    $('.comments__input').bind('input propertychange', function () {
        var maxLength = $(this).attr('maxlength');
        if ($(this).html().length > maxLength) {
            $(this).html($(this).html().substring(0, maxLength));
        }
    })
});

function openComments() {
    let comBlock = document.querySelector('.comments-popup')
    comBlock.classList.toggle('comments-popup_active')
    document.body.classList.toggle('locked_ovf')
}

function sendComment(type, id, input) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    let q = document.querySelector(input)


    // let errorBlock = document.querySelector('.')
    let errorArray = []
    if (q.length < 1) {
        errorArray.push("Field is empty.")
    }
    if (errorArray.length < 1) {
        request = $.ajax({
            url: `/${currLocale}/sendcomment`,
            type: "post",
            data: {
                "csrfmiddlewaretoken": csrf,
                "id": id,
                "type": type,
                "q": q.innerHTML
            }
        })
        request.done(function (response, textStatus, jqXHR) {
            response = JSON.parse(response)
            if (response.resp == "OK") {
                let request = getUrlVars()
                if (request.season && request.episode) {
                    window.location.replace(window.location.protocol + "//" + window.location.host + window.location.pathname + `?comments=t&season=${request.season}&episode=${request.episode}`)
                } else {
                    window.location.replace(window.location.protocol + "//" + window.location.host + window.location.pathname + "?comments=t")
                }

            } else if (response.resp == "redirect") {
                window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
            } else if (response.resp == "ERR") {
                old_q = q.innerHTML
                q.innerHTML = `<span style="color: #D20000">${response.msg}</span>`
                setTimeout(() => {
                    q.innerHTML = old_q
                }, 1400)
            }
        })
    } else {

    }

}


function setLike(heart, id) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    heart.classList.toggle('likes__heart_active')
    let counter = document.querySelector(`.likes__count[data-counterid="${id}"]`)
    switch (heart.classList.contains('likes__heart_active')) {
        case true:
            counter.innerHTML = parseInt(counter.innerHTML) + 1;
            break;
        case false:
            counter.innerHTML = parseInt(counter.innerHTML) - 1;
            break;
    }

    request = $.ajax({
        url: `/${currLocale}/likecomment`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "id": id,
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
            console.log("liked")
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        } else if (response.resp == "ERR") {
            console.log(response.msg)
        }
    })


}

function changeModeBtn() {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    console.log(csrf)
    request = $.ajax({
        url: `/${currLocale}/mode-change-post`,
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrf
        }
    })
    console.log(request)
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        location.reload()
    })
}


const ratingSlider = new Swiper('.u-rating__slider-container', {
    slidesPerView: 'auto',
    spaceBetween: 10,
    centeredSlides: true,
    touchRatio: 0.5,
    observer: true,
    observeParents: true,
    initialSlide: 10
})


function toggleBlockRatingSlider() {
    let slider = ratingSlider.$wrapperEl[0].parentElement
    if (slider.classList.contains('u-rating_blocked')) {
        slider.classList.remove('u-rating_blocked')
        ratingSlider.enable()
    } else {
        slider.classList.add('u-rating_blocked')
        ratingSlider.disable()
    }
}

function toggleBlockRatingBtns() {
    let slider = ratingSlider.$wrapperEl[0].parentElement
    let shareBtn = document.querySelector('.u-rating__share')
    let rateBtn = document.querySelector('.u-rating__rate')
    let basedA = document.querySelector('.u-rating__based_a')
    let basedB = document.querySelector('.u-rating__based_b')
    if (slider.classList.contains('u-rating_blocked')) {
        shareBtn.classList.remove('u-rating__btn_active')
        basedA.classList.add('u-rating__based_active')

        rateBtn.classList.add('u-rating__btn_active')
        basedB.classList.remove('u-rating__based_active')
    } else {
        shareBtn.classList.add('u-rating__btn_active')
        basedA.classList.remove('u-rating__based_active')

        rateBtn.classList.remove('u-rating__btn_active')
        basedB.classList.add('u-rating__based_active')
    }
}

function openRating() {
    let ratingPopup = document.querySelector('.rating-popup')
    let slider = ratingSlider.$wrapperEl[0].parentElement
    let goto = document.querySelector('.u-rating').getAttribute('data-slideto')
    if (goto != "False") {
        ratingSlider.slideTo(+goto - 1, 0, false)
    }
    ratingPopup.classList.toggle('rating-popup_active')
    document.body.classList.toggle('locked_ovf')
    if (slider.classList.contains('u-rating_blocked')) {
        ratingSlider.disable()
    }
    if (ratingPopup.classList.contains('rating-popup_active')) {
        setTimeout(() => {
            try {
                AndroidFunction.setBottomNavVisibility(false)
            } catch (e) {
            }
        }, 500)
    } else {
        setTimeout(() => {
            try {
                AndroidFunction.setBottomNavVisibility(true)
            } catch (e) {
            }
        }, 500)
    }
}

function updateRating() {
    toggleBlockRatingBtns()
    toggleBlockRatingSlider()
}

function setNewRatings(newRating) {
    console.log(newRating)
    let popupPating = document.querySelector('.u-rating__span-rating')
    let popupbased = document.querySelector('.u-rating__span-based')

    let videoRatingNum = document.querySelector('.video__rating_number')
    let videBasedOn = document.querySelector('.video__span-based')

    let videoDescRat = document.querySelector('.video__decription_rating')
    popupPating.innerHTML = newRating.grade.toFixed(1)
    popupbased.innerHTML = newRating.based
    videoRatingNum.innerHTML = newRating.grade.toFixed(1)
    videBasedOn.innerHTML = newRating.based
    videoDescRat.innerHTML = newRating.grade.toFixed(1)

}

function getNewRating(ct_id, model_id) {
    var result = {}
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/getrating`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "ct_id": ct_id,
            "model_id": model_id
        },
    })

    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
            setNewRatings(response.data)
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        } else if (response.resp == "ERR") {
            console.log(response.msg)
        }
    })

}

function sendNewRating(ct_id, model_id) {
    toggleBlockRatingBtns()
    toggleBlockRatingSlider()
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    let grade = document.querySelector('.u-rating__slide.swiper-slide-active .u-rating_digid').innerHTML
    request = $.ajax({
        url: `/${currLocale}/setrating`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "grade": grade,
            "ct_id": ct_id,
            "model_id": model_id
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        response = JSON.parse(response)
        if (response.resp == "OK") {
            getNewRating(ct_id, model_id)
        } else if (response.resp == "redirect") {
            window.location.replace(document.location.protocol + "//" + document.location.hostname + response.rev)
        } else if (response.resp == "ERR") {
            console.log(response.msg)
        }
    })

}

var AdsPlayer = ''

function adCreateFrame(wrp, link, type, tm, sposter, links, pixel, bid, rem_ad = false) {
    if (rem_ad == true) {
        sendMadf()
        adRemoveFrame(undefined, true)
        return false
    }
    wrp.remove()
    let adContent = document.querySelector('.ad-click__content')
    links = links.split(',')
    let linkCounter = 0
    let uid = ''
    uid = getCookie('u_id')
    try {
        uid = u_id
    } catch (e) {
    }
    if (uid == undefined) {
        uid = 0
    }
    let finalLink = ""
    if (type == "s") {
        finalLink = document.location.protocol + "//" + document.location.hostname + link
    } else {
        finalLink = link
    }
    AdsPlayer = new Playerjs({
        id: "pljs",
        file: finalLink,
        player: 2
    });
    let adclink = document.querySelector('.ad-click__link')
    adclink.setAttribute('href', links[linkCounter] + `?pm_id=${bid}&subId2=${uid}`)
    adclink.addEventListener('click', (event) => {
        adclink.setAttribute('href', links[linkCounter] + `?pm_id=${bid}&subId2=${uid}`)
        linkCounter++
        if (linkCounter > links.length - 1) {
            linkCounter = 0
        }
    })
    let adBlock = document.querySelector('.ad-click')
    let skipBtn = document.createElement('div')
    let pixelbl = document.createElement('div')
    gtag('event', 'show_video_prepoll');
    adBlock.appendChild(skipBtn)
    adBlock.appendChild(pixelbl)
    pixelbl.innerHTML = `<img src="${pixel}" alt="pixel" style="opacity: 0; visibility: hidden">`
    skipBtn.classList.add('ad-click__skip')
    skipBtn.setAttribute('onclick', 'adRemoveFrame(this)')
    skipBtn.innerHTML = `<span class="ad-click__end">${tm}</span><img src="${sposter}" alt="">`
    // setTimeout(() => {
    document.querySelector('.ad-click__skip').classList.add('ad-click__skip_active')
    // }, tm)
    let timeToSk = tm
    let adEndTimeInterval = setInterval(() => {
        document.querySelector('.ad-click__end').innerHTML = timeToSk
        if (timeToSk == 0) {
            clearInterval(adEndTimeInterval)
        }
        timeToSk--
    }, 1000)
    setTimeout(() => {
        clearInterval(adEndTimeInterval)
        skipBtn.innerHTML = `<span class="ad-click__end">Skip Ad</span><img src="${sposter}" alt="">`
        skipBtn.classList.add('ad-click__skip_act')
    }, tm * 1000)
}


function sendMadf() {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/minus-adf`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        console.log(response)
    })
}

function adRemoveFrame(btn, ev = false) {
    if (ev == false) {
        if (!btn.classList.contains('ad-click__skip_act')) {
            return false
        }
    }
    let adBlock = document.querySelector('.ad-click')
    adBlock.remove()
    MainPlayer.api("play")
}

function adGetEndTime() {
    return parseInt(AdsPlayer.api('duration') - AdsPlayer.api('time'))
}


function PlayerjsEvents(event, id, info) {
    console.log(id, event)

    if (id == "admid" && event == "end") {
        closeMidRoll()
    }
    if (event == "end") {
        adRemoveFrame(undefined, true)
    }

}

function setCookie(name, value, options = {}) {

    options = {
        path: '/',
        ...options
    };

    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

function sendDownload(ref_url) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: `/${currLocale}/add_download`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "ref_url": ref_url
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        console.log(response)
    })
}

var downloadsCounter = 0

function appDownload() {
    let ref_url = getCookie('ref_url')
    if (ref_url !== undefined) {
        downloadsCounter++
        if (downloadsCounter > 1) {
            return false
        }
        sendDownload(ref_url)
    }
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function changeLang(code, url) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    console.log(url)
    // setCookie('django_language', code, {secure: true, 'max-age': 2592000});

    request = $.ajax({
        url: "/il8n/setlang/",
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "language": code,
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        // console.log(response)
        window.location = '/'
    })
}

function SaveEventAlanytics(event, addit_info = undefined, pev = false) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
        url: "/analyt/s_event",
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "event": event,
            "url": window.location.href,
            "addit_info": addit_info,
            "pev": pev
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        console.log(response)
    })
}

function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
}


function SaveFirstAlanytics(event, addit_info = undefined, pev = false) {
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    let req = getUrlVars()
    let ad_id = null
    if (req.utm_zid) {
        ad_id = req.utm_zid
    }
    console.log(ad_id)

    request = $.ajax({
            url: "/analyt/s_first",
            type: "post",
            data: {
                "csrfmiddlewaretoken": csrf,
                "url": window.location.href,
                "ad_id": ad_id,
                // "uid": getRandomInt(100000, 9999999),
            },
            success: function (response) {
                if (response != "Error") {
                    setCookie('time_start', Date.now())
                    setCookie('url_start', window.location.href)
                    setCookie('u_id', response)
                    let req = getUrlVars()
                    if (req.utm_zid) {
                        setCookie('ad_id', req.utm_zid)
                    }

                }

            }
        }
    )

}

let midroll_element = document.querySelector('.ad-midroll__wrapper')
var timings = {}
try {
    let times = midroll_element.getAttribute('data-timing').split(',')
    times.forEach((elem) => {
        timings[elem] = false
    })
} catch (e) {

}


function MainplJSevents(event, id, info) {
    console.log(event, id, info)
    if (event == "ui") {
        console.log(event, info)
        let player_lang_btn = document.querySelector('#mainpl_control_button-lang')
        if (info == '1') {
            player_lang_btn.classList.add("player_lang_btn_active")
        } else if (info == '0') {
            player_lang_btn.classList.remove("player_lang_btn_active")
        }

    }
    if (event == "init") {
        let player_lang_btn = document.querySelector('#mainpl_control_button-lang')
        player_lang_btn.classList.add("player_lang_btn_active")
        let player_lang_link = document.querySelector('#mainpl_control_button-lang > pjsdiv:nth-child(3)')
        player_lang_link.classList.add('player_lang_link')
        let lang_txt = document.createElement('pjsdiv')
        lang_txt.classList.add('player_lang_txt')
        lang_txt.innerText = MainPlayer.api('audiotrack')
        player_lang_btn.appendChild(lang_txt)
        let player_subs_btn = document.querySelector('#mainpl_control_subtitle_btn')
        if (MainPlayer.api('subtitles') == "") {
            player_subs_btn.classList.add("player_subtitle_hide")
        }
    }
    if (event == "play") {
        console.log(event);
    }
    if (event == "time") {
        for (i = 0; i < Object.keys(timings).length; i++) {
            ev_time = parseInt(info)
            if (ev_time == parseInt(Object.keys(timings)[i]) && timings[Object.keys(timings)[i]] == false) {
                let midroll_element = document.querySelector('.ad-midroll__wrapper')
                let remadd = midroll_element.getAttribute('data-remad')
                if (remadd == "true") {
                    console.log('adskip')
                    sendMadf()
                    timings[Object.keys(timings)[i]] = true
                } else {
                    MainPlayer.api('pause')
                    showMidRoll()
                    timings[Object.keys(timings)[i]] = true
                }

            }
        }
    }
}

function showMidRoll() {

    let mp_fullscreen = MainPlayer.api('isfullscreen')
    let mp_element = document.querySelector('#mainpl')
    let midroll_element = document.querySelector('.ad-midroll__wrapper')
    let mid_clink = document.querySelector('.ad-midroll_link')
    let links = midroll_element.getAttribute('data-links').split(',')
    let to_skip_time = midroll_element.getAttribute('data-skiptime')
    let s_poster = midroll_element.getAttribute('data-poster')
    let pixel = midroll_element.getAttribute('data-pixel')
    let bid = midroll_element.getAttribute('data-bid')

    let linkCounter = 0
    let uid = ''
    uid = getCookie('u_id')
    try {
        uid = u_id
    } catch (e) {
    }
    if (uid == undefined) {
        uid = 0
    }
    let pixelbls = document.createElement('div')
    gtag('event', 'show_video_midroll');
    midroll_element.appendChild(pixelbls)
    pixelbls.innerHTML = `<img src="${pixel}" alt="pixel" style="opacity: 0; visibility: hidden">`
    mid_clink.setAttribute('href', links[linkCounter] + `?pm_id=${bid}&subId2=${uid}`)
    mid_clink.addEventListener('click', (event) => {
        mid_clink.setAttribute('href', links[linkCounter] + `?pm_id=${bid}&subId2=${uid}`)
        linkCounter++
        if (linkCounter > links.length - 1) {
            linkCounter = 0
        }
    })
    if (mp_fullscreen) {
        mp_element.classList.add('mp_hide_on_fsc')
        midroll_element.classList.add('midroll_active_fsc')
    } else {
        midroll_element.classList.add('midroll_active')
    }

    let skipBtn = document.createElement('div')
    let pixelbl = document.createElement('div')
    midroll_element.appendChild(skipBtn)
    skipBtn.classList.add('ad-click__skip')
    skipBtn.setAttribute('onclick', 'closeMidRbtn(this)')
    skipBtn.innerHTML = `<span class="ad-click__end">${to_skip_time}</span><img src="${s_poster}" alt="">`
    // setTimeout(() => {
    document.querySelector('.ad-click__skip').classList.add('ad-click__skip_active')
    // }, tm)
    let timeToSk = to_skip_time
    let adEndTimeInterval = setInterval(() => {
        document.querySelector('.ad-click__end').innerHTML = timeToSk
        if (timeToSk == 0) {
            clearInterval(adEndTimeInterval)
        }
        timeToSk--
    }, 1000)
    setTimeout(() => {
        clearInterval(adEndTimeInterval)
        skipBtn.innerHTML = `<span class="ad-click__end">Skip Ad</span><img src="${s_poster}" alt="">`
        skipBtn.classList.add('ad-click__skip_act')
    }, to_skip_time * 1000)
    //settimeout + time
    MidrollAdPl.api('play')

}

function closeMidRoll() {
    let mp_fullscreen = MainPlayer.api('isfullscreen')
    let mp_element = document.querySelector('#mainpl')
    document.querySelector('.ad-click__skip').remove()
    let midroll_element = document.querySelector('.ad-midroll__wrapper')
    mp_element.classList.remove('mp_hide_on_fsc')
    midroll_element.classList.remove('midroll_active_fsc')
    midroll_element.classList.remove('midroll_active')
    MidrollAdPl.api('stop')
    MainPlayer.api('play')
}

function closeMidRbtn(btn, ev = false) {
    if (ev == false) {
        if (!btn.classList.contains('ad-click__skip_act')) {
            return false
        }
    }
    closeMidRoll()
}

var counter_lang_btn_pl = false

function openAudioTracks() {
    if (counter_lang_btn_pl == false) {
        let player_lang_btn = document.querySelector('#mainpl_control_button-lang')
        let list_elem = document.createElement("pjsdiv")
        list_elem.classList.add('player_lang_list')
        player_lang_btn.appendChild(list_elem)
        let ul_elem = document.createElement('ul')
        list_elem.appendChild(ul_elem)
        let curr_at = MainPlayer.api('audiotrack')
        MainPlayer.api('audiotracks').forEach((elem, id) => {

            let li_elem = document.createElement('li')
            if (elem == curr_at) {
                li_elem.classList.add('player_lang_li_active')
            }
            li_elem.setAttribute('onclick', `MainPlayer.api('audiotrack', '${id}');closeAudioTracks();updateAudioBtn();`)
            li_elem.innerText = elem
            if (elem != '') {
                ul_elem.appendChild(li_elem)
            }
        })
    } else {
        let player_lang_list = document.querySelector('pjsdiv.player_lang_list')
        player_lang_list.remove()
    }
    counter_lang_btn_pl = !counter_lang_btn_pl
}

function closeAudioTracks() {
    counter_lang_btn_pl = false
    let list = document.querySelector('pjsdiv.player_lang_list')
    list.remove()
}

function updateAudioBtn() {
    let pl_txt = document.querySelector('pjsdiv.player_lang_txt')
    pl_txt.innerHTML = MainPlayer.api('audiotrack')
}

// var counter_subtitle_btn_pl = false

function selectSubtitle(name, disable = false) {
    if (disable !== true) {
        const sub_path = "http://subs.zola.bz:8880"
        const subtitle_url = `${sub_path}/${name}`
        MainPlayer.api('subtitle', subtitle_url)
    } else {
        MainPlayer.api('subtitle', -1)
    }
    closeSubtitles()

}

function debounce(func, wait, immediate) {
    let timeout;

    return function executedFunction() {
        const context = this;
        const args = arguments;

        const later = function () {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };

        const callNow = immediate && !timeout;

        clearTimeout(timeout);

        timeout = setTimeout(later, wait);

        if (callNow) func.apply(context, args);
    };
}

let subtitlesSearchListener = debounce((e) => subtitleSearchQtoDb(e.target.value), 250)

function closeSubtitles() {
    const subtitlesPopup = document.querySelector(".subtitle-popup")
    const subtitlesInput = subtitlesPopup.querySelector(".subtitle__input")
    subtitlesPopup.classList.remove('subtitle-popup_active')
    subtitlesInput.removeEventListener('keyup', subtitlesSearchListener)
    document.body.style.overflowY = "auto"
}


function subtitleSearchQtoDb(q) {
    console.log(q)
    const csrf = $('input[name="csrfmiddlewaretoken"]').val()
    const content = document.querySelector('.subtitle__results_ct')
    request = $.ajax({
        url: `/${currLocale}/subtitle-search.json`,
        type: "post",
        data: {
            "csrfmiddlewaretoken": csrf,
            "q": q,
        }
    })
    request.done(function (response, textStatus, jqXHR) {
        if (response.length > 0) {
            response = JSON.parse(response)
            template = `\
                    <li>\
                        <a data-id="{id}" class="subtitle-link" onclick="selectSubtitle('langs/{language}/unzipped/{file_name}{file_extension}')">\
                            <span class="subtitle-link__name">{file_name}</span>\
                            <span class="subtitle-link__lang">{language}</span>\
                        </a>\
                    </li>\
            `
            returnHTML = ''
            response.forEach(element => {
                returnHTML += template.fmt({
                    id: element.id || "",
                    file_name: element.file_name || "",
                    file_extension: element.file_extension || "",
                    language: element.language || "",
                })
            })
            if (returnHTML.length < 1) {
                content.innerHTML = ` \
                <div class="subtitle__results_not-found">No match</div> \
                `
            } else {
                content.innerHTML = returnHTML
            }

        }
    })
}

function openSubtitles() {
    const subtitlesPopup = document.querySelector(".subtitle-popup")
    const subtitlesInput = subtitlesPopup.querySelector(".subtitle__input")
    subtitlesPopup.classList.add('subtitle-popup_active')
    subtitlesInput.addEventListener('keyup', subtitlesSearchListener)
    MainPlayer.api('exitfullscreen')
    document.body.style.overflowY = "hidden"
}


function setTimeCookie() {
    if (getCookie('time_start') == undefined) {
        SaveFirstAlanytics()
    }
}

// const completedPPM = new Event('completedppm', {
//   bubbles: true,
//   cancelable: true,
//   composed: false
// })
const completedLoadPPM = new CustomEvent("completedLoadPPM", {
    detail: {},
    bubbles: true,
    cancelable: true,
    composed: false,
});


function PopupManager() {
    let uid = getCookie('u_id')
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    request = $.ajax({
            url: `/${currLocale}/get-pp`,
            type: "post",
            data: {
                "csrfmiddlewaretoken": csrf,
                "uid": uid,
            },
            success: function (response) {
                if (response != 'Error') {
                    response = JSON.parse(response)
                    let pp_html = document.querySelector('.popup-manager')
                    response.forEach((el) => {
                        let upp = getCookie('upp')
                        if (upp != undefined) {
                            upp_list = upp.split(';')
                            upp_curr_count = upp_list.filter(x => x == el.id).length
                            if (upp_curr_count < el.show_times) {
                                let ppm_el = document.createElement('div')
                                ppm_el.classList.add('ppm_popup')
                                ppm_el.setAttribute('data-loadtime', el.load_time)
                                ppm_el.setAttribute('data-id', el.id)
                                pp_html.appendChild(ppm_el)
                                ppm_el.innerHTML = el.html
                            }
                            console.log("upp:", upp_curr_count)
                        }
                    })
                    pp_html.dispatchEvent(completedLoadPPM);
                }
                console.log(response)
            }
        }
    )
}

let actived_l = []
let ppm_act = document.querySelector('.popup-manager')
ppm_act.addEventListener('completedLoadPPM', (event) => {
    let pp_els = ppm_act.querySelectorAll('.ppm_popup')
    pp_els.forEach((el) => {
        actived_l.push({el: el, showed: false})
    })
    showPPm()
    ratingPopup()
    regPopup()

    console.log(actived_l)
})

function showPPm() {
    for (let i = 0; i < actived_l.length; i++) {
        console.log(actived_l[i].el.querySelector('.pp-register'))
        if (actived_l[i].el.querySelector('.pp-register')) {
            let cont = new RegExp("login|register|profile|recover-email|recover-phone").test(window.location.href)
            if (cont) {
                continue
            }
        }
        if (!actived_l[i].showed) {
            setTimeout(() => {
                actived_l[i].el.classList.add('ppm_popup_active')
            }, actived_l[i].el.getAttribute('data-loadtime') * 1000)
            upp = getCookie('upp')
            if (upp != undefined) {
                upp += `${actived_l[i].el.getAttribute('data-id')};`
            } else {
                upp = `${actived_l[i].el.getAttribute('data-id')};`
            }
            setCookie('upp', upp)
            document.querySelectorAll('.pp_bg').forEach((el) => {
                el.addEventListener('click', (event) => {
                    closePP()
                })
            })
            actived_l[i].showed = true
            break
        }
    }
}

function regPopup() {
    try {
        let rpp = document.querySelector('.pp-register')
        let close_btn = rpp.querySelector('.pp_close_btn')
        close_btn.addEventListener('click', (event) => {
            closePP()
        })

    } catch (e) {
    }

}

function ratingPopup() {
    try {
        let rpp = document.querySelector('.pp-rating')
        let stars = rpp.querySelectorAll('.pp_star')
        let info_req = rpp.querySelector('.pp_info_req')
        for (let i = 0; i < stars.length; i++) {
            stars[i].addEventListener('click', (event) => {
                stars.forEach((el) => {
                    el.classList.remove('pp_star_active')
                })
                for (let j = 0; j <= i; j++) {
                    stars[j].classList.add('pp_star_active')
                }
            })
        }
        let submit = rpp.querySelector('.pp_rate_us')
        submit.addEventListener('click', (event) => {
            let quant_stars = rpp.querySelectorAll('.pp_star_active')
            if (quant_stars.length < 1) {
                console.log('OK')
                info_req.innerHTML = '<span class="pp_info_red">Please select from 1 to 5 stars</span>'
            } else {
                let uid = getCookie('u_id')
                let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value
                let message = rpp.querySelector('.pp_feetback').value
                request = $.ajax({
                    url: `/${currLocale}/send-rating`,
                    type: "post",
                    data: {
                        "csrfmiddlewaretoken": csrf,
                        "uid": uid,
                        "rating": quant_stars.length,
                        "message": message,
                    },
                    success: function (response) {
                        if (response != "USER-ERROR") {
                            info_req.innerHTML = '<span class="pp_info_green">Thanks, your rating has been sent</span>'
                            setTimeout(() => {
                                closePP()
                            }, 1200)
                        } else {
                            info_req.innerHTML = '<span class="pp_info_red">User-error</span>'
                        }
                    }
                })

            }

        })
        let close_btn = rpp.querySelector('.pp_close_btn')
        close_btn.addEventListener('click', (event) => {
            closePP()
        })
    } catch (e) {
    }
}

function closePP() {
    document.querySelectorAll('.ppm_popup_active').forEach((el) => {
        el.classList.remove('ppm_popup_active')
    })
    showPPm()
}
