$(function(){
    var $rating = 0;
    var $id = 0;

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
        var current_tags = $('#id_tags')[0];
        if(text.length != ''){
            var input = text.substr(0, text.length - 1);

            if($.inArray(text, [' ', ';', ',']) >= 0 ){
                $(this)[0].value = '';
                return;
            }

            if($.inArray(text.substr(text.length - 1), [' ', ';', ',']) >= 0){
                if($.inArray(input, current_tags.value.split(',')) > 0){
                    $(this)[0].value = '';
                    return;
                }
                create_tag(input);
                if(text.substr(text.length - 1) == ',')
                    current_tags.value += text;
                else
                    current_tags.value += text + ',';
                $(this)[0].value = '';
            }
            else
                ajaxPost('update',{'input': text},
                function(content){
                    var ele = $('#suggestions')[0];
                    var suggestions = content['msg'];
                    $('#suggestions').empty();
                    for (var i = 0; i < suggestions.length; ++i) {
                        if($.inArray(suggestions[i], current_tags.value.split(',')) < 0) {
                            var link = document.createElement("span");
                            link.className = "btn btn-link";
                            link.innerText = suggestions[i];
                            link.onclick = add_tag;

                            ele.appendChild(link);
                        }
                    }
                }, true);
        }
         else $('#suggestions').text('');
    });

    function create_tag(label){
        var tag = document.createElement("div");
        tag.className = "btn btn-info";
        tag.innerText = label;
        tag.onclick = remove_tag;
        $('#current_tags')[0].appendChild(tag);
    }

    function add_tag(){
        $('#id_tags')[0].value += this.innerText + ',';
        create_tag(this.innerText);
        $('#suggestions').text('');
        $('#id_tags_input')[0].value = '';
        this.remove();
    }

    function remove_tag(){
        var cut = $('#id_tags')[0].value.split(this.innerText + ',');
        $('#id_tags')[0].value = cut[0] + cut[1];
        this.remove();
    };

    $('.progress-bar').each(function() {
      var min = $(this).attr('aria-valuemin');
      var max = $(this).attr('aria-valuemax');
      var now = $(this).attr('aria-valuenow');
      var siz = (now-min)*100/(max-min);
      $(this).css('width', siz+'%');
      $(this).text(now);
    });
});