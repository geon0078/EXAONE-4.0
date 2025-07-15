<div align="center">
  <img src="assets/EXAONE_Symbol+BI_3d.png" alt="EXAONE Logo" width="200"/>
</div>

# EXAONE 4.0 Interactive Chat Interface

EXAONE 4.0 모델을 사용한 GPU 최적화 대화형 인터페이스입니다.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)

## 🚀 특징

- **🔥 GPU 가속**: CUDA 지원으로 빠른 추론 속도 (CPU 대비 10-20배)
- **🌍 다국어 지원**: 한국어, 영어, 스페인어 등 다양한 언어 지원
- **⚡ 메모리 최적화**: bfloat16 정밀도와 스마트 메모리 관리
- **📊 실시간 모니터링**: GPU 메모리 사용량 실시간 표시
- **🛡️ 안정성**: 강력한 에러 처리 및 graceful shutdown

## 📁 파일 구성

- `interactive_chat.py`: 계속해서 입력을 받는 대화형 인터페이스
- `simple_example.py`: 기본적인 단일 실행 예제
- `requirements.txt`: 필요한 패키지 목록

## 🛠️ 설치 및 실행

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 대화형 인터페이스 실행
```bash
python interactive_chat.py
```

### 3. 간단한 예제 실행
```bash
python simple_example.py
```

## 💬 사용법

### 대화형 인터페이스 (`interactive_chat.py`)
- 프로그램 실행 후 프롬프트에 원하는 텍스트를 입력하세요
- 종료하려면 `quit`, `exit`, `종료`, `q` 중 하나를 입력하세요
- GPU 메모리 사용량이 실시간으로 표시됩니다

### 예제 입력
```
사용자: 안녕하세요! 오늘 날씨가 어때요?
사용자: Explain quantum computing in simple terms
사용자: ¿Cómo estás hoy?
```

## ⚙️ 시스템 요구사항

- Python 3.8+
- PyTorch 2.0+
- transformers 4.30+
- CUDA 지원 GPU (권장)

## 🔧 GPU 설정

코드는 자동으로 CUDA 사용 가능 여부를 감지합니다:
- GPU 사용 가능: 자동으로 GPU에서 실행
- GPU 없음: CPU로 자동 fallback

## 📊 성능

- **GPU 가속**: CPU 대비 10-20배 빠른 추론 속도
- **메모리 효율**: bfloat16 사용으로 메모리 사용량 50% 절약
- **실시간 응답**: 평균 1-3초 내 응답 생성

## 🤝 기여

이 프로젝트는 LG AI Research의 EXAONE 4.0 모델을 기반으로 합니다.

### 🔗 관련 링크
- **원본 모델**: [LGAI-EXAONE/EXAONE-4.0-1.2B](https://huggingface.co/LGAI-EXAONE/EXAONE-4.0-1.2B)
- **EXAONE 공식 저장소**: [LG AI Research EXAONE](https://github.com/LG-AI-EXAONE)
- **논문**: [EXAONE 3.0 7.8B Instruction Tuned Language Model](https://arxiv.org/abs/2408.03541)

### 📈 개선사항 제안
- 버그 리포트나 기능 제안은 [Issues](https://github.com/geon0078/EXAONE-4.0/issues)에서 해주세요
- Pull Request는 언제나 환영합니다!

## 📄 라이선스

이 프로젝트는 Apache 2.0 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## ⚠️ 주의사항

- EXAONE 모델 사용 시 LG AI Research의 이용 약관을 준수해주세요
- 상업적 사용 시 해당 라이선스를 확인하시기 바랍니다
- 생성된 콘텐츠에 대한 책임은 사용자에게 있습니다

---

<div align="center">
  Made with ❤️ by the EXAONE Community
</div>
