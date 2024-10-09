document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const contentSection = document.getElementById('content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-content');
            loadTabContent(tabName);
        });
    });

    function loadTabContent(tabName) {
        fetch(`/data/${tabName}`)
            .then(response => response.json())
            .then(data => {
                displayContent(data, tabName);
            })
            .catch(error => {
                contentSection.innerHTML = '<p>에러가 발생했습니다.</p>';
            });
    }

    function displayContent(data, tabName) {
        contentSection.innerHTML = '';
        if (tabName === 'sns') {
            const table = document.createElement('table');
            data.forEach(row => {
                const tr = document.createElement('tr');
                for (let key in row) {
                    const td = document.createElement('td');
                    td.innerHTML = row[key];  // HTML 형식으로 링크도 포함
                    tr.appendChild(td);
                }
                table.appendChild(tr);
            });
            contentSection.appendChild(table);
        } else {
            contentSection.innerHTML = `<p>${tabName}의 내용을 준비 중입니다.</p>`;
        }
    }
});
