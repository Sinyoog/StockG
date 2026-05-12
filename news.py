import re
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QHBoxLayout, QMessageBox, QFrame, 
                             QTextEdit, QLineEdit, QComboBox, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

# --- 공통 스타일 시트 (HTS 테마) ---
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
    QTextEdit { background-color: #050505; border: 1px solid #222; color: #bbb; font-size: 13px; line-height: 150%; }
    
    #DetailFrame {
        background-color: #0a0a0a;
        border-left: 2px solid #00FF00;
    }
"""

class NewsWindow(QDialog):
    def __init__(self, hts_parent, engine, parent=None):
        super().__init__(parent)
        self.hts = hts_parent
        self.engine = engine
        self.all_events = [] 
        self.setModal(False)
        self.setWindowTitle("실시간 프리미엄 공시 분석 시스템 V12.5")
        self.resize(1400, 850) 
        self.setStyleSheet(HTS_STYLE)
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        # 메인 수직 레이아웃
        main_v_layout = QVBoxLayout()
        main_v_layout.setContentsMargins(10, 10, 10, 10)

        # 1. 상단 바 (구독 상태 및 버튼)
        top_bar = QFrame()
        top_bar.setStyleSheet("background: #111; border-bottom: 1px solid #333;")
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
        main_v_layout.addWidget(top_bar)

        # 2. 중앙 본문 영역 (좌측 리스트 7 : 우측 상세 리포트 3)
        content_layout = QHBoxLayout()
        
        # --- 좌측: 목록 영역 ---
        left_widget = QWidget()
        left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(0, 0, 0, 0)

        search_lay = QHBoxLayout()
        self.search_combo = QComboBox()
        self.search_combo.addItems(["전체 필터", "일자별", "구분별", "종목별", "내용 검색"])
        self.search_combo.currentIndexChanged.connect(self.filter_table)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색할 키워드를 입력하십시오...")
        self.search_input.textChanged.connect(self.filter_table)
        
        search_lay.addWidget(self.search_combo)
        search_lay.addWidget(self.search_input)
        left_lay.addLayout(search_lay)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["[ 일자 ]", "[ 구분 ]", "[ 대상/종목 ]", "[ 공시 데이터 요약 ]"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # 클릭 시 상세 내용이 바뀌도록 연결
        self.table.itemSelectionChanged.connect(self.update_detail_view)
        
        left_lay.addWidget(self.table)
        content_layout.addWidget(left_widget, 7)

        # --- 우측: 상세 리포트 영역 ---
        self.detail_frame = QFrame()
        self.detail_frame.setObjectName("DetailFrame")
        self.detail_lay = QVBoxLayout(self.detail_frame)
        
        self.det_header = QLabel("● 문서 정보 대기 중")
        self.det_header.setStyleSheet("font-size: 11px; color: #555;")
        
        self.det_title = QLabel("공시를 선택하십시오")
        self.det_title.setStyleSheet("font-size: 17px; font-weight: bold; color: #00FF00; margin-top: 5px;")
        self.det_title.setWordWrap(True)
        
        self.det_meta_box = QFrame()
        self.det_meta_box.setStyleSheet("background: #111; border: 1px solid #222; padding: 10px;")
        self.det_meta_lay = QVBoxLayout(self.det_meta_box)
        self.det_meta_label = QLabel("-")
        self.det_meta_label.setStyleSheet("color: #999; font-size: 13px; border: none; line-height: 160%;")
        self.det_meta_lay.addWidget(self.det_meta_label)
        
        self.det_content = QTextEdit()
        self.det_content.setReadOnly(True)
        
        self.detail_lay.addWidget(self.det_header)
        self.detail_lay.addWidget(self.det_title)
        self.detail_lay.addWidget(QLabel("◈ 상세 분석 정보"))
        self.detail_lay.addWidget(self.det_meta_box)
        self.detail_lay.addWidget(QLabel("◈ 본문 내용"))
        self.detail_lay.addWidget(self.det_content)
        
        content_layout.addWidget(self.detail_frame, 3)

        main_v_layout.addLayout(content_layout)
        self.setLayout(main_v_layout)

    def update_detail_view(self):
        selected_items = self.table.selectedItems()
        if not selected_items: return
        row = selected_items[0].row()
        ev = self.table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        meta = ev.get('meta_ref', {})
        
        # 엔진의 SECTOR_MAP에 접근하기 위해 self.engine.SECTOR_MAP 사용
        sector = getattr(self.engine, 'SECTOR_MAP', {}).get(meta.get('ind'), 'Growth')
        
        self.det_header.setText(f"● 문서 식별번호: {abs(id(ev)) % 1000000} | 분류: {ev.get('cat')}")
        self.det_title.setText(f"< {ev.get('target')} >")
        
        # [수정] 금액이 0원일 경우 '산정 중' 표시 및 콤마 적용
        m_cap = f"{ev.get('market_cap', 0):,}" if ev.get('market_cap', 0) > 0 else "데이터 분석 중"
        s_price = f"{ev.get('start_price', 0):,}" if ev.get('start_price', 0) > 0 else "산정 중"
        
        report_text = (
            f"상장일: {meta.get('listed_date', '-')} | 섹터: {sector}\n"
            f"------------------------------------------\n"
            f"[기업 정보]\n"
            f"그룹: {meta.get('group', '독립')}\n"
            f"규모: [{meta.get('tier', '기타')}]\n"
            f"산업: {meta.get('ind', '-')} ({meta.get('sub', '-')})\n"
            f"상태: {meta.get('char', 'Normal')}\n\n"
            f"[발행 정보]\n"
            f"주식수: {ev.get('shares', 0):,} 주\n"
            f"시가총액: {m_cap} 원\n"
            f"상장 시초가(예정): {s_price} 원\n"
            f"------------------------------------------\n"
            f"■ 공시 분석 내용:\n{ev.get('public')}"
        )
        self.det_content.setText(report_text)

    def is_currently_subscribed(self):
        b_date = getattr(self.hts, 'next_billing_date', None) or getattr(self.engine, 'next_billing_date', None)
        if not b_date: return False
        if isinstance(b_date, str):
            try: b_date = datetime.strptime(b_date, '%Y-%m-%d').date()
            except: return False
        elif hasattr(b_date, 'date'): b_date = b_date.date()
        return self.engine.current_date.date() <= b_date

    def refresh_data(self):
        self.all_events = self.get_all_cumulative_events()
        self.all_events.sort(key=lambda x: (x['date'], x['cat']), reverse=True)
        if len(self.all_events) > 1000: self.all_events = self.all_events[:1000]
        
        is_sub = self.is_currently_subscribed()
        will_renew = getattr(self.hts, 'has_paid_news_access', False)
        
        if is_sub:
            expire = self.hts.next_billing_date
            expire_str = expire.strftime('%Y-%m-%d') if hasattr(expire, 'strftime') else str(expire)
            if will_renew:
                self.status_label.setText(f"● 프리미엄 모드 활성 (차기 결제일: {expire_str})")
                self.status_label.setStyleSheet("color: #00FF00; font-weight: bold; border: none;")
                self.btn_buy.hide(); self.btn_cancel.show()
            else:
                self.status_label.setText(f"○ 라이선스 만료 예정: {expire_str}")
                self.status_label.setStyleSheet("color: #FFA500; font-weight: bold; border: none;")
                self.btn_buy.show(); self.btn_buy.setText("다시 구독"); self.btn_cancel.hide()
        else:
            self.status_label.setText("○ 일반 모드 (프리미엄 미가입)")
            self.status_label.setStyleSheet("color: #777; border: none;")
            self.btn_buy.show(); self.btn_buy.setText("프리미엄 구독 (1,000,000원)"); self.btn_cancel.hide()
        self.filter_table()

    def filter_table(self):
        idx = self.search_combo.currentIndex()
        text = self.search_input.text().lower().strip()
        is_sub = self.is_currently_subscribed()
        
        self.table.setRowCount(0)
        filtered = []

        for ev in self.all_events:
            # 검색 대상 텍스트 설정
            pub_content = ev.get('public', "").lower()
            target_name = ev.get('target', "").lower()
            category = ev.get('cat', "").lower()
            date_str = ev.get('date', "").lower()
            
            match = False
            if idx == 0: # 전체 필터
                if text in date_str or text in category or \
                   text in target_name or text in pub_content: match = True
            elif idx == 1: # 일자별
                if text in date_str: match = True
            elif idx == 2: # 구분별
                if text in category: match = True
            elif idx == 3: # 종목별
                if text in target_name: match = True
            elif idx == 4: # 내용 검색
                if text in pub_content: match = True
            
            if match:
                filtered.append(ev)

        self.table.setRowCount(len(filtered))
        
        for i, ev in enumerate(filtered):
            # 요약 문구 생성
            content = ev.get('public', "")
            summary = content[:55] + "..." if len(content) > 55 else content
            
            row_data = [ev['date'], ev['cat'], ev['target'], summary]
            
            for j, val in enumerate(row_data):
                it = QTableWidgetItem(str(val))
                
                # 정렬 설정
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter if j < 3 else Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
                # [수정 포인트] 구독 상태일 때 색상 로직
                if is_sub:
                    if "💎" in ev['cat']: # 상장예고 항목은 밝은 초록색 (HTS 강조형)
                        it.setForeground(QColor("#00FF00"))
                    else: # 일반 상장 완료 등은 일반 흰색/회색 계열 유지 혹은 흐린 초록
                        it.setForeground(QColor("#e0e0e0")) 
                
                # 핵심 데이터 저장 (클릭 시 우측 리포트 갱신용)
                it.setData(Qt.ItemDataRole.UserRole, ev) 
                self.table.setItem(i, j, it)

    def generate_news_list(stock_engine):
        news_list = []
        current_date = stock_engine.current_date
        
        for stock in stock_engine.stocks:
            # 1. 실적 발표 데이터 생성 체크 (D-Day 확인)
            if stock.is_earnings_day(current_date):
                stock_name = stock.name
                
                # --- 디버그 로그 추가 시작 ---
                print(f"DEBUG: [Earnings News Generated for: {stock_name}]")
                print(f"      - Net Income: {stock.last_net_income}")
                print(f"      - Paid Access Status: {stock_engine.has_paid_news_access}")
                # --- 디버그 로그 추가 끝 ---

                # 뉴스 객체 생성 로직
                content = f"[{stock_name}] 분기 실적 발표: "
                if stock_engine.has_paid_news_access:
                    content += f"당기순이익 {stock.last_net_income:,}원 달성"
                else:
                    content += "실적 수치는 프리미엄 구독자에게만 공개됩니다."
                
                news_list.append({"title": "기업 공시", "content": content, "type": "EARNINGS"})

        return news_list

    def show_toast_message(self, message):
        """중앙에 메시지를 띄우고 1초 뒤에 삭제하는 토스트 알림 기능"""
        from PyQt6.QtCore import QTimer
        
        # 메시지 라벨 생성
        self.toast_label = QLabel(message, self)
        self.toast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 스타일 설정 (스크린샷 느낌의 어두운 배경 + 빨간 테두리/글씨)
        self.toast_label.setStyleSheet("""
            background-color: rgba(20, 0, 0, 230); 
            color: #FF4444; 
            border: 2px solid #FF4444; 
            font-size: 20px; 
            font-weight: bold; 
            padding: 20px 40px;
            border-radius: 5px;
        """)
        
        # 위치 조정 (창 중앙)
        self.toast_label.adjustSize()
        x = (self.width() - self.toast_label.width()) // 2
        y = (self.height() - self.toast_label.height()) // 2
        self.toast_label.move(x, y)
        self.toast_label.show()
        
        # 1초 뒤에 사라지게 함
        QTimer.singleShot(1000, self.toast_label.deleteLater)

    def buy_paid_news(self):
        if not self.is_currently_subscribed():
            # 잔액 검사 로직
            if self.hts.my_cash < 1000000:
                # [수정] 경고창 대신 토스트 알림 호출
                self.show_toast_message("잔액이 부족합니다")
                return 

            # 결제 진행
            self.hts.my_cash -= 1000000
            expiry = self.engine.current_date + timedelta(days=30)
            
            # 데이터 동기화
            self.hts.next_billing_date = expiry
            self.engine.next_billing_date = expiry
            self.hts.has_paid_news_access = True 
            self.engine.has_paid_news_access = True
            
            self.show_toast_message("프리미엄 구독이 시작되었습니다")
        else:
            self.hts.has_paid_news_access = True 
            self.engine.has_paid_news_access = True
            
        self.refresh_data()

    def cancel_subscription(self):
        self.hts.has_paid_news_access = False
        self.engine.has_paid_news_access = False
        self.refresh_data()

    def get_all_cumulative_events(self):
        cumulative = []
        curr_dt_obj = self.engine.current_date
        curr_date = curr_dt_obj.date()
        is_sub = self.is_currently_subscribed()
        
        # 1. [상장 예정 리스트] 아직 상장 안 된 대기 종목들 (pending_listings)
        # 프리미엄 유저에게 상장 7일 전부터 "💎 상장예고"를 미리 보여줍니다.
        if hasattr(self.engine, 'pending_listings') and self.engine.pending_listings:
            for s in self.engine.pending_listings:
                try:
                    meta = s.get('meta', {})
                    l_date_str = meta.get('listed_date', '2000-01-01')
                    listed_dt = datetime.strptime(l_date_str, '%Y-%m-%d').date()
                    d_7_date = listed_dt - timedelta(days=7)
                    
                    if is_sub and curr_date >= d_7_date:
                        cumulative.append(self._create_ev(
                            d_7_date, "💎 상장예고", meta, 
                            f"[예고] {meta.get('c_name')} 신규 상장 예정 안내", s
                        ))
                except: continue

        # 2. [기존 종목 루프] 실적 및 상장 완료 처리
        for s in self.engine.stocks:
            try:
                real_meta = s.get('meta', {}) if isinstance(s, dict) else getattr(s, 'meta', {})
                c_name = real_meta.get('c_name', 'Unknown')
                year_str = str(curr_dt_obj.year)
                
                # --- A. 상장 관련 공시 (누적 기록) ---
                l_date_str = real_meta.get('listed_date', '2000-01-01')
                listed_dt = datetime.strptime(l_date_str, '%Y-%m-%d').date()
                
                # [유료] 이미 상장된 종목의 '상장 예고' 기록도 리스트에 유지
                if is_sub:
                    cumulative.append(self._create_ev(
                        listed_dt - timedelta(days=7), "💎 상장예고", real_meta, 
                        f"[예고] {c_name} 상장 예정 리포트", s
                    ))
                
                # [무료] 상장 완료 공시 (오늘 날짜가 상장일 이후면 상시 노출)
                if listed_dt <= curr_date:
                    cumulative.append(self._create_ev(
                        listed_dt, "🚀 신규상장", real_meta, 
                        f"[공시] {c_name} 기업 상장 완료", s
                    ))

                # --- B. 실적 공시 섹터 (예고 및 확정) ---
                if 'report_day' in real_meta:
                    y, m = curr_dt_obj.year, curr_dt_obj.month
                    if m in [3, 4, 6, 7, 9, 10, 12, 1]:
                        try:
                            r_day = min(real_meta.get('report_day', 15), 28)
                            report_dt = datetime(y, m, r_day).date()
                            d_7_date = report_dt - timedelta(days=7)
                            q_name = f"{(m-1)//3 + 1}분기" if m in [3, 6, 9, 12] else f"{(m-2)//3 + 1}분기"

                            if curr_date >= d_7_date:
                                # 상단 기업 정보를 가리기 위한 최소 메타
                                news_meta = {'c_name': c_name}
                                
                                if is_sub:
                                    data = real_meta.get('expected_earnings')
                                    if not data:
                                        data = {'revenue': real_meta.get('assets', 0) * 0.08, 'net_income': real_meta.get('assets', 0) * 0.005}
                                    
                                    ni = data.get('net_income', 0)
                                    status = "흑자" if ni >= 0 else "적자"
                                    content = (
                                        f"분기: {q_name}\n"
                                        f"공시일: {report_dt.strftime('%m월 %d일')}\n"
                                        f"매출액: {data.get('revenue', 0):,.0f}원\n"
                                        f"영업이익: {ni * 1.1:,.0f}원 ({status})\n"
                                        f"당기순이익: {ni:,.0f}원 ({status})"
                                    )
                                    cat_name = "💎 실적예고(P)"
                                else:
                                    content = (
                                        f"분기: {q_name}\n"
                                        f"공시일: {report_dt.strftime('%m월 %d일')}\n"
                                        f"------------------------------------------\n"
                                        f"상세 지표는 프리미엄 전용입니다."
                                    )
                                    cat_name = "📊 실적예고"
                                
                                cumulative.append(self._create_ev(d_7_date, cat_name, news_meta, content, s))

                            # 실제 확정 실적 발표 (history 참조)
                            history = self.engine.earnings_history.get(c_name, {}).get(year_str, {})
                            if q_name in history:
                                h_data = history[q_name]
                                h_ni = h_data.get('net_income', 0)
                                h_status = "흑자" if h_ni >= 0 else "적자"
                                h_content = (
                                    f"분기: {q_name} (확정)\n"
                                    f"발표일: {h_data.get('date', '당일')}\n"
                                    f"매출액: {h_data.get('revenue', 0):,.0f}원\n"
                                    f"영업이익: {h_data.get('op_income', 0):,.0f}원 ({h_status})\n"
                                    f"당기순이익: {h_ni:,.0f}원 ({h_status})"
                                )
                                cumulative.append(self._create_ev(curr_date, "📢 실적공시", {'c_name': c_name}, h_content, s))
                        except: pass

            except: continue

        # 최신순 정렬
        cumulative.sort(key=lambda x: x['date'], reverse=True)
        return cumulative

    def _create_ev(self, dt, cat, meta, pub, stock=None):
        # 1. 주식수 확보
        shares = meta.get('shares', 0)
        if shares <= 0 and stock:
            shares = stock.get('shares', 0)
        if shares <= 0: # 최후의 수단: 자산 기반 추정 (엔진 설정에 따라 조정)
            shares = 50000000 

        # 2. 주가 확보 (상장 예정가는 보통 assets / shares)
        price = stock.get('price', 0) if stock else 0
        if price <= 0:
            assets = meta.get('assets', 0)
            price = assets / max(1, shares)

        # 3. 시가총액 산출
        market_cap = stock.get('market_cap', 0) if stock else (price * shares)

        ev = {
            "date": dt.strftime('%Y-%m-%d'),
            "cat": cat,
            "target": meta['c_name'],
            "public": pub,
            "meta_ref": meta,
            "shares": int(shares),
            "market_cap": int(market_cap),
            "start_price": int(price)
        }
        return ev