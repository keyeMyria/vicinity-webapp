var properties = {
    "data": [
        {
            "id": 1,
            "title": "Alki Beach Bathhouse",
            "price": 60,
            "listing_for": "Rent",
            'author': 'Occupancy 110',
            'date': '',
            "is_featured": true,
            "latitude": 47.5796251,
            "longitude": -122.4095955,
            "address": "2701 Alki Ave SW, Seattle WA",
            "area": 98116,
            "room": 4,
            "bathroom": 3,
            "balcony": 3,
            "lounge": 1,
            "garage": 1,
            "image": "img/properties/properties-1.jpg",
            "type_icon": "img/group.png",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor Lorem ipsum dolor sit amet, consectetur adipisicing"
        },
        {
            "id": 2,
            "title": "Alki Kitchen",
            "price": 510,
            "listing_for": "Rent",
            'author': 'Occupancy 110',
            'date': '',
            "is_featured": false,
            "latitude": 47.5728612,
            "longitude": -122.3743986,
            "address": "5817 SW Lander St., Seattle WA",
            "area": 98116,
            "room": 4,
            "bathroom": 3,
            "balcony": 3,
            "lounge": 1,
            "garage": 1,
            "image": "img/properties/properties-2.jpg",
            "type_icon": "img/group.png",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor Lorem ipsum dolor sit amet, consectetur adipisicing"
        },
        {
            "id": 3,
            "title": "Alki Playground Soccer Field",
            "price": 25,
            "listing_for": "Rent",
            'author': 'Occupancy 10',
            'date': '',
            "is_featured": true,
            "latitude": 47.65605619999999,
            "longitude": -122.3491132,
            "address": "4020 Fremont Ave. N, Seattle WA",
            "area": 98103,
            "room": 4,
            "bathroom": 3,
            "balcony": 3,
            "lounge": 1,
            "garage": 1,
            "image": "img/properties/properties-3.jpg",
            "type_icon": "img/group.png",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor Lorem ipsum dolor sit amet, consectetur adipisicing"
        },
        {
            "id": 4,
            "title": "Auburn Meeting Room #2",
            "price": 260,
            "listing_for": "Sale",
            'author': 'Occupancy 200',
            'date': '',
            "is_featured": true,
            "latitude": 47.3610494,
            "longitude": -122.3081823,
            "address": "26809 Pacific Highway South, Seattle WA",
            "area": 98198,
            "room": 4,
            "bathroom": 3,
            "balcony": 3,
            "lounge": 1,
            "garage": 1,
            "image": "img/properties/properties-5.jpg",
            "type_icon": "img/group.png",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor Lorem ipsum dolor sit amet, consectetur adipisicing"
        },
        {
            "id": 5,
            "title": "Ballard Gym",
            "price": 250,
            "listing_for": "Rent",
            'author': 'Jhon Doe',
            'date': '5 days ago',
            "is_featured": false,
            "latitude": 51.513915,
            "longitude": -122.3743152,
            "address": "2644 NW 60th St., Seattle WA",
            "area": 98107,
            "room": 4,
            "bathroom": 3,
            "balcony": 3,
            "lounge": 1,
            "garage": 1,
            "image": "img/properties/properties-5.jpg",
            "type_icon": "img/group.png",
            "description": "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor Lorem ipsum dolor sit amet, consectetur adipisicing"
        }

    ]
};

function drawInfoWindow(property) {
    var image = 'img/group.png';
    if (property.image) {
        image = property.image
    }

    var title = 'N/A';
    if (property.title) {
        title = property.title
    }

    var address = '';
    if (property.address) {
        address = property.address
    }

    var description = 'lorem ipsum dolor sit amet, cfeugiat congue qmper lorem ipsum dolor sit amet';
    if (property.description) {
        description = property.description
    }

    var area = 1000;
    if (property.area) {
        area = property.area
    }

    var Beds = 5;
    if (property.bedroom) {
        Beds = property.bedroom
    }

    var bathroom = 5;
    if (property.bathroom) {
        bathroom = property.bathroom
    }

    var garage = 1;
    if (property.garage) {
        garage = property.garage
    }

    var price = 253.33;
    if (property.price) {
        price = property.price
    }

    var ibContent = '';
    ibContent =
        "<div class='map-properties'>" +
        "<div class='map-img'>" +
        "<img src='" + image + "'/>" +
        "</div>" +
        "<div class='map-content'>" +
        "<div class='map-content-top'><h4><a href='properties-details.html'>" + title + "</a></h4>" +
        "<p class='address'> <i class='fa fa-map-marker'></i>" + address + "</p></div>" +
        "<p class='description'>" + description + "</p>" +
        "<div class='map-properties-fetures'> " +
        "<span><i class='flaticon-square-layouting-with-black-square-in-east-area'></i>  " + area + " sqft<sup>2</sup></span> " +
        "<span><i class='flaticon-bed'></i>  " + Beds + " Bed</span> " +
        "<span><i class='flaticon-holidays'></i>  " + bathroom + " Bath</span> " +
        "<span><i class='flaticon-vehicle'></i>    " + garage + " Garages</span> " +
        "</div>" +
        "<div class='map-properties-btns'><a href='properties-details.html' class='border-button-sm border-button-theme' style='margin-right:5px;'>$" + price + "</a><a href='properties-details.html' class='button-sm button-theme'>Details</a></div>" +
        "</div>";
    return ibContent;
}

