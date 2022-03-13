(function () {
    function accordion(id, menuProp, contentProp) {
        const ACTIVE_CLASS_NAME = 'is-active';
        const DATA_PROP_PREFIX = 'data-';

        const $accordion = document.getElementById(id);
        const $menuList = $accordion.querySelectorAll(`[${DATA_PROP_PREFIX}${menuProp}]`);
        const $contentList = $accordion.querySelectorAll(`[${DATA_PROP_PREFIX}${contentProp}]`);

        function init() {
            $contentList.forEach((element) => {
                element.style.display = 'none';
            });
        }
        init();

        const handleClick = (e) => {
            const targetVal = e.currentTarget.dataset[`${menuProp}`];
            const $content = $accordion.querySelector(`[${DATA_PROP_PREFIX}${contentProp}='${targetVal}']`);

            $content.classList.toggle(ACTIVE_CLASS_NAME);
            if ($content.classList.contains(ACTIVE_CLASS_NAME)) {
                $content.style.display = 'block';
            } else {
                $content.style.display = 'none';
            }

            const $toggleImg = e.currentTarget.querySelector('img.toggle');
            $toggleImg.classList.toggle(ACTIVE_CLASS_NAME);
            if ($toggleImg.classList.contains(ACTIVE_CLASS_NAME)) {
                $toggleImg.style.transform = 'rotate(-90deg)';
            } else {
                $toggleImg.style.transform = 'rotate(0deg)';
            }
        };

        for (let i = 0; i < $menuList.length; i++) {
            $menuList[i].addEventListener('click', handleClick);
        }
    }
    accordion('lang-accordion', 'lang', 'detail');


    function scrollToTop() {
        scrollTo(0, 0);
    }
    const $scrollButton = document.getElementById('scroll-to-top');
    $scrollButton.addEventListener('click', scrollToTop)

    function slide_section_from_left() {
        const $sections = document.querySelectorAll('section.container_section');
        $sections.forEach((element) => {
            if(window.innerHeight > element.getBoundingClientRect().top + 200) {
                element.classList.add('is-show');
            }
        })
    }
    window.addEventListener('scroll', () => slide_section_from_left());
})();