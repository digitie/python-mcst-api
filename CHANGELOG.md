# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- `maplibre-vworld-js` 프로젝트의 MCP 에이전트 설정 파일(`antigravity.json`, `claude.json`, `codex.json`, `.gemini/`, `.claude/`, `.codex/`) 도입.
- 작업 연속성 보장을 위한 `journal.md`, `tasks.md`, `decisions.md` 도입 및 `AGENTS.md` 갱신.
### Changed
- Windows worktree 환경에서 WSL 기본 `git` 대신 Windows Git (`git.exe`)를 사용하도록 개발/에이전트 문서를 정리하고 `.codegraph/`를 gitignore에 추가.
