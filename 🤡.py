"""조선 전생 장부 – 나의 엽전 일대기

streamlit run joseon_ledger.py

선택할 때마다 엽전이 들고 나는 '장부형' 전생 테스트.
두 갈래(모험 ↔ 안전, 씀씀이 ↔ 절약)를 조합해 네 가지 전생 신분이 나온다.

디자인 메모
- 쪽빛 보자기 위에 펼쳐 둔 한지 장부 한 장. 화면 전체가 '책상 위의 장부'다.
- 색은 다섯 가지만: 쪽빛(바탕), 한지(종이), 먹(글자), 인주(붉은 도장·손실), 놋쇠(엽전).
- 제목은 송명체, 본문은 고운바탕. 숫자는 고정폭 숫자로 줄을 맞춘다.
- 움직임은 결과 화면의 도장 찍기 한 번뿐이다(동작 줄이기 설정 시 생략).
"""

import streamlit as st

st.set_page_config(
    page_title="조선 전생 장부",
    page_icon="🪙",
    layout="centered",
)


def html(markup: str) -> None:
    """들여쓰기·빈 줄 때문에 HTML이 코드 블록으로 깨지지 않도록 정리해서 출력."""
    lines = [line.strip() for line in markup.strip().splitlines()]
    st.markdown("\n".join(line for line in lines if line), unsafe_allow_html=True)


