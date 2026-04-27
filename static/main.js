// ==================== КОНФИГУРАЦИЯ ====================
const API_BASE = ''; // все запросы относительные

// Вспомогательные функции для запросов
async function apiGet(url) {
    const res = await fetch(API_BASE + url);
    if (!res.ok) throw new Error(`GET ${url} failed`);
    return res.json();
}

async function apiPost(url, data = {}) {
    const res = await fetch(API_BASE + url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!res.ok) {
        const err = await res.text();
        throw new Error(err);
    }
    return res.json();
}

async function apiPatch(url, data = {}) {
    const res = await fetch(API_BASE + url, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`PATCH ${url} failed`);
    return res.json();
}

async function apiDelete(url) {
    const res = await fetch(API_BASE + url, { method: 'DELETE' });
    if (!res.ok) throw new Error(`DELETE ${url} failed`);
    return res.json();
}

// ========== 1. БЛОГ (Задание 1) ==========
let currentSearch = '';
const postsContainer = document.getElementById('posts');

async function loadPosts() {
    try {
        const url = `/blog/posts?search=${encodeURIComponent(currentSearch)}`;
        const posts = await apiGet(url);
        renderPosts(posts);
    } catch (e) {
        console.error('Ошибка загрузки постов:', e);
        postsContainer.innerHTML = '<p>Не удалось загрузить посты</p>';
    }
}

function renderPosts(posts) {
    if (posts.length === 0) {
        postsContainer.innerHTML = '<p>Постов не найдено</p>';
        return;
    }
    postsContainer.innerHTML = posts.map(p => `
        <div style="border:1px solid #ddd; padding:10px; margin:10px 0; border-radius:5px; cursor:pointer;" onclick="viewPost(${p.id})">
            <h3>${escapeHtml(p.title)}</h3>
            <p>${escapeHtml(p.content)}</p>
            <small>👁 ${p.views_count} ❤️ ${p.likes_count} | ${new Date(p.published_at).toLocaleDateString()}</small>
        </div>
    `).join('');
}

// Простая защита от XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function viewPost(postId) {
    try {
        await apiPost(`/blog/posts/${postId}/view`);
        await loadPosts(); // обновляем счётчик просмотров
    } catch (e) {
        console.error('Ошибка увеличения просмотров:', e);
    }
}

// Обработчик поиска с debounce
let searchTimeout;
document.getElementById('search').addEventListener('input', (e) => {
    currentSearch = e.target.value;
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(loadPosts, 300);
});

// Навигация блога (пока только демо)
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        alert('Навигация: ' + btn.textContent + ' ');
    });
});

// Первоначальная загрузка
loadPosts();

// ========== 2. ФОРМА РЕГИСТРАЦИИ (Задание 2) ==========
const emailInput = document.getElementById('email');
const pass1 = document.getElementById('pass');
const pass2 = document.getElementById('pass2');
const passError = document.getElementById('passError');
const dateInput = document.getElementById('date');
const registerForm = document.getElementById('registerForm');

// Автозаполнение email из localStorage
if (localStorage.getItem('savedEmail')) {
    emailInput.value = localStorage.getItem('savedEmail');
}

// Маска даты ДД/ММ/ГГГГ
dateInput.addEventListener('input', function(e) {
    let val = e.target.value.replace(/\D/g, '');
    if (val.length >= 2) val = val.slice(0, 2) + '/' + val.slice(2);
    if (val.length >= 5) val = val.slice(0, 5) + '/' + val.slice(5, 9);
    e.target.value = val;
});

// Проверка совпадения паролей
function checkPasswords() {
    if (pass1.value !== pass2.value && pass2.value !== '') {
        passError.style.display = 'block';
        return false;
    }
    passError.style.display = 'none';
    return true;
}
pass1.addEventListener('input', checkPasswords);
pass2.addEventListener('input', checkPasswords);

// Преобразование даты из ДД/ММ/ГГГГ в ISO
function parseDateMask(dateStr) {
    const parts = dateStr.split('/');
    if (parts.length !== 3) return null;
    const day = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10) - 1;
    const year = parseInt(parts[2], 10);
    const d = new Date(year, month, day);
    return isNaN(d) ? null : d.toISOString();
}

