
$.getScript(
	'https://maps.googleapis.com/maps/api/js?key=' +
		google_api_key +
		'&libraries=places&language=en'
).done(function (script, textStatus) {
	google.maps.event.addDomListener(window, 'load', initAutoComplete);
});

let autocomplete;


const initAutoComplete = () => {
	autocomplete = new google.maps.places.Autocomplete(
		document.getElementById('id-google-address'),
		{
			types: ['address'],
			componentRestrictions: { country: ['il'] },
			fields: ['place_id', 'geometry', 'name'],
		}
	);
	autocomplete.addListener('place_changed', onPlaceChanged)
}

const initMap = (point) => {

	var latitude = point ? point.latitude : user.latitude;
	var longitude = point ? point.longitude : user.longitude;

	var user_location = { lat: latitude, lng: longitude };

	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 5,
		center: user_location,
	});

	const marker = new google.maps.Marker({
		position: user_location,
		map: map,
	});
};

const onPlaceChanged = () => {
	window.initMap = initMap;
	let place = autocomplete.getPlace();
	let geocoder = new google.maps.Geocoder();
	let address = document.getElementById('id-google-address').value;
	let latitude;
	let longitude;
	geocoder.geocode({ address: address }, function (results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			latitude = results[0].geometry.location.lat();
			longitude = results[0].geometry.location.lng();
			$('#id_longitude').val(longitude);
			$('#id_latitude').val(latitude);
			window.initMap({latitude, longitude})
		}
	});

	if (!place.geometry) {
		document.getElementById('id-google-address').placeholder =
			'Begin typing address';
	} else {
		$('#id_address').val(address);
		//find all hidden inputs & ignore csrf token
		var x = $('input:hidden');
		for (let i = 0; i < x.length; i++) {
			if (x[i].name != 'csrfmiddlewaretoken') x[i].type = 'text';
			x.eq(x).attr('class', 'hidden-el');
		}

		//fade in the completed form
		$('.hidden-el').fadeIn();
		document.getElementById('par-address').innerHTML  = ''
		document.getElementById('address-btn').innerHTML  = 'Update'
	// 	$('#profile-btn').removeAttr('disabled');
	// }
	}
}






