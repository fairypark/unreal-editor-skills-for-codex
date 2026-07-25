# Codex 작업 인계 프롬프트

아래 내용을 새 Codex 작업의 첫 프롬프트로 사용한다.

---

`unreal-editor-skills-for-codex` 프로젝트 작업을 이어서 진행해줘.

## 프로젝트 목적

Epic Games의 공개 저장소
`https://github.com/EpicGames/unreal-engine-skills-for-claude-code-plugin`
에서 유용한 Unreal Editor 작업 지침을 분석해 Codex용 플러그인으로 재구성한 프로젝트다.
Claude Code 전용 표현을 그대로 복제하지 않고 Codex의 Plugin, Skill, MCP, Hook 구조에 맞게
적응시키는 것이 목표다.

## 현재 상태

- 플러그인 이름: `unreal-editor-skills-for-codex`
- 기본 버전: `0.1.1`이며 로컬 재설치 시 Codex cachebuster suffix가 추가될 수 있다.
- 개인 마켓플레이스 이름: `personal`
- 개인 마켓플레이스 엔트리:
  `unreal-editor-skills-for-codex@personal`
- 마켓플레이스의 로컬 소스 경로는 새 프로젝트를 가리키도록 연결되어 있다.
- Codex Plugin 및 Skill 정적 검증을 통과했다.
- 세션 훅은 `.uproject`와 프로젝트별 `.codex/config.toml`을 감지하도록 시험했다.
- Unreal Engine 5.8과 프로젝트별 포트 `8008` 오버라이드에서 MCP 초기화, 세 메타 도구,
  Toolset 탐색, Agent Skill 조회, 현재 레벨 및 Actor 읽기 전용 라이브 시험을 통과했다.
- 공개 플러그인의 기본 MCP 포트는 Unreal 공식 기본값인 `8000`이다.

## 주요 구성

- `.codex-plugin/plugin.json`
  - Codex 플러그인 매니페스트와 starter prompts
- `.mcp.json`
  - `http://127.0.0.1:8000/mcp`의 `unreal-mcp` 서버 연결
- `hooks/unreal-context.ps1`
  - Unreal 프로젝트와 엔진 소스 트리를 감지하여 세션 컨텍스트 제공
- `skills/unreal-mcp`
  - `list_toolsets`, `describe_toolset`, `call_tool` 기반 도구 탐색과 실행
- `skills/create-toolset`
  - C++ 및 Python 기반 Unreal MCP Toolset 제작 지침
- `skills/unreal-skill`
  - Unreal Editor 내부 Agent Skill과 Codex Skill의 역할 구분 및 제작 지침
- `LICENSE`, `THIRD_PARTY_NOTICES.md`
  - MIT 라이선스와 Epic Games 원본 저작권 및 비제휴 고지

## 유지해야 할 안전 원칙

- Unreal game-thread 변경 작업은 병렬 호출하지 않고 순차 실행한다.
- 긴 변경 전에는 저장 또는 체크포인트를 확보한다.
- Blueprint 컴파일, 에셋 저장, PIE 상태 및 도구 반환값을 확인한다.
- 임의 Python 실행처럼 권한이 큰 도구는 필요한 경우에만 사용한다.
- Unreal Engine 소스, 바이너리, 로고 등 재배포 권한이 없는 자료를 저장소에 포함하지 않는다.
- Epic Games 또는 OpenAI의 공식 제품처럼 표현하지 않는다.
- 기존 MIT 저작권 및 제3자 고지를 보존한다.

## 작업 시작 절차

1. `README.md`, `.codex-plugin/plugin.json`, `.mcp.json`을 먼저 읽는다.
2. 현재 파일 상태와 사용자 변경사항을 확인하고 보존한다.
3. Plugin 또는 Skill을 수정하면 공식 validator를 다시 실행한다.
4. 로컬 플러그인 업데이트 시 `plugin-creator`의
   `update_plugin_cachebuster.py`를 사용하고
   `codex plugin add unreal-editor-skills-for-codex@personal`로 재설치한다.
5. 플러그인을 재설치한 뒤에는 새 Codex 작업에서 로딩 상태를 확인한다.
6. 라이브 시험 시 Unreal Editor에서 Model Context Protocol 플러그인과 필요한 Toolset을
   활성화하고 `ModelContextProtocol.StartServer`로 MCP 서버를 시작한 후 읽기 전용
   조회부터 시험한다. 프로젝트가 다른 포트를 사용하면 해당 포트를 명시한다.

이전 작업의 핵심 판단은 “일반적인 파일 편집만으로도 Unreal 작업은 가능하지만, 반복적인
에디터 조작에서는 MCP 기반 도구 탐색, 저장·검증 규칙, 순차 실행 지침을 플러그인으로
표준화하면 시간 단축과 안정성 향상을 기대할 수 있다”는 것이다.

먼저 프로젝트 상태를 점검하고 현재 구현과 검증 결과를 요약한 뒤, 사용자의 다음 요청을
이어 받아 작업해줘.
