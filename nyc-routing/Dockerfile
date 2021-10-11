FROM osrm/osrm-backend

EXPOSE 5000/tcp

RUN mkdir /data
ADD https://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf /data/new-york-latest.osm.pbf

RUN osrm-extract -p /opt/car.lua /data/new-york-latest.osm.pbf
RUN osrm-partition /data/new-york-latest.osrm
RUN osrm-customize /data/new-york-latest.osrm

CMD ["osrm-routed", "--algorithm", "mld", "/data/new-york-latest.osrm"]