const API_BASE = 'http://localhost:8000/api';

// --- Управление токеном ---
function getToken() {
    let token = localStorage.getItem('token');
    if (token) {
        return Promise.resolve(token);
    }
    return fetch(`${API_BASE}/create_user`, { method: 'GET' })
        .then(response => {
            if (!response.ok) throw new Error('Failed to create user');
            return response.json();
        })
        .then(data => {
            if (data.token) {
                localStorage.setItem('token', data.token);
                return data.token;
            } else {
                throw new Error('No token in response');
            }
        });
}

function authorizedFetch(url, options = {}) {
    return getToken().then(token => {
        return fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            }
        });
    });
}

// --- Загрузка фотографий ---
function uploadPhotos(files) {
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('photos', files[i]);
    }
    return authorizedFetch(`${API_BASE}/upload_photo`, {
        method: 'POST',
        body: formData
    }).then(res => {
        if (!res.ok) throw new Error('Upload failed');
        return res.json();
    });
}

// --- Получение списка пакетов ---
function getBatches() {
    return authorizedFetch(`${API_BASE}/get_batches`)
        .then(res => {
            if (!res.ok) throw new Error('Failed to get batches');
            return res.json();
        });
}

// --- Получение элементов пакета ---
function getBatchItems(batchId) {
    return authorizedFetch(`${API_BASE}/get_batch_items?id=${batchId}`)
        .then(res => {
            if (!res.ok) throw new Error('Failed to get batch items');
            return res.json();
        });
}

// --- Скачать отдельный элемент ---
function downloadBatchItem(batchId, itemId, filename) {
    return getToken().then(token => {
        const url = `${API_BASE}/download_batch_item?batch_id=${batchId}&id=${itemId}`;
        return fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => {
            if (!response.ok) throw new Error('Download failed');
            return response.blob();
        })
        .then(blob => {
            const urlBlob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = urlBlob;
            a.download = filename || `item_${itemId}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(urlBlob);
        });
    });
}

// --- Скачать весь пакет ---
function downloadBatches(batchId) {
    return getToken().then(token => {
        const url = `${API_BASE}/download_batches?id=${batchId}`;
        return fetch(url, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        .then(response => {
            if (!response.ok) throw new Error('Download failed');
            return response.blob();
        })
        .then(blob => {
            const urlBlob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = urlBlob;
            a.download = `batch_${batchId}`;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(urlBlob);
        });
    });
}

// --- Вспомогательная функция для иконки статуса ---
function getStatusIcon(status) {
    switch (status) {
        case 'completed':
            return '<span class="text-success">✅</span>';
        case 'processed':
            return '<span class="spinner-border spinner-border-sm text-warning" role="status"><span class="visually-hidden">Обрабатывается</span></span>';
        case 'failed':
            return '<span class="text-danger fs-4">❗</span>';
        default:
            return '<span class="text-secondary">⏳</span>';
    }
}

// --- Рендеринг истории ---
function renderHistory(container) {
    getBatches()
        .then(data => {
            if (!data.batches || data.batches.length === 0) {
                container.innerHTML = '<p>Нет пакетов</p>';
                return;
            }
            let html = '<div class="accordion" id="historyAccordion">';
            data.batches.forEach((batch, index) => {
                const collapseId = `collapse${batch.id}`;
                const headingId = `heading${batch.id}`;
                const statusIcon = getStatusIcon(batch.status);
                // Кнопка скачивания активна только при статусе completed
                const downloadDisabled = batch.status !== 'completed' ? 'disabled' : '';
                html += `
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="${headingId}">
                            <div class="d-flex align-items-center justify-content-between p-2">
                                <button class="accordion-button collapsed flex-grow-1" type="button" data-bs-toggle="collapse" data-bs-target="#${collapseId}" aria-expanded="false" aria-controls="${collapseId}" data-batch-id="${batch.id}">
                                    <span>Пакет #${batch.id} (${batch.name})</span>
                                    <span class="ms-2">${statusIcon}</span>
                                </button>
                                <div class="ms-2">
                                    <button class="btn btn-sm btn-primary download-batch-btn" data-batch-id="${batch.id}" ${downloadDisabled}>
                                        Скачать всё
                                    </button>
                                </div>
                            </div>
                        </h2>
                        <div id="${collapseId}" class="accordion-collapse collapse" aria-labelledby="${headingId}" data-bs-parent="#historyAccordion">
                            <div class="accordion-body" id="batchItems_${batch.id}">
                                <p>Загрузка элементов...</p>
                            </div>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            container.innerHTML = html;

            // Обработчики для кнопок скачивания пакета
            container.querySelectorAll('.download-batch-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation(); // чтобы не сворачивать аккордеон
                    const batchId = this.dataset.batchId;
                    if (!this.disabled) {
                        downloadBatches(batchId).catch(err => alert(err.message));
                    }
                });
            });

            // Обработчики для раскрытия пакета (загрузка элементов)
            container.querySelectorAll('.accordion-collapse').forEach(collapse => {
                collapse.addEventListener('show.bs.collapse', function(e) {
                    const batchId = this.id.replace('collapse', '');
                    const itemsContainer = document.getElementById(`batchItems_${batchId}`);
                    if (itemsContainer && itemsContainer.dataset.loaded !== 'true') {
                        loadBatchItems(batchId, itemsContainer);
                    }
                });
            });
        })
        .catch(error => {
            container.innerHTML = `<p class="text-danger">Ошибка загрузки истории: ${error.message}</p>`;
        });
}

