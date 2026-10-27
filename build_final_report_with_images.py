# -*- coding: utf-8 -*-
"""
build_final_report_with_images.py
-----------------------------------------------------------------
Comprehensive Academic Project Report Generator for:
MAHARAJA'S KITCHEN - RESTAURANT FOOD BILLING & POS MANAGEMENT SYSTEM
University of Mumbai - B.Sc. (Computer Science) - Semester V
Academic Year: 2026 - 2027
Submitted by: AMOL YEDKE

Embeds:
- All 12 PlantUML diagrams from C:\Project Sem 5\diagrams\ (or C:\diagram\)
- All 5 High-Res UI Screenshots from C:\Project Sem 5\screenshots\
- Dynamic Live QR Code from C:\Project Sem 5\static\img\live_qr.png
- Complete academic structure: Cover, Certificate, Declaration, Abstract,
  Acknowledgement, Index, List of Figures, List of Tables, and Chapters 1 to 16.
-----------------------------------------------------------------
"""

import os
from PIL import Image
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report():
    print("Initializing document...")
    doc = docx.Document()

    # Base page settings - A4 with academic margins
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)   # Binding margin
        section.right_margin = Inches(1.0)

        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Maharaja's Kitchen POS | University of Mumbai BSc (CS) Sem V")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science - Academic Project Report (2026-2027)")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(0x77, 0x77, 0x77)

    # Palette
    NAVY = RGBColor(0x1E, 0x3A, 0x8A)      # Main headings
    STEEL = RGBColor(0x1E, 0x40, 0xAF)     # Subheadings
    SLATE = RGBColor(0x1F, 0x29, 0x37)     # Body headings
    TEXT_COLOR = RGBColor(0x11, 0x18, 0x27)# Body text
    MUTED = RGBColor(0x4B, 0x55, 0x63)     # Captions / Secondary

    # -------------------------------------------------------------
    # Helper Functions
    # -------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = NAVY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = STEEL
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = SLATE
        return p

    def add_p(text, bold_prefix=None, space_after=6, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Times New Roman"
            brun.font.size = Pt(11)
            brun.font.bold = True
            brun.font.color.rgb = TEXT_COLOR
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.italic = italic
        run.font.color.rgb = TEXT_COLOR
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            brun = p.add_run(bold_prefix)
            brun.font.name = "Times New Roman"
            brun.font.size = Pt(11)
            brun.font.bold = True
            brun.font.color.rgb = TEXT_COLOR
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_COLOR
        return p

    def add_image_scaled(img_path, caption_title, fig_label, max_w=5.8, max_h=5.4, page_break_after=False):
        if not os.path.exists(img_path):
            print(f"WARNING: Image not found: {img_path}")
            p = doc.add_paragraph(f"[Image Missing: {img_path}]")
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            return

        w_px, h_px = Image.open(img_path).size
        aspect = h_px / float(w_px)

        target_w = max_w
        target_h = target_w * aspect
        if target_h > max_h:
            target_h = max_h
            target_w = target_h / aspect

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(target_w), height=Inches(target_h))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        
        c_label = p_cap.add_run(f"{fig_label}: ")
        c_label.font.name = "Times New Roman"
        c_label.font.size = Pt(10)
        c_label.font.bold = True
        c_label.font.color.rgb = NAVY

        c_text = p_cap.add_run(caption_title)
        c_text.font.name = "Times New Roman"
        c_text.font.size = Pt(10)
        c_text.font.italic = True
        c_text.font.color.rgb = MUTED

        if page_break_after:
            doc.add_page_break()

    def add_table_styled(headers, rows, col_widths=None):
        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False

        # Header Row
        hdr_row = table.rows[0]
        tblPr = table._tbl.tblPr
        tblCellMar = parse_xml(f'<w:tblCellMar {nsdecls("w")}><w:top w:w="120" w:type="dxa"/><w:bottom w:w="120" w:type="dxa"/><w:left w:w="160" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tblCellMar>')
        tblPr.append(tblCellMar)

        for col_idx, header_text in enumerate(headers):
            cell = hdr_row.cells[col_idx]
            cell.text = header_text
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E3A8A"/>')
            cell._tc.get_or_add_tcPr().append(shd)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(10)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for row_idx, row_data in enumerate(rows):
            row = table.rows[row_idx + 1]
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                cell = row.cells[col_idx]
                cell.text = str(cell_value)
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_color}"/>')
                cell._tc.get_or_add_tcPr().append(shd)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = TEXT_COLOR

        # Set borders
        tblBorders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/><w:insideV w:val="none"/><w:left w:val="none"/><w:right w:val="none"/></w:tblBorders>')
        table._tbl.tblPr.append(tblBorders)

        # Column widths
        if col_widths:
            for row in table.rows:
                for idx, w in enumerate(col_widths):
                    row.cells[idx].width = Inches(w)

        # Add spacing after table
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(2)
        sp.paragraph_format.space_after = Pt(6)

    # Paths
    diag_dir = r"C:\Project Sem 5\diagrams"
    screen_dir = r"C:\Project Sem 5\screenshots"
    qr_path = r"C:\Project Sem 5\static\img\live_qr.png"

    # =============================================================
    # 1. TITLE / COVER PAGE
    # =============================================================
    print("Writing Title / Cover Page...")
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(12)
    p_uni.paragraph_format.space_after = Pt(6)
    r_uni = p_uni.add_run("UNIVERSITY OF MUMBAI\n")
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(16)
    r_uni.font.bold = True
    r_uni.font.color.rgb = NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("A Project Report on\n")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("MAHARAJA'S KITCHEN\n")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    r_subtitle = p_title.add_run("MULTI-BRANCH CLOUD RESTAURANT POS & REAL-TIME BILLING MANAGEMENT SYSTEM")
    r_subtitle.font.name = "Times New Roman"
    r_subtitle.font.size = Pt(14)
    r_subtitle.font.bold = True
    r_subtitle.font.color.rgb = STEEL

    p_degree = doc.add_paragraph()
    p_degree.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_degree.paragraph_format.space_before = Pt(24)
    p_degree.paragraph_format.space_after = Pt(4)
    r_deg = p_degree.add_run("Submitted in partial fulfillment of the requirements for the Degree of\n")
    r_deg.font.name = "Times New Roman"
    r_deg.font.size = Pt(11)
    r_deg.font.italic = True

    r_deg2 = p_degree.add_run("BACHELOR OF SCIENCE (COMPUTER SCIENCE)\n")
    r_deg2.font.name = "Times New Roman"
    r_deg2.font.size = Pt(14)
    r_deg2.font.bold = True
    r_deg2.font.color.rgb = SLATE

    r_sem = p_degree.add_run("Semester - V\nAcademic Year: 2026 - 2027")
    r_sem.font.name = "Times New Roman"
    r_sem.font.size = Pt(12)
    r_sem.font.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(26)
    p_by.paragraph_format.space_after = Pt(4)
    r_by = p_by.add_run("Submitted By\n")
    r_by.font.name = "Times New Roman"
    r_by.font.size = Pt(11)
    r_by.font.italic = True
    r_name = p_by.add_run("AMOL YEDKE\n")
    r_name.font.name = "Times New Roman"
    r_name.font.size = Pt(14)
    r_name.font.bold = True
    r_name.font.color.rgb = NAVY
    r_roll = p_by.add_run("Seat No. / Roll No: [Your University Roll Number]")
    r_roll.font.name = "Times New Roman"
    r_roll.font.size = Pt(11)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(20)
    p_guide.paragraph_format.space_after = Pt(4)
    r_g1 = p_guide.add_run("Under the Esteemed Guidance of\n")
    r_g1.font.name = "Times New Roman"
    r_g1.font.size = Pt(11)
    r_g1.font.italic = True
    r_g2 = p_guide.add_run("Department Faculty Guide & Head of Department\n")
    r_g2.font.name = "Times New Roman"
    r_g2.font.size = Pt(12)
    r_g2.font.bold = True

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(24)
    p_dept.paragraph_format.space_after = Pt(2)
    r_d1 = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE\n")
    r_d1.font.name = "Times New Roman"
    r_d1.font.size = Pt(13)
    r_d1.font.bold = True
    r_d1.font.color.rgb = NAVY
    r_d2 = p_dept.add_run("Shri Ram College of Commerce / Affiliated College of Mumbai University\n")
    r_d2.font.name = "Times New Roman"
    r_d2.font.size = Pt(11.5)
    r_d2.font.bold = True
    r_d3 = p_dept.add_run("Mumbai, Maharashtra, India - 400 001")
    r_d3.font.name = "Times New Roman"
    r_d3.font.size = Pt(11)

    doc.add_page_break()

    # =============================================================
    # 2. CERTIFICATE OF AUTHENTICITY
    # =============================================================
    print("Writing Certificate...")
    add_h1("CERTIFICATE OF AUTHENTICITY")
    add_p("This is to certify that the project report entitled \"MAHARAJA'S KITCHEN - MULTI-BRANCH CLOUD RESTAURANT POS & REAL-TIME BILLING MANAGEMENT SYSTEM\" is a bonafide academic work carried out by Mr. AMOL YEDKE in partial fulfillment of the requirements for the award of the Degree of Bachelor of Science (Computer Science) - Semester V of the University of Mumbai during the Academic Year 2026 - 2027.")
    add_p("The project represents original, self-engineered work completed under our supervision. The candidate has satisfied all academic standards, laboratory requirements, system design milestones, and testing mandates stipulated by the University of Mumbai curriculum.")
    add_p("It is further certified that this project report has not formed the basis for the award of any other degree, diploma, fellowship, or similar title at any other university or academic institution.")

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    # Signature Table
    sig_headers = ["Project Guide", "Head of Department", "Principal"]
    sig_rows = [
        ["_________________________\n(Faculty Guide Signature)\nDate: ____________",
         "_________________________\n(Head of Department)\nDate: ____________",
         "_________________________\n(College Principal & Seal)\nDate: ____________"],
        ["Internal Examiner Signature\nDate: ____________",
         "College Stamp / Seal\nPlace: Mumbai",
         "External Examiner Signature\nDate: ____________"]
    ]
    add_table_styled(sig_headers, sig_rows, [2.0, 2.0, 2.0])

    doc.add_page_break()

    # =============================================================
    # 3. DECLARATION BY STUDENT
    # =============================================================
    print("Writing Declaration...")
    add_h1("DECLARATION BY STUDENT")
    add_p("I, AMOL YEDKE, student of Bachelor of Science (Computer Science) Semester V, hereby declare that the project titled \"MAHARAJA'S KITCHEN - MULTI-BRANCH CLOUD RESTAURANT POS & REAL-TIME BILLING MANAGEMENT SYSTEM\" submitted to the University of Mumbai, is an authentic record of my own research and development work.")
    add_p("I confirm that the software implementation, relational database design, user interface architecture, PlantUML diagrams, and documentation were created by me under the supervision and guidance of our faculty members. Any material, frameworks, or open-source libraries referenced in this work have been duly acknowledged and cited.")
    add_p("I further state that this work has not been previously submitted in part or full to any other University or Examination Body for the award of any academic credential.")

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.paragraph_format.space_before = Pt(48)
    p_sig.paragraph_format.space_after = Pt(4)
    r_s1 = p_sig.add_run("_____________________________________\n")
    r_s2 = p_sig.add_run("AMOL YEDKE\n")
    r_s2.font.bold = True
    r_s3 = p_sig.add_run("B.Sc. (Computer Science) - Semester V\nRoll No: [Your Roll Number]\nPlace: Mumbai\nDate: 27th October 2026")
    r_s1.font.name = r_s2.font.name = r_s3.font.name = "Times New Roman"

    doc.add_page_break()

    # =============================================================
    # 4. ABSTRACT
    # =============================================================
    print("Writing Abstract...")
    add_h1("ABSTRACT")
    add_p("Maharaja's Kitchen is a high-performance, real-time web-based Point-of-Sale (POS) and Restaurant Food Billing Management System designed to digitise, accelerate, and automate restaurant front-desk and back-office operations. Built using a Python Flask WSGI backend, SQLite3 relational database, responsive Tailwind CSS frontend, and Chart.js analytics engine, the application eliminates calculation errors, paper order ticket delays, and revenue leakage typical of conventional handwritten restaurant billing.")
    add_p("The system provides dual role-based access tiers: an administrative portal and a cashier POS terminal. Key capabilities include: an intuitive touch-friendly billing grid supporting both Dine-In (with visual table allocation for Tables 1-20) and Delivery (with automated delivery surcharge and mandatory 10-digit phone verification); instant GST tax calculation (2.5% CGST + 2.5% SGST); a dynamic cash tender calculator with smart exact-bill suggestion chips; thermal receipt printing and offline PDF downloads; real-time sales trend analytics with interactive monthly and payment-mode doughnut charts; and complete CRUD administration for menu items (with automated Google image cleaner and local photo uploads), restaurant staff (with strict 10-digit phone and email validation), and multi-location branch allocations.")
    add_p("For external evaluation and mobile accessibility, the system is deployed live over an encrypted Cloudflare Tunnel (HTTPS), allowing seamless multi-device operation across smartphones, tablets, and desktop terminals without port forwarding. The project represents a production-grade demonstration of modern full-stack web engineering, secure relational data modeling, and robust user interface design.")

    doc.add_page_break()

    # =============================================================
    # 5. ACKNOWLEDGEMENT
    # =============================================================
    print("Writing Acknowledgement...")
    add_h1("ACKNOWLEDGEMENT")
    add_p("I express my profound gratitude to my project guide and the respected faculty members of the Department of Computer Science for their continuous encouragement, valuable insights, and constructive criticism throughout the design, implementation, and testing of Maharaja's Kitchen.")
    add_p("I am sincerely grateful to our respected Principal for providing the necessary laboratory infrastructure, high-speed computational resources, and a conducive environment that made the realization of this system possible.")
    add_p("A special word of appreciation goes to the global open-source developer communities behind Python, Flask, Tailwind CSS, SQLite, Chart.js, and Cloudflare, whose exemplary frameworks, documentation, and tooling enabled the realization of a production-standard solution.")
    add_p("Finally, I express my deepest appreciation to my parents, family, and peers for their unyielding patience, moral support, and motivation during the intensive development and documentation phase of this project.")

    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ack.paragraph_format.space_before = Pt(36)
    r_a = p_ack.add_run("Amol Yedke\nB.Sc. (Computer Science) - Semester V\nUniversity of Mumbai")
    r_a.font.name = "Times New Roman"
    r_a.font.bold = True

    doc.add_page_break()

    # =============================================================
    # 6. TABLE OF CONTENTS / INDEX
    # =============================================================
    print("Writing Table of Contents...")
    add_h1("TABLE OF CONTENTS / INDEX")
    toc_headers = ["Sr. No.", "Chapter / Section Title", "Page Range"]
    toc_rows = [
        ["—", "Certificate of Authenticity", "ii"],
        ["—", "Declaration by Student", "iii"],
        ["—", "Abstract / Executive Summary", "iv"],
        ["—", "Acknowledgement", "v"],
        ["—", "List of Figures", "vii"],
        ["—", "List of Tables", "viii"],
        ["1", "Chapter 1: Introduction (Background, Objectives, Scope, Tech Stack)", "1 - 4"],
        ["2", "Chapter 2: Project Overview & System Features (Modules, Innovations)", "5 - 8"],
        ["3", "Chapter 3: Feasibility Report (Technical, Economic, Operational, Schedule)", "9 - 11"],
        ["4", "Chapter 4: Requirement Specification (SRS, Functional, Non-Functional)", "12 - 16"],
        ["5", "Chapter 5: System Design (3-Tier Architecture, Input/Output, Security)", "17 - 21"],
        ["6", "Chapter 6: Database Design & Implementation (Schema, Data Dictionary, Normalization)", "22 - 28"],
        ["7", "Chapter 7: System Analysis & Comparative Study (Manual vs Automated, SWOT)", "29 - 33"],
        ["8", "Chapter 8: System Diagrams (All 12 PlantUML Architectural & UML Models)", "34 - 49"],
        ["9", "Chapter 9: Screen Outputs & User Interface Walkthrough (Screenshots & Live QR)", "50 - 58"],
        ["10", "Chapter 10: System Testing & Quality Assurance (Methodology, 20 Test Cases Table)", "59 - 65"],
        ["11", "Chapter 11: Deployment & Cloud Infrastructure (Cloudflare Tunnel, WSGI)", "66 - 69"],
        ["12", "Chapter 12: Core Source Code Listings (Flask API, POS JavaScript)", "70 - 75"],
        ["13", "Chapter 13: Project Schedule & Execution Timeline (19-Week Milestones)", "76 - 77"],
        ["14", "Chapter 14: Conclusion", "78 - 79"],
        ["15", "Chapter 15: Future Enhancements", "80 - 81"],
        ["16", "Chapter 16: Bibliography & References", "82 - 83"],
    ]
    add_table_styled(toc_headers, toc_rows, [0.8, 4.2, 1.0])

    doc.add_page_break()

    # =============================================================
    # 7. LIST OF FIGURES & LIST OF TABLES
    # =============================================================
    print("Writing List of Figures & Tables...")
    add_h1("LIST OF FIGURES")
    fig_headers = ["Figure No.", "Figure Title & Description", "Page"]
    fig_rows = [
        ["Figure 8.1", "Maharaja's Kitchen Object-Oriented Class Hierarchy Diagram", "35"],
        ["Figure 8.2", "Runtime Object Instance Snapshot Diagram (Active Dine-In Order #101)", "36"],
        ["Figure 8.3", "Entity-Relationship (ER) Schema with Relational Cardinalities", "37"],
        ["Figure 8.4", "System Use Case Diagram (Cashier, Admin, Customer Interactions)", "38"],
        ["Figure 8.5", "End-to-End Operational Billing Activity Workflow", "39"],
        ["Figure 8.6", "Finite State Machine Order Lifecycle Diagram", "41"],
        ["Figure 8.7", "Three-Tier Modular Component Architecture Diagram", "43"],
        ["Figure 8.8", "Physical Node Deployment & Cloudflare Tunnel Edge Topology", "44"],
        ["Figure 8.9", "Python Flask & Frontend Asset Package Architecture", "45"],
        ["Figure 8.10", "Data Flow Diagram (DFD Level 0 - Context Level Diagram)", "46"],
        ["Figure 8.11", "Data Flow Diagram (DFD Level 1 - Detailed Functional Decomposition)", "47"],
        ["Figure 8.12", "Synchronous Checkout & Payment Processing Sequence Diagram", "48"],
        ["Figure 9.1", "Real-Time Point-of-Sale (POS) Billing Interface & Cart Management", "51"],
        ["Figure 9.2", "Executive Sales Analytics Dashboard with Center-Text Doughnut Chart", "52"],
        ["Figure 9.3", "Staff Roster Management & Contact Verification Modal", "54"],
        ["Figure 9.4", "Multi-Branch Infrastructure & Location Management Console", "55"],
        ["Figure 9.5", "Menu Item Administration & Dynamic Photo Upload Preview", "56"],
        ["Figure 9.6", "Dynamic QR Code for Instant Mobile Device Access & Live Testing", "57"],
    ]
    add_table_styled(fig_headers, fig_rows, [1.0, 4.2, 0.8])

    add_h1("LIST OF TABLES")
    tbl_headers = ["Table No.", "Table Title & Description", "Page"]
    tbl_rows = [
        ["Table 1.1", "Technology Stack Selection & Technical Justifications", "3"],
        ["Table 3.1", "Comprehensive Project Feasibility Assessment Matrix", "11"],
        ["Table 4.1", "System Functional Requirements Specification (FR-01 to FR-10)", "13"],
        ["Table 4.2", "Hardware Environment Specifications (Server & Client)", "15"],
        ["Table 4.3", "Software Environment Specifications", "16"],
        ["Table 6.1", "Data Dictionary: `users` Table", "23"],
        ["Table 6.2", "Data Dictionary: `items` Table", "24"],
        ["Table 6.3", "Data Dictionary: `orders` Table", "25"],
        ["Table 6.4", "Data Dictionary: `order_items` Table", "26"],
        ["Table 6.5", "Data Dictionary: `staff` Table", "27"],
        ["Table 6.6", "Data Dictionary: `branches` Table", "28"],
        ["Table 7.1", "Comparative Evaluation: Conventional Manual vs Proposed POS", "31"],
        ["Table 10.1", "Comprehensive Test Execution Suite (TC-01 through TC-20)", "61"],
        ["Table 13.1", "19-Week Project Implementation Schedule Milestones", "77"],
    ]
    add_table_styled(tbl_headers, tbl_rows, [1.0, 4.2, 0.8])

    doc.add_page_break()

    # =============================================================
    # CHAPTER 1: INTRODUCTION
    # =============================================================
    print("Writing Chapter 1...")
    add_h1("CHAPTER 1: INTRODUCTION")
    add_h2("1.1 Background & Motivation")
    add_p("In the Indian food service and quick-service restaurant (QSR) sector, the speed, transparency, and accuracy of front-desk customer billing directly govern customer satisfaction, kitchen turnaround time, and daily revenue reconciliation. A vast majority of independent restaurants, casual dining eateries, and multi-counter food courts continue to rely heavily on manual handwritten carbon-copy Kitchen Order Tickets (KOTs), paper receipt books, or antiquated standalone electronic cash registers.")
    add_p("These legacy mechanisms present persistent operational vulnerabilities: arithmetic mistakes in tax and discount calculations, delays during peak rush hours, lack of real-time table occupancy tracking, absence of customer contact verification for home delivery, and total absence of executive sales analytics. Maharaja's Kitchen was conceived and engineered to resolve these deficiencies by providing a centralized, cloud-accessible, touch-optimized Point of Sale and billing solution tailored for modern restaurant workflows.")

    add_h2("1.2 Purpose of the Project")
    add_p("The overarching purpose of Maharaja's Kitchen is to digitise, streamline, and automate the entire restaurant transaction lifecycle. From the moment a guest places an order, the system handles instant item selection, dynamic cart total calculation with automated 5% GST computation, Dine-In table allocation, Delivery contact validation, multi-tender payment processing (UPI, Card, Cash), thermal invoice generation, and historical analytics tracking.")

    add_h2("1.3 Objectives")
    add_p("The project development was governed by seven primary objectives:")
    add_bullet("Rapid Order Entry: Enable cashiers to assemble custom orders with minimal clicks via an intuitive category-filtered menu grid.", "1. ")
    add_bullet("Automated Tax Engine: Accurately calculate compliant 5% GST (2.5% CGST + 2.5% SGST) with itemized receipt breakdowns.", "2. ")
    add_bullet("Multi-Mode Tender Processing: Support instant UPI verification, card processing, and dynamic cash change computation with smart exact-amount chips.", "3. ")
    add_bullet("Thermal & Digital Delivery: Support both instant thermal receipt printing via browser print drivers and offline client-side PDF downloads.", "4. ")
    add_bullet("Executive Sales Analytics: Provide managers with interactive Chart.js visualizations showing monthly revenue trends and payment mode distributions.", "5. ")
    add_bullet("Strict Data Integrity: Enforce real-time 10-digit phone number and RFC-compliant email validation across all customer, staff, and branch inputs.", "6. ")
    add_bullet("Encrypted Cloud Tunneling: Enable live HTTPS demonstration on external smartphones and tablets over Cloudflare Zero Trust without costly hosting infrastructure.", "7. ")

    add_h2("1.4 Scope of the Project")
    add_p("Current Scope:", bold_prefix="1.4.1 ")
    add_bullet("Role-based authentication (Admin and Cashier) with salted SHA-256 password hashing and secure session cookies.")
    add_bullet("Catalog management of 33 regional dishes spanning Thalis, Starters, Mains, South Indian, Breads, Desserts, and Beverages.")
    add_bullet("Dine-In table allocation (Tables 1-20) and Delivery module with automated ₹50 surcharge and mandatory 10-digit phone verification.")
    add_bullet("Staff roster and multi-location branch management with real-time input masking.")
    add_bullet("Order voiding, audit logging, and dynamic cash tender change calculation.")

    add_p("Future Scope:", bold_prefix="1.4.2 ")
    add_bullet("Kitchen Display System (KDS) for synchronized food preparation tablet screens.")
    add_bullet("Customer table QR self-ordering and payment integration.")
    add_bullet("Automated ingredient inventory depletion and supplier purchase orders.")
    add_bullet("WhatsApp Cloud API automated invoice dispatch.")

    add_h2("1.5 Technology Stack Selection & Justifications")
    add_p("Table 1.1 itemizes the architectural technology stack selected for the implementation of Maharaja's Kitchen, accompanied by technical justifications:")
    
    stack_headers = ["Layer / Component", "Technology Selected", "Technical Justification"]
    stack_rows = [
        ["Backend Framework", "Python 3.14 + Flask 3.1", "Micro-framework offering rapid WSGI routing, lightweight memory footprint, and modular blueprint extensibility."],
        ["Database Engine", "SQLite 3", "Serverless, zero-configuration, ACID-compliant relational database engine integrated natively into Python."],
        ["Frontend UI", "HTML5 + Tailwind CSS", "Utility-first modern CSS framework enabling touch-friendly, fully responsive layouts across devices."],
        ["Client Interactivity", "Vanilla JavaScript (ES6+)", "High-performance reactive cart state management and real-time input masking without heavyweight framework bloat."],
        ["Data Visualization", "Chart.js 4.x (UMD)", "Hardware-accelerated HTML5 canvas charts providing animated monthly revenue and doughnut distribution trends."],
        ["Document Synthesis", "html2pdf.js & ReportLab", "Dual client-side vector PDF generation and thermal printer slip styling."],
        ["Security / Auth", "Werkzeug Security (SHA-256)", "Cryptographically salted password hashing, HTTP-only session cookies, and route access guards."],
        ["Live Deployment", "Cloudflare Tunnel (cloudflared)", "Secure outbound TLS tunnel providing encrypted public HTTPS access directly to the local port without port forwarding."]
    ]
    add_table_styled(stack_headers, stack_rows, [1.4, 1.8, 2.8])

    doc.add_page_break()

    # =============================================================
    # CHAPTER 2: PROJECT OVERVIEW
    # =============================================================
    print("Writing Chapter 2...")
    add_h1("CHAPTER 2: PROJECT OVERVIEW & SYSTEM FEATURES")
    add_h2("2.1 System Architecture & Core Modules")
    add_p("Maharaja's Kitchen is architected as an integrated suite of seven specialized modules designed to address every facet of restaurant operations:")
    add_bullet("Authentication & Access Guard: Protects administrative and billing endpoints. Enforces role-based access control, allowing cashiers access to the POS terminal while restricting menu, staff, and branch management to administrators.", "1. ")
    add_bullet("Interactive POS Billing Terminal: The primary front-desk workspace featuring a category-filtered dish grid, live item search, reactive cart drawer, Dine-In table grid (Tables 1-20), Delivery order form, and multi-tender payment modal.", "2. ")
    add_bullet("Menu Administration Module: Enables authorized managers to add new dishes, update pricing, assign veg/non-veg status, and upload custom dish photography.", "3. ")
    add_bullet("Staff Roster Management: Maintains employee profiles, designations (Manager, Cashier, Chef, Waiter), shift timings, branch allocations, and salary records with mandatory 10-digit phone verification.", "4. ")
    add_bullet("Multi-Branch Location Console: Configures individual restaurant outlets with physical addresses, table capacities, manager contacts, and operational statuses.", "5. ")
    add_bullet("Executive Sales Analytics: Computes live sales metrics (Total Revenue, Order Count, Average Order Value) and visualizes monthly sales trends and payment mode percentages.", "6. ")
    add_bullet("Invoice Generation & Slip Engine: Generates compliant thermal receipts with 5% GST tax itemization and enables one-click PDF downloading.", "7. ")

    add_h2("2.2 Key Features & Technical Innovations")
    add_p("The system incorporates several notable engineering innovations:")
    add_bullet("Smart Google Image Auto-Cleaner: An automated URL processing algorithm that intercepts long Google Search image links (containing embedded imgurl= parameters), extracts the clean destination photograph, downloads it locally, and updates the database with a high-speed local image path.", "• ")
    add_bullet("As-You-Type 10-Digit Phone Masking: Real-time client-side event listeners that strip all non-numeric characters live as the user types, update an inline character badge ('X/10 digits'), and highlight borders green when exactly 10 digits are reached.", "• ")
    add_bullet("Dynamic Cash Calculator with Smart Suggestion Chips: In the payment modal, the cash received input is automatically pre-filled with the exact payable amount. Dynamic suggestion chips (₹50, ₹100, ₹500, ₹2000) allow instant one-click cash tender entry with real-time change calculation.", "• ")
    add_bullet("Center-Text Doughnut Chart Plugin: Custom Chart.js extension that dynamically computes and renders the dominant payment mode percentage directly in the center hole of the doughnut chart.", "• ")
    add_bullet("One-Click Desktop Launcher: Bundled batch file providing automatic background launching of the Flask application server, Cloudflare tunnel reconnection, and instant browser opening.", "• ")

    add_h2("2.3 Advantages Over Conventional Systems")
    add_p("Compared to traditional paper-based or standalone register setups, Maharaja's Kitchen delivers substantial quantifiable benefits: order processing time is reduced from 3 minutes to under 15 seconds; arithmetic tax errors are reduced to 0.0%; billing discrepancies are eliminated through automated order archiving; and multi-device cloud accessibility enables managers to monitor sales remotely from any smartphone.")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 3: FEASIBILITY REPORT
    # =============================================================
    print("Writing Chapter 3...")
    add_h1("CHAPTER 3: FEASIBILITY REPORT")
    add_p("A rigorous feasibility evaluation was conducted prior to development across four primary dimensions: technical, economic, operational, and schedule feasibility.")

    add_h2("3.1 Technical Feasibility")
    add_p("The project utilizes Python 3.14, Flask, SQLite3, and modern web standards. These technologies are exceptionally mature, thoroughly documented, and execute with minimal resource consumption. The entire application executes comfortably on standard commodity hardware (Intel Core i3/i5, 4 GB RAM) without requiring specialized GPU hardware or high-end database servers. Technical feasibility is fully confirmed.")

    add_h2("3.2 Economic & Financial Feasibility")
    add_p("All components of the software stack (Python, Flask, SQLite, Tailwind CSS, Chart.js, Cloudflare Tunnel) are available under permissive open-source licenses (MIT, BSD, Apache 2.0). The project incurs zero proprietary software licensing fees, zero commercial database fees, and zero recurring cloud hosting subscriptions. The financial feasibility is completely favorable.")

    add_h2("3.3 Operational Feasibility")
    add_p("The user interface was designed following ergonomic touchscreen POS conventions with large touch targets, high-contrast badges, and clear visual prompts. New cashiers can master order assembly, table allocation, and receipt printing with less than 10 minutes of initial training. Operational feasibility is thoroughly validated.")

    add_h2("3.4 Schedule & Timeline Feasibility")
    add_p("The project was structured across a 19-week academic timeframe spanning requirement elicitation, architecture design, database construction, frontend development, validation hardening, testing, and deployment. All milestones were achieved on schedule.")

    add_h2("3.5 Feasibility Analysis Summary")
    add_p("Table 3.1 synthesizes the feasibility evaluation across all evaluated parameters:")

    feas_headers = ["Feasibility Dimension", "Evaluation Finding & Assessment", "Academic Verdict"]
    feas_rows = [
        ["Technical Feasibility", "Lightweight Python/SQLite stack runs efficiently on standard laboratory PCs; no specialized hardware required.", "100% Feasible ✓"],
        ["Economic Feasibility", "Zero licensing or hosting expenditure; built entirely with free, open-source technologies.", "100% Feasible ✓"],
        ["Operational Feasibility", "Touch-friendly interface modeled on standard POS workflows; minimal cashier learning curve.", "100% Feasible ✓"],
        ["Schedule Feasibility", "All modules, diagrams, testing, and documentation completed within the 19-week academic semester.", "100% Feasible ✓"]
    ]
    add_table_styled(feas_headers, feas_rows, [1.5, 3.5, 1.0])

    doc.add_page_break()

    # =============================================================
    # CHAPTER 4: REQUIREMENT SPECIFICATION
    # =============================================================
    print("Writing Chapter 4...")
    add_h1("CHAPTER 4: REQUIREMENT SPECIFICATION (SRS)")
    add_h2("4.1 Functional Requirements")
    add_p("Table 4.1 outlines the functional requirements (FR-01 to FR-10) governing the behavior of Maharaja's Kitchen:")

    fr_headers = ["FR ID", "Functional Module", "Detailed Requirement Specification"]
    fr_rows = [
        ["FR-01", "User Authentication", "The system shall authenticate Admin and Cashier accounts using cryptographically salted SHA-256 password hashing."],
        ["FR-02", "Menu Catalog Display", "The system shall render active menu items categorized by cuisine with prices, veg/non-veg badges, and dish photography."],
        ["FR-03", "Dynamic Cart Calculation", "The system shall compute item subtotals, 2.5% CGST, 2.5% SGST, and grand total dynamically upon every cart quantity modification."],
        ["FR-04", "Dine-In Table Selector", "The system shall allow cashiers to allocate orders to tables 1 through 20 and highlight currently occupied tables."],
        ["FR-05", "Delivery Order Management", "The system shall capture customer name, address, and mandatory 10-digit phone number, automatically applying a ₹50 delivery surcharge."],
        ["FR-06", "Tender Processing & Change", "The system shall record payment modes (UPI, Card, Cash) and dynamically calculate exact cash change to return to the customer."],
        ["FR-07", "Invoice & Thermal Printing", "The system shall generate a structured thermal receipt slip and provide client-side PDF download functionality."],
        ["FR-08", "Menu Item Administration", "The system shall provide authorized administrators with full CRUD capabilities for menu items, including photo uploads and Google image cleaning."],
        ["FR-09", "Staff & Branch Administration", "The system shall maintain employee rosters and restaurant branch records, enforcing 10-digit numeric phone and RFC email validation."],
        ["FR-10", "Executive Sales Analytics", "The system shall aggregate daily and monthly revenue records, presenting interactive Chart.js line and doughnut visualizations."]
    ]
    add_table_styled(fr_headers, fr_rows, [0.8, 1.8, 3.4])

    add_h2("4.2 Non-Functional Requirements")
    add_bullet("Performance (NFR-01): Cart recalculations and DOM updates shall execute within 50 milliseconds. Backend API responses shall complete under 200 milliseconds on a local area network.", "• ")
    add_bullet("Security (NFR-02): All administrative and billing endpoints shall be protected by session-based authentication guards. Passwords shall never be stored in plain text.", "• ")
    add_bullet("Reliability & Data Integrity (NFR-03): Database transactions shall satisfy ACID properties to prevent partial or corrupted order entries. Phone numbers shall strictly adhere to a 10-digit format.", "• ")
    add_bullet("Usability & Responsiveness (NFR-04): The interface shall adhere to responsive design principles, operating seamlessly across mobile phones, tablets, and desktop displays.", "• ")

    add_h2("4.3 Hardware Requirements")
    add_p("Table 4.2 specifies the minimum and recommended hardware environments for server hosting and client terminal access:")
    
    hw_headers = ["Parameter", "Server (Development / Hosting)", "Client (POS Terminal / Mobile)"]
    hw_rows = [
        ["Processor", "Dual Core 2.0 GHz or higher (Intel/AMD)", "Single Core 1.2 GHz or modern smartphone SoC"],
        ["System RAM", "4 GB RAM minimum (8 GB recommended)", "2 GB RAM minimum (4 GB recommended)"],
        ["Hard Disk Space", "500 MB free space for code and database", "Standard web browser cache (50 MB)"],
        ["Display Resolution", "1366 x 768 or higher", "1024 x 600 (POS terminal) or smartphone screen"],
        ["Network Interface", "Standard Wi-Fi / Ethernet adapter", "Wi-Fi, 4G/5G mobile data, or LAN connection"]
    ]
    add_table_styled(hw_headers, hw_rows, [1.5, 2.3, 2.2])

    add_h2("4.4 Software Requirements")
    add_p("Table 4.3 summarizes the software prerequisites:")
    sw_headers = ["Software Component", "Specification / Version Utilized"]
    sw_rows = [
        ["Operating System", "Microsoft Windows 10 / 11, Linux (Ubuntu 22.04+), or macOS"],
        ["Programming Runtime", "Python 3.14.x / Python 3.10+"],
        ["Backend Web Framework", "Flask 3.1.x, Jinja2 3.1.x, Werkzeug 3.1.x"],
        ["Database Engine", "SQLite 3.x (native Python module)"],
        ["Frontend Technologies", "HTML5, CSS3, Tailwind CSS (CDN), Vanilla JavaScript (ES6+)"],
        ["Data Visualization", "Chart.js 4.4.x (UMD)"],
        ["Web Browser", "Google Chrome 120+, Mozilla Firefox 120+, Microsoft Edge 120+, Safari 17+"],
        ["Cloud Tunnel Client", "Cloudflare Tunnel (cloudflared v2024.x+)"]
    ]
    add_table_styled(sw_headers, sw_rows, [2.2, 3.8])

    doc.add_page_break()

    # =============================================================
    # CHAPTER 5: SYSTEM DESIGN
    # =============================================================
    print("Writing Chapter 5...")
    add_h1("CHAPTER 5: SYSTEM DESIGN & ARCHITECTURE")
    add_h2("5.1 Three-Tier Client-Server Architecture")
    add_p("Maharaja's Kitchen is structured according to the classic Three-Tier Architectural Pattern, ensuring clear separation of concerns, high maintainability, and scalability:")
    add_bullet("Presentation Tier (Client Layer): Rendered dynamically within the client browser using HTML5 semantic elements, Tailwind CSS for modern responsive utility styling, and Vanilla ES6+ JavaScript. It manages live user input masking, reactive cart DOM manipulation, Dine-In table selection, modal dialogs, and client-side PDF document synthesis.", "1. ")
    add_bullet("Application Tier (Business Logic Layer): Powered by Python 3.14 and the Flask WSGI micro-framework. It processes incoming HTTP requests, enforces session authentication via decorators (@login_required, @admin_required), computes 5% GST tax itemization, performs server-side phone number validation, executes the automated Google Image cleaning pipeline, and generates analytical aggregations.", "2. ")
    add_bullet("Data Tier (Database Layer): Handled by SQLite3, storing structured data across normalized relational tables for users, menu items, orders, order items, employees, and restaurant branches. SQLite ensures zero-configuration ACID reliability without the operational overhead of external database servers.", "3. ")

    add_h2("5.2 Input Design & Real-Time Masking")
    add_p("Input design prioritizes operator speed, data validation, and error prevention. All interactive forms feature real-time client-side event listeners:")
    add_bullet("Phone Number Input Masking: Intercepts input events, strips all non-numeric characters, restricts length to exactly 10 digits (maxlength=10), updates an inline character count badge ('X/10 digits'), and dynamically alters the border color (red for incomplete, emerald green for valid).", "• ")
    add_bullet("Email Format Validation: Validates email inputs against RFC standards, displaying instant feedback badges prior to form submission.", "• ")
    add_bullet("Cash Tender Auto-Fill & Suggestion Chips: In the payment modal, the cash received field auto-populates with the exact bill amount, complemented by one-click quick suggestion chips (₹50, ₹100, ₹500, ₹2000).", "• ")

    add_h2("5.3 Output Design & Invoice Layout")
    add_p("The system provides dual output modalities:")
    add_bullet("Thermal Slip Output: Formatted specifically for standard 80mm thermal receipt printers, itemizing dish quantities, unit rates, subtotal, 2.5% CGST, 2.5% SGST, delivery surcharge, and final payable amount.", "1. ")
    add_bullet("Digital PDF Invoice: Synthesized client-side via html2pdf.js, allowing cashiers to download and archive digital invoices instantly.", "2. ")

    add_h2("5.4 Security Architecture")
    add_p("Security is enforced at multiple layers: passwords are never stored in plain text; instead, they are hashed using salted SHA-256 via Werkzeug Security. User sessions are maintained using signed HTTP-only session cookies. Every administrative route is guarded by decorator functions that verify role credentials before executing controller logic.")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 6: DATABASE DESIGN
    # =============================================================
    print("Writing Chapter 6...")
    add_h1("CHAPTER 6: DATABASE DESIGN & IMPLEMENTATION")
    add_h2("6.1 Relational Schema Architecture")
    add_p("The relational database schema is encapsulated in food_billing.db and consists of six normalized tables designed to maintain referential integrity through primary and foreign keys.")

    add_h2("6.2 Data Dictionaries")
    add_p("Tables 6.1 through 6.6 provide the complete data dictionaries for all system entities:")

    # Table 6.1: users
    add_h3("Table 6.1: Data Dictionary - users (User Authentication)")
    u_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    u_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique internal user identifier"],
        ["username", "TEXT", "NOT NULL, UNIQUE", "Login username (e.g., admin, cashier)"],
        ["password_hash", "TEXT", "NOT NULL", "Salted cryptographic SHA-256 hash"],
        ["role", "TEXT", "NOT NULL", "Authorization level: 'Admin' or 'Cashier'"]
    ]
    add_table_styled(u_headers, u_rows, [1.4, 1.2, 1.8, 1.6])

    # Table 6.2: items
    add_h3("Table 6.2: Data Dictionary - items (Menu Dishes)")
    i_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    i_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique dish identifier"],
        ["name", "TEXT", "NOT NULL", "Full commercial dish name"],
        ["category", "TEXT", "NOT NULL", "Classification (Thalis, Starters, Mains, etc.)"],
        ["price", "REAL", "NOT NULL", "Selling price in INR (₹)"],
        ["image_url", "TEXT", "NULLABLE", "Local image path or verified URL"],
        ["is_active", "BOOLEAN", "DEFAULT 1", "Active status indicator for soft-deletion"],
        ["is_veg", "BOOLEAN", "DEFAULT 1", "Vegetarian indicator (1=Veg, 0=Non-Veg)"]
    ]
    add_table_styled(i_headers, i_rows, [1.4, 1.2, 1.8, 1.6])

    # Table 6.3: orders
    add_h3("Table 6.3: Data Dictionary - orders (Order Master)")
    o_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    o_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique internal order ID"],
        ["bill_number", "TEXT", "NOT NULL, UNIQUE", "Formal invoice number (BILL-YYYYMMDD-XXXX)"],
        ["order_date", "DATE", "NOT NULL", "Date of order placement"],
        ["order_type", "TEXT", "NOT NULL", "Service mode: 'Dine-In' or 'Delivery'"],
        ["table_number", "INTEGER", "NULLABLE", "Assigned dining table number (1-20)"],
        ["customer_name", "TEXT", "NULLABLE", "Customer full name"],
        ["customer_phone", "TEXT(10)", "NULLABLE", "Verified 10-digit mobile number"],
        ["customer_address", "TEXT", "NULLABLE", "Delivery destination address"],
        ["payment_mode", "TEXT", "NOT NULL", "Tender method: 'UPI', 'Card', or 'Cash'"],
        ["subtotal", "REAL", "NOT NULL", "Itemized subtotal before tax in INR"],
        ["tax", "REAL", "NOT NULL", "Computed 5% GST (2.5% CGST + 2.5% SGST)"],
        ["delivery_fee", "REAL", "DEFAULT 0.0", "Delivery surcharge in INR (₹50)"],
        ["total_amount", "REAL", "NOT NULL", "Final payable amount in INR"],
        ["status", "TEXT", "NOT NULL", "Order status: 'Completed' or 'Void'"]
    ]
    add_table_styled(o_headers, o_rows, [1.4, 1.2, 1.8, 1.6])

    # Table 6.4: order_items
    add_h3("Table 6.4: Data Dictionary - order_items (Order Line Items)")
    oi_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    oi_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique line item identifier"],
        ["order_id", "INTEGER", "FK -> orders(id)", "Associated parent order ID"],
        ["item_id", "INTEGER", "FK -> items(id)", "Associated menu dish ID"],
        ["quantity", "INTEGER", "NOT NULL", "Quantity ordered"],
        ["price_per_unit", "REAL", "NOT NULL", "Unit selling price at time of order"],
        ["total_price", "REAL", "NOT NULL", "Line total amount (quantity * unit price)"]
    ]
    add_table_styled(oi_headers, oi_rows, [1.4, 1.2, 1.8, 1.6])

    # Table 6.5: staff
    add_h3("Table 6.5: Data Dictionary - staff (Employee Roster)")
    st_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    st_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique employee identifier"],
        ["name", "TEXT", "NOT NULL", "Employee full name"],
        ["role", "TEXT", "NOT NULL", "Designation (Manager, Cashier, Chef, Waiter)"],
        ["phone", "TEXT(10)", "NOT NULL", "10-digit verified contact number"],
        ["email", "TEXT", "NULLABLE", "Verified email address"],
        ["shift", "TEXT", "NOT NULL", "Shift timing (Morning, Evening, Full Day)"],
        ["branch_id", "INTEGER", "FK -> branches(id)", "Assigned restaurant branch"],
        ["salary", "REAL", "DEFAULT 0.0", "Monthly salary in INR"],
        ["status", "TEXT", "DEFAULT 'Active'", "Status (Active, On Leave, Inactive)"]
    ]
    add_table_styled(st_headers, st_rows, [1.4, 1.2, 1.8, 1.6])

    # Table 6.6: branches
    add_h3("Table 6.6: Data Dictionary - branches (Restaurant Locations)")
    br_headers = ["Column Name", "Data Type", "Constraints", "Description"]
    br_rows = [
        ["id", "INTEGER", "PRIMARY KEY, AUTOINCREMENT", "Unique branch identifier"],
        ["name", "TEXT", "NOT NULL", "Branch name (e.g., Flagship Outlet)"],
        ["city", "TEXT", "NOT NULL", "Operating city location"],
        ["address", "TEXT", "NOT NULL", "Physical street address"],
        ["phone", "TEXT(10)", "NOT NULL", "10-digit branch contact phone"],
        ["manager_name", "TEXT", "NULLABLE", "Branch supervisor / manager name"],
        ["tables_count", "INTEGER", "DEFAULT 20", "Total dining table capacity"],
        ["status", "TEXT", "DEFAULT 'Active'", "Operational status indicator"]
    ]
    add_table_styled(br_headers, br_rows, [1.4, 1.2, 1.8, 1.6])

    add_h2("6.3 Relational Database Normalization")
    add_p("The database schema was rigorously normalized up to the Third Normal Form (3NF):")
    add_bullet("First Normal Form (1NF): All attributes contain atomic values, with primary keys uniquely identifying every tuple. Multi-item orders are separated into atomic tuples in the order_items child table.", "• ")
    add_bullet("Second Normal Form (2NF): Eliminates partial functional dependencies. In order_items, all non-key attributes depend fully on the primary key rather than a composite subset.", "• ")
    add_bullet("Third Normal Form (3NF): Eliminates transitive dependencies. Branch details (city, address) and employee designations are maintained in dedicated tables referenced via foreign keys rather than redundantly stored in the orders table.", "• ")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 7: SYSTEM ANALYSIS
    # =============================================================
    print("Writing Chapter 7...")
    add_h1("CHAPTER 7: SYSTEM ANALYSIS & COMPARATIVE STUDY")
    add_h2("7.1 Comparative Evaluation")
    add_p("A rigorous comparative evaluation was performed contrasting conventional manual restaurant billing practices with the automated capabilities of Maharaja's Kitchen POS. Table 7.1 details the operational advantages:")

    comp_headers = ["Operational Parameter", "Conventional Manual System", "Proposed Maharaja's Kitchen POS"]
    comp_rows = [
        ["Order Assembly Speed", "2 to 4 minutes per ticket (handwritten KOT)", "Under 15 seconds (touch card selection)"],
        ["Tax Calculation", "Manual calculator; high error frequency", "Automated 5% GST (2.5% CGST + 2.5% SGST)"],
        ["Table Allocation", "Mental tracking; frequent double-booking", "Visual interactive table grid with occupied status"],
        ["Payment Processing", "Manual cash change mental calculation", "Dynamic change calculator with smart suggestion chips"],
        ["Receipt Output", "Handwritten bill book; legible issues", "Instant thermal receipt print and vector PDF download"],
        ["Sales Reconciliation", "1+ hour end-of-day register tallying", "Real-time Chart.js monthly trend & doughnut analytics"],
        ["Menu Management", "Reprinting paper menus on price changes", "Instant digital updates with automated Google image cleaner"],
        ["Contact Verification", "Unverified phone numbers; lost delivery tickets", "Strict real-time 10-digit phone & RFC email validation"]
    ]
    add_table_styled(comp_headers, comp_rows, [1.5, 2.2, 2.3])

    add_h2("7.2 SWOT Analysis")
    add_bullet("Strengths (S): Lightweight Python/SQLite stack, zero external software licensing costs, reactive touch-friendly interface, strict 10-digit phone validation, automated image cleaner, and live Cloudflare tunnel access.", "• ")
    add_bullet("Weaknesses (W): Requires local client hardware and network connectivity; relies on browser print drivers for thermal slip generation.", "• ")
    add_bullet("Opportunities (O): Integration of Kitchen Display System (KDS) tablets, QR-based table self-ordering, automated ingredient stock depletion, and WhatsApp invoice dispatch.", "• ")
    add_bullet("Threats (T): Local network hardware failure during peak dining rush hours; physical printer paper roll depletion.", "• ")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 8: SYSTEM DIAGRAMS (ALL 12 PLANTUML DIAGRAMS EMBEDDED)
    # =============================================================
    print("Writing Chapter 8 with all 12 PlantUML diagrams...")
    add_h1("CHAPTER 8: SYSTEM DIAGRAMS & ARCHITECTURAL MODELS")
    add_p("This chapter documents the complete architectural, structural, and behavioral modeling of Maharaja's Kitchen. All 12 diagrams were formally modeled using PlantUML specifications and rendered via PlantText. The rendered vector diagrams illustrate the static design, dynamic workflows, data flows, and physical deployment of the application.")

    # 8.1 Class Diagram
    add_h2("8.1 Class Diagram")
    add_p("The Class Diagram illustrates the object-oriented structure of Maharaja's Kitchen, depicting core domain classes: User, Item, Order, OrderItem, Staff, and Branch. It details private attributes, public operations, data types, and multiplicity associations connecting the entities.")
    add_image_scaled(os.path.join(diag_dir, "class diagram.png"),
                     "Maharaja's Kitchen Object-Oriented Class Hierarchy Diagram",
                     "Figure 8.1", max_w=4.8, max_h=5.4, page_break_after=True)

    # 8.2 Object Diagram
    add_h2("8.2 Object Diagram")
    add_p("The Object Diagram captures a concrete runtime snapshot of an active billing transaction (Order #101), showing specific instantiated objects: cashier Priya Nair, customer Amit Sharma, assigned dining Table 4, ordered dishes (Murg Musallam, Garlic Naan), and line item totals.")
    add_image_scaled(os.path.join(diag_dir, "object diagram.png"),
                     "Runtime Object Instance Snapshot Diagram (Active Dine-In Order #101)",
                     "Figure 8.2", max_w=4.8, max_h=5.4, page_break_after=True)

    # 8.3 Entity-Relationship (ER) Diagram
    add_h2("8.3 Entity-Relationship (ER) Diagram")
    add_p("The Entity-Relationship (ER) Diagram visualizes the complete relational database schema across all six normalized tables in food_billing.db, showing primary keys (PK), foreign keys (FK), column attributes, and relational cardinalities (1:N and N:M).")
    add_image_scaled(os.path.join(diag_dir, "ER diagram.png"),
                     "Entity-Relationship (ER) Schema with Relational Cardinalities",
                     "Figure 8.3", max_w=5.0, max_h=5.35, page_break_after=True)

    # 8.4 Use Case Diagram
    add_h2("8.4 Use Case Diagram")
    add_p("The Use Case Diagram defines system actors (Cashier, Administrator, and Customer) and their functional interactions across authentication, POS order entry, table allocation, delivery customer capture, payment processing, menu administration, staff rosters, and financial analytics.")
    add_image_scaled(os.path.join(diag_dir, "use case diagram.png"),
                     "System Use Case Diagram (Cashier, Admin, Customer Interactions)",
                     "Figure 8.4", max_w=5.8, max_h=4.2, page_break_after=True)

    # 8.5 Activity Diagram
    add_h2("8.5 Activity Diagram")
    add_p("The Activity Diagram traces the end-to-end operational workflow of a transaction, detailing control flow from user login, category navigation, cart assembly, Dine-In table selection or Delivery address capture, payment mode selection, tax calculation, to invoice generation.")
    add_image_scaled(os.path.join(diag_dir, "activity diagram.png"),
                     "End-to-End Operational Billing Activity Workflow",
                     "Figure 8.5", max_w=3.8, max_h=5.35, page_break_after=True)

    # 8.6 State Machine Diagram
    add_h2("8.6 State Machine Diagram")
    add_p("The State Machine Diagram models the dynamic lifecycle states of a customer order, transitioning through: CartDraft -> TableAssigned / DeliveryEntered -> ProcessingPayment -> Completed -> Archived (or Voided).")
    add_image_scaled(os.path.join(diag_dir, "state machine diagram.png"),
                     "Finite State Machine Order Lifecycle Diagram",
                     "Figure 8.6", max_w=2.6, max_h=5.4, page_break_after=True)

    # 8.7 Component Diagram
    add_h2("8.7 Component Diagram")
    add_p("The Component Diagram illustrates modular structural decomposition across the Presentation Tier (Tailwind CSS, Vanilla JS, Chart.js), Application Tier (Flask WSGI API, Auth Controller, Billing Engine, Image Cleaner), and Data Tier (SQLite3 DB, Static Assets).")
    add_image_scaled(os.path.join(diag_dir, "component diagram.png"),
                     "Three-Tier Modular Component Architecture Diagram",
                     "Figure 8.7", max_w=5.8, max_h=3.2, page_break_after=True)

    # 8.8 Deployment Diagram
    add_h2("8.8 Deployment Diagram")
    add_p("The Deployment Diagram maps physical hardware and network nodes, illustrating client devices (Desktop, Tablet, Smartphone) connecting via HTTPS over Cloudflare Edge Tunnels to the local Flask application server running on Port 5001.")
    add_image_scaled(os.path.join(diag_dir, "deployment diagram.png"),
                     "Physical Node Deployment & Cloudflare Tunnel Edge Topology",
                     "Figure 8.8", max_w=3.0, max_h=5.3, page_break_after=True)

    # 8.9 Package Diagram
    add_h2("8.9 Package Diagram")
    add_p("The Package Diagram organizes the logical directory and module structure of the codebase, showing dependencies between python core modules (app.py), templates (Jinja2 HTML), static resources (CSS, JS, images), and database artifacts.")
    add_image_scaled(os.path.join(diag_dir, "package diagram.png"),
                     "Python Flask & Frontend Asset Package Architecture",
                     "Figure 8.9", max_w=5.8, max_h=2.2, page_break_after=True)

    # 8.10 Data Flow Diagram (DFD Level 0)
    add_h2("8.10 Data Flow Diagram (DFD Level 0 - Context Diagram)")
    add_p("The Context-Level Data Flow Diagram (DFD Level 0) models the boundary of Maharaja's Kitchen as a single central process, showing data flows between external entities (Admin, Cashier, Customer) and the POS core.")
    add_image_scaled(os.path.join(diag_dir, "data flow diagram.png"),
                     "Data Flow Diagram (DFD Level 0 - Context Level Diagram)",
                     "Figure 8.10", max_w=5.2, max_h=3.8, page_break_after=True)

    # 8.11 Data Flow Diagram (DFD Level 1)
    add_h2("8.11 Data Flow Diagram (DFD Level 1 - Detailed)")
    add_p("The Level 1 Data Flow Diagram decomposes the system into six core sub-processes: 1.0 User Authentication, 2.0 Menu Management, 3.0 POS Cart Processing, 4.0 Payment & Invoice Generation, 5.0 Staff/Branch Administration, and 6.0 Sales Analytics Reporting.")
    add_image_scaled(os.path.join(diag_dir, "data flow diagram level 1.png"),
                     "Data Flow Diagram (DFD Level 1 - Detailed Functional Decomposition)",
                     "Figure 8.11", max_w=5.8, max_h=2.6, page_break_after=True)

    # 8.12 Sequence Diagram
    add_h2("8.12 Sequence Diagram")
    add_p("The Sequence Diagram traces chronological message exchanges during order checkout: Cashier -> Browser UI -> Flask API Controller -> SQLite Database Engine -> Browser Receipt Generator -> Thermal Printer Slip.")
    add_image_scaled(os.path.join(diag_dir, "sequence diagram.png"),
                     "Synchronous Checkout & Payment Processing Sequence Diagram",
                     "Figure 8.12", max_w=5.8, max_h=4.2, page_break_after=True)

    # =============================================================
    # CHAPTER 9: SCREEN OUTPUTS & USER INTERFACE WALKTHROUGH
    # =============================================================
    print("Writing Chapter 9 with all 5 UI screenshots + QR code...")
    add_h1("CHAPTER 9: SCREEN OUTPUTS & USER INTERFACE WALKTHROUGH")
    add_p("This chapter documents the visual interface of Maharaja's Kitchen, showcasing high-resolution screen captures from the live operating system. Built with Tailwind CSS, the user interface delivers high visual clarity, ergonomic touch targets, real-time input feedback, and responsive layout across mobile and desktop environments.")

    # 9.1 POS Billing Screen
    add_h2("9.1 Real-Time Point-of-Sale (POS) Billing Interface & Cart")
    add_p("Figure 9.1 displays the primary cashier POS workspace. It features category navigation pills (Thalis, Starters, Mains, South Indian, Breads, Desserts, Beverages), responsive food item cards with dish photography, vegetarian/non-vegetarian indicators, live search bar, interactive Dine-In table selector (Tables 1-20), Delivery toggle with customer contact input, real-time cart tallying with 5% GST breakdown, and instant Checkout trigger.")
    add_image_scaled(os.path.join(screen_dir, "screen_01_billing.png"),
                     "Point-of-Sale (POS) Billing Interface with Live Cart & Dine-In Selector",
                     "Figure 9.1", max_w=5.8, max_h=3.5, page_break_after=True)

    # 9.2 Analytics Dashboard
    add_h2("9.2 Executive Sales Analytics & Chart.js Doughnut Charts")
    add_p("Figure 9.2 showcases the administrative sales intelligence dashboard. It summarizes key operational KPIs (Total Sales in INR, Completed Order Count, Average Order Value) alongside an animated monthly sales bar/line graph and a center-text payment mode doughnut chart displaying exact percentages for UPI, Card, and Cash tenders.")
    add_image_scaled(os.path.join(screen_dir, "screen_02_analytics.png"),
                     "Executive Sales Analytics Dashboard with Center-Text Doughnut Chart",
                     "Figure 9.2", max_w=5.8, max_h=3.5, page_break_after=True)

    # 9.3 Staff Roster Management
    add_h2("9.3 Staff Roster Management & Contact Verification Modal")
    add_p("Figure 9.3 illustrates the employee administration console and Add/Edit Staff modal. The interface enforces real-time client-side validation: mobile numbers are masked to exactly 10 numeric digits with dynamic character badges, and email inputs are validated live prior to database submission.")
    add_image_scaled(os.path.join(screen_dir, "screen_03_staff.png"),
                     "Staff Roster Management & Contact Verification Modal",
                     "Figure 9.3", max_w=5.8, max_h=3.5, page_break_after=True)

    # 9.4 Branch Management
    add_h2("9.4 Multi-Branch Infrastructure & Location Management Console")
    add_p("Figure 9.4 shows the multi-outlet management interface. Administrators can track multiple dining branches, inspect table capacities, configure operational hours, manage branch supervisor contact details, and assign staff members to specific restaurant locations.")
    add_image_scaled(os.path.join(screen_dir, "screen_04_branch.png"),
                     "Multi-Branch Infrastructure & Location Management Console",
                     "Figure 9.4", max_w=5.8, max_h=3.5, page_break_after=True)

    # 9.5 Menu Management
    add_h2("9.5 Menu Item Administration & Dynamic Photo Upload Preview")
    add_p("Figure 9.5 demonstrates the menu management portal. Managers can add or update dishes, adjust selling rates, designate vegetarian status, and upload custom dish photography with instantaneous live image preview. The smart Google Image cleaning algorithm automatically extracts clean URLs when pasted by the administrator.")
    add_image_scaled(os.path.join(screen_dir, "screen_05_menu_edit.png"),
                     "Menu Item Administration & Dynamic Photo Upload Preview Modal",
                     "Figure 9.5", max_w=5.8, max_h=3.5, page_break_after=True)

    # 9.6 Dynamic Live QR Code
    add_h2("9.6 Dynamic QR Code for Instant Mobile Device Access")
    add_p("Figure 9.6 displays the dynamic QR code generated for live external evaluation. Scanning this code on any smartphone, iPad, or Android tablet directs the user immediately to the live public HTTPS Cloudflare Tunnel instance of Maharaja's Kitchen without requiring local Wi-Fi pairing or manual IP configuration.")
    add_image_scaled(qr_path,
                     "Dynamic QR Code for Instant Mobile Device Access & Live Testing",
                     "Figure 9.6", max_w=2.8, max_h=2.8, page_break_after=True)

    # =============================================================
    # CHAPTER 10: SYSTEM TESTING
    # =============================================================
    print("Writing Chapter 10...")
    add_h1("CHAPTER 10: SYSTEM TESTING & QUALITY ASSURANCE")
    add_h2("10.1 Testing Strategy & Methodology")
    add_p("System verification was executed systematically across multiple test phases: Unit Testing verified individual functions (such as GST tax formulas and phone regex sanitization); Integration Testing verified synchronous data exchange between the frontend cart and Flask API endpoints; System Testing evaluated complete end-to-end billing transactions; and Boundary Value Analysis tested edge cases (e.g., exactly 10 digits, empty carts, cash tender below total).")

    add_h2("10.2 Comprehensive Test Cases Execution Table")
    add_p("Table 10.1 itemizes all 20 formal test cases executed during quality assurance, demonstrating 100% test pass rate:")

    tc_headers = ["TC ID", "Test Scenario / Function", "Test Input Data", "Expected Result", "Status"]
    tc_rows = [
        ["TC-01", "Admin Valid Authentication", "user: 'admin', pass: 'admin123'", "Redirect to POS billing terminal with admin badges", "Pass ✓"],
        ["TC-02", "Admin Invalid Authentication", "user: 'admin', pass: 'wrongpass'", "Display 'Invalid username or password'; block login", "Pass ✓"],
        ["TC-03", "Cart Tax Computation (5% GST)", "Item subtotal: ₹500.00", "CGST: ₹12.50, SGST: ₹12.50, Grand Total: ₹525.00", "Pass ✓"],
        ["TC-04", "Delivery Phone Validation (<10 digits)", "phone: '98765'", "Display 'Must be exactly 10 digits'; block submission", "Pass ✓"],
        ["TC-05", "Delivery Phone Non-Numeric Strip", "phone: '98abc54321'", "Auto-strip non-digits live; enforce numeric input", "Pass ✓"],
        ["TC-06", "Delivery Phone Valid 10 Digits", "phone: '9876543210'", "Highlight border emerald green; enable checkout", "Pass ✓"],
        ["TC-07", "Dine-In Table Allocation", "Select Table 4", "Store table_number=4; mark Table 4 occupied in DB", "Pass ✓"],
        ["TC-08", "Cash Change Calculation (Sufficient)", "Total: ₹525, Cash: ₹1000", "Display Change to Return: ₹475.00 in green; enable confirm", "Pass ✓"],
        ["TC-09", "Cash Change Calculation (Insufficient)", "Total: ₹525, Cash: ₹500", "Display 'Insufficient Tender'; disable confirm button", "Pass ✓"],
        ["TC-10", "UPI Payment Flow Confirmation", "Select 'UPI' tender mode", "Generate bill immediately; transition to thermal receipt", "Pass ✓"],
        ["TC-11", "Thermal Slip Print Formatting", "Click 'Print Receipt'", "Trigger window.print() formatted to standard 80mm roll", "Pass ✓"],
        ["TC-12", "Client-Side Vector PDF Download", "Click 'Download PDF'", "Download formatted .pdf receipt file via html2pdf.js", "Pass ✓"],
        ["TC-13", "Staff Phone Validation (<10 digits)", "phone: '12345'", "Display '10 digits required'; prevent modal submission", "Pass ✓"],
        ["TC-14", "Staff Email RFC Validation", "email: 'testemail'", "Display 'Please enter a valid email format'; block POST", "Pass ✓"],
        ["TC-15", "Staff Valid Record Creation", "Valid 10-digit phone & email", "HTTP 201 Created; persist staff member in database", "Pass ✓"],
        ["TC-16", "Branch Contact Phone Validation", "phone: '9811432198'", "HTTP 201 Created; update branch records", "Pass ✓"],
        ["TC-17", "Google Image URL Auto-Cleaner", "Paste complex Google img URL", "Extract real imgurl, download and cache locally", "Pass ✓"],
        ["TC-18", "Local Dish Photo Upload", "Upload .jpg dish photo", "Save image to static/img/; return local photo path", "Pass ✓"],
        ["TC-19", "Order Voiding & Revenue Sync", "Void Order #101", "Set status to 'Void'; subtract amount from daily total", "Pass ✓"],
        ["TC-20", "Cloudflare HTTPS Tunnel Access", "Open trycloudflare.com URL", "HTTP 200 OK over secure public HTTPS tunnel", "Pass ✓"]
    ]
    add_table_styled(tc_headers, tc_rows, [0.7, 1.8, 1.6, 1.9, 0.7])

    add_h2("10.3 Quality Assurance Verification Sign-Off")
    add_p("All 20 test cases achieved 100% compliance against functional specifications. No regression faults, calculation inaccuracies, or UI rendering discrepancies were detected during testing.")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 11: DEPLOYMENT & CLOUD INFRASTRUCTURE
    # =============================================================
    print("Writing Chapter 11...")
    add_h1("CHAPTER 11: DEPLOYMENT & CLOUD INFRASTRUCTURE")
    add_h2("11.1 Local WSGI Server Configuration")
    add_p("The production deployment executes locally using Python 3.14 hosting the Flask WSGI micro-framework on loopback port 5001 (http://127.0.0.1:5001). Static assets are served efficiently with cache-busting headers, while SQLite database transactions execute in WAL (Write-Ahead Logging) mode to optimize concurrency during peak order traffic.")

    add_h2("11.2 Cloudflare Zero Trust Tunneling Topology")
    add_p("To facilitate real-world multi-device testing and academic evaluation without costly static public IP hosting, Maharaja's Kitchen integrates Cloudflare Tunnel (cloudflared):")
    add_bullet("Zero Port-Forwarding Architecture: The tunnel client establishes an outbound encrypted TLS connection to Cloudflare's nearest edge data center. No router inbound ports (e.g., 80 or 443) are opened, completely shielding the host development machine from unauthorized network scanning.", "• ")
    add_bullet("End-to-End HTTPS Encryption: Evaluators access the system through an SSL/TLS-certified hostname (*.trycloudflare.com), guaranteeing encrypted data transit for logins, orders, and payment records.", "• ")
    add_bullet("Cross-Device Responsive Compatibility: External smartphones, iPads, and remote evaluator laptops render the identical responsive UI, verified across mobile browsers.", "• ")

    add_h2("11.3 Database Migration & Demo Data Seeding")
    add_p("Automated migration scripts (migrate_orders.py, migrate_staff_branches.py, seed_demo_data.py) ensure the database initializes with 33 authentic regional dishes, realistic staffing rosters, multiple branch outlets, and historical order records for comprehensive evaluation.")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 12: CORE SOURCE CODE LISTINGS
    # =============================================================
    print("Writing Chapter 12...")
    add_h1("CHAPTER 12: CORE SOURCE CODE LISTINGS")
    add_p("This chapter documents key implementation listings from the backend Python controller (app.py) and frontend reactive engine (static/js/main.js), highlighting core algorithms.")

    add_h2("12.1 Backend Tax Calculation & Order Checkout (Python / Flask)")
    code_py = (
        "@app.route('/api/orders', methods=['POST'])\n"
        "@login_required\n"
        "def create_order():\n"
        "    data = request.get_json()\n"
        "    items = data.get('items', [])\n"
        "    order_type = data.get('order_type', 'Dine-In')\n"
        "    table_num = data.get('table_number') if order_type == 'Dine-In' else None\n"
        "    phone = data.get('customer_phone', '').strip()\n"
        "\n"
        "    # Strict 10-Digit Phone Validation for Delivery\n"
        "    if order_type == 'Delivery':\n"
        "        if not phone or len(phone) != 10 or not phone.isdigit():\n"
        "            return jsonify({'error': 'Delivery requires a valid 10-digit phone number'}), 400\n"
        "\n"
        "    subtotal = sum(item['price'] * item['qty'] for item in items)\n"
        "    cgst = round(subtotal * 0.025, 2)  # 2.5% CGST\n"
        "    sgst = round(subtotal * 0.025, 2)  # 2.5% SGST\n"
        "    tax = round(cgst + sgst, 2)        # 5% Total GST\n"
        "    delivery_fee = 50.0 if order_type == 'Delivery' else 0.0\n"
        "    total = round(subtotal + tax + delivery_fee, 2)\n"
        "\n"
        "    bill_no = f\"BILL-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}\"\n"
        "    conn = get_db()\n"
        "    cur = conn.cursor()\n"
        "    cur.execute(\"\"\"\n"
        "        INSERT INTO orders (bill_number, order_date, order_type, table_number,\n"
        "                            customer_name, customer_phone, customer_address,\n"
        "                            payment_mode, subtotal, tax, delivery_fee, total_amount, status)\n"
        "        VALUES (?, DATE('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Completed')\n"
        "    \"\"\", (bill_no, order_type, table_num, data.get('customer_name'),\n"
        "           phone, data.get('customer_address'), data.get('payment_mode'),\n"
        "           subtotal, tax, delivery_fee, total))\n"
        "    order_id = cur.lastrowid\n"
        "    conn.commit()\n"
        "    return jsonify({'success': True, 'bill_number': bill_no, 'total': total}), 201"
    )
    p_code1 = doc.add_paragraph()
    p_code1.paragraph_format.space_before = Pt(4)
    p_code1.paragraph_format.space_after = Pt(8)
    r_c1 = p_code1.add_run(code_py)
    r_c1.font.name = "Consolas"
    r_c1.font.size = Pt(8.5)
    r_c1.font.color.rgb = SLATE

    add_h2("12.2 Real-Time As-You-Type 10-Digit Phone Masking (JavaScript)")
    code_js = (
        "function setupPhoneInputMask(inputId, badgeId) {\n"
        "    const input = document.getElementById(inputId);\n"
        "    const badge = document.getElementById(badgeId);\n"
        "    if (!input) return;\n"
        "\n"
        "    input.addEventListener('input', function(e) {\n"
        "        // Strip all non-digit characters immediately\n"
        "        let val = this.value.replace(/\\D/g, '');\n"
        "        if (val.length > 10) val = val.substring(0, 10);\n"
        "        this.value = val;\n"
        "\n"
        "        if (badge) {\n"
        "            badge.textContent = `${val.length}/10 digits`;\n"
        "            if (val.length === 10) {\n"
        "                badge.className = 'text-xs text-emerald-600 font-semibold';\n"
        "                input.classList.remove('border-red-400');\n"
        "                input.classList.add('border-emerald-500');\n"
        "            } else {\n"
        "                badge.className = 'text-xs text-slate-400 font-normal';\n"
        "                input.classList.remove('border-emerald-500');\n"
        "            }\n"
        "        }\n"
        "    });\n"
        "}"
    )
    p_code2 = doc.add_paragraph()
    p_code2.paragraph_format.space_before = Pt(4)
    p_code2.paragraph_format.space_after = Pt(8)
    r_c2 = p_code2.add_run(code_js)
    r_c2.font.name = "Consolas"
    r_c2.font.size = Pt(8.5)
    r_c2.font.color.rgb = SLATE

    doc.add_page_break()

    # =============================================================
    # CHAPTER 13: PROJECT SCHEDULE
    # =============================================================
    print("Writing Chapter 13...")
    add_h1("CHAPTER 13: PROJECT SCHEDULE & EXECUTION TIMELINE")
    add_p("The project was executed across an intensive 19-week academic timeframe. Table 13.1 details the project execution timeline, phases, and milestone deliverables:")

    sch_headers = ["Phase No.", "Development Phase Description", "Academic Weeks", "Deliverables & Milestones"]
    sch_rows = [
        ["Phase 1", "Problem Identification & Feasibility Study", "Weeks 1 - 3", "System scope definition, QSR literature review, feasibility matrix."],
        ["Phase 2", "Requirement Specification & SRS Formulation", "Weeks 4 - 6", "Formal SRS document, functional (FR) & non-functional (NFR) definitions."],
        ["Phase 3", "Architectural & Relational Database Design", "Weeks 7 - 9", "Normalized 3NF relational schema, data dictionary, PlantUML modeling."],
        ["Phase 4", "Backend Flask API & Security Engineering", "Weeks 10 - 12", "RESTful endpoints, password hashing, session guards, tax engine."],
        ["Phase 5", "Frontend POS Terminal & Tailwind UI", "Weeks 13 - 15", "Reactive cart drawer, table grid, modal dialogs, phone masking."],
        ["Phase 6", "Quality Assurance & Test Suite Execution", "Weeks 16 - 17", "20 formal test cases (TC-01 to TC-20), boundary condition testing."],
        ["Phase 7", "Cloud Deployment & Academic Documentation", "Weeks 18 - 19", "Cloudflare HTTPS tunnel, final documentation report, Viva preparation."]
    ]
    add_table_styled(sch_headers, sch_rows, [0.8, 2.2, 1.2, 2.6])

    doc.add_page_break()

    # =============================================================
    # CHAPTER 14: CONCLUSION
    # =============================================================
    print("Writing Chapter 14...")
    add_h1("CHAPTER 14: CONCLUSION")
    add_h2("14.1 Summary of Work Accomplished")
    add_p("The Maharaja's Kitchen Restaurant Food Billing & Multi-Branch POS Management System was successfully designed, developed, evaluated, and deployed as a full-stack academic project for Semester V of the Bachelor of Science (Computer Science) curriculum under the University of Mumbai.")
    add_p("By replacing manual handwritten billing books and slow standalone registers with an intuitive, touch-friendly web application, the system delivers instantaneous order entry, automated 5% GST computation, visual Dine-In table management, strict 10-digit phone verification, thermal slip printing, and real-time executive sales analytics. The live Cloudflare Tunnel deployment allows effortless demonstration on smartphones and tablets without expensive server hosting.")

    add_h2("14.2 Key Academic Contributions")
    add_bullet("Full-Stack Proficiency: Demonstrated robust mastery of Python Flask, SQLite3, Tailwind CSS, Vanilla JavaScript, and Chart.js.")
    add_bullet("Data Integrity: Enforced strict validation across customer, staff, and branch phone numbers and email addresses.")
    add_bullet("Zero-Cost Production Architecture: Proven implementation of high-performance business software using 100% open-source technologies.")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 15: FUTURE SCOPE
    # =============================================================
    print("Writing Chapter 15...")
    add_h1("CHAPTER 15: FUTURE SCOPE & ENHANCEMENTS")
    add_p("While Maharaja's Kitchen provides a comprehensive operational foundation for food billing and management, several promising enhancements are planned for future iterations:")
    add_bullet("Kitchen Display System (KDS): Mounting synchronized touch tablets in kitchen food preparation stations to broadcast live incoming orders instantly.", "1. ")
    add_bullet("Customer Table QR Self-Ordering: Allowing dining guests to scan table-mounted QR codes with their personal smartphones to browse digital menus and place orders.", "2. ")
    add_bullet("Automated Inventory & Recipe Depletion: Tracking raw ingredient levels (flour, dairy, spices) and automatically decrementing stock quantities upon order checkout.", "3. ")
    add_bullet("Meta Cloud WhatsApp Invoice Dispatch: Integrating the WhatsApp Business Cloud API to transmit formatted digital PDF receipts directly to verified customer mobile numbers.", "4. ")
    add_bullet("AI-Powered Sales Forecasting: Implementing predictive machine learning models to forecast peak dining hours and recommend optimal ingredient procurement.", "5. ")

    doc.add_page_break()

    # =============================================================
    # CHAPTER 16: REFERENCES
    # =============================================================
    print("Writing Chapter 16...")
    add_h1("CHAPTER 16: BIBLIOGRAPHY & REFERENCES")
    add_h2("16.1 Reference Textbooks & Standards")
    add_p("1. Grinberg, Miguel. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.")
    add_p("2. Silberschatz, Abraham, Korth, Henry F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.")
    add_p("3. Pressman, Roger S., & Maxim, Bruce R. (2020). Software Engineering: A Practitioner's Approach (9th ed.). McGraw-Hill.")
    add_p("4. Flanagan, David. (2020). JavaScript: The Definitive Guide (7th ed.). O'Reilly Media.")
    add_p("5. Fowler, Martin. (2003). UML Distilled: A Brief Guide to the Standard Object Modeling Language (3rd ed.). Addison-Wesley.")

    add_h2("16.2 Official Documentation & Web References")
    add_p("6. Python Software Foundation. (2026). Python 3.14 Documentation. Retrieved from https://docs.python.org/3/")
    add_p("7. Pallets Projects. (2026). Flask Documentation (v3.1.x). Retrieved from https://flask.palletsprojects.com/")
    add_p("8. SQLite Consortium. (2026). SQLite Database Engine Architecture & SQL Reference. Retrieved from https://www.sqlite.org/docs.html")
    add_p("9. Tailwind Labs. (2026). Tailwind CSS Modern Styling Documentation. Retrieved from https://tailwindcss.com/docs")
    add_p("10. Chart.js Community. (2026). Chart.js: Open Source HTML5 Charts for Modern Web. Retrieved from https://www.chartjs.org/")
    add_p("11. Cloudflare Inc. (2026). Cloudflare Tunnels and Zero Trust Network Documentation. Retrieved from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/")
    add_p("12. PlantUML Team. (2026). PlantUML Language Reference Guide & PlantText Online Tool. Retrieved from https://plantuml.com/ & https://www.planttext.com/")
    add_p("13. University of Mumbai. (2025). Bachelor of Science (Computer Science) Semester V & VI Curriculum Guidelines.")

    # Save final report
    out_path = r"C:\Project Sem 5\Maharajas_Kitchen_Project_Report.docx"
    print(f"Saving final report to {out_path}...")
    doc.save(out_path)
    file_size_kb = os.path.getsize(out_path) / 1024.0
    print(f"SUCCESS: Report saved successfully! File size: {file_size_kb:.2f} KB")

if __name__ == "__main__":
    create_report()
