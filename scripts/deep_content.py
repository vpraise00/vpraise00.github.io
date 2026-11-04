"""Hand-edited, paper-specific Korean technical notes.

Sources: the corresponding arXiv paper abstracts and, where accessible, official
HTML/project pages. Editorial replication proposals are explicitly marked.
All numerical results below are paper-reported, NOT cross-paper rankings.
"""

D = {}

D['2610.42021'] = dict(
 lead='Nexus-VLA에서 중요한 질문은 “사람의 손동작을 로봇 관절값으로 어떻게 바꿀까?”보다 앞선다. 사람과 로봇이 공통으로 이해할 수 있는 **작업 의도·행동 단계·접촉 사건**의 의미 표현을 만들고, 그 표현이 실제 action 생성 손실에 영향을 주도록 만드는 것이다. 따라서 이 논문은 단순 비디오 사전학습보다 인간–로봇 표현 정렬과 제어의 end-to-end 결합에 초점을 둔다.',
 pipeline=[
  ('서로 다른 embodiment의 경험 모으기','사람의 egocentric 조작 영상과 로봇 시연을 병렬 학습 대상으로 준비한다. 사람 영상에는 로봇의 관절 위치나 gripper command가 없으므로 raw action label을 그대로 맞출 수 없다.','입력: 인간 영상 + 로봇 시각·행동 궤적'),
  ('여러 수준에서 공통 의미를 맞추기','거친 수준의 task intent에서 세밀한 interaction 수준까지 계층적으로 의미 정보를 정렬한다. 이는 같은 작업이라도 손의 형태·카메라 시점·운동학이 달라 보이는 문제를 줄이려는 선택이다.','중간 표현: hierarchical cross-embodiment semantics'),
  ('공유 잠재 공간으로 압축','정렬한 정보를 별개의 보조 과제 결과로 끝내지 않고 shared manipulation latent representation에 담는다. 인간 지식이 제어기 내부 경로에 들어간다는 점이 핵심이다.','표현: 공유 manipulation latent'),
  ('연속 로봇 action 생성','로봇 observation 및 공유 잠재 정보가 연속 행동 생성에 영향을 주도록 공동 훈련한다. 실제 제어 시 인간의 손 동작을 그대로 복제하는 것이 아니라 로봇 action space로 디코딩한다.','출력: robot-specific continuous actions')],
 mechanisms=[
  ('정렬과 행동 예측의 분리 문제','cross-embodiment alignment를 사전학습한 뒤 고정 encoder로 정책을 따로 학습하면, 최종 action loss가 어떤 의미 정보를 필요한지 되돌려주기 어렵다. Nexus-VLA는 shared latent를 action 생성 경로에 사용해 이 결합 문제를 겨냥한다.','정렬 목표의 성능만 보고 정책 개선을 추정하지 말고, joint training이 실제 성공률을 바꾸는지 보자.'),
  ('‘공통’과 ‘embodiment-specific’ 정보의 경계','물체를 집어 옮긴다는 의도는 공유되지만, gripper aperture·관절 제한·접근 궤적은 embodiment마다 다르다. 모든 정보를 억지로 하나의 latent에 집어넣으면 로봇 고유의 운동 제약을 지우는 위험이 있다.','latent가 보존해야 하는 것은 의도인지 접촉 상태인지, 혹은 동작의 시간적 구조인지 구분하자.'),
  ('데이터 이득의 원인 분리','인간 비디오를 추가한 효과와 계층적 감독 구조를 설계한 효과를 분리해 봐야 한다. 표현 구조 자체가 로봇 데이터만으로도 성능을 올릴 수 있기 때문이다.','robot-only → alignment-only → human+robot joint training의 ablation이 중요하다.')],
 evidence=[
  ('RoboCasa-GR1 성능','80.5% 성공률','저자들이 보고한 RoboCasa-GR1 과제 평가 결과. 벤치마크·checkpoint·태스크별 분포가 같이 제시되어야 해석 가능.'),
  ('일반화 평가','OOD + 실제 로봇 실험','초록은 추가 도메인과 실환경 결과를 보고하지만 일괄적인 개선 수치를 제시하지 않는다.'),
  ('사람 데이터 활용','학습 효율 개선 주장','공유 표현으로 인간 영상의 도움을 높였다는 주장. 데이터 수와 비교군의 학습 스텝을 함께 확인해야 한다.')],
 evidence_note='80.5%는 논문 내부 평가의 reported score이다. 성능 기여를 분석할 때 human video의 순수 효과와 구조 변경 효과를 별도로 확인하자.',
 comparison='일반적인 imitation learning은 로봇 action label이 있는 시연에 의존하고, 분리형 human-video representation learning은 사람 영상에서 배운 특징을 후속 정책에 간접 전달한다. Nexus-VLA는 **사람–로봇 공동 학습 + 계층적 의미 정렬 + 공유 latent를 연속 action 생성에 직접 연결**한다는 조합에서 차별화된다.',
 reading_guide=[
  '‘공유 latent’가 정확히 어느 위치에 들어가며 gradient가 인간 영상 경로까지 전달되는지 네트워크 그림을 확인하기.',
  '인간 영상에 부여한 라벨·의미 감독의 출처가 자동 추론인지 수작업인지 확인하기. 감독 비용은 데이터 효율의 일부다.',
  'robot-only / human-only / joint training의 성공률과 같은 학습 스텝·동일 로봇 데이터 사용 여부를 비교하기.',
  'OOD를 구분하는 축(물체, 시점, 공간, 로봇 형태)을 분리하고, 실패 유형이 어떤 정렬 단계에서 생기는지 보기.'],
 replication=dict(hypothesis='사람 영상을 단순 concatenation하는 것보다 **action-conditioned shared latent**로 정렬할 때 새 물체·시점에서 성공률이 높아질 것이다.',setup='RoboCasa 또는 RoboTwin의 동일 task subset을 고정하고 robot demonstration 양을 100/50/25%로 줄인다. 이에 상응하는 egocentric human video를 0/소/대로 늘려 학습곡선을 기록한다.',baselines='robot-only VLA, freeze된 human-video encoder 결합, joint training만 한 모델, full hierarchical alignment. backbone·action head·총 업데이트 수는 맞춘다.',metrics='성공률, robot-data sample efficiency, unseen object/viewpoint generalization, training GPU-hour, 단계별 오류(탐지/접근/접촉/완료).',risks='사람 영상과 테스트 작업이 의미적으로 중복되거나 detector가 새 시점에서 급락하면 표현 정렬의 순수 효과를 과대평가할 수 있다.'),
 related=['2406.09246','2504.16054','2610.40373']
)

D['2610.40373'] = dict(
 lead='HiFOR의 포인트는 “미래 영상을 그럴듯하게 예측한다”가 아니라 **현재 생성 중인 action에 필요한 미래 단서만 검색한다**는 데 있다. 짧은 시계열 상태 변화, 중간 작업 단계, 최종 목표를 함께 예측하고, 이 정보를 시간·시점·공간 축으로 구조화해 denoising 도중 조건부로 활용한다. 계획과 저수준 제어 사이의 정보 연결을 설계한 VLA 연구다.',
 pipeline=[
  ('현재 observation과 language condition 입력','카메라 시점과 언어 지시를 받아 현재 물체 배치·작업 목표를 인코딩한다.','입력: images + instruction'),
  ('Hierarchical Foresight Prediction','단기 상태 진화, semantic milestone, 최종 목표 상태를 함께 예측한다. Hierarchical Dependency Mask(HDM)가 서로 다른 시간 범위의 의존 관계를 구조화한다.','예측: short / middle / goal horizons'),
  ('Structure-Aware Latent World Modeling','미래 latent를 시간(horizon)·시점(view)·공간(spatial) 축으로 배열해 필요한 정보만 선택할 수 있게 만든다.','메모리: factorized latent future'),
  ('Action-Guided World Retrieval','action denoising이 진행되며 바뀌는 표현을 쿼리로 사용해 미래 공간에서 관련 정보를 찾아온다. 첫 스텝에 모든 미래 정보를 동일하게 주입하지 않는다.','질의: current denoising action features'),
  ('미래 단서로 action refinement','검색한 정보가 현재 행동을 수정하는 방향으로 작용한다. 이때 미래 예측 정확성과 실제 manipulation success가 반드시 같은 지표는 아니다.','출력: guided action chunk')],
 mechanisms=[
  ('Hierarchical Dependency Mask','단기 물리 변화와 장기 목표를 완전히 독립적으로 예측하면 중간 상태가 최종 목표와 어긋날 수 있다. HDM의 설계는 이 의존성을 모델 안에 명시하려는 시도다.','mask의 attention 허용 범위, 정보 누수 가능성, inference 시 필요한 입력을 확인하자.'),
  ('Latent 구조화가 필요한 이유','미래 시점들을 하나로 압축하면 특정 카메라의 작은 접촉 단서가 장기 목표 정보에 묻힐 수 있다. 축별 구조화는 retrieval granularity를 높인다.','시점 수 증가에 따른 메모리 크기와 지연시간을 확인하자.'),
  ('Denoising 중 동적 쿼리','action 생성 초기에 필요한 정보와 접촉 직전에 필요한 정보는 다를 수 있다. 변하는 행동 표현에서 future retrieval을 수행하는 구성은 action-dependent attention이라는 해석이 가능하다.','retrieval 호출 빈도가 행동 품질에 비해 latency를 얼마나 추가하는지가 실용성을 좌우한다.')],
 evidence=[
  ('시뮬레이션 평가','2개 벤치마크','초록에서 평가 개수만 확인 가능. 환경별 성공률과 baseline은 본문 표 확인 필요.'),
  ('실환경 평가','6개 manipulation tasks','현실 로봇 실험이 포함됐다는 주장. 과제별 시도 수·실패 모드를 봐야 한다.'),
  ('정량 비교 수치','초록에 미제시','서로 다른 연구의 성공률을 임의로 채워 넣지 않는다. 아키텍처 ablation은 원문에서 확인해야 한다.')],
 evidence_note='이 글에서는 확인되지 않은 과제별 성공률을 기재하지 않았다. Full paper의 실험표와 HDM/retrieval ablation을 직접 확인하자.',
 comparison='미래 latent 전체를 정책 조건으로 고정 전달하는 접근은 task-relevant 정보와 불필요한 변화가 섞일 수 있다. HiFOR는 미래를 **계층적으로 예측**한 후 **행동 예측 과정 중 조회(retrieval)** 하도록 설계해 예측 모델과 제어기의 연결 인터페이스에 기여한다.',
 reading_guide=[
  'HDM이 단기→중기→장기 예측 간 정보 방향을 어떻게 제한하는지 그림과 수식 읽기.',
  'future latent의 공간 해상도·카메라 수·horizon 길이를 확인해 추론 비용 계산하기.',
  'retrieval을 제거하고 모든 미래 정보를 넣는 baseline과, 미래 예측을 제거한 baseline을 분리하기.',
  '실제 로봇에서 한 행동 chunk의 계산시간·제어 주기·observation 갱신 주기를 확인하기.'],
 replication=dict(hypothesis='같은 예측 품질이라도 **action-guided retrieval**이 전역 미래 latent concat보다 접촉 과제 성공률을 높일 것이다.',setup='LIBERO 또는 RoboTwin에서 병 열기·서랍 닫기 등 단계가 분명한 과제들을 고르고, 예측 horizon 1/4/8·카메라 1/2대 조건을 변화시킨다.',baselines='no world model, flat future conditioning, hierarchical foresight only, hierarchical+retrieval full model.',metrics='task success, trajectory length, action inference p50/p95 latency, future prediction error, retrieval attention의 단계별 변화.',risks='정량 개선이 예측 모델의 추가 파라미터 때문인지 retrieval 메커니즘 때문인지 혼동하지 않도록 총 compute를 통제하자.'),
 related=['2610.07922','2608.01397','2410.24164']
)