// Отправка формы регистрации
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!checkPasswords()) return;

    const formData = new FormData(registerForm);
    const data = Object.fromEntries(formData.entries());

    // Сохраняем email в localStorage
    localStorage.setItem('savedEmail', data.email);

    // Подготовка данных для API
    const payload = {
        email: data.email,
        password: data.password,
        full_name: data.name || null,
        birth_date: data.date ? parseDateMask(data.date) : null
    };

    try {
        const response = await apiPost('/users/register', payload);
        console.log('Регистрация успешна:', response);
        alert('Регистрация прошла успешно!');
        registerForm.reset();
        passError.style.display = 'none';
    } catch (error) {
        alert('Ошибка регистрации: ' + error.message);
    }
});

// ========== 3. ГАЛЕРЕЯ (Задание 3) ==========
const galleryDiv = document.getElementById('gallery');
let currentImageIndex = 0;
let galleryImages = [];

async function loadGallery() {
    try {
        // Загружаем все изображения (можно добавить фильтр по категории)
        galleryImages = await apiGet('/gallery/images');
        renderGallery();
    } catch (e) {
        console.error('Ошибка загрузки галереи:', e);
        galleryDiv.innerHTML = '<p>Не удалось загрузить изображения</p>';
    }
}

function renderGallery() {
    if (galleryImages.length === 0) {
        galleryDiv.innerHTML = '<p>Нет изображений</p>';
        return;
    }
    galleryDiv.innerHTML = galleryImages.map((img, index) => `
        <img src="${escapeHtml(img.thumb_url)}" 
             alt="${escapeHtml(img.alt_text || img.title)}"
             onclick="openModal(${index})"
             loading="lazy">
    `).join('');
}

async function openModal(index) {
    currentImageIndex = index;
    const img = galleryImages[currentImageIndex];
    document.getElementById('modalImg').src = img.full_url;
    document.getElementById('modal').classList.add('active');
    
    // Увеличиваем счётчик просмотров на сервере
    try {
        await apiPost(`/gallery/images/${img.id}/view`);
        // Обновляем локально для отображения (опционально)
        img.views += 1;
    } catch (e) {
        console.warn('Не удалось обновить счётчик просмотров:', e);
    }
}

function closeModal() {
    document.getElementById('modal').classList.remove('active');
}

// Закрытие по клику на фон
document.getElementById('modal').addEventListener('click', (e) => {
    if (e.target === document.getElementById('modal')) closeModal();
});

// Первоначальная загрузка галереи
loadGallery();

// ========== 4. СПИСОК ЗАДАЧ (Задание 4) ==========
let todos = [];                // локальный кэш задач
let filter = 'all';            // all, active, completed
let sortAZ = false;

const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addTodo');
const todoList = document.getElementById('todoList');
const activeCountSpan = document.getElementById('activeCount');

// Загрузка задач с сервера
async function loadTodos() {
    try {
        let url = '/todo/tasks';
        if (filter === 'active') url += '?completed=false';
        else if (filter === 'completed') url += '?completed=true';
        
        todos = await apiGet(url);
        applySortAndRender();
    } catch (e) {
        console.error('Ошибка загрузки задач:', e);
    }
}

function applySortAndRender() {
    let filtered = [...todos];
    if (sortAZ) {
        filtered.sort((a, b) => a.task_text.localeCompare(b.task_text));
    }
    renderTodoList(filtered);
    updateActiveCount();
}

function renderTodoList(taskArray) {
    todoList.innerHTML = taskArray.map(task => `
        <li class="todo-item">
            <input type="checkbox" ${task.is_completed ? 'checked' : ''} 
                   onchange="toggleTodo(${task.id}, ${task.is_completed})">
            <span class="${task.is_completed ? 'completed' : ''}">${escapeHtml(task.task_text)}</span>
            <button onclick="deleteTodo(${task.id})">Удалить</button>
        </li>
    `).join('');
}

function updateActiveCount() {
    const active = todos.filter(t => !t.is_completed).length;
    activeCountSpan.textContent = active;
}

// Добавление задачи
async function addTodo() {
    const text = todoInput.value.trim();
    if (!text) return;
    try {
        await apiPost('/todo/tasks', {
            task_text: text,
            priority: 0,   // можно добавить выбор приоритета в UI
            category: null
        });
        todoInput.value = '';
        await loadTodos();
    } catch (e) {
        alert('Ошибка добавления задачи: ' + e.message);
    }
}