// --- Загрузка элементов пакета (внутри тела аккордеона) ---
function loadBatchItems(batchId, container) {
    getBatchItems(batchId)
        .then(data => {
            if (!data.items || data.items.length === 0) {
                container.innerHTML = '<p>Нет элементов</p>';
                return;
            }
            let html = '<ul class="list-group">';
            data.items.forEach(item => {
                const statusClass = {
                    'completed': 'text-success',
                    'processed': 'text-warning',
                    'pending': 'text-secondary',
                    'failed': 'text-danger'
                }[item.status] || '';
                html += `
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <span>${item.name} - <span class="${statusClass}">${item.status}</span></span>
                        <div>
                            ${item.status === 'completed' ? `<button class="btn btn-sm btn-success download-item-btn" data-batch-id="${batchId}" data-item-id="${item.id}" data-name="${item.name}">Скачать</button>` : ''}
                        </div>
                    </li>
                `;
            });
            html += '</ul>';
            container.innerHTML = html;
            container.dataset.loaded = 'true';

            // Обработчики для кнопок скачивания отдельных элементов
            container.querySelectorAll('.download-item-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    const batchId = this.dataset.batchId;
                    const itemId = this.dataset.itemId;
                    const name = this.dataset.name || `item_${itemId}`;
                    downloadBatchItem(batchId, itemId, name).catch(err => alert(err.message));
                });
            });
        })
        .catch(error => {
            container.innerHTML = `<p class="text-danger">Ошибка загрузки элементов: ${error.message}</p>`;
        });
}

// --- Инициализация при загрузке страницы ---
document.addEventListener('DOMContentLoaded', function() {
    getToken().catch(err => console.error('Token init error:', err));

    // Загрузка фотографий
    const uploadForm = document.getElementById('uploadForm');
    const uploadResult = document.getElementById('uploadResult');
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('photoInput');
        const files = fileInput.files;
        if (files.length === 0) {
            uploadResult.innerHTML = '<div class="alert alert-warning">Выберите хотя бы один файл</div>';
            return;
        }
        uploadResult.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Загрузка...</span></div>';
        uploadPhotos(files)
            .then(data => {
                uploadResult.innerHTML = `<div class="alert alert-success">Загрузка успешна: ${data.status}</div>`;
                fileInput.value = '';
            })
            .catch(err => {
                uploadResult.innerHTML = `<div class="alert alert-danger">Ошибка: ${err.message}</div>`;
            });
    });

    // История – модальное окно
    const historyModal = document.getElementById('historyModal');
    historyModal.addEventListener('shown.bs.modal', function() {
        const container = document.getElementById('historyContent');
        container.innerHTML = '<p>Загрузка...</p>';
        renderHistory(container);
    });

    // Переключатель формата
    const formatToggle = document.getElementById('formatToggle');
    let format = localStorage.getItem('format') || 'tabs_to_notes';
    updateFormatButton(format);
    formatToggle.addEventListener('click', function() {
        let newFormat = format === 'tabs_to_notes' ? 'notes_to_tabs' : 'tabs_to_notes';
        localStorage.setItem('format', newFormat);
        format = newFormat;
        updateFormatButton(format);
    });

    function updateFormatButton(format) {
        const btn = document.getElementById('formatToggle');
        btn.textContent = format === 'tabs_to_notes' ? 'Табы -> Ноты' : 'Ноты -> Табы';
    }
});