D['2610.40026'] = dict(
 lead='RoboSeed는 새로운 VLA를 설계하기보다 “어떤 모델을 선택해야 하는가?”를 연구 질문으로 삼는다. 연구실마다 GPU 예산·실시간 제어 요구·허용 가능한 파인튜닝 시간·공개 증거 수준이 달라 **단일 성공률 1등 = 최선 모델**이라는 판단이 성립하지 않는다고 본다. 측정 불가능한 영역을 0점처럼 취급하지 않고 결측으로 남기는 설계가 핵심이다.',
 pipeline=[
  ('비교할 후보 모델과 실행 조건 고정','모델 체크포인트, action interface, 관측 입력, 훈련/평가 프로토콜을 정의한다. 서로 다른 벤치마크를 그대로 한 테이블에 섞지 않는다.','입력: 후보 VLA/WAM + 평가 프로토콜'),
  ('5개 평가 축의 증거 수집','capability, downstream training affordability, deployment affordability, locally verified research value, reproduction evidence를 별도 기록한다.','증거: local runs, 공개 가중치, audit, serving traces'),
  ('고정 기준으로 점수 정규화','각 차원을 동일한 앵커에 따라 0~100 프로필로 변환한다. 비교 불가능한 프로토콜이나 측정되지 않은 비용은 명시적으로 남긴다.','출력: axis-wise profiles + evidence coverage'),
  ('연구자 환경별 선택','균형형, 훈련 예산 제약형, 서빙 예산 제약형 같은 선호 설정을 적용해 어떤 trade-off가 중요한지 본다.','결과: 조건부 의사결정, 무리한 단일 랭킹 금지')],
 mechanisms=[
  ('정규화 앵커의 의미','0~100은 동일한 물리량이 아니라 사전에 고정된 참조점에 대한 변환이다. 앵커를 바꾸면 모델의 상대 순위가 달라질 수 있다.','raw value와 normalized score를 항상 같이 저장해야 한다.'),
  ('결측과 비교 불가능성을 구분','측정하지 않은 데이터는 낮은 성능의 증거가 아니다. 별개 action space나 프롬프트 인터페이스는 평가 프로토콜의 동등성이 깨진 상황이다.','coverage와 score를 하나의 숫자로 뭉개지 말자.'),
  ('학습 레시피 민감도','같은 사전학습 모델이라도 action decoding, LoRA 범위, action chunk 길이, optimizer 등 adaptation recipe에 따라 비용과 성공률이 바뀔 수 있다.','체크포인트 선택과 fine-tuning recipe를 함께 비교 대상으로 기록하자.')],
 evidence=[
  ('평가 차원','5개 독립 차원','capability·훈련 비용·배포 비용·연구 가치·재현 증거를 분리한다.'),
  ('정규화 프로필','0–100 점수','고정 앵커를 사용하며 미측정 축의 값은 보정하거나 임의 추정하지 않는다.'),
  ('종합 순위','제시하지 않음','serving trace 누락 및 이질적 프로토콜 때문에 총점 산출을 유보했다고 초록이 명시한다.')],
 evidence_note='RoboSeed의 핵심 결과는 SOTA 성능표가 아니라 “증거의 충분성”과 “예산 조건에 따른 최적 선택 변화”다.',
 comparison='기존 benchmark 리더보드는 특정 과제의 성공률을 한 축으로 보여준다. RoboSeed는 모델을 사용할 때 들어가는 **학습·추론 자원, 증거의 재현성, 비교 프로토콜의 적합성**을 연구자의 의사결정에 포함한다. 특히 불완전한 종합 점수를 발표하지 않는 태도는 보수적인 실험 해석이다.',
 reading_guide=[
  '5차원별 원시 측정값이 무엇이며 normalization anchor가 어떤 근거로 정해졌는지 확인하기.',
  '‘비교 가능’ 판정 기준이 관측·action-space·policy frequency까지 포함하는지 보기.',
  '추론 지연시간에 이미지 전처리, 네트워크 전송, action chunk 길이, batch size가 포함됐는지 확인하기.',
  '저자 측 local evaluation과 기존 논문에서 인용한 결과를 섞지 않았는지 provenance 확인하기.'],
 replication=dict(hypothesis='VLA 리더보드 성공률 1위가 제한 GPU·실시간 제어 환경에서 항상 Pareto-optimal하지 않을 것이다.',setup='같은 RoboCasa/Libero task subset으로 OpenVLA·OpenVLA-OFT·π0 계열 등 공개 가능한 후보 3~4개를 동일 환경에서 재측정한다.',baselines='성공률 단일 정렬 vs latency/VRAM/training-hours/coverage를 포함한 Pareto frontier; 각 모델의 default recipe와 tuned recipe를 나눠 기록.',metrics='success %, p95 action latency, GPU peak memory, adaptation cost, evidence coverage, protocol mismatch flags.',risks='학습에 사용할 초기 데이터·추론 하드웨어가 다르면 자원 수치가 비뚤어진다. 표준화할 수 없는 경우 ‘비교 불가’로 표시해야 한다.'),
 related=['2406.09246','2410.24164','2609.16074']
)

D['2610.07922'] = dict(
 lead='OpenWAM은 “video predictor + action expert를 같이 쓰면 좋아진다”에서 끝나지 않고, **둘의 생성 순서를 바꿔가며 검증할 수 있는 공통 실험 플랫폼**을 제시한다. 로봇 비디오용 causal backbone, MoT 결합, VTA/JOIN 등의 추론 프로그램을 같은 토대 위에 올리고, counterfactual dynamics를 통해 시연 밖의 상태 전이까지 학습하는 효과를 비교한다.',
 pipeline=[
  ('로봇 비디오 기반 사전학습','Wan2.2-5B에서 출발해 다양한 로봇·인간·합성 상호작용 영상으로 causal robot-video pretraining을 수행한다. 이 단계의 핵심 supervision은 action label이 아니라 관찰 영상의 시간적 구조다.','입력: 1만 시간 이상 영상 / 로봇 동작 동역학의 시각 특징'),
  ('비디오 expert + action expert 구성','5B video stream과 약 2B action expert를 Mixture-of-Transformers 구조로 결합하고, 필요한 지점에서 두 종류의 토큰이 정보를 주고받게 한다.','구성: shared attention, expert-specific blocks'),
  ('생성 프로그램 바꾸기','joint 생성 / video→action / action→video / decoupled 등 서로 다른 영상·동작 인터랙션을 지원한다. 특정 방식에서 성능이 높아도 다른 방식에는 적용되지 않을 수 있다.','제어: composable video-action schedules'),
  ('역·순방향 동역학 학습','inverse dynamics는 상태 변화에서 action을, forward dynamics는 action에서 미래 변화를 추정한다. demonstration 외의 counterfactual transition도 supervision으로 사용한다.','출력: behavior policy 또는 reusable dynamics'),
  ('제한된 타깃 작업으로 전이','미래 영상 예측기만 작업에 맞춰 적응하고, 독립적으로 학습한 inverse dynamics를 재사용하는 구성을 실험한다.','평가: held-out task transfer')],
 mechanisms=[
  ('왜 Causal Video Pretraining인가','일반 비디오 모델의 대칭적 시간 처리가 실제 robot closed-loop inference와 맞지 않을 수 있다. 과거와 현재만으로 미래 chunk를 생성하도록 설계를 바꾸고 로봇 상호작용 분포에 맞춰 학습한다.','pretrain 데이터 크기뿐 아니라 causal adaptation 유무를 별도 ablation으로 읽자.'),
  ('Shared Mixture-of-Transformers','시각적 프레임 생성과 연속 행동 예측은 출력 차원·목적함수가 다르다. 하나의 trunk로 억지 통합하기보다 토큰 간 attention 경로는 공유하면서 video/action expert의 전용 파라미터를 보존한다.','MoT 개선 폭은 같은 pretraining, 같은 train data에서 측정된 것이어야 한다.'),
  ('Counterfactual Dynamics의 가치','성공 시연에는 특정 상태에서 실제 선택된 action 결과만 존재한다. 여러 다른 action을 취했을 때의 결과(counterfactual)를 학습하면 inverse/forward 모델이 관측 영상에 과적합하는 문제를 줄일 수 있다.','counterfactual 데이터가 실제 궤적과 얼마나 물리적으로 타당한지 확인할 것.'),
  ('Local-context IDM 전이','새 작업의 영상 생성기는 바꾸되, 짧은 시간 창만 보는 inverse dynamics를 동결해 행동을 회복한다. 긴 전체 문맥을 보게 하는 모델보다 국소 동역학의 이식성이 높을 수 있다는 가설이다.','task-specific retraining 없이 unseen scene/action 분포에서 성립하는지 중요하다.')],
 evidence=[
  ('LIBERO-Long, VTA','68.4% → 97.8%','Wan2.2 초기화 대비 causal robot-video pretrained backbone 사용. 동일 interaction 프로그램 내 성능 비교.'),
  ('LIBERO-Long, Joint','62.2% → 96.6%','공식 프로젝트의 초기화 비교. 동일 architecture/후속 학습 조건에서 수행.'),
  ('Held-out LIBERO-90, IDM','84.0% / 47.0% / 21.5%','counterfactual+demonstration local-context IDM / full-context IDM / demonstration-only local IDM 비교. 각자 동일한 task 4개의 평균.'),
  ('Forward dynamics 예측','RGB 오류 34.5% 감소','counterfactual 감독 추가 시 저자 보고.'),
  ('16-way outcome identification','21.1% → 71.3%','동일 상태에서 발생 가능한 16개 결과 구분 성능. 연속 제어 성공률과는 별도 지표.')],
 evidence_note='VTA·Joint는 영상/행동 상호작용 프로그램이다. 97.8%와 84.0%는 서로 다른 평가 설정이므로 숫자만 뽑아 순위를 매기지 말 것.',
 comparison='일부 WAM 연구는 pretraining 규모·비디오 백본·action decoder·조건부 생성 순서를 동시에 바꾼다. OpenWAM은 이를 구성 가능한 프로그램으로 나눠 **같은 비디오 파운데이션 위에서 원인을 분해**하려는 점이 가치다. SG-WAM이 정책 latent의 alignment를 연구한다면 OpenWAM은 비디오와 행동을 결합하는 **시스템 설계 공간**을 연구한다.',
 reading_guide=[
  '영상 사전학습 자료 구성(로봇/인간/합성 비중)과 causal attention 설계가 초기화 개선 폭에 얼마나 기여했는지 분리하기.',
  'VTA, Joint, ATV, decoupled의 token-visible 구조와 샘플링 순서를 그림으로 다시 그리기.',
  'LIBERO-Long 비교의 action frequency, denoising 횟수, 예측 horizon, 로봇 observation frame 수 확인하기.',
  'counterfactual IDM의 frozen setting이 다른 작업·카메라·로봇 embodiment에서 유지되는지 찾아보기.',
  '가용 GPU 수와 학습시간을 포함한 재현 가능성을 판단하기. 대규모 비디오 단계의 비용은 별도다.'],
 replication=dict(hypothesis='정책 학습 성능에서 **로봇 비디오 causal pretraining**과 **video-action 결합 순서**의 효과를 독립적으로 확인할 수 있다.',setup='기존 공개 video backbone과 소형 action head를 사용해 동일 LIBERO task subset에서 2×3 factor experiment(비디오 pretraining 유무 × Joint/VTA/decoupled) 수행.',baselines='영상 없는 VLA, raw Wan initialization, robot-video pretrained initialization, MoT vs shared-head. 가능한 한 총 학습 토큰·fine-tune 데이터량을 맞춘다.',metrics='success %, video prediction quality, inverse dynamics action error, control latency, GPU-hour, failure recovery.',risks='모델 크기·pretraining data 차이를 통제하지 않으면 interaction 방식 자체의 효과가 과장될 수 있다.'),
 related=['2608.01397','2609.23578','2609.16074']
)

