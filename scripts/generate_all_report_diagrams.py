"""
generate_all_report_diagrams.py
Generates publication-quality architectural and workflow diagrams for GuardNode IoT
based on the system specifications and Eraser board architecture.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

ASSETS_DIR = "docs/report_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

# Shared Color Palette
NAVY = "#0F2942"
HEADER_BLUE = "#1E3A8A"
BLUE = "#2563EB"
TEAL = "#0D9488"
INDIGO = "#4F46E5"
AMBER = "#D97706"
RED = "#DC2626"
EMERALD = "#059669"
PURPLE = "#7C3AED"
BOX_BG = "#F8FAFC"
BOX_BORDER = "#CBD5E1"
TEXT_DARK = "#1E293B"
TEXT_MUTED = "#64748B"
ARROW_COLOR = "#334155"

def generate_fsm_diagram():
    """Generates Figure 3.2: Endpoint Security State Transition Machine."""
    fig, ax = plt.subplots(figsize=(11.5, 6.0), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 95, "ENDPOINT SECURITY FINITE STATE MACHINE (FSM) & QUARANTINE LIFECYCLE",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color=NAVY)
    ax.text(50, 90.5, "Dynamic Threat Scoring, Transient Burst Smoothing, and Automated Alert Mitigation",
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color=TEXT_MUTED)

    # 4 States
    states = [
        {
            "title": "OBSERVING / WARMUP",
            "desc": "Buffer Warmup ($|H_i| < K_{min}$)\nCollecting initial 5s windows\nNo inference evaluated",
            "color": BLUE, "bg": "#EFF6FF", "border": "#93C5FD",
            "x": 4, "y": 42, "w": 20, "h": 36
        },
        {
            "title": "NORMAL TRAFFIC",
            "desc": "Decision function $f(z) < \\tau$\nBaseline operating envelope\nNominal background telemetry\nSuspicion counter decrements",
            "color": EMERALD, "bg": "#ECFDF5", "border": "#6EE7B7",
            "x": 28, "y": 42, "w": 20, "h": 36
        },
        {
            "title": "SUSPICIOUS BURST",
            "desc": "First anomaly trigger ($f(z) \\geq \\tau$)\nSingle 5s window threshold breach\nFlagged for priority polling\nNo disruptive network block",
            "color": AMBER, "bg": "#FFFBEB", "border": "#FCD34D",
            "x": 52, "y": 42, "w": 20, "h": 36
        },
        {
            "title": "INTRUSION QUARANTINE",
            "desc": "Consecutive trigger ($f(z) \\geq \\tau$ twice)\nActive high-confidence flood\nImmediate alert dispatched\niptables drop / traffic isolated",
            "color": RED, "bg": "#FEF2F2", "border": "#FCA5A5",
            "x": 76, "y": 42, "w": 20, "h": 36
        }
    ]

    for st in states:
        card = FancyBboxPatch((st["x"], st["y"]), st["w"], st["h"],
                              boxstyle="round,pad=0.5,rounding_size=1.2",
                              facecolor=st["bg"], edgecolor=st["border"], linewidth=1.5)
        ax.add_patch(card)
        
        # Header banner
        hdr = FancyBboxPatch((st["x"], st["y"] + st["h"] - 7.5), st["w"], 7.5,
                             boxstyle="round,pad=0.3,rounding_size=1.0",
                             facecolor=st["color"], edgecolor=st["color"])
        ax.add_patch(hdr)
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 3.75, st["title"],
                ha='center', va='center', fontsize=8.5, fontweight='bold', color='#FFFFFF')

        # Description text
        lines = st["desc"].split('\n')
        for l_idx, line in enumerate(lines):
            ax.text(st["x"] + 1.5, st["y"] + st["h"] - 11.5 - (l_idx * 5.2), "• " + line,
                    ha='left', va='center', fontsize=7.2, color=TEXT_DARK)

    # Transition Arrows
    # 1. Start -> Observing
    ax.annotate("", xy=(4, 60), xytext=(0.5, 60),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR, lw=1.8))
    ax.text(2.0, 62.5, "New IP", ha='center', va='bottom', fontsize=7.0, fontweight='bold', color=ARROW_COLOR)

    # 2. Observing -> Normal
    ax.annotate("", xy=(28, 60), xytext=(24, 60),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR, lw=1.8))
    ax.text(26, 62.5, r"$K \geq 2$", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=ARROW_COLOR)

    # 3. Normal -> Suspicious
    ax.annotate("", xy=(52, 64), xytext=(48, 64),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR, lw=1.8))
    ax.text(50, 66.5, r"$f(z) \geq \tau$", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=ARROW_COLOR)

    # 4. Suspicious -> Normal (Burst decays)
    ax.annotate("", xy=(48, 52), xytext=(52, 52),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR, lw=1.8, connectionstyle="arc3,rad=-0.15"))
    ax.text(50, 48.0, r"$f(z) < \tau$ (Decay)", ha='center', va='top', fontsize=7.0, fontweight='bold', color=ARROW_COLOR)

    # 5. Suspicious -> Intrusion
    ax.annotate("", xy=(76, 64), xytext=(72, 64),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.0))
    ax.text(74, 66.5, r"2nd $f(z) \geq \tau$", ha='center', va='bottom', fontsize=7.2, fontweight='bold', color=RED)

    # 6. Intrusion -> Suspicious (Attack Ceasing)
    ax.annotate("", xy=(72, 52), xytext=(76, 52),
                arrowprops=dict(arrowstyle="-|>", color=ARROW_COLOR, lw=1.8, connectionstyle="arc3,rad=-0.15"))
    ax.text(74, 48.0, r"$f(z) < \tau$", ha='center', va='top', fontsize=7.0, fontweight='bold', color=ARROW_COLOR)

    # Summary box at bottom
    sum_box = FancyBboxPatch((8, 8), 84, 24, boxstyle="round,pad=0.5,rounding_size=1.0",
                             facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0)
    ax.add_patch(sum_box)
    ax.text(10, 27, "FSM OPERATIONAL PARAMETERS & MITIGATION POLICIES:", fontsize=8.5, fontweight='bold', color=NAVY)
    ax.text(10, 21, "1. Observation Window: Discrete 5.0-second non-overlapping epochs.", fontsize=7.8, color=TEXT_DARK)
    ax.text(10, 16, "2. Transient Smoothing: Requires 2 consecutive threshold breaches to prevent false alarms from legitimate camera/download bursts.", fontsize=7.8, color=TEXT_DARK)
    ax.text(10, 11, "3. Automated Quarantine: On INTRUSION trigger, system notifies dashboard and can automatically inject iptables packet drop rules.", fontsize=7.8, color=TEXT_DARK)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "figure_fsm_state_machine.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"FSM diagram generated: {out_path}")

def generate_sniffing_pipeline_diagram():
    """Generates Figure 4.1: Live Packet Sniffing & Ingestion Pipeline."""
    fig, ax = plt.subplots(figsize=(12.0, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 95.5, "GUARDNODE LIVE PACKET SNIFFING & INGESTION PIPELINE",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color=NAVY)
    ax.text(50, 91.0, "Multi-Threaded Asynchronous Frame Capture, Interface Auto-Resolution, and Ring Buffer Aggregation",
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color=TEXT_MUTED)

    # 4 Main Blocks
    blocks = [
        {
            "step": "STEP 1: NIC RESOLUTION",
            "title": "Network Interface Manager",
            "items": [
                "UDP Socket Outbound Probe (8.8.8.8)",
                "Resolves Active Local IP Route",
                "Matches Scapy conf.route table",
                "Extracts WinPcap / Npcap Adapter GUID"
            ],
            "color": BLUE, "x": 3, "y": 30, "w": 21, "h": 52
        },
        {
            "step": "STEP 2: PROMISCUOUS CAPTURE",
            "title": "Scapy Sniffer Worker",
            "items": [
                "Non-blocking background thread",
                "Promiscuous Ethernet/Wi-Fi sniffing",
                "Filters IP Header (Layer 3)",
                "Thread-safe atomic packet counter"
            ],
            "color": TEAL, "x": 27, "y": 30, "w": 21, "h": 52
        },
        {
            "step": "STEP 3: WINDOW AGGREGATION",
            "title": "Temporal Window Emitter",
            "items": [
                "Periodic 5-second timer trigger",
                "Calculates arrival rate $r = C / 5.0$",
                "Appends to endpoint deque ($W=3$)",
                "Flushes atomic counter for next epoch"
            ],
            "color": INDIGO, "x": 51, "y": 30, "w": 21, "h": 52
        },
        {
            "step": "STEP 4: STATE & INFERENCE",
            "title": "Device Tracker Registry",
            "items": [
                "In-Memory Device Dictionary",
                "Extracts 3D vector [Mean, Med, Max]",
                "Log-transform & StandardScaler",
                r"Evaluates $f(z) \geq -0.4149$"
            ],
            "color": EMERALD, "x": 75, "y": 30, "w": 22, "h": 52
        }
    ]

    for blk in blocks:
        card = FancyBboxPatch((blk["x"], blk["y"]), blk["w"], blk["h"],
                              boxstyle="round,pad=0.5,rounding_size=1.2",
                              facecolor=BOX_BG, edgecolor=BOX_BORDER, linewidth=1.2)
        ax.add_patch(card)

        # Header
        hdr = FancyBboxPatch((blk["x"], blk["y"] + blk["h"] - 8.5), blk["w"], 8.5,
                             boxstyle="round,pad=0.3,rounding_size=1.0",
                             facecolor=blk["color"], edgecolor=blk["color"])
        ax.add_patch(hdr)
        ax.text(blk["x"] + blk["w"]/2, blk["y"] + blk["h"] - 3.2, blk["step"],
                ha='center', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF')
        ax.text(blk["x"] + blk["w"]/2, blk["y"] + blk["h"] - 6.4, blk["title"],
                ha='center', va='center', fontsize=7.2, color='#E2E8F0')

        # Items
        for idx, itm in enumerate(blk["items"]):
            cy = blk["y"] + blk["h"] - 14.5 - (idx * 8.5)
            ax.text(blk["x"] + 1.5, cy, "•", fontsize=10, color=blk["color"], fontweight='bold')
            ax.text(blk["x"] + 3.2, cy, itm, fontsize=7.2, color=TEXT_DARK, va='center')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="-|>", color=ARROW_COLOR, lw=2.0, mutation_scale=12)
    ax.annotate("", xy=(27, 56), xytext=(24, 56), arrowprops=arrow_props)
    ax.annotate("", xy=(51, 56), xytext=(48, 56), arrowprops=arrow_props)
    ax.annotate("", xy=(75, 56), xytext=(72, 56), arrowprops=arrow_props)

    # Bottom Architecture Specs
    bottom_box = FancyBboxPatch((3, 6), 94, 18, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0)
    ax.add_patch(bottom_box)
    ax.text(5, 19, "MULTI-THREADING ARCHITECTURAL SPECIFICATIONS:", fontsize=8.5, fontweight='bold', color=NAVY)
    ax.text(5, 13.5, "• Thread 1: Async Packet Capture (Scapy sniff with zero store buffer to eliminate memory leaks).", fontsize=7.5, color=TEXT_DARK)
    ax.text(5, 9.0, "• Thread 2: Sliding Window Aggregator & Rate Emitter (Emits rates every 5.0 seconds under threading.Lock).", fontsize=7.5, color=TEXT_DARK)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "figure_packet_sniffing_pipeline.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Sniffing pipeline diagram generated: {out_path}")

def generate_training_pipeline_diagram():
    """Generates Figure 5.1: Model Training, Stratification, and Calibration Pipeline."""
    fig, ax = plt.subplots(figsize=(12.0, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 95.5, "CICIoT2023 STRATIFIED TRAINING & OPTIMIZATION PIPELINE",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color=NAVY)
    ax.text(50, 91.0, "Outlier-Robust Log-Variance Stabilization, Dual Coordinate Descent, and Decision Threshold Tuning",
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color=TEXT_MUTED)

    # 4 Stages
    stages = [
        {
            "phase": "PHASE 1",
            "title": "Dataset Stratification",
            "items": [
                "46M CICIoT2023 flow records",
                "Group into 5-flow blocks",
                "Extract 3D rate feature vectors",
                "Balanced quota sampling (25,907/class)"
            ],
            "color": BLUE, "x": 3, "y": 30, "w": 21, "h": 52
        },
        {
            "phase": "PHASE 2",
            "title": "Variance Stabilization",
            "items": [
                r"Element-wise $z = \ln(x + 1)$",
                "Compresses 8 orders of magnitude",
                "Fit StandardScaler on Train ONLY",
                r"Freezes $(\mu, \sigma)$ to prevent leakage"
            ],
            "color": TEAL, "x": 27, "y": 30, "w": 21, "h": 52
        },
        {
            "phase": "PHASE 3",
            "title": "LinearSVC Optimization",
            "items": [
                "L2-regularized L2-loss LinearSVC",
                "LIBLINEAR dual coordinate solver",
                r"Asymmetric penalty: $w_0=5.0, w_1=1.0$",
                r"Primal parameters: $w \in \mathbb{R}^3, b \in \mathbb{R}$"
            ],
            "color": AMBER, "x": 51, "y": 30, "w": 21, "h": 52
        },
        {
            "phase": "PHASE 4",
            "title": "Threshold Calibration",
            "items": [
                r"Sweep $\tau$ across validation split",
                r"Target: Normal Specificity $\geq 90\%$",
                r"Optimal Threshold: $\tau = -0.4149$",
                "Reduces False Alarm Rate to 9.78%"
            ],
            "color": RED, "x": 75, "y": 30, "w": 22, "h": 52
        }
    ]

    for st in stages:
        card = FancyBboxPatch((st["x"], st["y"]), st["w"], st["h"],
                              boxstyle="round,pad=0.5,rounding_size=1.2",
                              facecolor=BOX_BG, edgecolor=BOX_BORDER, linewidth=1.2)
        ax.add_patch(card)

        hdr = FancyBboxPatch((st["x"], st["y"] + st["h"] - 8.5), st["w"], 8.5,
                             boxstyle="round,pad=0.3,rounding_size=1.0",
                             facecolor=st["color"], edgecolor=st["color"])
        ax.add_patch(hdr)
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 3.2, st["phase"],
                ha='center', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF')
        ax.text(st["x"] + st["w"]/2, st["y"] + st["h"] - 6.4, st["title"],
                ha='center', va='center', fontsize=7.2, color='#E2E8F0')

        for idx, itm in enumerate(st["items"]):
            cy = st["y"] + st["h"] - 14.5 - (idx * 8.5)
            ax.text(st["x"] + 1.5, cy, "•", fontsize=10, color=st["color"], fontweight='bold')
            ax.text(st["x"] + 3.2, cy, itm, fontsize=7.2, color=TEXT_DARK, va='center')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="-|>", color=ARROW_COLOR, lw=2.0, mutation_scale=12)
    ax.annotate("", xy=(27, 56), xytext=(24, 56), arrowprops=arrow_props)
    ax.annotate("", xy=(51, 56), xytext=(48, 56), arrowprops=arrow_props)
    ax.annotate("", xy=(75, 56), xytext=(72, 56), arrowprops=arrow_props)

    # Bottom Specs
    bottom_box = FancyBboxPatch((3, 6), 94, 18, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0)
    ax.add_patch(bottom_box)
    ax.text(5, 19, "PREVENTION OF METHODOLOGICAL EVALUATION BIAS:", fontsize=8.5, fontweight='bold', color=NAVY)
    ax.text(5, 13.5, "• Strict Split Independence: Scaling parameters fitted solely on Training partition to prevent data leakage.", fontsize=7.5, color=TEXT_DARK)
    ax.text(5, 9.0, "• Natural Imbalanced Test Set: Evaluated on 235,369 unaugmented records (97.65% attack, 2.35% normal).", fontsize=7.5, color=TEXT_DARK)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "figure_training_pipeline.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Training pipeline diagram generated: {out_path}")

def generate_fullstack_architecture_diagram():
    """Generates Figure 4.3: Full-Stack Edge Software Architecture & Telemetry Flow."""
    fig, ax = plt.subplots(figsize=(12.0, 6.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Title
    ax.text(50, 95.5, "GUARDNODE IOT: FULL-STACK EDGE SOFTWARE ARCHITECTURE",
            ha='center', va='center', fontsize=12.5, fontweight='bold', color=NAVY)
    ax.text(50, 91.0, "Promiscuous Engine, Asynchronous FastAPI Backend, In-Memory Registry, and React 19 Luminescent UI",
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color=TEXT_MUTED)

    # 3 Layers (Columns)
    layers = [
        {
            "layer": "EDGE MONITORING CORE",
            "title": "Low-Level Sniffing Engine",
            "items": [
                "Scapy Promiscuous Sniffer",
                "WinPcap / Npcap Kernel Driver",
                "Interface Auto-Discovery Manager",
                "Per-Endpoint Ring Buffer ($W=3$)",
                "Temporal Window Emitter (5s loop)"
            ],
            "color": BLUE, "x": 3, "y": 26, "w": 28, "h": 58
        },
        {
            "layer": "ASYNC BACKEND TIER",
            "title": "FastAPI & Inference Service",
            "items": [
                "FastAPI Asynchronous Web Server",
                "LinearSVC Engine ($w^T z + b$)",
                "Device Registry & Threat Scorer",
                "In-Memory Alert Circular Buffer",
                "RESTful APIs (/api/devices, /api/alerts)"
            ],
            "color": INDIGO, "x": 36, "y": 26, "w": 28, "h": 58
        },
        {
            "layer": "PRESENTATION TIER",
            "title": "Luminescent UI Dashboard",
            "items": [
                "React 19 Single Page Application",
                "Tailwind CSS Dark Theme (#090D16)",
                "Lucide Vector Iconography",
                "Recharts Real-Time Rate Streaming",
                "Subnet Device Inventory & Alerts Page"
            ],
            "color": EMERALD, "x": 69, "y": 26, "w": 28, "h": 58
        }
    ]

    for lyr in layers:
        card = FancyBboxPatch((lyr["x"], lyr["y"]), lyr["w"], lyr["h"],
                              boxstyle="round,pad=0.5,rounding_size=1.2",
                              facecolor=BOX_BG, edgecolor=BOX_BORDER, linewidth=1.2)
        ax.add_patch(card)

        hdr = FancyBboxPatch((lyr["x"], lyr["y"] + lyr["h"] - 8.5), lyr["w"], 8.5,
                             boxstyle="round,pad=0.3,rounding_size=1.0",
                             facecolor=lyr["color"], edgecolor=lyr["color"])
        ax.add_patch(hdr)
        ax.text(lyr["x"] + lyr["w"]/2, lyr["y"] + lyr["h"] - 3.2, lyr["layer"],
                ha='center', va='center', fontsize=7.8, fontweight='bold', color='#FFFFFF')
        ax.text(lyr["x"] + lyr["w"]/2, lyr["y"] + lyr["h"] - 6.4, lyr["title"],
                ha='center', va='center', fontsize=7.2, color='#E2E8F0')

        for idx, itm in enumerate(lyr["items"]):
            cy = lyr["y"] + lyr["h"] - 14.5 - (idx * 8.2)
            ax.text(lyr["x"] + 1.5, cy, "•", fontsize=10, color=lyr["color"], fontweight='bold')
            ax.text(lyr["x"] + 3.2, cy, itm, fontsize=7.2, color=TEXT_DARK, va='center')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="-|>", color=ARROW_COLOR, lw=2.2, mutation_scale=14)
    ax.annotate("", xy=(36, 55), xytext=(31, 55), arrowprops=arrow_props)
    ax.text(33.5, 57.5, "Rates", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=ARROW_COLOR)

    ax.annotate("", xy=(69, 55), xytext=(64, 55), arrowprops=arrow_props)
    ax.text(66.5, 57.5, "JSON Telemetry", ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=ARROW_COLOR)

    # Bottom Box
    bottom_box = FancyBboxPatch((3, 6), 94, 16, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor="#F1F5F9", edgecolor="#CBD5E1", linewidth=1.0)
    ax.add_patch(bottom_box)
    ax.text(5, 17, "COMMUNICATION PROTOCOLS & DATA EXCHANGE:", fontsize=8.5, fontweight='bold', color=NAVY)
    ax.text(5, 11.5, "• Edge-to-Backend: Thread-safe in-process function invocation and shared state dictionary.", fontsize=7.5, color=TEXT_DARK)
    ax.text(5, 7.5, "• Backend-to-Frontend: HTTP polling & JSON REST endpoints over loopback (127.0.0.1:8000).", fontsize=7.5, color=TEXT_DARK)

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "figure_fullstack_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close()
    print(f"Fullstack architecture diagram generated: {out_path}")

if __name__ == "__main__":
    generate_fsm_diagram()
    generate_sniffing_pipeline_diagram()
    generate_training_pipeline_diagram()
    generate_fullstack_architecture_diagram()
    print("All architectural diagrams generated successfully.")
