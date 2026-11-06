const form = document.getElementById("studentForm");

form.addEventListener("submit", async function(event) {
    event.preventDefault();

    const student = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        course: document.getElementById("course").value
    };

    const response = await fetch("/students", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(student)
    });

    const result = await response.json();

    document.getElementById("message").textContent =
        result.message || result.error;

    if (response.ok) {
        form.reset();
        loadStudents();
    }
});

async function loadStudents() {
    const response = await fetch("/students");
    const students = await response.json();

    const list = document.getElementById("studentList");
    list.innerHTML = "";

    students.forEach(student => {
        const row = document.createElement("tr");

        [student.id, student.name, student.email, student.course]
            .forEach(value => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

        const action = document.createElement("td");
        const button = document.createElement("button");

        button.textContent = "Delete";
        button.className = "delete-btn";

        button.onclick = () => deleteStudent(student.id);

        action.appendChild(button);
        row.appendChild(action);
        list.appendChild(row);
    });
}

async function deleteStudent(id) {
    if (!confirm("Are you sure you want to delete this student?")) {
        return;
    }

    const response = await fetch(`/students/${id}`, {
        method: "DELETE"
    });

    const result = await response.json();

    document.getElementById("message").textContent =
        result.message || result.error;

    if (response.ok) {
        loadStudents();
    }
}

loadStudents();
