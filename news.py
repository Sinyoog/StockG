import re
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QHBoxLayout, QMessageBox, QFrame, 
                             QTextEdit, QLineEdit, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

# --- 공통 스타일 시트 (HTS 테마 강화) ---
HTS_STYLE = """
    QDialog { background-color: #0d0d0d; color: #e0e0e0; font-family: 'Malgun Gothic'; }
    QLabel { color: #aaaaaa; }
    QTableWidget { 
        background-color: #000; 
        gridline-color: #1a1a1a; 
        border: 1px solid #333; 
        color: #ddd;
        selection-background-color: #1a331a;
    }
    QHeaderView::section { 
        background-color: #1a1a1a; 
        color: #00FF00; 
        padding: 8px; 
        border: 1px solid #222;
        font-weight: bold;
    }
    QComboBox { 
        background-color: #111; 
        color: #eee; 
        border: 1px solid #444; 
        padding: 5px; 
        border-radius: 2px; 
    }
    QLineEdit { 
        background-color: #000; 
        border: 1px solid #00FF00; 
        color: #00FF00; 
        padding: 5px; 
        selection-background-color: #004400;
    }
    QTextEdit { background-color: #050505; border: 1px solid #222; color: #bbb; }
"""

class NewsDetailWindow(QDialog):
    def __init__(self, ev, is_sub, parent=None):
        super().__init__(parent)
        self.ev = ev
        self.is_sub = is_sub
        self.setModal(False)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle(f"상세 리포트 - {ev.get('target', '시장')}")
        self.resize(550, 700)
        self.setStyleSheet(HTS_STYLE)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel(f"● 문서 식별번호: {abs(id(self.ev)) % 1000000} | 분류: {self.ev.get('cat')}")
        header.setStyleSheet("font-size: 11px; color: #555;")
        layout.addWidget(header)

        title = QLabel(self.ev.get('public', '데이터 정보 없음'))
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #00FF00; margin-top: 5px;")
        title.setWordWrap(True)
        layout.addWidget(title)

        info_frame = QFrame()
        info_frame.setStyleSheet("background: #111; border: 1px solid #222;")
        info_lay = QVBoxLayout(info_frame)
        
        meta = self.ev.get('meta_ref', {})
        body_txt = (f"■ 발행대상: {self.ev.get('target', '-')}\n"
                    f"■ 기업규모: {meta.get('tier', '기타')}\n"
                    f"■ 산업군: {meta.get('ind', '-')} ({meta.get('sub', '-')})\n"
                    f"■ 발행주수: {self.ev.get('shares', 0):,} 주")
        
        info_label = QLabel(body_txt)
        info_label.setStyleSheet("border: none; color: #999; line-height: 160%; font-size: 13px;")
        info_lay.addWidget(info_label)
        layout.addWidget(info_frame)

        layout.addWidget(QLabel("◈ 상세 분석 내용"))
        content_area = QTextEdit()
        content_area.setReadOnly(True)
        content_area.setText(self.ev.get('public'))
        layout.addWidget(content_area)

        # 프리미엄 섹션
        premium_box = QFrame()
        box_bg = "#051a05" if self.is_sub else "#111"
        border_c = "#00FF00" if self.is_sub else "#333"
        premium_box.setStyleSheet(f"background-color: {box_bg}; border: 1px solid {border_c}; border-radius: 4px;")
        
        pre_lay = QVBoxLayout(premium_box)
        pre_title = QLabel("💎 프리미엄 독점 전략 데이터")
        pre_title.setStyleSheet(f"font-weight: bold; color: {'#00FF00' if self.is_sub else '#555'}; border: none;")
        pre_lay.addWidget(pre_title)

        pre_content = QLabel(self.ev.get('premium', '분석 데이터가 존재하지 않습니다.') if self.is_sub else "프리미엄 구독 시 열람 가능한 보안 데이터입니다.")
        pre_content.setStyleSheet("color: #ddd; border: none; font-size: 13px;")
        pre_content.setWordWrap(True)
        pre_lay.addWidget(pre_content)
        layout.addWidget(premium_box)

        btn_close = QPushButton("리포트 닫기")
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("background: #222; color: white; border: 1px solid #444; padding: 10px; font-weight: bold;")
        layout.addWidget(btn_close)
        self.setLayout(layout)

