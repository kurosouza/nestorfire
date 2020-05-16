
import { Map, TileLayer } from 'react-leaflet-universal';
import React from 'react';

import L from 'leaflet';

export default ({ ref }) => {

    return (
        <div style={{ height: 400 + 'px', width: 400 + 'px' }}>
            <Map center={[4.8241, 7.0336]} zoom={13} leafletRef={ref} style={{ height: 400 + 'px', width: 400 + 'px' }}>
                <TileLayer attribution="" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            </Map>
        </div>
    );
};