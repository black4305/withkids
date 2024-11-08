document.addEventListener("DOMContentLoaded", function() {
    showContent('nino-trip');  // 페이지 로드 시 '니뇨의 여행' 섹션 보이기
});

// 탭 전환 함수
function showContent(contentId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none'; // 모든 섹션 숨기기
    });
    
    document.getElementById(contentId).style.display = 'block'; // 선택된 섹션만 보이게 하기
}

// 즐겨찾기 생성 (PWA 설정 완료 상태에서는 필요 없을 수도 있음)
function createShortcut() {
    if (window.matchMedia('(display-mode: standalone)').matches) {
        alert("이미 앱으로 설치되었습니다.");
    } else {
        alert("이 사이트를 홈 화면에 추가하려면 브라우저 메뉴에서 '홈 화면에 추가'를 선택하세요.");
    }
}

document.querySelector('.menu-icon').addEventListener('click', toggleMenu);

function toggleMenu() {
    const nav = document.querySelector('nav');
    nav.classList.toggle('open');
}
