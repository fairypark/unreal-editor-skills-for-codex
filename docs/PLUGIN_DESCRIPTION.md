# Plugin introduction copy

## English

### One-line

Control and extend a live Unreal Editor from Codex with safe, discoverable MCP workflows.

### Short

Unreal Editor Skills for Codex connects Codex to a running Unreal Editor through Unreal's
Model Context Protocol support. It helps Codex inspect levels, work with Actors and assets,
author or extend ToolsetRegistry tools, and create project-specific Unreal Agent Skills
while following Unreal-aware safety and verification practices. Its environment skill executes
approved level designs through Landscape, PCG, Foliage, materials, collision, fixed-camera
evidence, and runtime verification. The separately installable Unreal Development Handbook for
Codex can provide the design-first and validation-first reasoning contract before execution.

Optional local usage metrics can help evaluate reliability and workflow quality. They are
off until the user explicitly opts in, remain on the user's device, never store prompts,
paths, Actor or Asset names, tool arguments, or response contents, and can be disabled or
deleted at any time.

### Release-page

Unreal Editor Skills for Codex brings Epic's Unreal Engine agent workflows to Codex-native
Plugin, Skill, MCP, and Hook structures. Connect it to a live Unreal Editor to discover
toolsets on demand, inspect or modify Editor state, build AI-callable C++ or Python tools,
preserve project knowledge as Unreal Agent Skills, and execute repeatable environment workflows
without imposing one project's art direction on another. The plugin remains independently usable
and can consume planning and validation contracts from Unreal Development Handbook for Codex when
that companion plugin is installed.

The plugin emphasizes recoverable changes, sequential game-thread calls, explicit result
checking, and verification after mutation. Its optional usefulness metrics are consent-based
and local-only, giving users transparent controls to enable, disable, summarize, rate, or
delete the collected operational signals.

This is a community-maintained MIT-licensed port and is not affiliated with or endorsed by
Epic Games, OpenAI, or Anthropic.

## 한국어

### 한 줄 소개

Codex에서 실행 중인 Unreal Editor를 안전하게 제어하고 확장할 수 있는 MCP 워크플로 플러그인입니다.

### 짧은 소개

Unreal Editor Skills for Codex는 Unreal의 Model Context Protocol 지원을 통해 Codex와 실행
중인 Unreal Editor를 연결합니다. 레벨과 Actor·Asset을 조사하거나 변경하고,
ToolsetRegistry 기반의 AI 호출 가능 도구를 작성하며, 프로젝트 전용 Unreal Agent Skill을
만드는 작업을 Unreal 규칙과 안전 절차에 맞게 수행하도록 돕습니다. 환경 스킬은 승인된
레벨 설계를 Landscape, PCG, Foliage, 재질, 충돌, 고정 카메라 증거와 런타임 검증 작업으로
실행합니다. 별도 설치 가능한 Unreal Development Handbook for Codex가 설계 우선·검증 우선
계약을 먼저 제공할 수 있습니다.

선택적 로컬 사용 지표를 통해 호출 안정성, 재시도, 변경 후 검증 여부와 같은 워크플로
품질을 확인할 수 있습니다. 사용자가 명시적으로 동의하기 전에는 수집하지 않으며,
프롬프트·경로·Actor/Asset 이름·도구 인수·응답 내용은 저장하지 않습니다. 모든 데이터는
사용자의 기기에만 남고 언제든 수집을 끄거나 삭제할 수 있습니다.

### 배포 페이지용

Unreal Editor Skills for Codex는 Epic의 Unreal Engine 에이전트 워크플로를 Codex의 Plugin,
Skill, MCP, Hook 구조에 맞게 이식한 커뮤니티 플러그인입니다. 실행 중인 Unreal Editor에
연결해 필요한 Toolset을 동적으로 찾고, Editor 상태를 조사하거나 수정하고, C++ 또는
Python 기반 AI 도구를 만들며, 프로젝트 지식을 Unreal Agent Skill로 보존할 수 있습니다.
플러그인은 단독으로 동작하고, 동반 Handbook이 설치되어 있으면 그 설계와 검증 계약을
실제 Editor 실행으로 이어받습니다.

복구 가능한 변경, Unreal game thread 호출의 순차 실행, 명시적인 결과 확인, 변경 후
검증을 중요하게 다룹니다. 선택적 유용성 지표는 명시적 동의와 로컬 저장을 원칙으로
하며, 사용자가 자연어로 활성화·비활성화·요약·평가·삭제할 수 있습니다.

MIT 라이선스로 제공되는 커뮤니티 유지보수 포트이며 Epic Games, OpenAI 또는 Anthropic의
공식 제품이나 보증을 받은 프로젝트가 아닙니다.
