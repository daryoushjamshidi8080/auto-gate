
console.log('hi')

document.addEventListener('DOMContentLoaded', function () {
const modal = document.getElementById('createAntennaModal');
const modalBody = document.getElementById('antenna-modal-body');
const form = document.getElementById('antennaCreateForm');

const antennaListDiv = document.getElementById('antenna-list');


// 📦 تابع بارگذاری لیست آنتن‌ها با AJAX
function loadAntennaList() {
    fetch("{% url 'setting:antenna_list_partial' %}")
    .then(res => res.json())
    .then(data => {
        antennaListDiv.innerHTML = data.html;
    })
    .catch(err => {
        antennaListDiv.innerHTML = "<p>❌ خطا در بارگذاری لیست آنتن‌ها</p>";
        console.error("Error loading antenna list:", err);
    });
}

loadAntennaList();

window.loadAntennaList = loadAntennaList;

modal.addEventListener('show.bs.modal', function () {
    fetch("{% url 'setting:create_antenna' %}")
    .then(res => res.json())
    .then(data => {
        modalBody.innerHTML = data.form_html;
    });
});

form.addEventListener('submit', function (e) {
    e.preventDefault();
    
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    console.log("csrf input:", csrfInput);
    
    const formData = new FormData(form);
    fetch("{% url 'setting:create_antenna' %}", {
    method: 'POST',
    body: formData
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
        const bsModal = bootstrap.Modal.getInstance(modal);
        bsModal.hide();
        form.reset();
        alert("✅ آنتن با موفقیت ثبت شد!"); //create antenna
        loadAntennaList();

        window.loadAntennaList = loadAntennaList;
        } else {
        modalBody.innerHTML = data.form_html;
        }
    });
});


});

document.addEventListener('click', function (e) {
if (e.target.classList.contains('delete-antenna')) {
    const antennaId = e.target.getAttribute('data-id');

    

    if (confirm("آیا مطمئن هستید که می‌خواهید این آنتن را حذف کنید؟")) {
    fetch(`/setting/delete-antenna/${antennaId}/`, {
        method: 'POST',
        headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
        .then(res => res.json())
        .then(data => {
        if (data.success) {
            alert("✅ آنتن با موفقیت حذف شد!");
            loadAntennaList();  // ✅ بروزرسانی لیست بدون رفرش
        } else {
            alert("❌ خطا در حذف آنتن");
        }
        });
    }
}
});


