
document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('searchInput');
    const dropdown = document.getElementById('searchDropdown');

    input.addEventListener('keyup', function () {
        const query = input.value;
        
        if (query.length > 1) {
            fetch(`/products/search/?q=${query}`)
                .then(response => response.json())
                    
                .then(data => {
                    dropdown.innerHTML = '';
                    dropdown.style.display = 'block';
                    
                    if (data.results.length > 0) {
                        data.results.forEach(item => {
                            const div = document.createElement('div');
                            div.classList.add('search-item');
                            div.innerHTML = `
                                <strong>${item.title}</strong><br>
                                <small>${item.author}</small>
                            `;
                            div.onclick = () => {
                                window.location.href = item.url;
                            };
                            dropdown.appendChild(div);
                        });
                    } else {
                        dropdown.innerHTML = '<div class="search-item">No result found</div>';
                    }
                });
        } else {
            dropdown.style.display = 'none';
        }
    });

    document.addEventListener('click', function (e) {
        if (!document.querySelector('.search-wrapper').contains(e.target)) {
            dropdown.style.display = 'none';
        }
    });
});
