// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});
	
$(document).ready(function() {
	var dates = $("#id_dateF, #id_dateT").datepicker({
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		onSelect: function(selectedDate) {
			var option = this.id == "id_dateF" ? "minDate" : "maxDate",
				instance = $(this).data("datepicker"),
				date = $.datepicker.parseDate(
					instance.settings.dateFormat ||
					$.datepicker._defaults.dateFormat,
					selectedDate, instance.settings );
			dates.not(this).datepicker("option", option, date);
		}
	});
	
	function togglePriceType() {
		var chart = $('#id_chartType').val();
		
		if(chart == 'candle')
			$('#priceTypeWraper').hide();
		else
			$('#priceTypeWraper').show();
	}
	
	$('#id_chartType').change(function() {
		togglePriceType()
	});
	togglePriceType();
});
