"""
Star field rendered as coloured GL points that follow the camera,
giving the illusion of an infinite sky full of stars.
"""

import math
import random

from panda3d.core import (
    AntialiasAttrib,
    Geom,
    GeomNode,
    GeomPoints,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    RenderModeAttrib,
)

# ── Tunables ────────────────────────────────────────────────────────────────
_NUM_STARS   = 3000    # total star count
_SKY_RADIUS  = 500.0   # units — large sphere around the camera; moves with it
_POINT_SIZE  = 2.5     # pixel diameter of each star point
# ────────────────────────────────────────────────────────────────────────────


def _build_star_geom(seed: int = 1337) -> GeomNode:
    """Generate a GeomNode containing randomly coloured point-stars."""
    fmt   = GeomVertexFormat.get_v3c4()
    vdata = GeomVertexData("stars", fmt, Geom.UHStatic)
    vdata.set_num_rows(_NUM_STARS)

    v_wr = GeomVertexWriter(vdata, "vertex")
    c_wr = GeomVertexWriter(vdata, "color")
    prim = GeomPoints(Geom.UHStatic)
    rng  = random.Random(seed)

    for i in range(_NUM_STARS):
        # Uniformly distributed point on a sphere (trig method)
        theta = rng.uniform(0.0, 2.0 * math.pi)
        phi   = math.acos(rng.uniform(-1.0, 1.0))
        r     = _SKY_RADIUS
        v_wr.add_data3f(
            r * math.sin(phi) * math.cos(theta),
            r * math.sin(phi) * math.sin(theta),
            r * math.cos(phi),
        )

        # Brightness + subtle spectral tint (hot blue → sun-like → cool orange → white)
        brightness = rng.uniform(0.35, 1.0)
        tint = rng.random()
        if tint < 0.25:                                           # blue-white (hot)
            c_wr.add_data4f(brightness * 0.82, brightness * 0.88, brightness,        1.0)
        elif tint < 0.45:                                         # yellow-white (sun-like)
            c_wr.add_data4f(brightness,        brightness * 0.93, brightness * 0.62, 1.0)
        elif tint < 0.55:                                         # orange-red (cool giant)
            c_wr.add_data4f(brightness,        brightness * 0.52, brightness * 0.30, 1.0)
        else:                                                     # pure white
            c_wr.add_data4f(brightness,        brightness,        brightness,        1.0)

        prim.add_vertex(i)

    prim.close_primitive()
    geom = Geom(vdata)
    geom.add_primitive(prim)
    node = GeomNode("starfield")
    node.add_geom(geom)
    return node


class StarField:
    """
    An infinite-looking star field.

    Stars are rendered as GL points on a large sphere that follows the
    camera every frame, so they always fill the background regardless of
    how far the ship has travelled.
    """

    def __init__(self, app):
        geom_node = _build_star_geom()
        self._np  = app.render.attach_new_node(geom_node)

        # Render behind all scene geometry — no depth interaction
        self._np.set_bin("background", 0)
        self._np.set_depth_write(False)
        self._np.set_depth_test(False)
        self._np.set_light_off()            # stars emit their own light

        # Round anti-aliased points for a realistic look
        self._np.set_antialias(AntialiasAttrib.MPoint)
        self._np.set_attrib(RenderModeAttrib.make(RenderModeAttrib.MPoint, _POINT_SIZE))

    def update(self, camera_pos):
        """Call once per frame — re-centres the sphere on the camera."""
        self._np.set_pos(camera_pos)
