from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "submission" / "BUFS_Admissions_RAG_결과보고서_20232829.docx"

AUTHOR = "맥슈웰 데이브"
STUDENT_ID = "20232829"
REPORT_DATE = "2026년 7월 24일"
GITHUB_URL = "https://github.com/davemaxuell/ai-bootcamp-rag"
DEPLOY_URL = "https://ai-bootcamp-rag-7ahkiva6fmc7qzkiifmz6a.streamlit.app/"

CALIBRI = "Calibri"
KOREAN_FONT = "Malgun Gothic"
NAVY = "203748"
BLUE = "2E74B5"
DARK_BLUE = "1F4D78"
MUTED = "66717D"
LIGHT_GRAY = "F2F4F7"
MID_GRAY = "D8DEE5"
PALE_BLUE = "EEF5FB"
GOLD = "A66F00"
WHITE = "FFFFFF"

PAGE_WIDTH_DXA = 9360
TABLE_INDENT_DXA = 120


def set_run_font(
    run,
    *,
    size=None,
    color=None,
    bold=None,
    italic=None,
    ascii_font=CALIBRI,
    east_asia_font=KOREAN_FONT,
):
    run.font.name = ascii_font
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), east_asia_font)
    if size is not None:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = RGBColor.from_string(color)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic


def set_style_font(style, size, color=None, bold=None):
    style.font.name = CALIBRI
    style._element.rPr.rFonts.set(qn("w:ascii"), CALIBRI)
    style._element.rPr.rFonts.set(qn("w:hAnsi"), CALIBRI)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), KOREAN_FONT)
    style.font.size = Pt(size)
    if color:
        style.font.color.rgb = RGBColor.from_string(color)
    if bold is not None:
        style.font.bold = bold


def configure_styles(doc):
    normal = doc.styles["Normal"]
    set_style_font(normal, 11, color="222222")
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.10

    title = doc.styles["Title"]
    set_style_font(title, 30, color=NAVY, bold=True)
    title.paragraph_format.space_before = Pt(0)
    title.paragraph_format.space_after = Pt(8)
    title.paragraph_format.keep_with_next = True

    subtitle = doc.styles["Subtitle"]
    set_style_font(subtitle, 15, color=DARK_BLUE)
    subtitle.paragraph_format.space_before = Pt(0)
    subtitle.paragraph_format.space_after = Pt(8)

    heading_tokens = {
        "Heading 1": (16, BLUE, 16, 8),
        "Heading 2": (13, BLUE, 12, 6),
        "Heading 3": (12, DARK_BLUE, 8, 4),
    }
    for name, (size, color, before, after) in heading_tokens.items():
        style = doc.styles[name]
        set_style_font(style, size, color=color, bold=True)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    for name in ("List Bullet", "List Number"):
        style = doc.styles[name]
        set_style_font(style, 11, color="222222")
        style.paragraph_format.space_after = Pt(8)
        style.paragraph_format.line_spacing = 1.167

    caption = doc.styles["Caption"]
    set_style_font(caption, 9, color=MUTED)
    caption.font.italic = True
    caption.paragraph_format.space_before = Pt(4)
    caption.paragraph_format.space_after = Pt(4)


def set_page_geometry(section):
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1)
    section.right_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.header_distance = Inches(0.492)
    section.footer_distance = Inches(0.492)


def add_page_field(paragraph):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, separate, text, end):
        run._r.append(node)
    set_run_font(run, size=9, color=MUTED)


def configure_header_footer(section):
    header = section.header
    paragraph = header.paragraphs[0]
    paragraph.text = "BUFS MULTILINGUAL ADMISSIONS RAG  |  FINAL PROJECT REPORT"
    paragraph.paragraph_format.space_after = Pt(0)
    for run in paragraph.runs:
        set_run_font(run, size=8.5, color=MUTED, bold=True)

    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    paragraph.paragraph_format.space_before = Pt(0)
    prefix = paragraph.add_run(f"{AUTHOR} · {STUDENT_ID}   |   ")
    set_run_font(prefix, size=9, color=MUTED)
    add_page_field(paragraph)


def paragraph_shading(paragraph, fill):
    ppr = paragraph._p.get_or_add_pPr()
    shd = ppr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        ppr.append(shd)
    shd.set(qn("w:fill"), fill)