D['2609.23578'] = dict(
 lead='AR-WAM은 “LLM 에이전트가 이미 무엇을 할지 계획한다면, 하위 로봇 정책에 긴 자연어를 다시 입력할 필요가 있을까?”라는 인터페이스 질문을 던진다. 자연어 대신 **목표 물체의 bounding box + 원자적 동작을 뜻하는 operation token**으로 정책을 호출하고, 긴 시간 기억과 실패 복구는 상위 에이전트가 처리한다. 정책과 에이전트의 책임 분리라는 시스템 관점이 중요하다.',
 pipeline=[
  ('상위 에이전트에서 작업 분해','언어 지시를 처리하는 VLM/agent가 현재 목표 객체와 수행할 원자적 skill을 결정한다. 에이전트는 검출·실행·조회 인터페이스를 사용할 수 있다.','Agent: detect / execute / query'),
  ('객체 위치를 시각 프롬프트로 지정','target bounding box로 조작할 물체와 공간적 참조를 구체화한다. “저기 왼쪽 컵” 같은 모호한 자연어 참조를 로봇 정책에 중복 전달하지 않는다.','Condition: visual bounding box'),
  ('행동 종류는 operation token으로 지정','배운 연산 토큰이 집기·누르기·놓기 같은 기본 동작을 구분한다. 이 token은 문장 생성이 아니라 조작 정책을 조건화한다.','Condition: learned operation token'),
  ('장면 변화 예측 및 action decoding','고정 pretrained visual encoder를 이용한 약 0.5B 모델이 compact latent scene evolution을 추정하고 행동을 출력한다.','Output: action chunk + inspectable predicted state'),
  ('긴 과제에서는 에이전트로 되돌아가기','원자 skill 이후 상태를 확인하고 상위 에이전트가 다음 동작 또는 오류 복구를 결정한다. 장기 memory는 하위 정책의 책임 밖에 둔다.','Closed loop: observe → query → re-plan')],
 mechanisms=[
  ('Visual grounding vs 언어 grounding','지시 표현에 bounding box를 쓰면 object reference를 픽셀 공간에서 명확하게 만들 수 있다. 다만 detector 오검출이나 가려진 객체의 참조 문제는 상위 시스템의 부담이 된다.','bbox 품질을 고정한 Oracle vs detector 조건을 분리해 비교하자.'),
  ('Policy/agent 경계 설정','정책이 각 atomic skill을 안정적으로 실행하고 에이전트가 task-level state를 관리하는 구조다. 즉 하위 policy 평가와 system-level long-horizon 평가의 실패 원인을 분리할 수 있다.','성공률 증가가 policy 자체인지 에이전트 기억·재시도 능력인지 확인할 것.'),
  ('경량 모델과 실시간성','0.5B 정책은 거대한 language backbone을 반복하지 않아 action inference가 짧다는 설명이다. 단, agent API 호출 및 detect latency까지 포함한 전체 루프 시간과는 구분해야 한다.','14.1ms 측정이 정확히 어느 GPU, batch, action chunk를 기준으로 하는지 확인하자.')],
 evidence=[
  ('표준 조작 평균','87.2%','RoboTwin 2.0 등의 설정에서 저자 보고. 프로젝트 페이지에는 clean/randomized 평균도 별도로 제시된다.'),
  ('Action inference','약 14.1 ms','논문 초록 수치. 프로젝트는 RTX 4090 bf16에서 action chunk 기준 14.09ms를 제시한다.'),
  ('Memory-dependent / long-horizon','+5.9 / +36.7%p','기존 강한 비교군 대비 성공률 개선으로 저자 보고. 과제/환경별 실험표를 구분해야 한다.'),
  ('실제 Astribot S1 평균','71.7% vs 35.0%','공식 프로젝트의 3개 long-horizon 작업, 각 20회 시도. π0.5와 비교.')],
 evidence_note='14.1ms는 모델 추론 기준이며 원격 에이전트·객체 검출·로봇 명령 전송을 포함한 end-to-end wall-clock 제어 지연과 같지 않다.',
 comparison='일반 VLA는 이미지+자연어 지시를 하나의 정책으로 받아 action을 출력한다. AR-WAM은 상위 에이전트에 language/memory/recovery를 넘기고 하위 policy는 **bbox 및 operation token으로 조건화된 원자 skill**을 담당한다. 특히 에이전트 시스템과 빠른 로봇 컨트롤러를 실용적으로 연결하려는 시도다.',
 reading_guide=[
  'Operation token이 학습 시 어떤 supervision을 받는지, skill taxonomy가 고정인지 확인하기.',
  'RoboTwin clean/randomized 결과와 실환경 Astribot S1 결과를 혼용하지 않고 각각 표로 정리하기.',
  'detect/execute/query 호출 시 상위 agent가 어느 타이밍에 다음 상태를 관찰하는지 추적하기.',
  'end-to-end latency를 별도 측정해 model-only 14.1ms와 비교하고, 실패 복구로 추가된 총 실행시간을 기록하기.'],
 replication=dict(hypothesis='동일 action policy 규모에서 **bbox+operation interface**가 자연어 조건보다 모호한 참조가 많은 장기 과제에서 실패를 줄일 것이다.',setup='양팔 RoboTwin 2.0에서 좌/우가 유사한 물체 선택, 여러 번 반복 누르기, 순서 기억 과제를 구성하고 동일 perception stack을 붙인다.',baselines='language-conditioned low-level policy, oracle bbox+operation, detected bbox+operation, agent memory 제거/추가.',metrics='정확한 객체 선택률, task success, replan 횟수, perception error %, p95 end-to-end latency.',risks='상위 agent 성능이나 검출기 모델을 바꾸면서 interface만의 이득이라고 해석하지 않도록 한다.'),
 related=['2503.14734','2610.07922','2504.16054']
)

D['2609.19600'] = dict(
 lead='WorldContact는 접촉이 잦은 변형체를 빠르게 전개하는 **학습된 물리 surrogate**를 만든 다음, 결과로 생성한 추가 시연 데이터를 VLA fine-tuning에 투입한다. 핵심 성과는 장면을 그럴듯하게 생성한 것이 아니라 **simulator 기반 학습 데이터를 확장해 실제 봉투 들기 성공률을 개선했다는 연결**이다. 원래 물리 시뮬레이터가 필요로 하는 매우 작은 적분 스텝을 큰 학습 예측 스텝으로 대체한다.',
 pipeline=[
  ('소수의 품질 높은 물리 시연 확보','원본 numerical simulator에서 접촉·변형·도구 조건이 정확한 궤적을 수집한다. 실패한 시뮬레이션이나 이상한 접촉은 데이터 품질 문제를 만들 수 있다.','입력: physically verified trajectories'),
  ('접촉 조건을 구조화','변형물체 각 정점의 위치·속도와 함께 다른 물체, 표면, gripper, 물체 내부 연결(topology)에서 발생하는 접촉 관계를 인코딩한다.','특징: contact-aware deformable-object state'),
  ('큰 시간 간격으로 전진 예측','학습된 transition model이 짧은 수치 적분 여러 번 대신 다음 상태를 직접 예측하고 rollout을 전개한다.','출력: synthetic future vertex states'),
  ('예측 상태를 로봇 관찰로 렌더링','물체 정점의 예측 상태를 카메라 관측으로 변환하고, 해당 전이를 만들 때 사용된 robot action과 쌍으로 구성한다.','학습 데이터: rendered images + known actions'),
  ('기존 VLA를 fine-tuning해 실제 평가','모델로 확장한 데이터와 소수의 source simulation 시연만을 사용한 모델을 동일한 실물 봉투 조작 조건에서 비교한다.','출력: real-robot grasp-and-lift success')],
 mechanisms=[
  ('Contact-centric representation','봉투의 두 정점이 화면상 가까운 것과 동일한 천 표면의 이웃인 것은 서로 다른 물리 관계다. 로봇 gripper의 접촉도 고정 테이블과 의미가 다르므로 종류를 구분해야 한다.','접촉 그래프가 물체의 topology 변화·self-contact를 얼마나 처리하는지 확인하자.'),
  ('학습된 큰 step과 안정성','source simulator가 작은 integration step을 반복하는 대신 predictor가 비교적 긴 상태 전이를 직접 출력한다. 빠르지만 rollout error가 누적될 수 있으므로 충돌·관통·구조 보존 규칙이 중요하다.','원본 10× 수치는 **상태 rollout** 속도이지 렌더링·I/O·전체 학습 시간 비교가 아니다.'),
  ('Surrogate → 데이터 → 정책의 인과 사슬','동역학 MSE가 낮다고 로봇 policy가 더 잘 작동하는 것은 아니다. 결과로 생성한 관측-행동 데이터가 target task의 state coverage를 넓혔을 때에만 실제 성능 개선을 기대할 수 있다.','합성 데이터의 양, 상태 다양성, label noise를 함께 ablation하자.')],
 evidence=[
  ('변형체 과제 범위','쇼핑백 관련 16개 과제','원문 초록에 명시된 물리 월드 모델 평가 범위.'),
  ('State rollout 처리량','10×','단일 H100, source simulator 대비. 렌더링·디스크 I/O 제외.'),
  ('실제 봉투 들어 올리기','65% → 95%','source simulation 데이터만 사용한 policy 대비 WorldContact 확장 데이터를 활용한 동일 policy의 single-attempt success.'),
  ('실패 판정','단회 시도 성공률','한 번 집어 들어 올리기를 완수하는 평가이며 장기 일반 조작의 성공률은 아니다.')],
 evidence_note='큰 성능 차이는 특정 쇼핑백 manipulation, 정책, 환경에서 관찰됐다. 다른 deformable objects로의 전이 효과는 미검증이다.',
 comparison='고정된 시뮬레이터로 무한한 학습 데이터를 만드는 접근은 느리고 비용이 크다. 일반 pixel-video generator는 접촉·변형을 실제 제어에 필요한 수준으로 보존하지 못할 수 있다. WorldContact는 **접촉 중심 상태공간의 빠른 dynamics + image rendering + 동일 VLA fine-tuning**이라는 연결을 검증한다.',
 reading_guide=[
  'contact neighborhood에 gripper/환경/물체 topology가 각각 어떻게 입력되는지 그림으로 확인하기.',
  'model rollout의 오차 누적과 충돌 판정을 몇 step까지 측정했는지 보기.',
  '합성 데이터 수를 늘렸을 때 65→95%가 항상 유지되는지, 어떤 state coverage가 늘었는지 확인하기.',
  '시간 측정에 포함된 계산(상태 전진)과 제외된 계산(rendering, I/O)을 구분하기.'],
 replication=dict(hypothesis='접촉 특징을 갖춘 예측기가 일반 dynamics network보다 데이터 확장 효율과 실제 deformable manipulation 성공률을 높일 것이다.',setup='쇼핑백·수건·비닐 포장 3종에서 25/50/100개 물리 시연으로 surrogate를 학습하고, 렌더링 기반 VLA 데이터 확장 비율 1/3/6배를 조절한다.',baselines='source sim only, learned world model without contact features, contact-centric model with/without topology constraint.',metrics='penetration rate, vertex positional error, rollout stability, end-to-end data generation time, real grasp success/hold duration.',risks='SIM 재질 파라미터와 테스트 물체가 다르면 10× 가속이 유지돼도 실세계 정책 성능은 악화할 수 있다.'),
 related=['2605.00080','2610.07922','2403.12945']
)

