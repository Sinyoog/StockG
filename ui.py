import sys
import os
import math  # 📌 누락된 math 모듈 추가
import json
import re
from datetime import datetime, timedelta
from pyqtgraph import AxisItem
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QFrame, QTextEdit, QDialog, 
                             QLineEdit, QMessageBox, QSizePolicy)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QColor, QFont
import pyqtgraph as pg
from g import StockGameEngine

# --- [1] 그룹사 전용 창 (비모달 & 실시간 갱신 지원) ---
class GroupInfoDialog(QDialog):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("🏢 글로벌 그룹사 경영 현황 (실시간)")
        self.resize(1500, 900)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout()
        
        # [상단 테이블] 그룹 순위 요약
        self.upper_label = QLabel("📊 [그룹사 경영 순위 요약]")
        self.upper_label.setStyleSheet("color: #00FF00; font-weight: bold; font-size: 15px;")
        layout.addWidget(self.upper_label)
        
        self.upper_table = QTableWidget(0, 4)
        self.upper_table.setFixedHeight(280)
        self.upper_table.setStyleSheet("QTableWidget { background-color: #000; color: #e0e0e0; gridline-color: #222; } QHeaderView::section { background-color: #222; color: #00FF00; }")
        layout.addWidget(self.upper_table)

        # [하단 테이블] 종목별 상세 현황
        self.lower_label = QLabel("📋 [그룹사별 상세 종목 현황]")
        self.lower_label.setStyleSheet("color: #00FF00; font-weight: bold; font-size: 15px; margin-top: 10px;")
        layout.addWidget(self.lower_label)
        
        self.lower_table = QTableWidget(0, 15)
        self.lower_table.setStyleSheet("QTableWidget { background-color: #000; color: #e0e0e0; gridline-color: #222; } QHeaderView::section { background-color: #222; color: #00FF00; }")
        layout.addWidget(self.lower_table)

        self.update_all_info()
        self.setLayout(layout)

    def update_all_info(self):
        """데이터 갱신 로직 (메인창 handle_next_day에 의해 호출됨)"""
        # 1. 그룹 데이터 계산
        group_list = []
        max_member_count = 0
        for gid, ginfo in self.engine.groups.items():
            members = [s for s in self.engine.stocks if s['meta'].get('group_id') == gid]
            if members:
                members.sort(key=lambda x: x['market_cap'], reverse=True)
                total_cap = sum(s['market_cap'] for s in members)
                if len(members) > max_member_count: max_member_count = len(members)
                group_list.append({'name': ginfo['name'], 'count': len(members), 'total_cap': total_cap, 'member_names': [s['meta']['c_name'] for s in members]})
        
        group_list.sort(key=lambda x: x['total_cap'], reverse=True)

        # 2. 상단 테이블 갱신
        base_headers = ["그룹 순위", "그룹명", "계열사", "그룹 시가총액 합계"]
        dyn_headers = [f"그룹 내 {i+1}위" for i in range(max_member_count)]
        self.upper_table.setColumnCount(len(base_headers + dyn_headers))
        self.upper_table.setHorizontalHeaderLabels(base_headers + dyn_headers)
        self.upper_table.setRowCount(len(group_list))
        
        for i, g in enumerate(group_list):
            row = [i+1, g['name'], f"{g['count']}개", f"{g['total_cap']:,.0f}원"] + g['member_names'] + ["-"] * (max_member_count - len(g['member_names']))
            for j, val in enumerate(row):
                it = QTableWidgetItem(str(val)); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if j == 3: it.setForeground(QColor("#FFD700"))
                if j == 4: it.setForeground(QColor("#00FF00"))
                self.upper_table.setItem(i, j, it)

        # 3. 하단 테이블 갱신
        gs = sorted([st for st in self.engine.stocks if st['meta'].get('group')], key=lambda x: x['market_cap'], reverse=True)
        self.lower_table.setRowCount(len(gs))
        
        for i, st in enumerate(gs):
            m = st['meta']
            raw_tier = m.get('tier', '소형주')
            size_tag = f"[{raw_tier[0]}]"
            
            row = [
                i+1, 
                size_tag, 
                f"[ {m['char']} ]", 
                m.get('group', '-'), 
                m['ind'], 
                m['c_name'], 
                f"{m['ind']}({m['sub']})", 
                f"{int(st['price']):,}원 ({st.get('rate',0.0):+.2f}%)", 
                f"{st['shares']:,}주", 
                f"{st['market_cap']:,.0f}원", 
                f"{m.get('treasury_share',0)*100:.1f}%", 
                f"{m.get('owner_share',0)*100:.1f}%", 
                f"{m.get('foreign_share',0)*100:.1f}%", 
                f"{m.get('inst_share',0)*100:.1f}%", 
                f"{m.get('retail_share',0)*100:.1f}%"
            ]
            
            for j, val in enumerate(row):
                it = QTableWidgetItem(str(val))
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                if j == 9 or (j == 1 and size_tag == "[대]"):
                    it.setForeground(QColor("#FFD700")) # 금색
                elif "+" in str(val):
                    it.setForeground(QColor("#FF4444"))
                elif "-" in str(val):
                    it.setForeground(QColor("#4444FF"))
                
                self.lower_table.setItem(i, j, it)

        for t in [self.upper_table, self.lower_table]:
            t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            t.resizeColumnsToContents()
            for col in range(t.columnCount()):
                t.setColumnWidth(col, t.columnWidth(col) + 25)

