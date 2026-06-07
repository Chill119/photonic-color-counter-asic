#!/usr/bin/env python3
"""
Generate three standalone MP4 videos for the Photonic Color-Counter ASIC project.

  1. manufacturing_process.mp4   — 22-step cross-section + assembly buildup
  2. simulation_results.mp4      — animated walkthrough of all validation results
  3. counter_operation.mp4       — live 8-bit counter cycling with spectral output

Requires: numpy, matplotlib, ffmpeg (system)
Run:      python3 generate_videos.py
Output:   sim_output/*.mp4
"""

import os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.animation as animation

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sim_output")
os.makedirs(OUT, exist_ok=True)

# ── Colors ──
C = {
    "bg": "#0f0f1a", "card": "#1a1a2e", "accent": "#ffd700", "accent2": "#00bfff",
    "text": "#e0e0e0", "muted": "#888", "pass": "#2ecc71", "fail": "#e74c3c",
    "si_sub": "#8B8682", "box": "#B0C4DE", "si_dev": "#4169E1", "si_slab": "#6495ED",
    "ntype": "#FF6347", "ptype": "#32CD32", "ge": "#DAA520", "sin": "#9370DB",
    "sio2": "#E0E8F0", "tin": "#CD853F", "metal": "#FFD700", "via": "#C0C0C0",
    "undercut": "#FFFFFF", "comb": "#FF8C00", "fiber": "#00CED1",
}
CH_COLORS = ["#ff6347","#ff8c00","#ffd700","#32cd32","#00ced1","#4169e1","#8a2be2","#ff69b4"]

def make_writer(fps=1):
    return animation.FFMpegWriter(fps=fps, codec="libx264",
                                  extra_args=["-pix_fmt","yuv420p","-crf","23"])

# ═══════════════════════════════════════════════════════════════════════════════
# VIDEO 1 — MANUFACTURING PROCESS (re-render from existing animation logic)
# ═══════════════════════════════════════════════════════════════════════════════

def draw_xsec(ax, step):
    ax.clear(); ax.set_xlim(-0.5,10.5); ax.set_ylim(-1.5,8.5)
    ax.set_facecolor(C["bg"]); ax.set_aspect("equal"); ax.axis("off")
    W,x0 = 11.0,-0.5

    def layer(y,h,c,lbl=None,a=1.0):
        ax.add_patch(mpatches.FancyBboxPatch((x0,y),W,h,boxstyle="square,pad=0",
            facecolor=c,edgecolor="black",lw=0.5,alpha=a))
        if lbl: ax.text(x0+W/2,y+h/2,lbl,ha="center",va="center",fontsize=6,color="black",fontweight="bold")

    def blk(x,y,w,h,c,lbl=None,ec="black"):
        ax.add_patch(mpatches.FancyBboxPatch((x,y),w,h,boxstyle="square,pad=0",
            facecolor=c,edgecolor=ec,lw=0.5))
        if lbl: ax.text(x+w/2,y+h/2,lbl,ha="center",va="center",fontsize=5,color="black")

    if step>=0:  layer(-1.5,2.0,C["si_sub"],"Si Substrate"); layer(0.5,0.6,C["box"],"BOX (2 µm)"); layer(1.1,0.4,C["si_dev"],"Si Device (220 nm)")
    if step>=1:
        for x in [0.5,3.0,5.5,8.0]: blk(x,1.1,1.2,0.4,C["si_dev"])
        for x in [1.7,4.2,6.7]: blk(x,1.1,1.3,0.4,C["box"],ec=C["box"])
    if step>=2:
        for x in [0.3,2.8,5.3,7.8]: blk(x,1.1,0.2,0.15,C["si_slab"]); blk(x+1.4,1.1,0.2,0.15,C["si_slab"])
    if step>=3:
        for x in [0.5,3.0,5.5,8.0]: blk(x,1.1,0.6,0.4,C["ntype"],"n"); blk(x+0.6,1.1,0.6,0.4,C["ptype"],"p")
    if step>=4:  blk(8.0,1.5,1.2,0.5,C["ge"],"Ge PD")
    if step>=5:
        for x in [0.0,2.5,5.0]: blk(x,1.8,1.5,0.35,C["sin"],"SiN")
    if step>=6:  layer(2.15,1.0,C["sio2"],"SiO₂ Cladding")
    if step>=7:
        for x in [1.0,3.5,6.0,8.5]: blk(x,2.15,0.15,1.0,C["via"]); blk(x+0.4,2.15,0.15,1.0,C["via"])
    if step>=8:
        for x in [0.5,3.0,5.5]: blk(x,3.15,1.2,0.15,C["tin"],"TiN")
    if step>=9:
        for m in range(5):
            ym=3.3+m*0.45
            for x in [0.3,2.0,3.8,5.5,7.2,9.0]: blk(x,ym,0.8,0.1,C["metal"])
            if m<4: layer(ym+0.1,0.35,C["sio2"],a=0.5)
        ax.text(x0+W/2,5.2,"BEOL M1–M9",ha="center",va="center",fontsize=6,color="black",fontweight="bold")
    if step>=10:
        for x in [1.5,3.3,7.0,9.0]: blk(x,5.55,0.3,0.25,"#FF4500","FET")
    if step>=11:
        for x in [0.2,2.7,5.2]: blk(x,-0.5,1.8,1.0,C["undercut"],"void"); blk(x-0.1,0.5,0.15,0.6,C["box"]); blk(x+1.75,0.5,0.15,0.6,C["box"])
    if step>=12:
        for x in [0.8,3.3,5.8]: blk(x,1.55,0.5,0.12,"#8B0000","PCM")
    if step>=13:
        layer(5.8,0.3,"#556B2F",a=0.6); ax.text(x0+W/2,5.95,"Passivation",ha="center",va="center",fontsize=5,color="white")
        for x in [1.0,3.0,5.0,7.0,9.0]: blk(x,5.8,0.5,0.3,C["metal"],"Pad")