D['2609.16074'] = dict(
 lead='이 서베이는 WAM을 모든 비디오 생성 모델의 동의어로 쓰지 않는다. 핵심 범위는 **미래 세계 변화 예측과 실행 가능한 로봇 행동 생성이 어떤 방식으로 결합되는가**이다. 상태 표현·전이·action interface·학습 데이터·평가를 나눠 놓고 논문을 보면, ‘월드 모델이 실제 정책에 어떻게 도움이 되는가?’라는 질문을 비교 가능하게 만든다.',
 pipeline=[
  ('세계와 행동의 입력·출력 공간 정의','관찰이 RGB video인지 3D geometry인지 policy latent인지, 행동이 low-level command인지 semantic instruction인지부터 정한다.','분류축: observation/state/action representations'),
  ('미래 전이 예측의 역할 분리','월드 모델이 다음 상태를 예측해 planning에 쓰이는지, 생성 데이터를 공급하는지, policy action을 직접 조건화하는지 구분한다.','역할: prediction / imagination / planning / data generation'),
  ('World–Action 연결 패턴 비교','joint generation, video-first, action-first, inverse dynamics 등 정보 흐름의 위치를 정리한다.','구성: couplings & architectures'),
  ('학습 및 평가 프로토콜 정리','시연·영상·합성·온라인 경험의 감독 형태와 시뮬레이션/실환경 결과를 구분한다.','평가: prediction accuracy vs action success'),
  ('열린 문제로 연구 가설 만들기','action alignment, 멀티뷰 공간 일관성, 긴 시간 기억, inference 효율을 실제 시스템 연구의 축으로 제안한다.','산출물: research roadmap')],
 mechanisms=[
  ('WAM과 VLA의 개념적 차이','반응형 VLA는 현재 observation과 instruction에서 바로 행동을 만들 수 있다. WAM은 행동을 내면서 세계가 어떻게 바뀔지 모델링하는 경로를 명시적 또는 학습 잠재 방식으로 더한다.','둘 사이의 명확한 경계보다 실제 prediction loss/usage를 살펴보자.'),
  ('World prediction의 평가 함정','video reconstruction fidelity가 높아도 action-relevant contact state를 잃으면 정책에는 도움 되지 않을 수 있다. 반대로 latent transition이 픽셀로 그럴듯하지 않아도 제어성에 기여할 수 있다.','visual quality, dynamics accuracy, closed-loop success의 상관을 따로 검증하자.'),
  ('장기·부분 관측의 난점','장기 작업에서는 uncertainty가 누적되고, 손에 가려진 물체·가해진 힘·마찰처럼 이미지에서 직접 관찰하기 어려운 변수가 중요하다.','history length, belief state, failure recovery를 어떤 module이 담당하는지 볼 것.')],
 evidence=[
  ('논문 유형','기술 서베이','새로운 policy SOTA를 증명하는 논문이 아니다.'),
  ('핵심 분류 축','표현·전이·액션·학습·데이터·스케일링·평가','공통 설계 요소를 체계적으로 정리한다.'),
  ('적용 영역','조작·내비게이션·자율주행','도메인이 달라 성능 숫자를 횡단 비교하기 어렵다.')],
 evidence_note='서베이는 기존 문헌의 분류와 시사점을 제공한다. 해당 페이지의 결과 표는 수치적 성능 주장을 하지 않는다.',
 comparison='일반 video world-model survey가 생성 품질과 latent dynamics 전체를 넓게 다룬다면, 이 서베이는 **robot-control interface와 행동 생성 결합**을 중심축으로 삼는다. 기존 WAM 논문들의 설계 차이를 분리하는 데 참고할 지도 역할을 한다.',
 reading_guide=[
  '새 WAM 논문을 읽을 때 먼저 입력 상태·출력 action type·prediction target·policy 결합 방식을 4칸 표로 정리하기.',
  '저자가 closed-loop 실험을 했는지, future prediction만 보여주는지 구분하기.',
  '환경별 관측 가능성(부분 관측, contact sensing)과 action latency가 비교 프로토콜에 반영됐는지 보기.',
  'survey 분류에 들어가지 않는 새 아키텍처가 등장했다면 분류 확장을 제안할 여지를 남기기.'],
 replication=dict(hypothesis='WAM 벤치마크를 prediction metric만으로 평가하면 실제 manipulation success와 일치하지 않는 경우가 많을 것이다.',setup='공개 WAM 3~4개에서 같은 action-conditioned 예측의 FVD/PSNR과 downstream policy success, contact error를 함께 측정한다.',baselines='reactive VLA, explicit future-prediction WAM, policy-latent transition WAM.',metrics='video metric, contact consistency, closed-loop success, control latency, uncertainty under domain shift.',risks='prediction target이 달라 metric을 맞추기 어렵다면 무리한 단일 점수 대신 Pareto plot을 사용한다.'),
 related=['2610.07922','2608.01397','2605.00080']
)

D['2608.01397'] = dict(
 lead='SG-WAM은 예측 공간을 policy 외부에 따로 두지 않는다. **현재 정책 backbone의 내부 표현에서 dynamics token을 만들고 같은 정책의 EMA 복사본으로 미래 목표를 만든다.** 여기에 기하학적 감독을 넣어 미래 latent가 로봇의 접촉·공간 관계를 잃지 않게 한다. 거대한 별도 video world model 없이 행동과 미래예측을 동시에 학습하는 방향이다.',
 pipeline=[
  ('Multi-view observation과 언어 지시 인코딩','policy backbone이 현재 시각 정보에서 action과 관련된 표현을 구성한다. 기하 감독이 객체 위치·로봇과의 상대 배치 같은 공간적 관계를 강화한다.','입력: observation views + instruction'),
  ('Dynamics tokens 추출','학습 가능한 dynamics tokens가 정책 내부 정보와 상호작용하면서 compact한 현재 상태를 나타낸다.','상태: policy-derived latent z_t'),
  ('Action-conditioned latent 전이','Self-Guided World Predictor가 intervening action chunk를 조건으로 미래 dynamics token을 예측한다.','transition: z_t + action → predicted z_(t+Δ)'),
  ('EMA target으로 stop-gradient 감독','같은 정책 backbone의 EMA 버전으로 미래 observation을 인코딩해 target token을 만들고 prediction loss를 계산한다.','supervision: stopped-gradient EMA future latent'),
  ('Flow-matching action generation','미래 예측·geometry grounding·연속 행동 생성을 공동 최적화해 제어와 예측을 같은 policy representation에 정렬한다.','출력: continuous action chunk')],
 mechanisms=[
  ('Self-guided target','별도 고정된 영상 모델의 feature를 imitation하면 현재 정책 action에 불필요한 정보까지 학습할 수 있다. EMA target은 policy와 같은 representation family 내에서 예측 목표를 부여한다.','EMA decay와 stop-gradient가 collapse를 어떻게 막는지 코드/원문에서 확인하자.'),
  ('Geometry grounding의 역할','잠재 공간이 이미지 의미만 잘 표현해도 로봇 손끝과 물체 접촉 위치를 놓칠 수 있다. 기하학적 신호는 dynamics token이 공간 상태에 민감하도록 유도한다.','depth/geometry label이 없을 때 성능 손실이 얼마나 큰지 보기.'),
  ('Dynamics token 개수','너무 적으면 상태 변화 압축이 심하고 너무 많으면 중요한 정보에 대한 집중도가 떨어질 수 있다. 원문 ablation에서는 1→8 토큰 개선 후 16에서 평균 성능이 떨어진다.','토큰 수를 하드웨어·카메라·task horizon 별로 최적화할 필요가 있다.')],
 evidence=[
  ('LIBERO 4개 suite 평균','98.5%','원문 Table 4, geometric supervision과 world modeling을 모두 사용.'),
  ('LIBERO-Plus 평균','73.0%','원문 초록에 제시된 강화된 benchmark 설정.'),
  ('No geo / no WM','95.3%','LIBERO ablation baseline, 완전 모델 대비 -3.2%p.'),
  ('Geo only / WM only','96.6% / 97.6%','각 보조 목적의 독립 기여. Table 4.'),
  ('Dynamics tokens 1 / 8 / 16','96.1% / 98.5% / 97.2%','원문 Table 5. 같은 모델의 token 개수 ablation.')],
 evidence_note='98.5%는 LIBERO 동일 설정에서의 평균. 다른 논문의 LIBERO 성능과 곧바로 모델 우열을 비교할 수 없으며, 이 논문 자체의 ablation이 가장 설득력 있는 증거다.',
 comparison='OpenWAM 같은 explicit video foundation 결합과 달리 SG-WAM은 **policy-derived latent**에서 action-conditioned future learning을 수행한다. 예측의 화질을 높이는 목표보다 action relevance·geometry alignment에 집중한다. reactive VLA 대비 world prediction loss의 실질적 기여를 ablation으로 보여준다.',
 reading_guide=[
  '현재 latent와 EMA future target이 동일 정책 표현 공간에서 생성되는 경로를 식 2와 네트워크 그림으로 확인하기.',
  'world modeling만 넣었을 때 97.6%, geometry만 넣었을 때 96.6%라는 개별 효과를 무조건 합산하지 않기.',
  'LIBERO-Long에서 world modeling 제거 시 실패 유형이 어떻게 바뀌는지 보고, 단기 vs 장기 전이 기여를 분리하기.',
  'real-world 실험의 UR5e와 시뮬레이션 policy 차이(카메라 수, observation, task set)를 확인하기.'],
 replication=dict(hypothesis='정책 latent에 미래 target을 구성하는 방식이 외부 perceptual encoder target보다 실환경 contact-success와 더 높은 상관을 가질 것이다.',setup='같은 LIBERO 4 suite에서 token 1/4/8/16, EMA 유무, geometry loss 유무를 재현하고 UR 계열 하드웨어에서 한 과제로 검증한다.',baselines='reactive flow-matching VLA; frozen visual-target world model; policy EMA target; geometry only; full combination.',metrics='task success by suite, transition cosine/MSE, inference latency, contact pose error, domain-shift retention.',risks='geometry 감독 비용과 action chunk 설정을 동일하게 해야 모델 구조의 이득을 공정하게 평가할 수 있다.'),
 related=['2610.07922','2610.40373','2410.24164']
)

