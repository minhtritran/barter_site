$(function(){
    $rating = 0;
    $id = 0;

    $('.stars span').hover(
        function () {

            $id = $(this)[0].id;

            $('.stars span').each(function(){
                if($(this)[0].id <= $id){
                    $(this).removeClass('glyphicon glyphicon-star-empty');
                    $(this).addClass('glyphicon glyphicon-star');
                }
                else{
                    $(this).removeClass('glyphicon glyphicon-star');
                    $(this).addClass('glyphicon glyphicon-star-empty');
                }
            });
        },
        function () {

            $id = $(this)[0].id;

            $('.stars span').each(function(){
                if($(this)[0].id > $rating){
                    $(this).removeClass('glyphicon glyphicon-star');
                    $(this).addClass('glyphicon glyphicon-star-empty');
                }
                else{
                    $(this).removeClass('glyphicon glyphicon-star-empty');
                    $(this).addClass('glyphicon glyphicon-star');
                }
            });
        }
    );
    $('.stars span').click(
        function(){
            $rating = $(this)[0].id;
            $('#id_rating')[0].value = $rating;
        });

    $('h2').on('click', function(){
        $('h2 span').toggleClass('glyphicon glyphicon-chevron-down');
        $('h2 span').toggleClass('glyphicon glyphicon-chevron-up');
        $('.hiddenform').slideToggle(300);
    });

    $('#id_tags').on('input',function() {
        if($(this)[0].value != '')
            ajaxPost('update',{'input': $(this)[0].value},
            function(content){
                $('#suggestions').text(content['msg']);
            }, true);
        else $('#suggestions').text('');
    });

});