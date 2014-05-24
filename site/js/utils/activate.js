var tabs = $('#user-bar').children();

tabs.each(
	function(this){
		this.onclick(
			function(e){
        tabs.removeClass('active');
        this.addClass('active');
			});
});