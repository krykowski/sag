// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart']});
	
$(document).ready(function() {
	var dates = $("#id_dateF, #id_dateT").datepicker({
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		maxDate: current_date,
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
	
	$(".datepicker").datepicker({
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		defaultDate: current_date,
	});
	
	$(".datepicker_future").datepicker({
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true,
		minDate: current_date,
		defaultDate: current_date,
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
	
	function setPrice() {
		var id = $('#buyWalletItemForm #id_item').val();
		
		$('#itemPrice').html('<div class="ajaxLoader"></div>');
		
		$.ajax({
			url: '/market/item/' + id + '/json/',
			success: function(data) {
				$('#itemPrice').html(parseFloat(data['open_price']).toFixed(2) + ' PLN');
			},
			error: function(jqXHR, textStatus, errorThrown) {
				$('#itemPrice').html('Brak danych');
			}
		});
	}
	
	$('#buyWalletItemForm #id_item').change(function() {
		setPrice();
	});
	setPrice();
});