def paragraph_left_border(paragraph, color, size=18, space=10):
    ppr = paragraph._p.get_or_add_pPr()
    pbdr = ppr.find(qn("w:pBdr"))
    if pbdr is None:
        pbdr = OxmlElement("w:pBdr")
        ppr.append(pbdr)
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(size))
    left.set(qn("w:space"), str(space))
    left.set(qn("w:color"), color)
    pbdr.append(left)


def add_lead_callout(doc, label, text):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.left_indent = Inches(0.18)
    paragraph.paragraph_format.right_indent = Inches(0.12)
    paragraph.paragraph_format.space_before = Pt(5)
    paragraph.paragraph_format.space_after = Pt(12)
    paragraph.paragraph_format.line_spacing = 1.15
    paragraph_shading(paragraph, PALE_BLUE)
    paragraph_left_border(paragraph, BLUE)
    label_run = paragraph.add_run(f"{label}  ")
    set_run_font(label_run, size=11, color=DARK_BLUE, bold=True)
    text_run = paragraph.add_run(text)
    set_run_font(text_run, size=11, color="222222")


def set_cell_margins(cell, top=80, start=120, bottom=80, end=120):
    tc = cell._tc
    tcpr = tc.get_or_add_tcPr()
    tc_mar = tcpr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tcpr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def shade_cell(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = tcpr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tcpr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_table_borders(table, color=MID_GRAY, size=6):
    tblpr = table._tbl.tblPr
    borders = tblpr.find(qn("w:tblBorders"))
    if borders is None:
        borders = OxmlElement("w:tblBorders")
        tblpr.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = borders.find(qn(f"w:{edge}"))
        if node is None:
            node = OxmlElement(f"w:{edge}")
            borders.append(node)
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)


def set_table_geometry(table, widths_dxa):
    if sum(widths_dxa) != PAGE_WIDTH_DXA:
        raise ValueError(f"Column widths must sum to {PAGE_WIDTH_DXA}")

    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    tbl = table._tbl
    tblpr = tbl.tblPr

    tblw = tblpr.find(qn("w:tblW"))
    if tblw is None:
        tblw = OxmlElement("w:tblW")
        tblpr.append(tblw)
    tblw.set(qn("w:w"), str(PAGE_WIDTH_DXA))
    tblw.set(qn("w:type"), "dxa")

    tblind = tblpr.find(qn("w:tblInd"))
    if tblind is None:
        tblind = OxmlElement("w:tblInd")
        tblpr.append(tblind)
    tblind.set(qn("w:w"), str(TABLE_INDENT_DXA))
    tblind.set(qn("w:type"), "dxa")

    grid = tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths_dxa:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)

    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            tcpr = cell._tc.get_or_add_tcPr()
            tcw = tcpr.find(qn("w:tcW"))
            if tcw is None:
                tcw = OxmlElement("w:tcW")
                tcpr.append(tcw)
            tcw.set(qn("w:w"), str(widths_dxa[idx]))
            tcw.set(qn("w:type"), "dxa")
            set_cell_margins(cell)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    trpr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    trpr.append(tbl_header)


def format_cell_text(cell, *, bold=False, color="222222", size=9.5, align=None):
    for paragraph in cell.paragraphs:
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = 1.08
        if align is not None:
            paragraph.alignment = align
        for run in paragraph.runs:
            set_run_font(run, size=size, color=color, bold=bold)


