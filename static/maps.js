let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: 40.7128, lng: 74.0060 },
    zoom: 8,
  });
}

initMap();