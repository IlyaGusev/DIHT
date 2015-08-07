$(function() {
	/* ��������� ������� */
	$('#event-pencil').click(function() {
		$('#event-noedit').removeClass('visible');
		$('#event-noedit').addClass('hidden');
		$('#event-selector').removeClass('hidden');
		$('#event-selector').addClass('visible');
		$('#event-selector').focus();
		
	})
	
	$('#event-selector').blur(function() {
		//AJAX �������� �� ������
		$('#event-noedit').removeClass('hidden');
		$('#event-noedit').addClass('visible');
		$('#event-selector').removeClass('visible');
		$('#event-selector').addClass('hidden');
	})
	
	/* ��������� �������� */
	
	$('#desc-pencil').click(function() {
		$('#desc').removeClass('visible');
		$('#desc').addClass('hidden');
		$('#desc-area').removeClass('hidden');
		$('#desc-area').addClass('visible');
		$('#desc-area').focus();
	})
	
	$('#desc-area').blur(function() {
		//AJAX �������� �� ������
		$('#desc').removeClass('hidden');
		$('#desc').addClass('visible');
		$('#desc-area').removeClass('visible');
		$('#desc-area').addClass('hidden');
	})
	
	/* ��������� ��������� �� */
	
	$('#est-hours-pencil').click(function() {
		
		$('#est-hours').removeClass('visible');
		$('#est-hours').addClass('hidden');
		$('#est-hours-edit').removeClass('hidden');
		$('#est-hours-edit').addClass('visible');
		$('#est-hours-field').focus();
	})
	
	$('#est-hours-field').blur(function() {
		//AJAX �������� �� ������
		$('#est-hours').removeClass('hidden');
		$('#est-hours').addClass('visible');
		$('#est-hours-edit').removeClass('visible');
		$('#est-hours-edit').addClass('hidden');
	})
	
	/* ��������� ������ */
	
	$('#datelimit-pencil').click(function() {
		
		$('#datelimit').removeClass('visible');
		$('#datelimit').addClass('hidden');
		$('#dateedit').removeClass('hidden');
		$('#dateedit').addClass('visible');
		$('#datepicker').focus();
		
		console.log(($("#datepicker").is(":focus")));
		console.log(($("#timepicker").is(":focus")));
		console.log(itemHasFocus("datepicker"));
		console.log(itemHasFocus("timepicker"));
		
	})
	
	$('#datepicker').blur(function() {
		//AJAX �������� �� ������
		setTimeout(function() {if (! ($("#timepicker").is(":focus"))) {
			$('#datelimit').removeClass('hidden');
			$('#datelimit').addClass('visible');
			$('#dateedit').removeClass('visible');
			$('#dateedit').addClass('hidden');
		}}, 0);
	})
	$('#timepicker').blur(function() {
		//AJAX �������� �� ������
		setTimeout(function() {if (! ($("#datepicker").is(":focus"))) {
			$('#datelimit').removeClass('hidden');
			$('#datelimit').addClass('visible');
			$('#dateedit').removeClass('visible');
			$('#dateedit').addClass('hidden');
		}}, 0);
	})
	
});