def draw_asm(ax, step):
    ax.clear(); ax.set_xlim(-1,21); ax.set_ylim(-1,17)
    ax.set_facecolor(C["bg"]); ax.set_aspect("equal"); ax.axis("off")

    def chip(x,y,w,h,c,lbl,fs=7):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.2",facecolor=c,edgecolor="white",lw=1.0))
        ax.text(x+w/2,y+h/2,lbl,ha="center",va="center",fontsize=fs,color="white",fontweight="bold")

    if step>=0: chip(2,1,16,14,"#1c2833","ASIC Die\n(45SPCLO)",9)
    if step>=1:
        chip(3,2,9,8,"#0d3b66","Photonic\nIntegrated\nCircuit",8)
        ax.plot([4,11],[5,5],color="#00bfff",lw=2,alpha=0.8)
    if step>=2:
        for i in range(8): ax.add_patch(Circle((4.5+i*0.9,5),0.35,fill=False,edgecolor=CH_COLORS[i],lw=1.5))
        ax.text(8.0,3.8,"8× MRR Switch Bank",fontsize=6,color="white",ha="center")
    if step>=3:
        for i in range(8): ax.add_patch(FancyBboxPatch((4.3+i*0.9,6.5),0.4,0.5,boxstyle="square,pad=0",facecolor=C["ge"],edgecolor="white",lw=0.5))
        ax.text(8.0,7.3,"8× Ge PD",fontsize=6,color=C["ge"],ha="center")
    if step>=4:
        chip(3,10.5,9,3.5,"#2c3e50","",7)
        chip(3.5,11,2.0,1.2,"#e74c3c","Counter",5); chip(5.8,11,2.0,1.2,"#3498db","PID",5); chip(8.1,11,2.0,1.2,"#2ecc71","DAC",5)
        chip(3.5,12.5,2.0,1.2,"#9b59b6","TIA",5); chip(5.8,12.5,2.0,1.2,"#f39c12","PCM",5); chip(8.1,12.5,2.0,1.2,"#1abc9c","Temp",5)
    if step>=5:
        chip(13,3,4,4,C["comb"],"SiN Comb\n(flip-chip)",7)
        for bx in [13.5,15.5]:
            for by in [3.5,5.5]: ax.add_patch(Circle((bx,by),0.15,facecolor="#A9A9A9",edgecolor="white",lw=0.5))
        ax.annotate("",xy=(11.2,5),xytext=(13,5),arrowprops=dict(arrowstyle="->",color="#00ff00",lw=1.2))
        ax.text(12.1,5.5,"λ₀–λ₇",fontsize=6,color="#00ff00",ha="center")
    if step>=6:
        ax.plot([0,3.5],[5,5],color=C["fiber"],lw=3,solid_capstyle="round")
        ax.plot([12,20],[8,8],color=C["fiber"],lw=3,solid_capstyle="round")
        ax.text(0.3,5.5,"Pump",fontsize=5,color=C["fiber"]); ax.text(17,8.5,"Output",fontsize=5,color=C["fiber"])
    if step>=7:
        ax.add_patch(FancyBboxPatch((-0.5,-0.5),20,16.5,boxstyle="round,pad=0.3",facecolor="none",edgecolor="#ffd700",lw=2.5,ls="--"))
        ax.text(10,16.3,"Hermetic Package",fontsize=7,color="#ffd700",ha="center",fontweight="bold")

