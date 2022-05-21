
$.getScript(
	'https://maps.googleapis.com/maps/api/js?key=' +
		google_api_key +
		'&libraries=places&language=en'
).done(function (script, textStatus) {
	google.maps.event.addDomListener(window, 'load', initAutoComplete);
});

let autocomplete;

function initAutoComplete() {
	autocomplete = new google.maps.places.Autocomplete(
		document.getElementById('id-google-address'),
		{
			types: ['address'],
			componentRestrictions: { country: ['il'] },
			fields: ['place_id', 'geometry', 'name'],
		}
	);
	autocomplete.addListener('place_changed', onPlaceChanged);
}

const onPlaceChanged = () => {
	let place = autocomplete.getPlace();
	let geocoder = new google.maps.Geocoder();
	let address = document.getElementById('id-google-address').value;
    console.log(address);
	geocoder.geocode({ address: address }, function (results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			let latitude = results[0].geometry.location.lat();
			let longitude = results[0].geometry.location.lng();

			$('#id_longitude').val(longitude);
			$('#id_latitude').val(latitude);
		}
	});

	if (!place.geometry) {
		document.getElementById('id-google-address').placeholder =
			'Begin typing address';
	} else {
		$('#id_address').val(address);
    }

		//find all hidden inputs & ignore csrf token
		var x = $('input:hidden');
		for (let i = 0; i < x.length; i++) {
			if (x[i].name != 'csrfmiddlewaretoken') x[i].type = 'text';
			x.eq(x).attr('class', 'hidden-el');
		}

		//fade in the completed form
		$('.hidden-el').fadeIn();

	// 	$('#profile-btn').removeAttr('disabled');
	// }
}
