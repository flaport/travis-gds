""" example layout from gdsfactory

source: https://github.com/gdsfactory/gdsfactory/blob/master/notebooks/04_routing.ipynb

"""

# imports
import pp
import numpy as np

from pp.routing.connect_component import add_io_optical


# component definition
@pp.autoname
def big_device(w=400.0, h=400.0, N=16, port_pitch=15.0, layer=pp.LAYER.WG, wg_width=0.5):
    """ big device with N ports on each side """
    component = pp.Component()
    p0 = np.array((0, 0))
    dx = w / 2
    dy = h / 2

    points = [[dx, dy], [dx, -dy], [-dx, -dy], [-dx, dy]]
    component.add_polygon(points, layer=layer)
    port_params = {"layer": layer, "width": wg_width}
    for i in range(N):
        port = pp.Port(
            name="W{}".format(i),
            midpoint=p0 + (-dx, (i - N / 2) * port_pitch),
            orientation=180,
            **port_params
        )
        component.add_port(port)

    for i in range(N):
        port = pp.Port(
            name="E{}".format(i),
            midpoint=p0 + (dx, (i - N / 2) * port_pitch),
            orientation=0,
            **port_params
        )
        component.add_port(port)

    for i in range(N):
        port = pp.Port(
            name="N{}".format(i),
            midpoint=p0 + ((i - N / 2) * port_pitch, dy),
            orientation=90,
            **port_params
        )
        component.add_port(port)

    for i in range(N):
        port = pp.Port(
            name="S{}".format(i),
            midpoint=p0 + ((i - N / 2) * port_pitch, -dy),
            orientation=-90,
            **port_params
        )
        component.add_port(port)
    return component

# create design
if __name__ == "__main__":
    bend_radius = 5.0
    c = big_device(N=10)
    c = add_io_optical(c, bend_radius=bend_radius, fanout_length=50.0)
    pp.write_component(c, "design.gds")