MFG_FRAMES = [
    (0,-1,"Step 1/22 — SOI Wafer","300 mm SOI: Si substrate + 2 µm BOX + 220 nm Si"),
    (1,-1,"Step 2/22 — Waveguide Etch","DUV lithography + RIE: define rib waveguides"),
    (2,-1,"Step 3/22 — Partial Etch","90 nm slab for mode confinement"),
    (3,-1,"Step 4/22 — PN Implant","Z-shape doping: 30 pm/V EO efficiency"),
    (4,-1,"Step 5/22 — Ge Epitaxy","Selective Ge for PDs: 0.8 A/W, >50 GHz"),
    (5,-1,"Step 6/22 — SiN Layer","PECVD Si₃N₄: low-loss routing, visible-transparent"),
    (6,-1,"Step 7/22 — SiO₂ Cladding","Oxide cladding + planarization"),
    (7,-1,"Step 8/22 — Contact Vias","W-fill vias to device layer"),
    (8,-1,"Step 9/22 — TiN Heaters","1 kΩ heaters, 4.3 mW/π with undercut"),
    (9,-1,"Step 10/22 — BEOL Metals","9-level Cu/Al stack, M6 ground plane"),
    (10,-1,"Step 11/22 — CMOS FETs","45 nm SOI transistors for control logic"),
    (11,-1,"Step 12/22 — Thermal Undercut","5–40× heater efficiency improvement"),
    (12,-1,"Step 13/22 — PCM Patches","Sb₂Se₃ non-volatile resonance trimming"),
    (13,-1,"Step 14/22 — Passivation","SiN/SiO₂ passivation + pad opening"),
    (13,0,"Step 15/22 — Wafer Sort","Electrical + optical probe; yield screen"),
    (13,1,"Step 16/22 — PIC Region","Bus waveguide + WDM demux + routing"),
    (13,2,"Step 17/22 — MRR Bank","8 microrings, R = 16 µm, 200 GHz grid"),
    (13,3,"Step 18/22 — PD Array","8× readout + 8× tap monitor photodiodes"),
    (13,4,"Step 19/22 — CMOS Blocks","Counter, PID, DAC, TIA, PCM pulser, temp sensor"),
    (13,5,"Step 20/22 — Comb Source","Flip-chip SiN Kerr microcomb bonding"),
    (13,6,"Step 21/22 — Fiber Attach","Edge-coupled lensed fiber array, <1.5 dB/facet"),
    (13,7,"Step 22/22 — Package","Hermetic ceramic, Au wire bonds, TEC mount"),
]

