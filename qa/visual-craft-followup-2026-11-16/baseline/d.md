# 작업실 러프 행동/공개 비트

status: draft — 텍스트 제안, 실제 동작·가독성 미검증.

목표: 봉투의 배송번호 확인. 승인된 대체 수단은 봉투 방향을 바꿔 창의 자연광을 받는 것뿐이다. 실제 번호는 미정이다. 봉투·휴대등의 현재 소유자와 위치, B의 빈손 여부는 제공되지 않았으므로 확정하거나 임의로 넘기지 않는다.

선택한 구조와 이유: 5비트. **B의 우선순위는 굴러오는 상자 대응 → 잔류 위험 확인 → 조건이 허용할 때 번호 확인 재개.** A는 이미 전시판을 지지하므로 그 역할을 갑자기 해제하지 않는다.

## 인과 비트 / Plot(관객 공개 배열)

1. **실패와 병행 위협 공개.** B가 휴대등 점등 실패를 확인하는 안을 제안한다. 원인은 주어진 배터리 부족이며 재시도·충전으로 해결하지 않는다. A는 전시판을 계속 잡고, 상자는 다른 방향에서 계속 굴러온다. 관객에게 상자를 먼저 공개한다. **모름:** A는 점등 실패를 보았는지 미정, B는 아직 상자 접근을 보지 못한 상태로 제안. 둘 다 번호를 모른다.
2. **주의 전환.** B의 시선이 상자에 닿아 번호 확인을 중단한다. A에게 접근 방향을 알리되 A의 손은 전시판에 남긴다. 봉투·휴대등은 직전 소유·위치를 유지한다. **모름:** A의 경고 인지 여부는 반응 전 미확인. B는 상자를 제때 막을 수 있는지 모른다.
3. **한 위협에만 개입.** B가 발로 상자를 막으려 한다. 접촉·정지는 성공으로 확정하지 않는다. 성공 분기에서도 발의 제지가 남아 있어야 하며, 실패하면 상자는 계속 움직여 이후 읽기 시도를 보류한다. A의 지지는 지속된다. **모름:** 두 인물 모두 전시판이 손을 놓아도 버틸지는 확인하지 않았다.
4. **조건부 목표 복귀.** 상자가 실제로 제지되고 그 접촉을 유지할 수 있을 때만 봉투 접근·빈손·자연광 도달 여부를 확인한다. 조건이 맞으면 현재 봉투 보유자가 방향만 바꾼다. B가 보유자라고 단정하지 않는다. **모름:** A·B 모두 자연광에서 번호가 판독될지 아직 모른다.
5. **미해결 끝 상태.** 배송번호를 읽으려는 시도에서 멈춘다. 번호 정답이나 판독 성공은 공개하지 않는다. A는 여전히 전시판을 잡고, 상자는 직전 분기의 이동/제지 상태, 봉투는 회전했다면 그 방향을 유지한다. **모름:** A·B 모두 실제 번호와 전체 위험 해소 여부를 모른다.

미확인 사항: 상자 접촉 가능성, 동시 지지·제지의 지속 가능성, 봉투 접근·자연광·판독성. 물리 수치·Blender·이미지 생성 및 실제 시각 검사는 수행하지 않았다.

## 읽은 참조 경로
- video-production-assets/SKILL.md
- video-production-assets/references/workspace-integration.md
- video-production-assets/references/contract.md
- video-production-assets/references/02-story.md
- video-production-assets/assets/02-story-template.md
- video-production-assets/references/visual-scene-communication.md
- video-production-assets/references/26-state-causality-continuity.md
- video-production-assets/references/performance-and-style-recipes.md (§진행 중 과제)
- video-production-assets/references/world-rules-and-information-recipes.md (§발화·믿음, §지식의 한계)
