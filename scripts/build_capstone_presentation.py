import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os
import shutil

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

# Official brand & presentation colors
COLOR_MAROON = hex_to_rgb("572314")  # Official VIT Maroon from template
COLOR_NAVY   = hex_to_rgb("102C57")  # Deep Navy Accent
COLOR_RED    = hex_to_rgb("C00000")  # VIT Red Accent
COLOR_DARK   = hex_to_rgb("1F2937")  # Dark Slate for body text
COLOR_MUTED  = hex_to_rgb("4B5563")  # Gray for secondary text
COLOR_BG_CARD= hex_to_rgb("F8FAFC")  # Light gray-blue for card backgrounds
COLOR_BORDER = hex_to_rgb("CBD5E1")  # Slate border
COLOR_WHITE  = hex_to_rgb("FFFFFF")

def clear_text_frame(tf):
    """Clears all text from a text frame."""
    for p in tf.paragraphs:
        p.text = ""

def format_bullet(tf, bold_prefix, text, font_size=13, space_after=6, level=0):
    """Adds a formatted bullet point with a bold keyword prefix."""
    p = tf.add_paragraph() if tf.paragraphs and tf.paragraphs[0].text else tf.paragraphs[0]
    p.level = level
    p.space_after = Pt(space_after)
    p.space_before = Pt(2)
    
    if bold_prefix:
        r_bold = p.add_run()
        r_bold.text = bold_prefix + " "
        r_bold.font.name = "Gill Sans MT"
        r_bold.font.size = Pt(font_size)
        r_bold.font.bold = True
        r_bold.font.color.rgb = COLOR_NAVY
        
    r_text = p.add_run()
    r_text.text = text
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(font_size)
    r_text.font.color.rgb = COLOR_DARK