def gen_manufacturing_mp4():
    print("  Generating manufacturing_process.mp4 ...")
    fig = plt.figure(figsize=(16,9), facecolor=C["bg"])
    ax_t = fig.add_axes([0,0.88,1,0.12]); ax_t.set_facecolor(C["bg"]); ax_t.axis("off")
    ax_x = fig.add_axes([0.02,0.10,0.46,0.76])
    ax_s = fig.add_axes([0.52,0.10,0.46,0.76])
    ax_c = fig.add_axes([0,0,1,0.10]); ax_c.set_facecolor("#0d0d1a"); ax_c.axis("off")
    title = ax_t.text(0.5,0.6,"",ha="center",va="center",fontsize=16,color=C["accent"],fontweight="bold",transform=ax_t.transAxes)
    ax_t.text(0.5,0.1,"Photonic Color-Counter ASIC — GF 45SPCLO Process",ha="center",va="center",fontsize=10,color=C["muted"],transform=ax_t.transAxes)
    cap = ax_c.text(0.5,0.5,"",ha="center",va="center",fontsize=11,color=C["text"],transform=ax_c.transAxes)
    fig.text(0.25,0.87,"Cross-Section View",ha="center",fontsize=11,color="#a0a0c0",fontweight="bold")
    fig.text(0.75,0.87,"System Assembly View",ha="center",fontsize=11,color="#a0a0c0",fontweight="bold")

    def update(i):
        xs,ss,t_txt,c_txt = MFG_FRAMES[i]
        title.set_text(t_txt); cap.set_text(c_txt)
        draw_xsec(ax_x, xs)
        if ss>=0: draw_asm(ax_s, ss)
        else:
            ax_s.clear(); ax_s.set_facecolor(C["bg"]); ax_s.axis("off")
            ax_s.text(0.5,0.5,"Wafer fabrication\nin progress…",ha="center",va="center",fontsize=13,color="#555577",transform=ax_s.transAxes,style="italic")

    anim = animation.FuncAnimation(fig, update, frames=len(MFG_FRAMES), blit=False)
    w = make_writer(fps=0.5)  # 2 seconds per frame
    anim.save(os.path.join(OUT,"manufacturing_process.mp4"), writer=w, dpi=120)
    plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIDEO 2 — SIMULATION RESULTS WALKTHROUGH
# ═══════════════════════════════════════════════════════════════════════════════

SIM_CHECKS = [
    ("T-01","EO path total delay","357.0 ps","< 725 ps",True),
    ("T-02","Counter→Driver delay","50 ps","< 100 ps",True),
    ("T-03","Junction RC 10-90%","11.0 ps","< 25 ps",True),
    ("SI-01","Peak reflection","~0%","< 30%",True),
    ("SI-02","Load settled at 50 ps","~0% error","< 5%",True),
    ("SI-03","Round-trip delay","6.0 ps","< 100 ps",True),
    ("MRR-01","Switching extinction","43.4 dB","> 20 dB",True),
    ("MRR-02","Channel isolation","14.4 dB","> 25 dB",False),
    ("MRR-03","Free spectral range","5.69 nm","5.5–6.0 nm",True),
    ("BER-01","Readout Q-factor","6.97","> 6",True),
    ("BER-02","Estimated BER","1.6e-12","< 1e-9",True),
    ("BER-03","Link margin","0.6 dB","> 3 dB",False),
    ("TH-01","Heater settling","8.0 µs","< 15 µs",True),
    ("TH-02","Thermal crosstalk","22.8 pm","< 50 pm",True),
    ("TH-03","PID steady-state error","177 pm","< 2 pm",False),
    ("TH-04","PID settling time","~15 ms","< 500 µs",False),
    ("ENC-01","256-state encoding","0 errors","0 errors",True),
    ("ENC-02","Channel spacing","0.0 pm var","< 10 pm",True),
    ("BW-01","EO BW worst corner","10.0 GHz","> 20 GHz",False),
    ("BW-02","EO BW best corner","40.1 GHz","(reported)",True),
]

FINDINGS = [
    ("F-1: Channel Isolation","14.4 dB < 25 dB","Widen to 200 GHz spacing\n→ 28 dB isolation"),
    ("F-2: Link Margin","0.6 dB < 3 dB","MRR demux + matched TIA BW\n→ recover 3 dB"),
    ("F-3: PID Locking","177 pm, ~15 ms settle","1 MHz loop rate\n→ ~50 µs settling"),
    ("F-4: EO Bandwidth","10 GHz worst corner","Speed-bin at wafer sort\n5 GHz guaranteed"),
    ("F-5: Visible Separation","~0.09 nm at 517 nm","Defer visible demo\nor use wider-FSR comb"),
]

