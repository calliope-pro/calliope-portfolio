(function () {
    document.getElementById('js_confirm_delete').addEventListener('click', function (e) {
        const flag = confirm('削除しますか？');
        if (!flag) {
            e.preventDefault();
        }
    });
})();

(function () {
    document.querySelectorAll('.card').forEach((element) => {
        element.addEventListener('mouseover', () => {
            element.classList.add('shadow-lg');
        });
        element.addEventListener('mouseout', () => {
            element.classList.remove('shadow-lg');
        });
    });
})();