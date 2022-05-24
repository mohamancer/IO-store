$.getScript(
	'https://maps.googleapis.com/maps/api/js?key=' +
		google_api_key 
).done(function (script, textStatus) {
	google.maps.event.addDomListener(window, 'load', initMap);
});

function pinitMa() {
    var user_address = user.address
    if (user_address) {

        const user_location = { lat: user.latitude, lng: user.longitude };
        var map = new google.maps.Map(document.getElementById('map'), {
					zoom: 8,
					center: user_location,
				});
        
        const marker = new google.maps.Marker({
					position: user_location,
					map: map,
				});
    }
}



// const waypts = [
// 	{ location: { lat: lat_c, lng: long_c }, stopover: true },
// 	{ location: { lat: lat_d, lng: long_d }, stopover: true },
// ];

// function calculateAndDisplayRoute(directionsService, directionsDisplay) {
// 	directionsService.route(
// 		{
// 			origin: origin,
// 			destination: destination,
// 			waypoints: waypts,
// 			optimizeWaypoints: true,
// 			travelMode: google.maps.TravelMode.DRIVING,
// 		},
// 		function (response, status) {
// 			if (status === 'OK') {
// 				directionsDisplay.setDirections(response);
// 			} else {
// 				alert('Directions request failed due to ' + status);
// 				window.location.assign('/route');
// 			}
// 		}
// 	);
// }
