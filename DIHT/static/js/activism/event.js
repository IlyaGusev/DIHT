$(function() {
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
	
});