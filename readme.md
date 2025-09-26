## 📦 Git LFS 파일 다운로드 안내

이 저장소는 **Git Large File Storage (LFS)** 를 사용하여 대용량 파일을 관리합니다.  
단순히 `git clone`만 하면 실제 파일이 아닌 **포인터 파일**만 내려받게 되므로, 아래 절차에 따라 Git LFS를 설치하고 동기화해야 합니다.

---

### ✅ 1. Git LFS 설치

👉 [공식 사이트](https://git-lfs.com/)에서 설치 파일을 다운로드하여 설치하세요.  
설치 후 아래 명령어로 초기화합니다:

```bash
git lfs install
```

---

### 📥 2. 저장소 클론 및 LFS 파일 동기화

```bash
git clone <레포지토리 주소>
cd <레포지토리 폴더>
git lfs pull
```

> `git clone` 후에는 `.gitattributes`와 포인터 파일만 내려받고, 실제 파일은 비어 있을 수 있습니다.  
> 반드시 `git lfs pull`을 실행해야 실제 파일이 다운로드됩니다.

---

### 📄 3. 특정 파일만 다운로드하고 싶을 때

GitHub 웹에서 직접 다운로드하면 포인터 파일만 받아오게 됩니다 ❌  
특정 파일만 받고 싶다면 아래 명령어를 사용하세요:

```bash
git lfs fetch --include="path/to/file"
git lfs checkout path/to/file
```

---

### 📝 요약

1. Git LFS 설치 ([공식 사이트](https://git-lfs.com/))
2. `git clone` 후 `git lfs pull` 실행
3. 필요한 경우 `git lfs fetch` + `git lfs checkout`으로 개별 파일 받기

---

💡 참고: [Git LFS 개념과 사용법 정리 블로그](https://sanghyu.tistory.com/178)

---