function insertPropertyToArray(property, layout) {
    var image = 'img/group.png';
    if (property.image) {
        image = property.image
    }

    var title = 'N/A';
    if (property.title) {
        title = property.title
    }

    var listing_for = 'Sale';
    if (property.listing_for) {
        listing_for = property.listing_for
    }

    var address = '';
    if (property.address) {
        address = property.address
    }

    var description = 'lorem ipsum dolor sit amet, cfeugiat congue qmper lorem ipsum dolor sit amet';
    if (property.description) {
        description = property.description
    }

    var area = 1000;
    if (property.area) {
        area = property.area
    }

    var Beds = 5;
    if (property.bedroom) {
        Beds = property.bedroom
    }

    var bathroom = 5;
    if (property.bathroom) {
        bathroom = property.bathroom
    }

    var garage = 1;
    if (property.garage) {
        garage = property.garage
    }

    var balcony = 1;
    if (property.balcony) {
        balcony = property.balcony
    }

    var lounge = 1;
    if (property.lounge) {
        lounge = property.lounge
    }

    var price = 253.33;
    if (property.price) {
        price = property.price
    }

    var is_featured = '';
    if (property.is_featured) {
        is_featured = '<div class="property-tag button alt featured">Featured</div> ';
    }

    var date = '';
    if (property.date) {
        date = property.date;
    }

    var author = '';
    if (property.author) {
        author = property.author;
    }

    var element = '';

    if(layout == 'grid_layout'){
        element = '<div class="col-lg-6 col-md-6 col-sm-6 col-xs-12"><div class="property">' +
            '<!-- Property img --> ' +
            '<a href="properties-details.html" class="property-img">' +
            is_featured +
            '<div class="property-tag button sale">'+listing_for+'</div> ' +
            '<div class="property-price">$'+price+'</div> ' +
            '<img src="'+image+'" alt="properties-3" class="img-responsive"> ' +
            '</a>' +
            '<!-- Property content --> ' +
            '<div class="property-content"> ' +
            '<!-- title --> ' +
            '<h1 class="title">' +
            '<a href="properties-details.html">'+title+'</a> ' +
            '</h1> ' +
            '<!-- Property address --> ' +
            '<h3 class="property-address"> ' +
            '<a href="properties-details.html"> ' +
            '<i class="fa fa-map-marker"></i>'+address+' ' +
            '</a> ' +
            '</h3> ' +
            '<!-- Facilities List --> ' +
            '<ul class="facilities-list clearfix"> ' +
            '<li> ' +
            '<i class="flaticon-square-layouting-with-black-square-in-east-area"></i> ' +
            '<span>'+area+' sq ft</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-bed"></i> ' +
            '<span>'+Beds+' Beds</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-monitor"></i> ' +
            '<span>TV </span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-holidays"></i> ' +
            '<span> '+bathroom+' Baths</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-vehicle"></i> ' +
            '<span>'+garage+' Garage</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-building"></i> ' +
            '<span> '+balcony+' Balcony</span> ' +
            '</li> ' +
            '</ul> ' +
            '<!-- Property footer --> ' +
            '<div class="property-footer"> ' +
            '<a class="left"><i class="fa fa-user"></i>'+author+'</a> ' +
            '<span class="right"> ' +
            '<i class="fa fa-calendar"></i>' + date +
            '</span> ' +
            '</div>' +
            '</div>' +
            '</div>';
            '</div>';
    }
    else{
        element = '' +
            '<div class="property map-properties-list clearfix"> ' +
            '<div class="col-lg-5 col-md-5 col-sm-5 col-xs-12 col-pad"> ' +
            '<a href="properties-details.html" class="property-img height"> ' +
            is_featured +
            '<div class="property-tag button sale">'+listing_for+'</div> ' +
            '<div class="property-price">$'+price+'</div> ' +
            '<img src="'+image+'" alt="properties" class="img-responsive img-inside-map"> ' +
            '</a> ' +
            '</div> ' +
            '<div class="col-lg-7 col-md-7 col-sm-7 col-xs-12 property-content "> ' +
            '<!-- title --> ' +
            '<h1 class="title"> ' +
            '<a href="properties-details.html">'+title+'</a> </h1> ' +
            '<!-- Property address --> ' +
            '<h3 class="property-address"> ' +
            '<a href="properties-details.html"> ' +
            '<i class="fa fa-map-marker"></i>'+address+', ' +
            '</a>' +
            '</h3>' +
            '<!-- Facilities List --> ' +
            '<ul class="facilities-list clearfix"> ' +
            '<li> ' +
            '<i class="flaticon-square-layouting-with-black-square-in-east-area"></i> ' +
            '<span>'+area+' sq ft</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-bed"></i> ' +
            '<span>'+Beds+' Beds</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-monitor"></i> ' +
            '<span>TV </span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-holidays"></i>' +
            '<span> '+bathroom+' Baths</span> ' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-vehicle"></i>' +
            '<span>'+garage+' Garage</span>' +
            '</li> ' +
            '<li> ' +
            '<i class="flaticon-building"></i> ' +
            '<span> '+balcony+' Balcony</span> ' +
            '</li> ' +
            '</ul> ' +
            '<!-- Property footer --> ' +
            '<div class="property-footer"> ' +
            '<a class="left" href="#"><i class="fa fa-user"></i>'+author+'</a> ' +
            '<span class="right"> ' +
            '<i class="fa fa-calendar"></i>' + date +
            '</span> ' +
            '</div> ' +
            '</div> ' +
            '</div>';
    }
    return element;
}