# -- 설정 다이로그 --
class SystemMenuDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hts = parent
        self.setWindowTitle("시스템 관리")
        self.setFixedSize(320, 320)
        self.setStyleSheet("background-color: #1a1a1a; color: white; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout()
        btn_style = """
            QPushButton { 
                background: #333; color: white; padding: 12px; 
                font-weight: bold; border-radius: 5px; border: 1px solid #444;
            }
            QPushButton:hover { background: #444; border: 1px solid #666; }
        """
        
        # 🛠️ 치트 콘솔 열기
        self.btn_cheat = QPushButton("🛠️ 디버그 콘솔 (치트)")
        self.btn_cheat.setStyleSheet(btn_style + "QPushButton { color: #00FF00; border: 1px solid #00FF00; }")
        self.btn_cheat.clicked.connect(self.open_cheat)

        # 데이터 초기화 버튼 (trigger_reset 함수 연결)
        self.btn_reset = QPushButton("데이터 초기화")
        self.btn_reset.setStyleSheet(btn_style + "QPushButton { color: #FF4444; }")
        self.btn_reset.clicked.connect(self.trigger_reset)

        self.btn_exit = QPushButton("게임 종료 (저장)")
        self.btn_exit.setStyleSheet(btn_style)
        self.btn_exit.clicked.connect(self.hts.save_and_exit)

        self.btn_close = QPushButton("돌아가기")
        self.btn_close.setStyleSheet(btn_style + "QPushButton { background: #222; }")
        self.btn_close.clicked.connect(self.close)

        layout.addWidget(QLabel("시스템 옵션을 선택하세요."))
        layout.addWidget(self.btn_cheat)
        layout.addWidget(self.btn_reset)
        layout.addWidget(self.btn_exit)
        layout.addSpacing(10)
        layout.addWidget(self.btn_close)
        self.setLayout(layout)

    def open_cheat(self):
        self.hide() # 메뉴 숨기기
        CheatConsoleDialog(self.hts).exec() # 치트창 띄우기
        self.close()

    def trigger_reset(self):
        """메뉴 창에서 직접 확인 창을 띄우고 초기화 실행"""
        msg = "모든 자산과 투자 기록이 영구적으로 파기됩니다.\n정말 초기화하시겠습니까?"
        dialog = CustomConfirmDialog("시스템 초기화 확인", msg, self.hts)
        
        # 확인창에서 승인 시 즉시 로직 실행 (두 번 클릭 방지)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.hts.reset_game_logic() 
            self.close()
        
# --- [2] 상장폐지 역사관 (비모달 & 실시간 갱신 지원) ---
class InfoTableDialog(QDialog):
    def __init__(self, title, headers, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle(title)
        self.resize(1300, 700)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout()
        self.table = QTableWidget(0, len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setStyleSheet("QTableWidget { background-color: #000; color: #e0e0e0; gridline-color: #222; } QHeaderView::section { background-color: #222; color: #00FF00; }")
        
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.table.cellClicked.connect(self.on_cell_clicked)
        self.refresh_data()

    def refresh_data(self):
        """상장폐지 데이터를 다시 불러와서 테이블을 채움 (뉴스 함수 호출 금지!)"""
        delisted = getattr(self.engine, 'delisted_stocks', [])
        self.table.setRowCount(len(delisted))
        for i, st in enumerate(delisted):
            m = st['meta']
            row = [i+1, f"{m.get('listed_date')}~{m.get('delisted_date')}", "[소]", "[DELISTED]", 
                m.get('group', '-'), m['ind'], m['c_name'], f"{m['ind']}({m['sub']})", 
                f"{int(st['price']):,}원", f"{st['shares']:,}주", f"{m.get('treasury_share',0)*100:.1f}%"]
            for j, val in enumerate(row):
                it = QTableWidgetItem(str(val)); it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if "[DELISTED]" in str(val): it.setForeground(QColor("#FF4444"))
                self.table.setItem(i, j, it)
        
        # 테이블 간격 조정 로직 유지
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.resizeColumnsToContents()

    def on_cell_clicked(self, row, col):
        item = self.table.item(row, 6)
        if item:
            stock_name = item.text()
            stock_obj = next((s for s in self.engine.delisted_stocks if s['meta']['c_name'] == stock_name), None)
            
            if stock_obj:
                dialog = DelistedDetailDialog(stock_obj, self.engine, self)
                dialog.show()  # 📌 [수정] 모달리스(Modeless) 창으로 실행하여 다른 창 조작 가능

# --- [3] 실적 조회 창 (비모달 지원) ---
class EarningsDialog(QDialog):
    def __init__(self, name, engine, parent=None):
        super().__init__(parent)
        self.name = name; self.engine = engine
        self.setWindowTitle(f"🔎 [실적 상세] {self.name}"); self.resize(700, 800)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout(); btn_lay = QHBoxLayout()
        self.year_in = QLineEdit(); self.year_in.setPlaceholderText("연도"); self.year_in.setFixedWidth(100)
        btn_style = "QPushButton { background: #333; color: white; padding: 5px; } QPushButton:hover { border: 1px solid #00FF00; }"
        
        btn_s = QPushButton("조회"); btn_s.clicked.connect(self.load_year); btn_s.setStyleSheet(btn_style)
        btn_c = QPushButton("현재"); btn_c.clicked.connect(self.load_cur); btn_c.setStyleSheet(btn_style)
        btn_a = QPushButton("전체"); btn_a.clicked.connect(self.load_all); btn_a.setStyleSheet(btn_style)
        
        btn_lay.addWidget(self.year_in); btn_lay.addWidget(btn_s); btn_lay.addStretch(); btn_lay.addWidget(btn_c); btn_lay.addWidget(btn_a)
        layout.addLayout(btn_lay); self.report = QTextEdit(); self.report.setReadOnly(True)
        self.report.setStyleSheet("background-color: #000; border: 1px solid #333; padding: 20px;"); layout.addWidget(self.report)
        self.setLayout(layout); self.load_cur()

    def make_table_html(self, year, data):
        html = f"<h2 style='color:#00FF00;'>📅 {year}년도 실적 공시 리포트</h2>"
        html += "<table border='1' style='border-collapse: collapse; width: 100%; color: white; font-size: 14px;'>"
        html += "<tr style='background-color: #222; color: #00FF00;'><th>분기</th><th>공시일</th><th>매출액</th><th>영업이익</th><th>당기순이익</th></tr>"
        all_h = self.engine.earnings_history.get(self.name, {})
        sorted_keys = [(y, q) for y in sorted(all_h.keys()) for q in ["1분기", "2분기", "3분기", "4분기"] if q in all_h[y]]
        
        for q_n in ["1분기", "2분기", "3분기", "4분기"]:
            if q_n in data:
                d = data[q_n]; rev_s = ""
                try:
                    curr_idx = sorted_keys.index((year, q_n))
                    if curr_idx > 0:
                        p_y, p_q = sorted_keys[curr_idx - 1]; p_rev = all_h[p_y][p_q]['revenue']
                        rev_s = " <b style='color:#FF4444;'>(↑)</b>" if d['revenue'] > p_rev else " <b style='color:#4444FF;'>(↓)</b>"
                except: pass
                op_status = f"({'흑자' if d['op_income'] > 0 else '적자'})"; net_status = f"({'흑자' if d['net_income'] > 0 else '적자'})"
                op_c = "#FF4444" if d['op_income'] > 0 else "#4444FF"; net_c = "#FF4444" if d['net_income'] > 0 else "#4444FF"
                html += f"<tr style='text-align: center;'><td>{q_n}</td><td>{d['date']}</td><td>{d['revenue']:,.0f}원{rev_s}</td>"
                html += f"<td style='color:{op_c};'><b>{d['op_income']:,.0f}원 {op_status}</b></td><td style='color:{net_c};'><b>{d['net_income']:,.0f}원 {net_status}</b></td></tr>"
        return html + "</table><br/>"

    def load_year(self):
        y = self.year_in.text().strip(); h = self.engine.earnings_history.get(self.name, {})
        if y in h: self.report.setHtml(self.make_table_html(y, h[y]))
    def load_cur(self):
        y = str(self.engine.current_date.year); self.year_in.setText(y); self.load_year()
    def load_all(self):
        all_h = ""; h = self.engine.earnings_history.get(self.name, {})
        for y in sorted(h.keys()): all_h += self.make_table_html(y, h[y])
        self.report.setHtml(all_h)

# --- [4] 내 투자 창  ---
class MyInvestmentDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.hts = parent # 메인 윈도우 참조
        self.setWindowTitle("💰 내 투자 포트폴리오 (증권 계좌)")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout()

        self.summary_label = QLabel()
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.summary_label.setStyleSheet("""
            background-color: #1a1a1a; 
            border: 1px solid #333; 
            padding: 10px; 
            border-radius: 5px;
            margin-bottom: 5px;
        """)
        layout.addWidget(self.summary_label)

        self.label = QLabel("📊 실시간 보유 주식 상세 현황")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2ECC71;")
        layout.addWidget(self.label)
        
        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["종목명", "보유수량", "평균단가", "현재가", "매수금액", "평가금액", "수익률"])
        self.table.setStyleSheet("QTableWidget { background-color: #000; gridline-color: #222; } QHeaderView::section { background-color: #222; color: #2ECC71; }")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.cellClicked.connect(self.go_to_stock)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.update_info()

    def update_info(self, total_eval_value=None, total_profit=None, total_rate=None):
        """메인 HTS에서 계산된 데이터를 받아 요약 라벨과 테이블을 갱신"""
        
        if total_eval_value is None:
            total_buy = 0
            total_eval = 0
            for name, data in self.hts.my_portfolio.items():
                stock = next((s for s in self.hts.engine.stocks if s['meta']['c_name'] == name), None)
                cur_p = stock['price'] if stock else 0
                total_buy += data['shares'] * data['avg_price']
                total_eval += data['shares'] * cur_p
            
            total_eval_value = total_eval
            total_profit = total_eval_value - total_buy
            total_rate = (total_profit / total_buy * 100) if total_buy > 0 else 0.0

        p_color = "#FF4444" if total_profit > 0 else ("#4444FF" if total_profit < 0 else "#e0e0e0")
        
        summary_html = f"""
            <div align='center'>
                <table width='100%'><tr>
                    <td width='50%'>
                        <div style='background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333;'>
                            <span style='color:#888; font-size:12px;'>현재 투자 금액</span><br/>
                            <span style='color:{p_color}; font-size:24px; font-weight:bold;'>{int(total_eval_value):,}원</span>
                            <span style='color:{p_color}; font-size:16px;'> ({total_rate:+.2f}%)</span>
                        </div>
                    </td>
                    <td width='50%'>
                        <div style='background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-left: 10px;'>
                            <span style='color:#888; font-size:12px;'>보유 현금(예수금)</span><br/>
                            <span style='color:#FFD700; font-size:24px; font-weight:bold;'>{int(self.hts.my_cash):,}원</span>
                        </div>
                    </td>
                </tr></table>
            </div>
        """
        self.summary_label.setText(summary_html)

        portfolio = self.hts.my_portfolio
        self.table.setRowCount(len(portfolio))
        
        if not portfolio: 
            return

        for i, (name, data) in enumerate(portfolio.items()):
            stock_data = next((s for s in self.hts.engine.stocks if s['meta']['c_name'] == name), None)
            cur_price = float(stock_data['price']) if stock_data else 0
            shares, avg_p = data['shares'], data['avg_price']
            buy_total, eval_total = shares * avg_p, shares * cur_price
            profit_rate = ((cur_price / avg_p) - 1) * 100 if avg_p > 0 else 0.0
            
            items = [str(name), f"{shares:,}주", f"{int(avg_p):,}원", f"{int(cur_price):,}원", 
                     f"{int(buy_total):,}원", f"{int(eval_total):,}원", f"{profit_rate:+.2f}%"]
            
            for j, text in enumerate(items):
                it = QTableWidgetItem(text)
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if j == 6:
                    it.setForeground(QColor("#FF4444" if profit_rate > 0 else ("#4444FF" if profit_rate < 0 else "#e0e0e0")))
                self.table.setItem(i, j, it)

    def go_to_stock(self, r, c):
        # 1. 클릭한 테이블의 종목명 가져오기
        stock_name = self.table.item(r, 0).text()
        self.hts.selected_stock_name = stock_name
        
        # 2. 검색창 초기화 및 메인 HTS의 종목 테이블에서 해당 종목 선택 및 강조
        self.hts.search_search_search_bar_text_silent = True # 무한 루프 방지용 (필요시)
        self.hts.search_bar.clear()
        
        # 3. 테이블에서 종목을 찾아 스크롤 이동 및 활성화
        for i in range(self.hts.stock_table.rowCount()):
            item = self.hts.stock_table.item(i, 0)
            if item and item.text() == stock_name:
                self.hts.stock_table.setCurrentCell(i, 0)
                self.hts.on_stock_clicked(i, 0) # 클릭 이벤트 강제 실행
                break
                
        self.hts.scroll_to_selected()

# -- [5] 매매 수량 창 --
class TradeDialog(QDialog):
    def __init__(self, mode, stock_name, price, limit, hts_parent):
        super().__init__(hts_parent)
        self.hts = hts_parent
        self.mode = mode
        self.stock_name = stock_name
        self.price = price  # 이 값은 이제 실시간으로 변합니다
        self.limit = limit
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        
        self.setWindowTitle(f"💸 {self.mode} - {self.stock_name}")
        self.setFixedWidth(350)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        layout = QVBoxLayout()
        info_color = "#FF4444" if mode == "매수" else "#4444FF"
        
        title = QLabel(f"[{self.mode}] {self.stock_name}")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {info_color};")
        layout.addWidget(title)
        
        # 가격 표시 라벨 (실시간 업데이트를 위해 self로 선언)
        self.price_label = QLabel(f"현재가: {int(self.price):,}원")
        layout.addWidget(self.price_label)
        
        self.limit_label = QLabel(f"가능 수량: {limit:,}주")
        layout.addWidget(self.limit_label)
        
        input_lay = QHBoxLayout()
        self.amount_input = QLineEdit("1")
        self.amount_input.setStyleSheet("background-color: #222; color: #00FF00; font-size: 20px; font-weight: bold; border: 1px solid #444; height: 40px; padding-left: 10px;")
        self.amount_input.textChanged.connect(self.update_total)
        
        btn_max = QPushButton("MAX")
        btn_max.setFixedSize(60, 40)
        btn_max.setStyleSheet("background-color: #333; color: #FFD700; font-weight: bold; border: 1px solid #555;")
        btn_max.clicked.connect(self.set_max)
        
        input_lay.addWidget(self.amount_input); input_lay.addWidget(btn_max); layout.addLayout(input_lay)
        
        self.total_label = QLabel(f"총 금액: {int(self.price):,}원")
        self.total_label.setStyleSheet("font-size: 15px; color: #FFD700; margin-top: 10px; font-weight: bold;")
        layout.addWidget(self.total_label)
        
        self.btn_confirm = QPushButton(f"{self.mode} 확정")
        self.btn_confirm.setFixedHeight(45)
        self.btn_confirm.setStyleSheet(f"background-color: {info_color}; color: white; font-weight: bold; font-size: 16px; border-radius: 5px;")
        self.btn_confirm.clicked.connect(self.execute_trade)
        layout.addWidget(self.btn_confirm)
        self.setLayout(layout)

    def set_max(self):
        self.amount_input.setText(str(self.limit))

    def update_total(self, text):
        try:
            val = int(text) if text else 0
            if val > self.limit: 
                val = self.limit
                self.amount_input.setText(str(val))
            self.total_label.setText(f"총 금액: {int(self.price * val):,}원")
        except: pass

    def execute_trade(self):
        amount = int(self.amount_input.text() if self.amount_input.text() else 0)
        if amount <= 0: return
        if self.mode == "매수":
            self.hts.process_buy(self.stock_name, self.price, amount)
        else:
            self.hts.process_sell(self.stock_name, self.price, amount)
        self.update_info()

    def update_info(self):
        """[핵심] NEXT DAY 클릭 시 엔진에서 바뀐 가격을 가져와서 UI 갱신"""
        # 엔진에서 해당 종목의 최신 데이터 찾기
        stock_data = next((s for s in self.hts.engine.stocks if s['meta']['c_name'] == self.stock_name), None)
        if stock_data:
            self.price = stock_data['price'] # 최신 가격으로 업데이트
            self.price_label.setText(f"현재가: {int(self.price):,}원")
        
        # 가능 수량 갱신
        if self.mode == "매수":
            self.limit = self.hts.my_cash // self.price
        else:
            p = self.hts.my_portfolio.get(self.stock_name, {'shares': 0})
            self.limit = p['shares']
        
        self.limit_label.setText(f"가능 수량: {self.limit:,}주")
        self.update_total(self.amount_input.text())

    def get_amount(self):
        text = self.amount_input.text()
        return int(text) if text and text.isdigit() else 0

class StockFilterDialog(QDialog):
    def __init__(self, hts_parent):
        super().__init__(hts_parent)
        self.hts = hts_parent
        self.setWindowTitle("⚙️ 종목 상세 검색 필터")
        self.resize(500, 450)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        self.setModal(False)
        
        layout = QVBoxLayout()
        
        # 1. 체급 필터 그룹화
        tier_layout = QHBoxLayout()
        tier_layout.addWidget(QLabel("<b>체급:</b>"))
        
        # 버튼 객체 생성
        self.tier_all = QPushButton("전체")
        self.tier_all.setCheckable(True)
        self.tier_all.setChecked(True) # 기본값 전체 켜기
        
        self.tier_large = QPushButton("대형주")
        self.tier_large.setCheckable(True)
        
        self.tier_mid = QPushButton("중형주")
        self.tier_mid.setCheckable(True)
        
        self.tier_small = QPushButton("소형주")
        self.tier_small.setCheckable(True)
        
        # 버튼 그룹 묶기
        from PyQt6.QtWidgets import QButtonGroup
        self.tier_group = QButtonGroup(self)
        self.tier_group.setExclusive(False) # 여러 개 선택 가능하도록 설정하거나 필요 시 단일 선택
        
        # 버튼 추가
        self.tier_group.addButton(self.tier_all)
        self.tier_group.addButton(self.tier_large)
        self.tier_group.addButton(self.tier_mid)
        self.tier_group.addButton(self.tier_small)
        
        for btn in [self.tier_all, self.tier_large, self.tier_mid, self.tier_small]:
            btn.setStyleSheet("QPushButton:checked { color: #00FF00; font-weight:bold; border: 1px solid #00FF00; }")
            # 연결 시 시그널 람다로 전체 <-> 개별 토글 상호작용 구현
            btn.clicked.connect(self.on_filter_changed)
            tier_layout.addWidget(btn)
            
        layout.addLayout(tier_layout)
        
        # 2. 그룹 여부 필터
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("<b>그룹사:</b>"))
        self.group_all = QPushButton("전체")
        self.group_all.setCheckable(True)
        self.group_all.setChecked(True)
        self.group_yes = QPushButton("계열사만")
        self.group_yes.setCheckable(True)
        self.group_no = QPushButton("단독기업")
        self.group_no.setCheckable(True)
        
        for btn in [self.group_all, self.group_yes, self.group_no]:
            btn.setStyleSheet("QPushButton:checked { color: #00FF00; font-weight:bold; border: 1px solid #00FF00; }")
            btn.clicked.connect(self.on_filter_changed)
            group_layout.addWidget(btn)
        layout.addLayout(group_layout)
        
        # 3. 상세 가격 필터
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("<b>가격대:</b>"))
        self.price_min = QLineEdit()
        self.price_min.setPlaceholderText("최소(원)")
        self.price_min.setStyleSheet("background: #111; color: #00FF00; padding: 5px; border: 1px solid #333;")
        self.price_min.textChanged.connect(self.on_filter_changed)
        
        self.price_max = QLineEdit()
        self.price_max.setPlaceholderText("최대(원)")
        self.price_max.setStyleSheet("background: #111; color: #00FF00; padding: 5px; border: 1px solid #333;")
        self.price_max.textChanged.connect(self.on_filter_changed)
        
        price_layout.addWidget(self.price_min)
        price_layout.addWidget(QLabel("~"))
        price_layout.addWidget(self.price_max)
        layout.addLayout(price_layout)
        
        # 4. 발행주식수 필터
        shares_layout = QHBoxLayout()
        shares_layout.addWidget(QLabel("<b>발행주식수:</b>"))
        self.shares_min = QLineEdit()
        self.shares_min.setPlaceholderText("최소(주)")
        self.shares_min.setStyleSheet("background: #111; color: #00FF00; padding: 5px; border: 1px solid #333;")
        self.shares_min.textChanged.connect(self.on_filter_changed)
        
        self.shares_max = QLineEdit()
        self.shares_max.setPlaceholderText("최대(주)")
        self.shares_max.setStyleSheet("background: #111; color: #00FF00; padding: 5px; border: 1px solid #333;")
        self.shares_max.textChanged.connect(self.on_filter_changed)
        
        shares_layout.addWidget(self.shares_min)
        shares_layout.addWidget(QLabel("~"))
        shares_layout.addWidget(self.shares_max)
        layout.addLayout(shares_layout)
        
        # 5. 산업군 필터 (다중 선택 버튼 목록)
        ind_layout = QHBoxLayout()
        ind_layout.addWidget(QLabel("<b>산업군:</b>"))
        
        self.ind_buttons = {}
        industries = [
            "IT", "에너지", "건강관리", "산업재", "소재", "자유소비재", 
            "커뮤니케이션", "금융", "필수소비재", "유틸리티", "부동산", "재건"
        ]
        
        ind_btn_layout = QHBoxLayout()
        
        self.ind_all = QPushButton("전체")
        self.ind_all.setCheckable(True)
        self.ind_all.setChecked(True)
        self.ind_all.setStyleSheet("QPushButton:checked { color: #00FF00; font-weight:bold; border: 1px solid #00FF00; }")
        self.ind_all.clicked.connect(self.on_ind_all_clicked)
        ind_btn_layout.addWidget(self.ind_all)
        
        for ind in industries:
            btn = QPushButton(ind)
            btn.setCheckable(True)
            btn.setChecked(False)
            btn.setStyleSheet("QPushButton:checked { color: #00FF00; font-weight:bold; border: 1px solid #00FF00; }")
            btn.clicked.connect(self.on_ind_button_clicked)
            ind_btn_layout.addWidget(btn)
            self.ind_buttons[ind] = btn
            
        layout.addLayout(ind_btn_layout)
        
        # 6. 섹터 필터
        sector_layout = QHBoxLayout()
        sector_layout.addWidget(QLabel("<b>섹터:</b>"))
        self.sec_all = QPushButton("전체")
        self.sec_all.setCheckable(True)
        self.sec_all.setChecked(True)
        self.sec_grow = QPushButton("Growth")
        self.sec_grow.setCheckable(True)
        self.sec_val = QPushButton("Value")
        self.sec_val.setCheckable(True)
        
        # 📌 누락된 2개 섹터 버튼 추가 생성
        self.sec_defensive = QPushButton("Defensive")
        self.sec_defensive.setCheckable(True)
        self.sec_theme = QPushButton("Theme")
        self.sec_theme.setCheckable(True)
        
        for btn in [self.sec_all, self.sec_grow, self.sec_val, self.sec_defensive, self.sec_theme]:
            btn.setStyleSheet("QPushButton:checked { color: #00FF00; font-weight:bold; border: 1px solid #00FF00; }")
            btn.clicked.connect(self.on_filter_changed)
            sector_layout.addWidget(btn)
        layout.addLayout(sector_layout)
        
        # 7. 필터 초기화 버튼
        self.btn_reset = QPushButton("필터 초기화")
        self.btn_reset.setStyleSheet("background: #222; color: #FF4444; padding: 10px; border-radius: 4px; font-weight: bold;")
        self.btn_reset.clicked.connect(self.reset_filters)
        layout.addWidget(self.btn_reset)

        # 8. 적용 및 닫기 버튼
        self.btn_close = QPushButton("적용 및 닫기")
        self.btn_close.setStyleSheet("background: #222; color: white; padding: 10px; border-radius: 4px; font-weight: bold;")
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)
        
        self.setLayout(layout)

    def on_filter_changed(self):
        """체급, 그룹사, 섹터 버튼의 상호 배타적 토글 로직 통일 및 즉시 반영"""
        sender = self.sender()
        
        # 1. 체급 필터 상호작용
        if sender in [self.tier_large, self.tier_mid, self.tier_small] and sender.isChecked():
            self.tier_all.setChecked(False)
        elif sender == self.tier_all and self.tier_all.isChecked():
            self.tier_large.setChecked(False)
            self.tier_mid.setChecked(False)
            self.tier_small.setChecked(False)

        # 2. 그룹사 필터 상호작용
        if sender == self.group_all and self.group_all.isChecked():
            self.group_yes.setChecked(False)
            self.group_no.setChecked(False)
        elif sender in [self.group_yes, self.group_no] and sender.isChecked():
            self.group_all.setChecked(False)
            
            # 계열사와 단독기업은 둘 중 하나만 선택되도록 상호 배타적 처리
            if sender == self.group_yes:
                self.group_no.setChecked(False)
            else:
                self.group_yes.setChecked(False)

        # 3. 섹터 필터 상호작용
        if sender in [self.sec_grow, self.sec_val, self.sec_defensive, self.sec_theme] and sender.isChecked():
            self.sec_all.setChecked(False)
        elif sender == self.sec_all and self.sec_all.isChecked():
            self.sec_grow.setChecked(False)
            self.sec_val.setChecked(False)
            self.sec_defensive.setChecked(False)
            self.sec_theme.setChecked(False)

        # 메인창 필터링 함수 즉시 실행
        self.hts.filter_stocks()

    def reset_filters(self):
        """모든 필터 조건을 초기 상태로 되돌림"""
        # 1. 체급 버튼 초기화
        self.tier_all.setChecked(True)
        self.tier_large.setChecked(False)
        self.tier_mid.setChecked(False)
        self.tier_small.setChecked(False)
        
        # 2. 그룹사 버튼 초기화
        self.group_all.setChecked(True)
        self.group_yes.setChecked(False)
        self.group_no.setChecked(False)
        
        # 3. 상세 가격 및 주식 수 입력 필드 초기화
        self.price_min.clear()
        self.price_max.clear()
        self.shares_min.clear()
        self.shares_max.clear()
        
        # 4. 산업군 버튼 초기화
        if hasattr(self, 'ind_buttons'):
            for btn in self.ind_buttons.values():
                btn.setChecked(False)
            self.ind_all.setChecked(True)
            
        # 5. 섹터 버튼 초기화
        self.sec_all.setChecked(True)
        self.sec_grow.setChecked(False)
        self.sec_val.setChecked(False)
        if hasattr(self, 'sec_defensive'):
            self.sec_defensive.setChecked(False)
            self.sec_theme.setChecked(False)
            
        # UI에 즉시 반영
        self.hts.filter_stocks()

    def closeEvent(self, event):
        # 부모(hts_parent)의 활성 다이얼로그 리스트에서 자기 자신을 제거
        if self.hts and hasattr(self.hts, 'active_dialogs'):
            if self in self.hts.active_dialogs:
                self.hts.active_dialogs.remove(self)
        event.accept()

    def on_ind_all_clicked(self):
        """산업군 전체 버튼 클릭 시 개별 버튼 해제"""
        if self.ind_all.isChecked():
            for btn in self.ind_buttons.values():
                btn.setChecked(False)
        self.hts.filter_stocks()

    def on_ind_button_clicked(self):
        """개별 산업군 버튼 클릭 시 전체 버튼 해제 및 필터링"""
        # 개별 버튼이 하나라도 눌리면 '전체' 버튼 해제
        any_checked = any(btn.isChecked() for btn in self.ind_buttons.values())
        self.ind_all.setChecked(not any_checked)
        
        self.hts.filter_stocks()