// Переключение статуса задачи
window.toggleTodo = async function(id, currentCompleted) {
    try {
        await apiPatch(`/todo/tasks/${id}`, {
            is_completed: !currentCompleted
        });
        await loadTodos();
    } catch (e) {
        console.error('Ошибка обновления задачи:', e);
    }
};

// Удаление задачи
window.deleteTodo = async function(id) {
    try {
        await apiDelete(`/todo/tasks/${id}`);
        await loadTodos();
    } catch (e) {
        console.error('Ошибка удаления задачи:', e);
    }
};

// Обработчики кнопок фильтрации
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        filter = btn.dataset.filter;
        loadTodos();
    });
});

// Кнопка сортировки
document.getElementById('sortBtn').addEventListener('click', () => {
    sortAZ = !sortAZ;
    document.getElementById('sortBtn').textContent = sortAZ ? 'Сортировка Z-A' : 'Сортировка A-Z';
    applySortAndRender();
});

// Добавление по кнопке и Enter
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTodo();
});

// Первоначальная загрузка задач
loadTodos();

// ========== 5. КАЛЬКУЛЯТОР (Задание 5) ==========
let calcValue = '0';
let calcPrev = '';
let calcOp = null;
const display = document.getElementById('display');

function updateDisplay() {
    display.textContent = calcValue;
}

function calcNumber(num) {
    if (calcValue === '0') calcValue = num;
    else calcValue += num;
    updateDisplay();
}

function calcOperation(op) {
    if (calcPrev && calcOp) calcEqual();
    calcPrev = calcValue;
    calcOp = op;
    calcValue = '0';
}

async function calcEqual() {
    if (!calcPrev || !calcOp) return;
    
    const prev = parseFloat(calcPrev);
    const curr = parseFloat(calcValue);
    if (isNaN(prev) || isNaN(curr)) return;
    
    let result;
    let isError = false;
    
    switch (calcOp) {
        case '+': result = prev + curr; break;
        case '-': result = prev - curr; break;
        case '*': result = prev * curr; break;
        case '/': 
            if (curr === 0) {
                alert('На ноль делить нельзя!');
                calcClear();
                return;
            }
            result = prev / curr;
            break;
        default: return;
    }
    
    const expression = `${calcPrev} ${calcOp} ${calcValue}`;
    calcValue = result.toString();
    calcPrev = '';
    calcOp = null;
    updateDisplay();
    
    // Сохраняем вычисление в историю
    try {
        await apiPost('/calc/calculate', {
            expression,
            result,
            is_error: isError
        });
        console.log('Вычисление сохранено:', expression, '=', result);
    } catch (e) {
        console.warn('Не удалось сохранить историю:', e);
    }
}

function calcClear() {
    calcValue = '0';
    calcPrev = '';
    calcOp = null;
    updateDisplay();
}

// Генерация кнопок калькулятора
const calcButtons = [
    '7','8','9','/',
    '4','5','6','*',
    '1','2','3','-',
    '0','.','=','+',
    'C'
];

const calcGrid = document.getElementById('calcButtons');
calcButtons.forEach(btn => {
    const button = document.createElement('button');
    button.textContent = btn;
    button.addEventListener('click', () => {
        if (btn >= '0' && btn <= '9') calcNumber(btn);
        else if (btn === '.') calcNumber(btn);
        else if (btn === '=') calcEqual();
        else if (btn === 'C') calcClear();
        else calcOperation(btn);
    });
    calcGrid.appendChild(button);
});

// Поддержка клавиатуры
document.addEventListener('keydown', (e) => {
    const key = e.key;
    if (key >= '0' && key <= '9') calcNumber(key);
    else if (key === '.') calcNumber(key);
    else if (key === '+' || key === '-' || key === '*' || key === '/') {
        e.preventDefault();
        calcOperation(key);
    }
    else if (key === 'Enter' || key === '=') {
        e.preventDefault();
        calcEqual();
    }
    else if (key === 'Escape') calcClear();
});

// ========== ТЕМА (Dark/Light) ==========
const themeBtn = document.getElementById('themeBtn');
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark');
    themeBtn.textContent = 'Светлая';
}
themeBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    themeBtn.textContent = isDark ? 'Светлая' : 'Тёмная';
});

// ========== ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ ==========
window.addEventListener('DOMContentLoaded', () => {
    // Все загрузки уже вызваны выше, можно добавить дополнительные проверки
});