function animatedMarkers(map, propertiesMarkers, properties, layout) {
    var bounds = map.getBounds();
    var propertiesArray = [];
    $.each(propertiesMarkers, function (key, value) {
        if (bounds.contains(propertiesMarkers[key].getLatLng())) {
            propertiesArray.push(insertPropertyToArray(properties.data[key], layout));
            setTimeout(function () {
                if (propertiesMarkers[key]._icon != null) {
                    propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable bounce-animation marker-loaded';
                }
            }, key * 50);
        }
        else {
            if (propertiesMarkers[key]._icon != null) {
                propertiesMarkers[key]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable';
            }
        }
    });
    $('.fetching-properties').html(propertiesArray);
}

function generateMap(latitude, longitude, mapProvider, layout) {

    var map = L.map('map', {
        center: [latitude, longitude],
        zoom: 12,
        scrollWheelZoom: true
    });

    L.tileLayer.provider(mapProvider).addTo(map);
    var markers = L.markerClusterGroup({
        showCoverageOnHover: false,
        zoomToBoundsOnClick: false
    });
    var propertiesMarkers = [];

    $.each(properties.data, function (index, property) {
        var icon = '<img src="img/group.png">';
        if (property.type_icon) {
            icon = '<img src="' + property.type_icon + '">';
        }
        var color = '';
        var markerContent =
            '<div class="map-marker ' + color + '">' +
            '<div class="icon">' +
            icon +
            '</div>' +
            '</div>';

        var _icon = L.divIcon({
            html: markerContent,
            iconSize: [36, 46],
            iconAnchor: [18, 32],
            popupAnchor: [130, -28],
            className: ''
        });

        var marker = L.marker(new L.LatLng(property.latitude, property.longitude), {
            title: property.title,
            icon: _icon
        });

        propertiesMarkers.push(marker);
        marker.bindPopup(drawInfoWindow(property));
        markers.addLayer(marker);
        marker.on('popupopen', function () {
            this._icon.className += ' marker-active';
        });
        marker.on('popupclose', function () {
            this._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        });
    });

    map.addLayer(markers);
    animatedMarkers(map, propertiesMarkers, properties, layout);
    map.on('moveend', function () {
        animatedMarkers(map, propertiesMarkers, properties, layout);
    });

    $('.fetching-properties .item').hover(
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded marker-active';
        },
        function () {
            propertiesMarkers[$(this).attr('id') - 1]._icon.className = 'leaflet-marker-icon leaflet-zoom-animated leaflet-clickable marker-loaded';
        }
    );

    $('.geolocation').on("click", function () {
        map.locate({setView: true})
    });
    $('#map').removeClass('fade-map');
}