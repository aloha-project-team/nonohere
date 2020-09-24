function changenoyes(){
    if($('input:radio[id=no]').is(':checked')){
        $('#no_div').show();
        $('#yes_div').hide();
    }else{
        $('#no_div').hide();
        $('#yes_div').show();
    }
}