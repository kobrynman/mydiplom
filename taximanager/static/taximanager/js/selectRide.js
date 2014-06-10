var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;




// функція прокладає маршрут
function calcRoute() {

  var pickupAddress = /** @type {HTMLInputElement} */(
      document.getElementById('start_address')).value;

  var dropOffAddress = /** @type {HTMLInputElement} */(
      document.getElementById('end_address')).value;

  var request = {
      origin: pickupAddress,
      destination: dropOffAddress,
      //waypoints - проміжні точки
      region: 'UA',
      // Note that Javascript allows us to access the constant
      // using square brackets and a string value as its
      // "property."
      travelMode: google.maps.TravelMode.DRIVING


  };
  directionsService.route(request, function(response, status) {

    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);

    }
  });
}



// ініціалізація карти
function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var mapOptions = {
    center: new google.maps.LatLng(49.839683, 24.029717),
    zoom: 13
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
  directionsDisplay.setMap(map);

  calcRoute();
}



google.maps.event.addDomListener(window, 'load', initialize);