D['2605.00080'] = dict(
 lead='이 서베이는 world model을 “동영상 생성기”로 한정하지 않는다. **로봇 행동 이후 환경이 어떻게 바뀌는지 예측**하고, 그 결과가 정책 학습·계획·시뮬레이션·평가·데이터 생성의 어떤 단계에서 사용되는지에 초점을 맞춘다. WAM 연구뿐 아니라 learned simulator, model-based RL, embodied navigation을 큰 지도 안에 배치하는 참고 논문이다.',
 pipeline=[
  ('용어부터 분리','world model, video generator, visuomotor policy, VLA를 구분한다. 예측의 조건에 로봇 low-level action이 있는지, 고수준 language goal만 있는지 확인한다.','기초: state x, action a, high-level condition l'),
  ('정책과 world model의 결합 위치 정리','future prediction이 직접 action 생성 입력에 들어가는지, inverse dynamics와 결합되는지, 계획 알고리즘의 후보 평가에 쓰이는지 나눈다.','역할: action conditioning / planning / IDM'),
  ('학습된 시뮬레이터로서의 활용','world model rollout을 사용해 policy RL을 학습하거나 안전성·성능을 가상 평가할 수 있다. 현실에서 관찰하지 못한 행동에 대한 error가 관건이다.','역할: training environment / evaluation'),
  ('로봇 비디오 파운데이션과 구조화 모델','비디오 모델이 대규모 사전학습을 통해 얻는 일반화와, geometry/contact-aware 모델이 주는 물리 구조를 비교한다.','설계: generative visual vs geometric dynamics'),
  ('도메인 확장과 연구 과제','조작·내비게이션·자율주행의 observation horizon과 행동 주기를 비교하고 미해결 과제를 정리한다.','범위: diverse embodied tasks')],
 mechanisms=[
  ('Action-conditioned prediction의 최소 조건','전형적인 표현은 현재 상태 x_t, 행동 시퀀스 a, 고수준 조건 l에 대한 미래 x_(t+1:t+H)의 조건부 예측이다. 중요한 것은 미래 예측이 실제 action choice에 쓸 수 있는가다.','미래예측이 텍스트/이미지에서만 평가됐는지 closed-loop control까지 이어졌는지 나누자.'),
  ('Predictive state와 policy state 차이','비디오 모델의 고차원 pixel state는 시각적 질감까지 담지만 policy에는 접촉·상대 위치·도달 가능성 같은 작은 정보가 핵심일 수 있다. 구조화된 representation은 효율과 해석성을 얻는 대신 표현 범위를 제한한다.','원 논문 비교 시 input modality와 prediction target을 같은 축에서 정리하자.'),
  ('상상 데이터의 위험','학습된 simulator가 실제로는 일어나지 않을 전이를 많이 만들어도 policy는 그 데이터에 적응할 수 있다. distribution shift와 compounding error를 피하려면 rollout horizon와 uncertainty 평가가 필요하다.','단기 pixel metric보다 closed-loop policy uplift가 강한 증거다.')],
 evidence=[
  ('논문 성격','43쪽, 서베이','원문 arXiv 메타데이터에 6개 figure가 보고되어 있다.'),
  ('다루는 용도','정책 학습·계획·시뮬레이션·평가·데이터 생성','다른 활용 사례를 역할별로 나눠 설명한다.'),
  ('적용 분야','robot manipulation / navigation / autonomous driving','하나의 benchmark ranking을 내는 연구가 아니다.')],
 evidence_note='이 포스팅의 수식적 설명은 서베이의 개념을 이해하기 위한 요약이다. 모델별 정량 결과는 각각의 원논문을 확인해야 한다.',
 comparison='WAM 전용 서베이(2609.16074)가 미래 예측과 실행가능 action의 결합을 강조한다면 이 종합 서베이는 **월드 모델의 여러 기능**—예측 모델, 학습 시뮬레이터, 정책 평가 도구—을 더 폭넓게 분류한다. 연구 주제를 정할 때 먼저 이 논문으로 전체 지형을 잡고, 실험 설계는 대상 원논문에서 찾아보는 것이 효율적이다.',
 reading_guide=[
  'Method가 예측하는 state가 RGB 영상·latent·3D/point cloud 중 무엇인지 모든 모델을 표로 정리하기.',
  'world model 사용 목적이 policy conditioning, planning, RL simulator, data augmentation 중 어느 것인지 고정하기.',
  'closed-loop success와 prediction-only metric을 같은 성능열에 섞지 않기.',
  'long horizon, real-world domain shift, inference compute 문제를 구체적 테스트 프로토콜로 변환해 보기.'],
 replication=dict(hypothesis='예측 representation을 접촉/3D 상태에 맞출수록 pixel generation 품질과 무관하게 contact-rich manipulation 성능이 좋아질 수 있다.',setup='RoboCasa에서 동일 task에 video latent dynamics, compact geometry latent dynamics, reactive VLA를 두고 액션 정보를 공유하도록 통제한다.',baselines='reactive policy vs explicit predictor vs geometry-aware predictor. 예측기는 데이터 증강에만 쓰는 variant도 분리한다.',metrics='task success, predicted contact error, compute cost, planning horizon sensitivity, unseen scene generalization.',risks='각 방법의 관측/행동 입력을 다르게 하면 표현 자체의 효과를 알 수 없게 된다.'),
 related=['2609.16074','2609.19600','2610.07922']
)

D['2504.16054'] = dict(
 lead='π0.5는 단순히 π0 모델 크기를 키운 후속작이 아니라 **서로 다른 종류의 데이터를 한 정책의 의미 이해와 제어 학습에 함께 활용하는 훈련 레시피**를 검증한다. 로봇 시연만으로는 충분히 모으기 어려운 ‘새 집에서 부엌을 정리하라’ 같은 과제를 위해 웹 데이터·타 로봇 데이터·고수준 단계 지시·연속 action을 연결한다.',
 pipeline=[
  ('다종 로봇·웹·언어 데이터를 섞어 사전학습','로봇 궤적과 object localization, image caption, 언어 지시, subtask 예측 등 서로 다른 형태의 예시를 co-train한다.','입력: robot datasets + web multimodal + semantic tasks'),
  ('이산 표현 기반 광범위한 사전학습','여러 modality와 행동을 sequence-modeling 형태로 구성한다. 원문은 pretraining 단계의 FAST action tokenizer를 설명한다.','pretrain: discrete action/semantic token learning'),
  ('실제 mobile manipulation에 맞춘 post-training','새 가정에서 해야 할 이동식 조작을 위한 low-level action과 ‘어떤 세부 과제를 먼저 해야 하는가?’라는 high-level semantic action을 함께 학습한다.','adapt: household manipulation + semantic subtasks'),
  ('실행 중 high-level → low-level 분할','현재 장면에서 필요한 subtask를 먼저 추론하고, 그 subtask를 조건으로 flow-matching continuous action chunk를 생성한다.','runtime: subtask prediction → action chunk'),
  ('처음 보는 집에서 장기 로봇 과제 실행','청소·수건 걸기·침대 정리 등의 작업을 새로운 가정에서 실행한다. 실제 학습 데이터와 테스트 공간의 분리를 검토해야 한다.','evaluation: unseen real homes')],
 mechanisms=[
  ('의미적 일반화와 물리적 숙련의 결합','웹 데이터는 물체 이름·공간 의미를 보강하지만 그 자체로 정확한 gripper trajectory를 알려주지는 않는다. 로봇 데이터는 모터 기술을 주고, high-level semantic label은 장기 계획을 연결한다.','co-training component 제거 실험이 서로의 역할을 보여주는지 확인하자.'),
  ('두 단계 pre/post training','논문 본문에 따르면 큰 이질 데이터 혼합으로 pretrain한 뒤 목표 로봇 과제에서 continuous flow-matching action을 포함해 post-train한다. 이산+연속 action 표현을 한동안 다르게 쓰는 이유는 범용성·정밀 제어의 trade-off다.','pre/post training 경계와 loss mixture 비율을 읽어 보자.'),
  ('장기 과제에서 실패 회복','10~15분 수준의 멀티스테이지 작업을 성공적으로 시연한다는 보고는 중요하지만 단계별 reset·개입 빈도·부분 성공 판정이 결과 해석을 좌우한다.','긴 시연 영상을 숫자 하나로 요약하지 말고 intervention count와 subtask completion을 보자.')],
 evidence=[
  ('목표 플랫폼 데이터','가정 환경 mobile manipulation 약 400h','원문 Introduction에 제시된 target-domain 데이터 규모.'),
  ('Pretraining data mixture','초기 학습 예시 97.6%는 타 출처','원문은 대부분의 사전학습 예시가 목표 mobile manipulator 가정 데이터가 아님을 보고.'),
  ('Long-horizon 실환경 작업','10–15분 수준','논문에 소개된 새로운 가정에서의 정리·청소·침대 정리 등의 사례.'),
  ('일반화 핵심 요인','co-training ablation','모든 세부 점수를 한 숫자로 요약하지 않고 구성 요소별 차이를 읽어야 한다.')],
 evidence_note='정량 환경별 성공률은 원논문의 V장·부록의 과제별 rubric과 함께 해석할 것. 장기 과제 시연은 모든 조건에서의 보편적 신뢰성 보증이 아니다.',
 comparison='π0가 다양한 로봇 제어를 위한 연속 flow-matching action expert의 능력을 강조한다면, π0.5는 여기에 **고수준 semantic task 예측·웹 지식·이질적 co-training·새 가정 평가**를 더해 open-world generalization을 겨냥한다.',
 reading_guide=[
  '사전학습 이산 action과 post-training flow-matching action이 어디서 교체되는지 모델 그림과 Section IV를 대조하기.',
  '웹 데이터, 고수준 subtask label, 타 로봇 시연 각각을 제거했을 때 성능이 얼마나 떨어지는지 ablation 확인하기.',
  '새 가정 데이터 누출이 없는지, 집/물체/과제의 split이 어떤 단위인지 보기.',
  '장기 작업 성공률뿐 아니라 각 subtask의 실패·사람 개입·총 작업 시간과 목표 완료 rubric을 분석하기.'],
 replication=dict(hypothesis='실제 모바일 조작 데이터가 적을 때 **semantic subtask co-training**은 action-only fine-tuning보다 낯선 실내 배치에서의 장기 성공률을 높일 것이다.',setup='개별 로봇 대상 5~10개 단계로 이루어진 책상 정리 task를 정의하고, 목표 로봇 시연을 고정한 채 web semantic data/subtask labels를 0/25/100%로 변동한다.',baselines='π0-style action-only, high-level language planner+fixed policy, π0.5-style joint subtask/action, no web data.',metrics='whole-task success, subtask success, novel-room success, human intervention, task duration, failed grasp recovery.',risks='실험실 영상·웹 라벨이 새로운 환경의 정답을 암묵적으로 포함하지 않도록 split을 엄격히 설정하자.'),
 related=['2410.24164','2503.14734','2610.42021']
)