class NewsWindow(QDialog):
    def __init__(self, hts_parent, engine, parent=None):
        super().__init__(parent)
        self.hts = hts_parent
        self.engine = engine
        self.all_events = [] 
        self.setModal(False)
        self.setWindowTitle("실시간 프리미엄 공시 분석 시스템 V12.5")
        self.resize(1150, 800)
        self.setStyleSheet(HTS_STYLE)
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)

        # 상단 바 (구독 상태 및 버튼)
        top_bar = QFrame()
        top_bar.setStyleSheet("background: #111; border-bottom: 2px solid #00FF00;")
        top_lay = QHBoxLayout(top_bar)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; border: none;")
        
        btn_style = """
            QPushButton { 
                background-color: #222; color: #eee; border: 1px solid #444; 
                padding: 7px 20px; font-weight: bold; border-radius: 3px;
            }
            QPushButton:hover { background-color: #333; border: 1px solid #00FF00; color: #00FF00; }
            QPushButton#premium_btn { background-color: #004400; border: 1px solid #00FF00; color: #00FF00; }
            QPushButton#cancel_btn { background-color: #331111; border: 1px solid #FF4444; color: #FF4444; }
        """

        self.btn_buy = QPushButton()
        self.btn_buy.setObjectName("premium_btn")
        self.btn_buy.clicked.connect(self.buy_paid_news)
        self.btn_buy.setStyleSheet(btn_style)

        self.btn_cancel = QPushButton("구독 해제")
        self.btn_cancel.setObjectName("cancel_btn")
        self.btn_cancel.clicked.connect(self.cancel_subscription)
        self.btn_cancel.setStyleSheet(btn_style)

        top_lay.addWidget(self.status_label)
        top_lay.addStretch()
        top_lay.addWidget(self.btn_buy)
        top_lay.addWidget(self.btn_cancel)
        layout.addWidget(top_bar)

        # 검색 영역
        search_lay = QHBoxLayout()
        self.search_combo = QComboBox()
        self.search_combo.addItems(["전체 필터", "일자별", "구분별", "종목별", "내용 검색"])
        self.search_combo.currentIndexChanged.connect(self.filter_table)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색할 키워드를 입력하십시오...")
        self.search_input.textChanged.connect(self.filter_table)
        
        search_lay.addWidget(self.search_combo)
        search_lay.addWidget(self.search_input)
        layout.addLayout(search_lay)

        # 테이블 레이아웃
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["[ 일자 ]", "[ 구분 ]", "[ 대상/종목 ]", "[ 공시 데이터 요약 ]"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 110)
        self.table.setColumnWidth(1, 110)
        self.table.setColumnWidth(2, 160)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.cellDoubleClicked.connect(self.show_news_detail)
        
        layout.addWidget(self.table)
        self.setLayout(layout)

    def is_currently_subscribed(self):
        """[최종 보강] 어떤 상황에서도 결제 날짜가 남아있으면 구독 유지"""
        # hts나 engine 객체 어디에든 날짜가 저장되어 있는지 확인
        b_date = getattr(self.hts, 'next_billing_date', None) or getattr(self.engine, 'next_billing_date', None)
        
        if not b_date: 
            return False
            
        # 날짜 형식 변환 (문자열 로드 대응)
        if isinstance(b_date, str):
            try: 
                b_date = datetime.strptime(b_date, '%Y-%m-%d').date()
            except: 
                return False
        elif hasattr(b_date, 'date'): 
            b_date = b_date.date()
        
        # 현재 날짜보다 결제 만료일이 크거나 같으면 무조건 TRUE
        return self.engine.current_date.date() <= b_date

    def refresh_data(self):
        """데이터 갱신 로직 (최신 뉴스 1,000개 제한 최적화 적용)"""
        # 1. 모든 누적 데이터를 가져옴
        self.all_events = self.get_all_cumulative_events()
        
        # 2. 최신순 정렬 (날짜 -> 카테고리 순)
        self.all_events.sort(key=lambda x: (x['date'], x['cat']), reverse=True)
        
        # [최적화 핵심] 데이터가 1,000개를 초과하면 최신순으로 1,000개만 남기고 삭제
        # 이를 통해 2100년 시점의 수만 개 데이터를 전부 처리하는 부하를 방지합니다.
        if len(self.all_events) > 1000:
            self.all_events = self.all_events[:1000]
        
        # 3. 구독 유효 기간 및 연장 여부 확인
        is_sub = self.is_currently_subscribed()
        will_renew = getattr(self.hts, 'has_paid_news_access', False)
        
        # 4. 상단 상태 표시줄 및 버튼 UI 업데이트 (한글화 유지)
        if is_sub:
            expire = self.hts.next_billing_date
            expire_str = expire.strftime('%Y-%m-%d') if hasattr(expire, 'strftime') else str(expire)
            
            if will_renew:
                self.status_label.setText(f"● 프리미엄 모드 활성 (차기 결제일: {expire_str})")
                self.status_label.setStyleSheet("color: #00FF00; font-weight: bold; border: none;")
                self.btn_buy.hide()
                self.btn_cancel.show()
                self.btn_cancel.setText("구독 해제")
            else:
                self.status_label.setText(f"○ 라이선스 만료 예정: {expire_str}")
                self.status_label.setStyleSheet("color: #FFA500; font-weight: bold; border: none;")
                self.btn_buy.show()
                self.btn_buy.setText("다시 구독")
                self.btn_cancel.hide()
        else:
            self.status_label.setText("○ 일반 모드 (프리미엄 미가입)")
            self.status_label.setStyleSheet("color: #777; border: none;")
            self.btn_buy.show()
            self.btn_buy.setText("프리미엄 구독 (1,000,000원)")
            self.btn_cancel.hide()

        # 5. 기존 테이블 잔상 제거 후 데이터 출력
        self.table.setRowCount(0)
        self.filter_table()

    def buy_paid_news(self):
        """결제 시 hts와 engine 양쪽에 기록을 박아버림 (유실 방지)"""
        if not self.is_currently_subscribed():
            if self.hts.my_cash < 1000000:
                return QMessageBox.warning(self, "잔액 부족", "계좌 잔액이 부족합니다.")
            
            self.hts.my_cash -= 1000000
            
            # 결제일 계산
            expiry = self.engine.current_date + timedelta(days=30)
            
            # [중요] 두 곳 모두에 저장하여 데이터 유실 차단
            self.hts.next_billing_date = expiry
            self.engine.next_billing_date = expiry
            
            # 구독 스위치 강제 활성화
            self.hts.has_paid_news_access = True 
            self.engine.has_paid_news_access = True
            
        else:
            # 기간 연장 또는 재활성화
            self.hts.has_paid_news_access = True 
            self.engine.has_paid_news_access = True
            
        self.refresh_data()

    def cancel_subscription(self):
        self.hts.has_paid_news_access = False
        self.engine.has_paid_news_access = False # 해제 시점 기록
        self.refresh_data()

    def get_all_cumulative_events(self):
        cumulative = []
        curr_date = self.engine.current_date.date()
        is_sub = self.is_currently_subscribed()

        if is_sub and hasattr(self.engine, 'pending_listings'):
            for s in self.engine.pending_listings:
                meta = s['meta']
                listed_dt = datetime.strptime(meta['listed_date'], '%Y-%m-%d').date()
                report_date = listed_dt - timedelta(days=7)
                if curr_date >= report_date:
                    cumulative.append(self._create_ev(report_date, "💎 상장예고", meta, 
                                                     f"[예고] {meta['c_name']} 신규 상장 예정 안내", 
                                                     f"7일 후 본 시장에 신규 상장될 예정입니다. ({meta['listed_date']})", s))

        for s in self.engine.stocks:
            meta = s['meta']
            listed_dt = datetime.strptime(meta['listed_date'], '%Y-%m-%d').date()
            if is_sub:
                old_report_date = listed_dt - timedelta(days=7)
                cumulative.append(self._create_ev(old_report_date, "💎 상장예고", meta, 
                                                 f"[예고] {meta['c_name']} 상장 예정 안내", "7일 후 상장 예정 리포트", s))
            if listed_dt <= curr_date:
                cumulative.append(self._create_ev(listed_dt, "🚀 신규상장", meta, 
                                                 f"[공시] {meta['c_name']} 기업 신규 상장 완료", "상장 직후 데이터 분석 완료", s))
        return cumulative

    def _create_ev(self, dt, cat, meta, pub, pre, stock=None):
        ev = {"date": dt.strftime('%Y-%m-%d'), "cat": cat, "target": meta['c_name'], "public": pub, "premium": pre, "meta_ref": meta}
        if stock: ev.update({"shares": stock.get('shares', 0), "market_cap": stock.get('market_cap', 0)})
        return ev

    def filter_table(self):
        idx = self.search_combo.currentIndex()
        text = self.search_input.text().lower().strip()
        is_sub = self.is_currently_subscribed()
        self.table.setRowCount(0)
        filtered = []

        for ev in self.all_events:
            content = ev['premium'] if is_sub else ev['public']
            match = False
            if idx == 0: # 전체
                if text in ev['date'].lower() or text in ev['cat'].lower() or \
                   text in ev['target'].lower() or text in content.lower(): match = True
            elif idx == 1: # 일자
                if text in ev['date'].lower(): match = True
            elif idx == 2: # 구분
                if text in ev['cat'].lower(): match = True
            elif idx == 3: # 종목
                if text in ev['target'].lower(): match = True
            elif idx == 4: # 내용
                if text in content.lower(): match = True
            if match: filtered.append((ev, content))

        self.table.setRowCount(len(filtered))
        for i, (ev, content) in enumerate(filtered):
            summary = content[:55] + "..." if len(content) > 55 else content
            row_data = [ev['date'], ev['cat'], ev['target'], summary]
            for j, val in enumerate(row_data):
                it = QTableWidgetItem(val)
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter if j < 3 else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                if is_sub: it.setForeground(QColor("#00FF00"))
                it.setData(Qt.ItemDataRole.UserRole, ev) 
                self.table.setItem(i, j, it)

    def show_news_detail(self, row, col):
        it = self.table.item(row, 0)
        if not it: return
        ev = it.data(Qt.ItemDataRole.UserRole)
        detail = NewsDetailWindow(ev, self.is_currently_subscribed(), self)
        detail.show()