# Codex 작업 인계 프롬프트

아래 내용을 새 Codex 작업의 첫 프롬프트로 사용한다.

---

`unreal-editor-skills-for-codex` 프로젝트 작업을 이어서 진행해줘.

## 프로젝트 목적과 현재 상태 확인

Epic Games의 공개 저장소
`https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin`에서
Unreal Editor 작업 지침을 가져와 Codex의 Plugin, Skill, MCP, Hook 구조에 맞게
유지하는 커뮤니티 프로젝트다. 사용자에게 승인받은 Codex 확장은 Epic 변경과
구분한다. 설계·제작 판단은 별도 Unreal Development Handbook for Codex가 담당한다.

버전은 이 문서의 과거 숫자 대신 `.codex-plugin/plugin.json`에서 읽고,
해당 `docs/releases/` 기록과 공개 태그를 비교한다. 설치본의
`+codex.<timestamp>`는 로컬 갱신 식별자이며 별도 공개 릴리스가 아니다.
작업 파일, 커밋, 공개 릴리스, 설치 캐시, 새 세션의 로딩 상태를 각각 확인한다.

- 플러그인: `unreal-editor-skills-for-codex`
- 공개 설치: `unreal-editor-skills-for-codex@fairypark`
- 개인 설치: `unreal-editor-skills-for-codex@personal`
- 공개 MCP 기본 주소: `http://127.0.0.1:8000/mcp`
- 프로젝트별 포트와 개인 설정은 공개 패키지에 섞지 않는다.

## 주요 구성

- `unreal-mcp`: 연결 사전 점검, Toolset 탐색과 안전한 Editor 실행.
- `create-toolset`: Unreal C++·Python Toolset 제작.
- `unreal-skill`: Unreal Editor 내부 Agent Skill 제작·관리.
- `environment-level-design`: 승인된 설계의 환경 제작, 저장, PIE와 증거 검증.
- `building-grounding`: 건물의 네 모서리 지지·지형 접촉 검증.
- `unreal-usage-metrics`: 명시적 동의에 따른 선택적 로컬 사용량 관리.
- `hooks/`: 프로젝트 컨텍스트 및 분리된 사용량 Hook 연결.
- `docs/VALIDATION.md`: Windows 회귀 검사와 공식 Plugin·Skill 검증 절차.
- `LICENSE`, `THIRD_PARTY_NOTICES.md`: 원본 저작권·라이선스·비제휴 고지.

## 작업 시작과 업데이트

1. `AGENTS.md`, `README.md`, 매니페스트와 현재 Git 상태를 확인한다.
   기존 수정·미추적 파일을 보존하고, 오래된 HEAD 때문에 이미 배포된 파일이
   수정 또는 미추적으로 보이는지 실제 내용을 비교한다.
2. 업데이트 요청이면 작업 파일과 HEAD 각각의 `THIRD_PARTY_NOTICES.md` 기준을
   Epic 최신 리비전과 비교하고 변경 사항을 먼저 요약한다. 적용·검토한 변경만
   upstream 리비전에 반영한다. 관련 없는 기능이나 리팩터링을 추가하지 않는다.
3. 동의·수집·Hook·배포 변경 전 `docs/USAGE_METRICS.md`를 읽는다.
   명시적 동의 전에는 수집하지 않으며, 비활성화와 삭제를 구분한다.
   프롬프트, 응답, 경로, 프로젝트·객체명, 도구 인수·응답, 원시 식별자는 저장하거나
   전송하지 않는다. Epic 파생 Skill과 컨텍스트 Hook에 지표 로직을 넣지 않는다.
4. `docs/VALIDATION.md`의 회귀 및 공식 검증을 실행한다. Hook을 변경하면 세션
   컨텍스트·동의·비활성화·삭제·개인정보 시나리오도 확인한다. stage, commit,
   push, publish 전에 정확한 파일 목록과 구성된 비밀정보 검사를 확인한다.
5. 공개 릴리스와 로컬 설치를 구분한다. 개인 마켓플레이스가 가리키는 소스를
   확인하고 공식 `plugin-creator`의 `read_marketplace_name.py`와
   `update_plugin_cachebuster.py`를 사용한 뒤
   `codex plugin add unreal-editor-skills-for-codex@personal`로 재설치한다.
   마켓플레이스 설정을 임의로 편집하지 않는다.
6. 설치 파일의 버전·해시와 새 Codex 세션의 Skill 로딩을 검증한다. 기존 대화가
   자동으로 새 지침을 다시 읽었다고 주장하지 않는다.

## Unreal 실행과 증거 범위

- 라이브 작업은 활성 프로젝트·월드·MCP 연결을 읽기 전용으로 확인한 뒤 시작한다.
- game-thread 변경과 서로 의존하는 호출은 순차 실행한다.
- 큰 변경 전 복구 지점을 확보하고, 변경 후 컴파일·저장·재조회·필요한 PIE를 확인한다.
- 새 레벨·대규모 변경은 승인된 설계와 평면도를 구현하며, Handbook이 없으면
  독립 실행용 최소 계약과 plan-feature 기록을 사용한다.
- 블록아웃 승격은 독립 검토를 거친다. 대표 구간의 임시 큐브 교체·퇴역은 그
  구간의 승인 전에 검증하고, 제작 범위가 커질 때 범위를 확장해 다시 확인한다.
- 설치·정적 검사 통과는 Unreal 렌더링, 플레이, cook, 성능 또는 배포 준비 완료의
  증거가 아니다. 실행하지 않은 검증과 남은 제한을 명시한다.
- Unreal Engine 소스·바이너리·로고 또는 배포 권한 없는 에셋을 포함하지 않으며,
  Epic Games·OpenAI·Anthropic의 공식 제품으로 표현하지 않는다.

먼저 현재 상태와 이번 작업 범위를 확인하고, 이미 주어진 사용자 승인을 이어서
적용해 검증과 결과 보고까지 진행해줘.