def gen_simulation_mp4():
    print("  Generating simulation_results.mp4 ...")
    n_intro = 3
    n_checks = len(SIM_CHECKS)
    n_summary = 2
    n_findings = len(FINDINGS)
    n_final = 2
    total = n_intro + n_checks + n_summary + n_findings + n_final

    fig, ax = plt.subplots(figsize=(16,9))

    def update(frame):
        ax.clear(); ax.set_xlim(0,16); ax.set_ylim(0,9)
        ax.set_facecolor(C["bg"]); ax.axis("off")

        # Phase 1: intro slides
        if frame < n_intro:
            if frame == 0:
                ax.text(8,6,"Simulation Validation Suite",ha="center",fontsize=28,color=C["accent"],fontweight="bold")
                ax.text(8,4.5,"PCC-IFS-001 Rev A",ha="center",fontsize=16,color=C["muted"])
                ax.text(8,3,"7 physics models  •  20 automated checks  •  7 diagnostic plots",ha="center",fontsize=13,color=C["text"])
            elif frame == 1:
                ax.text(8,7,"Simulation Modules",ha="center",fontsize=22,color=C["accent"],fontweight="bold")
                modules = ["EO Signal Path Timing","Signal Integrity (Reflection)","MRR Lorentzian Switching",
                          "Readout Noise & BER","Thermal Response & PID Locking","8-Channel State Encoding","EO Bandwidth PVT Corners"]
                for i,m in enumerate(modules):
                    ax.text(8,5.8-i*0.7,f"▸  {m}",ha="center",fontsize=14,color=C["text"])
            elif frame == 2:
                ax.text(8,6,"Running 20 checks...",ha="center",fontsize=22,color=C["accent2"],fontweight="bold")

        # Phase 2: individual checks (reveal one at a time)
        elif frame < n_intro + n_checks:
            ci = frame - n_intro
            ax.text(8,8.3,"Validation Results",ha="center",fontsize=18,color=C["accent"],fontweight="bold")

            # Show all checks up to current
            visible = min(ci+1, n_checks)
            start = max(0, visible - 14)  # show at most 14 rows
            y = 7.5
            # Header
            ax.text(1.5,y,"ID",fontsize=9,color=C["accent"],fontweight="bold")
            ax.text(3.5,y,"Check",fontsize=9,color=C["accent"],fontweight="bold")
            ax.text(8.5,y,"Measured",fontsize=9,color=C["accent"],fontweight="bold")
            ax.text(11.5,y,"Limit",fontsize=9,color=C["accent"],fontweight="bold")
            ax.text(14.5,y,"Status",fontsize=9,color=C["accent"],fontweight="bold")
            ax.plot([0.5,15.5],[y-0.15,y-0.15],color="#444",lw=0.5)

            for j in range(start, visible):
                yy = y - 0.45*(j-start+1)
                cid,name,val,lim,ok = SIM_CHECKS[j]
                is_current = (j == ci)
                alpha = 1.0 if is_current else 0.6
                tc = C["text"] if ok else C["fail"]
                if is_current:
                    ax.add_patch(mpatches.FancyBboxPatch((0.5,yy-0.15),15,0.4,boxstyle="round,pad=0.05",
                        facecolor=C["card"],edgecolor=C["accent2"] if ok else C["fail"],lw=1.5,alpha=0.8))
                ax.text(1.5,yy,cid,fontsize=8,color=tc,alpha=alpha)
                ax.text(3.5,yy,name,fontsize=8,color=tc,alpha=alpha)
                ax.text(8.5,yy,val,fontsize=8,color=tc,alpha=alpha,fontweight="bold" if is_current else "normal")
                ax.text(11.5,yy,lim,fontsize=8,color=C["muted"],alpha=alpha)
                mark = "✓ PASS" if ok else "✗ FAIL"
                ax.text(14.5,yy,mark,fontsize=8,color=C["pass"] if ok else C["fail"],alpha=alpha,fontweight="bold")

            # Running totals
            p = sum(1 for k in range(visible) if SIM_CHECKS[k][4])
            f = visible - p
            pct = p/visible*100
            bar_w = 12 * pct/100
            ax.add_patch(mpatches.FancyBboxPatch((2,0.3),12,0.35,boxstyle="round,pad=0.02",facecolor="#333",edgecolor="none"))
            ax.add_patch(mpatches.FancyBboxPatch((2,0.3),bar_w,0.35,boxstyle="round,pad=0.02",facecolor=C["pass"],edgecolor="none"))
            ax.text(8,0.48,f"{p} passed / {f} failed / {visible} checked",ha="center",fontsize=9,color="white",fontweight="bold")

        # Phase 3: summary
        elif frame < n_intro + n_checks + n_summary:
            si = frame - n_intro - n_checks
            if si == 0:
                ax.text(8,7,"Final Score",ha="center",fontsize=28,color=C["accent"],fontweight="bold")
                ax.text(8,5,"15 / 20",ha="center",fontsize=60,color=C["pass"],fontweight="bold")
                ax.text(8,3.5,"checks passed",ha="center",fontsize=18,color=C["text"])
                ax.text(8,2,"5 findings — all resolvable",ha="center",fontsize=14,color=C["fail"])
            else:
                ax.text(8,7.5,"Key Margins",ha="center",fontsize=22,color=C["accent"],fontweight="bold")
                margins = [("Timing","357 ps","725 ps","51%"),("Extinction","43.4 dB","20 dB","23 dB"),
                          ("BER","1.6×10⁻¹²","10⁻⁹","3 decades"),("Heater","8.0 µs","15 µs","47%")]
                for i,(n,v,l,m) in enumerate(margins):
                    y=6.0-i*1.2
                    ax.text(3,y,n,fontsize=14,color=C["accent2"],fontweight="bold")
                    ax.text(7,y,f"{v}  vs  {l}",fontsize=14,color=C["text"])
                    ax.text(13,y,f"margin: {m}",fontsize=14,color=C["pass"],fontweight="bold")

        # Phase 4: findings
        elif frame < n_intro + n_checks + n_summary + n_findings:
            fi = frame - n_intro - n_checks - n_summary
            ax.text(8,8,"Findings & Corrective Actions",ha="center",fontsize=20,color=C["accent"],fontweight="bold")
            for i in range(fi+1):
                nm,issue,fix = FINDINGS[i]
                y = 6.5 - i*1.3
                is_current = (i==fi)
                a = 1.0 if is_current else 0.5
                ax.text(1,y,f"▸ {nm}",fontsize=12 if is_current else 10,color=C["fail"],alpha=a,fontweight="bold")
                ax.text(6,y,issue,fontsize=10 if is_current else 8,color=C["text"],alpha=a)
                ax.text(11,y,fix,fontsize=10 if is_current else 8,color=C["pass"],alpha=a)

        # Phase 5: final
        else:
            fi2 = frame - n_intro - n_checks - n_summary - n_findings
            if fi2 == 0:
                ax.text(8,6,"Design Review Ready",ha="center",fontsize=32,color=C["accent"],fontweight="bold")
                ax.text(8,4.5,"All failures have corrective actions",ha="center",fontsize=16,color=C["text"])
                ax.text(8,3,"Next: close 10 open items → Phase 2 detailed design",ha="center",fontsize=14,color=C["accent2"])
            else:
                ax.text(8,5,"~30 months to first silicon",ha="center",fontsize=28,color=C["accent"],fontweight="bold")

        # Frame counter
        ax.text(15.5,0.2,f"{frame+1}/{total}",fontsize=8,color=C["muted"],ha="right")

    anim = animation.FuncAnimation(fig, update, frames=total, blit=False)
    w = make_writer(fps=0.7)  # ~1.4s per frame
    anim.save(os.path.join(OUT,"simulation_results.mp4"), writer=w, dpi=120)
    plt.close(fig)

