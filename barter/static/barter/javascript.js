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

    $('#id_tags_input').on('input',function() {
        var text = $(this)[0].value;
        if(text != ''){
            if($.inArray(text.substr(text.length - 1), [' ', ';', ',']) >= 0){
                tag = document.createElement("div");
                tag.className = "btn btn-info";
                tag.innerText = text.substr(0,text.length - 1);
                $('#current_tags')[0].appendChild(tag);
                $('#id_tags')[0].value += text + ',';
                $(this)[0].value = '';
            }
            else
                ajaxPost('update',{'input': text},
                function(content){
                    $('#suggestions').text(content['msg']);
                }, true);
        }
         else $('#suggestions').text('');
    });

    $('.progress-bar').each(function() {
      var min = $(this).attr('aria-valuemin');
      var max = $(this).attr('aria-valuemax');
      var now = $(this).attr('aria-valuenow');
      var siz = (now-min)*100/(max-min);
      $(this).css('width', siz+'%');
      $(this).text(now);
    });
});