def add_table(doc, headers, rows, widths_dxa, alignments=None):
    table = doc.add_table(rows=1, cols=len(headers))
    set_table_geometry(table, widths_dxa)
    set_table_borders(table)
    header_cells = table.rows[0].cells
    for idx, header in enumerate(headers):
        header_cells[idx].text = header
        shade_cell(header_cells[idx], LIGHT_GRAY)
        format_cell_text(
            header_cells[idx],
            bold=True,
            color=NAVY,
            size=9.5,
            align=(alignments[idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT),
        )
    set_repeat_table_header(table.rows[0])

    for row_values in rows:
        row = table.add_row()
        for idx, value in enumerate(row_values):
            cell = row.cells[idx]
            cell.text = str(value)
            format_cell_text(
                cell,
                size=9.3,
                align=(alignments[idx] if alignments else WD_ALIGN_PARAGRAPH.LEFT),
            )
    after = doc.add_paragraph()
    after.paragraph_format.space_before = Pt(0)
    after.paragraph_format.space_after = Pt(3)
    return table


def add_bullet(doc, text):
    paragraph = doc.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.left_indent = Inches(0.5)
    paragraph.paragraph_format.first_line_indent = Inches(-0.25)
    paragraph.add_run(text)
    return paragraph


def add_number(doc, title, text):
    paragraph = doc.add_paragraph(style="List Number")
    paragraph.paragraph_format.left_indent = Inches(0.5)
    paragraph.paragraph_format.first_line_indent = Inches(-0.25)
    title_run = paragraph.add_run(f"{title}: ")
    set_run_font(title_run, bold=True, color=DARK_BLUE)
    paragraph.add_run(text)
    return paragraph


def add_metadata_line(doc, label, value, *, align=WD_ALIGN_PARAGRAPH.CENTER):
    paragraph = doc.add_paragraph()
    paragraph.alignment = align
    paragraph.paragraph_format.space_after = Pt(4)
    label_run = paragraph.add_run(f"{label}  ")
    set_run_font(label_run, size=10.5, color=MUTED, bold=True)
    value_run = paragraph.add_run(value)
    set_run_font(value_run, size=10.5, color=NAVY)


def add_page_break(doc):
    paragraph = doc.add_paragraph()
    paragraph.add_run().add_break(WD_BREAK.PAGE)


def build_report():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = Document()
    doc.core_properties.title = "BUFS 다국어 입학 도우미 프로젝트 결과보고서"
    doc.core_properties.subject = "LangChain 및 RAG 기반 다국어 실용 서비스"
    doc.core_properties.author = f"{AUTHOR} ({STUDENT_ID})"
    doc.core_properties.keywords = "LangChain, RAG, Chroma, Streamlit, multilingual"
    doc.core_properties.comments = "부산외국어대학교 AI 부트캠프 최종 프로젝트"

    configure_styles(doc)
    for section in doc.sections:
        set_page_geometry(section)
        configure_header_footer(section)

    # Cover — intentionally simple and student-report-like.
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(88)

    kicker = doc.add_paragraph()
    kicker.alignment = WD_ALIGN_PARAGRAPH.CENTER
    kicker.paragraph_format.space_after = Pt(16)
    run = kicker.add_run("프로젝트 결과보고서")
    set_run_font(run, size=11, color=GOLD, bold=True)

    title = doc.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("BUFS 다국어 입학 도우미")

    subtitle = doc.add_paragraph(style="Subtitle")
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run("공식 입학 문서를 근거로 답하는 LangChain·RAG 서비스")

    summary = doc.add_paragraph()
    summary.alignment = WD_ALIGN_PARAGRAPH.CENTER
    summary.paragraph_format.left_indent = Inches(0.65)
    summary.paragraph_format.right_indent = Inches(0.65)
    summary.paragraph_format.space_after = Pt(58)
    run = summary.add_run(
        "외국인 지원자가 입학 서류와 일정을 자신의 언어로 쉽게 확인할 수 있도록 만든 웹 서비스"
    )
    set_run_font(run, size=10.5, color=MUTED)

    add_metadata_line(doc, "작성자", AUTHOR)
    add_metadata_line(doc, "학번", STUDENT_ID)
    add_metadata_line(doc, "제출일", REPORT_DATE)
    add_metadata_line(doc, "GitHub", GITHUB_URL)
    add_metadata_line(doc, "배포 URL", DEPLOY_URL)

    closing = doc.add_paragraph()
    closing.alignment = WD_ALIGN_PARAGRAPH.CENTER
    closing.paragraph_format.space_before = Pt(42)
    run = closing.add_run("부산외국어대학교 AI 부트캠프")
    set_run_font(run, size=10, color=MUTED)

    add_page_break(doc)

    doc.add_heading("1. 프로젝트를 시작한 이유", level=1)
    doc.add_paragraph(
        "부산외대에는 한국어가 익숙하지 않은 외국인 지원자가 많다. 입학 관련 자료는 한국어와 "
        "영어 PDF로 나뉘어 있고, 모집요강 안에서도 마감일·지원 자격·제출 서류가 여러 페이지에 "
        "흩어져 있다. 필요한 내용을 찾으려면 문서를 하나씩 열어 봐야 해서 처음 지원하는 학생에게는 "
        "불편할 수 있다고 생각했다."
    )
    doc.add_paragraph(
        "그래서 단순히 문장을 번역하는 서비스보다, 공식 문서에서 질문과 관련된 부분을 먼저 찾고 "
        "그 근거를 보여 주는 도구를 만들기로 했다. 특히 '무슨 서류를 준비해야 하는가'는 지원자의 "
        "과정과 신입·편입 여부에 따라 달라지므로, 일반 질문 답변과 별도로 체크리스트 기능도 넣었다."
    )

    doc.add_heading("1.1 만들고 싶었던 기능", level=2)
    add_bullet(doc, "질문은 한국어·영어뿐 아니라 중국어와 베트남어 등 다른 언어로도 입력할 수 있게 한다.")
    add_bullet(doc, "답변에는 참고한 PDF 파일명과 페이지를 함께 표시한다.")
    add_bullet(doc, "학부/대학원과 신입/편입 조건을 반영한 제출서류 목록을 만든다.")
    add_bullet(doc, "문서에서 찾지 못한 내용은 추측하지 않고 입학처 확인을 안내한다.")

    doc.add_heading("1.2 프로젝트 한눈에 보기", level=2)
    add_table(
        doc,
        ["항목", "내용"],
        [
            ("사용 문서", "BUFS 공식 입학 관련 PDF 6개(한국어·영어)"),
            ("검색 데이터", "페이지 정보를 포함한 텍스트 청크 64개"),
            ("주요 기능", "다국어 질문 답변, 출처 표시, 맞춤형 서류 체크리스트"),
            ("사용 기술", "LangChain, Chroma, OpenAI API, Streamlit"),
            ("배포", "GitHub + Streamlit Community Cloud"),
        ],
        [2300, 7060],
    )

    doc.add_heading("2. 구현 과정", level=1)
    doc.add_heading("2.1 PDF에서 검색 데이터 만들기", level=2)
    doc.add_paragraph(
        "먼저 모집요강 4개, 온라인 원서접수 안내 1개, 제출서류 체크리스트 1개를 모았다. "
        "pdfplumber로 페이지별 텍스트를 읽고, 추출된 글자가 너무 적은 페이지는 pypdf로 "
        "한 번 더 읽도록 했다. 이후 한 페이지의 글이 길면 최대 2,000자 단위로 나누었다. "
        "각 조각에는 원본 파일명, 페이지 번호, 문서 언어, 학부/대학원 구분을 저장했다."
    )
    doc.add_paragraph(
        "실제 문서를 돌려 보니 총 64개 청크가 나왔다. 이 수가 많지는 않지만, 약 50페이지 정도의 "
        "입학 자료를 실습용으로 검색하기에는 충분했고 출처 페이지를 유지하기도 쉬웠다."
    )

    doc.add_heading("2.2 RAG 동작 순서", level=2)
    add_number(doc, "임베딩", "64개 청크를 text-embedding-3-small로 변환해 Chroma에 저장했다.")
    add_number(doc, "검색", "사용자의 질문과 의미가 가까운 문서 조각을 기본 6개 가져온다.")
    add_number(doc, "필터", "체크리스트에서는 학부/대학원 자료와 공통 안내 문서만 검색한다.")
    add_number(doc, "답변", "검색 결과와 질문을 gpt-4o-mini에 보내 문서 안의 내용으로만 답하게 한다.")
    add_number(doc, "출처", "검색된 파일명과 페이지를 답변 아래에 별도로 표시한다.")

    doc.add_heading("2.3 파일 구성", level=2)
    add_table(
        doc,
        ["파일", "역할"],
        [
            ("extract.py", "PDF를 읽고 페이지 정보가 있는 청크로 나눈다."),
            ("ingest.py", "청크를 임베딩해 persistent Chroma DB를 만든다."),
            ("retriever.py", "질문과 가까운 문서를 검색하고 과정 필터를 적용한다."),
            ("answerer.py", "검색 문서만 근거로 다국어 답변과 출처를 만든다."),
            ("checklist.py", "지원 조건을 반영한 제출서류 목록을 만든다."),
            ("app.py", "질문 탭과 체크리스트 탭을 제공하는 Streamlit 화면이다."),
        ],
        [2200, 7160],
    )

    doc.add_heading("2.4 다국어 질문 처리", level=2)
    doc.add_paragraph(
        "원본 문서는 한국어와 영어지만 임베딩 모델이 여러 언어의 의미를 비교할 수 있기 때문에, "
        "중국어와 베트남어 질문도 관련 영어 또는 한국어 문서로 연결할 수 있었다. 답변 프롬프트에는 "
        "사용자가 질문한 언어로 답하라는 조건을 넣었다. 따라서 별도의 번역기처럼 문장을 1:1로 "
        "바꾸는 것이 아니라, 다른 언어로 검색한 뒤 필요한 내용을 정리해서 답하는 구조다."
    )

    doc.add_heading("3. 완성한 기능", level=1)
    doc.add_heading("3.1 다국어 질문 답변", level=2)
    doc.add_paragraph(
        "첫 번째 탭에서는 사용자가 자연어로 질문할 수 있다. 예를 들어 영어로 지원 마감일을 묻거나, "
        "중국어로 학부 지원 서류를 물어도 관련 모집요강을 검색한다. 답변 아래에는 실제로 검색된 "
        "PDF와 페이지가 표시된다. 중요한 날짜나 금액을 확인할 때 원문으로 다시 돌아갈 수 있게 한 것이다."
    )

    doc.add_heading("3.2 제출서류 체크리스트", level=2)
    doc.add_paragraph(
        "두 번째 탭에서는 학부/대학원, 전공, 신입/편입, 원하는 답변 언어를 입력한다. 그러면 일반 "
        "체크리스트와 해당 과정의 모집요강을 같이 검색해 번호가 있는 준비 서류 목록을 만든다. "
        "지원자에 따라 달라질 수 있는 어학 성적이나 가족관계 서류는 조건이 있다는 점도 함께 설명하도록 했다."
    )

    doc.add_heading("3.3 답변을 찾지 못했을 때", level=2)
    doc.add_paragraph(
        "검색 결과가 비어 있으면 모델을 호출하지 않고 '공식 문서에서 찾지 못했으니 입학처에 확인해 "
        "달라'는 문구를 반환한다. 입학 정보는 잘못된 날짜 하나도 문제가 될 수 있기 때문에, 그럴듯한 "
        "답을 만드는 것보다 모른다고 말하는 편이 더 중요하다고 판단했다."
    )

    doc.add_heading("4. 개발하면서 생긴 문제", level=1)
    doc.add_heading("4.1 PDF가 두 번 들어가던 문제", level=2)
    doc.add_paragraph(
        "처음에는 소문자 *.pdf와 대문자 *.PDF를 각각 검색했다. 그런데 Windows에서는 두 패턴이 "
        "같은 파일을 모두 잡아서 64개여야 할 청크가 128개가 되었다. 테스트 자체는 통과했지만 그대로 "
        "두면 임베딩 비용과 검색 결과가 중복될 수 있었다. 파일명을 기준으로 경로를 한 번만 남기도록 "
        "수정한 뒤 청크가 64개인지 다시 확인했다. 예상하지 못했던 운영체제 차이였다."
    )

    doc.add_heading("4.2 표와 이미지가 많은 PDF", level=2)
    doc.add_paragraph(
        "모집요강에는 표가 많아서 일반 텍스트 추출만 사용하면 줄 순서가 자연스럽지 않은 부분이 있었다. "
        "이번 버전에서는 표 처리에 비교적 나은 pdfplumber를 우선 사용하고 pypdf를 보조로 사용했다. "
        "여섯 파일의 모든 페이지에서 텍스트가 나오기는 했지만, 스크린샷 안의 글자까지 읽는 OCR은 넣지 못했다."
    )

    doc.add_heading("4.3 배포 시 API 키 관리", level=2)
    doc.add_paragraph(
        "로컬에서는 .env를 사용했지만 GitHub에는 키가 올라가면 안 된다. .env와 기존 키 파일을 "
        ".gitignore에 넣고, Streamlit 배포에서는 Secrets에 OPENAI_API_KEY를 따로 등록했다. "
        "마지막 푸시 전에 커밋 대상 파일에 키 형태의 문자열이 없는지도 확인했다."
    )

    doc.add_heading("5. Claude Code를 사용한 부분", level=1)
    doc.add_paragraph(
        "Claude Code는 서비스 안에서 답변하는 모델이 아니라 개발 과정의 도구로 사용했다. 처음에는 "
        "요구사항을 기능별 파일로 나누고 각 함수의 입력과 출력을 정리하는 데 도움을 받았다. 이후 "
        "테스트 코드를 먼저 만들고, 실패하는 부분을 확인한 뒤 구현하는 순서로 진행했다."
    )
    doc.add_paragraph(
        "생성된 코드를 그대로 끝내지는 않았다. 실제 PDF를 실행했을 때 나온 청크 수를 확인했고, "
        "Windows 중복 문제처럼 계획에 없던 오류는 원인을 다시 찾아 수정했다. 마지막에는 테스트, "
        "비밀키 검사, Git 상태, Streamlit 공개 URL을 각각 확인했다. 이 과정에서 AI 코딩 도구도 "
        "실행 결과를 직접 검토해야 한다는 점을 배웠다."
    )

    doc.add_heading("6. 테스트 결과", level=1)
    doc.add_paragraph(
        "자동 테스트는 총 12개를 작성했다. 설정값과 파일명 분류, PDF 청크, 빈 검색 결과 처리, "
        "체크리스트 거절 로직, 안정적인 문서 ID, 과정 필터를 확인했다."
    )
    add_table(
        doc,
        ["확인한 항목", "결과"],
        [
            ("단위 테스트", "12개 모두 통과"),
            ("Chroma 저장 데이터", "64개 벡터 확인"),
            ("다국어 질문", "한국어·영어·중국어·베트남어 4개 질문 통과"),
            ("로컬 Streamlit", "헬스 체크 HTTP 200"),
            ("공개 웹 서비스", "실제 질문 답변과 PDF 파일명·페이지 표시 확인"),
        ],
        [3300, 6060],
    )
    doc.add_paragraph(
        "다국어 평가는 아직 4개 질문만 사용한 간단한 확인용 테스트다. 마감일이나 등록금처럼 정답을 "
        "정확히 비교해야 하는 질문을 더 추가하면 서비스 품질을 더 제대로 평가할 수 있다."
    )

    doc.add_heading("7. 배포", level=1)
    doc.add_paragraph(
        "소스 코드는 GitHub의 main 브랜치에 올렸고, Streamlit Community Cloud에서 app.py를 "
        "실행하도록 연결했다. Chroma 데이터베이스도 저장소에 포함했기 때문에 배포 서버에서 PDF를 "
        "다시 임베딩하지 않아도 된다."
    )
    add_table(
        doc,
        ["제출 항목", "위치"],
        [
            ("공개 웹 서비스", DEPLOY_URL),
            ("GitHub 저장소", GITHUB_URL),
            ("소스 코드 노트북", "submission/BUFS_Admissions_RAG_20232829.ipynb"),
            ("결과보고서", "submission/BUFS_Admissions_RAG_결과보고서_20232829.docx"),
        ],
        [2600, 6760],
    )

    doc.add_heading("8. 아쉬운 점과 앞으로 해 보고 싶은 것", level=1)
    add_bullet(doc, "이미지로 된 안내 화면도 검색할 수 있도록 OCR을 추가하고 싶다.")
    add_bullet(doc, "질문이 학부인지 대학원인지 먼저 선택하게 하면 서로 다른 과정의 출처가 섞이는 일을 줄일 수 있다.")
    add_bullet(doc, "입학 공지가 바뀔 때 자동으로 문서를 다시 수집하고 인덱스를 갱신하는 기능이 필요하다.")
    add_bullet(doc, "실제 외국인 지원자에게 사용해 보게 하고 어려웠던 표현이나 빠진 질문을 수집하고 싶다.")

    doc.add_heading("9. 느낀 점", level=1)
    doc.add_paragraph(
        "이번 프로젝트를 하면서 RAG는 단순히 PDF를 넣고 질문하는 기능이 아니라는 것을 알게 되었다. "
        "텍스트를 어떻게 나누는지, 출처 정보를 어떻게 남기는지, 검색 결과가 없을 때 어떻게 처리하는지가 "
        "최종 답변의 신뢰도에 직접 영향을 줬다."
    )
    doc.add_paragraph(
        "또한 다국어 서비스에서는 번역 품질만큼 사용자가 원문을 확인할 수 있게 하는 것이 중요했다. "
        "현재 기능은 작은 규모이지만, 학교에 처음 지원하는 학생이 여러 PDF를 반복해서 찾는 시간을 "
        "줄여 줄 수 있다는 점에서 실제 사용 목적이 분명한 결과물을 만들었다고 생각한다."
    )

    signoff = doc.add_paragraph()
    signoff.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    signoff.paragraph_format.space_before = Pt(16)
    run = signoff.add_run(f"{AUTHOR}  |  {STUDENT_ID}")
    set_run_font(run, size=10.5, color=DARK_BLUE, bold=True)

    doc.save(OUTPUT)
    return OUTPUT


if __name__ == "__main__":
    print(build_report())