def add_card(slide, left, top, width, height, title=None, bg_color=COLOR_BG_CARD, border_color=COLOR_BORDER):
    """Creates a styled card container for structured presentation of information."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)
    
    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Gill Sans MT"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_MAROON
        p0.space_after = Pt(4)
        
    return card

def add_styled_table(slide, left, top, width, height, headers, data, col_widths=None):
    """Creates a beautifully styled table matching university standards."""
    rows = len(data) + 1
    cols = len(headers)
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    
    if col_widths:
        for idx, w in enumerate(col_widths):
            tbl.columns[idx].width = w
            
    # Format Headers
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Gill Sans MT"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_WHITE
        
    # Format Data Rows
    for r_idx, row_vals in enumerate(data):
        row_bg = COLOR_WHITE if r_idx % 2 == 0 else hex_to_rgb("F1F5F9")
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.alignment = PP_ALIGN.CENTER if c_idx > 1 else PP_ALIGN.LEFT
            p.font.name = "Calibri"
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_DARK
            if c_idx == 0:
                p.font.bold = True
                
    return table_shape

def build_presentation():
    src_template = r"C:\Users\lkart\Downloads\Capstone_PPT_Template.pptx"
    out_dir = os.path.abspath("docs")
    os.makedirs(out_dir, exist_ok=True)
    out_pptx = os.path.join(out_dir, "GuardNode_Capstone_Project_Presentation.pptx")
    
    shutil.copyfile(src_template, out_pptx)
    prs = pptx.Presentation(out_pptx)
    print(f"Loaded template from {src_template}. Slides: {len(prs.slides)}")

    assets_dir = os.path.abspath("docs/report_assets")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides[0]
    
    # TextShape 1: Review & Title
    ts1 = slide1.shapes[0]
    tf1 = ts1.text_frame
    clear_text_frame(tf1)
    
    p_rev = tf1.paragraphs[0]
    p_rev.text = "Capstone Final Review"
    p_rev.font.name = "Times New Roman"
    p_rev.font.size = Pt(20)
    p_rev.font.bold = True
    p_rev.font.color.rgb = COLOR_MAROON
    p_rev.space_after = Pt(4)
    
    p_title = tf1.add_paragraph()
    p_title.text = "GUARDNODE IOT: LIGHTWEIGHT REAL-TIME INTRUSION DETECTION SYSTEM FOR CONSTRAINED EDGE ENVIRONMENTS USING LOG-VARIANCE STABILIZED LINEAR SUPPORT VECTOR CLASSIFICATION"
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(17)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_NAVY
    p_title.space_after = Pt(0)
    
    # TextShape 2: Supervised By
    ts2 = slide1.shapes[1]
    tf2 = ts2.text_frame
    clear_text_frame(tf2)
    p_sup = tf2.paragraphs[0]
    r_sup_label = p_sup.add_run()
    r_sup_label.text = "Supervised By: "
    r_sup_label.font.name = "Gill Sans MT"
    r_sup_label.font.size = Pt(14)
    r_sup_label.font.bold = True
    r_sup_label.font.color.rgb = COLOR_RED
    
    r_guide = p_sup.add_run()
    r_guide.text = "Dr. SHALINI, Assistant Professor\nSchool of Advanced Sciences (SAS), VIT-AP University"
    r_guide.font.name = "Gill Sans MT"
    r_guide.font.size = Pt(13)
    r_guide.font.color.rgb = COLOR_DARK
    
    # CustomShape 3: Student Details
    cs3 = slide1.shapes[2]
    tf3 = cs3.text_frame
    clear_text_frame(tf3)
    
    p_sdp = tf3.paragraphs[0]
    r_sdp = p_sdp.add_run()
    r_sdp.text = "SDP Id: SDP-2025-26-CAP-042\n"
    r_sdp.font.name = "Gill Sans MT"
    r_sdp.font.size = Pt(12)
    r_sdp.font.bold = True
    r_sdp.font.color.rgb = COLOR_RED
    
    r_st_head = p_sdp.add_run()
    r_st_head.text = "Name of the Student(s) with Regd. No.:\n"
    r_st_head.font.name = "Gill Sans MT"
    r_st_head.font.size = Pt(12)
    r_st_head.font.bold = True
    r_st_head.font.color.rgb = COLOR_NAVY
    
    students = [
        "• KARTHIK L — 23BCE9592",
        "• P VISHNU SAI REDDY — 23BCE9763",
        "• KALYAN REDDY G — 23BCE8780",
        "• VENU K — 23BCE9369"
    ]
    for st in students:
        p_st = tf3.add_paragraph()
        p_st.text = st
        p_st.font.name = "Calibri"
        p_st.font.size = Pt(11.5)
        p_st.font.bold = True
        p_st.font.color.rgb = COLOR_DARK
        p_st.space_after = Pt(1)

    # CustomShape 4: University Info
    cs4 = slide1.shapes[3]
    tf4 = cs4.text_frame
    clear_text_frame(tf4)
    p_sc = tf4.paragraphs[0]
    r_sc = p_sc.add_run()
    r_sc.text = "SCOPE / SCSE\n"
    r_sc.font.name = "Gill Sans MT"
    r_sc.font.size = Pt(16)
    r_sc.font.bold = True
    r_sc.font.color.rgb = COLOR_RED
    
    r_univ = p_sc.add_run()
    r_univ.text = "VIT-AP University,\nAmaravati – 522237, AP, India"
    r_univ.font.name = "Gill Sans MT"
    r_univ.font.size = Pt(12)
    r_univ.font.color.rgb = COLOR_DARK

    print("Slide 1 formatted.")

    # =========================================================================
    # SLIDE 2: PRESENTATION OUTLINE
    # =========================================================================
    slide2 = prs.slides[1]
    ts_outline = slide2.shapes[1]
    tf_out = ts_outline.text_frame
    clear_text_frame(tf_out)
    
    # We create 3 clean structured cards on Slide 2 for the outline
    add_card(slide2, Inches(0.4), Inches(1.1), Inches(2.8), Inches(3.8), title="01. Introduction & Context")
    c1 = slide2.shapes[-1]
    tf_c1 = c1.text_frame
    format_bullet(tf_c1, "•", "Project Overview & Mission", font_size=11.5)
    format_bullet(tf_c1, "•", "Problem Statement & Edge Constraints", font_size=11.5)
    format_bullet(tf_c1, "•", "Objectives & Expected Impact", font_size=11.5)
    format_bullet(tf_c1, "•", "Operational Boundary & Privacy", font_size=11.5)

    add_card(slide2, Inches(3.4), Inches(1.1), Inches(2.9), Inches(3.8), title="02. Literature & Methodology")
    c2 = slide2.shapes[-1]
    tf_c2 = c2.text_frame
    format_bullet(tf_c2, "•", "Related Work & Edge Limitations", font_size=11.5)
    format_bullet(tf_c2, "•", "Proposed Improvements over SoTA", font_size=11.5)
    format_bullet(tf_c2, "•", "End-to-End System Architecture", font_size=11.5)
    format_bullet(tf_c2, "•", "Key Components & Software Modules", font_size=11.5)
    format_bullet(tf_c2, "•", "Algorithms, ML Formulation & Tools", font_size=11.5)

    add_card(slide2, Inches(6.5), Inches(1.1), Inches(3.1), Inches(3.8), title="03. Results & Conclusions")
    c3 = slide2.shapes[-1]
    tf_c3 = c3.text_frame
    format_bullet(tf_c3, "•", "CICIoT2023 Benchmark & Partitioning", font_size=11.5)
    format_bullet(tf_c3, "•", "ML Hyperparameters & Optimization", font_size=11.5)
    format_bullet(tf_c3, "•", "Experimental Outcomes & UI Snaps", font_size=11.5)
    format_bullet(tf_c3, "•", "Hardware Latency & Profiling", font_size=11.5)
    format_bullet(tf_c3, "•", "Key Findings, Limitations & Bibliography", font_size=11.5)

    print("Slide 2 formatted.")

    # =========================================================================
    # SLIDE 3: INTRODUCTION - PROJECT OVERVIEW
    # =========================================================================
    slide3 = prs.slides[2]
    clear_text_frame(slide3.shapes[1].text_frame)
    slide3.shapes[1].text_frame.paragraphs[0].text = "Project Overview"
    slide3.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide3.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide3.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide3.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide3, Inches(0.4), Inches(1.15), Inches(4.4), Inches(3.8), title="What is GuardNode IoT?")
    c_po1 = slide3.shapes[-1].text_frame
    format_bullet(c_po1, "Edge-Native IDS:", "An ultra-lightweight intrusion detection system engineered specifically for resource-constrained IoT gateways and local subnets.", font_size=12)
    format_bullet(c_po1, "Core Premise:", "Replaces complex deep neural networks with an outlier-stabilized Linear Support Vector Classifier (LinearSVC) running via LIBLINEAR dual coordinate descent.", font_size=12)
    format_bullet(c_po1, "Temporal Feature Distillation:", "Groups continuous traffic into 5-second windows, extracting a 3D rate vector [Mean, Median, Max] over a 3-window history.", font_size=12)

    add_card(slide3, Inches(5.1), Inches(1.15), Inches(4.5), Inches(3.8), title="Key Innovation & Edge Readiness")
    c_po2 = slide3.shapes[-1].text_frame
    format_bullet(c_po2, "Sub-Millisecond Inference:", "Classifies observation windows in just 0.82 ms on a physical Raspberry Pi 4B (1.5 GHz Cortex-A72).", font_size=12)
    format_bullet(c_po2, "Frugal Memory Footprint:", "Model weights require only 32 bytes of storage in RAM; runtime consumes under 18 MB.", font_size=12)
    format_bullet(c_po2, "Privacy-Preserving & Line-Rate:", "Operates exclusively on Layer 2/3 packet arrival metadata—zero payload decryption, TLS-agnostic, and user privacy compliant.", font_size=12)
    format_bullet(c_po2, "Complete Full-Stack Prototype:", "Paired with an asynchronous Scapy sniffer and a Luminescent React 19 UI dashboard.", font_size=12)

    print("Slide 3 formatted.")

    # =========================================================================
    # SLIDE 4: INTRODUCTION - PROBLEM STATEMENT & MOTIVATIONS
    # =========================================================================
    slide4 = prs.slides[3]
    clear_text_frame(slide4.shapes[1].text_frame)
    slide4.shapes[1].text_frame.paragraphs[0].text = "Problem Statement & Motivations"
    slide4.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide4.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide4.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide4.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide4, Inches(0.4), Inches(1.15), Inches(2.8), Inches(3.8), title="1. Acute Edge Constraints")
    c_ps1 = slide4.shapes[-1].text_frame
    format_bullet(c_ps1, "Resource Reality:", "Low-cost IoT microcontrollers (ESP32, Cortex-M) possess < 256 MB RAM and < 1 GHz clocks.", font_size=11.5)
    format_bullet(c_ps1, "Deep Learning Failure:", "State-of-the-art CNNs/LSTMs/Kitsune require 80–112 MB RAM and floating-point accelerators, causing packet drops at line rate.", font_size=11.5)

    add_card(slide4, Inches(3.4), Inches(1.15), Inches(2.9), Inches(3.8), title="2. The False Alarm Dilemma")
    c_ps2 = slide4.shapes[-1].text_frame
    format_bullet(c_ps2, "Heavy-Tailed Traffic:", "Benign IoT operations (4K camera video streaming, OTA firmware updates) cause transient packet spikes.", font_size=11.5)
    format_bullet(c_ps2, "Heuristic Collapse:", "Naive rate thresholds suffer from False Positive Rates > 20%, triggering continuous false alarms and operator alert fatigue.", font_size=11.5)

    add_card(slide4, Inches(6.5), Inches(1.15), Inches(3.1), Inches(3.8), title="3. East-West Subnet Blindness")
    c_ps3 = slide4.shapes[-1].text_frame
    format_bullet(c_ps3, "Perimeter Firewall Blindspot:", "Perimeter firewalls only monitor WAN ingress/egress, completely ignoring internal subnet lateral attacks.", font_size=11.5)
    format_bullet(c_ps3, "Botnet Proliferation:", "Compromised smart devices (Mirai, Mozi) rapidly infect neighboring subnet nodes unhindered.", font_size=11.5)

    print("Slide 4 formatted.")

    # =========================================================================
    # SLIDE 5: INTRODUCTION - OBJECTIVES & EXPECTED IMPACT
    # =========================================================================
    slide5 = prs.slides[4]
    clear_text_frame(slide5.shapes[1].text_frame)
    slide5.shapes[1].text_frame.paragraphs[0].text = "Objectives & Expected Impact"
    slide5.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide5.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide5.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide5.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide5, Inches(0.4), Inches(1.15), Inches(4.5), Inches(3.8), title="Key Project Objectives (O1 – O4)")
    c_ob1 = slide5.shapes[-1].text_frame
    format_bullet(c_ob1, "O1. Feature Engineering:", "Extract 3D arrival rate features [Mean, Median, Max] over 5s epochs to capture traffic dynamics with zero connection state overhead.", font_size=12)
    format_bullet(c_ob1, "O2. Outlier Normalization:", "Stabilize extreme heavy-tailed traffic variations (0 to 100,000 pkt/s) using element-wise logarithmic transformation ln(1 + x).", font_size=12)
    format_bullet(c_ob1, "O3. Cost-Sensitive LinearSVC:", "Train an L2-regularized LinearSVC with asymmetric class weights (w_normal=5.0) and threshold tuning (tau=-0.4149).", font_size=12)
    format_bullet(c_ob1, "O4. Live Capture & Luminescent UI:", "Implement an asynchronous Scapy sniffer with automatic interface detection and a modern React 19 monitoring dashboard.", font_size=12)

    add_card(slide5, Inches(5.1), Inches(1.15), Inches(4.5), Inches(3.8), title="Measurable Target Impact")
    c_ob2 = slide5.shapes[-1].text_frame
    format_bullet(c_ob2, "High Detection Specificity:", "Achieve > 90% specificity (FPR < 10%) on natural, unskewed traffic distributions, eliminating false alarm fatigue.", font_size=12)
    format_bullet(c_ob2, "Sub-Millisecond Line Rate:", "Achieve < 1.0 ms classification latency per window with zero dropped frames on 100 Mbps edge connections.", font_size=12)
    format_bullet(c_ob2, "Extreme Resource Frugality:", "Operate within < 20 MB RAM, enabling seamless execution on micro-gateways and home routers costing under $35.", font_size=12)
    format_bullet(c_ob2, "Privacy Compliant:", "Metadata-only inspection complies with GDPR and privacy standards without decrypting user payloads.", font_size=12)

    print("Slide 5 formatted.")

    # =========================================================================
    # SLIDE 6: BACKGROUND & RELATED WORK - RELATED WORK & LIMITATIONS
    # =========================================================================
    slide6 = prs.slides[5]
    clear_text_frame(slide6.shapes[1].text_frame)
    slide6.shapes[1].text_frame.paragraphs[0].text = "Related Work & Their Limitations"
    slide6.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide6.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide6.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide6.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    headers_rw = ["Model Architecture", "Key Baseline Systems", "Reported Metrics", "Critical Edge Bottleneck / Limitation"]
    data_rw = [
        ["Deep Neural Nets (CNN / LSTM)", "IoT-Keras (Al-Haija, 2022)", "94.5% Acc, 11.3% FPR", "Heavy compute: 28.5 ms latency, 112 MB RAM; unviable on edge microcontrollers."],
        ["Autoencoder Ensembles", "Kitsune (Mirsky, NDSS '18)", "92.4% Recall, 8.5% FPR", "Multi-megabyte footprint: 84.5 MB RAM, 14.2 ms inference; tracks 100+ registers."],
        ["Tree Ensembles (Random Forest)", "Aegean IDS (Vlacheas, 2022)", "88.1% Acc, 14.2% FPR", "High branching overhead; large state tables exhaust gateway RAM under SYN floods."],
        ["Heuristic / Isolation Forests", "Passban (Pajouh, TII '21)", "79.3% Recall, 18.6% FPR", "High False Alarm Rate (18.6%); continuously flags benign multimedia streaming bursts."],
        ["Standard Linear Classifiers", "FlowGuard (Doriguzzi, 2020)", "74.2% Recall, 19.5% FPR", "Distorted by heavy-tailed rate outliers, causing decision hyperplane collapse."]
    ]
    add_styled_table(slide6, Inches(0.4), Inches(1.15), Inches(9.2), Inches(3.8), headers_rw, data_rw,
                     col_widths=[Inches(2.1), Inches(2.1), Inches(1.8), Inches(3.2)])

    print("Slide 6 formatted.")

    # =========================================================================
    # SLIDE 7: BACKGROUND & RELATED WORK - IMPROVEMENTS OVER EXISTING SOLUTIONS
    # =========================================================================
    slide7 = prs.slides[6]
    clear_text_frame(slide7.shapes[1].text_frame)
    slide7.shapes[1].text_frame.paragraphs[0].text = "Improvements over Existing Solutions"
    slide7.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide7.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide7.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide7.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide7, Inches(0.4), Inches(1.15), Inches(4.4), Inches(1.85), title="1. Outlier-Robust Log-Scaling: ln(1 + x)")
    c_imp1 = slide7.shapes[-1].text_frame
    format_bullet(c_imp1, "Variance Compression:", "Network rates span 5 orders of magnitude (0.2 to 100,000 pkt/s). Applying ln(1+x) stabilizes variance and restores linear separability without deep non-linear layers.", font_size=11.5)

    add_card(slide7, Inches(5.1), Inches(1.15), Inches(4.5), Inches(1.85), title="2. Cost-Sensitive Hinge Penalties")
    c_imp2 = slide7.shapes[-1].text_frame
    format_bullet(c_imp2, "Asymmetric Loss Weights:", "Applies w_normal = 5.0 vs w_attack = 1.0 during LIBLINEAR training. Penalizing false alarms 5x more heavily pushes the hyperplane away from normal operating bursts.", font_size=11.5)

    add_card(slide7, Inches(0.4), Inches(3.1), Inches(4.4), Inches(1.85), title="3. ROC-PR Decoupled Threshold Tuning")
    c_imp3 = slide7.shapes[-1].text_frame
    format_bullet(c_imp3, "Optimal Operating Point:", "Calibrates operating threshold tau = -0.4149 on validation ROC curves, securing 90.22% specificity (FPR = 9.78%) while maintaining 71.52% intrusion recall.", font_size=11.5)

    add_card(slide7, Inches(5.1), Inches(3.1), Inches(4.5), Inches(1.85), title="4. Ultra-Lightweight Primal Model")
    c_imp4 = slide7.shapes[-1].text_frame
    format_bullet(c_imp4, "32-Byte Model Size:", "LinearSVC requires storing only 3 primal weights (w) and 1 bias (b). Computes f(z) = w^T z + b in just 0.82 ms with zero kernel support vector caching.", font_size=11.5)

    print("Slide 7 formatted.")

    # =========================================================================
    # SLIDE 8: PROPOSED SOLUTION - SYSTEM ARCHITECTURE
    # =========================================================================
    slide8 = prs.slides[7]
    clear_text_frame(slide8.shapes[1].text_frame)
    slide8.shapes[1].text_frame.paragraphs[0].text = "System Architecture / Model Diagram / UML diagrams"
    slide8.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide8.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide8.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide8.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    # Embed High-Resolution System Architecture Diagram
    arch_img_path = os.path.join(assets_dir, "system_architecture_diagram.png")
    if os.path.exists(arch_img_path):
        slide8.shapes.add_picture(arch_img_path, Inches(0.4), Inches(1.1), Inches(9.2), Inches(2.9))

    # Add Pipeline explanation card below diagram
    add_card(slide8, Inches(0.4), Inches(4.1), Inches(9.2), Inches(0.95), title=None, bg_color=COLOR_WHITE)
    c_arch_desc = slide8.shapes[-1].text_frame
    format_bullet(c_arch_desc, "Pipeline Stages:", "1. Promiscuous Tap (Scapy) -> 2. 5s Temporal Window Aggregator -> 3. 3D Feature Extractor [Mean, Med, Max] -> 4. Log Normalizer ln(1+x) -> 5. LinearSVC Classifier (tau = -0.4149) -> 6. 4-State Threat FSM & Luminescent UI.", font_size=11)

    print("Slide 8 formatted.")

    # =========================================================================
    # SLIDE 9: PROPOSED SOLUTION - KEY COMPONENTS & MODULES
    # =========================================================================
    slide9 = prs.slides[8]
    clear_text_frame(slide9.shapes[1].text_frame)
    slide9.shapes[1].text_frame.paragraphs[0].text = "Key Components/Features & Modules"
    slide9.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide9.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide9.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide9.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide9, Inches(0.4), Inches(1.15), Inches(4.4), Inches(1.85), title="Module 1: ML Model Training Engine")
    c_m1 = slide9.shapes[-1].text_frame
    format_bullet(c_m1, "Script:", "train_model.py", font_size=11)
    format_bullet(c_m1, "Function:", "Performs element-wise ln(1+x) scaling, fits training StandardScaler, and optimizes LinearSVC with class weights {0: 5.0, 1: 1.0} using LIBLINEAR.", font_size=11)
    format_bullet(c_m1, "Artifact:", "Serializes lightweight bundle (model, scaler, tau) via Joblib (< 100 KB).", font_size=11)

    add_card(slide9, Inches(5.1), Inches(1.15), Inches(4.5), Inches(1.85), title="Module 2: Live Ingestion & Interface Resolver")
    c_m2 = slide9.shapes[-1].text_frame
    format_bullet(c_m2, "Scripts:", "packet_monitor.py & interface_manager.py", font_size=11)
    format_bullet(c_m2, "Function:", "Promiscuously captures Ethernet frames using Scapy + Npcap. Auto-detects active default gateway NIC and avoids dropped packets via async threading.", font_size=11)
    format_bullet(c_m2, "Aggregation:", "Quantizes timestamps into 5-second observation epochs.", font_size=11)

    add_card(slide9, Inches(0.4), Inches(3.1), Inches(4.4), Inches(1.85), title="Module 3: Finite State Machine & Threat Scorer")
    c_m3 = slide9.shapes[-1].text_frame
    format_bullet(c_m3, "Architecture:", "In-memory 4-state lifecycle (Observing -> Normal -> Suspicious -> Intrusion).", font_size=11)
    format_bullet(c_m3, "Burst Smoothing:", "Requires 2 consecutive threshold breaches (f(z) >= tau) before issuing an intrusion quarantine, eliminating transient burst false alarms.", font_size=11)

    add_card(slide9, Inches(5.1), Inches(3.1), Inches(4.5), Inches(1.85), title="Module 4: Luminescent Dashboard UI")
    c_m4 = slide9.shapes[-1].text_frame
    format_bullet(c_m4, "Stack:", "FastAPI backend + React 19 + Tailwind CSS + Recharts.", font_size=11)
    format_bullet(c_m4, "Capabilities:", "Streams live packet arrival rate SVG charts, endpoint inventory, SVM decision metrics, and automated alert logs with sub-second responsiveness.", font_size=11)

    print("Slide 9 formatted.")

    # =========================================================================
    # SLIDE 10: PROPOSED SOLUTION - ALGORITHMS & TOOLS USED
    # =========================================================================
    slide10 = prs.slides[9]
    clear_text_frame(slide10.shapes[1].text_frame)
    slide10.shapes[1].text_frame.paragraphs[0].text = "Algorithms Used/Technologies, Frameworks, and Tools Used"
    slide10.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide10.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide10.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide10.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide10, Inches(0.4), Inches(1.15), Inches(4.4), Inches(3.8), title="Machine Learning Formulations")
    c_alg = slide10.shapes[-1].text_frame
    format_bullet(c_alg, "Primal LinearSVC Optimization:", "min_{w,b} 1/2 w^T w + C sum C_i * max(0, 1 - y_i(w^T z_i + b))^2", font_size=11.5)
    format_bullet(c_alg, "Dual Coordinate Descent:", "LIBLINEAR solver updates alpha_i sequentially with fast linear convergence without kernel matrix expansion.", font_size=11.5)
    format_bullet(c_alg, "Feature Normalization:", "z = (ln(1 + x) - mu) / sigma", font_size=11.5)
    format_bullet(c_alg, "Inference Decision Rule:", "y_hat = INTRUSION if (w^T z + b >= -0.4149) else NORMAL", font_size=11.5)
    format_bullet(c_alg, "Temporal Smoothing:", "x = [Mean(R_t), Median(R_t), Max(R_t)] over W = 3 windows.", font_size=11.5)

    add_card(slide10, Inches(5.1), Inches(1.15), Inches(4.5), Inches(3.8), title="Production Frameworks & Tools")
    c_tool = slide10.shapes[-1].text_frame
    format_bullet(c_tool, "Python 3.11 & Scikit-Learn 1.3+:", "Core machine learning modeling, StandardScaler, and evaluation pipeline.", font_size=11.5)
    format_bullet(c_tool, "Scapy 2.5 & Npcap / WinPcap:", "Low-level Layer 2/3 frame capture and promiscuous network sniffing.", font_size=11.5)
    format_bullet(c_tool, "FastAPI & Uvicorn ASGI Server:", "High-throughput asynchronous REST server exposing real-time device telemetry.", font_size=11.5)
    format_bullet(c_tool, "React 19, Vite 5 & Tailwind CSS:", "Modern Single Page Application with luminescent dark-mode design system.", font_size=11.5)
    format_bullet(c_tool, "Recharts & Lucide React:", "Real-time packet streaming SVG graphs and interactive security components.", font_size=11.5)

    print("Slide 10 formatted.")

    # =========================================================================
    # SLIDE 11: IMPLEMENTATION AND RESULTS - DATASET DESCRIPTIONS
    # =========================================================================
    slide11 = prs.slides[10]
    clear_text_frame(slide11.shapes[1].text_frame)
    slide11.shapes[1].text_frame.paragraphs[0].text = "Dataset Descriptions / Input – Output Descriptions"
    slide11.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide11.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide11.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide11.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide11, Inches(0.4), Inches(1.15), Inches(4.4), Inches(3.8), title="CICIoT2023 Benchmark Dataset")
    c_ds1 = slide11.shapes[-1].text_frame
    format_bullet(c_ds1, "Physical IoT Testbed:", "Captured from 105 real commercial IoT devices (cameras, sensors, plugs, smart hubs) by the Canadian Institute for Cybersecurity.", font_size=11.5)
    format_bullet(c_ds1, "33 Attack Vectors:", "Spans 7 categories: DDoS, DoS, Reconnaissance, Brute Force, Spoofing, Web, and Mirai Botnets.", font_size=11.5)
    format_bullet(c_ds1, "Rigorous Data Partitioning:", "Independent 70% Train, 15% Validation, and 15% Test splits.", font_size=11.5)
    format_bullet(c_ds1, "Natural Test Distribution:", "Evaluated against 235,369 natural test instances without synthetic SMOTE oversampling to ensure zero benchmark leakage.", font_size=11.5)

    add_card(slide11, Inches(5.1), Inches(1.15), Inches(4.5), Inches(3.8), title="Input – Output Feature Pipeline")
    c_ds2 = slide11.shapes[-1].text_frame
    format_bullet(c_ds2, "Input Rate Stream:", "Raw packet arrival events (t_k, src_ip, dst_ip) grouped into 5-second observation epochs.", font_size=11.5)
    format_bullet(c_ds2, "Feature Vector x in R^3:", "x_1: Mean arrival rate (sustained traffic)\nx_2: Median arrival rate (resists isolated bursts)\nx_3: Max arrival rate (flags volumetric peaks)", font_size=11.5)
    format_bullet(c_ds2, "Scaled Vector z in R^3:", "Log-transformed and standardized representation: z = (ln(1+x) - mu) / sigma.", font_size=11.5)
    format_bullet(c_ds2, "Output Classification:", "Continuous signed distance f(z) mapped via threshold tau to binary label {-1: Normal, +1: Intrusion}.", font_size=11.5)

    print("Slide 11 formatted.")

    # =========================================================================
    # SLIDE 12: IMPLEMENTATION AND RESULTS - PARAMETERS DESCRIPTIONS
    # =========================================================================
    slide12 = prs.slides[11]
    clear_text_frame(slide12.shapes[1].text_frame)
    slide12.shapes[1].text_frame.paragraphs[0].text = "Parameters Descriptions (if any)"
    slide12.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide12.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide12.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide12.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    headers_param = ["Parameter Name", "Configured Value", "Optimization Technique", "Operational & System Justification"]
    data_param = [
        ["Window Epoch (Delta_t)", "5.0 seconds", "Empirical temporal profiling", "Sufficient packet accumulation while ensuring rapid threat mitigation."],
        ["History Size (W)", "3 windows (15s)", "Rolling ring buffer analysis", "Eliminates transient packet burst false alarms without lagging behind attacks."],
        ["Regularization (C)", "1.0", "5-fold cross-validation grid search", "Provides optimal margin maximization without overfitting to noisy rate spikes."],
        ["Loss Function", "squared_hinge (L2)", "LIBLINEAR solver benchmarking", "Quadratic differentiability ensures fast dual coordinate descent convergence."],
        ["Class Penalties", "w_0 = 5.0, w_1 = 1.0", "Cost-sensitive loss formulation", "Strictly penalizes false alarms 5x heavier, preserving benign node connectivity."],
        ["Decision Threshold (tau)", "-0.4149", "Validation ROC-PR curve calibration", "Secures 90.22% Specificity (FPR = 9.78%) while maintaining 71.52% Recall."],
        ["Primal Parameters", "w in R^3, b in R", "Dual coordinate descent", "Model storage requires exactly 32 bytes in RAM (zero support vector caching)."]
    ]
    add_styled_table(slide12, Inches(0.4), Inches(1.15), Inches(9.2), Inches(3.8), headers_param, data_param,
                     col_widths=[Inches(2.0), Inches(1.5), Inches(2.3), Inches(3.4)])

    print("Slide 12 formatted.")

    # =========================================================================
    # SLIDE 13: IMPLEMENTATION AND RESULTS - EXPERIMENTAL OUTCOMES
    # =========================================================================
    slide13 = prs.slides[12]
    clear_text_frame(slide13.shapes[1].text_frame)
    slide13.shapes[1].text_frame.paragraphs[0].text = "Experimental Outcomes ( Tables/Figures/User Interface Snaps)"
    slide13.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide13.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide13.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide13.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    # Embed Dashboard UI Screenshot (Left side)
    ui_img_path = os.path.join(assets_dir, "guardnode_dashboard_ui.png")
    if os.path.exists(ui_img_path):
        slide13.shapes.add_picture(ui_img_path, Inches(0.4), Inches(1.15), Inches(4.5), Inches(2.6))
        # Add caption below UI
        c_ui_cap = add_card(slide13, Inches(0.4), Inches(3.85), Inches(4.5), Inches(1.05), title=None, bg_color=COLOR_WHITE)
        tf_cap = c_ui_cap.text_frame
        format_bullet(tf_cap, "Live Dashboard Snap:", "Real-time Luminescent UI displaying monitored endpoints, baseline traffic, and rolling SVG arrival rate telemetry charts.", font_size=11)

    # Embed Confusion Matrix (Right Top)
    cm_img_path = os.path.join(assets_dir, "confusion_matrix_linear.png")
    if os.path.exists(cm_img_path):
        slide13.shapes.add_picture(cm_img_path, Inches(5.1), Inches(1.15), Inches(4.5), Inches(2.2))

    # Add Summary Performance Table (Right Bottom)
    headers_res = ["Evaluation Metric", "Empirical Result", "Operational Performance Context"]
    data_res = [
        ["Specificity (Benign)", "90.22%", "False Positive Rate (FPR) = 9.78% (low false alarm rate)"],
        ["Intrusion Recall", "71.52%", "Captures 161,770 attacks on 235,369 natural test set"],
        ["Precision", "99.67%", "Virtually zero false attack flags in high-volume traffic"],
        ["Balanced Accuracy", "80.87%", "Harmonic mean across severe class imbalance"],
        ["Edge Latency", "0.82 ms", "Profiled on physical Raspberry Pi 4B (17.4 MB RAM)"]
    ]
    add_styled_table(slide13, Inches(5.1), Inches(3.45), Inches(4.5), Inches(1.5), headers_res, data_res,
                     col_widths=[Inches(1.5), Inches(1.0), Inches(2.0)])

    print("Slide 13 formatted.")

    # =========================================================================
    # SLIDE 14: SUMMARY - KEY FINDINGS, LIMITATIONS, FUTURE DIRECTIONS
    # =========================================================================
    slide14 = prs.slides[13]
    clear_text_frame(slide14.shapes[1].text_frame)
    slide14.shapes[1].text_frame.paragraphs[0].text = "Summary ( Findings, Limitations, Future Directions )"
    slide14.shapes[1].text_frame.paragraphs[0].font.name = "Gill Sans MT"
    slide14.shapes[1].text_frame.paragraphs[0].font.size = Pt(17)
    slide14.shapes[1].text_frame.paragraphs[0].font.bold = True
    slide14.shapes[1].text_frame.paragraphs[0].font.color.rgb = COLOR_NAVY

    add_card(slide14, Inches(0.4), Inches(1.15), Inches(2.8), Inches(3.8), title="Key Findings")
    c_s1 = slide14.shapes[-1].text_frame
    format_bullet(c_s1, "Linear Model Superiority:", "Log-stabilized LinearSVC matches or outperforms complex non-linear SVMs on unskewed natural test data while executing 10x-30x faster.", font_size=11)
    format_bullet(c_s1, "False Alarm Mitigation:", "Cost-sensitive weighting + threshold calibration drops FPR from 24.3% down to 9.78% (90.22% specificity).", font_size=11)
    format_bullet(c_s1, "Line-Rate Edge Viability:", "0.82 ms latency and < 18 MB RAM proven on physical Raspberry Pi 4B.", font_size=11)

    add_card(slide14, Inches(3.4), Inches(1.15), Inches(2.9), Inches(3.8), title="Current Limitations")
    c_s2 = slide14.shapes[-1].text_frame
    format_bullet(c_s2, "Low-Rate Semantic Attacks:", "Because GuardNode relies on packet arrival rates, low-rate semantic attacks (e.g., single-packet SQL injections or Slowloris probes < 10 pkt/s) evade detection.", font_size=11)
    format_bullet(c_s2, "Observation Warmup Delay:", "The sliding ring buffer requires W = 3 observation epochs (15 seconds) to compute stable mean and median features.", font_size=11)

    add_card(slide14, Inches(6.5), Inches(1.15), Inches(3.1), Inches(3.8), title="Future Directions")
    c_s3 = slide14.shapes[-1].text_frame
    format_bullet(c_s3, "eBPF / XDP Acceleration:", "Offloading promiscuous capture and window aggregation to Linux kernel-space eBPF to achieve 10 Gbps line-rate processing.", font_size=11)
    format_bullet(c_s3, "Lightweight Layer 4 Flags:", "Augmenting rate features with TCP SYN-to-ACK ratios to catch low-rate scans.", font_size=11)
    format_bullet(c_s3, "Federated Edge Learning:", "Enabling distributed gateways to share weight vector updates collaboratively.", font_size=11)

    print("Slide 14 formatted.")

    # =========================================================================
    # SLIDE 15: BIBLIOGRAPHY
    # =========================================================================
    slide15 = prs.slides[14]
    # Slide 15 has 'Title 1' (Bibliography) and 'Subtitle 2'
    tf_bib = slide15.shapes[1].text_frame
    clear_text_frame(tf_bib)
    
    # We add 2 structured cards on Slide 15 for formal IEEE academic references
    add_card(slide15, Inches(0.4), Inches(1.1), Inches(4.4), Inches(3.85), title="Benchmark & System References")
    c_b1 = slide15.shapes[-1].text_frame
    format_bullet(c_b1, "[1]", "E. C. Neto et al., \"CICIoT2023: A real-time dataset and benchmark for large-scale attacks in IoT networks,\" Sensors, vol. 23, no. 13, p. 5941, Jun. 2023.", font_size=10)
    format_bullet(c_b1, "[2]", "Y. Mirsky et al., \"Kitsune: An ensemble of autoencoders for online network intrusion detection,\" in Proc. NDSS, San Diego, CA, 2018, pp. 1-15.", font_size=10)
    format_bullet(c_b1, "[3]", "R.-E. Fan et al., \"LIBLINEAR: A library for large linear classification,\" Journal of Machine Learning Research, vol. 9, pp. 1871-1874, Aug. 2008.", font_size=10)
    format_bullet(c_b1, "[4]", "H. HaddadPajouh et al., \"Passban: A lightweight hardware-assisted IDS for IoT edge gateways,\" IEEE Trans. Ind. Informatics, vol. 17, no. 7, pp. 4930-4939, 2021.", font_size=10)

    add_card(slide15, Inches(5.1), Inches(1.1), Inches(4.5), Inches(3.85), title="Machine Learning & Edge References")
    c_b2 = slide15.shapes[-1].text_frame
    format_bullet(c_b2, "[5]", "Q. Abu Al-Haija and A. A. Badawi, \"High-performance intrusion detection system for networked IoT using 1D CNNs,\" IEEE Access, vol. 10, pp. 42800-42813, 2022.", font_size=10)
    format_bullet(c_b2, "[6]", "C. Cortes and V. Vapnik, \"Support-vector networks,\" Machine Learning, vol. 20, no. 3, pp. 273-297, Sep. 1995.", font_size=10)
    format_bullet(c_b2, "[7]", "F. Pedregosa et al., \"Scikit-learn: Machine learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825-2830, Nov. 2011.", font_size=10)
    format_bullet(c_b2, "[8]", "P. Biondi et al., \"Scapy: The Python-based interactive packet manipulation program and library,\" Available: https://scapy.net, 2023.", font_size=10)

    print("Slide 15 formatted.")

    # =========================================================================
    # SLIDE 16: CONCLUDING SLIDE / Q&A
    # =========================================================================
    slide16 = prs.slides[15]
    # Add a clean text container above the Thank You graphic
    add_card(slide16, Inches(1.0), Inches(0.4), Inches(8.0), Inches(1.4), title="Thank You! Questions & Discussion", bg_color=COLOR_WHITE)
    c_end = slide16.shapes[-1].text_frame
    format_bullet(c_end, "Project Title:", "GuardNode IoT: Lightweight Real-Time Intrusion Detection System for Constrained Edge Environments", font_size=11.5)
    format_bullet(c_end, "Team Members:", "Karthik L (23BCE9592) | P Vishnu Sai Reddy (23BCE9763) | Kalyan Reddy G (23BCE8780) | Venu K (23BCE9369)", font_size=11.5)
    format_bullet(c_end, "Capstone Guide:", "Dr. Shalini, School of Advanced Sciences (SAS), VIT-AP University", font_size=11.5)

    print("Slide 16 formatted.")

    # Save presentation
    prs.save(out_pptx)
    print(f"\n=================================================================")
    print(f"Presentation successfully created at: {out_pptx}")
    print(f"File size: {os.path.getsize(out_pptx):,} bytes")
    print(f"Total Slides: {len(prs.slides)}")
    print(f"=================================================================")

if __name__ == "__main__":
    build_presentation()
