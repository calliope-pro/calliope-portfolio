$(function(){
    $('#confirm_delete').on('click', function() {
        let flag = confirm('削除しますか？');
        if (!flag) {
            return false;
        }
    });
});