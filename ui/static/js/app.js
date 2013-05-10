$(function() {
	$('select[name=lights]').change(function() {
		//console.log( $(this) );
		//console.log( $(this) );
		//console.log( $(this).find('option:selected').val() );
		$.ajax('/lights', {
		
			'type': 'POST',
			'data': {
				'light': $(this).attr('id'),
				'mode': $(this).find('option:selected').val()
			},
			success: function(r) {
				//console.log('success');
				//console.log(r);
			},
			error: function() {
				//console.log('error');
			}
		
		});
		
	});
});
