(function () {
    const ACTIVE_CLASS_NAME = 'is-active';

    function accordion(id, menuProp, contentProp) {
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
    accordion('program-lang-accordion', 'lang', 'detail');

})();