D['2503.14734'] = dict(
 lead='GR00T N1은 humanoid를 위한 공개 기반 VLA로서 고수준 장면/언어 이해와 빠른 연속 동작을 **System 2 + System 1** 이중 구조로 분리·결합한다. 학습 데이터도 실제 로봇 궤적만이 아니라 인간 영상과 합성 데이터까지 포함한다. 연구 초점은 하나의 특정 손동작보다 서로 다른 형태와 과제에서 재사용 가능한 humanoid policy이다.',
 pipeline=[
  ('다양한 modality의 사전학습 데이터 수집','실제 로봇 시연, 인간 영상, 합성 trajectory를 결합한다. humanoid 외 타 embodiment도 학습 대상으로 포함한다.','입력: robot/human/synthetic mix'),
  ('System 2가 scene과 instruction 이해','vision-language module이 카메라와 언어 지시를 처리하고 조작 과제의 의미·환경 단서를 만든다.','중간: semantic/visual context'),
  ('System 1이 연속 action 생성','diffusion transformer가 빠른 모터 동작 시퀀스를 생성한다. 단지 language token으로 motor command를 직렬 출력하는 구조가 아니다.','출력: motor action trajectory'),
  ('두 모듈 공동 학습','이중 시스템을 느슨하게 연결한 파이프라인이 아니라 end-to-end 학습하며 로봇 형태에 맞게 제어 표현을 적용한다.','training: jointly optimized coupled modules'),
  ('시뮬레이션과 실물 humanoid 평가','다양한 embodiment의 standard simulation과 Fourier GR-1의 언어 조건 양팔 조작을 검증한다.','평가: sim multi-embodiment + real bimanual')],
 mechanisms=[
  ('System 2가 해소하는 문제','저수준 모터 패턴만 학습한 정책은 낯선 언어 지시·물체 개념에 취약할 수 있다. VLM 모듈이 의미 지식을 담당한다.','VLM만 교체해도 제어 성능이 향상되는지 ablation을 확인할 것.'),
  ('System 1과 action chunk','Motor diffusion transformer는 연속 제어 궤적을 생성한다. 한 step의 action loss와 chunk horizon, denoising 비용의 균형이 중요하다.','고정 주기 로봇 제어에서 추론 시간을 얼마나 점유하는지 확인하자.'),
  ('Cross-embodiment의 어려움','같은 “컵 집기”도 인간 손·그리퍼·humanoid 양팔의 action dimension과 기구학적 제한이 다르다. 데이터 혼합만으로 공통 표현을 얻었는지, 로봇별 adapter가 필요한지 중요하다.','평가 대상과 실제 제어를 지원하는 관절·팔·손 구성은 분리해 읽자.')],
 evidence=[
  ('공개 모델','GR00T N1 foundation VLA','이중 시스템 구조 및 공개 기반 모델을 제안한다.'),
  ('학습 소스','실제 로봇 + 인간 영상 + 합성 데이터','저자들이 제시한 이질적 학습 자료의 범주.'),
  ('시뮬레이션','다중 embodiment 평가','강한 imitation-learning baseline보다 우세하다는 저자 보고. 초록에는 통합 수치 없음.'),
  ('실제 로봇','Fourier GR-1 양팔 조작','language-conditioned bimanual task를 실험. 보행 및 균형 전체를 평가한 것은 아니다.')],
 evidence_note='같은 이름의 후속 GR00T 버전과 2025년 N1 논문을 구분할 것. 특정 제품 발표 자료의 성능을 N1 논문에 소급 적용하지 않는다.',
 comparison='일반 VLA처럼 vision-language와 motion을 한 함수로 다루면서도, 실제 구조는 **의미 해석과 확산 기반 모터 제어의 역할을 분리한 두 경로**로 되어 있다. π0 계열과 닮은 점도 있지만, GR00T N1은 humanoid·cross-embodiment 및 합성 데이터의 결합을 강조한다.',
 reading_guide=[
  'System 1이 받는 System 2의 토큰·feature 경로와 두 모듈의 공동 학습 조건을 확인하기.',
  '훈련 데이터 혼합에서 실제/인간/합성 비율과 robot morphology별 데이터 비율을 알아보기.',
  '시뮬레이션 benchmark의 robot 종류와 실물 Fourier GR-1 평가에서의 차이를 구분하기.',
  '팔·손 조작 성공률을 full-body humanoid locomotion/general autonomy로 과잉 해석하지 않기.'],
 replication=dict(hypothesis='정확한 humanoid 제어에 필요한 모터 다양성은 **합성 데이터**가, 언어적 일반화는 **웹·인간 영상**이 더 크게 기여할 것이다.',setup='동일 manipulation task를 단팔/양팔의 두 형태로 실행하고, synthetic trajectories와 human videos를 각각 on/off하는 2×2 fine-tuning 실험을 수행한다.',baselines='robot-only IL, robot+human, robot+synthetic, robot+human+synthetic.',metrics='각 형태의 task success, transfer to novel instruction, action frequency stability, data efficiency, end-to-end inference latency.',risks='합성 데이터 품질과 sensor 관측 구성의 차이가 modality 조합 효과를 가릴 수 있다.'),
 related=['2410.24164','2502.05855','2609.23578']
)

D['2502.05855'] = dict(
 lead='DexVLA는 VLM의 semantic 성능만 높이면 로봇 제어가 좋아진다는 단순 가정을 비판한다. **행동 생성기 자체를 대형 diffusion expert로 키우고**, 이를 다양한 embodiment에서 먼저 학습한 뒤 VLA와 정렬하고 새 작업에 적응시키는 단계적 훈련 레시피를 제안한다. action-space modeling이 로봇 일반화의 핵심이라는 입장이다.',
 pipeline=[
  ('1B diffusion action expert 사전학습','다양한 로봇 형태의 행동 데이터를 사용해 시각언어 모델과 분리 가능한 motor expert를 먼저 학습한다.','pretrain: cross-embodiment actions'),
  ('Embodiment-specific VLA 정렬','특정 로봇의 observation/action interface와 vision-language representation을 diffusion expert에 맞춘다.','align: VLM features ↔ action generation'),
  ('새로운 과제에 post-training','낯선 작업이나 추가 embodiment에 대해 적은 타깃 데이터로 적응한다.','adapt: new task, new robot'),
  ('연속 조작 행동 출력','언어 조건과 시각 입력을 해석해 diffusion head가 정밀 motor sequence를 생성한다.','output: continuous action chunk'),
  ('단팔·양팔·손 조작 검증','새로운 형태의 dexterous skill과 빨래 접기 같은 장기 과제를 시험한다.','test: single arm / bimanual / dexterous hand')],
 mechanisms=[
  ('Motor expert의 독립성','VLM과 action expert의 학습 역할을 분리하면 언어표현 학습과 정밀 행동 분포 모델링을 서로 다른 데이터에서 먼저 진행할 수 있다.','독립 pretrain이 데이터/계산비용을 절약하는지 adaptation 실험으로 확인하자.'),
  ('Embodiment curriculum','행동 공간이 다른 여러 로봇 데이터를 무작정 섞는 대신 모터 expert 사전학습→embodiment alignment→task post-training의 순서로 훈련한다.','curriculum 순서를 바꾼 ablation이 핵심 증거다.'),
  ('Diffusion 기반 연속 행동','정밀 동작에서 다중가능한 행동 분포를 표현하는 데 적합할 수 있지만, 여러 denoising step이 실제 inference 주기에 부담을 줄 수 있다.','모델 파라미터 규모뿐 아니라 rollout frequency와 latency를 측정할 것.')],
 evidence=[
  ('Action expert 규모','약 1B 파라미터','초록에 명시된 diffusion-based action expert.'),
  ('다양한 로봇 형태','single arm / bimanual / dexterous hand','여러 embodiment에서 학습·실험을 수행한다고 명시.'),
  ('대표 long-horizon 사례','laundry folding','직접 언어 지시를 사용한 장기 과제 수행을 보고.'),
  ('비교군','Octo·OpenVLA·Diffusion Policy','저자들은 우수한 성능을 보고하나 과제별 실제 수치는 본문 표에서 확인해야 한다.')],
 evidence_note='DexVLA의 비교 성능은 사용한 action head·task set·fine-tuning budget에 따라 달라진다. 초록만으로 단일 종합 우승률을 만들어내지 않는다.',
 comparison='OpenVLA가 거대 VLM 기반 공개 VLA와 파인튜닝을, π0가 flow-matching action expert를 강조한다면, DexVLA는 **큰 diffusion motor expert의 독립 사전학습 및 embodiment curriculum**으로 운동 제어의 병목을 공략한다.',
 reading_guide=[
  'action expert pretraining에 어떤 embodiment 데이터를 쓰고 서로 다른 action dimension을 어떻게 처리하는지 확인하기.',
  'curriculum 3단계 각각의 freeze/unfreeze 범위와 learning rate를 살펴보기.',
  '새로운 형태에 적은 데이터로 적응했다는 주장을 평가한 데이터 수·초기화·동일 baseline 확인하기.',
  '고주파 제어를 위해 diffusion denoising을 몇 step 수행하고 chunk length가 얼마인지 확인하기.'],
 replication=dict(hypothesis='모터 expert를 cross-embodiment 데이터로 먼저 훈련하면 target robot의 적은 시연으로도 안정된 연속 동작을 학습할 수 있다.',setup='UR5e와 양팔 task에서 robot-only action expert, cross-embodiment pretrained expert, VLM-heavy baseline을 동일 데이터 예산으로 adaptation한다.',baselines='no motor pretrain, motor expert pretrain only, staged embodiment curriculum, joint-from-scratch.',metrics='few-shot task success, training stability, action jerk, p95 inference latency, GPU-hour, unseen object recovery.',risks='expert의 파라미터 크기가 baseline보다 매우 크면 curriculum 자체의 효과라고 말하기 어렵다.'),
 related=['2406.09246','2410.24164','2503.14734']
)