class DateAxisItem(pg.AxisItem):
    def __init__(self, dates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates = dates  # 날짜 리스트 (datetime 객체들)

    def tickStrings(self, values, scale, spacing):
        # 축에 표시될 숫자(인덱스)를 실제 날짜 문자열로 변환
        return [self.dates[int(v)].strftime('%y-%m-%d') if 0 <= int(v) < len(self.dates) else "" for v in values]
    
# --- [6] 메인 HTS 클래스 (전체 통합 및 실시간 관리) ---
class StockHTS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = StockGameEngine()

        self.auto_speed_days = 1  # 기본값은 1일
        self.current_loop = 0
        self.is_auto_running = False
        self.has_paid_news_access = False
        self.next_billing_date = None
        
        saved_player = self.engine.load_game()
        
        # ui.py 내 데이터 로드 부분
        if saved_player:
            self.my_cash = saved_player["my_cash"]
            self.my_portfolio = saved_player["my_portfolio"]

            # 🚀 [수정 핵심] 엔진(g.py)에 저장된 구독 정보를 UI 변수로 강제 복사
            # 이 부분이 누락되거나 False가 되면 news.py에서 뉴스가 하나도 안 뜹니다.
            self.has_paid_news_access = getattr(self.engine, 'has_paid_news_access', False)
            self.next_billing_date = getattr(self.engine, 'next_billing_date', None)

            # 기존에 있던 로그 출력 및 장 오픈 로직
            print(f"✅ {self.engine.current_date.strftime('%Y-%m-%d')} 데이터를 성공적으로 불러왔습니다.")
            
            if hasattr(self.engine, 'virtual_weekday') and self.engine.virtual_weekday <= 4:
                self.engine.is_market_open = True
                print("🚀 [시스템] 저장된 데이터가 평일이므로 시장을 엽니다.")
        else:
            self.engine.initialize_market()
            self.my_cash = 1000000 
            self.my_portfolio = {}
            print("🚀 신규 게임 세션을 시작합니다.")

        self.selected_stock_name = ""
        self.current_tf = "1일"
        self.TF_LIMITS = {"1일": 1, "1주": 7, "1달": 30, "3달": 90, "1년": 365, "5년": 1260, "전체": 999999}
        self.active_dialogs = []
        
        self.init_ui()
        self.sync_ui_with_engine()

    def open_stock_filter_window(self):
        existing_dialog = next((d for d in self.active_dialogs if isinstance(d, StockFilterDialog)), None)
        
        if existing_dialog:
            existing_dialog.raise_()
            existing_dialog.activateWindow()
        else:
            dialog = StockFilterDialog(self)
            self.active_dialogs.append(dialog)
            dialog.show()

    def open_news_window(self):
        try:
            from news import NewsWindow
        except ImportError:
            QMessageBox.critical(self, "파일 오류", "news.py 파일을 찾을 수 없습니다.")
            return

        # [수정] 이미 열려있는 뉴스창 인스턴스가 있는지 확인
        existing_nw = next((d for d in self.active_dialogs if d.__class__.__name__ == "NewsWindow"), None)

        if existing_nw:
            try:
                # 창이 존재하면 데이터를 새로고침하고 맨 앞으로 가져옴
                existing_nw.refresh_data()
                existing_nw.raise_()
                existing_nw.activateWindow()
                existing_nw.show()
                return
            except RuntimeError:
                # 창이 파괴되었는데 리스트에 남아있는 경우 방어 로직
                self.active_dialogs.remove(existing_nw)

        # 새 창 생성
        nw = NewsWindow(self, self.engine, self)
        self.active_dialogs.append(nw)
        nw.show()

    def init_ui(self):
        self.setWindowTitle("G.PY Economic System Sync v10.0")
        self.resize(1800, 950)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # --- [대시보드 영역 시작] ---
        self.dashboard = QFrame()
        self.dashboard.setStyleSheet("background-color: #000; border: 1px solid #333; border-radius: 5px;")
        dash_lay = QVBoxLayout(self.dashboard)
        
        row1 = QHBoxLayout()
        self.date_label = QLabel()
        self.date_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FF00;")
        self.date_label.setWordWrap(False) 
        self.date_label.setMinimumWidth(300) 
        
        self.index_label = QLabel()
        self.index_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FF00; margin-left: 20px;")
        self.index_label.setMinimumWidth(550) 
        
        top_right_lay = QHBoxLayout()
        self.asset_label = QLabel() 
        self.asset_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.asset_label.setStyleSheet("color: white; font-family: 'Malgun Gothic'; border: none;")
        
        self.btn_system = QPushButton("✕")
        self.btn_system.setFixedSize(35, 35)
        self.btn_system.setStyleSheet("""
            QPushButton { 
                background: #222; color: white; font-size: 18px; border-radius: 5px; 
                font-weight: bold; border: 1px solid #444; 
            }
            QPushButton:hover { background: #FF4444; border: 1px solid #FF4444; }
        """)
        self.btn_system.clicked.connect(self.open_system_menu)
        
        top_right_lay.addWidget(self.asset_label)
        top_right_lay.addWidget(self.btn_system)

        row1.addWidget(self.date_label)
        row1.addWidget(self.index_label, stretch=1)
        row1.addLayout(top_right_lay) # 📌 [수정 완료] 올바른 변수명 적용
        dash_lay.addLayout(row1)
        
        self.macro_label = QLabel()
        self.macro_label.setStyleSheet("font-size: 14px; color: #00BFFF;")
        dash_lay.addWidget(self.macro_label)
        
        self.inflation_label = QLabel()
        self.inflation_label.setStyleSheet("font-size: 14px; color: #FFA500; font-weight: bold;")
        dash_lay.addWidget(self.inflation_label)
        
        main_layout.addWidget(self.dashboard)
        
        content_lay = QHBoxLayout()
        
        # [좌측 테이블 영역]
        left_panel = QVBoxLayout()
        search_lay = QHBoxLayout()
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 회사명 검색...")
        self.search_bar.setStyleSheet("background-color: #222; color: white; border: 1px solid #444; height: 30px; padding-left: 10px; font-weight: bold;")
        self.search_bar.textChanged.connect(self.filter_stocks)
        
        self.btn_filter_popup = QPushButton("⚙️ 상세 필터")
        self.btn_filter_popup.setFixedSize(80, 30)
        self.btn_filter_popup.setStyleSheet("""
            QPushButton { background: #333; color: #00FF00; font-weight: bold; border: 1px solid #444; border-radius: 3px; }
            QPushButton:hover { border: 1px solid #00FF00; }
        """)
        self.btn_filter_popup.clicked.connect(self.open_stock_filter_window)
        
        search_lay.addWidget(self.search_bar)
        search_lay.addWidget(self.btn_filter_popup)
        left_panel.addLayout(search_lay)
        
        self.stock_table = QTableWidget(0, 3)
        self.stock_table.setHorizontalHeaderLabels(["종목명", "현재가", "등락율"])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.stock_table.cellClicked.connect(self.on_stock_clicked)
        left_panel.addWidget(self.stock_table)
        
        content_lay.addLayout(left_panel, 2)

        # [중앙 차트]
        chart_lay = QVBoxLayout()
        self.chart_widget = pg.PlotWidget()
        self.chart_widget.setBackground('#000000')
        self.chart_widget.setMouseEnabled(x=False, y=False)
        self.chart_widget.setMenuEnabled(False)
        self.chart_widget.hideButtons()

        self.curve = self.chart_widget.plot(pen=pg.mkPen(color='#00FF00', width=2))
        self.baseline = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen('#555', width=1, style=Qt.PenStyle.DashLine))
        self.chart_widget.addItem(self.baseline)
        chart_lay.addWidget(self.chart_widget)
        
        tab_lay = QHBoxLayout()
        self.tabs = {}
        t_style = "QPushButton { background: #222; color: #888; border: 1px solid #444; padding: 5px; border-radius: 3px; } QPushButton:checked { background: #000; color: #00FF00; font-weight: bold; border: 2px solid #00FF00; }"
        
        for tf in self.TF_LIMITS.keys():
            btn = QPushButton(tf)
            btn.setCheckable(True)
            btn.setFixedWidth(55)
            btn.setStyleSheet(t_style)
            if tf == "1일": btn.setChecked(True)
            btn.clicked.connect(lambda ch, t=tf: self.change_tf(t))
            tab_lay.addWidget(btn)
            self.tabs[tf] = btn
        
        self.change_summary_label = QLabel()
        self.change_summary_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        tab_lay.addStretch()
        tab_lay.addWidget(self.change_summary_label)
        chart_lay.addLayout(tab_lay)
        content_lay.addLayout(chart_lay, 5)
        
        # [우측 리포트 및 매매 버튼]
        rep_lay = QVBoxLayout()
        self.report_panel = QTextEdit()
        self.report_panel.setReadOnly(True)
        self.report_panel.setStyleSheet("background-color: #000; color: #e0e0e0; border: 1px solid #333; font-size: 13px;")
        rep_lay.addWidget(self.report_panel, 1)
        
        # 📌 [추가] 우측 패널 내 보유 현황 테이블
        self.holding_table = QTableWidget(1, 4)
        self.holding_table.setFixedHeight(50)
        self.holding_table.setHorizontalHeaderLabels(["평균단가", "보유수량", "수익률", "총 금액"])
        self.holding_table.setStyleSheet("""
            QTableWidget { background-color: #111; border: 1px solid #333; gridline-color: #222; }
            QHeaderView::section { background-color: #222; color: #aaa; font-size: 11px; }
        """)
        self.holding_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.holding_table.verticalHeader().setVisible(False)
        
        for j in range(4):
            item = QTableWidgetItem("-")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.holding_table.setItem(0, j, item)
            
        rep_lay.addWidget(self.holding_table)
        
        trade_lay = QHBoxLayout()
        self.btn_buy = QPushButton("🔴 주식 매수")
        self.btn_buy.setFixedHeight(40)
        self.btn_buy.setStyleSheet("QPushButton { background-color: #C0392B; color: white; font-weight: bold; border-radius: 3px; } QPushButton:hover { background-color: #E74C3C; }")
        self.btn_buy.clicked.connect(self.handle_buy)
        
        self.btn_sell = QPushButton("🔵 주식 매도")
        self.btn_sell.setFixedHeight(40)
        self.btn_sell.setStyleSheet("QPushButton { background-color: #2980B9; color: white; font-weight: bold; border-radius: 3px; } QPushButton:hover { background-color: #3498DB; }")
        self.btn_sell.clicked.connect(self.handle_sell)
        
        trade_lay.addWidget(self.btn_buy)
        trade_lay.addWidget(self.btn_sell)
        rep_lay.addLayout(trade_lay)

        self.btn_earn = QPushButton("📊 실적 상세조회")
        self.btn_earn.setFixedHeight(35)
        self.btn_earn.setStyleSheet("QPushButton { background-color: #1a1a1a; color: #00FF00; border: 1px solid #00FF00; border-radius: 5px; }")
        self.btn_earn.clicked.connect(self.open_earnings_window)
        rep_lay.addWidget(self.btn_earn)
        content_lay.addLayout(rep_lay, 3)
        main_layout.addLayout(content_lay)
        
        btm_lay = QHBoxLayout()
        b_style = "QPushButton { background-color: #222; color: white; font-weight: bold; border: 1px solid #444; border-radius: 5px; padding: 12px; } QPushButton:hover { border: 1px solid #00FF00; }"
        
        self.btn_grp = QPushButton("🏢 그룹사 경영 현황 (전체)")
        self.btn_grp.setStyleSheet(b_style)
        self.btn_grp.clicked.connect(self.open_group_window)
        
        self.btn_del = QPushButton("💀 상장폐지 역사관 (전체)")
        self.btn_del.setStyleSheet(b_style)
        self.btn_del.clicked.connect(self.open_delisted_window)

        self.btn_news = QPushButton("📰 뉴스 보기")
        self.btn_news.setStyleSheet("QPushButton { background-color: #E67E22; color: white; font-weight: bold; border-radius: 5px; padding: 12px; }")
        self.btn_news.clicked.connect(self.open_news_window)
        
        self.btn_invest = QPushButton("💰 내 투자 (포트폴리오)")
        self.btn_invest.setStyleSheet("QPushButton { background-color: #2ECC71; color: black; font-weight: bold; border-radius: 5px; padding: 12px; }")
        self.btn_invest.clicked.connect(self.open_investment_window)
        
        self.btn_nxt = QPushButton("▶ NEXT DAY")
        self.btn_nxt.setFixedHeight(50)
        self.btn_nxt.setStyleSheet("QPushButton { background-color: #E67E22; color: white; font-weight: bold; border-radius: 5px; min-width: 300px; font-size: 16px; }")
        self.btn_nxt.clicked.connect(self.handle_next_day)
        
        btm_lay.addWidget(self.btn_grp, 1)
        btm_lay.addWidget(self.btn_del, 1)
        btm_lay.addWidget(self.btn_invest, 1)
        btm_lay.addWidget(self.btn_news, 1)
        btm_lay.addWidget(self.btn_nxt, 2)
        main_layout.addLayout(btm_lay)
        
        cont = QWidget()
        cont.setLayout(main_layout)
        self.setCentralWidget(cont)

    # ui.py 내 open_news_window 함수를 아래와 같이 완전히 교체하세요.
    def open_delisted_window(self):
        # 중복 방지 로직 추가
        existing_delisted = next((d for d in self.active_dialogs if isinstance(d, InfoTableDialog)), None)
        if existing_delisted:
            existing_delisted.raise_()
            existing_delisted.activateWindow()
            return

        headers = ["No", "생애 주기", "등급", "상태", "그룹", "섹터", "회사명", "산업분류", "마지막 주가", "발행주수", "자사주 %"]
        dialog = InfoTableDialog("💀 상장폐지 역사관", headers, self.engine, self)
        
        # 역사관도 다른 창과 같이 쓰려면 비모달 설정
        dialog.setModal(False)
        dialog.setWindowFlags(Qt.WindowType.Window)
        dialog.show() 
        
        self.active_dialogs.append(dialog)

    def _run_next_day_logic(self):
        # 1. 날짜를 넘기기 전에 기준가 업데이트
        if self.engine.is_market_open:
            for st in self.engine.stocks: 
                st['start_price'] = float(st['price'])
                
        # 2. 엔진 날짜 변경
        self.engine.next_day(silent=True)
        self.adjust_portfolio_for_splits()
        self.engine.record_current_state()

        # 🚀 [결제 로직] 창을 갱신하기 전에 오늘이 결제일인지 먼저 체크
        curr_now = self.engine.current_date.date()
        bill_date = self.next_billing_date

        if bill_date:
            # 날짜 객체 타입 정규화
            if isinstance(bill_date, str):
                bill_date = datetime.strptime(bill_date, '%Y-%m-%d').date()
            elif hasattr(bill_date, 'date'):
                bill_date = bill_date.date()

            # 오늘이 결제일이거나 지났다면 (자동 연장 시점)
            if curr_now >= bill_date:
                # 사용자가 '해지 예약'을 안 한 상태(has_paid_news_access == True)
                if getattr(self, 'has_paid_news_access', False):
                    if self.my_cash >= 1000000:
                        self.my_cash -= 1000000
                        # 📌 결제 성공: 오늘로부터 다시 30일 뒤로 결제일 연장
                        self.next_billing_date = self.engine.current_date + timedelta(days=30)
                        # 엔진 데이터와도 동기화
                        self.engine.next_billing_date = self.next_billing_date
                        print(f"💰 [자동결제] 구독 갱신 완료. 다음 결제일: {self.next_billing_date.date()}")
                    else:
                        # 돈 없으면 자동 해지
                        self.has_paid_news_access = False
                        self.engine.has_paid_news_access = False
                        print("⚠️ [자동결제] 잔액 부족으로 구독이 종료되었습니다.")
                # 해지 예약 상태(False)라면 여기서 연장 로직이 실행되지 않아 자연스럽게 만료됨

        # 3. 저장 로직
        if self.engine.virtual_weekday == 4:
            self.engine.save_game(self.my_cash, self.my_portfolio)
        
        # 4. UI 및 모든 활성 팝업 갱신 (결제가 완전히 끝난 뒤에 호출해야 함)
        self.sync_ui_with_engine()
        
        from news import NewsWindow 

        for dialog in self.active_dialogs[:]:
            try:
                if not dialog or not dialog.isVisible():
                    continue

                c_name = dialog.__class__.__name__

                if c_name == "NewsWindow":
                    if hasattr(dialog, 'refresh_data'):
                        dialog.refresh_data()
                elif c_name == "GroupInfoDialog":
                    dialog.update_all_info()
                elif c_name == "InfoTableDialog":
                    dialog.refresh_data()
                elif c_name == "EarningsDialog":
                    dialog.load_cur()
                elif c_name == "MyInvestmentDialog":
                    if hasattr(self, '_calculate_assets'):
                        total_eval, total_buy, total_prof, rate = self._calculate_assets()
                        dialog.update_info(total_eval, total_prof, rate)
                    else:
                        dialog.update_info()
                elif c_name == "TradeDialog":
                    dialog.update_info()

            except Exception as e:
                print(f"⚠️ {dialog} 갱신 실패: {e}")
                if dialog in self.active_dialogs:
                    self.active_dialogs.remove(dialog)

    def _calculate_assets(self):
        """현재 보유 포트폴리오를 기반으로 자산을 계산하는 내부 함수"""
        total_buy = 0
        total_eval = 0
        for name, data in self.my_portfolio.items():
            stock = next((s for s in self.engine.stocks if s['meta']['c_name'] == name), None)
            cur_p = stock['price'] if stock else 0
            total_buy += data['shares'] * data['avg_price']
            total_eval += data['shares'] * cur_p
        
        profit = total_eval - total_buy
        rate = (profit / total_buy * 100) if total_buy > 0 else 0.0
        return total_eval, total_buy, profit, rate

    # --- [시스템 관리 로직] ---
    def open_system_menu(self):
        menu = SystemMenuDialog(self)
        menu.exec()

    def save_and_exit(self):
        self.engine.save_game(self.my_cash, self.my_portfolio)
        QApplication.quit()

    # ui.py 내 StockHTS 클래스 안의 함수
    def reset_game_logic(self):
        """실제 초기화 수행 (DB, 파일, 메모리 변수, UI 잔상 전체 삭제)"""
        # 1. 기존 데이터 및 세이브 파일 삭제
        self.engine.clear_save_file()
        self.engine.clear_all_history()
        
        # 2. 엔진 객체 새로 생성 및 시장 초기화
        self.engine = StockGameEngine()
        self.engine.initialize_market(silent=False)
        
        # 3. 플레이어 자산 및 구독 정보 리셋 (메모리 변수)
        self.my_cash = 1000000 
        self.my_portfolio = {}
        self.selected_stock_name = "" 
        
        # 📌 구독제 관련 초기화 추가
        self.has_paid_news_access = False   # 구독 권한 리셋
        self.next_billing_date = None       # 구독 결제일 리셋
        self.engine.has_paid_news_access = False # 엔진 내 권한 리셋 (동기화)
        
        # 4. UI 텍스트 및 패널 초기화
        self.report_panel_text = ""
        self.report_panel.clear()
        self.change_summary_label.clear()
        self.curve.setData([]) # 차트 곡선 데이터 비우기
        
        # 5. 📌 차트 그래픽 잔상(최고/최저점 포인트 및 텍스트) 완벽 제거
        if hasattr(self, 'max_scatter'):
            try:
                self.chart_widget.removeItem(self.max_scatter)
                self.chart_widget.removeItem(self.min_scatter)
                self.chart_widget.removeItem(self.max_text)
                self.chart_widget.removeItem(self.min_text)
            except:
                pass # 이미 제거된 경우 무시
        
        # 6. 열려있는 모든 대화상자(뉴스, 역사관 등) 강제 종료 및 리스트 비우기
        for d in self.active_dialogs[:]:
            try:
                d.close() # closeEvent를 통해 active_dialogs에서 자동 제거됨
            except:
                pass
        self.active_dialogs.clear()
        
        # 7. UI 최종 동기화 (초기 상태 반영)
        self.sync_ui_with_engine()
        
        print("🚀 [시스템] 구독 정보, DB 히스토리 및 UI 잔상이 모두 초기화되었습니다.")

    # --- [매매 로직] ---
    def handle_buy(self):
        s = self.get_selected_stock_data()
        if not s: return
        max_shares = self.my_cash // s['price']
        dialog = TradeDialog("매수", s['meta']['c_name'], s['price'], int(max_shares), self)
        dialog.show() 
        self.active_dialogs.append(dialog)

    def process_buy(self, name, price, num):
        """매수 처리 후 즉시 UI 동기화 호출"""
        cost = price * num
        if self.my_cash < cost:
            QMessageBox.warning(self, "잔액 부족", "살 돈이 없습니다.")
            return
        
        self.my_cash -= cost # 현금 차감
        
        if name not in self.my_portfolio:
            self.my_portfolio[name] = {'shares': 0, 'avg_price': 0}
        
        p = self.my_portfolio[name]
        total_cost = (p['shares'] * p['avg_price']) + cost
        p['shares'] += num
        p['avg_price'] = total_cost / p['shares']
        
        # [중요] 계산 직후 UI를 다시 그려서 즉시 반영되게 함
        self.sync_ui_with_engine()
        self.engine.save_game(self.my_cash, self.my_portfolio)

    def handle_sell(self):
        s = self.get_selected_stock_data()
        if not s: return
        name = s['meta']['c_name']
        if name not in self.my_portfolio:
            return QMessageBox.warning(self, "보유량 부족", "팔 주식이 없습니다.")
        max_sell = self.my_portfolio[name]['shares']
        dialog = TradeDialog("매도", name, s['price'], max_sell, self)
        dialog.show()
        self.active_dialogs.append(dialog)

    def process_sell(self, name, price, num):
        if name not in self.my_portfolio or self.my_portfolio[name]['shares'] < num:
            QMessageBox.warning(self, "보유량 부족", "팔 수 있는 주식이 부족합니다.")
            return
        self.my_cash += price * num
        self.my_portfolio[name]['shares'] -= num
        if self.my_portfolio[name]['shares'] <= 0:
            del self.my_portfolio[name]
        self.sync_ui_with_engine()
        self.engine.save_game(self.my_cash, self.my_portfolio) # 💾 자동 저장

    # --- [창 열기 로직] ---
    def open_group_window(self):
        dialog = GroupInfoDialog(self.engine, self)
        dialog.show(); self.active_dialogs.append(dialog)

    def open_delisted_window(self):
        headers = ["No", "생애 주기", "등급", "상태", "그룹", "섹터", "회사명", "산업분류", "마지막 주가", "발행주수", "자사주 %"]
        dialog = InfoTableDialog("💀 상장폐지 역사관", headers, self.engine, self)
        dialog.show(); self.active_dialogs.append(dialog)

    def open_earnings_window(self):
        if self.selected_stock_name:
            dialog = EarningsDialog(self.selected_stock_name, self.engine, self)
            dialog.show(); self.active_dialogs.append(dialog)

    def open_investment_window(self):
        dialog = MyInvestmentDialog(self)
        dialog.show(); self.active_dialogs.append(dialog)

    # --- [시스템 로직 및 동기화] ---
    def handle_next_day(self):
        """SPEED 치트에 따라 1일 또는 N일을 자동으로 진행"""
        if self.is_auto_running: return 
        
        self.current_loop = 0
        self.is_auto_running = True
        self.btn_nxt.setEnabled(False) 
        
        # 반복 횟수 결정 (SPEED 치트값)
        loop_count = getattr(self, 'auto_speed_days', 1)
        
        if loop_count <= 1:
            self._run_next_day_logic()
            self.btn_nxt.setEnabled(True)
            self.is_auto_running = False
            self.auto_speed_days = 1 # 스피드 초기화
        else:
            self.auto_timer = QTimer()
            self.auto_timer.timeout.connect(self._auto_step)
            self.auto_timer.start(50)

    # StockHTS 클래스 내부에 추가
    def adjust_portfolio_for_splits(self):
        """엔진에서 발생한 분할/병합 정보를 바탕으로 사용자 자산을 보정합니다."""
        if not hasattr(self.engine, 'daily_splits') or not self.engine.daily_splits:
            return

        for name, ratio in list(self.engine.daily_splits.items()):
            if name in self.my_portfolio:
                data = self.my_portfolio[name]
                stock_data = self.get_selected_stock_data_by_name(name)
                if not stock_data: continue

                # 이론상 주식 수 (소수점 포함)
                theoretical_shares = data['shares'] * ratio
                
                # 실제 가질 주식 수 (무조건 내림)
                actual_shares = int(math.floor(theoretical_shares))
                
                # 단주(소수점) 계산 및 환급금 처리
                fractional_shares = theoretical_shares - actual_shares
                
                if fractional_shares > 0:
                    refund_raw = fractional_shares * stock_data['price']
                    final_refund = int(math.ceil(refund_raw)) # 무조건 올림
                    
                    self.my_cash += final_refund
                    print(f"💰 [{name}] 단주 처리: {fractional_shares:.4f}주 -> {final_refund:,}원 입금")

                # 포트폴리오 갱신
                data['shares'] = actual_shares
                data['avg_price'] = data['avg_price'] / ratio # 평단가 보정
                
                if data['shares'] <= 0:
                    del self.my_portfolio[name]
                    print(f"⚠️ [{name}] 병합 후 1주 미만이 되어 전량 환급 처리되었습니다.")

        # 보정 완료 후 엔진 기록 초기화
        self.engine.daily_splits = {}

    def get_selected_stock_data_by_name(self, name):
        return next((st for st in self.engine.stocks if st['meta']['c_name'] == name), None)
    
    def _auto_step(self):
        """타이머에 의해 반복 실행되는 로직"""
        if self.current_loop < self.auto_speed_days:
            self._run_next_day_logic()
            self.current_loop += 1
        else:
            self.auto_timer.stop()
            self.btn_nxt.setEnabled(True)
            self.is_auto_running = False
            print(f"🏁 {self.auto_speed_days}일간의 시뮬레이션이 완료되었습니다.")

    def _run_next_day_logic(self):
        # 1. 날짜를 넘기기 전에 기준가 업데이트
        if self.engine.is_market_open:
            for st in self.engine.stocks: 
                st['start_price'] = float(st['price'])
                
        # 2. 엔진 날짜 변경
        self.engine.next_day(silent=True)
        self.adjust_portfolio_for_splits()
        self.engine.record_current_state()

        # 🚀 [구독 자동 결제 시스템] 
        curr_now = self.engine.current_date.date()
        bill_date = self.next_billing_date

        if bill_date:
            # 날짜 객체 타입 정규화
            if isinstance(bill_date, str):
                bill_date = datetime.strptime(bill_date, '%Y-%m-%d').date()
            elif hasattr(bill_date, 'date'):
                bill_date = bill_date.date()

            # 📌 결제일 도달 시
            if curr_now >= bill_date:
                # 사용자가 '해지 예약'을 안 한 상태(has_paid_news_access == True)
                if getattr(self, 'has_paid_news_access', False):
                    if self.my_cash >= 1000000:
                        self.my_cash -= 1000000
                        # 30일 연장
                        self.next_billing_date = self.engine.current_date + timedelta(days=30)
                        # 🔥 핵심: 엔진의 구독 권한도 강제로 True 유지 (풀림 방지)
                        self.engine.has_paid_news_access = True
                        self.engine.next_billing_date = self.next_billing_date
                        print(f"💰 [자동결제] 구독 갱신 성공. 다음 결제일: {self.next_billing_date.date()}")
                    else:
                        # 돈 없으면 종료
                        self.has_paid_news_access = False
                        self.engine.has_paid_news_access = False
                        print("⚠️ [자동결제] 잔액 부족으로 구독이 만료되었습니다.")
                else:
                    # 해지 예약 상태였다면 여기서 권한 박탈
                    self.engine.has_paid_news_access = False
                    print("🚫 [구독] 해지 예약에 따라 프리미엄 서비스가 종료되었습니다.")

        # 3. 저장 로직
        if self.engine.virtual_weekday == 4:
            self.engine.save_game(self.my_cash, self.my_portfolio)
        
        # 4. UI 및 모든 활성 팝업 갱신
        self.sync_ui_with_engine()
        
        from news import NewsWindow 

        for dialog in self.active_dialogs[:]:
            try:
                if not dialog or not dialog.isVisible():
                    continue

                c_name = dialog.__class__.__name__

                if c_name == "NewsWindow":
                    if hasattr(dialog, 'refresh_data'):
                        dialog.refresh_data()
                elif c_name == "GroupInfoDialog":
                    dialog.update_all_info()
                elif c_name == "InfoTableDialog":
                    dialog.refresh_data()
                elif c_name == "EarningsDialog":
                    dialog.load_cur()
                elif c_name == "MyInvestmentDialog":
                    if hasattr(self, '_calculate_assets'):
                        total_eval, total_buy, total_prof, rate = self._calculate_assets()
                        dialog.update_info(total_eval, total_prof, rate)
                    else:
                        dialog.update_info()
                elif c_name == "TradeDialog":
                    dialog.update_info()

            except Exception as e:
                if dialog in self.active_dialogs:
                    self.active_dialogs.remove(dialog)

    def sync_ui_with_engine(self):
        """엔진 데이터를 UI에 직접 동기화하고 활성 창을 갱신합니다."""
        
        # 📌 [추가] 엔진의 virtual_weekday가 0~4(월~금)일 때 is_market_open이 True가 되도록 보정
        if hasattr(self.engine, 'virtual_weekday') and self.engine.virtual_weekday <= 4:
            self.engine.is_market_open = True
            
        is_open = getattr(self.engine, 'is_market_open', True)
        self.btn_buy.setEnabled(is_open)
        self.btn_sell.setEnabled(is_open)
        
        market_status = " [영업 중]" if is_open else " [장마감 - 휴장]"
        if hasattr(self, 'label_market_status'):
            self.label_market_status.setText(market_status)

        # 자산 계산 및 UI 갱신 로직
        total_buy_value = 0  
        total_eval_value = 0 
        for name, data in self.my_portfolio.items():
            stock = next((s for s in self.engine.stocks if s['meta']['c_name'] == name), None)
            cur_p = stock['price'] if stock else 0
            total_buy_value += data['shares'] * data['avg_price']
            total_eval_value += data['shares'] * cur_p

        total_profit = total_eval_value - total_buy_value
        total_rate = (total_profit / total_buy_value * 100) if total_buy_value > 0 else 0.0
        p_color = "#FF4444" if total_profit > 0 else ("#4444FF" if total_profit < 0 else "#e0e0e0")

        cash_box = f"""
            <div style='background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; min-width: 200px;'>
                <span style='color:#aaa; font-size:12px;'>보유 현금(예수금)</span><br/>
                <span style='color:#FFD700; font-size:26px; font-weight:bold;'>{int(self.my_cash):,}원</span><br/>
                <span style='color:#555; font-size:11px;'>출금 가능</span>
            </div>
        """
        invest_box = f"""
            <div style='background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 8px; margin-left: 10px; min-width: 240px;'>
                <span style='color:#aaa; font-size:12px;'>내 투자 금액</span><br/>
                <span style='color:{p_color}; font-size:26px; font-weight:bold;'>{int(total_eval_value):,}원</span><br/>
                <span style='color:{p_color}; font-size:14px; font-weight:bold;'>{int(total_profit):+,}원 ({total_rate:+.2f}%)</span>
            </div>
        """
        self.asset_label.setText(f"<div align='right'><table><tr><td>{cash_box}</td><td>{invest_box}</td></tr></table></div>")
        self.asset_label.setMinimumWidth(550)

        m = self.engine.macro
        wdays = ['월','화','수','목','금','토','일']
        w = wdays[self.engine.virtual_weekday]
        
        self.date_label.setText(f"📅 {self.engine.current_date.strftime('%Y-%m-%d')} ({w}){market_status}")
        self.index_label.setText(f"📊 GRI: {self.engine.gri:,.2f} | WSI: {self.engine.wsi:,.2f} | LV.{self.engine.max_tech_reached}")
        
        self.macro_label.setText(
            f"🌍 금리: {m['interest_rate']:.2f}% | 유가: ${m['oil_price']:.2f} | "
            f"물가: {m['cpi']:.2f}% | 환율: ₩{m['exchange_rate']:,.1f}"
        )
        self.inflation_label.setText(f"🛍️ 물가체감: 2000년 ₩1,000 → 현재 ₩{self.engine.base_item_price:,.0f}")

        self.filter_stocks()
        self.refresh_chart()
        
        # 📌 [핵심 수정] update_report 호출 전 최신 상태의 종목 데이터를 다시 바인딩
        s = self.get_selected_stock_data()
        if s:
            self.update_report()
        
        # ... 하단 보유 현황 갱신 로직 ...
        port_info = self.my_portfolio.get(self.selected_stock_name, None)
        if port_info:
            shares = port_info['shares']
            avg_price = port_info['avg_price']
            
            cur_price = s['price'] if s else 0
            eval_price = shares * cur_price
            rate = ((cur_price / avg_price) - 1) * 100 if avg_price > 0 else 0.0
            
            self.holding_table.item(0, 0).setText(f"{int(avg_price):,}원")
            self.holding_table.item(0, 1).setText(f"{shares:,}주")
            
            rate_text = f"{rate:+.2f}%"
            self.holding_table.item(0, 2).setText(rate_text)
            
            if rate > 0:
                self.holding_table.item(0, 2).setForeground(QColor("#FF4444"))
            elif rate < 0:
                self.holding_table.item(0, 2).setForeground(QColor("#4444FF"))
            else:
                self.holding_table.item(0, 2).setForeground(QColor("#e0e0e0"))
                
            self.holding_table.item(0, 3).setText(f"{int(eval_price):,}원")
        else:
            self.holding_table.item(0, 0).setText("-")
            self.holding_table.item(0, 1).setText("-")
            self.holding_table.item(0, 2).setText("-")
            self.holding_table.item(0, 3).setText("-")

        for dialog in self.active_dialogs[:]:
            try:
                if dialog and dialog.isVisible():
                    if isinstance(dialog, MyInvestmentDialog):
                        dialog.update_info(total_eval_value, total_profit, total_rate)
                    elif hasattr(dialog, 'update_info'):
                        dialog.update_info()
                else:
                    if dialog in self.active_dialogs:
                        self.active_dialogs.remove(dialog)
            except (RuntimeError, Exception):
                if dialog in self.active_dialogs:
                    self.active_dialogs.remove(dialog)
                
    def filter_stocks(self):
        """상세 필터 조건을 먼저 검사하도록 수정된 필터링 로직"""
        query = self.search_bar.text().strip().lower()
        snaps = self.engine.get_stock_snapshots()
        filtered = []
        
        f_dialog = next((d for d in self.active_dialogs if isinstance(d, StockFilterDialog)), None)

        for s in snaps:
            # 1. 상세 필터 조건 검사 (열려 있는 경우)
            if f_dialog and f_dialog.isVisible():
                # [체급 필터]
                if not f_dialog.tier_all.isChecked():
                    t_val = s['meta'].get('tier', '소형주')
                    matched = False
                    if f_dialog.tier_large.isChecked() and "대" in t_val: matched = True
                    if f_dialog.tier_mid.isChecked() and "중" in t_val: matched = True
                    if f_dialog.tier_small.isChecked() and "소" in t_val: matched = True
                    if not matched: continue
                
                # [그룹사 필터]
                if not f_dialog.group_all.isChecked():
                    has_group = s['meta'].get('group_id') is not None
                    if f_dialog.group_yes.isChecked() and not has_group: continue
                    if f_dialog.group_no.isChecked() and has_group: continue
                        
                # [가격대 필터]
                p_min = f_dialog.price_min.text()
                p_max = f_dialog.price_max.text()
                if p_min.isdigit() and s['price'] < int(p_min): continue
                if p_max.isdigit() and s['price'] > int(p_max): continue
                    
                # [발행주식수 필터]
                s_min = f_dialog.shares_min.text()
                s_max = f_dialog.shares_max.text()
                if s_min.isdigit() and s['shares'] < int(s_min): continue
                if s_max.isdigit() and s['shares'] > int(s_max): continue
                    
                # [산업군 필터]
                ind_selected = []
                for ind, btn in f_dialog.ind_buttons.items():
                    if btn.isChecked():
                        ind_selected.append(ind)
                        
                if not f_dialog.ind_all.isChecked() and len(ind_selected) > 0:
                    s_ind = s['meta'].get('ind', '').lower()
                    matched_ind = False
                    for sel in ind_selected:
                        if sel.lower() in s_ind:
                            matched_ind = True
                            break
                    if not matched_ind:
                        continue
                    
                # [섹터 필터]
                # [섹터 필터]
                if not f_dialog.sec_all.isChecked():
                    s_name = self.engine.SECTOR_MAP.get(s['meta'].get('ind'), "Value")
                    matched_sector = False
                    if f_dialog.sec_grow.isChecked() and s_name == "Growth": matched_sector = True
                    if f_dialog.sec_val.isChecked() and s_name == "Value": matched_sector = True
                    if f_dialog.sec_defensive.isChecked() and s_name == "Defensive": matched_sector = True
                    if f_dialog.sec_theme.isChecked() and s_name == "Theme": matched_sector = True

                    if not matched_sector:
                        continue

            # 2. 마지막으로 검색어 조건 검사
            if query not in s['name'].lower():
                continue

            filtered.append(s)

        self.update_table(filtered)
        if len(filtered) == 1:
            self.selected_stock_name = filtered[0]['name']

    def update_table(self, snps):
        self.stock_table.setRowCount(len(snps))
        for i, st in enumerate(snps):
            n_it = QTableWidgetItem(st['name']); p_it = QTableWidgetItem(f"{int(st['price']):,}원"); r_it = QTableWidgetItem(f"{st['rate']:+.2f}%")
            col = "#FF4444" if st['rate'] > 0 else ("#4444FF" if st['rate'] < 0 else "white")
            if st['name'] == self.selected_stock_name:
                n_it.setForeground(QColor("#00FF00")); n_it.setFont(QFont("Malgun Gothic", 10, QFont.Weight.Bold))
            p_it.setForeground(QColor(col)); r_it.setForeground(QColor(col))
            self.stock_table.setItem(i, 0, n_it); self.stock_table.setItem(i, 1, p_it); self.stock_table.setItem(i, 2, r_it)

    def on_stock_clicked(self, r, c):
        it = self.stock_table.item(r, 0)
        if it: 
            self.selected_stock_name = it.text()
            self.sync_ui_with_engine()

    def calculate_moving_average(self, data, window_size=3):
        """단기 변동성을 부드럽게 처리하는 단순 이동평균 함수"""
        if not data:
            return []
        smoothed = []
        for i in range(len(data)):
            start = max(0, i - window_size + 1)
            window = data[start:i+1]
            avg = sum(window) / len(window)
            smoothed.append(avg)
        return smoothed

    def refresh_chart(self):
        s = self.get_selected_stock_data()
        if not s:
            return
        name = s['meta']['c_name']
        
        lim = self.TF_LIMITS.get(self.current_tf, 1)
        fetch_days = 10000 if self.current_tf == "전체" else lim
        
        # 📌 1. DB에서 날짜(date)와 가격(price)을 한 번에 가져오기
        cur = self.engine.conn.cursor()
        if fetch_days > 900000:
            cur.execute("SELECT date, price FROM stock_history WHERE company_name = ? ORDER BY date ASC", (name,))
        else:
            cur.execute("SELECT date, price FROM stock_history WHERE company_name = ? ORDER BY date DESC LIMIT ?", (name, fetch_days))
        
        rows = cur.fetchall()
        if not rows: return
        
        if fetch_days <= 900000: 
            rows = rows[::-1] # 최신순을 과거순으로 정렬
        
        dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in rows]
        prices = [float(row[1]) for row in rows]

        # 📌 2. X축을 날짜 전용 축으로 교체
        self.chart_widget.setAxisItems({'bottom': DateAxisItem(dates=dates, orientation='bottom')})
        
        cur_p = float(s['price']) 

        if self.current_tf == "1일":
            rat_today = float(s.get('rate', 0))
            if rat_today == -100:
                base_p = cur_p
            else:
                base_p = cur_p / (1 + rat_today / 100) if (1 + rat_today / 100) != 0 else cur_p
            disp = [base_p, cur_p]
        else:
            # 📌 3. 기존 로직 유지 (prices 리스트 사용)
            base_p = prices[0]
            cur_p = prices[-1]
            count = len(prices)
            
            if count == 1:
                disp = [prices[0], prices[0]]
            else:
                if count < 180:
                    step = 1
                elif count < 1095:
                    step = 7
                elif count < 3650:
                    step = 30
                elif count < 14600:
                    step = 180
                else:
                    step = 365

                if step > 1:
                    disp = [prices[i] for i in range(0, count, step)]
                    if (count - 1) % step != 0:
                        disp.append(cur_p)
                else:
                    disp = [float(x) for x in prices]

        smoothed_disp = self.calculate_moving_average(disp, window_size=3)
        
        diff = cur_p - base_p
        actual_period_rate = (diff / base_p * 100) if base_p != 0 else 0
        
        if diff > 0:
            c_hex = "#FF4444"; sign = "▲"
        elif diff < 0:
            c_hex = "#4444FF"; sign = "▼"
        else:
            c_hex = "#e0e0e0"; sign = "─"
            
        self.curve.setPen(pg.mkPen(color=c_hex, width=2))
        self.baseline.setPos(base_p)
        self.curve.setData(smoothed_disp)

        if smoothed_disp:
            y_min = min(smoothed_disp)
            y_max = max(smoothed_disp)
            if y_min == y_max:
                y_range = max(1.0, y_min * 0.01)
                self.chart_widget.setYRange(y_min - y_range, y_max + y_range)
            else:
                self.chart_widget.setYRange(y_min, y_max)

        if hasattr(self, 'max_scatter'):
            self.chart_widget.removeItem(self.max_scatter)
            self.chart_widget.removeItem(self.min_scatter)
            self.chart_widget.removeItem(self.max_text)
            self.chart_widget.removeItem(self.min_text)

        if self.current_tf != "1일" and len(smoothed_disp) > 0:
            max_val = max(smoothed_disp)
            min_val = min(smoothed_disp)
            max_idx = smoothed_disp.index(max_val)
            min_idx = smoothed_disp.index(min_val)

            self.max_scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush('#FF4444'), symbol='o')
            self.max_scatter.addPoints([{'pos': (max_idx, max_val)}])
            self.chart_widget.addItem(self.max_scatter)

            self.min_scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush('#4444FF'), symbol='o')
            self.min_scatter.addPoints([{'pos': (min_idx, min_val)}])
            self.chart_widget.addItem(self.min_scatter)

            max_is_right = max_idx > (len(smoothed_disp) * 0.75)
            max_anchor = (1.1, 1.1) if max_is_right else (0, 1) 

            self.max_text = pg.TextItem(
                html=f"<span style='color: #FF4444; font-weight: bold; background-color: #000;'>최고: {int(max_val):,}</span>",
                anchor=max_anchor,
            )
            self.max_text.setPos(max_idx, max_val)
            self.chart_widget.addItem(self.max_text)

            min_is_left = min_idx < (len(smoothed_disp) * 0.25)
            min_is_right = min_idx > (len(smoothed_disp) * 0.75)
            
            if min_is_right:
                min_anchor = (1.1, -0.1)
            else:
                min_anchor = (-0.1, -0.1) if min_is_left else (0, 0)

            self.min_text = pg.TextItem(
                html=f"<span style='color: #4444FF; font-weight: bold; background-color: #000;'>최저: {int(min_val):,}</span>",
                anchor=min_anchor,
            )
            self.min_text.setPos(min_idx, min_val)
            self.chart_widget.addItem(self.min_text)

        summary_text = (
            f"<span style='color:#ffffff;'>{self.current_tf} 기준: </span>"
            f"<span style='color:#aaaaaa;'>{int(base_p):,}원</span>"
            f"<span style='color:#ffffff;'> → </span>"
            f"<span style='color:{c_hex}; font-weight:bold;'>{int(cur_p):,}원 </span>"
            f"<span style='color:{c_hex};'>({sign}{int(abs(diff)):,}원, {actual_period_rate:+.2f}%)</span>"
        )
        self.change_summary_label.setText(summary_text)

    def get_ui_chart_data(self, company_name, days=30):
        try:
            cur = self.conn.cursor()
            
            # 1. 90만 일 이상 (전체 보기) 조회 시
            if days > 900000:
                cur.execute("""
                    SELECT price FROM stock_history 
                    WHERE company_name = ? 
                    ORDER BY date ASC
                """, (company_name,))
                rows = cur.fetchall()
                return [row[0] for row in rows]
                
            else:
                # 2. 기간 조회 시 최근 N개의 데이터를 가져옴
                cur.execute("""
                    SELECT price FROM stock_history 
                    WHERE company_name = ? 
                    ORDER BY date DESC LIMIT ?
                """, (company_name, days))
                
                rows = cur.fetchall()
                if not rows: 
                    return []
                
                prices = [row[0] for row in rows]
                # 최신순에서 과거순으로 뒤집기
                return prices[::-1]
                
        except Exception as e:
            print(f"❌ DB 로드 실패: {e}")
            return []

    def get_delisted_stock_history(self, company_name):
        """상장폐지된 종목의 전체 기록을 DB에서 가져옴 (메모리 점유 0)"""
        cur = self.conn.cursor()
        cur.execute("SELECT price FROM stock_history WHERE company_name = ? ORDER BY date ASC", (company_name,))
        return [row[0] for row in cur.fetchall()]
    
    def scroll_to_selected(self):
        for i in range(self.stock_table.rowCount()):
            item = self.stock_table.item(i, 0)
            if item and item.text() == self.selected_stock_name:
                self.stock_table.scrollToItem(item, QTableWidget.ScrollHint.PositionAtCenter); break

    def change_tf(self, tf): 
        self.current_tf = tf
        for n, btn in self.tabs.items(): btn.setChecked(n == tf)
        self.refresh_chart()

    def get_selected_stock_data(self):
        return next((st for st in self.engine.stocks if st['meta']['c_name'] == self.selected_stock_name), None)

    def update_report(self):
        s = self.get_selected_stock_data()
        if not s: return
        m = s['meta']
        ts, os, fs, ins, rs = [m.get(k, 0)*100 for k in ['treasury_share', 'owner_share', 'foreign_share', 'inst_share', 'retail_share']]
        size = {"대형주": "[대기업]", "중형주": "[중견기업]", "소형주": "[중소기업]"}.get(m.get('tier', '소형주'), "[중소기업]")
        
        # 100% 기준으로 비율 정규화
        total_share = ts + os + fs + ins + rs
        if total_share > 0:
            ts_norm, os_norm, fs_norm, ins_norm, rs_norm = (
                ts / total_share * 100,
                os / total_share * 100,
                fs / total_share * 100,
                ins / total_share * 100,
                rs / total_share * 100
            )
        else:
            ts_norm, os_norm, fs_norm, ins_norm, rs_norm = ts, os, fs, ins, rs

        report = f"""
        <div style='font-family: Malgun Gothic;'>
            <h2 style='color:#00FF00; margin-bottom: 0px;'>&lt; {m['c_name']} &gt;</h2>
            <p style='color:#888; font-size: 11px; margin-top: 2px;'>상장일: {m['listed_date']} | 섹터: {self.engine.SECTOR_MAP.get(m['ind'], 'Value')}</p>
            <hr style='border: 0.5px solid #333;'/>
            <p style='font-size: 13px;'>
                <b>[기업 정보]</b><br/>
                그룹: {m.get('group','단독기업')}<br/>
                규모: <b style='color:#FFD700;'>{size}</b><br/>
                산업: {m['ind']} ({m['sub']})<br/>
                상태: <b style='color:#00FF00;'>{m['char']}</b>
            </p>
            <p style='font-size: 13px;'>
                <b>[발행 정보]</b><br/>
                주식수: {s['shares']:,} 주<br/>
                시총: {s['market_cap']:,} 원
            </p>
            <hr style='border: 0.5px solid #333;'/>
            <p style='font-size: 13px;'>
                <b>[지배구조]</b><br/>
                자사주: {ts_norm:.1f}% | 대주주: {os_norm:.1f}%<br/>
                외국인: {fs_norm:.1f}% | 기관 : {ins_norm:.1f}%<br/>
                개인 : {rs_norm:.1f}%
            </p>
            <p style='color: #FF4444; font-size: 14px;'><b>리스크: {m['risk_score']:.2f} / 150</b></p>
        </div>
        """
        self.report_panel.setHtml(report)

