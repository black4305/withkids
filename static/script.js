// 탭 전환 함수
function showContent(contentId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none'; // 모든 섹션 숨기기
    });
    
    document.getElementById(contentId).style.display = 'block'; // 선택된 섹션만 보이게 하기
}

// 바탕화면에 바로가기 생성 함수
function createShortcut() {
    const url = window.location.href;
    const title = document.title;

    const link = document.createElement('a');
    link.href = url;
    link.download = title;
    
    const blob = new Blob([url], { type: 'text/plain' });
    const linkUrl = URL.createObjectURL(blob);
    link.href = linkUrl;
    
    link.click();
    alert("바탕화면에 바로가기가 생성되었습니다.");
}
