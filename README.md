# kartograf

This is a very basic web frontend for routing in New York City.  It is not a production application and is intended solely for demonstrating predictive models involving transportation.

## Getting started

First, install [poetry](https://python-poetry.org) if necessary.  (On a Mac, use `homebrew`; on Linux, use your distribution's package manager or `pipx`.)

Then you can install the Python dependencies for kartograf:

`poetry install`

Next up, you can build a docker image for the routing service:

`(cd nyc-routing ; docker build -t nyc-routing .)`

Finally, you can run the routing service:

`docker run --rm -t -p 5000:5000 nyc-routing`

and the application:

`poetry run python -m flask run --port 8000`

## Adapting the application

### Use a local geolocation service

This application currently uses the public nominatim endpoint for geolocation, which is not suitable for heavy use.  You can install your own [nominatim service in a Docker container](https://github.com/mediagis/nominatim-docker) and then change the `endpoint` argument to `resolve_address` in [`app.py`](./app.py) to refer to a locally-running service.

### Add extra logic to map lookup

To integrate a predictive model into the app, add a call to the model itself (or a prediction API) from within the `index` function.  You'll also need to pass any results that you want to render as keyword arguments to the `render_template` call in `index` and specify where you want to render them in [`map.html`](./templates/map.html).  