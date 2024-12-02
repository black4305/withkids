document.addEventListener('DOMContentLoaded', function () {
    showContent('nino-trip');  // 페이지 로드 시 '니뇨의 여행' 섹션 보이기
    const form = document.getElementById('inquiryForm');

    if (form) {
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton.disabled) return; // 중복 클릭 방지

            submitButton.disabled = true; // 버튼 비활성화

            const data = {
                name: document.getElementById('name').value,
                message: document.getElementById('message').value,
            };

            try {
                const response = await fetch('/api/inquiries', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                const result = await response.json();
                if (response.ok) {
                    alert(result.message || '문의가 성공적으로 접수되었습니다.');
                    form.reset();
                    loadInquiries();
                } else {
                    alert(result.error || '문의 접수 중 오류가 발생했습니다.');
                }
            } catch (error) {
                alert('서버와 연결할 수 없습니다. 다시 시도해주세요.');
            } finally {
                submitButton.disabled = false;
            }
        });
    }
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

// 버튼으로 검색 기능 실행
function filterTableWithButton(tableId, searchInputId) {
    const searchInput = document.getElementById(searchInputId);
    const query = searchInput.value.trim();
    filterTable(tableId, query);
}

// 기존 검색 함수 (oninput에서 호출)
function filterTable(tableId, query) {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tbody tr');
    const searchText = query.toLowerCase();

    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll('td'));
        const match = cells.some(cell => cell.textContent.toLowerCase().includes(searchText));
        row.style.display = match ? '' : 'none';
    });
}