D['2410.24164'] = dict(
 lead='π0의 핵심은 vision-language backbone의 의미 지식 위에 **flow matching으로 연속 robot action chunk를 생성하는 expert**를 붙인다는 데 있다. 이산 언어 토큰만 예측하는 정책은 빠르고 부드러운 로봇 제어에 부적합할 수 있고, 반대로 action-only policy는 언어 의미·새 물체에 취약하다. π0는 의미와 모터 제어를 함께 학습하면서도 출력을 다르게 취급한다.',
 pipeline=[
  ('이미지·언어·robot state 입력','시각 관측, 자연어 지시와 로봇의 현재 상태를 받아 VLM 조건 정보를 만든다.','입력: vision + instruction + proprioception'),
  ('Pretrained VLM의 semantic context 추출','시각과 언어의 의미 정보를 action head에서 사용할 수 있는 표현으로 전달한다. 인터넷 규모의 사전학습 지식을 조작 task에 연결한다.','조건 표현: visual-language features'),
  ('Flow matching으로 연속 action chunk 생성','연속 행동 시퀀스에 잡음을 둔 상태에서 방향장(velocity field)을 학습하고, 추론 시 이를 따라 action trajectory를 복원한다.','출력: temporally structured continuous actions'),
  ('다양한 embodiment 시연으로 공동 학습','단팔·양팔·모바일 매니퓰레이터의 행동 공간을 지원하는 정책을 사전학습한다.','데이터: heterogeneous manipulation demonstrations'),
  ('새 작업에 zero-shot 또는 fine-tuning','새로운 언어 명령을 그대로 수행하거나 상위 VLM이 제안한 subtask를 실행한다. target task에 추가 데이터를 주어 adaptation 성능을 본다.','검증: zero-shot / adapted skill / long tasks')],
 mechanisms=[
  ('Flow matching의 관점','action chunk를 독립된 discrete token으로 생성하기보다 연속 분포를 향하는 denoising trajectory로 본다. 이는 정밀 궤적 생성의 표현력을 얻는 대신 샘플링 단계의 계산비용이 생긴다는 뜻이다.','flow field의 supervision, noise schedule, inference step 수를 Section Model에서 확인할 것.'),
  ('Action chunk와 제어 주기','로봇은 수십 Hz 이상으로 행동하지만 큰 VLM은 한 순간에 한 토큰씩 느리게 출력할 수 있다. chunk 단위 행동 생성은 제어 빈도와 모델 추론비용의 타협이다.','rollout에서 새 observation을 얼마나 자주 반영하는지가 폐루프 정확도를 좌우한다.'),
  ('멀티로봇 데이터 통합','단팔, 양팔, 모바일 로봇의 동작 자유도·좌표계·gripper 표현은 다르다. 통합 모델의 강점은 이 차이를 관리하면서도 시각-언어 특성을 공유할 수 있다는 점이다.','action normalization, embodiment tokenization, robot-specific head를 살펴보자.')],
 evidence=[
  ('지원 로봇 형태','단팔·양팔·모바일 매니퓰레이터','원문 초록의 학습 데이터 구성을 기준으로 설명.'),
  ('평가 관점','zero-shot / language following / fine-tuning','사전학습 상태와 downstream 적응 조건을 따로 평가.'),
  ('대표 작업','laundry folding / table cleaning / box assembly','저자들이 대표적인 복합 조작 시연으로 보고.'),
  ('정량 수치','초록에 통합 성공률 미제시','과제별 결과를 논문의 정식 표/비디오와 함께 읽어야 한다.')],
 evidence_note='π0의 사례 영상은 정책이 해당 장면에서 성공할 수 있음을 보여주지만, 일반화 성공률은 과제별 반복 실험과 split을 함께 봐야 한다.',
 comparison='OpenVLA는 7B Llama 기반의 공개 action-token VLA에서 적응성을 연구했고, π0는 **연속적인 action-flow 기반 head**로 고주파·고정밀 조작을 겨냥한다. 후속 π0.5에서는 웹과 로봇 이질 데이터를 co-training하고 semantic subtask를 추가해 새 장소의 장기작업으로 확장한다.',
 reading_guide=[
  'VLM에서 action expert로 전달하는 조건 표현과 action dimension 정규화를 그림으로 추적하기.',
  'Flow matching loss와 noisy action trajectory의 시간 변수를 수식 수준에서 이해하기.',
  'Zero-shot 시연과 task-specific post-training 결과를 구분하고 각각의 데이터량을 확인하기.',
  '실제 action frequency, chunk horizon, resampling cadence와 latency가 closed-loop 성공에 주는 영향을 분석하기.'],
 replication=dict(hypothesis='같은 시각언어 backbone이라도 연속 flow-matching action head가 discrete action-token head보다 contact-rich skill에서 제어 품질을 높일 것이다.',setup='동일 로봇 및 시연 데이터에서 action head만 discrete / L1 regression / flow matching으로 바꿔 drawer close 및 precise insertion task를 평가한다.',baselines='OpenVLA-style discrete token, direct regression, diffusion head, π0-style flow head. backbone와 데이터는 동일하게 한다.',metrics='success, endpoint error, action jerk, gripper contact stability, p95 inference latency, control frequency.',risks='추론 step과 chunk length 차이가 그대로 성능 차이로 나타날 수 있으므로 compute-matched 비교도 함께 수행한다.'),
 related=['2504.16054','2406.09246','2502.05855']
)

D['2406.09246'] = dict(
 lead='OpenVLA는 VLA를 읽는 로보틱스 연구자가 가장 먼저 재현해 볼 만한 기준점이다. **7B 공개 모델**을 Llama 2 언어 backbone + DINOv2/SigLIP 시각 특징 + robot action 출력으로 구성하고, 약 **97만 개 실제 로봇 시연**으로 학습했다. 이 논문의 가치는 단지 높은 benchmark 점수보다 공개 체크포인트·학습 코드·LoRA·quantization 레시피에 있다.',
 pipeline=[
  ('Pretrained language·vision backbone 준비','Llama 2와 DINOv2, SigLIP의 서로 다른 시각 특징을 결합해 물체·장면과 언어 지시를 동시에 표현한다.','입력: RGB observation + language goal'),
  ('여러 robot dataset의 action 표준화','다양한 로봇 관절·gripper·coordinate frame을 모델에 학습 가능한 action 표기로 변환한다. preprocessing 선택이 downstream transfer에 직접적인 영향을 준다.','데이터: 약 970k real-robot demonstrations'),
  ('Vision-Language-Action 조건부 모델 학습','언어 지시와 관측으로 해당 embodiment의 action을 예측하도록 학습한다. 동작 토큰화와 action decoding 전략은 후속 OFT 연구에서 추가 개선 대상이 된다.','출력: robot action prediction'),
  ('새로운 환경에서 적응 및 경량화','LoRA를 이용한 적은 비용 fine-tuning과 quantization 기반 serving 실험을 통해 실제 연구실에서 접근 가능한 레시피를 제시한다.','적응: low-rank tuning + efficient inference'),
  ('새 물체·작업·형태에 대한 비교','여러 조작 task와 로봇 embodiment에서 pretrained 정책과 baseline의 성공률을 비교한다.','평가: multi-task generalist manipulation')],
 mechanisms=[
  ('DINOv2 + SigLIP 융합','DINOv2의 강한 visual representation과 SigLIP의 언어와 연결된 시각 의미를 함께 쓰려는 설계다. 언어 지시가 예측 action으로 전달될 때 한 종류의 visual encoder만으로 놓치는 신호를 보완할 수 있다.','vision encoder 한 가지를 제거한 ablation과 입력 해상도 의존성을 확인하자.'),
  ('Tokenized action의 장단점','이산 token 방식은 언어 모델 학습 방식과 잘 결합되지만 연속 action의 해상도·추론 빈도에 제한을 가할 수 있다. 이 점이 후속 OpenVLA-OFT의 continuous action/chunking 연구로 이어진다.','action bins·정규화·gripper encoding을 꼭 확인할 것.'),
  ('LoRA와 quantization','7B 전체를 매번 갱신하지 않고 low-rank parameter로 target task에 적응하면 작은 연구실도 실험할 수 있다. 양자화 inference에서 정확도 저하가 없는지 데이터셋별로 검증했다는 점이 실용적이다.','GPU 메모리·latency·학습 가능 parameter를 재현 노트에 남기자.')],
 evidence=[
  ('모델 크기','7B 파라미터','Llama 2 기반 공개 Vision-Language-Action 모델.'),
  ('학습 데이터','약 970k real-robot demos','여러 로봇 형태의 데이터 수집.'),
  ('RT-2-X 대비','+16.5%p 성공률','29개 task·여러 embodiment에서 비교한 저자 보고. 비교 데이터/조건을 직접 확인해야 함.'),
  ('Diffusion Policy 대비','+20.4%p','fine-tuning된 다중 작업 평가의 보고 결과. RT-2-X 비교와 실험 구성은 다르다.'),
  ('효율적 adaptation','LoRA + quantization','소비자급 GPU fine-tuning과 효율적 서빙 실험을 논문에 포함.')],
 evidence_note='16.5%p와 20.4%p는 서로 다른 baseline/평가 설정의 개선 폭. 두 숫자를 한 표에서 절대 모델 우열로 비교하면 안 된다.',
 comparison='Octo는 센서·action space가 다른 로봇으로 쉽게 파인튜닝하는 transformer generalist policy를 제공했고, OpenVLA는 **대형 pretrained VLM의 의미 지식과 공개 VLA 학습 파이프라인**을 핵심으로 삼는다. π0 계열의 연속 action 생성과 비교하면 discrete action의 속도·정밀도 trade-off를 검토하기 좋다.',
 reading_guide=[
  '로봇 action normalization과 tokenizer가 여러 hardware에서 동일한 의미를 갖는지 확인하기.',
  '29개 task에서의 baseline 설정·배포 주기·checkpoint selection이 공정한지 비교표 확인하기.',
  'LoRA rank, fine-tuning step, GPU memory 및 quantization 설정을 README/코드로 재현하기.',
  'OpenVLA 초기 모델과 OFT recipe의 성능을 혼동하지 않기. OFT는 별도 후속 연구다.'],
 replication=dict(hypothesis='작은 UR manipulator 데이터셋에서 OpenVLA LoRA 초기화가 from-scratch policy보다 새로운 물체·지시 조합에 강할 것이다.',setup='10개 물체 × 5개 동작 지시를 학습/미지 물체로 split한 뒤 단팔 카메라/손목 카메라를 동일하게 구성해 학습한다.',baselines='OpenVLA full fine-tune, LoRA 4/16/64, random-init policy, Diffusion Policy 동일 data budget.',metrics='in-domain/OOD success, language grounding accuracy, adaptation GPU-hour/VRAM, action latency.',risks='pretrained web 지식으로 대상 물체를 이미 알 수 있어 단순 물체 이름 일반화와 새로운 물리 기술 학습을 분리해야 한다.'),
 related=['2405.12213','2410.24164','2502.05855']
)

