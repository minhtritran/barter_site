$(document).ready(function(){
    var $rating = 0;
    var $id = 0;
    var $tag_count = 0;

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

    $('#id_tags_input').on('input', function() {
        //Characters at the end of the String that triggers tag creation
        var KEYS = [';', ','];
        //Everything in the input field, with spaces replaced with dashes
        var input = $(this)[0].value;
        input = input.replace(/ /g, '-').toLowerCase();
        //Element that holds the current tag data
        var current_tags = $('#id_tags')[0];

        //If the text is not empty(to prevent negative substring index, triggers when deleting)
            //and the input is not a KEY character
        //Else clear suggestions and input field
        if(input.length != 0 && $.inArray(input, KEYS) == -1 ){
            //separates the KEY character at the end
            var text = input.substr(0, input.length - 1);
            var last_char = input.substr(input.length - 1);
            //If the last character is one of the KEYS
            //Else search the db for similar tags
            if($.inArray(last_char, KEYS) >= 0){
                //If the tag already exists, clear input field and do nothing
                if($.inArray(text, current_tags.value.split(',')) >= 0){
                    $(this)[0].value = '';
                    return;
                }
                create_tag(text);

                //If there's no existing tag insert without comma
                if(current_tags.value == '')
                    current_tags.value += text;
                else
                    current_tags.value += ',' + text;

                //Clear input Field
                $(this)[0].value = '';
            }
            else {
                ajaxPost('update', {'text': input},
                    function (content) {
                        var ele = $('#suggestions')[0];
                        var suggestions = content['msg'];
                        $('#suggestions').empty();
                        for (var i = 0; i < suggestions.length; ++i) {
                            if ($.inArray(suggestions[i], current_tags.value.split(',')) < 0) {
                                var link = document.createElement("span");
                                link.className = "btn btn-link";
                                link.textContent = suggestions[i];
                                link.onclick = add_tag;

                                ele.appendChild(link);
                            }
                        }
                    }, true);
            }
        }
         else {
            $(this)[0].value = '';
            $('#suggestions').empty();
        }
    });

    function create_tag(label){
        var tag = document.createElement("div");
        tag.className = "btn btn-info";
        //Capitalize First letters of words (does not effect slug input)
        var words = label.split('-');
        var formatted_label = '';
        for(var i = 0; i < words.length; i++) {
            formatted_label += words[i].charAt(0).toUpperCase() + words[i].substr(1) + '-';
        }
        tag.textContent = label;
        tag.onclick = remove_tag;
        $('#current_tags')[0].appendChild(tag);
    }

    function add_tag(){
        var current_tags = $('#id_tags')[0];
        if(current_tags.value == '')
            current_tags.value += this.textContent;
        else
            current_tags.value += ',' + this.textContent;
        create_tag(this.textContent);
        $('#suggestions').empty();
        $('#id_tags_input')[0].value = '';
        this.remove();
    }

    function remove_tag(){
        var current_tags = $('#id_tags')[0];
        var cut = current_tags.value.split(',');
        var index = cut.indexOf(this.textContent.toLowerCase());
        if (index !== -1)
            cut[index] = '';
        cut = cut.join();
        var last_char = cut.substr(cut.length -1);
        if(last_char == ',')
            cut = cut.substr(0,cut.length - 1);
        current_tags.value = cut;
        this.remove();
    }

    $('.progress-bar').each(function() {
      var min = $(this).attr('aria-valuemin');
      var max = $(this).attr('aria-valuemax');
      var now = $(this).attr('aria-valuenow');
      var siz = (now-min)*100/(max-min);
      $(this).css('width', siz+'%');
      $(this).text(now);
    });
});