# ──────────────────────────────────────────────
# 스타일
# ──────────────────────────────────────────────
html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Song+Myung&display=swap');

    :root {
        --indigo: #1e2b4a;
        --indigo-deep: #131c31;
        --paper: #efe7d4;
        --paper-shade: #e3d8bf;
        --ink: #24201b;
        --ink-soft: #5a5046;
        --seal: #b3302a;
        --brass: #a8843a;
        --rule: #cdb994;
        --display: 'Song Myung', 'Noto Serif KR', serif;
        --body: 'Gowun Batang', 'Noto Serif KR', serif;
    }

    /* 글꼴은 글자에만, Streamlit 아이콘 글꼴은 그대로 둔다 */
    html, body, .stApp, p, li, span, div, label, button, td, th, h1, h2, h3, h4 { font-family: var(--body); }
    [data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons {
        font-family: 'Material Symbols Rounded' !important;
    }
    [data-testid="stHeaderActionElements"], .stMarkdown a.anchor-link { display: none !important; }

    /* 쪽빛 보자기 바탕 + 한지 한 장 */
    .stApp {
        background:
            radial-gradient(circle at 20% 10%, rgba(255,255,255,0.05), transparent 45%),
            var(--indigo);
        word-break: keep-all; overflow-wrap: break-word;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stMainBlockContainer"], .block-container {
        background: var(--paper);
        color: var(--ink);
        max-width: 680px;
        margin: 48px auto 64px auto;
        padding: 44px 48px 40px 48px !important;
        border-radius: 3px;
        box-shadow: 0 1px 0 var(--paper-shade), 0 24px 48px var(--indigo-deep);
    }
    @media (max-width: 640px) {
        [data-testid="stMainBlockContainer"], .block-container {
            margin: 12px 10px 32px 10px; padding: 28px 20px 28px 20px !important;
        }
    }

    /* 장부 머리 */
    .book-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 16px; }
    .book-title { font-family: var(--display); font-size: 2.1rem; line-height: 1.15; color: var(--ink); margin: 0; }
    .book-lede { color: var(--ink-soft); font-size: 0.95rem; line-height: 1.7; margin-top: 8px; max-width: 30em; }
    .book-rule { border-top: 3px double var(--ink); margin: 20px 0 22px 0; }

    /* 엽전 진행 표시: 답한 장은 채운 엽전, 지금 장은 테두리 강조 */
    .coins { display: flex; flex-wrap: wrap; gap: 6px; }
    .coin {
        width: 18px; height: 18px; border-radius: 50%; position: relative;
        border: 1.5px solid var(--brass); box-sizing: border-box;
    }
    .coin::after {
        content: ""; position: absolute; width: 6px; height: 6px; left: 50%; top: 50%;
        transform: translate(-50%, -50%); background: var(--paper); border: 1px solid var(--brass);
    }
    .coin.done { background: var(--brass); }
    .coin.now { box-shadow: 0 0 0 2px var(--paper), 0 0 0 3.5px var(--ink); }
    .progress-row { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
    .purse { text-align: right; }
    .purse .k { font-size: 0.8rem; color: var(--ink-soft); }
    .purse .v { font-family: var(--display); font-size: 1.6rem; font-variant-numeric: tabular-nums; }
    .neg { color: var(--seal); }

    .last-line {
        display: flex; justify-content: space-between; gap: 12px;
        font-size: 0.9rem; color: var(--ink-soft);
        border-bottom: 1px solid var(--rule); padding: 10px 0 8px 0; margin-top: 14px;
    }
    .last-line b { font-variant-numeric: tabular-nums; color: var(--ink); }
    .last-line b.neg { color: var(--seal); }

    /* 질문 */
    .chapter { color: var(--seal); font-size: 0.9rem; margin: 28px 0 8px 0; }
    .prompt { font-family: var(--display); font-size: 1.65rem; line-height: 1.45; margin: 0 0 22px 0; }

    /* 선택지: 장부에 끼워 둔 쪽지 */
    div[class*="st-key-pick_"] button {
        background: #f8f3e7 !important;
        color: var(--ink) !important;
        border: 1px solid var(--rule) !important;
        border-left: 4px solid var(--ink) !important;
        border-radius: 2px !important;
        min-height: 68px !important; height: auto !important;
        padding: 14px 20px !important;
        justify-content: flex-start !important; text-align: left !important;
        box-shadow: none !important;
        transition: background 120ms ease, border-color 120ms ease;
    }
    div[class*="st-key-pick_"] button p {
        white-space: normal !important; font-size: 1.05rem !important; line-height: 1.6 !important;
    }
    div[class*="st-key-pick_"] button:hover {
        background: #fffaf0 !important; border-left-color: var(--seal) !important;
    }
    div[class*="st-key-pick_"] button:focus-visible,
    .stButton button:focus-visible { outline: 2px solid var(--indigo) !important; outline-offset: 3px; }

    /* 보조 버튼: 글자만 */
    .st-key-undo button, .st-key-restart button {
        background: transparent !important; color: var(--ink-soft) !important;
        border: none !important; box-shadow: none !important; padding: 4px 0 !important;
        text-decoration: underline; text-underline-offset: 4px;
    }
    .st-key-undo button:hover, .st-key-restart button:hover { color: var(--seal) !important; }

    /* 결과: 전생 초상화 + 낙관 도장 */
    .verdict { display: grid; grid-template-columns: 196px 1fr; gap: 32px; align-items: center; }
    .verdict .pre { color: var(--ink-soft); font-size: 0.95rem; }
    .verdict .name { font-family: var(--display); font-size: clamp(1.9rem, 7vw, 2.5rem); line-height: 1.2; margin: 4px 0 8px 0; }
    .verdict .sub { color: var(--ink-soft); line-height: 1.6; }
    .portrait {
        position: relative; background: var(--paper-shade);
        border: 1px solid var(--ink); outline: 4px solid var(--paper-shade); outline-offset: 3px;
        margin: 7px;
    }
    .portrait svg { display: block; width: 100%; height: auto; }
    @media (max-width: 520px) {
        .verdict { grid-template-columns: 1fr; gap: 26px; }
        .portrait { width: 70%; max-width: 220px; margin: 7px auto; }
    }
    .seal {
        position: absolute; right: -16px; bottom: -14px;
        width: 62px; height: 62px; border: 3px solid var(--seal); border-radius: 5px;
        background: rgba(239, 231, 212, 0.55);
        color: var(--seal); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1px;
        font-family: var(--display); font-size: 1.3rem; line-height: 1;
        transform: rotate(-6deg); opacity: 0.92;
        animation: stamp 520ms cubic-bezier(.2,.9,.3,1.2) 200ms both;
    }
    @keyframes stamp {
        from { transform: rotate(-6deg) scale(1.8); opacity: 0; }
        to   { transform: rotate(-6deg) scale(1);   opacity: 0.92; }
    }
    @media (prefers-reduced-motion: reduce) { .seal { animation: none; } }

    /* 결과: 합계 줄 */
    .total {
        display: flex; justify-content: space-between; align-items: baseline; gap: 12px; flex-wrap: wrap;
        border-top: 1px solid var(--ink); border-bottom: 3px double var(--ink);
        padding: 14px 0; margin: 26px 0 8px 0;
    }
    .total .k { font-size: 0.95rem; }
    .total .v { font-family: var(--display); font-size: 2.2rem; font-variant-numeric: tabular-nums; }
    .tier { color: var(--ink-soft); font-size: 0.95rem; margin-bottom: 26px; }

    /* 결과: 저울 */
    .h { font-family: var(--display); font-size: 1.3rem; margin: 28px 0 12px 0; }
    .scale { margin-bottom: 18px; }
    .scale .ends { display: flex; justify-content: space-between; font-size: 0.92rem; margin-bottom: 6px; }
    .scale .beam { position: relative; height: 22px; }
    .scale .beam::before {
        content: ""; position: absolute; left: 0; right: 0; top: 50%; border-top: 2px solid var(--ink);
    }
    .scale .beam::after {
        content: ""; position: absolute; left: 50%; top: 3px; height: 16px; border-left: 1px solid var(--ink-soft);
    }
    .scale .knob {
        position: absolute; top: 0; width: 22px; height: 22px; margin-left: -11px; border-radius: 50%;
        background: var(--brass); border: 1.5px solid var(--ink); box-sizing: border-box; z-index: 1;
    }
    .scale .knob::after {
        content: ""; position: absolute; width: 7px; height: 7px; left: 50%; top: 50%;
        transform: translate(-50%, -50%); background: var(--paper); border: 1px solid var(--ink);
    }

    .story { font-size: 1.02rem; line-height: 1.85; max-width: 34em; }
    .note {
        margin-top: 16px; padding: 12px 16px; background: #f8f3e7;
        border: 1px dashed var(--rule); font-size: 0.95rem; line-height: 1.7; color: var(--ink-soft);
    }
    .note b { color: var(--seal); font-weight: 700; margin-right: 6px; }

    /* 결과: 장부 표 */
    .ledger-wrap { overflow-x: auto; }
    table.ledger { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
    table.ledger th {
        text-align: left; font-weight: 700; padding: 8px 10px;
        border-bottom: 1px solid var(--ink); color: var(--ink);
    }
    table.ledger td { padding: 8px 10px; border-bottom: 1px solid var(--rule); vertical-align: top; }
    table.ledger td + td, table.ledger th + th { border-left: 1px solid rgba(179,48,42,0.35); }
    table.ledger .num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
    table.ledger .when { color: var(--ink-soft); white-space: nowrap; }
    table.ledger tr.sum td { border-top: 1px solid var(--ink); border-bottom: 3px double var(--ink); font-weight: 700; }
    </style>
    """
)

START_COIN = 100

# ──────────────────────────────────────────────
# 문항: 선택마다 '갈래 기울기(lean)'와 '엽전 증감(coin)'이 붙는다
#   risk  갈래: +1 모험, -1 안전
#   spend 갈래: +1 씀씀이, -1 절약
# ──────────────────────────────────────────────
QUESTIONS = [
    {
        "scene": "봄, 집 마당", "axis": "risk",
        "prompt": "여윳돈 100냥이 생겼다! 어떻게 지킬까?",
        "options": [
            {"text": "땅을 파고 항아리에 엽전을 꽁꽁 숨겨둔다", "lean": -1, "coin": 0, "memo": "항아리에 묻음"},
            {"text": "장사하는 친구에게 빌려주고 이자를 받아낸다", "lean": +1, "coin": 40, "memo": "친구 이자 수입"},
        ],
    },
    {
        "scene": "봄, 저잣거리", "axis": "spend",
        "prompt": "눈에 쏙 들어오는 명품 비단신을 발견했다!",
        "options": [
            {"text": "실속형 짚신이면 충분하다, 눈길도 안 준다", "lean": -1, "coin": 10, "memo": "짚신으로 버팀"},
            {"text": "품위도 자기 투자! 기꺼이 지갑을 연다", "lean": +1, "coin": -30, "memo": "비단신 구입"},
        ],
    },
    {
        "scene": "여름, 흉년", "axis": "risk",
        "prompt": "흉년으로 장사 수입이 반토막 났다. 어떻게 할까?",
        "options": [
            {"text": "불필요한 지출을 끊고 허리띠를 바짝 졸라맨다", "lean": -1, "coin": -10, "memo": "흉년 버티기"},
            {"text": "새 살림 도구나 유통 품목을 찾아 돌파구를 연다", "lean": +1, "coin": 30, "memo": "새 품목 개척"},
        ],
    },
    {
        "scene": "여름, 논두렁", "axis": "spend",
        "prompt": "고된 논일을 끝낸 일꾼들에게 품삯을 줄 때 나는?",
        "options": [
            {"text": "오늘 일한 만큼 칼같이 계산해서 준다", "lean": -1, "coin": -15, "memo": "품삯 정산"},
            {"text": "앞으로의 신뢰를 보고 넉넉히 얹어준다", "lean": +1, "coin": -25, "memo": "품삯과 웃돈"},
        ],
    },
    {
        "scene": "여름, 장터 소문", "axis": "risk",
        "prompt": "'어느 고을 특산품 값이 폭등한다'는 소문이 돈다!",
        "options": [
            {"text": "뜬소문일지 몰라, 내 논밭 일에만 집중한다", "lean": -1, "coin": 10, "memo": "논밭 수확"},
            {"text": "보부상 줄을 통해 진위를 캐고 바로 움직인다", "lean": +1, "coin": 50, "memo": "특산품 차익"},
        ],
    },
    {
        "scene": "가을, 객주", "axis": "risk",
        "prompt": "객주 주인에게 급히 돈을 빌려야 할 일이 생겼다면?",
        "options": [
            {"text": "아쉬운 소리도, 빚도 질색이다", "lean": -1, "coin": 0, "memo": "빚 없음"},
            {"text": "신용도 자산! 계획을 세워 빌린 돈을 굴린다", "lean": +1, "coin": 60, "memo": "빌린 돈 굴린 이문"},
        ],
    },
    {
        "scene": "가을, 이사철", "axis": "spend",
        "prompt": "살 집을 고르는 가장 중요한 기준은?",
        "options": [
            {"text": "텃밭 딸린 정겨운 초가집이면 족하다", "lean": -1, "coin": 20, "memo": "텃밭 채소 수입"},
            {"text": "번듯한 기와집이 체면이고 자산이다", "lean": +1, "coin": -50, "memo": "기와집 수리비"},
        ],
    },
    {
        "scene": "가을, 서해 뱃길", "axis": "risk",
        "prompt": "청나라 무역선을 탔는데 폭풍우를 만났다!",
        "options": [
            {"text": "역시 모험은 아니었어… 다음엔 내 땅만 믿는다", "lean": -1, "coin": 0, "memo": "무사 귀환"},
            {"text": "위험이 클수록 이문도 크다! 끝까지 버틴다", "lean": +1, "coin": -40, "memo": "폭풍에 짐 일부 유실"},
        ],
    },
    {
        "scene": "겨울, 사랑방", "axis": "spend",
        "prompt": "한 달 엽전 장부를 들여다보는 나의 모습은?",
        "options": [
            {"text": "한 푼 오차도 없이 대조하고 반성한다", "lean": -1, "coin": 15, "memo": "새는 돈 막음"},
            {"text": "큰 틀에서 흑자면 그만, 대충 훑는다", "lean": +1, "coin": -20, "memo": "어디 갔는지 모를 돈"},
        ],
    },
    {
        "scene": "겨울, 마을 회의", "axis": "risk",
        "prompt": "이웃이 '대박 금광 사업'을 같이 하자고 한다!",
        "options": [
            {"text": "눈에 보이는 곡식과 땅이 아니면 안 믿는다", "lean": -1, "coin": 10, "memo": "곡식 저장"},
            {"text": "성장 가능성을 따져보고 과감히 투자한다", "lean": +1, "coin": 100, "memo": "금광 지분 배당"},
        ],
    },
    {
        "scene": "노년, 은퇴", "axis": "spend",
        "prompt": "은퇴 후 꿈꾸는 노후는?",
        "options": [
            {"text": "논 몇 마지기 물려주고 조용히 시골살이", "lean": -1, "coin": 20, "memo": "소박한 노후"},
            {"text": "큰 가옥에서 손님 치르며 넉넉하게", "lean": +1, "coin": -40, "memo": "잔치 비용"},
        ],
    },
    {
        "scene": "마지막 장", "axis": "spend",
        "prompt": "내 인생에서 엽전이란?",
        "options": [
            {"text": "땀 흘린 정직한 대가, 가족을 지키는 도구", "lean": -1, "coin": 10, "memo": "가족 비상금"},
            {"text": "쓰라고 있는 것! 써야 세상이 돈다", "lean": +1, "coin": -10, "memo": "인심 쓰기"},
        ],
    },
]

# (risk 갈래, spend 갈래) → 전생 신분. seal은 도장에 새길 두 글자.
TYPES = {
    ("안전", "절약"): {
        "seal": "農夫", "portrait": "farmer",
        "title": "곳간지기 농부",
        "sub": "한 톨도 허투루 안 쓰는 든든한 살림꾼",
        "desc": "땅과 곡식처럼 눈에 보이는 것만 믿고, 들어온 엽전은 꼭꼭 쌓아두던 사람입니다. "
                "흉년이 와도 마을에서 가장 늦게 굶는 집이 바로 당신 집이었죠.",
        "tip": "가끔은 이웃 장사꾼 이야기에도 귀를 열어보세요. 곳간 문을 반 뼘만 열어도 볕이 듭니다.",
    },
    ("안전", "씀씀이"): {
        "seal": "兩班", "portrait": "yangban",
        "title": "체면 지키는 양반 나리",
        "sub": "재산은 안전하게, 쓰는 건 품위 있게",
        "desc": "위험한 장사엔 손대지 않지만 비단신과 기와집, 손님 대접만큼은 아끼지 않던 사람입니다. "
                "곳간보다 사랑방이 더 붐비던 집이었죠.",
        "tip": "들어오는 길은 좁은데 나가는 길이 넓어요. 장부 한 번만 들여다보면 체면도 곳간도 지킬 수 있습니다.",
    },
    ("모험", "절약"): {
        "seal": "褓商", "portrait": "peddler",
        "title": "발로 뛰는 보부상",
        "sub": "소문은 빠르게, 지갑은 단단하게",
        "desc": "등짐을 지고 팔도를 누비며 남보다 먼저 시세를 읽던 사람입니다. "
                "번 돈은 허투루 쓰지 않고 다음 장사 밑천으로 돌렸죠.",
        "tip": "기회를 보는 눈과 아끼는 손을 다 가졌어요. 다만 몸이 밑천이니 쉬는 것도 투자랍니다.",
    },
    ("모험", "씀씀이"): {
        "seal": "巨商", "portrait": "merchant",
        "title": "판을 키우는 거상",
        "sub": "크게 벌고 크게 쓰는 저잣거리의 큰손",
        "desc": "금광이든 무역선이든 판이 크면 일단 뛰어들고, 번 만큼 화끈하게 쓰던 사람입니다. "
                "객주마다 당신 이름 석 자 모르는 사람이 없었죠.",
        "tip": "들고 나는 폭이 큰 만큼 비상금 항아리 하나쯤은 따로 묻어두세요.",
    },
}


# ──────────────────────────────────────────────
# 전생 초상화: 같은 얼굴 틀에 신분별 모자·옷·소품만 바꿔 그린다
# ──────────────────────────────────────────────
INK, SKIN, BLUSH = "#24201b", "#f2d4bd", "#e39a8c"
LINE = f'stroke="{INK}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"'

PORTRAIT_PARTS = {
    "farmer": {
        "behind": "",
        "robe": "#d8c9a3",
        "eyes": f'<path d="M66 95 q5 -5 10 0 M84 95 q5 -5 10 0" fill="none" {LINE}/>',
        "extra_face": "",
        "hat": (
            # 삿갓: 넓은 고깔 + 짚 결
            f'<polygon points="80,34 20,84 140,84" fill="#c9a45c" {LINE}/>'
            f'<path d="M80 36 L50 82 M80 36 L80 83 M80 36 L110 82" fill="none" stroke="#8a6d33" stroke-width="1"/>'
        ),
        # 벼 이삭
        "prop": (
            f'<path d="M124 178 Q122 150 132 128" fill="none" stroke="#7a6a2e" stroke-width="2"/>'
            f'<g fill="#c9a45c" stroke="{INK}" stroke-width="0.8">'
            f'<ellipse cx="134" cy="126" rx="3" ry="6" transform="rotate(25 134 126)"/>'
            f'<ellipse cx="128" cy="134" rx="3" ry="6" transform="rotate(-30 128 134)"/>'
            f'<ellipse cx="136" cy="138" rx="3" ry="6" transform="rotate(35 136 138)"/></g>'
        ),
    },
    "yangban": {
        "behind": "",
        "robe": "#f6f1e6",
        "eyes": f'<path d="M65 96 h11 M84 96 h11" fill="none" {LINE}/>',
        # 가는 수염
        "extra_face": f'<path d="M72 112 q8 -4 16 0" fill="none" {LINE}/><path d="M80 118 v10" fill="none" {LINE}/>',
        "hat": (
            # 갓: 검은 챙 + 높은 모자 + 갓끈
            f'<rect x="60" y="34" width="40" height="34" rx="5" fill="{INK}" opacity="0.88"/>'
            f'<ellipse cx="80" cy="70" rx="60" ry="9" fill="{INK}" opacity="0.82"/>'
            f'<path d="M48 72 Q56 120 74 130 M112 72 Q104 120 86 130" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="1 4"/>'
        ),
        # 남색 세조대
        "prop": f'<path d="M48 160 Q80 168 112 160" fill="none" stroke="#1e2b4a" stroke-width="5"/>',
    },
    "peddler": {
        # 등에 진 지게
        "behind": (
            f'<path d="M40 98 L34 182 M120 98 L126 182" fill="none" stroke="#7a5a32" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M37 132 H123" fill="none" stroke="#7a5a32" stroke-width="4"/>'
        ),
        "robe": "#1e2b4a",
        "eyes": f'<circle cx="70" cy="95" r="3" fill="{INK}"/><circle cx="90" cy="95" r="3" fill="{INK}"/>',
        "extra_face": "",
        "hat": (
            # 패랭이 + 목화송이
            f'<rect x="58" y="44" width="44" height="26" rx="8" fill="#b8975a" {LINE}/>'
            f'<ellipse cx="80" cy="71" rx="46" ry="8" fill="#b8975a" {LINE}/>'
            f'<circle cx="108" cy="52" r="7" fill="#ffffff" {LINE}/>'
            f'<circle cx="116" cy="62" r="6" fill="#ffffff" {LINE}/>'
        ),
        # 등짐 끈
        "prop": f'<path d="M58 128 L66 178 M102 128 L94 178" fill="none" stroke="#b8975a" stroke-width="4"/>',
    },
    "merchant": {
        "behind": "",
        "robe": "#a8843a",
        "eyes": f'<path d="M65 97 q5 -6 11 -1 M84 96 q6 -5 11 1" fill="none" {LINE}/>',
        # 끝이 말린 콧수염
        "extra_face": f'<path d="M80 108 q-8 4 -14 -1 M80 108 q8 4 14 -1" fill="none" {LINE}/>',
        "hat": (
            # 둥근 두건
            f'<path d="M48 80 Q46 40 80 38 Q114 40 112 80 Q80 70 48 80 Z" fill="#1e2b4a" {LINE}/>'
            f'<path d="M110 74 q12 4 10 18" fill="none" stroke="#1e2b4a" stroke-width="5" stroke-linecap="round"/>'
        ),
        # 가슴께에 큰 엽전
        "prop": (
            f'<circle cx="80" cy="158" r="13" fill="#d9b45a" {LINE}/>'
            f'<rect x="75" y="153" width="10" height="10" fill="#efe7d4" {LINE}/>'
        ),
    },
}


def portrait_svg(kind: str, title: str) -> str:
    p = PORTRAIT_PARTS[kind]
    return (
        f'<svg viewBox="0 0 160 184" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title} 초상화">'
        f'{p["behind"]}'
        f'<path d="M26 184 Q28 136 80 126 Q132 136 134 184 Z" fill="{p["robe"]}" {LINE}/>'
        f'<path d="M66 128 L80 150 L94 128" fill="none" {LINE}/>'
        f'<circle cx="80" cy="98" r="28" fill="{SKIN}" {LINE}/>'
        f'{p["eyes"]}'
        f'<circle cx="62" cy="106" r="5" fill="{BLUSH}" opacity="0.55"/>'
        f'<circle cx="98" cy="106" r="5" fill="{BLUSH}" opacity="0.55"/>'
        f'<path d="M74 110 q6 5 12 0" fill="none" {LINE}/>'
        f'{p["extra_face"]}{p["hat"]}{p["prop"]}'
        "</svg>"
    )


def wealth_tier(coin: int) -> str:
    if coin < 0:
        return "객주에 빚 문서가 남은 살림"
    if coin <= 60:
        return "바닥이 보이는 엽전 꾸러미"
    if coin <= 150:
        return "소박하지만 굶지는 않는 살림"
    if coin <= 250:
        return "넉넉한 곳간"
    return "만석꾼 부럽지 않은 금고"


# ──────────────────────────────────────────────
# 상태: 고른 선택지 번호를 순서대로 쌓는 '장부(history)' 하나로 관리
# ──────────────────────────────────────────────
st.session_state.setdefault("history", [])
history = st.session_state.history


def entry(i: int, choice: int) -> dict:
    return QUESTIONS[i]["options"][choice]


def balance(hist: list) -> int:
    return START_COIN + sum(entry(i, c)["coin"] for i, c in enumerate(hist))


def signed(n: int) -> str:
    return f"+{n}" if n > 0 else str(n)


def money(n: int) -> str:
    cls = " class='neg'" if n < 0 else ""
    return f"<span{cls}>{n:,}냥</span>"


# ──────────────────────────────────────────────
# 장부 머리 (두 화면 공통)
# ──────────────────────────────────────────────
done = len(history) >= len(QUESTIONS)

html(
    f"""
    <div class="book-head">
    <div>
    <div class="book-title" role="heading" aria-level="1">조선 전생 장부</div>
    <div class="book-lede">{"한 해 장부를 다 적었습니다. 마지막 잔액과 씀씀이로 전생의 신분을 가려 보았어요."
        if done else "물려받은 밑천 100냥으로 열두 장을 살아 보세요. 고르는 대로 엽전이 들고 납니다."}</div>
    </div>
    </div>
    <div class="book-rule"></div>
    """
)

# ──────────────────────────────────────────────
# 문항 화면
# ──────────────────────────────────────────────
if not done:
    idx = len(history)
    q = QUESTIONS[idx]
    coins = "".join(
        f"<span class='coin {'done' if i < idx else 'now' if i == idx else ''}'></span>"
        for i in range(len(QUESTIONS))
    )

    last = ""
    if history:
        prev = entry(idx - 1, history[-1])
        cls = " class='neg'" if prev["coin"] < 0 else ""
        last = (
            f"<div class='last-line'><span>지난 줄: {prev['memo']}</span>"
            f"<b{cls}>{signed(prev['coin'])}냥</b></div>"
        )

    html(
        f"""
        <div class="progress-row">
        <div class="coins" role="img" aria-label="{len(QUESTIONS)}장 중 {idx}장 적음">{coins}</div>
        <div class="purse"><div class="k">지금 잔액</div><div class="v">{money(balance(history))}</div></div>
        </div>
        {last}
        <div class="chapter">제{idx + 1}장, {q['scene']}</div>
        <div class="prompt">{q['prompt']}</div>
        """
    )

    # 고르면 바로 다음 장으로 넘어간다
    for i, opt in enumerate(q["options"]):
        if st.button(opt["text"], key=f"pick_{idx}_{i}", use_container_width=True):
            history.append(i)
            st.rerun()

    if history and st.button("방금 적은 줄 지우기", key="undo"):
        history.pop()
        st.rerun()

# ──────────────────────────────────────────────
# 결과 화면
# ──────────────────────────────────────────────
else:
    def lean_sum(axis: str) -> int:
        return sum(entry(i, c)["lean"] for i, c in enumerate(history) if QUESTIONS[i]["axis"] == axis)

    def axis_size(axis: str) -> int:
        return sum(1 for q in QUESTIONS if q["axis"] == axis)

    risk, spend = lean_sum("risk"), lean_sum("spend")
    t = TYPES[("모험" if risk > 0 else "안전", "씀씀이" if spend > 0 else "절약")]
    final = balance(history)

    def scale(left: str, right: str, score: int, total: int) -> str:
        pos = (score + total) / (2 * total) * 100
        return (
            f"<div class='scale' role='img' aria-label='{left}과 {right} 사이 {pos:.0f}% 지점'>"
            f"<div class='ends'><span>{left}</span><span>{right}</span></div>"
            f"<div class='beam'><div class='knob' style='left:calc(11px + (100% - 22px) * {pos / 100:.3f})'></div></div></div>"
        )

    rows, running = [], START_COIN
    for i, c in enumerate(history):
        opt = entry(i, c)
        running += opt["coin"]
        amount_cls = "num neg" if opt["coin"] < 0 else "num"
        bal_cls = "num neg" if running < 0 else "num"
        rows.append(
            f"<tr><td class='when'>{QUESTIONS[i]['scene']}</td><td>{opt['memo']}</td>"
            f"<td class='{amount_cls}'>{signed(opt['coin'])}</td><td class='{bal_cls}'>{running:,}</td></tr>"
        )

    html(
        f"""
        <div class="verdict">
        <div class="portrait">{portrait_svg(t['portrait'], t['title'])}
        <div class="seal" aria-hidden="true">{"".join(f"<span>{ch}</span>" for ch in t['seal'])}</div>
        </div>
        <div>
        <div class="pre">전생의 당신은</div>
        <div class="name">{t['title']}</div>
        <div class="sub">{t['sub']}</div>
        </div>
        </div>
        <div class="total"><span class="k">한 해 마감 잔액</span><span class="v">{money(final)}</span></div>
        <div class="tier">시작 밑천 {START_COIN}냥에서 {signed(final - START_COIN)}냥. {wealth_tier(final)}입니다.</div>
        <div class="h">두 갈래 저울</div>
        {scale("안전", "모험", risk, axis_size("risk"))}
        {scale("절약", "씀씀이", spend, axis_size("spend"))}
        <div class="h">전생 이야기</div>
        <div class="story">{t['desc']}</div>
        <div class="note"><b>덧붙임</b>{t['tip']}</div>
        <div class="h">한 해 장부</div>
        <div class="ledger-wrap"><table class="ledger">
        <tr><th>때와 곳</th><th>적요</th><th class="num">들고 남</th><th class="num">잔액</th></tr>
        <tr><td class='when'>시작</td><td>물려받은 밑천</td><td class='num'>+{START_COIN}</td><td class='num'>{START_COIN}</td></tr>
        {"".join(rows)}
        <tr class="sum"><td colspan="3">합계</td><td class="num {'neg' if final < 0 else ''}">{final:,}</td></tr>
        </table></div>
        """
    )

    st.write("")
    if st.button("새 장부로 다시 하기", key="restart"):
        st.session_state.history = []
        st.rerun()
