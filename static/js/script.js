/*$(document).ready( function(){
    $("#search-form").hide();
    $("#search-button").hover( function(){
    
    $("#search-form").show();
    $("#search-form").focus( function(){
        if (this.focusout() == 0 && this.val().length=="0" ){
            this.hide()
        };
    });
    
});

$("#search-button").hover({
    
    $("#search-form").show();
    $("#search-form").focus( function(){
        if (this.focusout() == 0 && this.val().length=="0" ){
            this.hide()
        };
                          
        if ( (this.focusout()==0) && (this.val().length != "0")) 
    });
    
});
})
*/

$('.hover').hover(function(){
			$(this).addClass('flip');
		},function(){
			$(this).removeClass('flip');
		});
	

