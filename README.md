# HTMX demo

A demo to show how a HTMX version of an administration app might look, to get
a feel for feasability of using HTMX for such a purpose and to have a point of
comparison for other solutions.

## Running the app in dev mode

If you have a `python3` interpreter in your `PATH`, simply run:

```
make local
```

and it will provision a virtual environment, install the dependencies, and
run the development server.

## Dependencies

You need to have a python 3 interpreter installed.

The Makefile defaults to running `python3` as the interpreter to create the
virtual environment, but this can be overridden, for example:

```
make local PY=~/local/bin/python3.15
```

The project depends on `jinja2` and `fastapi`.
