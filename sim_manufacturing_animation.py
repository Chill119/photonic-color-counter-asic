#!/usr/bin/env python3
"""
Photonic Color-Counter ASIC — Manufacturing Process Animation
==============================================================
Generates a two-panel animated GIF:
  Left:  Wafer cross-section buildup (14 fabrication steps)
  Right: Top-down system assembly (8 integration steps)

Each frame adds one process step with a descriptive caption.

Requirements: numpy, matplotlib, pillow
Run:          python3 sim_manufacturing_animation.py
Output:       ~/sim_output/manufacturing_process.gif
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Arc, FancyArrowPatch
import matplotlib.animation as animation

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_output")
os.makedirs(OUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# COLOR PALETTE — material-coded
# ═══════════════════════════════════════════════════════════════════════════
C = {
    "si_sub":    "#8B8682",  # silicon substrate (gray)
    "box":       "#B0C4DE",  # buried oxide (light steel blue)
    "si_dev":    "#4169E1",  # Si device layer (royal blue)
    "si_slab":   "#6495ED",  # Si slab (cornflower blue)
    "ntype":     "#FF6347",  # n-type implant (tomato)
    "ptype":     "#32CD32",  # p-type implant (lime green)
    "ge":        "#DAA520",  # Germanium (goldenrod)
    "sin":       "#9370DB",  # Silicon nitride (medium purple)
    "sio2_clad": "#E0E8F0",  # SiO2 cladding (very light blue)
    "tin":       "#CD853F",  # TiN heater (peru)
    "metal":     "#FFD700",  # Metal interconnect (gold)
    "via":       "#C0C0C0",  # Vias (silver)
    "undercut":  "#FFFFFF",  # Undercut void (white)
    "comb_chip": "#FF8C00",  # Comb source chiplet (dark orange)
    "fiber":     "#00CED1",  # Optical fiber (dark turquoise)
    "pcb":       "#006400",  # PCB (dark green)
    "solder":    "#A9A9A9",  # Solder bumps
    "laser":     "#FF0000",  # Laser light
    "bg":        "#1a1a2e",  # Dark background
    "text":      "#e0e0e0",  # Light text
}

# ═══════════════════════════════════════════════════════════════════════════
# CROSS-SECTION FABRICATION STEPS
# ═══════════════════════════════════════════════════════════════════════════

def draw_cross_section(ax, step):
    """Draw the wafer cross-section at the given fabrication step (0-13)."""
    ax.clear()
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-1.5, 8.5)
    ax.set_facecolor(C["bg"])
    ax.set_aspect("equal")
    ax.axis("off")

    W = 11.0   # total width
    x0 = -0.5  # left edge

    # Helper to draw a layer
    def layer(y, h, color, label=None, alpha=1.0, pattern=None):
        r = mpatches.FancyBboxPatch(
            (x0, y), W, h, boxstyle="square,pad=0",
            facecolor=color, edgecolor="black", linewidth=0.5, alpha=alpha
        )
        ax.add_patch(r)
        if label:
            ax.text(x0 + W / 2, y + h / 2, label, ha="center", va="center",
                    fontsize=6, color="black", fontweight="bold")

    # Helper for a partial rectangle
    def block(x, y, w, h, color, label=None, ec="black"):
        r = mpatches.FancyBboxPatch(
            (x, y), w, h, boxstyle="square,pad=0",
            facecolor=color, edgecolor=ec, linewidth=0.5
        )
        ax.add_patch(r)
        if label:
            ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                    fontsize=5, color="black")

    # ── Step 0: Starting SOI wafer ──
    if step >= 0:
        layer(-1.5, 2.0, C["si_sub"], "Si Substrate")
        layer(0.5, 0.6, C["box"], "BOX (2 µm)")
        layer(1.1, 0.4, C["si_dev"], "Si Device (220 nm)")

    # ── Step 1: Waveguide patterning (full etch) ──
    if step >= 1:
        # Etch away parts of Si, leave waveguide ridges
        # Overlay white to "remove" Si, then draw remaining ridges
        for x in [0.5, 3.0, 5.5, 8.0]:
            block(x, 1.1, 1.2, 0.4, C["si_dev"])
        # Etch gaps
        for x in [1.7, 4.2, 6.7]:
            block(x, 1.1, 1.3, 0.4, C["box"], ec=C["box"])

    # ── Step 2: Partial etch for slab ──
    if step >= 2:
        for x in [0.3, 2.8, 5.3, 7.8]:
            block(x, 1.1, 0.2, 0.15, C["si_slab"])
            block(x + 1.4, 1.1, 0.2, 0.15, C["si_slab"])

    # ── Step 3: PN junction implantation ──
    if step >= 3:
        # N-type on left half of each ridge, P-type on right
        for x in [0.5, 3.0, 5.5, 8.0]:
            block(x, 1.1, 0.6, 0.4, C["ntype"], "n")
            block(x + 0.6, 1.1, 0.6, 0.4, C["ptype"], "p")

    # ── Step 4: Germanium epitaxy for photodetectors ──
    if step >= 4:
        block(8.0, 1.5, 1.2, 0.5, C["ge"], "Ge PD")

    # ── Step 5: SiN deposition and patterning ──
    if step >= 5:
        layer(1.8, 0.35, C["sin"], alpha=0.0)  # invisible base
        for x in [0.0, 2.5, 5.0]:
            block(x, 1.8, 1.5, 0.35, C["sin"], "SiN")

    # ── Step 6: SiO2 cladding deposition ──
    if step >= 6:
        layer(2.15, 1.0, C["sio2_clad"], "SiO₂ Cladding")

    # ── Step 7: Contact vias ──
    if step >= 7:
        for x in [1.0, 3.5, 6.0, 8.5]:
            block(x, 2.15, 0.15, 1.0, C["via"])
            block(x + 0.4, 2.15, 0.15, 1.0, C["via"])

    # ── Step 8: TiN heater layer ──
    if step >= 8:
        for x in [0.5, 3.0, 5.5]:
            block(x, 3.15, 1.2, 0.15, C["tin"], "TiN")

    # ── Step 9: Metal interconnect stack (M1-M9) ──
    if step >= 9:
        metal_y = 3.3
        for m_idx in range(5):  # show 5 representative metal layers
            y_m = metal_y + m_idx * 0.45
            # Metal lines
            for x in [0.3, 2.0, 3.8, 5.5, 7.2, 9.0]:
                block(x, y_m, 0.8, 0.1, C["metal"])
            # Oxide between
            if m_idx < 4:
                layer(y_m + 0.1, 0.35, C["sio2_clad"], alpha=0.5)
        ax.text(x0 + W / 2, 5.2, "BEOL M1–M9", ha="center", va="center",
                fontsize=6, color="black", fontweight="bold")

    # ── Step 10: CMOS transistors (simplified) ──
    if step >= 10:
        for x in [1.5, 3.3, 7.0, 9.0]:
            # Gate stack
            block(x, 5.55, 0.3, 0.25, "#FF4500", "FET")

    # ── Step 11: Thermal undercut ──
    if step >= 11:
        # White voids under the MRR regions
        for x in [0.2, 2.7, 5.2]:
            block(x, -0.5, 1.8, 1.0, C["undercut"], "void")
            # Re-draw BOX bridges at edges
            block(x - 0.1, 0.5, 0.15, 0.6, C["box"])
            block(x + 1.75, 0.5, 0.15, 0.6, C["box"])

    # ── Step 12: Sb2Se3 phase-change patches ──
    if step >= 12:
        for x in [0.8, 3.3, 5.8]:
            block(x, 1.55, 0.5, 0.12, "#8B0000", "PCM")

    # ── Step 13: Passivation + pad opening ──
    if step >= 13:
        layer(5.8, 0.3, "#556B2F", alpha=0.6)
        ax.text(x0 + W / 2, 5.95, "Passivation + Pad Openings",
                ha="center", va="center", fontsize=5, color="white")
        # Bond pad openings
        for x in [1.0, 3.0, 5.0, 7.0, 9.0]:
            block(x, 5.8, 0.5, 0.3, C["metal"], "Pad")


# ═══════════════════════════════════════════════════════════════════════════
# TOP-DOWN SYSTEM ASSEMBLY STEPS
# ═══════════════════════════════════════════════════════════════════════════

def draw_system_assembly(ax, step):
    """Draw the top-down system assembly at the given step (0-7)."""
    ax.clear()
    ax.set_xlim(-1, 21)
    ax.set_ylim(-1, 17)
    ax.set_facecolor(C["bg"])
    ax.set_aspect("equal")
    ax.axis("off")

    def chip(x, y, w, h, color, label, fontsize=7):
        r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                           facecolor=color, edgecolor="white", linewidth=1.0)
        ax.add_patch(r)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=fontsize, color="white", fontweight="bold")

    def ring(cx, cy, r, color):
        circle = Circle((cx, cy), r, fill=False, edgecolor=color, linewidth=1.5)
        ax.add_patch(circle)

    def arrow(x1, y1, x2, y2, color="white"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.2))

    # ── Step 0: Bare ASIC die ──
    if step >= 0:
        chip(2, 1, 16, 14, "#1c2833", "ASIC Die\n(45SPCLO)", fontsize=9)

    # ── Step 1: Photonic circuit region ──
    if step >= 1:
        chip(3, 2, 9, 8, "#0d3b66", "Photonic\nIntegrated\nCircuit", fontsize=8)
        # Bus waveguide
        ax.plot([4, 11], [5, 5], color="#00bfff", lw=2, alpha=0.8)
        ax.text(7.5, 5.4, "Bus WG", fontsize=5, color="#00bfff", ha="center")

    # ── Step 2: MRR array ──
    if step >= 2:
        colors_mrr = ["#ff6347", "#ff8c00", "#ffd700", "#32cd32",
                       "#00ced1", "#4169e1", "#8a2be2", "#ff69b4"]
        for i in range(8):
            cx = 4.5 + i * 0.9
            ring(cx, 5, 0.35, colors_mrr[i])
        ax.text(8.0, 3.8, "8× MRR Switch Bank", fontsize=6,
                color="white", ha="center")

    # ── Step 3: Photodetector array ──
    if step >= 3:
        for i in range(8):
            cx = 4.5 + i * 0.9
            block_ax = FancyBboxPatch((cx - 0.2, 6.5), 0.4, 0.5,
                        boxstyle="square,pad=0", facecolor=C["ge"],
                        edgecolor="white", linewidth=0.5)
            ax.add_patch(block_ax)
        ax.text(8.0, 7.3, "8× Ge PD Array", fontsize=6,
                color=C["ge"], ha="center")

    # ── Step 4: CMOS control region ──
    if step >= 4:
        chip(3, 10.5, 9, 3.5, "#2c3e50", "", fontsize=7)
        # Sub-blocks
        chip(3.5, 11, 2.0, 1.2, "#e74c3c", "Counter\nLogic", fontsize=5)
        chip(5.8, 11, 2.0, 1.2, "#3498db", "PID\nLocking", fontsize=5)
        chip(8.1, 11, 2.0, 1.2, "#2ecc71", "DAC\nBank", fontsize=5)
        chip(3.5, 12.5, 2.0, 1.2, "#9b59b6", "TIA\nArray", fontsize=5)
        chip(5.8, 12.5, 2.0, 1.2, "#f39c12", "PCM\nPulser", fontsize=5)
        chip(8.1, 12.5, 2.0, 1.2, "#1abc9c", "Temp\nSensor", fontsize=5)
        ax.text(7.5, 10.2, "CMOS Control ASIC", fontsize=6,
                color="white", ha="center")

    # ── Step 5: Flip-chip comb source ──
    if step >= 5:
        chip(13, 3, 4, 4, C["comb_chip"], "SiN Comb\nSource\n(flip-chip)", fontsize=7)
        # Solder bumps
        for bx in [13.5, 14.5, 15.5, 16.0]:
            for by in [3.5, 5.5]:
                c = Circle((bx, by), 0.15, facecolor=C["solder"], edgecolor="white", lw=0.5)
                ax.add_patch(c)
        # Optical coupling arrow
        arrow(13, 5, 11.2, 5, "#00ff00")
        ax.text(12.1, 5.5, "λ₀-λ₇", fontsize=6, color="#00ff00", ha="center")

    # ── Step 6: Fiber array attach ──
    if step >= 6:
        # Input fiber
        ax.plot([0, 3.5], [5, 5], color=C["fiber"], lw=3, solid_capstyle="round")
        ax.text(0.3, 5.5, "Pump\nFiber", fontsize=5, color=C["fiber"])
        # Output fiber
        ax.plot([12, 20], [8, 8], color=C["fiber"], lw=3, solid_capstyle="round")
        ax.text(17, 8.5, "Output\nFiber", fontsize=5, color=C["fiber"])
        # Edge couplers
        for y in [5, 8]:
            ec = FancyBboxPatch((2.8, y - 0.3), 0.5, 0.6,
                    boxstyle="round,pad=0.05", facecolor="#00ffff",
                    edgecolor="white", linewidth=0.8)
            ax.add_patch(ec)

    # ── Step 7: Wire bonds + package ──
    if step >= 7:
        # Package outline
        pkg = FancyBboxPatch((-0.5, -0.5), 20, 16.5,
                boxstyle="round,pad=0.3", facecolor="none",
                edgecolor="#ffd700", linewidth=2.5, linestyle="--")
        ax.add_patch(pkg)
        ax.text(10, 16.3, "Hermetic Package", fontsize=7,
                color="#ffd700", ha="center", fontweight="bold")

        # Bond pads + wires to package edge
        pad_xs = [3, 5, 7, 9, 11]
        for px in pad_xs:
            # Bond wire arcs (simplified as curves)
            ax.plot([px, px - 0.5, -0.3], [14.5, 15.5, 15.8],
                    color=C["metal"], lw=0.8, alpha=0.7)
            ax.plot([px, px + 0.5, 19.3], [14.5, 15.5, 15.8],
                    color=C["metal"], lw=0.8, alpha=0.7)

        # DC + RF labels
        ax.text(-0.3, -0.2, "DC supply\nClock in", fontsize=5,
                color=C["text"], ha="left")
        ax.text(19, -0.2, "Readout\nbus", fontsize=5,
                color=C["text"], ha="right")


# ═══════════════════════════════════════════════════════════════════════════
# ANIMATION FRAME SEQUENCE
# ═══════════════════════════════════════════════════════════════════════════

# Each frame: (cross_section_step, assembly_step, title, caption)
FRAMES = [
    # Phase 1: Wafer fabrication (cross-section builds up)
    (0,  -1, "Step 1 / 22 — SOI Wafer",
     "Start: 300 mm SOI wafer\nSi substrate + 2 µm BOX + 220 nm Si device layer"),
    (1,  -1, "Step 2 / 22 — Waveguide Patterning",
     "Deep UV lithography + RIE etch\nDefine rib waveguides and MRR ring cavities"),
    (2,  -1, "Step 3 / 22 — Partial Etch (Slab)",
     "Partial Si etch: 90 nm slab for mode confinement\nEnables rib waveguide geometry + coupler regions"),
    (3,  -1, "Step 4 / 22 — PN Junction Implantation",
     "Ion implantation: n-type (phosphorus) + p-type (boron)\nZ-shape doping profile for 30 pm/V EO efficiency"),
    (4,  -1, "Step 5 / 22 — Germanium Epitaxy",
     "Selective Ge epitaxy on Si for photodetectors\n0.8 A/W responsivity, >50 GHz bandwidth"),
    (5,  -1, "Step 6 / 22 — SiN Deposition & Patterning",
     "PECVD Si₃N₄ (200–400 nm) for passive routing\nLow loss (0.14 dB/cm), visible-transparent"),
    (6,  -1, "Step 7 / 22 — SiO₂ Cladding",
     "PECVD oxide cladding deposition\nPlanarization for BEOL metal stack"),
    (7,  -1, "Step 8 / 22 — Contact Vias",
     "Via etch + tungsten fill to Si device layer\nConnects PN junctions and heaters to BEOL"),
    (8,  -1, "Step 9 / 22 — TiN Heater Layer",
     "TiN resistive heater patterning on M4–M5\n1 kΩ per heater, 4.3 mW/π with undercut"),
    (9,  -1, "Step 10 / 22 — Metal Interconnect Stack",
     "9-level Cu/Al BEOL metallization\nM6 ground plane shields RF from heater layers"),
    (10, -1, "Step 11 / 22 — CMOS Transistor Formation",
     "45 nm SOI FETs: counter logic, DACs, TIAs, PID\n< 1 mW digital power at 10 GHz clock"),
    (11, -1, "Step 12 / 22 — Thermal Undercut",
     "Isotropic Si substrate etch beneath MRR heaters\n5–40× improvement in thermal tuning efficiency"),
    (12, -1, "Step 13 / 22 — Phase-Change Material (Sb₂Se₃)",
     "Back-end Sb₂Se₃ patch deposition on MRR junctions\nNon-volatile resonance trimming, full-FSR range"),
    (13, -1, "Step 14 / 22 — Passivation + Pad Opening",
     "SiN/SiO₂ passivation; bond pad window etch\nWafer fabrication complete — ready for sort"),

    # Phase 2: System assembly (top-down view builds up)
    (13, 0, "Step 15 / 22 — Wafer Sort & Dice",
     "Electrical + optical probe test per die\nYield screen: ≥7/8 channels functional → pass"),
    (13, 1, "Step 16 / 22 — Photonic Circuit Region",
     "Bus waveguide connects all 8 MRR switch channels\nSiN routing, WDM demux, tap monitors"),
    (13, 2, "Step 17 / 22 — MRR Switch Bank",
     "8 microrings (R = 16 µm) on 100 GHz grid\nEach ring: EO switch + thermo-optic trim + PCM patch"),
    (13, 3, "Step 18 / 22 — Photodetector Array",
     "8× Ge-on-Si PIN photodiodes for readout\n+ 8× tap monitor PDs for wavelength locking"),
    (13, 4, "Step 19 / 22 — CMOS Control Blocks",
     "Counter logic | PID locking | DAC bank\nTIA array | PCM pulse generator | temp sensor"),
    (13, 5, "Step 20 / 22 — Comb Source Integration",
     "Flip-chip bonded high-Q SiN microcomb die\nDFB-pumped Kerr soliton → 8 wavelength channels"),
    (13, 6, "Step 21 / 22 — Fiber Array Attach",
     "Edge-coupled lensed fiber array (V-groove aligned)\nPump input + optical output; < 1.5 dB/facet"),
    (13, 7, "Step 22 / 22 — Package & Wire Bond",
     "Hermetic ceramic package; Au wire bonds\nTEC mount; DC + RF + fiber interfaces"),
]


# ═══════════════════════════════════════════════════════════════════════════
# RENDER ANIMATION
# ═══════════════════════════════════════════════════════════════════════════

def render():
    fig = plt.figure(figsize=(16, 8), facecolor=C["bg"])

    # Title area
    ax_title = fig.add_axes([0.0, 0.88, 1.0, 0.12])
    ax_title.set_facecolor(C["bg"])
    ax_title.axis("off")

    # Left panel: cross-section
    ax_xsec = fig.add_axes([0.02, 0.12, 0.46, 0.74])

    # Right panel: system assembly
    ax_sys = fig.add_axes([0.52, 0.12, 0.46, 0.74])

    # Caption area
    ax_cap = fig.add_axes([0.0, 0.0, 1.0, 0.12])
    ax_cap.set_facecolor("#0d0d1a")
    ax_cap.axis("off")

    title_text = ax_title.text(
        0.5, 0.55, "", ha="center", va="center",
        fontsize=14, color="#ffd700", fontweight="bold",
        transform=ax_title.transAxes
    )
    subtitle_text = ax_title.text(
        0.5, 0.1, "Photonic Color-Counter ASIC — GF 45SPCLO Process",
        ha="center", va="center", fontsize=9, color="#a0a0a0",
        transform=ax_title.transAxes
    )
    caption_text = ax_cap.text(
        0.5, 0.5, "", ha="center", va="center",
        fontsize=10, color=C["text"],
        transform=ax_cap.transAxes, linespacing=1.4
    )

    # Panel labels
    ax_xsec_label = fig.text(0.25, 0.87, "Cross-Section View",
                              ha="center", fontsize=10, color="#a0a0c0",
                              fontweight="bold")
    ax_sys_label = fig.text(0.75, 0.87, "System Assembly View",
                             ha="center", fontsize=10, color="#a0a0c0",
                             fontweight="bold")

    # Progress bar axis
    ax_prog = fig.add_axes([0.1, 0.095, 0.8, 0.015])
    ax_prog.set_facecolor("#0d0d1a")
    ax_prog.set_xlim(0, len(FRAMES))
    ax_prog.set_ylim(0, 1)
    ax_prog.axis("off")
    prog_bg = mpatches.FancyBboxPatch(
        (0, 0), len(FRAMES), 1, boxstyle="round,pad=0.05",
        facecolor="#333355", edgecolor="#555577", linewidth=0.5
    )
    ax_prog.add_patch(prog_bg)
    prog_bar = mpatches.FancyBboxPatch(
        (0, 0), 0, 1, boxstyle="round,pad=0.05",
        facecolor="#ffd700", edgecolor="none"
    )
    ax_prog.add_patch(prog_bar)

    def update(frame_idx):
        xs_step, sys_step, title, caption = FRAMES[frame_idx]

        title_text.set_text(title)
        caption_text.set_text(caption)

        draw_cross_section(ax_xsec, xs_step)
        if sys_step >= 0:
            draw_system_assembly(ax_sys, sys_step)
        else:
            ax_sys.clear()
            ax_sys.set_facecolor(C["bg"])
            ax_sys.axis("off")
            ax_sys.text(0.5, 0.5, "Wafer fabrication\nin progress…",
                        ha="center", va="center", fontsize=12,
                        color="#555577", transform=ax_sys.transAxes,
                        style="italic")

        # Update progress bar
        prog_bar.set_width(frame_idx + 1)

        return [title_text, caption_text]

    anim = animation.FuncAnimation(
        fig, update, frames=len(FRAMES),
        interval=2200,  # 2.2 seconds per frame
        blit=False, repeat=True
    )

    out_path = os.path.join(OUT_DIR, "manufacturing_process.gif")
    print(f"Rendering {len(FRAMES)}-frame animation...")
    print(f"  Frame interval: 2.2s | Total loop: {len(FRAMES) * 2.2:.0f}s")

    anim.save(out_path, writer="pillow", fps=1000/2200, dpi=120)
    print(f"  Saved: {out_path}")

    # Also save key frames as individual PNGs for reference
    key_frames = [0, 3, 5, 8, 11, 13, 16, 19, 21]
    for kf in key_frames:
        if kf < len(FRAMES):
            update(kf)
            frame_path = os.path.join(OUT_DIR, f"mfg_frame_{kf:02d}.png")
            fig.savefig(frame_path, dpi=100, facecolor=C["bg"], bbox_inches="tight")

    print(f"  Key frames saved: {len(key_frames)} PNGs")
    plt.close(fig)


if __name__ == "__main__":
    print("=" * 60)
    print("Manufacturing Process Animation Generator")
    print("PCC-ARCH-001 / PCC-IFS-001")
    print("=" * 60)
    render()
    print("\nDone.")