# -- 닫기 및 초기화 창 --
class CustomConfirmDialog(QDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(450, 220)
        
        # 🎨 HTS 테마 스타일시트
        self.setStyleSheet("""
            QDialog { 
                background-color: #0d0d0d; 
                border: 2px solid #333; 
            }
            QLabel { 
                color: #e0e0e0; 
                font-family: 'Malgun Gothic';
                font-size: 15px; 
            }
            QPushButton { 
                background-color: #222; 
                color: #fff; 
                border: 1px solid #444; 
                padding: 10px; 
                border-radius: 4px; 
                min-width: 100px;
                font-weight: bold;
            }
            QPushButton:hover { 
                border: 1px solid #00FF00; 
                color: #00FF00; 
                background-color: #111;
            }
            #warning_header { 
                color: #FF4444; 
                font-size: 18px; 
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 경고 헤더
        header = QLabel("⚠️ SYSTEM ALERT")
        header.setObjectName("warning_header")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # 본문 메시지
        self.msg_label = QLabel(message)
        self.msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_label.setWordWrap(True)
        layout.addWidget(self.msg_label)
        
        layout.addSpacing(20)
        
        # 버튼 영역
        btn_lay = QHBoxLayout()
        self.btn_yes = QPushButton("CONFIRM (초기화)")
        self.btn_no = QPushButton("CANCEL (취소)")
        
        btn_lay.addStretch()
        btn_lay.addWidget(self.btn_yes)
        btn_lay.addSpacing(10)
        btn_lay.addWidget(self.btn_no)
        btn_lay.addStretch()
        
        layout.addLayout(btn_lay)
        self.setLayout(layout)
        
        # 이벤트 연결
        self.btn_yes.clicked.connect(self.accept)
        self.btn_no.clicked.connect(self.reject)

class DelistedDetailDialog(QDialog):
    def __init__(self, stock_obj, engine, parent=None):
        super().__init__(parent, Qt.WindowType.Window)
        self.engine = engine
        self.s = stock_obj
        self.meta = stock_obj['meta']
        self.stock_name = self.meta['c_name']
        
        # 📌 [핵심] 메인 HTS의 current_tf를 참조하도록 연결
        if parent and hasattr(parent, 'current_tf'):
            self.current_tf = parent.current_tf
        else:
            self.current_tf = "전체"
        
        self.setWindowTitle(f"💀 [상장폐지 상세 기록] {self.stock_name}")
        self.resize(1400, 800)
        self.setStyleSheet("background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic';")
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # --- [1] 상단 헤더 영역 ---
        header_lay = QHBoxLayout()
        title_vbox = QVBoxLayout()
        
        title_sub_lay = QHBoxLayout()
        self.title_label = QLabel(f"< {self.stock_name} >")
        self.title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #00FF00; margin-bottom: 0px;")
        
        self.price_summary_label = QLabel("")
        self.price_summary_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-left: 20px; margin-top: 5px;")
        
        title_sub_lay.addWidget(self.title_label)
        title_sub_lay.addWidget(self.price_summary_label)
        title_sub_lay.addStretch()
        
        sector_name = self.engine.SECTOR_MAP.get(self.meta['ind'], 'Value')
        self.sub_title = QLabel(f"상장일: {self.meta.get('listed_date', '-')} | 폐지일: {self.meta.get('delisted_date', '-')} | 섹터: {sector_name}")
        self.sub_title.setStyleSheet("color: #888; font-size: 14px;")
        
        title_vbox.addLayout(title_sub_lay)
        title_vbox.addWidget(self.sub_title)
        
        header_lay.addLayout(title_vbox)
        header_lay.addStretch()
        
        self.btn_close = QPushButton("✕")
        self.btn_close.setFixedSize(40, 40)
        self.btn_close.setStyleSheet("""
            QPushButton { background: #222; color: white; font-size: 20px; border-radius: 5px; border: 1px solid #444; }
            QPushButton:hover { background: #FF4444; border: 1px solid #FF4444; }
        """)
        self.btn_close.clicked.connect(self.close)
        header_lay.addWidget(self.btn_close, alignment=Qt.AlignmentFlag.AlignTop)
        
        main_layout.addLayout(header_lay)
        
        # --- [2] 중앙 본문 영역 ---
        content_lay = QHBoxLayout()
        
        import pyqtgraph as pg
        self.chart_widget = pg.PlotWidget()
        self.chart_widget.setBackground('#000000')
        self.chart_widget.setMouseEnabled(x=False, y=False)
        self.chart_widget.hideButtons()
        
        self.curve = self.chart_widget.plot(pen=pg.mkPen(color='#5DADE2', width=2))
        content_lay.addWidget(self.chart_widget, 7)
        
        right_vbox = QVBoxLayout()
        
        self.report_panel = QTextEdit()
        self.report_panel.setReadOnly(True)
        self.report_panel.setStyleSheet("""
            QTextEdit { 
                background-color: #000; color: #e0e0e0; border: 1px solid #333; 
                font-size: 13px; padding: 10px; line-height: 1.5;
            }
        """)
        self.update_report_html()
        right_vbox.addWidget(self.report_panel, 4)
        
        self.earnings_table = QTableWidget(0, 4)
        self.earnings_table.setHorizontalHeaderLabels(["분기", "매출액 (원)", "영업이익 (원)", "순이익 (원)"])
        self.earnings_table.setStyleSheet("""
            QTableWidget { background-color: #000; color: #e0e0e0; gridline-color: #222; border: 1px solid #333; } 
            QHeaderView::section { background-color: #222; color: #00FF00; }
        """)
        self.earnings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_vbox.addWidget(self.earnings_table, 6)
        
        content_lay.addLayout(right_vbox, 3)
        
        main_layout.addLayout(content_lay)
        self.setLayout(main_layout)
        
        self.load_full_history()
        self.load_earnings_table()

    def update_report_html(self):
        m = self.meta
        ts, os, fs, ins, rs = [m.get(k, 0)*100 for k in ['treasury_share', 'owner_share', 'foreign_share', 'inst_share', 'retail_share']]
        total = ts + os + fs + ins + rs
        if total > 0:
            ts, os, fs, ins, rs = ts/total*100, os/total*100, fs/total*100, ins/total*100, rs/total*100

        size = {"대형주": "[대기업]", "중형주": "[중견기업]", "소형주": "[중소기업]"}.get(m.get('tier', '소형주'), "[중소기업]")
        
        html = f"""
        <div style='font-family: Malgun Gothic;'>
            <p><b style='color:#FFD700; font-size:14px;'>[기업 정보]</b><br/>
            그룹: {m.get('group','단독기업')}<br/>
            규모: <b style='color:#FFD700;'>{size}</b><br/>
            산업: {m['ind']} ({m['sub']})<br/>
            상태: <b style='color:#FF4444;'>{m['char']}</b></p>

            <p><b style='color:#FFD700; font-size:14px;'>[발행 정보]</b><br/>
            주식수: {self.s['shares']:,} 주<br/>
            시총: {self.s['market_cap']:,} 원</p>

            <p><b style='color:#FFD700; font-size:14px;'>[지배구조]</b><br/>
            자사주: {ts:.1f}% | 대주주: {os:.1f}%<br/>
            외국인: {fs:.1f}% | 기관 : {ins:.1f}%<br/>
            개인 : {rs:.1f}%</p>

            <p style='color: #FF4444; font-size: 14px;'><b>리스크: {m['risk_score']:.2f} / 150</b></p>
            <hr style='border: 0.5px solid #333;'/>
            <p style='color: #888; font-size: 11px;'>* 위 수치는 상장폐지 확정 시점의 데이터입니다.</p>
        </div>
        """
        self.report_panel.setHtml(html)

    def load_earnings_table(self):
        e_history = self.engine.earnings_history.get(self.stock_name, {})
        all_records = []
        for year in sorted(e_history.keys()):
            for qtr in ["1분기", "2분기", "3분기", "4분기"]:
                if qtr in e_history[year]:
                    d = e_history[year][qtr]
                    all_records.append((f"{year} {qtr}", d['revenue'], d['op_income'], d.get('net_income', 0)))
                    
        self.earnings_table.setRowCount(len(all_records))
        for i, (qtr, rev, op, net) in enumerate(all_records):
            it0 = QTableWidgetItem(qtr)
            it0.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.earnings_table.setItem(i, 0, it0)
            
            it1 = QTableWidgetItem(f"{rev:,.0f}")
            it1.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.earnings_table.setItem(i, 1, it1)
            
            it2 = QTableWidgetItem(f"{op:,.0f}")
            it2.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if op < 0:
                it2.setForeground(QColor("#4444FF"))
            else:
                it2.setForeground(QColor("#FF4444"))
            self.earnings_table.setItem(i, 2, it2)
            
            it3 = QTableWidgetItem(f"{net:,.0f}")
            it3.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            if net < 0:
                it3.setForeground(QColor("#4444FF"))
            else:
                it3.setForeground(QColor("#FF4444"))
            self.earnings_table.setItem(i, 3, it3)

    def load_full_history(self):
        try:
            import pyqtgraph as pg
            
            if not hasattr(self, 'current_tf'):
                self.current_tf = "전체"
            
            cur = self.engine.conn.cursor()
            cur.execute("SELECT price FROM stock_history WHERE company_name = ? ORDER BY date ASC", (self.stock_name,))
            rows = cur.fetchall()
            if not rows:
                return
                
            raw = [row[0] for row in rows]
            if any(x is None for x in raw):
                return
                
            count = len(raw)
            
            # 📌 데이터가 1개뿐일 때 붕괴 방지
            if count == 1:
                disp = [float(raw[0]), float(raw[0])]
            else:
                if count < 180:
                    step = 1
                elif count < 1095:
                    step = 7
                elif count < 3650:
                    step = 30
                elif count < 14600:
                    step = 180
                else:
                    step = 365

                if step > 1:
                    disp = [float(raw[i]) for i in range(0, count, step)]
                    if (count - 1) % step != 0 and raw:
                        disp.append(float(raw[-1]))
                else:
                    disp = [float(x) for x in raw]

            def calculate_moving_average(data, window_size=3):
                if not data: return []
                smoothed = []
                for i in range(len(data)):
                    start = max(0, i - window_size + 1)
                    window = data[start:i+1]
                    smoothed.append(sum(window)/len(window))
                return smoothed

            smoothed_disp = calculate_moving_average(disp, window_size=3)
            self.curve.setData(smoothed_disp)
            
            # 📌 [핵심 방어 코드] 상장폐지 역사관 차트 붕괴 방지
            if len(smoothed_disp) <= 1:
                dummy_val = float(disp[-1]) if disp else 10000.0
                self.chart_widget.setYRange(dummy_val * 0.9, dummy_val * 1.1)
            else:
                y_min, y_max = min(smoothed_disp), max(smoothed_disp)
                if y_min == y_max:
                    self.chart_widget.setYRange(y_min * 0.95, y_min * 1.05)
                else:
                    self.chart_widget.setYRange(y_min, y_max)
            
            if hasattr(self, 'max_scatter'):
                self.chart_widget.removeItem(self.max_scatter)
                self.chart_widget.removeItem(self.min_scatter)
                self.chart_widget.removeItem(self.max_text)
                self.chart_widget.removeItem(self.min_text)

            # 📌 Y축 범위를 설정하여 극소수점 지수 표기 방지
            if smoothed_disp:
                y_min = min(smoothed_disp)
                y_max = max(smoothed_disp)
                if y_min == y_max:
                    y_range = max(1.0, y_min * 0.01)
                    self.chart_widget.setYRange(y_min - y_range, y_max + y_range)
                else:
                    self.chart_widget.setYRange(y_min, y_max)
                
            if self.current_tf != "1일" and len(smoothed_disp) > 0:
                max_val = max(smoothed_disp)
                min_val = min(smoothed_disp)
                max_idx = smoothed_disp.index(max_val)
                min_idx = smoothed_disp.index(min_val)

                self.max_scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush('#FF4444'), symbol='o')
                self.max_scatter.addPoints([{'pos': (max_idx, max_val)}])
                self.chart_widget.addItem(self.max_scatter)

                self.min_scatter = pg.ScatterPlotItem(size=10, brush=pg.mkBrush('#4444FF'), symbol='o')
                self.min_scatter.addPoints([{'pos': (min_idx, min_val)}])
                self.chart_widget.addItem(self.min_scatter)

                max_is_right = max_idx > (len(smoothed_disp) * 0.75)
                max_anchor = (1.1, 1.1) if max_is_right else (0, 1)

                self.max_text = pg.TextItem(
                    html=f"<span style='color: #FF4444; font-weight: bold; background-color: #000;'>최고: {int(max_val):,}</span>",
                    anchor=max_anchor,
                )
                self.max_text.setPos(max_idx, max_val)
                self.chart_widget.addItem(self.max_text)

                min_is_left = min_idx < (len(smoothed_disp) * 0.25)
                min_is_right = min_idx > (len(smoothed_disp) * 0.75) 
                
                if min_is_right:
                    min_anchor = (1.1, -0.1)
                else:
                    min_anchor = (-0.1, -0.1) if min_is_left else (0, 0)

                self.min_text = pg.TextItem(
                    html=f"<span style='color: #4444FF; font-weight: bold; background-color: #000;'>최저: {int(min_val):,}</span>",
                    anchor=min_anchor,
                )
                self.min_text.setPos(min_idx, min_val)
                self.chart_widget.addItem(self.min_text)

                start_p = float(raw[0])
                end_p = float(raw[-1])
                diff = end_p - start_p
                rate = (diff / start_p * 100) if start_p != 0 else 0
                
                c_hex = "#FF4444" if diff > 0 else ("#4444FF" if diff < 0 else "#e0e0e0")
                sign = "▲" if diff > 0 else ("▼" if diff < 0 else "─")
                
                summary_text = (
                    f"<span style='color:#aaa;'>전체 기준: </span>"
                    f"<span style='color:#ffffff;'>{int(start_p):,}원</span>"
                    f"<span style='color:#ffffff;'> → </span>"
                    f"<span style='color:{c_hex}; font-weight:bold;'>{int(end_p):,}원 </span>"
                    f"<span style='color:{c_hex}; font-weight:bold;'>({sign}{int(abs(diff)):,}원, {rate:+.2f}%)</span>"
                )
                self.price_summary_label.setText(summary_text)
                
        except Exception as e:
            print(f"❌ 상장폐지 전체 그래프 및 헤더 로드 실패: {e}")

# -- 치트키 --
class CheatConsoleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hts = parent
        self.setWindowTitle("🛠️ SYSTEM DEBUG CONSOLE")
        self.setFixedSize(450, 180) # 안내 문구가 길어져 세로 길이를 살짝 늘렸습니다.
        
        self.setStyleSheet("""
            QDialog { background-color: #050505; border: 2px solid #00FF00; }
            QLabel { color: #00FF00; font-family: 'Consolas'; font-size: 13px; font-weight: bold; }
            QLineEdit { 
                background-color: #000; color: #00FF00; border: 1px solid #00FF00; 
                font-family: 'Consolas'; font-size: 18px; padding: 8px; 
            }
        """)
        
        layout = QVBoxLayout()
        # 안내 문구를 사용자님 요청에 맞게 변경했습니다.
        info_text = (
            "COMMAND SHORTCUTS:\n"
            " [ 1:숫자 ] : 골드(예수금) 추가 (예: 1:1000000)\n"
            " [ 2:숫자 ] : 스피드 일수 지정 (예: 2:30)\n"
            "(기존 명령어인 GOLD, SPEED도 계속 사용 가능)"
        )
        self.label = QLabel(info_text)
        layout.addWidget(self.label)
        
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("단축 명령어를 입력하세요...")
        self.input_line.returnPressed.connect(self.execute_command)
        layout.addWidget(self.input_line)
        self.setLayout(layout)

    def execute_command(self):
        cmd = self.input_line.text().strip().upper()
        if not cmd: return

        # 1) 단축키 파싱 로직 추가 (예: 1:1000000)
        if ":" in cmd:
            try:
                prefix, value_str = cmd.split(":")
                value = int(value_str)
                
                # 단축키 1: 골드 추가
                if prefix == "1":
                    self.hts.my_cash += value
                    self.hts.sync_ui_with_engine()
                    self.accept()
                    return
                # 단축키 2: 스피드 일수 지정
                elif prefix == "2":
                    self.hts.auto_speed_days = value
                    print(f"⚡ [SPEED] NEXT DAY 클릭 시 {value}일씩 자동 진행됩니다.")
                    self.accept()
                    return
            except:
                pass

        # 2) 기존 명령어 호환 (GOLD:, SPEED:)
        if cmd.startswith("GOLD:"):
            try:
                amount = int(cmd.split(":")[1])
                self.hts.my_cash += amount
                self.hts.sync_ui_with_engine()
                self.accept()
            except: pass

        elif cmd.startswith("SPEED:"):
            try:
                days = int(cmd.split(":")[1])
                self.hts.auto_speed_days = days
                print(f"⚡ [SPEED] NEXT DAY 클릭 시 {days}일씩 자동 진행됩니다.")
                self.accept()
            except:
                self.label.setText("❌ ERROR: 숫자를 입력하세요. (예: 1:1000000)")

if __name__ == "__main__":
    app = QApplication(sys.argv); window = StockHTS(); window.show(); sys.exit(app.exec())