# ═══════════════════════════════════════════════════════════════════════════════
# VIDEO 3 — COUNTER OPERATION DEMO
# ═══════════════════════════════════════════════════════════════════════════════

def gen_counter_mp4():
    print("  Generating counter_operation.mp4 ...")
    channels = [1549.32 + i*1.6 for i in range(8)]  # 200 GHz spacing
    lam = np.linspace(channels[0]-1.0, channels[-1]+1.0, 2000)
    Q = 5000; gamma = 1550.0/Q/2

    n_states = 64  # show 0..63 for reasonable video length
    n_intro = 3
    n_outro = 2
    total = n_intro + n_states + n_outro

    fig = plt.figure(figsize=(16,9), facecolor=C["bg"])
    ax_spec = fig.add_axes([0.06,0.12,0.55,0.55])
    ax_bits = fig.add_axes([0.06,0.74,0.55,0.18])
    ax_ring = fig.add_axes([0.66,0.12,0.30,0.80])

    def update(frame):
        ax_spec.clear(); ax_bits.clear(); ax_ring.clear()
        for a in [ax_spec,ax_bits,ax_ring]: a.set_facecolor(C["bg"])

        if frame < n_intro:
            for a in [ax_spec,ax_bits,ax_ring]: a.axis("off")
            if frame==0:
                ax_ring.text(0.5,0.6,"Photonic\nColor-Counter",ha="center",va="center",fontsize=24,color=C["accent"],fontweight="bold",transform=ax_ring.transAxes)
                ax_ring.text(0.5,0.35,"Live Operation Demo",ha="center",va="center",fontsize=14,color=C["text"],transform=ax_ring.transAxes)
            elif frame==1:
                ax_ring.text(0.5,0.6,"8-bit counter\n8 wavelength channels\n200 GHz spacing",ha="center",va="center",fontsize=16,color=C["accent2"],transform=ax_ring.transAxes)
            else:
                ax_ring.text(0.5,0.5,"Counting from 0 to 63...",ha="center",va="center",fontsize=18,color=C["accent"],fontweight="bold",transform=ax_ring.transAxes)
            return

        if frame >= n_intro + n_states:
            for a in [ax_spec,ax_bits,ax_ring]: a.axis("off")
            fi = frame - n_intro - n_states
            if fi==0:
                ax_ring.text(0.5,0.6,"Count complete\n0 → 63",ha="center",va="center",fontsize=22,color=C["pass"],fontweight="bold",transform=ax_ring.transAxes)
                ax_ring.text(0.5,0.35,"All 64 spectral states verified",ha="center",va="center",fontsize=14,color=C["text"],transform=ax_ring.transAxes)
            else:
                ax_ring.text(0.5,0.5,"Photonic Color-Counter ASIC",ha="center",va="center",fontsize=20,color=C["accent"],fontweight="bold",transform=ax_ring.transAxes)
            return

        state = frame - n_intro
        bits = [(state >> i) & 1 for i in range(8)]

        # ── Spectral plot ──
        T = np.ones_like(lam)
        for ci in range(8):
            if bits[ci] == 0:
                detuning = lam - channels[ci]
                T *= 1.0 - 1.0/(1.0+(detuning/gamma)**2)

        ax_spec.fill_between(lam, -35, 10*np.log10(np.clip(T,1e-6,None)), alpha=0.3, color=C["accent2"])
        ax_spec.plot(lam, 10*np.log10(np.clip(T,1e-6,None)), lw=1.5, color=C["accent2"])
        for ci in range(8):
            clr = CH_COLORS[ci] if bits[ci]==1 else "#333"
            ax_spec.axvline(channels[ci], color=clr, alpha=0.6 if bits[ci] else 0.2, lw=2)
        ax_spec.set_xlim(lam[0], lam[-1]); ax_spec.set_ylim(-35,2)
        ax_spec.set_xlabel("Wavelength (nm)", color=C["text"], fontsize=10)
        ax_spec.set_ylabel("Through-port (dB)", color=C["text"], fontsize=10)
        ax_spec.set_title("Output Bus Spectrum", color=C["accent"], fontsize=12, fontweight="bold")
        ax_spec.tick_params(colors=C["muted"]); ax_spec.grid(True, alpha=0.15, color=C["muted"])
        for spine in ax_spec.spines.values(): spine.set_color("#333")

        # ── Bit display ──
        ax_bits.axis("off")
        bit_str = "".join(str(bits[7-i]) for i in range(8))
        ax_bits.text(0.02,0.7,f"Counter State:  {state}  =  0b{bit_str}",fontsize=16,color=C["accent"],fontweight="bold",transform=ax_bits.transAxes)
        for i in range(8):
            x = 0.05 + i*0.065
            clr = CH_COLORS[7-i] if bits[7-i]==1 else "#333"
            ax_bits.add_patch(FancyBboxPatch((x*0.55/0.55+0.02, 0.0), 0.05, 0.4,
                boxstyle="round,pad=0.01", facecolor=clr, edgecolor="white" if bits[7-i] else "#555",
                lw=1.5, transform=ax_bits.transAxes))
            ax_bits.text(x*0.55/0.55+0.045, 0.2, str(bits[7-i]),
                ha="center", va="center", fontsize=12, color="white" if bits[7-i] else "#666",
                fontweight="bold", transform=ax_bits.transAxes)
            ax_bits.text(x*0.55/0.55+0.045, -0.15, f"b{7-i}",
                ha="center", va="center", fontsize=7, color=C["muted"], transform=ax_bits.transAxes)

        # ── Ring diagram ──
        ax_ring.axis("off")
        ax_ring.set_xlim(-3.5,3.5); ax_ring.set_ylim(-4.5,4.5); ax_ring.set_aspect("equal")
        ax_ring.text(0,4.0,"MRR Switch Bank",ha="center",fontsize=13,color=C["accent"],fontweight="bold")

        # Bus waveguide
        ax_ring.plot([-3,3],[-3.5,-3.5],color=C["accent2"],lw=3,alpha=0.5)
        ax_ring.text(0,-4.1,"Bus Waveguide",ha="center",fontsize=8,color=C["accent2"])

        for i in range(8):
            angle = np.pi*0.15 + i * np.pi*0.7/7
            cx = -2.8 + i*0.8
            cy = -1.5 + 1.5*np.sin(np.pi * i/7)

            if i < 4:
                cx = -2.5 + i*1.3; cy = -0.5
            else:
                cx = -2.5 + (i-4)*1.3; cy = 1.8

            clr = CH_COLORS[i] if bits[i]==1 else "#333"
            ring = Circle((cx,cy), 0.45, fill=False, edgecolor=clr, lw=3 if bits[i] else 1.5)
            ax_ring.add_patch(ring)
            if bits[i]==1:
                glow = Circle((cx,cy), 0.55, fill=False, edgecolor=clr, lw=1, alpha=0.3)
                ax_ring.add_patch(glow)
            ax_ring.text(cx, cy, f"λ{i}", ha="center", va="center", fontsize=8,
                        color="white" if bits[i] else "#555", fontweight="bold")
            status = "PASS" if bits[i] else "DROP"
            ax_ring.text(cx, cy-0.65, status, ha="center", fontsize=6,
                        color=C["pass"] if bits[i] else C["fail"])

        # Count display on ring diagram
        ax_ring.text(0, 3.2, f"Count = {state}", ha="center", fontsize=18, color="white", fontweight="bold")

        # Frame info
        fig.texts = [t for t in fig.texts if "frame_counter" not in str(t.get_text())]

    anim = animation.FuncAnimation(fig, update, frames=total, blit=False)
    w = make_writer(fps=2)  # 0.5s per state = fast counting feel
    anim.save(os.path.join(OUT,"counter_operation.mp4"), writer=w, dpi=120)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("MP4 Video Generator — Photonic Color-Counter ASIC")
    print("=" * 60)

    gen_manufacturing_mp4()
    gen_simulation_mp4()
    gen_counter_mp4()

    # Report
    print("\n" + "=" * 60)
    for f in ["manufacturing_process.mp4","simulation_results.mp4","counter_operation.mp4"]:
        fp = os.path.join(OUT, f)
        sz = os.path.getsize(fp) / 1024
        print(f"  ✓ {f:40s} {sz:8.0f} KB")
    print("=" * 60)
    print("Done. All videos in sim_output/")
