import json, random, sys, re, math, time, csv, os, sqlite3
from datetime import datetime, timedelta

class StockGameEngine:
  def __init__(self):
    self.NAME_DB = [
      "한결", "서안", "대승", "해온", "가람", "진성", "세운", "정인", "태림", "선일", "성우", "영진", "경인", "태양", "삼영", "부국", "일성", "청해", "은성", "효성", "넥서스", "이노", "노바", "피닉스", "오로라", "대진",
      "제넥스", "퓨어", "솔라", "브릿지", "아이소", "뉴로", "쿼크", "옥타", "이오스", "베가", "시그마", "네오", "루시드", "코어", "플럭스", "다온", "누리", "라온", "마루", "이룸", "새론", "한울", "미리내", "온누리", "화성",
      "한빛", "나래", "다솜", "푸름", "슬기", "바른", "든든", "도담", "예그리나", "아리아", "에토스", "벨라", "리베", "로고스", "아인", "노블", "찬영", "지안", "윤성", "하진", "도준", "예준", "건우", "서우", "벨로스","골드만",
      "유진", "시우", "이안", "연우", "현승", "무진", "정본", "고조선", "백제", "고구려", "신라", "가야", "발해", "고려", "조선", "헬퍼", "가지", "포도", "복어", "퉁퉁", "기러기", "참새", "백조", "수리", "비둘기","에코플로우",
      "응가", "태백", "청안", "대양", "해람", "단군", "태극", "은하", "성운", "지평", "해오름", "청운", "벽산", "남산", "대안", "평화", "통일", "웅비", "비상", "천명", "명성", "수호", "대덕", "유성", "광원", "앵그리","목성",
      "신뢰", "창조", "진흥", "성신", "보성", "다산", "우신", "대동", "진명", "우주", "영원", "불멸", "상생", "도약", "정수", "이루", "다움", "늘봄", "시작", "뿌리", "줄기", "열매", "흐름", "결실", "마중", "아바", "플로",
      "디딤", "울림", "바람", "여울", "마음", "솔솔", "아사달", "사비", "웅진", "무령", "광개토", "장수", "을지", "충무", "다보", "석가", "경회", "근정", "화랑", "거북", "해학", "풍류", "단비", "가랑", "윤슬", "해피", "백산",
      "아라", "자라", "고래", "풍선", "진양", "동승", "세양", "한영", "리안", "수박", "망고", "미르", "새벽", "나무", "감자", "고구마", "코알라", "우성", "경성", "창해", "동우", "태평", "성진", "명인", "한성", "동남", "동양",
      "푸딩", "단추", "고무", "양파", "두부", "참깨", "딱지", "도토리", "루멘", "아토", "오빗", "테라", "아크", "모멘트", "다람쥐", "두루미", "상어", "호랑", "민들레", "타이거", "알타이르", "에테르", "시나르", "노릭", "퍼스트",
      "아이기스", "오리온", "루모스", "코어텍", "네오스", "인피니", "퀀텀", "솔리드", "에이펙스", "센트럴", "코뿔소", "두더지", "꿀벌", "망치", "구름", "번개", "먼지", "알밤", "붕어빵", "호떡", "까치", "고양이", "강아지", "곰돌이",
      "장화", "우산", "천하", "일송", "대명", "상록", "지성", "청산", "백운", "금강", "단풍", "이슬", "버들", "산들", "대숲", "철강", "태산", "천지", "건곤", "정진", "보람", "젤리", "티라노", "스테고", "스피노", "브라키", "모사",
      "미래", "육수", "금붕어", "웅이", "유삭", "이래", "법호", "고승", "산호", "현재", "오소리", "벌꿀", "리우스", "두까비", "늑구", "굴", "소풍", "유한", "이두", "삼두", "변율", "태안", "신성", "영풍", "세안", "해찬", "새늘",
      "호두", "앵무", "구슬", "우럭", "탐라", "파보", "디키", "모노로", "제플", "아토닉", "곰스오", "스타", "벼룩", "방울", "레온", "몽키", "호박", "해파리", "귤", "스프라이트", "티아라", "크샤트리라","뱀눈", "MALICE", "라이제올", "드래곤 테일", "야미", "K9",
      "뱅키시", "리시드", "현람", "펭귄", "물개", "하마", "코끼리", "표범", "퓨마", "치타", "사자", "고라니", "노루", "아이언", "브론즈", "실버", "골드", "플레", "에메", "다이아", "마스터", "K", "도마", "변기", "수성", "금성", "지구",
      "토성", "천왕성", "해왕성", "명왕성", "넥세논", "반티지", "에테리스", "데이터라이즈", "코어닉스", "제노플로우", "시냅틱스", "벨로시티", "제노버스", "퓨레틱", "리보니움", "옵티케어", "바이오닉스", "셀리드", "메디코어", "에이치바이오",
      "솔레인","아이로닉스", "테라폼", "하이젠", "에너테크", "그리드원", "퓨처엠", "아르카", "프라임에셋", "옴니캐피탈", "큐브홀딩스", "센트럴글로벌", "유니온네트웍스", "비전인베스트", "효승", "가놈", "유화", "삼광", "태화", "금양",
      "한창", "동성", "신일", "경남", "삼화", "대영", "성보", "한일", "대신", "한보","탈모", "에너스", "네오텍", "셀리온", "퓨처원", "에코시스", "아이온", "그린텍", "볼트닉스", "에이치엠", "엔솔", "넥스트라", "모빌리언", "리드",
      "커넥트", "데이터큐브", "플레이온", "하이퍼", "마인드", "링크소프트", "비트원", "클라우드나인", "픽셀트리", "스마트온", "디지털로", "밸류원", "트러스트", "에셋파이브", "크레딧", "참맛", "미디어", "올리브","퍼리",
      "메오티", "사향", "지니", "기영", "준철", "깨철", "오성", "장수", "이리", "흥아", "고추", "오이", "느그", "메뚜기", "바퀴", "푸들", "땡이", "도넛", "야호", "파이브", "핸드", "구독", "가이", "대아"
    ]
    self.group_base_names = ["제니스", "서한", "가온", "범양", "버거"]

    # 1. 시간 및 기본 데이터 설정
    self.start_date = datetime(1999, 12, 31)
    self.current_date = self.start_date
    self.is_market_open = False
    self.virtual_weekday = 6
    self.stocks = []
    self.groups = {}
    self.daily_history = {}
    self.history_records = []
    self.name_registry = {}
    self.delisted_stocks = []
    self.current_scenario = "정상 성장"
    self.world_line = "Normal"
    self.scenario_timer = 0
    self.is_recovering = False
    self.base_item_price = 1000.0
    self.cumulative_inflation = 1.0
    self.pre_reflection_events = []
    self.pending_listings = []
    self.has_paid_news_access = False

    import sqlite3
    self.conn = sqlite3.connect("stock_data.db", check_same_thread=False)
    self.create_db()
   
    # [수정] 위에서 선언한 리스트들을 사용하는 변수들
    self.earnings_history = {}
    self.used_all_time = set()
    self.name_pool = [n for n in self.NAME_DB if n not in self.group_base_names]
    random.shuffle(self.name_pool)
    self.current_generation = 1
   
    # 3. 거시 경제 지표 초기화get_tech_level
    self.wsi = 1500.0
    self.gri = 1000.0
    self.macro = {
      "oil_price": 30.0,
      "exchange_rate": 1100.0,
      "interest_rate": 4.0,
      "cpi": 2.0,
      "fear_index": 10.0
    }

    # 선반영 데이터 저장소
    self.pending_events = {
      "earnings": {},  # {company_name: {"date": D-Day, "net_income": 예상치}}
      "macro": {},   # {"target_interest": 목표치, "date": D-Day}
      "delist": {},   # {company_name: D-Day}
      "splits": {},   # {company_name: {"ratio": 비율, "date": D-Day}}
      "tech_jump": None # {"target_lv": 다음레벨, "date": D-Day}
    }
   
    # 4. 시장 구조 및 그룹사 설정
    self.MAX_STOCKS = 400
    self.initial_market_total_cap = 0.0
    self.max_tech_reached = 1
    self.daily_news = []
   
    # 그룹사 관련 제한 설정
    self.max_group_count = 8 # 초기 5개 + 신규 최대 3개
    self.group_limit_by_tech = {1: 3, 2: 5, 3: 8, 4: 10} # 테크별 최대 계열사 수
   
    # 5. 산업 및 섹터 페르소나 설정
    self.MAIN_INDUSTRIES = [
      "IT", "에너지", "건강관리", "산업재", "소재", "자유소비재",
      "커뮤니케이션", "금융", "필수소비재", "유틸리티", "부동산", "재건"
    ]
   
    self.SECTOR_MAP = {
      "IT": "Growth", "건강관리": "Growth", "커뮤니케이션": "Growth",
      "금융": "Value", "에너지": "Value", "소재": "Value", "산업재": "Value", "부동산": "Value",
      "필수소비재": "Defensive", "유틸리티": "Defensive",
      "재건": "Theme", "자유소비재": "Theme"
    }

    # 6. 체급별 시장 구성 정의 (요청 수치 반영)
    self.TIER_CONFIG = {
      "대형주": {"ratio": 0.11, "shares": (100, 1000), "price": (40000, 80000)}, # 백만 단위 multiplier 적용 전
      "중형주": {"ratio": 0.22, "shares": (50, 200), "price": (15000, 35000)}, # 5천만~2억 주 시작
      "소형주": {"ratio": 0.67, "shares": (1, 50), "price": (1000, 15000)}
    }
   
    self.INDUSTRY_LEVELS = {
      "IT": {
        1: [
          "PC용D램", "HDD저장장치", "유선랜카드", "LCD모니터패널", "피처폰부품", "MP3모듈", "기초노광장비", "PCB회로기판", "수동소자(MLCC)", "광학렌즈모듈", "PC케이스", "초정밀금형", "쿨링팬시스템", "입력장치제조", "전원공급장치",
          "CD-ROM드라이브", "사운드카드", "스캐너부품", "잉크젯헤드", "플로피디스크소재","CRT모니터부품", "기초방열판", "유선키보드제조", "볼마우스센서", "메인보드조립"
        ],
        2: [
          "HBM메모리", "GPU가속기", "모바일AP", "클라우드보안", "SaaS솔루션", "데이터센터리츠", "낸드컨트롤러", "핀테크인프라", "디지털트윈플랫폼", "API통합관리", "엔터프라이즈ERP", "엣지컴퓨팅", "모바일OS", "빅데이터분석", "워크플로우자동화",
          "사이버보안관제", "AI반도체설계", "서버용SSD", "팹리스파운드리", "저전력프로세서","안면인식모듈", "지문인식센서", "폴더블디스플레이", "초고성능서버", "가상화솔루션"
        ],
        3: [
          "초기양자컴퓨터", "NPU(신경망처리장치)", "6G통신장비", "저궤도위성망", "실시간통번역신경망", "초기형BCI", "지능형홈OS", "엣지AI칩셋", "초고속데이터버스", "광컴퓨팅부품",
          "자율에이전트", "데이터주권인프라", "지능형사이버방벽", "뉴로모픽소자", "실감형홀로그램","양자내성암호", "초저지연데이터망", "지능형센서허브", "분산원장데이터베이스", "나노회로설계장비"
        ],
        4: [
          "ASI(초지능)코어", "디지털의식저장소", "행성간양자망", "양자암호키분배", "의식업로딩백본", "초공간연산클러스터", "차원간데이터통신", "입자연산소자", "시간왜곡처리중추", "데이터엔트로피제어",
          "가상영혼아카이브", "전우주통합OS", "집단지성최적화엔진", "고차원연산매개체", "무한연산그리드"
        ]
      },
      "에너지": {
        1: [
          "원유정제", "화력발전소", "천연가스도매", "유연탄채굴", "전력변환장치", "송전인프라", "가스관매설", "정유시설설계", "윤활유생산", "기초석유화학", "LPG충전소", "원자력연료봉", "중유공급", "가압장시설", "가스미터기",
          "전주제조", "지하송전케이블", "산업용전력유통", "절연유생산", "아스팔트제조"
        ],
        2: [
          "리튬이온배터리", "태양광패널", "풍력터빈", "VPP(가상발전소)", "수소스테이션", "바이오연료", "지능형전력망", "전기차충전플랫폼", "폐배터리리사이클링", "그린수소생산", "암모니아발전", "마이크로그리드", "에너지중개거래", "고효율인버터", "조력발전부품",
          "에너지관리(EMS)", "가정용ESS", "수상태양광", "해상풍력단지운영", "고효율단열소재"
        ],
        3: [
          "SMR(소형원자로)", "전고체배터리", "페로브스카이트태양광", "탄소포집(CCUS)", "수소액화플랜트", "중력배터리", "고온초전도송전", "초임계CO2터빈", "지열발전터빈", "해수온도차발전",
          "바나듐흐름전지", "핵융합기초연구", "에너지자립도시망", "폐기물플라즈마에너지", "전력도매거래소","액체수소운반선", "에너지섬건설", "메탄하이드레이트추출", "심해연료기지", "바이오매스발전"
        ],
        4: [
          "상용핵융합로", "우주태양광수신기", "무선전력전송", "반물질추출기", "진공에너지추출기", "항성에너지집적망", "다이슨구체부분공정", "블랙홀강착원반발전", "입자붕괴에너지", "항성간에너지무역", "중력장에너지집적", "다차원에너지수급", "시공간에너지필터", "행성핵열교환기", "성간송전빔"
        ]
      },
      "방위산업": {
        1: [
          "전차제조", "자주포생산", "탄약/화약제조", "군용전술차량", "개인전투군장", "전함용엔진", "군용레이더모듈", "방탄소재", "기초사격시뮬레이션", "잠수함압력선체", "군납의류", "야전병원설비", "지뢰탐지기", "함정전투시스템", "군용타이어",
          "항공기기체", "특수목적헬기", "군용낙하산", "군용식량배급", "장갑차강판"
        ],
        2: [
          "정찰드론시스템", "대공미사일방어망", "전자전방해장치", "스텔스도료", "유도무기시스템", "전투용웨어러블", "무인차량(UGV)", "순항미사일", "함정스텔스", "군사용VR훈련", "저고도방공망", "대함미사일", "사이버전술보안", "EMP무기", "군용AI보안",
          "탄도미사일요격", "군용생체인증", "분석방어체계", "특수전용장비", "군용통신위성"
        ],
        3: [
          "레이저요격병기", "극초음속미사일", "드론스웜관제", "로봇보병지제장치", "초소형군사위성군", "전술핵융합탄두", "고고도공격드론", "군사용양자암호", "자율전투안드로이드", "작전용잠수정", "초장거리레일건", "전자기장장벽", "음속파무기", "지능형방어체계", "EMP방호장치",
          "스마트지뢰", "지각변동무기기초", "대기제어병기기초", "해저기지방어", "입자포시스템기초"
        ],
        4: [
          "행성방어쉴드", "소행성요격기", "궤도폭격시스템", "반물질병기", "공간왜곡방어", "시간정지필드", "중력장병기", "분자분해광선", "행성파괴급병기", "성간분쟁중재AI", "차원붕괴탄", "우주정거장방어포", "블랙홀탄", "문명종식시스템", "전우주방위망"
        ]
      },
      "건강관리": {
        1: [
          "범용항생제", "복제약(제네릭)", "치과용임플란트", "진단키트", "주사기제조", "수술용메스", "비타민제조", "혈압계제조", "약국체인", "붕대제조", "의료용스테인리스", "청진기제조", "범용진통제", "구급차설비", "체온계생산",
          "의료용거즈", "휠체어생산", "기초소독제", "안과용렌즈", "기초물리치료기"
        ],
        2: [
          "mRNA백신", "바이오시밀러", "표적항암제", "AI신약설계", "유전체분석", "개인형헬스케어", "디지털치료제", "임상수탁(CRO)", "전자약", "정밀진단기기", "웨어러블심전도", "바이오파운드리", "면역항암제", "세포치료제", "희귀질환치료제",
          "당뇨관리솔루션", "원격수술로봇", "재활로봇", "맞춤형영양제", "원격판독시스템"
        ],
        3: [
          "유전자가위치료", "줄기세포배양", "나노봇혈관수술", "노화지연약물", "치매역전치료", "합성단백질설계", "인공장기3D프린팅", "신경망복구", "마이크로바이옴치료", "사지재생배양액", "수면최적화유도기", "스트레스중화제", "대사최적화제", "근육합성나노봇", "바이오잉크",
          "기억보존장치기초", "청력복구임플란트", "시력회복망막", "맞춤형장기이식", "세포역분화"
        ],
        4: [
          "노화정복솔루션", "뇌이식인터페이스", "합성생명체디자인", "전신사이보그", "의식복제백업", "영생관리플랫폼", "인공진화설계", "신체개조스튜디오", "의식전이장치", "초감각증폭기", "통증차단뉴럴넷", "차원간생명유지", "무한재생DNA", "의식분산포털", "사후세계서버"
        ]
      },
      "커뮤니케이션": {
        1: [
          "지상파방송", "신문출판", "영화제작", "광고대행", "유선방송", "인쇄업", "우편서비스", "전화기제조", "라디오방송", "옥외광고물","잡지발행", "음반기획", "종이전단지", "전신전화소", "카탈로그제작","여행사기초", "전광판광고", "도서유통", "기초홍보대행", "비디오대여"
        ],
        2: [
          "종합포털서비스", "모바일메신저", "SNS플랫폼", "OTT서비스", "음원스트리밍", "데이터브로커", "디지털마케팅", "버추얼유튜버", "숏폼콘텐츠", "언어번역서비스", "라이브커머스", "뉴스애그리게이터", "클라우드게임", "커뮤니티운영", "MCN사업",
          "개인방송플랫폼", "웹툰스튜디오", "디지털폰트디자인", "이모티콘마켓", "검색엔진최적화","증강현실광고", "인공지능성우", "데이터마이닝", "스마트시티전광판", "커뮤니티매니지먼트"
        ],
        3: [
          "메타버스공간", "실감형게임", "홀로그램공연", "감정데이터거래", "언어번역AI", "뇌파기반메시징", "홀로포트서비스", "데이터인격화", "가상세계콘서트", "감각데이터스트리밍", "꿈데이터기록", "디지털향기스트리밍", "초실감오디오", "지능형홈네트워크", "디지털아바타에이전시",
          "뉴럴링크메신저", "다중언어동기화", "가상현실광고전략", "디지털기억공유", "인공지능기자"
        ],
        4: [
          "집단지성망", "의식공유네트워크", "전우주언어통합", "사후의식커뮤니티", "행성간통신백본", "지능합성방송", "다차원홀로그램망", "가상영혼포럼", "지성체통합포털", "차원간감정전송", "진리데이터스트림", "무한연결지능망", "행성간데이터허브", "정신적교감플랫폼", "전우주아카이브"
        ]
      },
      "금융": {
        1: [
          "상업은행", "화재보험", "생명보험", "증권위탁매매", "자산운용", "카드결제서비스", "신용평가기관", "저축은행", "할부금융", "환전업", "회계법인", "세무서비스", "연금관리", "보증보험", "어음중개소","부동산감정", "채권추심", "리스업", "금고제조", "전당업"
        ],
        2: [
          "인터넷전문은행", "간편결제플랫폼", "가상자산거래소", "로보어드바이저", "핀테크솔루션", "인슈어테크", "AI신용분석", "가상자산지갑", "스테이블코인발행", "NFT거래소", "결제대행(PG)", "비대면여신심사", "모바일월렛", "조각투자플랫폼", "크라우드펀딩",
          "소셜인베스팅", "자동결제API", "자산관리APP", "보안토큰발행(STO)", "가상자산수탁"
        ],
        3: [
          "AI퀀트트레이딩", "토큰화자산거래", "CBDC시스템", "양자보안은행", "알고리즘공매도", "예측시장플랫폼", "DAO자금관리", "AI금융비서", "디지털국가채권", "탈중앙화금융(DeFi)",
          "빅데이터리스크관리", "가치예측엔진", "실시간세무자동화", "마이크로결제망", "가상경제통계","우주영토보험", "인격자산금융", "실시간글로벌정산", "자동화벤처캐피탈", "가상자산파생상품"
        ],
        4: [
          "ASI경제예측", "성간무역금융", "자원우선권거래", "가치본위화폐", "시공간가치거래", "행성간환율조정", "전우주신용지수", "에너지본위화폐", "성간보험", "문명가치펀드", "초공간무역결제", "부의확률제어기", "차원거래증명소", "가상경제발권", "항성계중앙은행"
        ]
      },
      "소재": {
        1: [
          "철강판재", "범용화학용제", "시멘트제조", "구리제련", "범용플라스틱", "건설용골재", "알루미늄압출", "내화물생산", "황산공급", "아연도금", "특수합금강", "고무소재", "합성수지", "기초섬유", "내마모제","비철금속압연", "가성소다제조", "단열재생산", "도료용안료", "금속스크랩"
        ],
        2: [
          "양극재소재", "음극재탄소", "리튬정제", "니켈가공", "탄소섬유", "반도체용희귀가스", "방열소재", "전자파차단재", "나노입자코팅", "특수전해액", "고강도경량합금", "감광액(PR)", "세라믹필터", "엔지니어링플라스틱", "투명전도막",
          "유연디스플레이소재", "수소저장합금", "고열전도기판", "실리콘음극재", "나노와이어"
        ],
        3: [
          "초기상온초전도체", "탄소나노튜브", "그래핀응용", "자기치유소재", "메타물질", "특수세라믹", "액체금속", "양자점소재", "단일원자촉매", "바이오합성플라스틱", "극저온안정소재", "방사능차폐콘크리트", "우주항공용복합재", "스마트반응소재", "메모리금속",
          "희토류정밀추출", "고온초전도체", "분자각인고분자", "투명알루미늄", "나노셀룰로오스"
        ],
        4: [
          "상온초전도양산", "대기탄소고집적소재", "중력제어소재", "반물질저장용기", "초공간투과막", "강상관계물질", "고차원결정체", "우주끈복제소재", "항성내열소재", "물질재조합프레임", "시간지연소재", "불멸화세포기질", "에너지응축결정", "암흑물질안정기", "인공합성패널"
        ]
      },
      "필수소비재": {
        1: [
          "육가공", "식음료제조", "제분업", "생활잡화", "담배제조", "주류제조", "제과업", "유제품가공", "세제제조", "화장지생산","통조림제조", "냉동식품", "설탕제조", "식용유생산", "소금정제","기초농업", "기초화장품", "반려동물사료", "조미료제조", "차/커피유통"
        ],
        2: [
          "라스트마일택배", "실시간배달플랫폼", "새벽배송서비스", "이커머스물류", "기능성식품", "스마트팜부품", "수직농장운영", "간편식(HMR)제조", "식물성단백질", "콜드체인시스템", "위생안전인증", "가정용식물재배기",
          "맞춤형영양식", "무인편의점솔루션", "식재료최적화AI", "친환경패키징", "대체당제조","밀키트구독서비스", "프리미엄식자재유통", "신선식품직송", "반려동물헬스케어푸드", "바이오영양소","급식자동화", "인공당밀", "신선도유지필름"
        ],
        3: [
          "배양육생산", "식물성대체육", "3D음식프린팅", "합성향료디자인", "미생물배양식량", "해조류기반식품", "식량데이터분석", "도심완전냉장망", "식물공장자동화", "대체단백질플랫폼",
          "기능성음료설계", "영양상태모니터링", "자동조리로봇", "영양캡슐팩", "합성우유배양","완전재활용패키징", "식문화메타버스", "유전자맞춤식단", "스마트신선도센서", "식품데이터권"
        ],
        4: [
          "식량복제기", "행성간식량보급", "분자요리시스템", "의식전용영양액", "나노머신영양공급", "행성간식량거래", "영구보존식량", "물질재조합식단", "무중력특화식품", "에너지본위식량", "자아유지용에너지팩", "태양광직접흡수제", "식량텔레포팅", "무한자원순환계", "항성간물류식량"
        ]
      },
      "산업재": {
        1: [
          "벌크선건조", "특수강건설", "굴착기제조", "산업용펌프", "배전변압기", "공작기계", "플랜트설계", "산업용베어링", "화물트럭제조", "지게차생산", "산업용밸브", "크레인설치", "배관설비", "철강구조물", "기초볼트나사",
          "철도차량부품", "엘리베이터부품", "산업용압축기", "조선소크레인", "항만하역장비"
        ],
        2: [
          "물류용드론", "산업용협동로봇", "공장자동화SW", "자율주행트럭", "3D적층제조", "웨어러블슈트", "스마트팩토리센서", "무인창고관리", "AMR물류로봇", "친환경추진선", "모듈러주택", "고속열차엔진", "UAM기체제조", "원격건설관제", "자동적재솔루션",
          "배송로봇", "특수제조로봇", "디지털물류플랫폼", "예지보전시스템", "스마트포트인프라"
        ],
        3: [
          "가정용안드로이드", "달기지건설기계", "재사용로켓부품", "초고속하이퍼루프", "인공중력발생기", "해저채굴로봇", "상온초전도선재", "심해기지건조", "우주항만설비", "텔레프레즌스로봇", "분자단위적층장치", "심우주통신안테나", "외계기지건설", "자기부상물류망", "궤도자원분류기",
          "소행성포획그물", "우주선방사능차폐", "우주엘리베이터기초", "군사용드론스웜", "성간우주선기초"
        ],
        4: [
          "궤도엘리베이터", "소행성채굴기", "행성테라포밍기", "공간압축물류", "워프항법부품", "분자조립기", "자율문명건설", "행성간이동포털", "물질전송시스템", "차원안정화장치", "화이트홀물질수집", "우주메가스트럭처", "시공간수선기", "항성간항로개척", "스타게이트"
        ]
      },
      "유틸리티": {
        1: [
          "전기공급", "도시가스", "수처리", "폐기물처리", "지역난방", "하수도관리", "기초쓰레기매립", "가로등운영", "공용전신주", "댐운영", "상수도파이프", "정수기필터", "전기검침", "폐유처리", "산업용기체공급","가스안전점검", "수위조절시설", "산업용수공급", "공공분수시설", "기초소방용수"
        ],
        2: [
          "환경관리시스템", "스마트그리드", "폐수재활용", "미세먼지저감", "지능형상수도", "탄소배출권관리", "에너지효율화SW", "수소배관망", "스마트가로등", "전기차충전그리드",
          "재난대응인프라", "수자원최적화AI", "자원회수센터", "공공와이파이망", "대기오염감시","신재생연계망", "소음공해제어", "기상정보서비스", "스마트가로수", "냉난방에너지공유"
        ],
        3: [
          "자원순환로봇", "대기정화타워", "해수담수화플랜트", "스마트시티인프라", "지열냉각시스템", "플라즈마폐기물소각", "인공강우조절", "도시완전순환망", "탄소중립인프라", "플라스틱분해균주",
          "재난완화필드", "스마트시티운영AI", "수질완전정화나노머신", "자원회수자동화", "스마트기후돔","물부족해결플랜트", "중수도통합망", "생태계모니터링", "대기성분인공조절", "공공에너지공유"
        ],
        4: [
          "행성기후조절", "행성보호쉴드", "기후복원나노봇", "대기조성제어", "지각안정화장치", "항성에너지분배", "우주폐기물수거", "행성간자원순환", "다차원환경관리", "행성산소공급망", "지자기장강화장치", "시공간유지시스템", "문명유지인프라", "우주엔트로피역전", "항성기상중추"
        ]
      },
      "부동산": {
        1: [
          "주택임대", "오피스빌딩", "산업단지분양", "상업시설운영", "창고임대", "토지개발", "리조트운영", "쇼핑몰관리", "주차시설", "공공임대주택", "농지임대", "분양대행", "건물유지보수", "기초택지조성", "모델하우스제작",
          "호텔건물임대", "산림개발부지", "전시장임대", "등기대행업", "오피스텔분양"
        ],
        2: [
          "데이터센터리츠", "스마트홈관리", "물류창고리츠", "코워킹스페이스", "실버타운운영", "도시재생사업", "스마트빌딩시스템", "리모델링솔루션", "프롭테크서비스", "건물에너지최적화",
          "가상모델하우스", "주차자동화", "임대차관리SW", "청년창업공간", "공동주거관리","공유오피스플랫폼", "지능형보안빌딩", "모듈러건축부지", "역세권개발사업", "스마트팜부지"
        ],
        3: [
          "해상도시분양", "해저거주구관리", "스마트시티운영권", "지하도시개발", "수직농장리츠", "공중도시부지", "가상현실토지거래", "심해기지임대", "우주항만부지", "달기지초기분양",
          "메타버스상권개발", "지하시설자동화", "빙하위부동산업", "성층권호텔부지", "수직물류터미널","극지연구소부지", "자원채굴권리", "화성거주구청약", "부유식에너지거점", "해양생태도시"
        ],
        4: [
          "테라포밍권리", "행성거주구분양", "궤도스테이션임대", "초공간부동산", "행성간이동포털부지", "다차원거주지", "은하계무역거점", "성간통신망기지", "항성간항로사용권", "의식업로딩서버부지", "시공간부동산거래", "차원안정화구역", "블랙홀근접부지", "가상영혼분양권", "전우주거지최적화"
        ]
      },
      "자유소비재": {
        1: [
          "가전제품", "내연기관차", "의류제조", "가구제조", "완구제조", "스포츠용품", "대형마트유통", "신발생산", "화장품제조", "백화점", "편의점체인", "주방기구", "여행사", "호텔프랜차이즈", "패스트푸드","악기생산", "문구류", "시계제조", "침구류생산", "미용실프랜차이즈"
        ],
        2: [
          "전기차설계", "스마트폰제조", "명품브랜드", "모바일게임", "웹툰제작", "전기차충전망", "퍼스널모빌리티", "OTT서비스", "스마트홈기기", "콘솔게임기", "이커머스플랫폼", "웨어러블기기", "구독경제서비스", "배달플랫폼", "K-팝기획사",
          "이스포츠리그", "버추얼인플루언서", "개인미디어장비", "메이크업AI", "프리미엄가전"
        ],
        3: [
          "자율주행운영", "개인용항공기(VTOL)", "메타버스쇼핑", "AI콘텐츠생산", "배양육레스토랑", "우주여행패키지", "홀로그램기획", "가상현실관광", "스마트의류", "감정인식디바이스", "뇌파동기화게임", "로봇애완동물", "디지털사후세계", "개인맞춤형향수", "자아디자인서비스",
          "우주호텔운영", "실감형스포츠", "기억체험샵", "인공지능동화", "가상패션브랜드"
        ],
        4: [
          "개인용우주선", "물질합성식기", "행성간관광", "인격디자인스튜디오", "신경예술콘텐츠", "가상자아매니지먼트", "의식테마파크", "사고전달서비스", "꿈공유플랫폼", "시공간여행사", "외계종족문화체험", "물질복제기공급", "영생취미라이프", "우주패션브랜드", "차원여행장비"
        ]
      },
      "재건": {
        1: [
          "도시복구건설", "폐허정리", "기초토목", "임시수용시설", "도로재정비", "긴급물자유통", "기초방역", "잔해재활용", "상하수도복구", "임시전력망", "교량보강", "기초소방설비", "긴급구조장비", "오염수여과", "임시병원가동",
          "지뢰제거기초", "재해지역측량", "기초보안펜스", "전재민지원", "피해조사솔루션"
        ],
        2: [
          "방사능제염", "토양오염복원", "수질정화사업", "도시재생디자인", "인프라현대화", "스마트시티전환", "미세먼지제거", "산림재건사업", "해양쓰레기수거", "생태통로건설", "도심녹화솔루션", "지능형재난경보", "석면제거업", "지반강화공법", "환경영향평가AI",
          "산업폐기물처리", "기후대응인프라", "정밀오염분석", "도심하천재생", "폐기물에너지화"
        ],
        3: [
          "생태복원사업", "멸종위기종복원", "수소도시망구축", "대기정화사업", "해양생태계재건", "방호돔건설", "산소농도조절기", "빙하복원기술", "인공강우조절", "토양성분정상화", "오존층복구장치", "사막녹화사업", "생태계모니터링AI", "자연재해제어기", "지진파흡수장치",
          "초미세먼지필터", "플라즈마소각로", "수소도시운영", "생태계모뮬러", "재난완화필드"
        ],
        4: [
          "문명재건시스템", "테라포밍엔지니어링", "인류유산아카이브", "행성생태계시뮬", "문명복구안내AI", "종자기지관리", "기후조절엔진", "행성보호막", "대기조성제어기", "바이오스피어운영", "항성계보존지구", "다차원생태계관리", "차원복원엔진", "문명시뮬데이터뱅크", "은하유물복원"
        ]
      }
    }

    self.RED = "\033[91m"; self.BLUE = "\033[94m"; self.YELLOW = "\033[93m"; self.GREEN = "\033[92m"; self.RESET = "\033[0m"; self.CYAN = "\033[96m";

  # -- news.py 관련 --
  def add_pre_event(self, date_str, d_day_val, category, target, public_txt, premium_txt):
    """사전 선반영 및 도약 이벤트를 등록하는 메서드"""
    self.pre_reflection_events.append({
      "date": date_str,
      "d_day": f"D-{d_day_val}",
      "category": category,
      "target": target,
      "public_text": public_txt,
      "premium_text": premium_txt
    })

  def get_pre_events(self):
    """저장된 사전 이벤트 반환"""
    return self.pre_reflection_events

  def clear_pre_events(self):
    """초기화 시 사전 이벤트 비우기"""
    self.pre_reflection_events = []

  # -- 게임 저장 --
  def create_db(self):
    """SQLite 데이터베이스 파일과 테이블을 생성합니다."""
    try:
      cur = self.conn.cursor()
      # 테이블이 없을 경우에만 생성 (날짜, 종목명, 주가, 시가총액)
      cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_history (
          date TEXT,
          company_name TEXT,
          price INTEGER,
          market_cap INTEGER
        )
      """)
      self.conn.commit()
      print("🗄️ SQLite 데이터베이스 연결 및 테이블 확인 완료.")
    except Exception as e:
      print(f"❌ DB 테이블 생성 실패: {e}")

  # g.py의 StockGameEngine 클래스 내부에 추가
  def save_game(self, my_cash, my_portfolio, filename="save_game.json"):
    """엔진 상태와 플레이어 데이터를 통합 저장 (SQLite 최적화 버전)"""
    import json
    import copy
    from datetime import datetime

    try:
      # 1. 원본 데이터 보호를 위해 깊은 복사
      stocks_to_save = copy.deepcopy(self.stocks)
      delisted_to_save = copy.deepcopy(self.delisted_stocks)

      # 2. datetime 객체 문자열 변환
      for s_list in [stocks_to_save, delisted_to_save]:
        for s in s_list:
          if 'meta' in s:
            for key, value in s['meta'].items():
              if isinstance(value, datetime):
                s['meta'][key] = value.strftime("%Y-%m-%d %H:%M:%S")

      # 3. 저장 데이터 구조 생성 (daily_history는 제외하여 다이어트)
      save_data = {
        "engine": {
          "current_date": self.current_date.strftime("%Y-%m-%d"),
          "virtual_weekday": self.virtual_weekday,
          "daily_history": {}, # [최적화] 과거 기록은 DB에 있으므로 비웁니다.
          "stocks": stocks_to_save,
          "groups": self.groups,
          "macro": self.macro,
          "base_item_price": self.base_item_price,
          "cumulative_inflation": getattr(self, 'cumulative_inflation', 1.0),
          "has_paid_news_access": getattr(self, 'has_paid_news_access', False),
          "next_billing_date": self.next_billing_date.strftime("%Y-%m-%d") if getattr(self, 'next_billing_date', None) else None,
          "gri": self.gri,
          "wsi": self.wsi,
          "max_tech_reached": self.max_tech_reached,
          "delisted_stocks": delisted_to_save,
          "current_scenario": self.current_scenario,
          "world_line": self.world_line,
          "earnings_history": self.earnings_history, # 실적은 상대적으로 가벼워 유지
          "used_all_time": list(self.used_all_time)
        },
        "player": {
          "my_cash": my_cash,
          "my_portfolio": my_portfolio
        }
      }

      # 4. 파일 저장 (indent를 제거하면 저장 속도가 더 빨라집니다)
      with open(filename, "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, default=str)
     
      print(f"💾 [{self.current_date.strftime('%Y-%m-%d')}] 스냅샷이 안전하게 저장되었습니다. (과거 주가는 DB에 실시간 저장 중)")
     
    except Exception as e:
      print(f"❌ 저장 중 오류 발생: {e}")

  def load_game(self, filename="save_game.json"):
    """저장 파일 복구 (과거 기록은 DB에서 참조)"""
    if not os.path.exists(filename):
      print("⚠️ 세이브 파일을 찾을 수 없습니다.")
      return None
     
    try:
      with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
       
      eng = data["engine"]
     
      # 엔진 핵심 상태 복구
      self.current_date = datetime.strptime(eng["current_date"], "%Y-%m-%d")
      self.virtual_weekday = eng["virtual_weekday"]
     
      # [최적화] 메모리 차트 데이터는 빈 값으로 시작
      self.daily_history = {}
     
      self.stocks = eng["stocks"]
      self.groups = eng["groups"]
      self.macro = eng["macro"]
      self.base_item_price = eng["base_item_price"]
      self.cumulative_inflation = eng.get("cumulative_inflation", 1.0)
      self.gri = eng["gri"]
      self.wsi = eng["wsi"]
      self.max_tech_reached = eng["max_tech_reached"]
      self.delisted_stocks = eng["delisted_stocks"]
      self.current_scenario = eng["current_scenario"]
      self.world_line = eng["world_line"]
      self.earnings_history = eng["earnings_history"]
      self.used_all_time = set(eng.get("used_all_time", []))

      # 🚀 [추가 부분] 구독 상태 및 결제 만료일 복구
      # 저장할 때 넣었던 키값("has_paid_news_access" 등)을 그대로 가져옵니다.
      self.has_paid_news_access = eng.get("has_paid_news_access", False)
     
      billing_str = eng.get("next_billing_date")
      if billing_str:
        # 문자열로 저장된 날짜를 다시 파이썬 날짜 객체(datetime)로 변환
        self.next_billing_date = datetime.strptime(billing_str, "%Y-%m-%d")
      else:
        self.next_billing_date = None
     
      # [기존 로직] 종목 날짜 복원
      # apply_price_change 내부 수렴 로직 예시
      for s in self.stocks:
        meta = s['meta']
        name = meta['c_name']
       
        # 예: 실적 발표 선반영 (D-7 로직)
        if name in self.pending_events["earnings"]:
          target_info = self.pending_events["earnings"][name]
          days_left = (target_info['date'] - self.current_date).days
         
          if 0 < days_left <= 7:
            # 목표 주가를 미리 계산 (예: 순이익 기반 적정가)
            expected_price = target_info['expected_price']
            # 매일 차이의 15%씩 강제 수렴 (선반영)
            price_gap = (expected_price - s['price']) / days_left
            meta['momentum'] += (price_gap / s['price']) * 0.5

      print(f"✅ [{self.current_date.strftime('%Y-%m-%d')}] 게임을 성공적으로 불러왔습니다.")
      return data["player"]
     
    except Exception as e:
      print(f"❌ 불러오기 중 오류 발생: {e}")
      return None

  def clear_save_file(self, filename="save_game.json"):
    """저장 파일 삭제 (초기화)"""
    if os.path.exists(filename):
      os.remove(filename)
 
  def clear_all_history(self):
    """새 게임 시작 시 SQLite DB의 모든 주가 기록을 삭제합니다."""
    try:
      # DB 연결이 되어있는지 확인
      if not hasattr(self, 'conn') or self.conn is None:
        import sqlite3
        self.conn = sqlite3.connect("stock_data.db", check_same_thread=False)
     
      cur = self.conn.cursor()
      # 테이블의 모든 데이터 삭제
      cur.execute("DELETE FROM stock_history")
      self.conn.commit()
      print("🧹 [시스템] SQLite DB의 모든 과거 기록을 삭제했습니다.")
    except Exception as e:
      print(f"❌ DB 초기화 중 오류 발생: {e}")
 
  # G.PY 내부
  def get_ui_chart_data(self, company_name, days=30):
    try:
      cur = self.conn.cursor()
     
      # days가 900,000 이상(전체 버튼)이면 LIMIT을 무시하고
      # 처음부터 끝까지 과거순(ASC)으로 가져옵니다.
      if days > 900000:
        cur.execute("""
          SELECT price FROM stock_history
          WHERE company_name = ?
          ORDER BY date ASC
        """, (company_name,))
        rows = cur.fetchall()
        return [row[0] for row in rows] # 이미 과거순이므로 바로 리턴
       
      else:
        # 특정 기간(1주, 1달 등)은 기존처럼 최신순으로 잘라서 가져옵니다.
        cur.execute("""
          SELECT price FROM stock_history
          WHERE company_name = ?
          ORDER BY date DESC LIMIT ?
        """, (company_name, days))
       
        rows = cur.fetchall()
        if not rows: return []
        prices = [row[0] for row in rows]
        return prices[::-1] # 짧은 기간은 뒤집어서 반환
       
    except Exception as e:
      print(f"❌ DB 로드 실패: {e}")
      return []
   
  # -- ui.py 와 연결 --
  # -- [G.PY 내부] StockGameEngine 클래스 안에 아래 함수들을 순서대로 배치하세요 -
  def get_macro_snapshot(self):
    """[AttributeError 해결] 대시보드용 매크로 지표 반환"""
    m = self.macro
    return {
      "interest": m.get("interest_rate", 0),
      "oil": m.get("oil_price", 0),
      "exchange": m.get("exchange_rate", 0),
      "cpi_display": f"물가체감: 2000년 ₩1,000 → 현재 ₩{self.base_item_price:,.0f}"
    }

  def get_chart_data(self, company_name, days=30):
    """DB에서 특정 종목의 최근 N일치 주가를 가져옴"""
    cur = self.conn.cursor()
    cur.execute("""
      SELECT price FROM stock_history
      WHERE company_name = ?
      ORDER BY date DESC LIMIT ?
    """, (company_name, days))
   
    prices = [row[0] for row in cur.fetchall()]
    return prices[::-1]
 
  def get_stock_snapshots(self):
    """종목별 모든 meta 데이터를 UI로 전달"""
    snapshots = []
    for s in self.stocks:
      snapshots.append({
        "name": s['meta']['c_name'],
        "price": int(s['price']),
        "rate": s.get('rate', 0.0),
        "meta": s['meta']
      })
    return snapshots

  # G.PY 내부
  def get_ui_packet(self):
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    return {
      "date": f"{self.current_date.strftime('%Y-%m-%d')} ({weekdays[self.virtual_weekday]})",
      "level": self.max_tech_reached,
      "gri": self.gri, # 엔진의 실시간 GRI
      "wsi": self.wsi, # 엔진의 실시간 WSI
      "scenario": self.current_scenario,
      "macro": self.macro,
      "stocks": [
        {
          "name": s['meta']['c_name'],
          "price": int(s['price']),
          "rate": s.get('rate', 0.0), # G.PY 규칙이 이미 적용된 등락률
          "meta": s['meta']
        } for s in self.stocks
      ]
    }

  def run_one_second(self):
    """UI 타이머 호출용: 수치 변화 없이 현재 확정된 패킷만 반환"""
    return self.get_ui_packet()

  def calculate_daily_change(self, s):
    """가치 기반 등락율 계산 엔진"""
    meta = s['meta']
    daily_target = 0.0003
    if "대공황" in self.current_scenario: daily_target = -0.015
    risk_penalty = (meta.get('risk_score', 0) / 1000)
    perf = (meta.get('efficiency', 0.05) + daily_target + meta.get('momentum', 0) - risk_penalty)
    return max(-0.3, min(0.3, perf))

  def next_day_process(self):
    """UI에서 NEXT DAY를 눌렀을 때 실행되는 엔진의 실제 연산 루프"""
    # [중요] 수정된 next_day 내부에서 이미 SQLite INSERT가 수행됩니다.
    self.next_day(silent=True)
   
    # record_current_state 내부에서도 거대한 리스트를 쓰고 있다면
    self.record_current_state()
   
    # (4) UI가 바로 쓸 수 있도록 패킷 반환
    return self.get_ui_packet()
 
  # -- 기본 코드 시작 --
  # --- 유틸리티 및 초기화 ---
  def get_width(self, text):
    return sum(2 if ord('가') <= ord(c) <= ord('힣') else 1 for c in text)
 
  def pad_text(self, text, target):
    return text + " " * max(0, target - self.get_width(text))
 
  def get_tech_level(self):
    """[v170.0+정보비대칭] 자연 진화 엔진: 테크 1~3은 예약 시스템을 거쳐 진화!"""
    cy = self.current_date.year
    current_lv = self.max_tech_reached
   
    # 분기점 이후 시나리오 상태 체크
    is_depression = "대공황" in self.current_scenario and "극복" not in self.current_scenario
    is_t4_world = "T4 발전" in self.current_scenario
    is_t3_world = "T3 유지" in self.current_scenario

    if is_depression: return current_lv # 대공황 시 발전 중단

    # 이미 진화 예약이 걸려있다면 새로 주사위를 굴리지 않음
    if self.pending_events.get("tech_jump"):
      evolution_chance = 0.0
    else:
      evolution_chance = 0.0
     
      # T1 -> T2 (확률 그대로)
      if current_lv == 1 and self.gri >= 2500:
        t1_probs = {2013: 12, 2014: 18, 2015: 30, 2016: 18, 2017: 12}
        if cy in t1_probs: evolution_chance = (t1_probs[cy] / 100) / 252
        elif cy >= 2018: evolution_chance = 0.10 / 252
     
      # T2 -> T3 (확률 그대로)
      elif current_lv == 2 and self.gri >= 14000:
        t2_probs = {2035: 2, 2036: 4, 2037: 5, 2038: 9, 2039: 13, 2040: 25, 2041: 13, 2042: 9, 2043: 5, 2044: 5}
        if cy in t2_probs: evolution_chance = (t2_probs[cy] / 100) / 252
        elif cy >= 2045: evolution_chance = 0.10 / 252
         
      # T3 -> T4 (분기점 통과 후 시나리오에 따라 확률 가동)
      elif current_lv == 3:
        if is_t3_world: return 3 # T3 세계선은 진화 불가
        elif is_t4_world:
          evolution_chance = 0.1 / 252
        elif cy >= 2050 and self.gri >= 150000 and not is_depression:
          evolution_chance = 0.05 / 252

    # ---------------------------------------------------------
    # [1] 주사위 판정 및 예약 (사건 발생 30일 전)
    # ---------------------------------------------------------
    if evolution_chance > 0 and random.random() < evolution_chance:
      # 즉시 레벨업 하지 않고 30일 뒤로 예약만 기록!
      jump_date = self.current_date + timedelta(days=30)
      self.pending_events["tech_jump"] = {
        "target_lv": current_lv + 1,
        "date": jump_date
      }
      # 이 시점부터 apply_price_change 엔진이 IT주 모멘텀을 올리기 시작함

    # ---------------------------------------------------------
    # [2] 예약된 날짜 체크 및 실제 실행 (D-Day)
    # ---------------------------------------------------------
    if self.pending_events.get("tech_jump"):
      jump_info = self.pending_events["tech_jump"]
      # 오늘이 예약된 날짜이거나 그 이후라면 실제 진화 처리
      if self.current_date.date() >= jump_info["date"].date():
        self.max_tech_reached = jump_info["target_lv"]
       
        # 뉴스 출력 (news.py가 담당하겠지만, 엔진 가시성을 위해 로그 남김)
        if not getattr(self, 'silent_mode', False):
          self.daily_news.append(f"{self.CYAN}🚀 [시대 진화] {cy}년, 문명이 {self.max_tech_reached}단계로 도약했습니다!{self.RESET}")
       
        # 진화가 완료되었으므로 예약 장부 비움
        self.pending_events["tech_jump"] = None

    return self.max_tech_reached
 
  def initialize_market(self, silent=False):
    print(f"🚀 [시스템] v19.0 가치 본위 엔진 가동 중...")
    # 1. 그룹사 및 일반 주식 생성
    for gn in ["제니스", "서한", "가온", "범양", "버거"]:
      gid = f"GROUP_{gn}"; self.groups[gid] = {"name": gn, "active": True}
      for i, ind in enumerate(random.sample(self.MAIN_INDUSTRIES, 2)):
        tier = "대" if i == 0 else "중"
        self.stocks.append(self.create_stock_data(None, ind, tier, gid))
    for _ in range(random.randint(25, 30)):
      self.stocks.append(self.create_stock_data(random.choice(self.NAME_DB), random.choice(self.MAIN_INDUSTRIES), "소"))

    # 2. 등급과 주가 최종 확정
    self.reassign_tiers_by_cap()
   
    # 3. [철학 반영] 상장일(1999-12-31) 데이터를 모든 저장소의 '기준점'으로 박제
    date_str = self.current_date.strftime('%Y-%m-%d')
    db_records = []
   
    for s in self.stocks:
      self.apply_stock_event(s, silent=silent)
     
      # 등락률 계산
      rate = s.get('rate', 0.0) / 100.0
      meta = s['meta']
      tier = meta.get('tier', '소형주') # 체급 정보 가져오기
     
      # [개선 핵심] 체급 및 주가 등락에 따른 현실적인 변동 계수 적용
      if "대형주" in tier:
        multiplier = 0.5 # 대형주는 덜 민감함
      elif "중형주" in tier:
        multiplier = 1.0 # 중형주
      else:
        multiplier = 2.5 # 소형주는 급등락에 크게 출렁임
     
      if rate > 0:
        # 상승 시: 기관/외국인 매수세 유입, 개인 매도
        meta['foreign_share'] = max(0.001, min(0.99, meta['foreign_share'] * (1.0 + rate * 1.5 * multiplier)))
        meta['inst_share'] = max(0.001, min(0.99, meta['inst_share'] * (1.0 + rate * 1.8 * multiplier)))
        meta['retail_share'] = max(0.001, min(0.99, meta['retail_share'] * (1.0 - rate * 0.8 * multiplier)))
      else:
        # 하락 시: 기관/외국인 손절매 및 개인의 저가 매수 유입
        meta['foreign_share'] = max(0.001, min(0.99, meta['foreign_share'] * (1.0 + rate * 2.0 * multiplier)))
        meta['inst_share'] = max(0.001, min(0.99, meta['inst_share'] * (1.0 + rate * 1.8 * multiplier)))
        meta['retail_share'] = max(0.001, min(0.99, meta['retail_share'] * (1.0 - rate * 0.5 * multiplier)))
     
      # 지분율 정규화 (대주주와 자사주는 고정, 유동 지분만 남은 비율에 맞춤)
      fixed_shares = meta.get('treasury_share', 0.0) + meta.get('owner_share', 0.0)
      remaining_shares = max(0.0, 1.0 - fixed_shares)
     
      sum_floating = meta['foreign_share'] + meta['inst_share'] + meta['retail_share']
      if sum_floating > 0:
        meta['foreign_share'] = (meta['foreign_share'] / sum_floating) * remaining_shares
        meta['inst_share'] = (meta['inst_share'] / sum_floating) * remaining_shares
        meta['retail_share'] = (meta['retail_share'] / sum_floating) * remaining_shares

      db_records.append((
        date_str,
        s['meta']['c_name'],
        int(s['price']),
        int(s['market_cap'])
      ))
   
    # [핵심] 상장 첫날 기록을 DB에 일괄 저장 (렉 방지)
    try:
      cur = self.conn.cursor()
      cur.executemany("INSERT INTO stock_history VALUES (?, ?, ?, ?)", db_records)
      self.conn.commit()
      print(f"📦 상장일({date_str}) 데이터 {len(db_records)}건이 DB에 저장되었습니다.")
    except Exception as e:
      print(f"❌ 상장일 데이터 저장 실패: {e}")
   
    # 4. 초기 시장 자산 합계 동기화
    self.initial_market_total_cap = sum(s['market_cap'] for s in self.stocks)
    if self.initial_market_total_cap == 0:
      self.initial_market_total_cap = 1.0
   
  def create_stock_data(self, base_name, ind, tier="소", group_id=None):
    """[v140.0] 지배구조 엔진: 자사주 및 체급별 5대 주주 구성 통합 로직"""
    cy = self.current_date.year
    actual_lv = self.get_tech_level()
    sector = self.SECTOR_MAP.get(ind, "Value")

    # 1. 황제주 성향 결정 (기본 분할 거부 로직 유지)
    dice_split = random.random()
    if tier == "대":
      will_to_split = dice_split > 0.25
    elif tier == "중":
      will_to_split = dice_split > 0.05
    else:
      will_to_split = True

    # 2. 자사주(Treasury) 결정 (섹터 + 체급 보정)
    if sector == "Growth":
      base_ts = random.uniform(0.00, 0.05)
    elif sector == "Value":
      base_ts = random.uniform(0.08, 0.15)
    elif sector == "Defensive":
      base_ts = random.uniform(0.05, 0.10)
    else:
      base_ts = random.uniform(0.01, 0.07)

    if tier == "소": base_ts -= 0.01
    elif tier == "대": base_ts += 0.02
    final_ts = max(0.0, base_ts)

    # 3. 주주 지분 분배 (자사주 제외 100% 기준 상대 비율)
    if tier == "대":
      owner_r = random.uniform(0.35, 0.45) # 대주주 (안정적 경영권)
      foreign_r = random.uniform(0.30, 0.40) # 외국인 (높은 선호도)
      inst_r = random.uniform(0.10, 0.15)  # 기관
    elif tier == "중":
      owner_r = random.uniform(0.30, 0.45)
      foreign_r = random.uniform(0.05, 0.15)
      inst_r = random.uniform(0.10, 0.20)
    else: # 소형주
      owner_r = random.uniform(0.25, 0.40)
      foreign_r = random.uniform(0.01, 0.05) # 외국인 거의 없음
      inst_r = random.uniform(0.05, 0.10)

    # 나머지는 개인(Retail) 몫
    retail_r = max(0.0, 1.0 - (owner_r + foreign_r + inst_r))

    # 4. 절대 지분율 변환 (전체 100% 기준)
    rem_p = 1.0 - final_ts
    owner_abs = owner_r * rem_p
    foreign_abs = foreign_r * rem_p
    inst_abs = inst_r * rem_p
    retail_abs = retail_r * rem_p

    # 5. 체급별 가격 및 주식수 설정
    if tier == "대":
      p = random.randint(40000, 80000)
      s_count = random.randint(100, 1000) * 1000000
    elif tier == "중":
      p = random.randint(15000, 35000)
      s_count = random.randint(50, 200) * 1000000
    else:
      p = random.randint(1000, 15000)
      s_count = random.randint(1, 50) * 1000000

    # 6. 이름 생성 및 그룹 정보 매칭
    is_group = (group_id is not None)
    gn_arg = self.groups[group_id]['name'] if is_group else None
    info_arg = ind if is_group else base_name
    full_name = self.get_unique_name(is_group, gn_arg, info_arg)

    return {
      "meta": {
        "c_name": full_name,
        "will_to_split": will_to_split,
        "listed_date_dt": self.current_date,
        "listed_date": self.current_date.strftime('%Y-%m-%d'),
        "group_id": group_id,
        "group": gn_arg,
        "tier": f"{tier}형주",
        "ind": ind,
        "sub": random.choice(self.INDUSTRY_LEVELS.get(ind, {}).get(actual_lv, ["기본 산업"])),
        "char": "Normal",
        "risk_score": 0.0,
        "delist_timer": 0,
        "split_count": 0,
        "merge_count": 0,
        "assets": float(p * s_count),
        "efficiency": random.uniform(0.02, 0.08),
        "momentum": 0.0,
        "continuous_loss_count": 0,
        "risk_sensitivity": {"대": 0.1, "중": 0.5, "소": 1.2}.get(tier, 1.0),
        # 지배구조 엔진 데이터 핵심 필드
        "treasury_share": final_ts, # 자사주
        "owner_share": owner_abs,  # 대주주
        "foreign_share": foreign_abs, # 외국인
        "inst_share": inst_abs,   # 기관
        "retail_share": retail_abs  # 개인
      },
      "price": p, "rate": 0.0, "shares": s_count, "market_cap": p * s_count
    }

  def format_cap(self, cap):
    """시가총액을 억, 조, 경 단위로 변환하여 가독성을 높임"""
    if cap >= 1_000_000_000_000_000:
      return f"{cap / 1_000_000_000_000_000:.2f}경"
    if cap >= 1_000_000_000_000:
      return f"{cap / 1_000_000_000_000:.2f}조"
    if cap >= 100_000_000:
      return f"{cap / 100_000_000:.1f}억"
    return f"{cap:,.0f}"
 
  # [로직 1] 그룹사 및 일반 주식 명칭 중복 방지 엔진
  def get_unique_name(self, is_group_member, group_name, info):
    # 1. 그룹 계열사인 경우 (예: 제니스 IT)
    if is_group_member:
      final_name = f"{group_name} {info}"
      if final_name in self.used_all_time:
        suffix = 2
        while f"{final_name} {suffix}" in self.used_all_time:
          suffix += 1
        final_name = f"{final_name} {suffix}"
      self.used_all_time.add(final_name)
      return final_name

    # 2. 일반 주식인 경우 (전달받은 info가 있으면 그것을 기반으로 생성)
    # 만약 info가 None이거나 비어있다면 name_pool에서 새로 꺼냄
    base_core_name = info if info else (self.name_pool.pop(0) if self.name_pool else "미명")
   
    # 이름 중복 및 세대 관리
    final_name = base_core_name if self.current_generation == 1 else f"{base_core_name} {self.current_generation}"
   
    # 만약 생성한 이름이 이미 존재한다면 (이름 풀을 다 썼을 때)
    if final_name in self.used_all_time:
      if self.name_pool: # 아직 풀에 여유가 있다면 다른 이름 시도
        return self.get_unique_name(False, None, self.name_pool.pop(0))
      else: # 풀이 다 찼다면 세대를 올림
        self.current_generation += 1
        self.name_pool = [n for n in self.NAME_DB if n not in self.group_base_names]
        random.shuffle(self.name_pool)
        return self.get_unique_name(False, None, self.name_pool.pop(0))

    self.used_all_time.add(final_name)
    return final_name
 
  # [로직 2] 실적 생성 엔진 (이자 비용 및 자산 반영)
  def announce_earnings(self, s):
    """[v41.1] 현실적 실적 엔진: 데이터 부재 방어 및 서프라이즈 로직 추가"""
    from datetime import datetime
    import random

    meta = s['meta']
    name = meta['c_name']
    year = str(self.current_date.year)
    month = self.current_date.month
    quarter = {3: "1분기", 4: "1분기", 6: "2분기", 7: "2분기", 9: "3분기", 10: "3분기", 12: "4분기", 1: "4분기"}.get(month, "수시")

    # [수정 1] 만약 expected_earnings가 없다면 즉시 생성 (에러 방지 핵심)
    if not meta.get('expected_earnings'):
        # 이전 대화에서 정의한 calculate_potential_earnings 또는 내부 계산 로직 호출
        meta['expected_earnings'] = self.calculate_potential_earnings(s)

    # 1. 기초 데이터 및 날짜 객체 검증
    ld = meta.get('listed_date_dt')
    if not ld or isinstance(ld, str):
        try:
            ld = datetime.strptime(meta['listed_date'], '%Y-%m-%d')
            meta['listed_date_dt'] = ld
        except (KeyError, ValueError):
            ld = self.current_date
            meta['listed_date_dt'] = ld

    age_days = (self.current_date - ld).days
    tier = meta.get('tier', '소형주')
    
    # 2. 매출 및 비용 계산
    revenue = meta['assets'] * random.uniform(0.04, 0.10)
    base_cost = {"대형주": 0.015, "중형주": 0.025, "소형주": 0.04}.get(tier, 0.04)
    
    # 기술 도태 패널티
    tech_penalty = 0.0
    if getattr(self, 'max_tech_reached', 1) > 1:
        # INDUSTRY_LEVELS 참조 시 에러 방지
        ind_levels = getattr(self, 'INDUSTRY_LEVELS', {}).get(meta['ind'], {})
        t1_subs = ind_levels.get(1, [])
        if meta['sub'] in t1_subs:
            tech_penalty = 0.03

    # 3. 영업이익 및 순이익 (티어 보너스 포함)
    tier_bonus = {"대형주": 0.02, "중형주": 0.00, "소형주": -0.01}.get(tier, 0)
    op_margin = meta['efficiency'] - base_cost + tier_bonus - tech_penalty
    op_income = revenue * op_margin
    interest_cost = meta['assets'] * (self.macro['interest_rate'] / 100) * 0.01
    net_income = op_income - interest_cost

    # [수정 2] 실적 발표 효과 반영 (예측 대비 실제 결과)
    expected = meta['expected_earnings']
    actual_surprise = (net_income / max(1, abs(expected['expected_net_income'])))
    
    # 예측치보다 잘 나왔을 경우 추가 모멘텀 (어닝 서프라이즈)
    if net_income > expected['expected_net_income']:
        meta['momentum'] += 0.05
    else:
        meta['momentum'] -= 0.05

    # 4. 리스크 및 자산 업데이트
    if net_income < 0:
        meta['continuous_loss_count'] = meta.get('continuous_loss_count', 0) + 1
        protection = 0.2 if age_days < 1095 else 1.0
        sensitivity = meta.get('risk_sensitivity', 1.0)
        risk_up = (abs(net_income) / max(1, meta['assets'])) * 10 * sensitivity * protection
        meta['risk_score'] += risk_up
    else:
        meta['continuous_loss_count'] = 0
        recovery = (net_income / max(1, meta['assets'])) * 10
        meta['risk_score'] = max(0, meta['risk_score'] - recovery - 0.5)

    # 5. DB 기록
    self.earnings_history.setdefault(name, {}).setdefault(year, {})[quarter] = {
        "date": self.current_date.strftime("%m월 %d일"),
        "revenue": revenue, 
        "op_income": op_income,
        "net_income": net_income, 
        "is_surplus": net_income > 0,
        "surprise": "서프라이즈" if net_income > expected['expected_net_income'] else "쇼크"
    }
    
    # 자산에 실적 반영
    meta['assets'] += net_income
    
    return True

  # -- 실적 미리 게산 --
  def calculate_potential_earnings(self, s):
    """실적 발표 7일 전 수치를 미리 계산하는 함수"""
    import random
    meta = s['meta']
    tier = meta.get('tier', '소형주')
   
    # 매출 계산
    revenue = meta['assets'] * random.uniform(0.04, 0.10)
   
    # 비용 및 마진 계산 (대형/중형/소형 차등)
    base_cost = {"대형주": 0.015, "중형주": 0.025, "소형주": 0.04}.get(tier, 0.04)
    tier_bonus = {"대형주": 0.02, "중형주": 0.00, "소형주": -0.01}.get(tier, 0)
   
    op_margin = meta['efficiency'] - base_cost + tier_bonus
    op_income = revenue * op_margin
   
    # 금리 반영 순이익 계산
    interest_rate = self.macro.get('interest_rate', 4.0)
    interest_cost = meta['assets'] * (interest_rate / 100) * 0.01
    net_income = op_income - interest_cost
   
    # 서프라이즈 지수 계산
    expected_avg = revenue * 0.03
    surprise = net_income / expected_avg if expected_avg != 0 else 1.0

    return {
      "revenue": revenue,
      "net_income": net_income,
      "surprise": surprise,
      "is_surplus": net_income > 0
    }

  # [로직 3] 실적 조회 시스템 (사용자 명령어용)
  def show_earnings(self, company_name, target_year=None):
    """[v31.0] 실적 조회 시스템: 성장성(↑↓) 및 수익성 상태 표기 엔진"""
    if company_name not in self.earnings_history:
      print(f"⚠️ {company_name}의 공시 기록이 없습니다.")
      return
   
    # 특정 연도 요청 시
    if target_year:
      year_str = str(target_year)
      year_data = self.earnings_history[company_name].get(year_str)
      if not year_data:
        print(f"⚠️ {target_year}년도 실적 데이터가 없습니다.")
        return

      print(f"\n🔎 [실적 조회] {self.CYAN}{company_name}{self.RESET} - {target_year}년도 공시 내역")
      print("-" * 140)
      print(f" 분기 | 공시일 |{'매출액':^35}|{'영업이익':^30}|{'당기순이익':^30}")
      print("-" * 140)
     
      # 이전 분기 매출 비교를 위한 변수
      prev_revenue = None
     
      # 1~4분기 순회
      for q in ["1분기", "2분기", "3분기", "4분기"]:
        if q in year_data:
          d = year_data[q]
         
          # 1. 매출 성장세 판정 (전 분기 대비)
          rev_status = ""
          if prev_revenue is not None:
            if d['revenue'] > prev_revenue:
              rev_status = f"({self.RED}성장 ↑{self.RESET})"
            elif d['revenue'] < prev_revenue:
              rev_status = f"({self.BLUE}역성장 ↓{self.RESET})"
          prev_revenue = d['revenue']

          # 2. 이익 상태 판정
          op_status = f"({self.RED}흑자{self.RESET})" if d['op_income'] > 0 else f"({self.BLUE}적자{self.RESET})"
          net_status = f"({self.RED}흑자{self.RESET})" if d['net_income'] > 0 else f"({self.BLUE}적자{self.RESET})"
         
          # 컬러 설정
          net_color = self.RED if d['net_income'] > 0 else self.BLUE
         
          # 출력 (간격 조정)
          rev_str = f"{d['revenue']:>18,.0f}원"
          op_str = f"{d['op_income']:>18,.0f}원"
          net_str = f"{d['net_income']:>18,.0f}원"
         
          print(f" {q} | {d['date']} | {rev_str}{rev_status:<15} | "
             f"{op_str}{op_status:<12} | "
             f"{net_color}{net_str}{self.RESET}{net_status}")
      print("-" * 140)
     
    # 연도 미지정 시 (요약 모드)
    else:
      print(f"\n📜 [{company_name}] 연도별 실적 요약")
      print("-" * 80)
      for y in sorted(self.earnings_history[company_name].keys()):
        y_data = self.earnings_history[company_name][y]
        total_rev = sum(q['revenue'] for q in y_data.values())
        total_net = sum(q['net_income'] for q in y_data.values())
       
        net_color = self.RED if total_net > 0 else self.BLUE
        status = f"({self.RED}흑자 경영{self.RESET})" if total_net > 0 else f"({self.BLUE}적자 경영{self.RESET})"
       
        print(f" {y}년 | 매출: {total_rev:>22,.0f}원 | 순이익: {net_color}{total_net:>22,.0f}원{self.RESET} {status}")

  def update_company_technology(self):
    """[v186.0] 체급별 포트폴리오 차등화 + 산업 1위 보호막 엔진 및 테크 도약 분기점 연동"""
    current_lv = self.max_tech_reached
   
    # 각 산업군별 시가총액 1위 기업 찾기
    top_companies_by_ind = {}
    for ind in self.MAIN_INDUSTRIES:
      ind_stocks = [s for s in self.stocks if s['meta']['ind'] == ind]
      if ind_stocks:
        top_s = max(ind_stocks, key=lambda x: x['market_cap'])
        top_companies_by_ind[ind] = top_s['meta']['c_name']

    for s in self.stocks:
      meta = s['meta']
      ind = meta['ind']
      tier = meta['tier']
      is_group = meta['group_id'] is not None
     
      # ------------------------------------------------------------
      # [신규 연계: 테크 도약 분기점(D-30) 가중치 및 도약 효과 연동]
      # ------------------------------------------------------------
      # 현재 연도 및 기술 레벨 확인
      cy = self.current_date.year
     
      # 12월 1일 D-30 기술 도약 구간인 경우
      is_tech_jump_period = (self.current_date.month == 12) and (self.current_date.day == 1)
     
      if is_tech_jump_period:
        jump_premium = 1.0
        if getattr(self, 'has_paid_news_access', False):
          # 프리미엄 유료 뉴스 구독 시 산업군별 수혜 분석을 통한 추가 밸류에이션(15% 보정 효과)
          jump_premium = 1.15
       
        # 기술 레벨 도약 효과를 자산 및 가격에 반영
        meta['assets'] *= jump_premium
        s['price'] = int(s['price'] * jump_premium)
      # ------------------------------------------------------------

      max_subs = {"대형주": 3, "중형주": 2, "소형주": 1}.get(tier, 1)
      if is_group: max_subs = 3

      current_subs = [x.strip() for x in meta['sub'].split(',')]
     
      available_new_tech = self.INDUSTRY_LEVELS.get(ind, {}).get(current_lv, [])
      if available_new_tech and current_subs[0] not in available_new_tech:
        pivot_chance = {"대형주": 0.85, "중형주": 0.50, "소형주": 0.25}.get(tier, 0.25)
        if is_group: pivot_chance = 0.90
       
        if random.random() < pivot_chance:
          new_main = random.choice(available_new_tech)
          if new_main not in current_subs:
            current_subs.insert(0, new_main)
            current_subs = current_subs[:max_subs]
            meta['sub'] = ", ".join(current_subs)
            s['price'] = int(s['price'] * 1.08)
            meta['risk_score'] = max(0, meta['risk_score'] - 5)

      risk = meta.get('risk_score', 0)
      if (risk > 110 or meta.get('continuous_loss_count', 0) > 5) and len(current_subs) > 1:
        removed_sub = current_subs.pop()
        meta['sub'] = ", ".join(current_subs)
        s['price'] = int(s['price'] * 0.94)
        meta['risk_score'] = max(0, meta['risk_score'] - 25.0)
        if not self.silent_mode:
          self.daily_news.append(f"✂️ [구조조정] {self.YELLOW}{meta['c_name']}{self.RESET}이 경영난으로 {removed_sub} 사업을 정리했습니다.")

      t1_subs = self.INDUSTRY_LEVELS.get(ind, {}).get(1, [])
      if current_lv > 1 and current_subs[0] in t1_subs:
        if top_companies_by_ind.get(ind) != meta['c_name']:
          penalty = random.uniform(0.015, 0.035)
          s['price'] = int(s['price'] * (1 - penalty))
          meta['risk_score'] += 0.4
         
          if random.random() < 0.005:
            self.daily_news.append(f"🏚️ [산업도태] {self.YELLOW}{meta['c_name']}{self.RESET}이(가) 시대에 뒤처져 시장 점유율을 잃고 있습니다.")
           
  def check_delisting(self):
    """[v53.6] 딕셔너리 구조 완벽 대응 버전"""
    from datetime import datetime, timedelta
    import random

    MIN_STOCKS_LIMIT = 60
    if len(self.stocks) <= MIN_STOCKS_LIMIT: return

    delisted_this_turn = []
    is_depression = any("대공황" in str(val) for val in [self.current_scenario]) and "극복" not in self.current_scenario
    max_delist_this_turn = 30 if is_depression else 1
    new_reserved_count = 0

    candidates = sorted(self.stocks, key=lambda x: x['meta'].get('risk_score', 0), reverse=True)

    for s in candidates:
      meta = s['meta']
      name = meta['c_name']

      # --- [A. 이미 예약된 종목인가?] ---
      if name in self.pending_events["delist"]:
        info = self.pending_events["delist"][name]
       
        # [수정 핵심] 딕셔너리에서 'date' 키만 정확히 추출
        if isinstance(info, dict):
          target_date = info.get('date')
        else:
          target_date = info # 만약의 경우 대비
       
        # [중요] 아직 삭제일(target_date)이 되지 않았다면 그냥 통과(Continue)
        # 이래야 7일 동안 news.py에서 예고 뉴스를 띄울 시간을 법니다.
        if self.current_date < target_date:
          continue

        # 삭제일이 도래했을 때만 아래 로직 실행
        threshold = 100 if is_depression else 150
        is_risk_out = meta.get('risk_score', 0) >= threshold
       
        # 사유도 장부에서 가져오거나 새로 판정
        reason = info.get('reason') if isinstance(info, dict) else ("자본 잠식" if is_risk_out else "연속 적자")
       
        if not getattr(self, 'silent_mode', False):
          red_code, reset_code = getattr(self, 'RED', ''), getattr(self, 'RESET', '')
          self.daily_news.append(f"💀 {red_code}[상장폐지] {name}{reset_code} ({reason})")
       
        meta['delisted_date'] = self.current_date.strftime('%Y-%m-%d')
        delisted_this_turn.append(s)
        del self.pending_events["delist"][name]
        continue

      # --- [B. 신규 예약 대상 판정] ---
      # (이 부분은 사용자님이 작성하신 딕셔너리 저장 로직을 그대로 사용하되 중복만 제거하세요)
      ld = meta.get('listed_date_dt')
      if not ld or isinstance(ld, str):
        try: ld = datetime.strptime(meta['listed_date'], '%Y-%m-%d')
        except: ld = self.current_date
        meta['listed_date_dt'] = ld
     
      age_days = (self.current_date - ld).days
      threshold = 100 if is_depression else 150
      is_risk_out = meta.get('risk_score', 0) >= threshold
      is_zombie_out = (meta.get('continuous_loss_count', 0) >= 12) and (age_days >= 1825)
     
      if (is_risk_out or is_zombie_out) and not meta.get('is_doomed'):
        if new_reserved_count < max_delist_this_turn:
          if (len(self.stocks) - len(delisted_this_turn) - new_reserved_count) > MIN_STOCKS_LIMIT:
            delist_date = self.current_date + timedelta(days=7)
            reason = "🔥 경제 대공황 파산" if is_depression else ("자본 잠식" if is_risk_out else "연속 적자")
           
            # 딕셔너리 형태로 저장
            self.pending_events["delist"][name] = {
              "date": delist_date,
              "reason": reason
            }
            meta['is_doomed'] = True
            new_reserved_count += 1
            continue # 예약했으니 이번 턴 종료

    # --- [C. 실제 리스트에서 제거] ---
    for ds in delisted_this_turn:
      if ds in self.stocks:
        ds['meta']['delisted_date'] = self.current_date.strftime('%Y-%m-%d')
        ds['meta']['is_officially_delisted'] = True
        self.delisted_stocks.append(ds)
        self.stocks.remove(ds)

  def update_macro_logic(self):
    """매크로 지표 연산 및 대공황 V자 반등(D-30) 시그널 연동"""
    scenario = self.current_scenario
    lv = self.get_tech_level()
   
    progress = 0.0
    MAX_RATE_CHANGE = 0.05 if lv < 3 else 0.1
    MAX_FX_CHANGE = 5.0
   
    target_cpi = {1: 2.0, 2: 2.5, 3: 4.0, 4: 1.0}.get(lv, 2.0)
    target_interest = target_cpi + 1.5
    target_oil = {1: 45, 2: 90, 3: 140, 4: 25}.get(lv, 50)
    target_fx = {1: 1150, 2: 1250, 3: 1350, 4: 950}.get(lv, 1150)

    if "💀 대공황" in scenario or "✨ 대공황V" in scenario:
      total_days = 252 * 10
      elapsed_days = total_days - self.scenario_timer
      progress = max(0.0, min(1.0, elapsed_days / total_days))
     
      target_cpi = 2.0 + (23.0 * progress)
      target_interest = 4.0 + (31.0 * progress)
      target_oil = target_oil + (150 * progress)
      target_fx = target_fx + (700 * progress)

      # ------------------------------------------------------------
      # [신규 연계: 대공황 V자 반등 시그널(D-30) 가중치 연동]
      # ------------------------------------------------------------
      if self.scenario_timer <= 30:
        # 유료 뉴스 구매 시 위기 극복 및 회복 기대 심리를 더욱 강하게 매크로에 반영
        recovery_premium = 0.85 if getattr(self, 'has_paid_news_access', False) else 0.95
        target_interest *= recovery_premium
        target_cpi *= recovery_premium
      # ------------------------------------------------------------

      if "대공황V" in scenario:
        target_interest *= 0.8
        target_cpi *= 0.9

    elif "극복" in scenario:
      target_cpi = 8.2
      target_interest = 9.5
      target_oil = 155.0
      target_fx = 1450.0
     
    elif "🚀 T4 발전" in scenario:
      target_cpi = 0.5
      target_interest = 1.0
      target_oil = 15.0
      target_fx = 900.0

    cpi_step = (target_cpi - self.macro["cpi"]) * 0.02 + random.uniform(-0.05, 0.05)
    v_factor = 5.0 if (("대공황" in scenario) and progress > 0.5) else 1.0
    self.macro["cpi"] = max(0.5, min(45.0, self.macro["cpi"] + cpi_step * v_factor))

    if self.macro["cpi"] > target_cpi: target_interest += 1.0
   
    diff_r = (target_interest - self.macro["interest_rate"]) * 0.03 + random.uniform(-0.02, 0.02)
    self.macro["interest_rate"] += max(-MAX_RATE_CHANGE, min(MAX_RATE_CHANGE, diff_r))
   
    r_max = 40.0 if "대공황" in scenario else 15.0
    self.macro["interest_rate"] = max(0.25, min(r_max, self.macro["interest_rate"]))

    oil_drift = (target_oil - self.macro["oil_price"]) * 0.01
    self.macro["oil_price"] = max(5, self.macro["oil_price"] + oil_drift + random.uniform(-1.5, 1.5))

    rate_impact = (self.macro["interest_rate"] - 3.5) * -15
    fear_impact = (progress * 300) if "대공황" in scenario else 0
    final_target_fx = target_fx + rate_impact + fear_impact
   
    diff_fx = (final_target_fx - self.macro["exchange_rate"]) * 0.02 + random.uniform(-10, 10)
    self.macro["exchange_rate"] += max(-MAX_FX_CHANGE, min(MAX_FX_CHANGE, diff_fx))
    self.macro["exchange_rate"] = max(800, min(2500, self.macro["exchange_rate"]))

    self.cumulative_inflation *= (1 + (self.macro["cpi"] / 100) / 252)
    self.base_item_price = 1000.0 * self.cumulative_inflation
 
  def get_dynamic_target(self):
    """고정 로드맵 없이 현재 시나리오와 테크 레벨로만 목표치 계산"""
    # 1. 테크 레벨에 따른 기본 연간 기대 성장률 (Normal 기준)
    # LV1: 8%, LV2: 12%, LV3: 15%, LV4: 20%
    base_growth_rates = {1: 0.08, 2: 0.12, 3: 0.1, 4: 0.15}
    annual_rate = base_growth_rates.get(self.max_tech_reached, 0.08)

    # 2. 시나리오에 따른 성장률 변형 (강제성 제거)
    if "💀 대공황" in self.current_scenario:
      # 대공황 시 목표는 현재가보다 훨씬 낮게 (매일 -3~5% 하락 유도)
      return self.gri * 0.96
    elif "🚀 T4 발전" in self.current_scenario:
      # 테크 4 폭주 시 목표는 현재가보다 훨씬 높게 (매일 +5~7% 상승 유도)
      return self.gri * 1.07
    elif "🟢 T3 유지" in self.current_scenario:
      # 저성장 정체 시 성장률 반토막
      annual_rate *= 0.5
   
    # 3. 정상 상태일 때: 현재 지수에서 '하루치' 기대 성장만큼만 목표로 설정
    # 복리가 폭발하지 않도록 연율을 일일율로 변환하여 적용
    daily_rate = annual_rate / 252
    return self.gri * (1 + daily_rate)
 
  def apply_price_change(self):
    interest_rate = self.macro["interest_rate"]
    total_market_cap = 0
    cy = self.current_date.year

    # 지수 저항선 및 기본 변수 설정
    resistance = 1.0
    if self.gri > 50000:
      resistance = 1.0 / (1.0 + math.log10(self.gri / 50000) * 1.5)
   
    is_normal_depression = "대공황" in self.current_scenario and "V" not in self.current_scenario and "극복" not in self.current_scenario
   
    daily_target = 0.0003
    is_protected = False
    cpi_impact = self.macro["cpi"] / 100.0

    if is_normal_depression:
      is_protected = self.scenario_timer > -252
      if is_protected:
        daily_target = -0.008
      else:
        daily_target = -0.025 - (cpi_impact * 0.5)
        if self.gri < 700: daily_target *= 0.3
    elif "극복" in self.current_scenario:
      daily_target = 0.018 + (0.01 / max(1, cpi_impact))
    elif "대공황" in self.current_scenario:
      daily_target = -0.015 - (cpi_impact * 0.2)

    panic_factor = 1.0
    if self.gri < 7000: panic_factor = 0.93
    elif self.gri < 12000: panic_factor = 0.97

    # 매크로 공포 지수 가중치
    fear_index = self.macro.get("fear_index", 10.0)
    fear_multiplier = 1.0
    if fear_index >= 50.0 and "대공황" in self.current_scenario:
      fear_multiplier = 1.8 if getattr(self, 'has_paid_news_access', False) else 1.1

    # 개별 종목 연산 루프
    for s in self.stocks:
      meta = s['meta']
      name = meta['c_name']
      old_price = float(s['price'])
     
      # ============================================================
      # [수렴 엔진(Convergence Engine): 정보 비대칭 선반영 로직]
      # ============================================================
     
      # 1. 상장폐지 선반영 (D-7) - 명세서 3번
      if name in self.pending_events.get("delist", {}):
        p_date = self.pending_events["delist"][name]
        if isinstance(p_date, str): p_date = datetime.strptime(p_date, "%Y-%m-%d")
        days_left = (p_date.date() - self.current_date.date()).days
        if 0 < days_left <= 7:
          # 망하기 전까지 매일 강제 폭락 유도 (목표가 0원 수렴)
          s['price'] = int(s['price'] * random.uniform(0.80, 0.86))
          meta['momentum'] -= 0.25

      # 2. 테크 도약 선반영 (D-30) - 명세서 12~14번
      if self.pending_events.get("tech_jump"):
        jump_info = self.pending_events["tech_jump"]
        p_date = jump_info['date']
       
        # 날짜 객체 변환 및 안전 처리
        if isinstance(p_date, str):
          p_date = datetime.strptime(p_date, "%Y-%m-%d")
       
        # 현재 날짜와 예약 날짜의 차이 계산
        # (둘 다 .date()로 맞춰야 시/분/초 차이로 인한 에러가 없습니다)
        days_left = (p_date.date() - self.current_date.date()).days
       
        # 30일 전부터 IT/커뮤니케이션 종목에 모멘텀 주입
        if 0 < days_left <= 30 and meta['ind'] in ["IT", "커뮤니케이션"]:
          # D-30에는 0.008, D-1에는 0.016에 가깝게 모멘텀이 점진적으로 강해짐
          convergence_factor = (30 - days_left) / 30
          meta['momentum'] += 0.008 * (1 + convergence_factor)

      # 3. 대공황 V반등 선반영 (D-30) - 명세서 11번
      if self.pending_events.get("v_rebound"):
        p_date = self.pending_events["v_rebound"]
        if isinstance(p_date, str): p_date = datetime.strptime(p_date, "%Y-%m-%d")
        days_left = (p_date.date() - self.current_date.date()).days
        if 0 < days_left <= 30:
          # 바닥 통과 전 저가 매수세 유입 (회복 모멘텀)
          daily_recovery = 0.012 * (1 + (30 - days_left) / 15)
          meta['momentum'] += daily_recovery

      # ============================================================
      # [기존 변동성 및 리스크 연산]
      # ============================================================
      risk = meta.get('risk_score', 0)
      tier = meta['tier']
      loss_count = meta.get('continuous_loss_count', 0)
      loss_penalty = -(loss_count * 0.02) if loss_count > 0 else 0.0

      # 실적 발표 전 구간별 변동성 증폭 (명세서 1번/9번 연동)
      current_month = self.current_date.month
      cur_day = self.current_date.day
      report_day = meta.get('report_day', 15)
      is_pre_announcement = (current_month in [3, 6, 9, 12]) and (report_day - cur_day <= 7) and (report_day - cur_day > 0)
     
      vol_multiplier = 1.0
      if is_pre_announcement:
        vol_multiplier = 1.6 if getattr(self, 'has_paid_news_access', False) else 1.15

      # 체급별 기본 변동성 설정
      if "대형주" in tier:
        vol = 0.012 * vol_multiplier; decay = 0.85; growth_multiplier = 1.35 * resistance
      elif "중형주" in tier:
        vol = 0.045 * vol_multiplier; decay = 0.6; growth_multiplier = 1.45 * resistance
      else:
        vol = 0.180 * vol_multiplier; decay = 0.2; growth_multiplier = 1.8 * resistance

      denom = 400 if is_protected else 200
      risk_pressure = -((risk - 50) / denom) if risk > 50 else 0.0

      # 모멘텀 및 최종 등락률(perf) 계산
      meta['momentum'] = (meta.get('momentum', 0.0) * decay) + random.uniform(-vol, vol) + risk_pressure + loss_penalty
     
      risk_penalty = (risk / 1000)
      adj_efficiency = meta['efficiency'] * growth_multiplier
     
      int_impact = 0.002 if is_protected else 0.01
      # perf는 일일 수익률
      perf = (adj_efficiency + daily_target + meta['momentum'] - (interest_rate * int_impact) - risk_penalty) / 252
     
      # 매크로 섹터 민감도 및 외인/기관 충격 반영 (명세서 7번 연동)
      perf = self.apply_macro_sector_sensitivity(s, perf)
      perf = self.apply_foreign_inst_shock(s, perf)
     
      # 자산가치 업데이트 및 목표 주가 산출
      meta['assets'] *= (1 + perf)
      safe_assets = max(10000.0, meta['assets'])
      target_price = int(safe_assets / max(100, s['shares']))
     
      risk_panic = max(0.5, 1.0 - (risk / 200))
      raw_price = max(10, int(target_price * random.uniform(0.98, 1.02) * panic_factor * risk_panic * fear_multiplier))
     
      # 상하한가 제한 (전일 대비 30%)
      max_up = int(old_price * 1.3)
      max_down = int(old_price * 0.7)
      s['price'] = max(max_down, min(max_up, raw_price))
     
      # 등락률 및 시총 갱신
      s['rate'] = round(((s['price'] / old_price) - 1) * 100, 2) if old_price > 0 else 0.0
      s['market_cap'] = s['price'] * s['shares']
      total_market_cap += s['market_cap']
     
      # 생존 전략(자사주/증자) 핸들링
      self.handle_survival_strategy(s)

    # 시장 지수(GRI) 갱신 로직
    if getattr(self, 'initial_market_total_cap', 0) <= 0:
      self.initial_market_total_cap = total_market_cap if total_market_cap > 0 else 1.0
      raw_gri = 1000.0
    else:
      raw_gri = (total_market_cap / self.initial_market_total_cap) * 1000.0
   
    weight = 0.005
    if is_normal_depression:
      if raw_gri < 1500:
        weight = 0.02
        raw_gri = max(800, raw_gri)
      else:
        weight = 0.12
    elif "극복" in self.current_scenario:
      weight = 0.1
   
    self.gri = self.gri * (1 - weight) + raw_gri * weight
   
    return total_market_cap

  def apply_macro_sector_sensitivity(self, s, perf):
    """거시경제 지표 민감도 및 통화정책 회의 기대 심리(D-7) 연동"""
    meta = s['meta']
    sector = self.SECTOR_MAP.get(meta['ind'], "Value")
   
    ex_rate = self.macro["exchange_rate"]
    oil_price = self.macro["oil_price"]
    interest_rate = self.macro["interest_rate"]
   
    # 1. 환율 민감도
    fx_diff = (ex_rate - 1100.0) / 100.0
    if sector in ["IT", "산업재", "커뮤니케이션"]:
      perf += fx_diff * 0.0012
    elif sector in ["필수소비재", "유틸리티"]:
      perf -= fx_diff * 0.001
     
    # 2. 유가 민감도
    oil_diff = (oil_price - 30.0) / 50.0
    if sector == "에너지":
      perf += oil_diff * 0.0015
    elif sector in ["산업재", "유틸리티", "필수소비재"]:
      perf -= oil_diff * 0.001
     
    # 3. 금리 민감도 및 통화정책 연동
    if sector == "금융":
      interest_diff = (interest_rate - 4.0) / 5.0
      perf += interest_diff * 0.0008

    # ------------------------------------------------------------
    # [신규 연계: 통화정책 및 금리 인하/인상 기대 심리(D-7) 연동]
    # ------------------------------------------------------------
    is_interest_sensitive = (interest_rate >= 8.0) or (interest_rate <= 2.0)
   
    rate_multiplier = 1.0
    if is_interest_sensitive:
      # 유료 뉴스 구독 시 금리 변동에 대한 방향성을 더욱 명확하게 반영 (프리미엄 1.5배, 일반 1.0배)
      rate_multiplier = 1.5 if getattr(self, 'has_paid_news_access', False) else 1.05
     
    perf = perf * rate_multiplier
    # ------------------------------------------------------------
   
    return perf

  def apply_foreign_inst_shock(self, s, perf):
    """기관 및 외국인 지분 기반 수급 충격 반영 및 신규 상장(IPO) 수급 이동(D-7) 연동"""
    meta = s['meta']
    risk_score = meta.get('risk_score', 0.0)
    total_inst_share = meta.get('foreign_share', 0.0) + meta.get('inst_share', 0.0)
   
    # ------------------------------------------------------------
    # [신규 연계: 신규 상장(IPO) 수급 이동(D-7) 가중치 연동]
    # ------------------------------------------------------------
    current_month = self.current_date.month
    cur_day = self.current_date.day
   
    # 2월, 5월, 8월, 11월 21일 전후 (7일간) 수급 이동 기간 설정
    is_ipo_period = (cur_day >= 14 and cur_day <= 21) and (current_month in [2, 5, 8, 11])
   
    ipo_multiplier = 1.0
    if is_ipo_period and meta['tier'] == "소형주":
      # 대형주 상장에 따른 중소형주 수급 분산 충격 (프리미엄 구독 시 2.0배, 미구독 시 1.2배 적용)
      ipo_multiplier = 2.0 if getattr(self, 'has_paid_news_access', False) else 1.2
    # ------------------------------------------------------------
   
    if risk_score > 60.0:
      shock_factor = -random.uniform(0.005, 0.025) * min(2.0, total_inst_share * 3)
    else:
      shock_factor = random.uniform(-0.005, 0.005) * total_inst_share
     
    return perf + (shock_factor * ipo_multiplier)
 
  def apply_stock_event(self, s, silent=False):
    """[v65.1 수정본] 자사주 + AI분할 + 실적기반 누적리스크 엔진 (지분율 동적 분배 로직 적용)"""
    meta = s['meta']
    price = s['price']
    old_shares = s['shares']
    sector = self.SECTOR_MAP.get(meta['ind'], "Value")
    current_stocks_count = len(self.stocks)
   
    # --- [PART 1. 자사주 엔진 수정] ---
    # 1. 자사주 매입 로직 (개인 및 일반 지분에서 흡수)
    if meta.get('momentum', 0) < -0.05 and (s['market_cap'] < meta['assets'] * 0.7) and meta['risk_score'] < 1.0:
      buy_ratio = random.uniform(0.01, 0.03)
      meta['treasury_share'] += buy_ratio
      meta['momentum'] += 0.05
     
      inst_absorb_ratio = random.uniform(0.1, 0.35) # 기관/외국인이 흡수하는 비율
      retail_absorb_ratio = 1.0 - inst_absorb_ratio # 나머지는 개인 물량에서 흡수
     
      meta['inst_share'] = max(0.0, meta.get('inst_share', 0.0) - (buy_ratio * inst_absorb_ratio))
      meta['retail_share'] = max(0.0, meta.get('retail_share', 0.0) - (buy_ratio * retail_absorb_ratio))
     
      s['price'] = int(s['price'] * 1.02)
     
      if not silent:
        self.daily_news.append(f"📢 [자사주매입] {meta['c_name']} 주가 방어 및 지분 흡수")

    # 2. 자사주 매도 로직
    elif (s['market_cap'] > meta['assets'] * 2.0) and meta.get('treasury_share', 0) > 0.05:
      sell_ratio = random.uniform(0.02, 0.05)
      meta['treasury_share'] -= sell_ratio
      meta['momentum'] -= 0.04
     
      cash_in = (s['price'] * (old_shares * sell_ratio))
      meta['assets'] += cash_in
     
      tier = meta.get('tier', '소형주')
      if tier == "대형주":
        foreign_weight = random.uniform(0.4, 0.6)
        inst_weight = random.uniform(0.2, 0.4)
        retail_weight = max(0.0, 1.0 - (foreign_weight + inst_weight))
      elif tier == "중형주":
        foreign_weight = random.uniform(0.1, 0.25)
        inst_weight = random.uniform(0.3, 0.5)
        retail_weight = max(0.0, 1.0 - (foreign_weight + inst_weight))
      else: # 소형주
        foreign_weight = random.uniform(0.0, 0.05)
        inst_weight = random.uniform(0.1, 0.2)
        retail_weight = max(0.0, 1.0 - (foreign_weight + inst_weight))
       
      meta['foreign_share'] = meta.get('foreign_share', 0.0) + (sell_ratio * foreign_weight)
      meta['inst_share'] = meta.get('inst_share', 0.0) + (sell_ratio * inst_weight)
      meta['retail_share'] = meta.get('retail_share', 0.0) + (sell_ratio * retail_weight)
     
      total_shares_sum = (
        meta['treasury_share'] +
        meta['owner_share'] +
        meta['foreign_share'] +
        meta['inst_share'] +
        meta['retail_share']
      )
     
      if total_shares_sum > 1.0:
        excess = total_shares_sum - 1.0
        if meta['retail_share'] > 0:
          meta['retail_share'] = max(0.0, meta['retail_share'] - excess)
        else:
          meta['inst_share'] = max(0.0, meta['inst_share'] - excess)

      is_surplus = meta.get('continuous_loss_count', 0) == 0
      low_risk = meta.get('risk_score', 0) < 1.5
     
      if is_surplus and low_risk:
        s['price'] = int(s['price'] * 1.03)
        if not silent:
          self.daily_news.append(f"🟢 [자사주처분] {meta['c_name']} 우수 실적 기반 자금 확보")
      else:
        s['price'] = int(s['price'] * 0.94)
        if not silent:
          self.daily_news.append(f"🔴 [자사주처분] {meta['c_name']} 단순 현금화로 인한 수급 부담")
   
    self.handle_stock_split(s, silent)

    # --- [PART 3. 실적 기반 누적 리스크 관리] ---
    is_resistant = "대형주" in meta['tier'] or meta['group_id'] is not None
    sensitivity = 1.0
   
    # 대공황 및 섹터 민감도
    if "대공황" in self.current_scenario:
      sensitivity = 1.6 if sector == "Growth" else 0.5
    if is_resistant: sensitivity *= 0.3
   
    # [수정] 평생 적자 내는 놈은 리스크가 누적되어 탈출 불가능하게 설계
    loss_count = meta.get('continuous_loss_count', 0)
    risk_inc = -0.01 # 기본 회복치
   
    if loss_count > 0:
      # 적자가 길어질수록 리스크 상승폭이 가속됨 (좀비 기업 처단)
      risk_inc = 0.02 * loss_count * sensitivity
   
    if self.macro["interest_rate"] > 15.0: risk_inc += 0.05
    if price < 1000: risk_inc += 0.05 # 동전주는 생존 압박
   
    # 마지노선 방어 (60개 미만일 땐 리스크 상승 억제)
    if current_stocks_count < 60: risk_inc = min(risk_inc, -0.05)
   
    meta['risk_score'] = max(0, meta['risk_score'] + risk_inc)

    # --- [PART 4. 최종 폐지 프로세스] (기존 유지) ---
    if meta['risk_score'] >= 2.5 and meta['delist_timer'] == 0:
      # [수정] 주가가 일정 수준 이상이면 폐지 예고를 하지 않고 일단 버팀
      if current_stocks_count > 60 and s['price'] < 10000: # 1만원 이하일 때만 폐지 절차 진입
        meta['delist_timer'] = 20 if is_resistant else 10
        if not silent: self.daily_news.append(f"🚨 [상장폐지예고] {meta['c_name']} 퇴출 카운트다운")
      else:
        # 주가가 높으면 리스크 점수를 깎으며 버팀 (자본력으로 버티는 설정)
        meta['risk_score'] = max(0, meta['risk_score'] - 0.5)
        meta['momentum'] -= 0.1 # 대신 주가 하락 압력은 강하게 줌

    if meta['delist_timer'] > 0:
      timer_speed = 5 if "대공황" in self.current_scenario else 1
      meta['delist_timer'] -= timer_speed
     
      if meta['delist_timer'] <= 0:
        # 폐지 조건 검사 후 삭제 처리 (기존 로직 유지)
        if s['price'] < 5000 or "대공황" in self.current_scenario:
          if ("대공황" in self.current_scenario) or (self.daily_delist_count < 2):
            if len(self.stocks) > 60:
              meta['delisted_date'] = self.current_date.strftime('%Y-%m-%d')
              self.delisted_stocks.append(s)
              if s in self.stocks: self.stocks.remove(s)
              self.daily_delist_count += 1
              if not silent: self.daily_news.append(f"💀 [퇴출완료] {meta['c_name']} 상장 폐지")
        else:
          # 카운트다운이 끝났는데 주가가 기준치 이상으로 회복된 경우에만 회생 뉴스 출력
          meta['delist_timer'] = 0
          meta['risk_score'] = 1.0
          if not silent:
            self.daily_news.append(f"😇 [회생성공] {meta['c_name']}이 주가 회복으로 상장 유지에 성공했습니다.")
           
    # 상태 텍스트 갱신
    if meta.get('delist_timer', 0) > 0: meta['char'] = f"EXIT-{meta['delist_timer']}"
    elif meta['risk_score'] >= 1.2: meta['char'] = "WARNING"
    else: meta['char'] = "Normal"

  def handle_stock_split(self, s, silent=False):
    meta = s['meta']
    price = s['price']
    shares = s['shares']
    tier = meta['tier']
    sector = self.SECTOR_MAP.get(meta['ind'], "Value")
   
    # --- [신규: 황제주 고집 필터] ---
    # will_to_split이 False인 기업(황제주 성향)은 아래 분할 로직을 전부 무시하고 통과합니다.
    if not meta.get('will_to_split', True):
      # 단, 주가가 1,000만 원(초고가 마지노선)을 넘을 때만 아주 낮은 확률로 분할 검토
      if price < 10000000:
        return
      else:
        if random.random() > 0.01: return

    # --- [추가 핵심] UI 전달용 딕셔너리 초기화 ---
    if not hasattr(self, 'daily_splits'):
      self.daily_splits = {}

    split_ratio = 0
   
    # --- [A. 유동성 공급형 분할 로직] ---
    if "중형주" in tier or "대형주" in tier:
      if price >= 150000:
        if shares < 100_000_000:
          split_ratio = 10
        elif shares < 500_000_000:
          split_ratio = 5
        else:
          split_ratio = 2

    # --- [B. 기존 마지노선 기반 강제 분할 로직] ---
    if split_ratio == 0:
      hard_limit = 10000000 if sector == "Value" else 5000000
      if price >= hard_limit:
        split_ratio = 10 if price < hard_limit * 5 else 50
      elif price >= (hard_limit * 0.2) and shares < 50000000:
        if random.random() < 0.2:
          split_ratio = 5

    # --- [분할 실행] ---
    if split_ratio > 0:
      old_name = meta['c_name']
      s['price'] //= split_ratio
      s['shares'] *= split_ratio
      meta['split_count'] = meta.get('split_count', 0) + 1
     
      # [추가] UI 동기화용 기록 및 과거 주가 DB 수정
      self.daily_splits[old_name] = float(split_ratio)
      self.update_db_adjusted_price(old_name, 1 / split_ratio)
     
      if not silent:
        self.daily_news.append(f"✂️ [액면분할] {meta['c_name']}이 주가 부담 완화 및 유동성 확대를 위해 {split_ratio}:1 분할을 실시합니다.")
        self.daily_news.append(f" └ 현재가: {s['price']:,}원 | 발행주식수: {s['shares'] / 100000000:.1f}억 주")

    # --- [C. 액면병합 로직 (동전주 구제)] ---
    elif price < 1000:
      if random.random() < 0.8:
        ratio = 10
        old_name = meta['c_name']
        s['price'] *= ratio
        s['shares'] //= ratio
        meta['merge_count'] = meta.get('merge_count', 0) + 1
        meta['risk_score'] = max(0, meta['risk_score'] - 0.5)
       
        # [추가] UI 동기화용 기록 및 과거 주가 DB 수정
        self.daily_splits[old_name] = 1 / ratio
        self.update_db_adjusted_price(old_name, float(ratio))
       
        if not silent:
          self.daily_news.append(f"🧩 [AI병합] {self.YELLOW}{meta['c_name']}{self.RESET}이 상장 유지를 위해 1:{ratio} 병합을 단행했습니다.")

  # [신규 함수 추가] 과거 주가 데이터를 비율에 맞춰 일괄 수정 (그래프 보정)
  def update_db_adjusted_price(self, company_name, ratio):
    """환율, 물가 등 외부 변수의 영향을 받지 않고 오직 비율(ratio)에 의해서만 과거 주가를 수정"""
    try:
      cur = self.conn.cursor()
     
      # 비율(ratio)을 그대로 곱해서 정수형으로 변환
      cur.execute("""
        UPDATE stock_history
        SET price = CAST(price * ? AS INTEGER)
        WHERE company_name = ?
      """, (ratio, company_name))
      self.conn.commit()
    except Exception as e:
      print(f"❌ DB 수정 주가 반영 실패: {e}")
     
  def handle_survival_strategy(self, s):
    """[v110.0] 섹터별 위기 대응 차별화: 자사주 매각 vs 유상증자"""
    meta = s['meta']
    risk = meta.get('risk_score', 0)
    sector = self.SECTOR_MAP.get(meta['ind'], "Value")
   
    # [단계 1] 리스크가 위험 수준(80점 이상)일 때 자구책 실행
    if risk >= 80:
      # 1. 그룹사가 있는 경우: 그룹 내 자금 수혈 (최우선 생존)
      if meta.get('group_id'):
        meta['risk_score'] -= 5.0
        if not self.silent_mode:
          self.daily_news.append(f"🛡️ [그룹지원] {meta['c_name']}가 그룹사의 자금 지원으로 위기를 넘깁니다.")
     
      # 2. 독립 기업인 경우: 섹터별 자구책 실행
      else:
        # [A] 가치주(Value) 및 방어주(Defensive): 보유한 자사주를 시장에 팔아 현금 확보
        if sector in ["Value", "Defensive"] and meta.get('treasury_share', 0) > 0.02:
          sell_ratio = 0.02 # 2%씩 처분
          # 실제 처분 주식 수 계산
          sell_shares_count = int(s['shares'] * sell_ratio)
          cash_in = s['price'] * sell_shares_count
         
          meta['treasury_share'] -= sell_ratio
          meta['assets'] += cash_in
          meta['risk_score'] -= 10.0 # 현금 확보로 리스크 큰 폭 완화
         
          # 자사주 매각은 시장에 물량이 풀리는 것이므로 주가에 소폭 하락 압력
          s['price'] = int(s['price'] * 0.97)
         
          if not self.silent_mode:
            self.daily_news.append(f"💸 [위기처분] {meta['c_name']}가 자사주를 매각하여 운영 자금을 확보했습니다.")

        # [B] 성장주(Growth) 및 테마(Theme) 또는 자사주가 없는 경우: 유상증자(신주 발행)
        else:
          new_shares = int(s['shares'] * 0.15) # 15% 추가 발행
          capital_raised = new_shares * (s['price'] * 0.8) # 20% 할인 발행
         
          s['shares'] += new_shares
          meta['assets'] += capital_raised
          meta['risk_score'] -= 10.0 # 자산 유입으로 리스크 감소
         
          # 주주 가치 희석으로 인한 강력한 주가 하락 반영
          s['price'] = int(s['price'] * 0.85)
         
          if not self.silent_mode:
            self.daily_news.append(f"💉 [유상증자] {meta['c_name']}가 생존을 위해 증자를 단행했습니다. (가치 희석)")
         
  def display_groups(self):
    """[UI] 글로벌 그룹사 경영 현황 (이름 + 세부산업 + 시총 다단 출력)"""
    print(f"\n🏢 {self.CYAN}[글로벌 그룹사 경영 현황]{self.RESET}")
    print("=" * 165)
   
    group_list = []
    for gid, ginfo in self.groups.items():
      members = [s for s in self.stocks if s['meta']['group_id'] == gid]
      if members:
        members.sort(key=lambda x: x['market_cap'], reverse=True)
        total_cap = sum(x['market_cap'] for x in members)
        group_list.append((ginfo['name'], len(members), total_cap, members))
   
    group_list.sort(key=lambda x: x[2], reverse=True)
   
    for gname, count, tcap, members in group_list:
      # 그룹 상단 정보 (경 단위 시총 대응을 위해 간격 유지)
      print(f" ▶ {self.CYAN}{self.pad_text(gname, 12)}{self.RESET} | 계열사: {count:>2}개 | 그룹 시총합계: {tcap:>35,.0f}원")
      print(f" └ 계열사 목록:")
     
      # 한 줄에 4개씩 출력 (정보량이 늘어났으므로 간격 조절)
      cols = 4
      for i in range(0, len(members), cols):
        chunk = members[i:i + cols]
        row_items = []
        for s in chunk:
          # [요청 반영] 이름(세부산업): 시총 형태
          meta = s['meta']
          m_info = f"{meta['c_name']}({meta['sub']}): {s['market_cap']:,.0f}원"
         
          # 정보량이 많아졌으므로 칸 너비를 40으로 확장
          row_items.append(self.pad_text(m_info, 40))
       
        print(f"   {' '.join(row_items)}")
     
      print("-" * 165)
     
  def next_day(self, silent=False):
    import math
    import random
    from datetime import timedelta

    # 1. [날짜 및 시간 업데이트]
    self.current_date += timedelta(days=1)
    self.virtual_weekday = (self.virtual_weekday + 1) % 7
    self.is_market_open = self.virtual_weekday < 5
    
    curr_date_obj = self.current_date.date()
    current_month = self.current_date.month
    cur_day = self.current_date.day
    current_year_str = str(self.current_date.year)

    # 2. [기본 상태 초기화]
    self.daily_news = []
    self.daily_delist_count = 0
    self.silent_mode = silent
    lv = self.get_tech_level()
    
    if self.scenario_timer > 0:
        self.scenario_timer -= 1

    # --- [장이 열린 날에만 경제 연산 수행] ---
    if self.is_market_open:
        # 3. [실적 시스템: 예약 및 데이터 생성] - 뉴스 창에서 읽어갈 '재료'를 먼저 만듭니다.
        for s in self.stocks:
            meta = s['meta']
            
            # [A] 분기별 실적 발표일 예약 (2, 5, 8, 11월)
            if current_month in [2, 5, 8, 11] and cur_day == 1:
                meta['report_day'] = random.randint(1, 28)
                meta['expected_earnings'] = None # 새 시즌 시작 시에만 초기화
            
            if 'report_day' not in meta:
                meta['report_day'] = random.randint(1, 28)

            # [B] 실적 시즌(3, 6, 9, 12월) 데이터 주입
            if current_month in [3, 6, 9, 12]:
                try:
                    # 이번 달 실적 발표 예정일 객체 생성
                    report_date = self.current_date.replace(day=meta['report_day']).date()
                    d_7_date = report_date - timedelta(days=7)

                    # 오늘이 D-7 구간 이후라면 데이터가 없을 때 즉시 생성 (뉴스 노출용)
                    if curr_date_obj >= d_7_date:
                        if not meta.get('expected_earnings'):
                            meta['expected_earnings'] = self.calculate_potential_earnings(s)
                            
                            # 선반영 모멘텀 주입
                            surprise = meta['expected_earnings'].get('surprise', 1.0)
                            meta['momentum'] += max(-0.15, min(0.12, (surprise - 1.0) * 0.2))
                            
                            if not silent:
                                print(f"DEBUG: {meta['c_name']} 실적 데이터 긴급 복구 (발표일: {meta['report_day']}일)")
                except ValueError:
                    meta['report_day'] = 28

        # 4. [실적 시스템: 실제 실적 발표]
        report_target_months = [3, 6, 9, 12, 1, 4, 7, 10]
        if current_month in report_target_months:
            q_map = {3: "1분기", 4: "1분기", 6: "2분기", 7: "2분기", 9: "3분기", 10: "3분기", 12: "4분기", 1: "4분기"}
            target_q = q_map.get(current_month, "분기")
            
            for s in self.stocks:
                meta = s['meta']
                history = self.earnings_history.setdefault(meta['c_name'], {}).setdefault(current_year_str, {})
                
                if target_q not in history:
                    is_report_month = current_month in [3, 6, 9, 12]
                    report_day = meta.get('report_day', 15)
                    
                    if (is_report_month and cur_day >= report_day) or (not is_report_month and cur_day <= 5):
                        # 발표 시점에 데이터가 없으면 뉴스 창 에러 방지를 위해 즉시 생성
                        if not meta.get('expected_earnings'):
                            meta['expected_earnings'] = self.calculate_potential_earnings(s)
                        
                        # 실제 실적 확정 및 자산 반영
                        self.announce_earnings(s)
                        if not silent:
                            self.daily_news.append(f"📊 [실적공시] {self.CYAN}{meta['c_name']}{self.RESET} {target_q} 발표")
                        
                        # [주의] 여기서 meta['expected_earnings'] = None을 바로 실행하지 않습니다.
                        # 뉴스 창이 이 데이터를 읽어갈 수 있도록 다음 분기 예약 시점(2,5,8,11월)에 지웁니다.

        # 5. [기타 경제 엔진 가동]
        self.handle_group_expansion(silent)
        self.update_macro_logic()
        self.apply_price_change()
        self.update_company_technology()

        # 6. [데이터 업데이트 및 DB 저장]
        date_str = self.current_date.strftime('%Y-%m-%d')
        db_records = []
        for s in self.stocks:
            self.apply_stock_event(s, silent)
            db_records.append((date_str, s['meta']['c_name'], int(s['price']), int(s['market_cap'])))

        try:
            cur = self.conn.cursor()
            cur.executemany("INSERT INTO stock_history VALUES (?, ?, ?, ?)", db_records)
            self.conn.commit()
        except Exception as e:
            print(f"❌ DB 저장 오류: {e}")

        self.check_delisting()
        
        # 지수 업데이트 및 상장 관리
        wsi_multiplier = {1: 1.5, 2: 2.2, 3: 3.5, 4: 6.0}.get(lv, 3.5)
        self.wsi = self.gri * wsi_multiplier * random.uniform(0.98, 1.02)
        
        if self.virtual_weekday == 0:
            self.handle_new_listings(silent)
        self.reassign_tiers_by_cap(True)

    else:
        if not silent:
            self.daily_news.append(f"💤 [휴장] {self.current_date.strftime('%Y-%m-%d')} 주말입니다.")

    return True
 
  def handle_group_expansion(self, silent):
    """[v100.0] 그룹 통합 관리 엔진: 대공황 시 구조조정(삭제) 및 재건기 확장"""
    current_lv = self.max_tech_reached
    # 시나리오 판정
    is_depression = "대공황" in self.current_scenario and "극복" not in self.current_scenario
    is_recovery = "극복" in self.current_scenario or "재건" in self.current_scenario

    # 1. [대공황기] 피의 구조조정: 약한 계열사를 죽여 몸통을 살림
    if is_depression:
      group_ranking = []
      for gid, ginfo in self.groups.items():
        g_members = [s for s in self.stocks if s['meta']['group_id'] == gid]
        t_cap = sum(s['market_cap'] for s in g_members)
        group_ranking.append({"gid": gid, "cap": t_cap})
     
      group_ranking.sort(key=lambda x: x['cap'], reverse=True)
      top_3_gids = [g['gid'] for g in group_ranking[:3]]

      for gid, ginfo in list(self.groups.items()):
        members = [s for s in self.stocks if s['meta']['group_id'] == gid]
        if not members: continue
       
        # 시총 낮은 순으로 정렬 (못난 자식부터 희생)
        members.sort(key=lambda x: x['market_cap'])
        core_company = members[-1] # 가장 덩치 큰 놈을 '살려야 할 몸통'으로 지정

        survival_limit = 5 if gid in top_3_gids else 3

        if len(members) > survival_limit:
          count_to_del = len(members) - survival_limit
          for i in range(count_to_del):
            target = members[i]
            if target in self.stocks and target != core_company:
              # [자본 수혈 핵심] 삭제되는 기업 자산의 30%를 몸통 기업으로 강제 이전
              transfer_asset = target['meta']['assets'] * 0.3
              core_company['meta']['assets'] += transfer_asset
              # 리스크 대폭 경감 (수혈 효과)
              core_company['meta']['risk_score'] = max(0, core_company['meta']['risk_score'] - 15.0)
             
              self.stocks.remove(target)
              if not silent:
                self.daily_news.append(f"🔪 [피의 구조조정] {ginfo['name']}그룹이 {core_company['meta']['c_name']}를 살리기 위해 {target['meta']['c_name']}를 정리하고 자본을 수혈했습니다.")
      return # 대공황 중에는 신규 확장 금지

    # 2. [평시 및 재건기: 문어발 확장]
    limit = {1: 3, 2: 5, 3: 8, 4: 10}.get(current_lv, 3)
   
    # 만약 대공황을 극복한 '재건 모드'라면 한도를 8개로 강제 고정 (공격적 확장)
    if is_recovery:
      limit = 8

    # [기존 로직: 신규 그룹 탄생]
    if len(self.groups) < self.max_group_count and random.random() < 0.01:
      candidates = [s for s in self.stocks if s['meta']['tier'] == "대형주"
             and s['meta']['group_id'] is None and s['meta']['risk_score'] < 1.0]
      if candidates:
        target_stock = max(candidates, key=lambda x: x['market_cap'])
        parent_name = target_stock['meta']['c_name']
        gid = f"GROUP_{parent_name}"
        self.groups[gid] = {"name": parent_name, "active": True}
        target_stock['meta']['group_id'] = gid
        target_stock['meta']['group'] = parent_name
        # 탄생 직후 첫 계열사 추가
        new_ind = random.choice([ind for ind in self.MAIN_INDUSTRIES if ind != target_stock['meta']['ind']])
        self.stocks.append(self.create_stock_data(None, new_ind, "소", gid))
        if not silent:
          self.daily_news.append(f"🏢 [그룹승격] {parent_name}이 지주사 체제로 전환합니다!")

    # [기존 로직: 기존 그룹 계열사 추가]
    for gid, ginfo in self.groups.items():
      members = [s for s in self.stocks if s['meta']['group_id'] == gid]
      if len(members) < limit and random.random() < 0.03:
        existing_inds = [m['meta']['ind'] for m in members]
        available_inds = [ind for ind in self.MAIN_INDUSTRIES if ind not in existing_inds]
        if available_inds:
          new_ind = random.choice(available_inds)
          self.stocks.append(self.create_stock_data(None, new_ind, "소", gid))
          if not silent:
            self.daily_news.append(f"📢 [그룹확장] {ginfo['name']}그룹이 {new_ind} 계열사를 추가했습니다.")
       
  def handle_new_listings(self, silent):
    """[최종] 상장 프로세스 단순화: 월요일 예고 -> 다음 주 월요일 상장"""
    if len(self.stocks) >= self.MAX_STOCKS:
      return

    is_depression = "대공황" in self.current_scenario and "극복" not in self.current_scenario
    today_str = self.current_date.strftime('%Y-%m-%d')

    # 1. [실제 상장 처리] 매일 체크하지만, 날짜가 도래한 것만 상장
    # 부등호(<=)를 써서 혹시라도 시뮬레이션 점프로 지나친 경우에도 상장되게 방어
    for s in self.pending_listings[:]:
      if s['meta']['listed_date'] <= today_str:
        self.stocks.append(s)
        self.pending_listings.remove(s)
        if not silent:
          self.daily_news.append(f"🚀 [신규상장] {self.CYAN}{s['meta']['c_name']}{self.RESET}이 거래를 시작합니다!")

    # 2. [신규 생성 및 예고] 오직 월요일에만 실행
    if self.virtual_weekday == 0:
      # 대공황 로직 (기존 유지)
      if is_depression:
        total_days = 252 * 10
        elapsed_days = total_days - self.scenario_timer
        if (elapsed_days / total_days) < 0.5: return
        if random.random() > 0.1: return

      spawn_count = random.randint(2, 5)
      for _ in range(spawn_count):
        new_s = self.create_stock_data(random.choice(self.NAME_DB), random.choice(self.MAIN_INDUSTRIES))
       
        # [수정] 무조건 7일 뒤(다음 주 월요일)로 날짜 고정
        listing_date = self.current_date + timedelta(days=7)
        new_s['meta']['listed_date'] = listing_date.strftime('%Y-%m-%d')
       
        self.pending_listings.append(new_s)
       
        if not silent:
          msg = f"📅 [상장예고] {self.GREEN}{new_s['meta']['c_name']}{self.RESET} ({new_s['meta']['listed_date']} 상장 예정)"
          self.daily_news.append(msg)

  def reassign_tiers_by_cap(self, silent=False):
    self.stocks.sort(key=lambda x: x['market_cap'], reverse=True)
    total = len(self.stocks)
    b_lim = max(1, int(total * 0.11)) # 상위 11%만 대형주
    m_lim = max(1, int(total * 0.33))
   
    for i, s in enumerate(self.stocks):
      old_tier = s['meta']['tier']
      if i < b_lim:
        s['meta']['tier'] = "대형주"
      elif i < m_lim:
        s['meta']['tier'] = "중형주"
      else:
        s['meta']['tier'] = "소형주"
       
      # 등급 강등 시 뉴스 출력 (선택 사항)
      if not silent and old_tier == "대형주" and s['meta']['tier'] == "중형주":
        self.daily_news.append(f"📉 [체급강등] {s['meta']['c_name']}이 시가총액 밀려나며 중견기업으로 강등되었습니다.")

  # --- UI 및 디스플레이 ---
  def display_market(self, show_all=False):
    """[UI] v140.0 최종 통합: 지배구조(5대 지분) + 인플레이션 + 매크로 지표 출력"""
    m = self.macro
    w = ['월', '화', '수', '목', '금', '토', '일'][self.virtual_weekday]

    # 1. 시나리오별 테마 색상 결정
    s_name = self.current_scenario
    if "대공황" in s_name: s_color = self.RED
    elif "T4" in s_name: s_color = self.CYAN
    elif "극복" in s_name: s_color = self.GREEN
    else: s_color = self.RESET
   
    # 2. 상단 통합 정보바 (지수 및 매크로)
    print(f"\n📅 {self.current_date.strftime('%Y-%m-%d')} ({w}) [LV.{self.max_tech_reached}]")
    print(f" {self.CYAN}📊 시장지수:{self.RESET} GRI {self.gri:,.1f} / WSI {self.wsi:,.1f} | {s_color}시나리오: {s_name}{self.RESET}")
    print(f" {self.YELLOW}🌍 거시지표:{self.RESET} 금리 {m['interest_rate']:.2f}% | 유가 ${m['oil_price']:.2f} | 물가(CPI) {m['cpi']:.2f}% | 환율 ₩{m['exchange_rate']:,.1f} | 공포지수 {m['fear_index']:.1f}")
   
    # 3. 물가 체감 수치 (인플레이션 반영)
    print(f" {self.GREEN}🛍️ 물가체감:{self.RESET} 2000년 {self.CYAN}₩1,000{self.RESET} → 현재 {self.RED}₩{self.base_item_price:,.0f}{self.RESET}")
   
    print("="*205)
    # 4. 헤더 확장 (지분 구조 5종 포함)
    header = " No | 등급 | 상태    | 그룹   | 섹터   | 회사명            | 산업분류(세부)        | 현재가 (등락)        | 주식발행수   | 자사주 | 대주주 | 외국인 | 기관 | 개인"
    print(header)
   
    # 5. 종목 정렬 및 타겟팅
    d = sorted(self.stocks, key=lambda x: x['market_cap'], reverse=True)
    target = d if show_all else (d[:15] + d[-5:])
   
    for i, s in enumerate(target):
      idx = d.index(s) + 1
      meta = s['meta']
     
      # 상태 및 등락 컬러 로직
      scolor = self.RED if "EXIT" in meta['char'] else self.RESET
      tcolor = self.RED if s['rate'] > 0 else (self.BLUE if s['rate'] < 0 else self.RESET)
      arrow = '▲' if s['rate'] > 0 else ('▼' if s['rate'] < 0 else ' ')
     
      # 텍스트 패딩 처리
      g_name = self.pad_text(meta['group'] if meta['group'] else "-", 10)
      sect = self.pad_text(self.SECTOR_MAP.get(meta['ind'], "Value"), 10)
      name = self.pad_text(meta['c_name'], 30)
      ind_sub = self.pad_text(f"{meta['ind']}({meta['sub']})", 28)
     
      # [핵심] 지분 데이터 포맷팅 (소수점 1자리)
      ts = f"{meta.get('treasury_share', 0)*100:>5.1f}%" # 자사주
      os = f"{meta.get('owner_share', 0)*100:>5.1f}%"  # 대주주
      fs = f"{meta.get('foreign_share', 0)*100:>5.1f}%" # 외국인
      is_ = f"{meta.get('inst_share', 0)*100:>5.1f}%"  # 기관
      rs = f"{meta.get('retail_share', 0)*100:>5.1f}%" # 개인

      # 최종 라인 출력
      print(f"{idx:>3} | [{meta['tier'][0]}] | {scolor}[{meta['char']:^10}]{self.RESET} | {g_name} | {sect} | "
         f"{tcolor}{name}{self.RESET} | {ind_sub} | "
         f"{tcolor}{s['price']:>12,}{self.RESET}원 ({tcolor}{arrow}{abs(s['rate']):>6.2f}%{self.RESET}) | "
         f"{s['shares']:>14,}주 | {ts} | {os} | {fs} | {is_} | {rs}")
     
      if not show_all and i == 14: print("-" * 205)
   
    # 6. 뉴스 리포트
    if self.daily_news:
      print(f" {self.GREEN}📢 오늘의 주요 뉴스:{self.RESET}")
      for news in self.daily_news:
        print(f" - {news}")
   
    print("="*205)
   
  def display_delisted(self):
    if not self.delisted_stocks:
      print(f"\n{self.YELLOW}📜 아직 상장폐지된 기업이 없습니다.{self.RESET}")
      return

    print(f"\n{self.RED}💀 [상장폐지 기업 역사관 - 전체 기록]{self.RESET}")
    print("="*185)
    print(" No |     생애 주기 (상장일 ~ 폐지일)     | 등급 | 상태 | 그룹   | 섹터   | 회사명            | 산업분류(세부)        | 마지막 주가 (등락)     | 주식발행수   | 자사주 %")
    print("-" * 185)

    # 전체 기록 출력 (오래된 순서대로 보거나 reversed로 최근 순서 선택 가능)
    for i, s in enumerate(self.delisted_stocks):
      meta = s['meta']
     
      # 날짜 정보
      life_cycle = f"{meta['listed_date']} ~ {meta.get('delisted_date', '미정')}"
     
      # 등급 및 그룹/섹터 패딩
      tier_char = meta['tier'][0]
      group_name = self.pad_text(meta['group'] if meta['group'] else "-", 10)
      sector_name = self.pad_text(self.SECTOR_MAP.get(meta['ind'], "Value"), 10)

      cap_str = self.format_cap(s['market_cap'])
     
      # 가격 및 등락 색상 (폐지니까 보통 파란색/하락이겠지만 데이터대로 출력)
      tcolor = self.RED if s['rate'] > 0 else (self.BLUE if s['rate'] < 0 else self.RESET)
      arrow = '▲' if s['rate'] > 0 else ('▼' if s['rate'] < 0 else ' ')
     
      # 상세 정보 한 줄 출력
      line = (
        f"{i+1:>3} | {life_cycle:^45} | [{tier_char}] | "
        f"{self.RED}[DELISTED ]{self.RESET} | "
        f"{group_name} | {sector_name} | "
        f"{self.pad_text(meta['c_name'], 30)} | "
        f"{self.pad_text(f'{meta['ind']}({meta['sub']})', 28)} | "
        f"{s['price']:>12,}원 ({tcolor}{arrow}{abs(s['rate']):>6.2f}%{self.RESET}) | "
        f"{s['shares']:>15,}주 | "
        f"{meta.get('treasury_share', 0)*100:>5.1f}%"
      )
      print(line)

    print("="*185)
    print(f"💡 총 {len(self.delisted_stocks)}개의 기업이 역사 속으로 사라졌습니다.")

  # 1. 매일의 상태를 상세히 기록하는 함수
  def record_current_state(self):
    """
    매일의 지표와 모든 종목 정보를 기록.
    [최적화] 메모리 부족 방지를 위해 최근 5일치 데이터만 유지합니다.
    """
    # 1. 스냅샷 데이터 생성 (기존 로직 유지)
    day_snapshot = {
      "date": self.current_date.strftime('%Y-%m-%d'),
      "tech_level": self.max_tech_reached,
      "gri": self.gri,
      "wsi": self.wsi,
      "oil": self.macro["oil_price"],
      "interest": self.macro["interest_rate"],
      "cpi": self.macro["cpi"],
      "exchange_rate": self.macro["exchange_rate"],
      "price_index": self.base_item_price,
      "scenario": self.current_scenario,
      "stocks": {s['meta']['c_name']: {
        "tier": s['meta']['tier'],
        "ind": s['meta']['ind'],
        "sub": s['meta']['sub'],
        "char": s['meta']['char'],
        "group": s['meta']['group'],
        "sector": self.SECTOR_MAP.get(s['meta']['ind'], "Value"),
        "price": s['price'],
        "rate": s['rate'],
        "shares": s['shares'],
        "assets": s['meta']['assets'],
        "risk": s['meta']['risk_score'],
        "treasury_share": s['meta'].get('treasury_share', 0.0),
        "owner_share": s['meta'].get('owner_share', 0.0),
        "foreign_share": s['meta'].get('foreign_share', 0.0),
        "inst_share": s['meta'].get('inst_share', 0.0),
        "retail_share": s['meta'].get('retail_share', 0.0)
      } for s in self.stocks}
    }

    # 2. 히스토리 리스트에 추가
    self.history_records.append(day_snapshot)

    # 3. [핵심 최적화] 리스트 크기 제한
    if len(self.history_records) > 5:
      self.history_records.pop(0) # 가장 오래된 데이터를 삭제하여 메모리 확보
   
  def export_company_history(self, company_name, interval_months=0):
    """[v145.0 최종 통합본] 5대 지분 + 실적 상세 라벨 + 모든 거시지표 + 상장폐지 기간 서사"""
    import os
    from datetime import datetime
   
    suffix = f"{interval_months}개월간격" if interval_months > 0 else "전체일자"
   
    # 바탕화면 경로 확보 및 에러 방어
    try:
      desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    except KeyError:
      desktop = os.path.join(os.path.expanduser("~"), "Desktop")
     
    path = os.path.join(desktop, f"{company_name}_{suffix}_상세연대기.txt")
    found_data = False
    last_recorded_month = -1
    last_recorded_year = -1
   
    # 상장폐지 리스트에서 해당 기업 정보 미리 확보
    delisted_info = next((s for s in self.delisted_stocks if s['meta']['c_name'] == company_name), None)

    with open(path, "w", encoding="utf-8", errors="replace") as f:
      f.write(f"📜 [{company_name}] 기업 상세 성장 연대기 (v145.0 지배구조 및 상세 지표 통합본)\n")
      if delisted_info:
        f.write(f"⚠️ 본 기업은 {delisted_info['meta'].get('delisted_date')}부로 상장폐지되었습니다.\n")
      f.write("=" * 225 + "\n\n")
     
      for rec in self.history_records:
        if company_name in rec["stocks"]:
          curr_date = datetime.strptime(rec["date"], "%Y-%m-%d")
         
          # --- [1. 연도 전환 시 상세 실적 표 및 라벨 (v55.0 기능)] ---
          if last_recorded_year != -1 and curr_date.year > last_recorded_year:
            prev_year = str(last_recorded_year)
            if company_name in self.earnings_history and prev_year in self.earnings_history[company_name]:
              y_data = self.earnings_history[company_name][prev_year]
              f.write(f"🔎 [연간 실적 보고서] {company_name} - {prev_year}년도 공시 내역\n")
              f.write("-" * 160 + "\n")
              f.write(f" 분기 | 공시일 |{'매출액':^35}|{'영업이익':^30}|{'당기순이익':^30}\n")
              f.write("-" * 160 + "\n")
             
              prev_revenue = None
              for q in ["1분기", "2분기", "3분기", "4분기"]:
                if q in y_data:
                  d = y_data[q]
                  # 성장/역성장 상세 라벨
                  rev_status = ""
                  if prev_revenue is not None:
                    if d['revenue'] > prev_revenue: rev_status = "(성장 ↑)"
                    elif d['revenue'] < prev_revenue: rev_status = "(역성장 ↓)"
                  prev_revenue = d['revenue']
                 
                  op_res = "(흑자)" if d['op_income'] > 0 else "(적자)"
                  net_res = "(흑자)" if d['net_income'] > 0 else "(적자)"
                 
                  f.write(f" {q} | {d['date']} | {d['revenue']:>18,.0f}원{rev_status:<15} | "
                      f"{d['op_income']:>18,.0f}원{op_res:<12} | "
                      f"{d['net_income']:>18,.0f}원{net_res}\n")
              f.write("-" * 160 + "\n\n")
         
          last_recorded_year = curr_date.year

          # --- [2. 간격별 지배구조 및 매크로 지표 기록 (v145.0 기능)] ---
          if interval_months > 0:
            total_months = curr_date.year * 12 + curr_date.month
            if last_recorded_month != -1 and total_months < last_recorded_month + interval_months:
              continue
            last_recorded_month = total_months
         
          found_data = True
          s = rec["stocks"][company_name]
         
          # 상단 지표바 (모든 매크로 변수 포함)
          f.write(f"📅 {rec['date']} [LV.{rec.get('tech_level', 1)}]\n")
          f.write(f" 📊 시장지수: GRI {rec['gri']:,.1f} / WSI {rec['wsi']:,.1f} | 시나리오: {rec.get('scenario', 'Normal')}\n")
          f.write(f" 🌍 거시지표: 금리 {rec.get('interest', 0):.2f}% | 유가 ${rec.get('oil', 0):.2f} | "
              f"물가(CPI) {rec.get('cpi', 0):.2f}% | 환율 ₩{rec.get('exchange_rate', 0):,.1f} | 공포지수 {rec.get('fear_index', 10.0):.1f}\n")
          f.write(f" 🛍️ 물가체감: 2000년 ₩1,000 → 현재 ₩{rec.get('price_index', 1000):,.0f}\n")
          f.write("-" * 225 + "\n")
          f.write(" No | 등급 | 상태    | 그룹   | 섹터   | 회사명       | 산업분류(세부)       | 현재가 (등락)       | 주식발행수   | 자사주 | 대주주 | 외국인 | 기관 | 개인\n")
         
          arrow = '▲' if s['rate'] > 0 else ('▼' if s['rate'] < 0 else ' ')
         
          # 지분 구조 5종 데이터 정렬
          ts = f"{s.get('treasury_share', 0)*100:>6.1f}%"; os_ = f"{s.get('owner_share', 0)*100:>6.1f}%"
          fs = f"{s.get('foreign_share', 0)*100:>6.1f}%"; is_ = f"{s.get('inst_share', 0)*100:>6.1f}%"; rs = f"{s.get('retail_share', 0)*100:>6.1f}%"

          line = (
            f" {s.get('rank', '-'):>2} | [{s['tier'][0]}] | [{s['char']:^10}] | "
            f"{self.pad_text(str(s.get('group', '-')), 10)} | {self.pad_text(str(s.get('sector', '-')), 10)} | "
            f"{self.pad_text(company_name, 20)} | {self.pad_text(f'{s.get('ind', '-')}({s.get('sub', '-')})', 28)} | "
            f"{s['price']:>12,}원 ({arrow}{abs(s['rate']):>6.2f}%) | {s['shares']:>15,}주 | "
            f"{ts} | {os_} | {fs} | {is_} | {rs}\n"
          )
          f.write(line)
          f.write("=" * 225 + "\n\n")

      # --- [3. 상장폐지 서사 및 최종 데이터 기록] ---
      if delisted_info:
        m = delisted_info['meta']
        f.write(f"💀 [상장폐지 엔딩] {company_name}이(가) 시장에서 퇴출되었습니다.\n")
        f.write(f" 🕒 상장 유지 기간: {m.get('listed_date')} ~ {m.get('delisted_date')}\n")
        f.write("-" * 225 + "\n")
       
        # 최종 지분율 데이터
        ts = f"{m.get('treasury_share', 0)*100:>6.1f}%"; os_ = f"{m.get('owner_share', 0)*100:>6.1f}%"
        fs = f"{m.get('foreign_share', 0)*100:>6.1f}%"; is_ = f"{m.get('inst_share', 0)*100:>6.1f}%"; rs = f"{m.get('retail_share', 0)*100:>6.1f}%"
       
        f.write(f" [최종 데이터] 종가: {delisted_info['price']:,}원 | 자사주:{ts} | 대주주:{os_} | 외국인:{fs} | 기관:{is_} | 개인:{rs}\n")
        f.write("=" * 225 + "\n")
        f.write(f"🏁 {company_name}의 모든 기록 종료.\n")

    print(f"✅ {company_name} 상세 연대기(풀세트) 저장 완료!")

  def export_full_history(self, interval_months=0):
    """[v145.0 최종 통합본] 전 종목 TOP 10: 기간 수익률 + 5대 지분 + 모든 거시지표 포함"""
    import os
    from datetime import datetime
   
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    f_name = os.path.join(desktop, f"시장_개월단위_TOP10_{self.current_date.strftime('%Y%m%d')}.txt")
   
    print(f"\n📥 [데이터 추출] {interval_months}개월 간격으로 지배구조 및 매크로 통합 데이터를 생성 중...")
   
    try:
      with open(f_name, "w", encoding="utf-8", errors="replace") as f:
        f.write(f"📜 시장 성장 연대기 (TOP 10) | 지배구조 및 거시지표 풀세트 포함\n")
        f.write("=" * 225 + "\n\n")
       
        last_total_months = -1
        prev_prices_map = {}
       
        for rec in self.history_records:
          curr_date = datetime.strptime(rec["date"], "%Y-%m-%d")
          current_total_months = curr_date.year * 12 + curr_date.month
         
          if interval_months <= 0 or last_total_months == -1 or current_total_months >= last_total_months + interval_months:
            last_total_months = current_total_months
           
            # 상단 통합 지표 (GRI, WSI, 금리, 유가, CPI, 환율, 공포, 물가체감)
            f.write(f"📅 {rec['date']} [LV.{rec.get('tech_level', 1)}]\n")
            f.write(f" 📊 시장지수: GRI {rec['gri']:,.1f} / WSI {rec['wsi']:,.1f} | 시나리오: {rec.get('scenario', 'Normal')}\n")
            f.write(f" 🌍 거시지표: 금리 {rec.get('interest', 0):.2f}% | 유가 ${rec.get('oil', 0):.2f} | "
                f"물가(CPI) {rec.get('cpi', 0):.2f}% | 환율 ₩{rec.get('exchange_rate', 0):,.1f} | 공포지수 {rec.get('fear_index', 10.0):.1f}\n")
            f.write(f" 🛍️ 물가체감: 2000년 ₩1,000 → 현재 ₩{rec.get('price_index', 1000):,.0f}\n")
            f.write("-" * 225 + "\n")
            f.write(" No | 등급 | 상태    | 그룹   | 섹터   | 회사명       | 산업분류(세부)       | 현재가 (기간수익률)     | 주식발행수   | 자사주 | 대주주 | 외국인 | 기관 | 개인\n")
           
            sorted_stocks = sorted(rec["stocks"].items(), key=lambda x: x[1]['price'] * x[1]['shares'], reverse=True)
            top_10 = sorted_stocks[:10]
           
            for idx, (name, s) in enumerate(top_10, 1):
              # 기간 수익률 계산 로직 (v57.0)
              current_p = s['price']
              if name in prev_prices_map:
                old_p = prev_prices_map[name]
                display_rate = round(((current_p / old_p) - 1) * 100, 2) if old_p > 0 else 0.0
              else:
                display_rate = s['rate']
             
              arrow = '▲' if display_rate > 0 else ('▼' if display_rate < 0 else ' ')
             
              # 지분 구조 5종 데이터 정렬
              ts = f"{s.get('treasury_share', 0)*100:>6.1f}%"; os_ = f"{s.get('owner_share', 0)*100:>6.1f}%"
              fs = f"{s.get('foreign_share', 0)*100:>6.1f}%"; is_ = f"{s.get('inst_share', 0)*100:>6.1f}%"; rs = f"{s.get('retail_share', 0)*100:>6.1f}%"

              line = (
                f"{idx:>3} | [{s['tier'][0]}] | [{s['char']:^10}] | "
                f"{self.pad_text(str(s.get('group', '-')), 10)} | {self.pad_text(s.get('sector', '-'), 10)} | "
                f"{self.pad_text(name, 20)} | {self.pad_text(f'{s.get('ind', '-')}({s.get('sub', '-')})', 28)} | "
                f"{s['price']:>12,}원 ({arrow}{abs(display_rate):>6.2f}%) | {s['shares']:>15,}주 | "
                f"{ts} | {os_} | {fs} | {is_} | {rs}\n"
              )
              f.write(line)
           
            f.write("=" * 225 + "\n\n")
           
            # 기준가 갱신
            for s_name, s_data in rec["stocks"].items():
              prev_prices_map[s_name] = s_data['price']

      print(f"✅ 시장 TOP 10 통합 연대기 저장 완료!")
    except Exception as e:
      print(f"❌ 오류 발생: {e}")
     
if __name__ == "__main__":
  os.system('color')
  game = StockGameEngine()
  game.initialize_market()
  game.display_market()
 
  while True:
    # 입력 가이드
    prompt = f"\n▶ [{game.current_date.strftime('%Y-%m-%d')}] 엔터(다음날) | '전체' | '그룹' | '상장폐지' | 'YYYY-MM-DD[단위][간격]' | 뽑기[단위] | 실적[회사명][년도] | 종료 > "
    cmd = input(prompt).strip()
   
    if cmd == "종료":
      break

    # 1. 뽑기 명령어 처리 (데이터 추출)
    elif cmd.startswith("뽑기"):
      params = re.findall(r"\[(.*?)\]", cmd)
     
      if len(params) == 2: # 예: 뽑기[제니스 건강관리][6] -> 특정 회사/간격
        company = params[0]
        interval = int(params[1]) if params[1].isdigit() else 0
        game.export_company_history(company, interval)
     
      elif len(params) == 1:
        if params[0].isdigit(): # 예: 뽑기[12] -> 전체 시장/간격
          game.export_full_history(int(params[0]))
        else: # 예: 뽑기[제니스 건강관리] -> 특정 회사/전체 기간
          game.export_company_history(params[0], 0)
     
      else: # 예: 뽑기 -> 전체 시장/매일 기록
        game.export_full_history(0)

    # 2. 실적 명령어 처리 (분기 실적 조회)
    elif cmd.startswith("실적"):
      params = re.findall(r"\[(.*?)\]", cmd)
      if len(params) == 2: # 예: 실적[제니스 건강관리][2026]
        game.show_earnings(params[0], params[1])
      elif len(params) == 1: # 예: 실적[제니스 건강관리]
        game.show_earnings(params[0])
      else:
        print(f"{game.YELLOW}⚠️ 사용법: 실적[회사명] 또는 실적[회사명][연도]{game.RESET}")

    # 3. 단순 조회 명령어
    elif cmd == "전체":
      game.display_market(True)
    elif cmd == "상장폐지":
      game.display_delisted()
    elif cmd == "그룹":
      game.display_groups()
     
    # 4. 날짜 가속 및 시나리오 치트 로직
    elif re.match(r"\d{4}-\d{2}-\d{2}", cmd):
      try:
        target_date_str = re.search(r"\d{4}-\d{2}-\d{2}", cmd).group()
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
       
        params = re.findall(r"\[(.*?)\]", cmd)
        step = int(params[0]) if len(params) > 0 and params[0].isdigit() else 0
        cheat = params[1] if len(params) > 1 else None
       
        if cheat:
          scenarios = {
            "대공황V": "✨ 대공황V (고난과 부활)",
            "대공황": "💀 대공황 (시스템 붕괴)",
            "T4": "🚀 T4 발전 (기술 특이점)",
            "테크4": "🚀 T4 발전 (기술 특이점)",
            "T3": "🟢 T3 유지 (저성장 정체)",
            "테크3": "🟢 T3 유지 (저성장 정체)",
            "정상": "정상 성장"
          }
         
          target_scenario = "정상 성장"
          cheat_key = cheat.upper()
         
          for key, val in scenarios.items():
            if key.upper() in cheat_key:
              target_scenario = val
              # ❌ [삭제] 여기서 game.max_tech_reached를 3이나 4로 직접 바꾸는 코드를 지워!
              break
         
          # [수정 핵심] 2045년(또는 2050년) 이전이면 무조건 '예약'만 함
          # 이렇게 해야 실제 2050~2060년 분기점이 올 때까지 레벨이 유지돼.
          if game.current_date.year < 2045:
            game.world_line = "Normal"
            game.reserved_scenario = target_scenario
            print(f"🔮 [미래 예약] 2050~2060년 사이 분기점 운명이 '{target_scenario}'로 고정되었습니다.")
          else:
            game.world_line = "Decided"
            game.current_scenario = target_scenario
           
        # 3) 가속 시뮬레이션 엔진
        print(f"⏩ {target_date_str}까지 {step}년 간격 시뮬레이션 시작... (현재 테크: LV.{game.max_tech_reached})")
       
        # 가속 전 기준 가격 저장
        base_prices = {s['meta']['c_name']: s['price'] for s in game.stocks}

        while game.current_date < target_date:
          old_year = game.current_date.year
         
          # 하루 진행 (이 안에서 record_current_state가 모든 지표를 기록함)
          game.next_day(silent=True)
          game.record_current_state()
         
          # 설정한 step(년) 주기가 되었을 때 중간 보고서 출력
          if step > 0 and game.current_date.year > old_year:
            if (game.current_date.year - game.start_date.year) % step == 0:
              # 출력용 임시 수익률 계산 (이전 보고 시점 대비)
              for s in game.stocks:
                name = s['meta']['c_name']
                if name in base_prices:
                  old_p = base_prices[name]
                  s['rate'] = round(((s['price'] / old_p) - 1) * 100, 2) if old_p > 0 else 0.0
             
              print(f"\n{game.CYAN}📊 {game.current_date.year}년 정기 결산 보고 (LV.{game.max_tech_reached}){game.RESET}")
              game.display_market()
              game.display_groups()
             
              # 기준 가격 갱신 (다음 구간 계산용)
              base_prices = {s['meta']['c_name']: s['price'] for s in game.stocks}
       
        # 4) 가속 종료 후 최종 화면 처리
        # 가속 기간 전체 수익률로 마지막 rate 갱신
        for s in game.stocks:
          name = s['meta']['c_name']
          if name in base_prices:
            s['rate'] = round(((s['price'] / base_prices[name]) - 1) * 100, 2) if base_prices[name] > 0 else 0.0
       
        print(f"\n{game.GREEN}🏁 시뮬레이션 완료: {game.current_date.strftime('%Y-%m-%d')} (최종 테크: LV.{game.max_tech_reached}){game.RESET}")
        game.display_market()
        game.display_groups()
       
      except Exception as e:
        print(f"⚠️ 가속 중 오류 발생: {e}")
        import traceback
        traceback.print_exc() # 에러 위치 확인용

    # 5. 기본 동작: 엔터 입력 시 다음날로 진행
    else:
      game.next_day()
      game.display_market()
      game.record_current_state()