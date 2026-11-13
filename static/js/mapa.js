const map = L.map('map', {
  zoomControl: true,
  scrollWheelZoom: true,
}).setView([-32.8443, -68.8008], 12.6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors',
}).addTo(map);

const markersLayer = L.layerGroup().addTo(map);
const searchInput = document.getElementById('searchPlaza');
const stateFilter = document.getElementById('estadoFiltro');
const plazaList = document.getElementById('plazaList');
const plazaCount = document.getElementById('plazaCount');

function renderList(filteredPlazas) {
  plazaList.innerHTML = '';

  if (!filteredPlazas.length) {
    plazaList.innerHTML = '<div class="empty-list">No se encontraron plazas con los filtros actuales.</div>';
    plazaCount.textContent = '0';
    return;
  }

  plazaCount.textContent = String(filteredPlazas.length);

  filteredPlazas.forEach((plaza) => {
    const item = document.createElement('button');
    item.type = 'button';
    item.className = 'plaza-item';
    item.setAttribute('data-plaza-id', plaza.id);
    item.innerHTML = `
      <div class="plaza-item-top">
        <span class="status-badge status-${plaza.estado.toLowerCase().replace(/\s+/g, '-')}">${plaza.estado}</span>
      </div>
      <h3>${plaza.nombre}</h3>
      <p>${plaza.ubicacion}</p>
      <small>Ver detalles</small>
    `;

    item.addEventListener('click', () => {
      map.flyTo([plaza.latitud, plaza.longitud], 15, { duration: 1.2 });
      const marker = markersLayer.getLayers().find((layer) => Number(layer.options.plazaId) === Number(plaza.id));
      if (marker) {
        marker.openPopup();
      }
    });

    plazaList.appendChild(item);
  });
}

function renderMarkers(filteredPlazas) {
  markersLayer.clearLayers();

  filteredPlazas.forEach((plaza) => {
    const marker = L.marker([plaza.latitud, plaza.longitud], {
      plazaId: plaza.id,
    }).addTo(markersLayer);

    const popupHtml = `
      <div class="popup-card">
        <h3>${plaza.nombre}</h3>
        <p><strong>Ubicación:</strong> ${plaza.ubicacion}</p>
        <p>${plaza.descripcion}</p>
        <div class="popup-actions">
          <a href="/plaza/${plaza.id}" class="popup-link">Ver detalles</a>
          <a href="/plaza/${plaza.id}/formulario" class="popup-link alt">Realizar reclamo</a>
          <a href="/plaza/${plaza.id}/opiniones" class="popup-link alt">Ver opiniones</a>
        </div>
      </div>
    `;

    marker.bindPopup(popupHtml);
  });

  if (filteredPlazas.length) {
    const first = filteredPlazas[0];
    map.flyTo([first.latitud, first.longitud], 12.5, { duration: 1.2 });
  }
}

function applyFilters() {
  const text = (searchInput.value || '').trim().toLowerCase();
  const estado = stateFilter.value || 'Todas';

  const filtered = plazas.filter((plaza) => {
    const matchesText = !text || plaza.nombre.toLowerCase().includes(text) || plaza.ubicacion.toLowerCase().includes(text);
    const matchesEstado = estado === 'Todas' || plaza.estado === estado;
    return matchesText && matchesEstado;
  });

  renderMarkers(filtered);
  renderList(filtered);
}

searchInput.addEventListener('input', applyFilters);
stateFilter.addEventListener('change', applyFilters);

renderMarkers(plazas);
renderList(plazas);
