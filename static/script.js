function showContent(contentId) {
    const tabs = document.querySelectorAll('.tabs li');
    tabs.forEach(tab => {
        tab.classList.remove('active'); // 모든 탭에서 active 클래스 제거
    });
    document.querySelector(`li[onclick="showContent('${contentId}')"]`).classList.add('active'); // 클릭한 탭에 active 클래스 추가

    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none'; // 모든 섹션 숨김
    });
    document.getElementById(contentId).style.display = 'block'; // 선택된 섹션만 표시
}
