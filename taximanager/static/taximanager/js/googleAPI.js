var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;

// функція прокладає маршрут
function calcRoute(pickupAddress, dropOffAddress) {

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
    }else {
      alert('12312322: ' + status);
     }
  });
}


//функції для обчислення відстані
//origin1 - координати відправлення
//destinationA - координати прибуття
function calculateDistances(origin1, destinationA) {
  var service = new google.maps.DistanceMatrixService();
  service.getDistanceMatrix(
    {
      origins: [origin1],
      destinations: [destinationA],
      travelMode: google.maps.TravelMode.DRIVING,
      unitSystem: google.maps.UnitSystem.METRIC,
      avoidHighways: false,
      avoidTolls: false
    }, callback);
}


// для функції calculateDistances
function callback(response, status) {
  if (status != google.maps.DistanceMatrixStatus.OK) {
    alert('Error was: ' + status);
  } else {
    var origins = response.originAddresses;
    var destinations = response.destinationAddresses;
    var outputETA = document.getElementById('id_ETA');
    var outputDistance = document.getElementById('id_calculatedDistance');

    for (var i = 0; i < origins.length; i++) {
      var results = response.rows[i].elements;
      for (var j = 0; j < results.length; j++) {
            outputETA.value= results[j].duration.text
            outputDistance.value = results[j].distance.value/1000
      }
    }
  }
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


  var start = /** @type {HTMLInputElement} */(
      document.getElementById('id_pickupAddress'));

  var end = /** @type {HTMLInputElement} */(
      document.getElementById('id_dropOffAddress'));


  var autocompleteStart = new google.maps.places.Autocomplete(
      start,
      {
        componentRestrictions: { 'country': 'ua' }
      });
  var autocompleteEnd = new google.maps.places.Autocomplete(
      end,
      {
        componentRestrictions: { 'country': 'ua' }
      });



// подія прослуховування поля вводу точки відправлення
  google.maps.event.addListener(autocompleteStart, 'place_changed', function() {




     var placeStart = autocompleteStart.getPlace();
     var placeEnd = autocompleteEnd.getPlace();


    pickupAddress= placeStart.geometry.location;
    dropOffAddress = placeEnd.geometry.location;

    if (!placeStart.geometry||!placeEnd.geometry) {
      return;
    }
    document.getElementById('id_pickupLatitude').value=pickupAddress.lat()
    document.getElementById('id_pickupLongitude').value=pickupAddress.lng()
    document.getElementById('id_dropOffLatitude').value=dropOffAddress.lat()
    document.getElementById('id_dropOffLongitude').value=dropOffAddress.lng()

    calculateDistances(pickupAddress,dropOffAddress);
    calcRoute(pickupAddress, dropOffAddress );

  });

// подія прослуховування поля вводу точки прибуття
  google.maps.event.addListener(autocompleteEnd, 'place_changed', function() {
    var placeStart = autocompleteStart.getPlace();
    var placeEnd = autocompleteEnd.getPlace();
    pickupAddress= placeStart.geometry.location;
    dropOffAddress = placeEnd.geometry.location;

    if (!placeStart.geometry||!placeEnd.geometry) {
      return;
    }
    document.getElementById('id_dropOffLatitude').value=dropOffAddress.lat()
    document.getElementById('id_dropOffLongitude').value=dropOffAddress.lng()
    document.getElementById('id_pickupLatitude').value=pickupAddress.lat()
    document.getElementById('id_pickupLongitude').value=pickupAddress.lng()
    calculateDistances(pickupAddress,dropOffAddress);
    calcRoute(pickupAddress, dropOffAddress );

  });
}

google.maps.event.addDomListener(window, 'load', initialize);