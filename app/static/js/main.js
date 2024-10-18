document.addEventListener('DOMContentLoaded', function() {

    // Function to render the employee table
    function renderEmployeeTable(employees) {
        const container = document.getElementById('employee-table-container');
        if (employees.length === 0) {
            container.innerHTML = '<p>No employees found. Please add new employees.</p>';
            return;
        }

        let tableHTML = `
            <table class="table table-striped table-bordered employee-table">
                <thead class="table-dark">
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Position</th>
                        <th>Salary</th>
                        <th>Date Hired</th>
                        <th>Profile Picture</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
        `;

        employees.forEach(employee => {
            tableHTML += `
                <tr>
                    <td>${employee.id}</td>
                    <td>${employee.name}</td>
                    <td>${employee.email}</td>
                    <td>${employee.position}</td>
                    <td>$${employee.salary.toFixed(2)}</td>
                    <td>${employee.date_hired}</td>
                    <td>
                        ${employee.profile_picture ? `<img src="/static/uploads/${employee.profile_picture}" alt="Profile Picture" class="profile-pic">` : '<span>N/A</span>'}
                    </td>
                    <td>
                        <a href="/edit/${employee.id}" class="btn btn-sm btn-warning mb-1"><i class="fas fa-edit"></i> Edit</a>
                        <a href="#" data-url="/delete/${employee.id}" class="btn btn-sm btn-danger delete-btn"><i class="fas fa-trash-alt"></i> Delete</a>
                    </td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
        `;

        container.innerHTML = tableHTML;

        // Reattach delete button event listeners
        attachDeleteEventListeners();
    }

    // Function to fetch employees based on the search query
    function fetchEmployees(query) {
        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = 'block';

        fetch(`/search?q=${encodeURIComponent(query)}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            renderEmployeeTable(data.employees);
        })
        .catch(error => {
            console.error('Error fetching employees:', error);
        })
        .finally(() => {
            spinner.style.display = 'none';
        });
    }

    // Event listener for search input
    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        fetchEmployees(query);
    });

    // Event listener for search button
    const searchButton = document.getElementById('search-button');
    searchButton.addEventListener('click', function() {
        const query = searchInput.value.trim();
        fetchEmployees(query);
    });

    // Function to attach delete button event listeners
    function attachDeleteEventListeners() {
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.removeEventListener('click', handleDelete); // Remove previous listener if any
            button.addEventListener('click', handleDelete);
        });
    }

    // Delete confirmation handler
    function handleDelete(event) {
        event.preventDefault();
        const deleteUrl = this.getAttribute('data-url');

        Swal.fire({
            title: 'Are you sure?',
            text: "This action cannot be undone!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#e53935',
            cancelButtonColor: '#1e88e5',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                // Create a form and submit it
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = deleteUrl;

                document.body.appendChild(form);
                form.submit();
            }
        });
    }

    // Initial fetch of employees
    fetchEmployees('');

    // Flash messages handling with Bootstrap Toasts
    const flashMessagesElement = document.getElementById('flash-messages');
    if (flashMessagesElement) {
        const flashMessages = JSON.parse(flashMessagesElement.textContent);
        if (flashMessages.length > 0) {
            const toastContainer = document.getElementById('toast-container');
            flashMessages.forEach(([category, message]) => {
                const toastEl = document.createElement('div');
                toastEl.className = `toast align-items-center text-bg-${category === 'success' ? 'success' : 'danger'} border-0`;
                toastEl.role = 'alert';
                toastEl.ariaLive = 'assertive';
                toastEl.ariaAtomic = 'true';
                toastEl.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            ${message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                `;
                toastContainer.appendChild(toastEl);
                const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
                toast.show();
            });
        }
    }

});


let debounceTimer;
searchInput.addEventListener('input', function() {
    const query = this.value.trim();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
        fetchEmployees(query);
    }, 300); // Adjust the delay as needed
});
