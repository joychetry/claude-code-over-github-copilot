# Claude Code over GitHub Copilot 모델 엔드포인트 - 설정 가이드

**한국어** | [English](README.md)

## 개요

이 프로젝트는 Anthropic 서버 대신 GitHub Copilot을 통해 Claude Code를 사용할 수 있게 해줍니다.
회사 정보를 Anthropic에 전송할 수 없지만, VSCode 및 IDEA 에이전트를 위해 이미 GitHub Copilot과 계약을 맺은 상태입니다.

아키텍처 구성:
- **변환 레이어**: Claude Code와 GitHub Copilot API 간 변환을 위한 LiteLLM 프록시
- **로컬 프록시**: 로컬에서 실행되는 LiteLLM (외부 트래픽 없음)
- **GitHub 통합**: 이미 사용 승인된 GitHub Copilot 모델에 직접 연결

**참고 자료:**
- [Claude Code LLM 게이트웨이 문서](https://docs.anthropic.com/en/docs/claude-code/llm-gateway)
- [LiteLLM 빠른 시작](https://docs.litellm.ai/#quick-start-proxy---cli)
- [LiteLLM GitHub Copilot 프로바이더](https://docs.litellm.ai/docs/providers/github_copilot)

## 빠른 시작

### 1. Claude Code 설치 (미설치 시)
```bash
# npm을 통해 Claude Code 데스크톱 애플리케이션 설치
make install-claude
```

이 명령은 npm을 사용하여 Claude Code를 전역으로 설치합니다. Node.js와 npm이 설치되어 있어야 합니다.

### 2. 초기 설정
```bash
# 환경 설정, 의존성 및 API 키 생성
make setup
```

이 명령은:
- Python 가상 환경 생성
- LiteLLM 프록시 서버 및 필수 의존성 설치
- `.env` 파일에 UUID 기반 랜덤 API 키 생성 (파일이 없는 경우에만)

### 3. Claude Code 설정
```bash
# Claude Code를 로컬 프록시 사용하도록 설정
make claude-enable
```

이 명령은:
- 기존 Claude Code 설정 백업
- `http://localhost:4444`를 API 엔드포인트로 설정
- 모델 매핑 설정 (claude-sonnet-4.5, gpt-4)

### 4. 프록시 서버 시작
- **중요**: 첫 실행 시 GitHub 디바이스 인증이 필요합니다 - 터미널의 안내를 따르세요
```bash
# LiteLLM 프록시 서버를 백그라운드로 시작
make start
```

실행 내용:
- `copilot-config.yaml` 설정으로 백그라운드에서 LiteLLM 시작
- `logs/YYYYMMDD_HHMMSS.log`에 로그 저장
- 프로세스 관리를 위한 PID 파일 생성

### 5. 연결 테스트
```bash
# 모든 것이 정상 작동하는지 테스트
make test
```

### 6. 프로젝트 폴더에서 Claude Code 시작

```bash
# 프로젝트 폴더에서 Claude Code 열기
claude
```

## 모델 설정

프록시가 Claude Code에 노출하는 모델:

| Claude Code 모델 | GitHub Copilot 모델 매핑         |
|-------------------|----------------------------------|
| `claude-sonnet-4.5` | `github_copilot/claude-sonnet-4.5` |
| `gpt-4`         | `github_copilot/gpt-4`         |

## 추가 명령어

### 서버 관리
```bash
# 프록시 서버 실행 상태 확인
make status

# 실시간 로그 확인
make logs

# 프록시 서버 중지
make stop
```

### 사용 가능한 모델 목록 조회
```bash
# 사용 가능한 모든 GitHub Copilot 모델 목록 조회
make list-models

# 활성화된 GitHub Copilot 모델만 목록 조회
make list-models-enabled
```

이 명령은 GitHub API에서 직접 GitHub Copilot 모델을 가져와 `copilot-config.yaml`에 추가할 수 있는 YAML 형식으로 표시합니다.

**참고**: 이 명령은 GitHub 인증이 필요합니다. 먼저 `make start`를 실행하여 인증하세요.

### 상태 확인
```bash
# 현재 Claude Code 설정 및 프록시 상태 확인
make claude-status
```

### 원래 설정으로 복원
```bash
# Claude Code를 기본 Anthropic 서버로 복원
make claude-disable
```

## 문제 해결

- **서버 상태 확인**: `make status`를 사용하여 프록시 실행 여부 확인
- **로그 확인**: `make logs`를 사용하여 실시간 서버 로그 확인
- **인증 문제**: 첫 `make start` 실행 시 GitHub 인증 프롬프트가 표시됩니다
- **연결 문제**: `make test`를 사용하여 프록시가 작동하는지 확인하세요
- **설정 문제**: `make claude-status`를 사용하여 설정을 확인하세요
- **전체 리셋**: `make claude-disable` 후 `make claude-enable`을 실행하여 재설정하세요
