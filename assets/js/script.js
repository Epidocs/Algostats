$(document).ready(function() {
	// Get current URL path and assign 'active' class
	var pathname = window.location.pathname;
	var $link = $('#navbar .navbar-nav a[href="' + pathname + '"]');
	$link.addClass('active');
});
