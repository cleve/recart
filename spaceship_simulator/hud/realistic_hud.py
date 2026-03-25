"""
Realistic HUD system for spaceship simulator.
Creates a multi-panel dashboard with circular radar and viewport.
Panels use Pillow-generated PNG textures for an SVG-quality cockpit look.
"""

import math
from panda3d.core import TextNode, CardMaker, TransparencyAttrib
from spaceship_simulator.hud.panel import TouchControlPanel

# Fraction of RADAR_RANGE actually displayed on screen.
# At RADAR_RANGE=50000 and MAX_VELOCITY=1000, fraction=0.10 shows 5000 units;
# one second at full thrust shifts blips ~20% of the radar radius — clearly visible.
RADAR_DISPLAY_FRACTION = 0.10


class RealisticHUD:
    """Manages a realistic multi-panel HUD display with textured panels."""

    # Radar geometry in aspect2d
    RADAR_X      = -1.40
    RADAR_Y      =  0.90
    RADAR_SIZE   =  0.55
    RADAR_CX     = -1.40 + 0.55 / 2   # = -1.125
    RADAR_CY     =  0.90 - 0.55 / 2   # = +0.625
    RADAR_RADIUS =  0.55 * 0.43        # ~0.2365 (matches ring fraction in image)

    MAX_BLIPS = 25

    def __init__(self, app, ship_state, universe):
        self.app      = app
        self.ship     = ship_state
        self.universe = universe

        self.text_nodes = {}
        self.blip_nodes = []
        self.visible_targets = []
        self.view_mode  = 0

        self._load_textures()
        self._build_panels()
        self._build_radar_blips()
        self.touch_control_panel = TouchControlPanel(app, ship_state)

    # ------------------------------------------------------------------ textures

    def _load_textures(self):
        from spaceship_simulator.hud.hud_textures import (
            create_radar_bg, create_status_panel_bg,
            create_comms_panel_bg, create_bottom_panel_bg,
            create_crosshair, create_blip_texture,
        )
        self.tex_radar        = create_radar_bg(512)
        self.tex_status       = create_status_panel_bg(256, 420)
        self.tex_comms        = create_comms_panel_bg(480, 160)
        self.tex_bottom       = create_bottom_panel_bg(512, 160)
        self.tex_xhair        = create_crosshair(256)
        self.tex_blip_planet  = create_blip_texture(60,  120, 255)
        self.tex_blip_station = create_blip_texture(255, 180,  40)
        self.tex_blip_anomaly = create_blip_texture(255,  50,  50)

    # ------------------------------------------------------------------ helpers

    def _make_card(self, name, left, right, bottom, top, texture, sort=0):
        cm = CardMaker(name)
        cm.set_frame(left, right, bottom, top)
        cm.set_uv_range((0, 0), (1, 1))
        node = self.app.aspect2d.attach_new_node(cm.generate())
        node.set_texture(texture)
        node.set_transparency(TransparencyAttrib.M_alpha)
        node.set_bin("fixed", sort)
        return node

    def _make_text(self, name, x, y, scale, color, text="", sort=10):
        tn = TextNode(name)
        tn.set_text(text)
        tn.set_text_color(*color, 1.0)
        np = self.app.aspect2d.attach_new_node(tn)
        np.set_scale(scale)
        np.set_pos(x, 0, y)
        np.set_bin("fixed", sort)
        return tn

    # ------------------------------------------------------------------ panels

    def _build_panels(self):
        from spaceship_simulator.config.constants import (
            HUD_COLOR_PRIMARY, HUD_COLOR_SECONDARY,
        )
        GREEN = HUD_COLOR_PRIMARY
        CYAN  = (0.0, 0.85, 1.0)

        # --- RADAR (top-left) -------------------------------------------
        rx, ry, rs = self.RADAR_X, self.RADAR_Y, self.RADAR_SIZE
        self._make_card("RadarCard", rx, rx+rs, ry-rs, ry, self.tex_radar, sort=1)
        self.text_nodes["radar_title"] = self._make_text(
            "RadarTitle", rx+0.04, ry-0.04, 0.036, GREEN, "RADAR", sort=12)
        self.text_nodes["radar_data"] = self._make_text(
            "RadarData", rx+0.03, ry-rs+0.12, 0.030, GREEN,
            "Entities: 0\nClosest: ---\nDist: ---", sort=12)

        # --- FORWARD STATUS BAR (centre-top) ----------------------------
        self._make_card("ViewBar", -0.78, 0.78, 0.76, 0.90, self.tex_comms, sort=1)
        self.text_nodes["view_title"] = self._make_text(
            "ViewTitle", -0.74, 0.86, 0.033, CYAN, "FORWARD VIEW", sort=12)
        self.text_nodes["view_status"] = self._make_text(
            "ViewStatus", -0.74, 0.78, 0.030, CYAN,
            "View: FirstPerson | Heading: 0 | Pitch: 0 | Roll: 0", sort=12)

        # --- STATUS PANEL (top-right) -----------------------------------
        sx, sy, sw, sh = 0.88, 0.90, 0.52, 0.70
        self._make_card("StatusCard", sx, sx+sw, sy-sh, sy, self.tex_status, sort=1)
        self.text_nodes["status_title"] = self._make_text(
            "StatusTitle", sx+0.04, sy-0.04, 0.036, GREEN, "SYSTEMS", sort=12)
        self.text_nodes["status_data"] = self._make_text(
            "StatusData", sx+0.04, sy-0.14, 0.031, GREEN,
            "VEL: 0.0 u/s\nENR: 100%  SHD: 80%\n"
            "OXY: 100%  HUL: 100%\nCRW: 100%\nX:0  Y:0  Z:0", sort=12)

        # --- CROSSHAIR overlay ------------------------------------------
        xs = 0.22
        self._make_card("Crosshair", -xs, xs, -xs, xs, self.tex_xhair, sort=5)

        # --- COMMS PANEL (bottom-left) ----------------------------------
        cx, cy_pos, cw, ch = -1.40, -0.56, 1.05, 0.44
        self._make_card("CommsCard", cx, cx+cw, cy_pos-ch, cy_pos, self.tex_comms, sort=1)
        self.text_nodes["comms_title"] = self._make_text(
            "CommsTitle", cx+0.03, cy_pos-0.03, 0.033, CYAN, "COMMUNICATIONS", sort=12)
        self.text_nodes["comms_msg"] = self._make_text(
            "CommsMsg", cx+0.03, cy_pos-0.13, 0.026, CYAN,
            "[System] Ready for launch\n[Radar] Scanning...", sort=12)

        # --- CONTROLS PANEL (bottom-right) ------------------------------
        hx, hy, hw, hh = 0.20, -0.62, 1.20, 0.28
        self._make_card("HelpCard", hx, hx+hw, hy-hh, hy, self.tex_bottom, sort=1)
        self.text_nodes["help_title"] = self._make_text(
            "HelpTitle", hx+0.03, hy-0.03, 0.033, CYAN, "CONTROLS & NAV", sort=12)
        self.text_nodes["help_text"] = self._make_text(
            "HelpText", hx+0.03, hy-0.12, 0.026, CYAN,
            "FLIGHT: W/S Thrust  A/D Yaw  Q/E Pitch  Z/X Roll  Space/Ctrl Strafe\n"
            "VIEW: F1-F4 Cameras  H:Help  P:Pause  ESC:Exit", sort=12)

    # ------------------------------------------------------------------ blips

    def _build_radar_blips(self):
        bs = 0.016
        for _ in range(self.MAX_BLIPS):
            cm = CardMaker("Blip")
            cm.set_frame(-bs, bs, -bs, bs)
            cm.set_uv_range((0, 0), (1, 1))
            np = self.app.aspect2d.attach_new_node(cm.generate())
            np.set_texture(self.tex_blip_planet)
            np.set_transparency(TransparencyAttrib.M_alpha)
            np.set_bin("fixed", 8)
            np.hide()
            self.blip_nodes.append(np)

    def _update_blips(self, ship, universe):
        from spaceship_simulator.config.constants import RADAR_RANGE

        # Use a fraction of RADAR_RANGE so blips move visibly as the ship flies
        display_range = RADAR_RANGE * RADAR_DISPLAY_FRACTION
        nearby = universe.get_nearby_entities(ship.position, display_range)
        scale  = self.RADAR_RADIUS / display_range

        for bn in self.blip_nodes:
            bn.hide()

        self.visible_targets = []

        # Rotate blips into ship-heading frame so "forward" is always at top.
        # Ship axes: forward = (-sin(h), 0, -cos(h))  right = (cos(h), 0, -sin(h))
        # (from _update_axes in ship.py: forward.x=sin(h), forward.z=-cos(h) at pitch=0)
        h     = math.radians(ship.heading)
        cos_h = math.cos(h)
        sin_h = math.sin(h)

        for i, entity in enumerate(nearby[:self.MAX_BLIPS]):
            rel = entity.position - ship.position

            # Project world-space offset onto ship's right and forward axes.
            # Ship right  = ( cos(h), 0,  sin(h))
            # Ship forward = ( sin(h), 0, -cos(h))  [forward.z = -cos(h)]
            local_right   =  rel.x * cos_h + rel.z * sin_h
            local_forward =  rel.x * sin_h - rel.z * cos_h  # positive = ahead of ship

            bx = self.RADAR_CX + local_right   * scale
            bz = self.RADAR_CY + local_forward * scale

            # Clamp to radar circle so no blip ever renders outside the ring.
            dist_from_center = math.sqrt((bx - self.RADAR_CX)**2 + (bz - self.RADAR_CY)**2)
            if dist_from_center > self.RADAR_RADIUS:
                factor = self.RADAR_RADIUS * 0.95 / dist_from_center
                bx = self.RADAR_CX + (bx - self.RADAR_CX) * factor
                bz = self.RADAR_CY + (bz - self.RADAR_CY) * factor

            etype = getattr(entity, "type", "planet").lower()
            if "station" in etype:
                tex = self.tex_blip_station
            elif "anomaly" in etype:
                tex = self.tex_blip_anomaly
            else:
                tex = self.tex_blip_planet

            bn = self.blip_nodes[i]
            bn.set_texture(tex)
            bn.set_pos(bx, 0, bz)
            bn.show()

            self.visible_targets.append({
                "entity": entity,
                "x": bx,
                "z": bz,
            })

    def pick_radar_target(self, mouse_x, mouse_z, radius):
        """Return nearest visible radar target within click radius."""
        # Ignore clicks outside radar circle.
        radar_dist = math.sqrt((mouse_x - self.RADAR_CX) ** 2 + (mouse_z - self.RADAR_CY) ** 2)
        if radar_dist > self.RADAR_RADIUS:
            return None

        best = None
        best_dist = radius

        for target in self.visible_targets:
            dx = target["x"] - mouse_x
            dz = target["z"] - mouse_z
            d = math.sqrt(dx * dx + dz * dz)
            if d <= best_dist:
                best_dist = d
                best = target

        return best

    # ------------------------------------------------------------------ update

    def update(self, dt, ship, universe, view_mode):
        from spaceship_simulator.config.constants import RADAR_RANGE

        del dt

        self.text_nodes["status_data"].set_text(
            f"VEL: {ship.velocity.length():.1f} u/s\n"
            f"ENR: {ship.energy:.0f}%  SHD: {ship.shield:.0f}%\n"
            f"OXY: {ship.oxygen:.0f}%  HUL: {ship.hull:.0f}%\n"
            f"CRW: {ship.crew_health:.0f}%\n"
            f"X:{ship.position.x:.0f}  Y:{ship.position.y:.0f}  Z:{ship.position.z:.0f}"
        )

        modes     = ["FirstPerson", "Top-Down", "Rear", "Side"]
        view_name = modes[view_mode] if 0 <= view_mode < len(modes) else "---"
        self.text_nodes["view_status"].set_text(
            f"View: {view_name}  |  "
            f"Heading: {ship.heading:.0f}  "
            f"Pitch: {ship.pitch:.0f}  "
            f"Roll: {ship.roll:.0f}"
        )

        nearby = universe.get_nearby_entities(ship.position, RADAR_RANGE)
        if nearby:
            closest = nearby[0]
            dist = (closest.position - ship.position).length()
            self.text_nodes["radar_data"].set_text(
                f"Entities: {len(nearby)}\n"
                f"Closest: {closest.name[:14]}\n"
                f"Dist: {dist/1000:.1f} ku"
            )
        else:
            self.text_nodes["radar_data"].set_text("Entities: 0\nClosest: ---\nDist: ---")

        msgs = getattr(self.app, "comms_messages", [])
        if msgs:
            self.text_nodes["comms_msg"].set_text(
                "\n".join(m[:80] for m in msgs[-5:])
            )

        self._update_blips(ship, universe)
        self.touch_control_panel.update()

    def set_view_mode(self, mode):
        self.view_mode = mode

    def cleanup(self):
        self.touch_control_panel.cleanup()