D['2405.12213'] = dict(
 lead='Octo는 ‘어느 로봇에서든 바로 최적의 action을 내는 단일 초거대 모델’보다 현실적인 목표인 **새 센서·새 행동 공간으로 빠르게 전이 가능한 공개 generalist policy 초기화**를 제시한다. 약 80만 trajectory의 Open X-Embodiment 데이터로 transformer를 사전학습하고, 언어 또는 목표 이미지로 조건화한다. fine-tuning의 쉬움 자체가 중요한 연구 기여다.',
 pipeline=[
  ('로봇마다 다른 관측·action 인터페이스 수집','Open X-Embodiment의 로봇 시연 약 800k trajectory를 학습 데이터로 사용한다. 카메라와 action 차원이 서로 다르다는 것이 실질적인 난점이다.','입력: heterogeneous sensor + action streams'),
  ('유연한 observation/task token 구조','Transformer가 sensor token과 language instruction 또는 goal image를 처리하도록 정책 입력을 구성한다.','조건: language goal 또는 image goal'),
  ('일반 정책 사전학습','다양한 task와 robot의 행동 패턴을 통합해 robot-independent initial representation을 만든다.','학습: generalist policy pretraining'),
  ('새 로봇의 입출력 헤드 조정','새 camera configuration이나 action dimension을 대상으로 일부 파라미터를 바꾸거나 fine-tuning한다.','adaptation: new observation & action space'),
  ('여러 로봇 플랫폼에서 검증','기존 파라미터를 활용한 fine-tuning이 새 task/domain에서 얼마나 빨리 배울 수 있는지 본다.','평가: 9 robot platforms')],
 mechanisms=[
  ('Goal image와 language instruction의 역할','‘컵을 집어’라는 언어 목표와 ‘이 상태를 만들어’라는 목표 이미지가 줄 수 있는 제약 정보는 다르다. 두 조건 모드를 공통 policy에서 지원하면 여러 robot dataset을 더 폭넓게 사용할 수 있다.','목표 종류가 바뀔 때 성공률과 action entropy가 어떻게 변하는지 보기.'),
  ('입력/출력의 모듈성','다른 로봇으로 이식할 때 모델 전체를 처음부터 다시 훈련하는 대신 해당 observation/action interface를 바꾸는 설계를 평가한다.','새 로봇 카메라·관절 수를 코드가 얼마나 쉽게 수용하는지 확인하자.'),
  ('작은 GPU에서의 적응','저자들은 일반 소비자 GPU에서 수 시간 내 fine-tuning 가능성을 강조한다. 실제 총시간은 시연 수·해상도·하드웨어에 따라 달라진다.','모델 비교 시 동일 training budget과 데이터 양을 맞춰야 한다.')],
 evidence=[
  ('사전학습 데이터','약 800k trajectories','Open X-Embodiment 데이터셋 기반.'),
  ('실험 하드웨어 범위','9개 로봇 플랫폼','새 센서와 action space로의 adaptation을 확인.'),
  ('Task instruction 종류','language / goal image','두 종류의 조건 표현을 지원한다.'),
  ('Fine-tuning 비용','소비자 GPU에서 수 시간 내','원문 초록의 적응성 보고. 설정마다 실행 시간은 다를 수 있다.')],
 evidence_note='초록에는 모든 플랫폼의 합산 성공률이 없어 여기서는 가짜 통합 점수를 만들지 않는다. adaptation 전후를 동일 task에서 비교해야 한다.',
 comparison='OpenVLA가 7B VLM의 semantic knowledge transfer를 중심에 둔다면 Octo는 **이질적인 로봇 센서·action interface에 대한 adaptable transformer policy**를 우선 목표로 둔다. 데이터 파이프라인과 fine-tuning 구현을 설계할 때 참고하기 좋은 선행 연구다.',
 reading_guide=[
  '서로 다른 action dimensions를 어떻게 mask/normalize하고 adaptation head를 어떻게 바꾸는지 확인하기.',
  'language-conditioned vs goal-image-conditioned training data의 비중과 성능 차이를 살펴보기.',
  '9개 로봇 플랫폼에서 pretrain initialization 대비 from-scratch의 차이를 task 별로 정리하기.',
  '공개 JAX/학습 코드의 센서 전처리 및 action chunk를 그대로 재현할 수 있는지 검토하기.'],
 replication=dict(hypothesis='센서 구성과 action space가 달라도 일반 정책 사전학습이 소량의 target 로봇 demonstration 효율을 높일 것이다.',setup='한 로봇에서 wrist camera 유무 및 6-DoF/7-DoF action head를 바꾼 뒤 20/50/100 trajectory로 fine-tuning한다.',baselines='Octo initialization, random initialization, OpenVLA fine-tuning. 동일 train/test split.',metrics='adaptation success vs trajectory count, calibration drift sensitivity, GPU-hour, OOD camera robustness.',risks='센서 전처리를 잘못하면 모델 자체보다 입력 도메인 이동이 성능을 결정하므로 표준화를 문서화해야 한다.'),
 related=['2406.09246','2403.12945','2502.05855']
)

D['2403.12945'] = dict(
 lead='DROID는 새로운 모델 구조가 아니라 **로봇 학습의 데이터 다양성 병목**을 정면으로 다룬다. 한 연구실에서 반복한 같은 환경의 대량 시연보다, 다른 장소·과제·조작자가 수집한 경험이 강인한 정책을 만드는 데 중요하다는 가설을 76k 시연의 분산 수집으로 시험한다. 데이터셋을 학습할 때 무엇을 ‘다양성’으로 측정할지 생각하기 좋다.',
 pipeline=[
  ('표준화된 로봇 수집 시스템 설계','지리적으로 분산된 수집자가 비슷한 하드웨어·수집 프로토콜을 사용하도록 재현 가능한 시스템을 제공한다.','수집 기반: reproducible robot setup'),
  ('다양한 실제 장면에서 시연 기록','50명 수집자가 12개월 동안 여러 대륙·장면에서 84개 작업을 수행했다. 실험실 한 공간에 집중된 데이터 분포를 넓힌다.','입력: RGB/proprioception/action demonstrations'),
  ('메타데이터·품질 확인·분할','scene/task/operator/robot setup 등 분할 단위를 명확하게 기록해야 과대평가 없는 일반화 실험을 할 수 있다.','필수: task/scene diversity metadata'),
  ('로봇 정책 학습용 데이터 공개','데이터와 학습 코드, 하드웨어 재현 가이드가 공개돼 외부 연구자가 다양한 데이터 섞기 실험을 할 수 있다.','산출물: dataset + code + hardware guide'),
  ('Cross-scene generalization 평가','DROID 데이터를 사용한 정책이 기존 단일 환경 데이터에 비해 성능·일반화에서 이득을 내는지 실험한다.','검증: novel scene / task robustness')],
 mechanisms=[
  ('시연 수와 경험 분포의 차이','76k 시연이 많다는 것만으로 강한 데이터가 되는 게 아니다. 564개 장소와 84개 작업의 분산이 물체·배경·광량·관측 시점의 다양성을 늘린다는 점이 중요하다.','성능 기여를 따질 때 scene diversity를 시연 수와 분리해 측정해야 한다.'),
  ('Collector 및 hardware 편차','사람별 조작 습관과 캘리브레이션 편차가 노이즈가 될 수도, 강건성 학습의 기회가 될 수도 있다.','수집자·로봇별 평가 split에서 실제 장점과 노이즈 영향을 살펴보자.'),
  ('Offline 데이터의 한계','정답 action이 있는 관측만 모으면 policy가 한번 실패해 미지 상태로 진입했을 때 복구 동작을 배우기 어렵다. 대규모 데이터도 action-coverage 문제를 완전히 없애지는 못한다.','실패 상태·보정 시연 포함 여부를 확인하자.')],
 evidence=[
  ('Demonstration 수','약 76,000 trajectories','원논문에서 제시한 전체 시연 수.'),
  ('Interaction time','약 350시간','수집된 로봇 interaction 데이터 길이.'),
  ('Scene diversity','564개 장면','동일 실험실 반복보다 폭넓은 장소 구성.'),
  ('Task·collector 규모','84 tasks · 50 collectors','북미·아시아·유럽 12개월 수집.'),
  ('학습 효과','일반화 개선 보고','저자들은 DROID 학습으로 성공률과 일반화가 높아진다고 보고; 구체적 조건은 본문 표 확인.')],
 evidence_note='76k trajectories와 350시간은 데이터셋 규모 지표이지 모델 성능 점수가 아니다. 데이터 중복과 task/scene split 기준을 확인해야 한다.',
 comparison='데이터가 제한된 robot imitation learning이나 특정 실험실 중심 수집 방식보다 DROID는 **distributed in-the-wild demonstration collection**을 통해 다양한 실세계 장면을 포괄한다. 일반 정책 모델 논문인 Octo/OpenVLA를 이해하려면 어떤 데이터 분포를 학습했는지 함께 읽을 필요가 있다.',
 reading_guide=[
  'scene split인지 trajectory random split인지 확인해 테스트 누출 가능성을 평가하기.',
  '50명 collector 사이의 제어 방식·라벨 품질·하드웨어 캘리브레이션 차이가 정리돼 있는지 확인하기.',
  'scene 수를 고정하고 시연 수만 늘리는 실험 vs 시연 수를 고정하고 scene 수를 늘리는 실험을 구분하기.',
  '데이터 라이선스·개인정보·물체/장면 촬영 이슈 및 재현 하드웨어 비용을 확인하기.'],
 replication=dict(hypothesis='같은 trajectory budget이라면 여러 환경의 데모가 한 환경에 집중된 데모보다 unseen-scene generalization에 유리할 것이다.',setup='UR/Franka 조작 과제에서 총 500 trajectory를 고정하고 1/5/20개 실환경으로 나눠 수집한 뒤 VLA 정책을 동일 훈련스텝으로 학습한다.',baselines='single-scene 많은 시연, multi-scene 균등 시연, weighted scene-balanced sampling, DROID-pretrained initialization.',metrics='novel-scene success, OOD object success, 데이터 수집 총비용, 환경별 성능 편차, success CI.',risks='환경 수를 늘릴수록 task difficulty도 변하면 다양성 자체의 효과와 과제 난이도 영향이 섞일 수 있다.'),
 related=['2405.12213','2406.09246','2504.16054']
)
