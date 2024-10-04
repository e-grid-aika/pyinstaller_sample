import datetime
import math

from fpdf import FPDF
from fpdf.fonts import FontFace

tax_rate = 0.1


class PDF(FPDF):
    def 見積もり日(self):  # noqa
        base_x = -70
        base_y = 10
        self.set_xy(base_x, base_y)
        self.cell(txt=f"見積もり日 : {format(datetime.date.today(), '%Y年%m月%d日')}")

    def 見積もり番号(self):  # noqa
        base_x = -70
        base_y = 15
        self.set_xy(base_x, base_y)
        self.cell(txt=f"見積もり番号 : {format(datetime.date.today(), '%Y%m%d')}-001")

    def 見積書タイトル(self):  # noqa
        base_x = 95
        base_y = 30
        self.set_font(size=20)
        self.set_xy(95, 30)
        self.set_xy(base_x, base_y)
        self.cell(txt="見積書", align="C")

    def 顧客宛名(self, company_name: str):  # noqa
        base_x = 10
        base_y = 50
        self.set_xy(base_x, base_y)
        atena = f"{company_name}　御中"
        cell_width = atena.__len__() * 4
        cell_height = 20
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.cell(cell_width, cell_height, txt=atena)
        self.line(
            self.get_x() - cell_width,
            self.get_y() + cell_height - 5,
            self.get_x(),
            self.get_y() + cell_height - 5,
        )

    def 見積もり件名(self, title: str):  # noqa
        base_x = 10
        base_y = 70
        self.set_xy(base_x, base_y)
        self.cell(txt="件名：" + title)

    def 見積もり期限(self, interbal):  # noqa
        base_x = 10
        base_y = 75
        self.set_xy(base_x, base_y)
        self.cell(
            txt=f"有効期限 : {format(datetime.date.today() + datetime.timedelta(days=interbal), '%Y年%m月%d日')}"
        )

    def 見積もり金額(self, price):  # noqa
        base_x = 10
        base_y = 100
        self.set_xy(base_x, base_y)
        price_str = f"お見積もり金額   ¥{price:,}"  # price を 3桁区切りにする
        cell_width = price_str.__len__() * 3
        cell_height = 20
        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.cell(cell_width, cell_height, txt=price_str)
        self.line(
            self.get_x() - cell_width,
            self.get_y() + cell_height - 5,
            self.get_x(),
            self.get_y() + cell_height - 5,
        )

    def 見積もり会社(
        self, my_company_name: str, company_adress: str, account_user_name: str
    ):  # noqa
        base_x = 150
        base_y = 60
        self.set_xy(base_x, base_y)
        self.cell(txt=my_company_name)
        self.set_xy(base_x, base_y + 5)
        self.cell(txt=company_adress)
        self.set_xy(base_x, base_y + 10)
        self.cell(txt=account_user_name)

    def 見積もり明細(self, data: list[dict]) -> int:  # noqa
        if len(data) == 0:
            return 0
        base_x = 10
        base_y = 150
        self.set_xy(base_x, base_y)
        self.set_draw_color(255, 0, 0)
        self.set_line_width(0.3)
        headings_style = FontFace(color=255, fill_color=(255, 100, 0))
        with pdf.table(
            borders_layout="NO_HORIZONTAL_LINES",
            cell_fill_color=(224, 235, 255),
            col_widths=(42, 39, 35, 42),
            cell_fill_mode="ROWS",
            headings_style=headings_style,
            line_height=6,
            text_align=("LEFT", "CENTER", "RIGHT", "RIGHT"),
            width=160,
        ) as table:
            sub_total_amount = 0
            for page, data_row in enumerate(data):
                if page == 0:
                    row = table.row()
                    row.cell("項目")
                    row.cell("数量")
                    row.cell("単価")
                    row.cell("金額")
                row = table.row()
                row.cell(data_row["項目"])
                row.cell(data_row["数量"])
                row.cell(f"¥{int(data_row['単価']):,}")
                row.cell(f"¥{int(data_row['金額']):,}")
                sub_total_amount += int(data_row["金額"])
            row = table.row()
            row.cell("小計")
            row.cell("")
            row.cell("")
            row.cell(f"¥{sub_total_amount:,}")

            row = table.row()
            row.cell("消費税")
            row.cell("")
            row.cell("")
            row.cell(f"¥{int(sub_total_amount * tax_rate):,}")

            row = table.row()
            row.cell("合計")
            row.cell("")
            row.cell("")
            total_amount = sub_total_amount + (sub_total_amount * tax_rate)
            row.cell(f"¥{int(total_amount):,}")
            # total_amount を切り上げ
            return math.ceil(total_amount)

# -------------------------こっからメイン処理-------------------------------
customer_company_name = "hogehoge"
my_company_name = "Hoge Inc."
quotations_title = "各種加工見積もりの件"
quotation_items = [
    {"項目": "アイテム1", "数量": "1", "単価": "1000", "金額": "1000"},
    {"項目": "アイテム2", "数量": "2", "単価": "10000", "金額": "20000"},
    {"項目": "アイテム3", "数量": "10", "単価": "1000", "金額": "10000"},
]
account_user_name = "hogetarou"
company_address = "hoge県foo市1-1-1"
font_family = "NotoSansJP-Regular"
font_path = "font\\NotoSansJP-Regular.ttf"

pdf = PDF()
pdf.add_font(font_family, fname=font_path)
pdf.set_font(font_family, size=10)

pdf.set_title(f"{customer_company_name}様　お見積もり書")
pdf.set_author(my_company_name)

pdf.add_page()
pdf.見積もり日()
pdf.見積もり番号()
pdf.見積書タイトル()
pdf.set_font(font_family, size=10)
pdf.顧客宛名(customer_company_name)
pdf.見積もり件名(quotations_title)
pdf.見積もり期限(30)
pdf.見積もり会社(my_company_name, company_address, account_user_name)
total_amount = pdf.見積もり明細(data=quotation_items)
pdf.見積もり金額(total_amount)

pdf.output("quotation.pdf")

