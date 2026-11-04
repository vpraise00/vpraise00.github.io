"""Verified editorial seed reviews. Statements are attributed to paper abstracts.

Run only to rebuild the seed library from scratch (normally not needed).
The daily updater preserves existing editorial entries and never overwrites reviews.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = []

def add(id, title, authors, published, primary, tags, summary, problem, idea, method, findings, limitations, questions, *, featured=False, project='', code='', reading_minutes=8, abstract='', categories=None):
    P.append({
        'id': id, 'slug': id, 'title': title, 'authors': authors, 'published': published,
        'updated': published, 'primary_category': primary,
        'categories': categories or [primary], 'tags': tags, 'featured': featured,
        'curated': True, 'summary_ko': summary,
        'abstract': abstract or ('원문의 핵심 내용을 한국어로 재구성한 큐레이션 요약입니다. 정확한 실험 조건과 수치는 원문을 확인하세요. '+summary),
        'review': {'one_line': summary, 'problem': problem, 'idea': idea, 'method': method,
                   'findings': findings, 'limitations': limitations, 'questions': questions,
                   'source_scope': 'abstract+official sources', 'generated_by': 'editorial'},
        'source_url': f'https://arxiv.org/abs/{id}', 'pdf_url': f'https://arxiv.org/pdf/{id}',
        'project_url': project, 'code_url': code, 'reading_minutes': reading_minutes,
        'origin': 'curated'
    })

add('2610.42021', 'Nexus-VLA: Bridging Human and Robot Experiences via a Shared Hierarchical Semantic Latent Space',
    ['Biaoliang Guan', 'Tingyu Yuan', 'Wen Ye', 'et al.'], '2026-10-30', 'vla',
    ['Cross-Embodiment', 'Human Video', 'Manipulation'],
    '사람의 1인칭 조작 영상과 로봇 시연을 계층적 의미 공간에서 정렬해 실제 로봇 행동 학습에 연결한 VLA.',
    '사람 영상은 풍부하지만 사람과 로봇은 외형, 관절 구조, 행동 공간이 다릅니다. 기존 접근은 이 간극을 줄이는 표현 학습과 로봇 정책 학습을 따로 수행해 사람 데이터가 제어기에 충분히 기여하지 못한다는 점을 문제로 삼습니다.',
    '작업 의도부터 세밀한 접촉·상호작용까지 여러 수준의 공통 의미를 계층적으로 정렬합니다. 이 공유 표현을 최종 행동 예측 경로에 직접 넣어 인간 경험이 정책 학습 손실에 연결되도록 구성합니다.',
    '인간 영상과 로봇 데이터를 공동 학습하며, 다층 의미 정렬을 통해 공통 잠재 표현을 학습합니다. 잠재 표현이 연속 행동 생성의 조건으로 활용되기 때문에 단순히 사전학습 특징만 빌려오는 구성과 다릅니다.',
    '논문 초록은 RoboCasa-GR1에서 80.5%의 과제 성공률을 보고하며, OOD 설정과 실제 로봇 실험에서도 데이터 활용 효율·일반화 이점을 주장합니다. 실험 조건이 다른 수치와 직접 비교되지 않도록 주의해야 합니다.',
    '정렬된 잠재 공간이 새로운 로봇 형태나 극단적인 시점 변화에서도 안정적인지는 추가 검증이 필요합니다. 초록만으로 데이터 규모, 계산 비용, 모든 비교군의 공정성을 판단하기 어렵습니다.',
    ['공통 잠재 변수는 어떤 행동 자유도까지 보존하는가?', '인간 영상 비중을 늘릴 때 언제 성능이 포화되는가?', 'RoboCasa-GR1 성능이 실제 장기 과제로 얼마나 이전되는가?'], featured=True, reading_minutes=9)

add('2610.40373', 'HiFOR: Hierarchical Foresight with Action-Guided World Grounding for Vision-Language-Action Model',
    ['Rongxing Ding', 'Hongyu Qu', 'Kehong Wu', 'et al.'], '2026-10-29', 'vla',
    ['World Grounding', 'Planning', 'Manipulation'],
    '단기 상태 변화·중간 의미 목표·최종 목표를 함께 예측하고, 현재 행동 생성에 필요한 미래 정보만 선택적으로 참조.',
    '미래 예측을 VLA에 결합하는 연구는 많지만, 단기 물리 변화와 장기 목적을 별도로 다루거나 미래 표현 전체를 행동 정책에 무차별적으로 주입하기 쉽습니다. 실제 제어에는 현재 행동과 관련된 미래 정보만 필요한 경우가 있습니다.',
    '계층적 미래 예측(Hierarchical Foresight Prediction)과 행동 주도 검색(Action-Guided Retrieval)을 연결합니다. 미래를 미리 상상하는 데서 끝나지 않고, 행동을 생성하는 과정에서 필요한 지점의 정보를 다시 찾아 쓰는 구조입니다.',
    'Hierarchical Dependency Mask로 단기 상태, 중간 단계, 최종 목표 사이 의존관계를 모델링합니다. 미래 잠재 표현을 시간·시점·공간 축으로 구조화한 뒤, 디노이징 중 변하는 행동 표현을 쿼리로 사용해 필요한 예측 정보를 검색합니다.',
    '초록 기준 두 개의 시뮬레이션 벤치마크와 실제 조작 과제 6개에서 접근법의 유효성을 검증했다고 보고합니다. 구체적 성공률과 환경별 비교표는 본문을 참고해야 합니다.',
    '미래 표현을 계산·저장·검색하는 과정이 실시간 제어 지연을 얼마나 늘리는지 확인해야 합니다. 긴 작업에서 오예측이 누적될 가능성도 남습니다.',
    ['예측이 틀릴 때 retrieval은 오히려 정책을 방해하지 않는가?', '시간·공간 축 구조화의 개별 기여도는?', '실제 제어 지연이 허용 범위에 드는가?'], featured=True, reading_minutes=9)

add('2610.40026', 'RoboSeed: Multidimensional Evaluation of Vision-Language-Action and World-Action Models',
    ['Xin Ma', 'Furong Chen', 'Xinlong Man', 'et al.'], '2026-10-29', 'robotics',
    ['Evaluation', 'Benchmark', 'Reproducibility'],
    '성공률만으로 VLA·WAM을 줄 세우지 않고 학습비용·추론비용·재현 근거까지 다섯 축으로 검토하는 평가 프레임워크.',
    '성공률 1개의 숫자로 모델을 선택하면 파인튜닝 비용, 서버 운영비, 실험 재현성, 언어/시각 입력 조건을 간과할 수 있습니다. 예산과 실제 배치 조건이 다른 연구자에게 같은 순위를 적용하기 어렵습니다.',
    '모델 선택을 능력, 후속 학습 부담, 배포 부담, 직접 확인한 연구 가치, 재현 증거의 다차원 프로필 문제로 전환합니다. 균형형·훈련제약형·배포제약형 사용자 선호도도 따로 정의합니다.',
    '서로 비교 가능한 인터페이스와 프로토콜을 먼저 검사하고, 고정된 정규화 기준으로 개별 축을 0~100으로 표현합니다. 결측 측정은 감추지 않고 측정 범위를 따로 표시하며, 불완전한 총점은 산출하지 않습니다.',
    '대표 VLA 및 WAM에 적용했을 때 예산에 따라 유리한 모델 선택이 달라지고 학습 레시피의 영향이 크다고 설명합니다. **논문은 자료가 불완전하므로 단일 종합 순위를 제시하지 않습니다.**',
    '지표 정규화의 기준점과 개별 사용자 가중치에 따라 결론이 달라질 수 있습니다. 이 프레임워크 자체가 새로운 정책 성능 향상을 보장하는 것은 아닙니다.',
    ['우리 GPU 예산으로 환산하면 우선순위가 어떻게 달라지나?', '측정하지 않은 지표를 어떻게 보수적으로 취급할까?', 'LIBERO와 실제 로봇 결과를 같은 차트로 비교해도 되는가?'], featured=True, reading_minutes=8)

add('2610.07922', 'OpenWAM: An Open Framework for Composable World-Action Models',
    ['Heng Yu', 'David D. Yuan', 'Juze Zhang', 'et al.'], '2026-10-06', 'wam',
    ['World Model', 'Video Prediction', 'Action Expert'],
    '공통 비디오 백본 위에서 비디오와 행동의 생성 순서·결합 방식을 실험할 수 있는 조립형 WAM 프레임워크.',
    'WAM 논문들은 비디오 예측 모델, 행동 정책, 학습 감독, 추론 순서를 한꺼번에 바꾸는 일이 많아 무엇이 성능에 기여했는지 비교하기 어렵습니다. 동일 기반에서 결합 방식만 바꾸는 실험장이 필요합니다.',
    '공통 인과적 로봇 비디오 모델 위에 action expert를 붙이고, 비디오-행동 동시 생성, 비디오 선행, 행동 선행, 분리 생성 등을 공통 프레임에서 비교하도록 만듭니다.',
    'Wan2.2-5B에서 시작해 1만 시간 이상의 로봇 비디오로 causal pretraining을 수행합니다. Shared Mixture-of-Transformers 구성에서 비디오 생성과 행동 생성을 조합하고, inverse/forward dynamics 및 반사실적(counterfactual) 전이를 분석합니다.',
    '초록은 LIBERO-Long의 VTA 성공률이 causal video 학습 후 68.4%에서 97.8%로 상승했다고 보고합니다. 별도 held-out LIBERO-90 네 과제에서 counterfactual 학습을 쓴 local-context inverse dynamics가 평균 84.0% 성공률을 보인다고 설명합니다.',
    '비디오 생성의 계산비용과 지연시간이 실제 하드웨어 배치에 중요한 변수입니다. 1만 시간 이상의 비디오·대형 백본 사용은 소형 연구실의 재현 부담을 높일 수 있습니다.',
    ['joint와 video→action 중 특정 지연 제약에서 무엇이 유리한가?', '반사실적 데이터가 관측 불가능한 물리 변수에도 도움이 되는가?', '영상 품질과 제어 성공률은 어느 정도 상관하는가?'], featured=True, project='https://openwam.stanford.edu/', reading_minutes=11, categories=['wam','vla'])

add('2609.23578', 'AR-WAM: A Visual-Conditioned Agent-Ready World Action Model for Robotic Manipulation',
    ['Yicheng Jiang', 'Zesen Gan', 'Xiaobo Wang', 'et al.'], '2026-09-20', 'wam',
    ['Agent Control', 'Visual Grounding', 'Long Horizon'],
    '자연어 대신 바운딩 박스와 동작 토큰으로 로봇을 제어해 에이전트-로봇 연결을 단순화한 경량 WAM.',
    '상위 AI 에이전트가 이미 언어를 처리하는데 로봇 정책까지 긴 언어 지시를 반복 처리하면 참조가 모호해지고 공간 지시가 부정확할 수 있습니다. 어떤 물체를 어떤 기술로 조작할지 더 직접적인 인터페이스가 필요합니다.',
    '목표 객체를 지정하는 시각적 바운딩 박스와 원자적 조작을 지정하는 학습 가능한 operation token을 결합합니다. 상위 에이전트는 감지·실행·조회라는 세 가지 도구 인터페이스로 이 모델을 호출합니다.',
    '고정된 비전 인코더를 사용한 0.5B 정책이 작은 잠재 공간에서 장면 변화를 예측하며 행동을 디코딩합니다. 긴 문맥 기억과 에러 복구는 상위 에이전트가 담당해 정책과 계획의 책임을 나눕니다.',
    'RoboTwin 2.0, RMBench, 실제 듀얼암 플랫폼에서 평가하고, 초록은 일반 조작 평균 성공률 87.2%, 추론 지연 14.1ms를 제시합니다. 장기 작업에서의 개선도 주장하지만 비교 조건은 본문 확인이 필요합니다.',
    '바운딩 박스 탐지기와 상위 에이전트가 틀리면 정책 자체가 좋아도 실패할 수 있습니다. 언어 대신 시각 프롬프트가 항상 정보 손실이 적다는 뜻은 아닙니다.',
    ['detect→execute 루프에서 실패 회복은 어떻게 이뤄지나?', '복잡한 복합 지시를 operation token으로 충분히 표현하나?', '상위 에이전트 모델이 바뀌어도 비교 가능한가?'], reading_minutes=9)

add('2609.19600', 'WorldContact: A Contact-Centric World Model for Scalable Robot Learning',
    ['Caoliwen Wang', 'Mengdi Wang', 'Heng Zhang', 'et al.'], '2026-09-17', 'robotics',
    ['Contact-Rich', 'World Model', 'Sim2Real'],
    '변형 가능한 물체의 접촉 역학을 학습한 world model로 데이터를 확장하고 실제 로봇 조작 정책을 개선.',
    '봉투처럼 변형되는 물체는 고정 강체보다 접촉·마찰·변형의 계산이 어렵습니다. 정밀 시뮬레이션만으로 학습 데이터를 대량 생성하려면 많은 계산이 필요합니다.',
    '품질 높은 소수의 시연으로 접촉 중심 월드 모델을 학습한 후 빠른 rollout으로 시연 데이터를 확장합니다. 모델을 평가하는 것뿐 아니라 생성 데이터를 정책 학습에 실제 활용합니다.',
    '변형 물체의 동역학을 원본 수치 시뮬레이터보다 큰 시간 간격으로 예측하고, 이를 기반으로 조작 데이터를 만들어 기존 VLA를 파인튜닝합니다. 실제 쇼핑백 리프팅 문제로 배포 성능을 확인합니다.',
    '16개 쇼핑백 조작 과제에서 분석하며, 단일 H100의 상태 rollout이 원본 시뮬레이터보다 10배 빠르다고 보고합니다(렌더링·디스크 I/O 제외). 실제 봉투 들기 단회 성공률은 원본 시뮬 데이터만 쓸 때 65%, 모델 확장 데이터를 쓸 때 95%입니다.',
    '10배는 전체 학습·렌더링 파이프라인 속도를 의미하지 않습니다. 다른 물성이나 새로운 형태의 변형 물체에 그대로 적용할 수 있는지는 별도로 확인해야 합니다.',
    ['원본 시연 데이터가 얼마까지 줄어도 도움이 되나?', '다른 형태의 deformable object로 일반화 가능한가?', '모델 편향이 늘어날 때 정책은 어떤 실패를 보이는가?'], reading_minutes=9)

add('2609.16074', 'World-Action Models for Robot Learning and Control: A Survey',
    ['Zuxing Lu', 'Hongjia Zhai', 'Guanzhi Wang', 'et al.'], '2026-09-13', 'wam',
    ['Survey', 'Taxonomy', 'World Model'],
    '기존 world model, action-conditioned video, 반응형 VLA와 WAM의 경계를 정리한 로보틱스 중심 서베이.',
    '상태를 예측하는 world model과 직접 행동을 출력하는 VLA 사이의 연결이 다양해지면서 무엇을 WAM이라 부를지 불분명해졌습니다. 논문 비교를 위해 설계 축과 용어를 정리할 필요가 있습니다.',
    '미래 세계의 예측과 실행 가능한 행동 생성의 결합을 WAM의 핵심으로 보고, 예측 표현·행동 결합 방식·데이터·학습·평가를 통합 분류 체계로 정리합니다.',
    '표현 공간, 전이 모델, 액션 인터페이스, 아키텍처, 학습 파이프라인, 데이터 유형, 스케일링 전략과 평가 프로토콜을 다룹니다. 조작·내비게이션·자율주행의 사례를 모아 공통 설계 문제를 비교합니다.',
    '특정 새 모델의 성공률을 높이는 실험 논문이 아니라 분야를 정리하는 참고 서베이입니다. 연구 방향으로 action alignment, 공간·다시점 일관성, 긴 시간 기억, 온라인 추론 효율 등을 강조합니다.',
    '서베이의 분류 기준과 포함 범위는 작성 시점의 연구 지형에 의존합니다. 신생 모델을 분류할 때는 원문 정의와 공개 증거를 다시 확인해야 합니다.',
    ['내가 보는 VLA가 진짜 WAM인가?', '예측 품질과 제어 성능을 함께 평가하는 실험은?', 'joint 예측과 cascade 예측을 어떻게 비교할까?'], featured=True, project='https://rcl-robotics.github.io/Awesome-World-Action-Models/', reading_minutes=12)

add('2608.01397', 'SG-WAM: Self-Guided World Modeling in Geometry-Aware Policy Space',
    ['Ruiteng Zhao', 'Zhengshen Zhang', 'Yue Su', 'et al.'], '2026-08-02', 'wam',
    ['Geometry-Aware', 'Latent Dynamics', 'Flow Matching'],
    '행동 정책 자체의 표현 공간에서 기하 정보를 지닌 미래 잠재 상태를 예측하도록 공동 학습한 WAM.',
    '미래 상태 예측이 아무리 정확해도 그 표현이 로봇 정책의 행동 결정과 어긋나면 제어에 도움이 덜 될 수 있습니다. 또한 객체 위치·기하 구조를 잃은 잠재 예측은 조작에 취약합니다.',
    '정책 백본에서 나온 표현 공간에 dynamics token을 두고, EMA 복제 정책이 만든 목표 특징으로 미래를 예측합니다. 공간적 기하 감독을 함께 넣어 행동과 지각이 공유하는 표현을 만듭니다.',
    'Self-Guided World Predictor가 로봇 행동을 조건으로 미래 잠재 토큰을 예측합니다. 지오메트리 감독을 받은 이미지 토큰, 잠재 미래 예측, flow-matching 행동 생성을 end-to-end로 공동 최적화합니다.',
    '초록은 대규모 embodied 사전학습 없이 0.9B 구성으로 LIBERO 평균 98.5%, LIBERO-Plus 73%를 보고합니다. 이는 해당 평가 프로토콜 조건의 성능이지 모든 로봇 환경에서의 성공률은 아닙니다.',
    'EMA 목표 특징의 품질이 데이터 도메인 밖에서 떨어질 수 있습니다. 공간 감독에 필요한 데이터와 그 비용, 실제 로봇에서의 안전한 폐루프성 평가가 중요한 후속 문제입니다.',
    ['기하 감독 없이도 예측 성능이 유지되나?', '단기 잠재 예측이 긴 작업 계획에 충분한가?', '소형 모델 스케일의 이점은 추론 지연에서도 유효한가?'], featured=True, reading_minutes=9)

add('2605.00080', 'World Model for Robot Learning: A Comprehensive Survey',
    ['Bohan Hou', 'Gen Li', 'Jindou Jia', 'et al.'], '2026-04-30', 'robotics',
    ['Survey', 'Policy Learning', 'Simulation'],
    '월드 모델을 정책 학습·시뮬레이션·평가·데이터 생성 관점에서 총정리한 로봇 학습 서베이.',
    '월드 모델이라는 용어가 잠재 동역학, 비디오 생성, 학습된 시뮬레이터, 계획 모듈 등 다양한 시스템에 쓰이면서 논문 사이의 역할 구분이 어려워졌습니다.',
    '월드 모델을 그 자체의 예측 정확도뿐 아니라 정책과 어떻게 결합해 로봇 학습에 기여하는지에 따라 바라보는 관점을 제시합니다.',
    '정책 결합 방식, 강화학습용 학습된 시뮬레이터, 대규모 비디오 월드 모델, 내비게이션 및 자율주행까지 주요 흐름을 체계적으로 검토합니다. 평가 지표와 벤치마크의 차이도 정리합니다.',
    '새 모델의 실험 성과가 아니라 기존 연구의 체계적 지도 역할을 합니다. 후속 연구를 시작할 때 predictive model을 어디에 쓰는지 구분하는 기준을 제공합니다.',
    '다루는 범위가 넓어 개별 시스템의 구현 디테일은 원논문으로 보완해야 합니다. 서베이의 최신성은 지속적으로 갱신되는 저장소를 통해 확인하는 편이 좋습니다.',
    ['정책 학습용 시뮬레이터와 온라인 계획용 월드 모델은 어떻게 다를까?', 'closed-loop 성공률과 video quality 중 어느 지표를 우선할까?', '월드 모델이 실패할 때 정책도 실패하는가?'], reading_minutes=12,
    project='https://ntumars.github.io/wm-robot-survey/')

add('2504.16054', 'π0.5: a Vision-Language-Action Model with Open-World Generalization',
    ['Kevin Black', 'Noah Brown', 'James Darpinian', 'et al.'], '2025-04-22', 'vla',
    ['Generalization', 'Co-training', 'Long Horizon'],
    '여러 로봇·웹 데이터·하위 과제 예측을 함께 학습해 처음 방문한 실제 집에서도 긴 조작 과제를 수행하도록 설계.',
    '시연 데이터와 비슷한 실험실 상황을 잘 처리해도, 처음 보는 집·물체·배치를 마주하면 범용 로봇이 실패할 수 있습니다. 새로운 환경으로의 일반화가 핵심 문제입니다.',
    'π0 기반의 연속 행동 정책을 유지하면서 로봇 시연, 웹 시각·언어 데이터, 물체 탐지, 고수준 하위 과제 예측 등을 함께 학습합니다. 고수준 의미와 저수준 모터 제어를 분리하지 않고 연결합니다.',
    '이질적인 다중모달 예시를 co-training에 섞어 의미 지식과 조작 기술을 전달합니다. 신규 집안의 부엌 정리·방 청소 등 장기 작업에서 고수준 판단과 행동 생성이 연결됩니다.',
    '논문은 학습에 포함되지 않은 실제 가정에서 정리·청소 같은 장기·정밀 과제를 시연했다고 보고합니다. 이는 일반화에 대한 중요한 증거지만 모든 가정·로봇에서의 완전한 견고성을 뜻하지 않습니다.',
    '작업 성공 판정 기준, 실패 빈도, 사용자 개입, 학습 데이터와 테스트 환경의 중복 가능성 등을 함께 읽어야 합니다. 자료의 종류가 다양해 개별 요소의 기여도를 분리하기 어렵습니다.',
    ['고수준 하위 과제 예측을 제거해도 같은 일반화가 유지되나?', '새 물체와 새 공간 중 어디에서 가장 많이 실패하나?', '데이터 배합 비율의 변화가 정책에 어떤 영향을 주는가?'], featured=True, project='https://www.pi.website/blog/pi05', code='https://github.com/Physical-Intelligence/openpi', reading_minutes=10)

add('2503.14734', 'GR00T N1: An Open Foundation Model for Generalist Humanoid Robots',
    ['Johan Bjorck', 'Fernando Castañeda', 'NVIDIA team', 'et al.'], '2025-03-18', 'robotics',
    ['Humanoid', 'Dual-System', 'Diffusion'],
    '상황 이해(System 2)와 연속 동작 생성(System 1)을 나눠 구성한 공개 휴머노이드 기초 정책.',
    '휴머노이드 제어는 팔의 조작뿐 아니라 다양한 센서와 형태, 현실 변화에 대응해야 합니다. 단일 로봇 과제에만 맞춘 imitation learning으로는 범용성이 제한됩니다.',
    '언어·영상 해석 모듈(System 2)과 확산 트랜스포머 기반의 모터 행동 모듈(System 1)을 연결해 고수준 지시부터 연속 제어까지 함께 학습합니다.',
    '실제 로봇 궤적, 인간 영상, 합성 데이터의 이질적 혼합으로 사전학습합니다. 여러 로봇 형태의 벤치마크와 Fourier GR-1의 양팔 조작 사례를 통해 범용 기반 정책의 가능성을 평가합니다.',
    '원문은 기존 imitation learning 베이스라인 대비 시뮬레이션 성능의 우위와 실제 휴머노이드 양팔 조작 사례를 보고합니다. 이후 N1.7 등 제품 버전과 이 최초 논문 성과는 구분해 읽어야 합니다.',
    '형태별 제어 주기, 센서 구성, 데이터 분포가 달라지면 실제 성능도 달라집니다. 휴머노이드의 보행·균형까지 모두 해결됐다는 뜻은 아닙니다.',
    ['System 2와 System 1의 업데이트 주기는?', '새 로봇 embodiment 전환 시 어떤 파라미터를 조정하나?', '실제 배치에서 안전 계층을 어떻게 구성할까?'], code='https://github.com/NVIDIA/Isaac-GR00T', reading_minutes=10)

add('2502.05855', 'DexVLA: Vision-Language Model with Plug-In Diffusion Expert for General Robot Control',
    ['Junjie Wen', 'Yichen Zhu', 'Jinming Li', 'et al.'], '2025-02-09', 'vla',
    ['Dexterous', 'Diffusion', 'Cross-Embodiment'],
    '1B 규모의 별도 diffusion action expert와 단계적 embodiment curriculum을 사용한 정밀 조작 VLA.',
    'VLA 연구가 VLM의 크기를 키우는 데 집중하는 동안, 연속 행동 공간과 데이터·로봇 형태 차이는 조작 성능의 병목으로 남아 있습니다.',
    '시각·언어 모델과 결합할 수 있는 큰 diffusion action expert를 별도로 학습하고, 다양한 robot embodiment에서 학습한 모터 기술을 새로운 환경에 적응시킵니다.',
    '먼저 cross-embodiment 데이터로 diffusion expert를 사전학습하고, 특정 로봇과 VLA를 정렬한 후 과제별 post-training을 수행합니다. 단팔, 양팔, dexterous hand 등을 대상으로 시험합니다.',
    '초록은 Octo·OpenVLA·Diffusion Policy 같은 비교군보다 높은 성능을 보고하며, 빨래 접기 같은 긴 과제에서 언어 지시만으로 동작을 수행한 사례를 제시합니다.',
    '액션 expert를 크게 키우면 데이터·계산량 부담도 증가합니다. 비교군의 모델 용량과 사전학습 데이터 범위, 과제 난이도를 공정하게 확인해야 합니다.',
    ['diffusion expert 사전학습만으로 얼마나 전이되나?', '신규 로봇에서는 VLM과 action expert 중 어디를 고쳐야 하나?', '추론 속도와 정밀도 사이의 절충은?'], reading_minutes=9)

add('2410.24164', 'π0: A Vision-Language-Action Flow Model for General Robot Control',
    ['Kevin Black', 'Noah Brown', 'Danny Driess', 'et al.'], '2024-10-31', 'vla',
    ['Flow Matching', 'Generalist Policy', 'Manipulation'],
    '사전학습 VLM 위에 flow-matching 기반 연속 행동 생성기를 결합한 범용 로봇 제어의 핵심 기반 연구.',
    '기존 언어 모델 토큰화 방식은 로봇의 부드러운 고주파 연속 제어에 적합하지 않을 수 있습니다. 또한 단일 로봇의 시연만으로는 넓은 조작 기술을 학습하기 어렵습니다.',
    '인터넷 규모의 시각·언어 의미 지식을 가진 VLM과 연속 제어 궤적을 생성하는 flow-matching action head를 결합합니다. 의미 이해와 모터 제어의 다른 요구를 각각 반영합니다.',
    '단팔, 양팔, 모바일 매니퓰레이터의 데이터를 함께 학습합니다. 명령을 직접 따르거나 상위 VLM의 하위 지시를 실행하고, 새로운 작업을 파인튜닝으로 습득하도록 평가합니다.',
    '논문은 빨래 접기, 탁자 청소, 상자 조립 등 다양한 조작 시연을 제시합니다. 이후 π0.5 계열 논문을 읽을 때 연속 action expert의 기반 아키텍처로 이해하면 좋습니다.',
    '다양한 하드웨어 행동 공간을 통일하는 표준화가 중요하며, 훈련·추론 비용과 긴 작업 중 에러 회복은 별도 과제입니다.',
    ['flow matching과 diffusion policy의 제어 안정성은 어떻게 비교되나?', 'action chunk 길이가 반응성에 미치는 영향은?', '정밀 접촉 동작에서 정책 지연을 어떻게 줄일까?'], featured=True, code='https://github.com/Physical-Intelligence/openpi', reading_minutes=10)

add('2406.09246', 'OpenVLA: An Open-Source Vision-Language-Action Model',
    ['Moo Jin Kim', 'Karl Pertsch', 'Siddharth Karamcheti', 'et al.'], '2024-06-13', 'vla',
    ['Open Source', 'Fine-tuning', 'Baseline'],
    '97만 실제 로봇 시연으로 학습한 공개 7B VLA로, 후속 연구의 재현 가능한 대표 베이스라인.',
    'VLA의 잠재력과 달리 기존 고성능 모델들은 폐쇄형이거나 새로운 환경에 맞게 쉽게 파인튜닝할 수 없었습니다. 연구 재현성과 확장성이 중요한 문제였습니다.',
    'Llama 2 언어 모델에 DINOv2와 SigLIP 특징을 결합한 비전 인코더를 붙이고, 로봇 행동을 출력하는 공개 VLA를 구축합니다.',
    '다양한 실제 로봇 시연 약 97만 개로 7B 정책을 학습합니다. 다양한 조작 과제의 zero-shot 및 파인튜닝 결과를 공개하고 LoRA와 양자화 등 자원 절약 방법도 실험합니다.',
    '논문은 29개 과제에서 RT-2-X(55B)보다 절대 성공률 16.5%p 높았다고 보고합니다(해당 실험 프로토콜 기준). 공개 코드와 체크포인트가 있어 재현·확장 연구에 유리합니다.',
    '행동 토큰화의 분해능, 데이터 분포와 다른 하드웨어에 대한 이전성, 정밀한 접촉 제어는 지속적인 개선 대상입니다. 최신 모델과의 비교에선 평가 프로토콜의 동등성이 핵심입니다.',
    ['LoRA로 적응할 때 어느 계층을 업데이트해야 하나?', '행동 토큰화가 연속 제어에 주는 한계는?', '다른 입력 카메라 구성에서 얼마나 강건한가?'], featured=True, code='https://github.com/openvla/openvla', reading_minutes=10)

add('2405.12213', 'Octo: An Open-Source Generalist Robot Policy',
    ['Dibya Ghosh', 'Homer Walke', 'Karl Pertsch', 'et al.'], '2024-05-20', 'robotics',
    ['Generalist Policy', 'Open-X', 'Transfer'],
    '80만 로봇 궤적으로 학습하고 새 센서·로봇 동작 공간에 빠르게 적응하도록 설계한 공개 일반 정책.',
    '로봇 정책을 폭넓게 재사용하려면 로봇마다 다른 카메라·센서 구성, 동작 공간, 목표 표현을 수용해야 합니다. 모델 자체뿐 아니라 실제 파인튜닝 편의성이 중요합니다.',
    '트랜스포머 기반의 일반 정책에 언어 지시와 목표 이미지를 모두 조건으로 넣고, 다양한 observation/action 인터페이스로 전이하기 쉽게 설계합니다.',
    'Open X-Embodiment 데이터의 약 80만 궤적으로 사전학습합니다. 새로운 로봇의 감각 입력과 동작 공간에 소비자급 GPU에서 수 시간 내 파인튜닝할 수 있음을 평가합니다.',
    '원문은 9개 로봇 플랫폼 실험에서 범용 초기화 정책의 유용성을 제시하고 모델 구조·학습 데이터 설계의 ablation을 제공합니다.',
    '관측과 행동의 정규화 및 하드웨어 인터페이스가 전이에 핵심입니다. 특수한 dexterous task는 추가적인 데이터와 정책 head가 필요할 수 있습니다.',
    ['새 센서에 맞춘 토큰 구성은 어떻게 바뀌나?', '목표 이미지 조건과 언어 조건은 언제 차이가 나는가?', '초기화 이점이 데이터가 많아져도 유지되나?'], code='https://github.com/octo-models/octo', reading_minutes=9)

add('2403.12945', 'DROID: A Large-Scale In-The-Wild Robot Manipulation Dataset',
    ['Alexander Khazatsky', 'Karl Pertsch', 'Suraj Nair', 'et al.'], '2024-03-19', 'robotics',
    ['Dataset', 'Real Robot', 'Generalization'],
    '다양한 실제 환경에서 모은 7.6만 시연·350시간 조작 데이터로 로봇 학습의 데이터 다양성 문제를 다룸.',
    '대규모 로봇 정책은 다양한 환경에서 시연이 필요하지만 하드웨어와 사람의 작업이 비싸고, 단일 연구실에서 만든 데이터는 상황 다양성이 부족하기 쉽습니다.',
    '여러 지역의 수집자가 동일한 조작 하드웨어 구성과 프로토콜로 광범위한 생활환경 데이터를 공동 수집하는 분산 로봇 데이터 구축 방법을 제시합니다.',
    '북미·아시아·유럽의 50명 수집자가 12개월 동안 564개 장면, 84개 과제를 대상으로 약 7.6만 궤적/350시간의 데이터를 수집했습니다. 정책 학습 및 재현용 하드웨어 문서를 공개합니다.',
    '연구는 DROID 데이터로 학습한 정책의 성능과 일반화 개선을 보고합니다. 수치가 아닌 다양한 환경과 수집 절차의 공개 자체도 중요한 기여입니다.',
    '지역과 하드웨어 구성이 다양해도 특정 그리퍼·제어 방식의 편향이 남을 수 있습니다. 새로운 데이터셋과 조합할 때 액션·시간 정렬과 데이터 라이선스를 확인해야 합니다.',
    ['우리 로봇의 action schema로 매핑하려면 무엇이 필요한가?', '장면 다양성과 과제 다양성 중 어디가 더 중요한가?', '고품질 시연을 자동으로 필터링할 수 있나?'], reading_minutes=9)

if __name__ == '__main__':
    target = ROOT / 'data' / 'papers.json'
    target.write_text(json.dumps({'last_checked': '2026-11-04T00:00:00Z', 'papers': P}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Seeded {len(P)} verified editorial articles in {target}')
