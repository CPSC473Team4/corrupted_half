(function() {
    $(function() {

        $('.business-detail .business-name').bind('mouseenter mouseleave', function() {
            $('.business-detail .bookmark').toggleClass('animated swing');
        });

        $('.btn-action').click(function() {
          window.location = $(this).attr('data-href');
        });


        if ($('#map-canvas').length)
        {
            // Define the address we want to map.
            var address = $('#map-canvas').attr('data-address');

            // Create a new Geocoder
            var geocoder = new google.maps.Geocoder();

            // Locate the address using the Geocoder.
            geocoder.geocode( { "address": address }, function(results, status) {

              // If the Geocoding was successful
              if (status == google.maps.GeocoderStatus.OK) {

                // Create a Google Map at the latitude/longitude returned by the Geocoder.
                var myOptions = {
                  zoom: 16,
                  center: results[0].geometry.location,
                  mapTypeId: google.maps.MapTypeId.ROADMAP
                };
                var map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);

                // Add a marker at the address.
                var marker = new google.maps.Marker({
                  map: map,
                  position: results[0].geometry.location
                });

              } else {
                try {
                  console.error("Geocode was not successful for the following reason: " + status);
                } catch(e) {}
              }
            });
        }
    });
})();