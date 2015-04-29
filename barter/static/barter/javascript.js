/**
 * Created by Andy on 4/27/2015.
 */

//function changeRatingOn(ele){
//    while(ele.id != null){
//        ele.removeClass("glyphicon glyphicon-star-empty");
//        ele.addClass("glyphicon glyphicon-star");
//        ele = ele.previousElementSibling;
//    }
//}
//
//function changeRatingOff(ele){
//    while(ele.name > 0){
//        alert(ele.name);
//        ele.class = "glyphicon glyphicon-star-empty";
//        ele = ele.previousElementSibling;
//    }
//}
//
//
//$(".glyphicon").hover(
//   function () {
//     $(this).toggleClass('glyphicon glyphicon-star');
//   },
//  function () {
//      $(this).toggleClass('glyphicon glyphicon-star');
//   }
//);

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
        $('span').toggleClass('glyphicon glyphicon-chevron-down');
        $('span').toggleClass('glyphicon glyphicon-chevron-up');
        $('.password').slideToggle(300);
    });
});