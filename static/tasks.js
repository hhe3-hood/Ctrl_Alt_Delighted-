document.addEventListener("DOMContentLoaded", () => {

    // ------------------------------------------------------
    // ELEMENTS
    // ------------------------------------------------------
    const addModal = document.getElementById("addTaskModal");
    const editModal = document.getElementById("editTaskModal");
    const deleteModal = document.getElementById("deleteModal");

    const openAddBtn = document.getElementById("openAddModal");
    const saveAddTaskBtn = document.getElementById("saveAddTask");
    const saveEditTaskBtn = document.getElementById("saveEditTask");
    const confirmDeleteTaskBtn = document.getElementById("confirmDeleteTask");

    // close modal buttons
    document.querySelectorAll(".closeAddModal").forEach(btn =>
        btn.addEventListener("click", () => addModal.classList.add("hidden"))
    );
    document.querySelectorAll(".closeEditModal").forEach(btn =>
        btn.addEventListener("click", () => editModal.classList.add("hidden"))
    );
    document.querySelectorAll(".closeDeleteModal").forEach(btn =>
        btn.addEventListener("click", () => deleteModal.classList.add("hidden"))
    );

    const columns = {
        todo: document.getElementById("todo"),
        inprogress: document.getElementById("inprogress"),
        done: document.getElementById("done"),
    };


    // ------------------------------------------------------
    // FETCH EXISTING TASKS
    // ------------------------------------------------------
    fetch("/api/tasks")
        .then(res => res.json())
        .then(tasks => {
            tasks.forEach(renderTask);
        });


    // ------------------------------------------------------
    // OPEN ADD TASK MODAL
    // ------------------------------------------------------
    openAddBtn.addEventListener("click", () => {
        clearAddForm();
        addModal.classList.remove("hidden");
    });


    // ------------------------------------------------------
    // SAVE NEW TASK
    // ------------------------------------------------------
    saveAddTaskBtn.addEventListener("click", async () => {
        const payload = {
            title: document.getElementById("add_title").value,
            description: document.getElementById("add_description").value,
            subject: document.getElementById("add_subject").value,
            due_date: document.getElementById("add_due_date").value,
            status: "todo",
        };

        const res = await fetch("/api/tasks/add", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload),
        });

        const newTask = await res.json();
        renderTask(newTask);

        addModal.classList.add("hidden");
    });


    // ------------------------------------------------------
    // RENDER TASK CARD
    // ------------------------------------------------------
    function renderTask(task) {
        const card = document.createElement("div");
        card.classList.add("taskCard");
        card.draggable = true;
        card.dataset.taskId = task.task_id;

        card.innerHTML = `
            <h4>${task.title}</h4>
            <p class="taskSubject">${task.subject || ""}</p>
            <p class="taskDue">${task.due_date ? "Due: " + task.due_date : ""}</p>
            <p class="taskDesc">${task.description || ""}</p>

            <div class="taskActions">
                <button class="tinyBtn editBtn">Edit</button>
                <button class="tinyBtn deleteBtn">Delete</button>
            </div>
        `;

        // edit button
        card.querySelector(".editBtn").addEventListener("click", () => {
            openEditTask(task);
        });

        // delete button
        card.querySelector(".deleteBtn").addEventListener("click", () => {
            document.getElementById("delete_task_id").value = task.task_id;
            deleteModal.classList.remove("hidden");
        });

        // drag events
        card.addEventListener("dragstart", dragStart);

        columns[task.status].appendChild(card);
    }


    // ------------------------------------------------------
    // OPEN EDIT TASK MODAL
    // ------------------------------------------------------
    function openEditTask(task) {
        document.getElementById("edit_task_id").value = task.task_id;
        document.getElementById("edit_title").value = task.title;
        document.getElementById("edit_description").value = task.description;
        document.getElementById("edit_subject").value = task.subject;
        document.getElementById("edit_due_date").value = task.due_date || "";

        editModal.classList.remove("hidden");
    }


    // ------------------------------------------------------
    // SAVE EDITS
    // ------------------------------------------------------
    saveEditTaskBtn.addEventListener("click", async () => {
        const payload = {
            task_id: document.getElementById("edit_task_id").value,
            title: document.getElementById("edit_title").value,
            description: document.getElementById("edit_description").value,
            subject: document.getElementById("edit_subject").value,
            due_date: document.getElementById("edit_due_date").value,
        };

        const res = await fetch("/api/tasks/edit", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload),
        });

        const updated = await res.json();

        // Remove old card
        document.querySelector(`[data-task-id="${updated.task_id}"]`)?.remove();

        // Re-render with updates
        renderTask(updated);

        editModal.classList.add("hidden");
    });


    // ------------------------------------------------------
    // DELETE TASK
    // ------------------------------------------------------
    confirmDeleteTaskBtn.addEventListener("click", async () => {
        const taskId = document.getElementById("delete_task_id").value;

        await fetch("/api/tasks/delete", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ task_id: taskId }),
        });

        // Remove from UI
        document.querySelector(`[data-task-id="${taskId}"]`)?.remove();

        deleteModal.classList.add("hidden");
    });


    // ------------------------------------------------------
    // DRAG + DROP
    // ------------------------------------------------------
    let dragged = null;

    function dragStart(e) {
        dragged = this;
        setTimeout(() => this.classList.add("dragging"), 0);
    }

    document.querySelectorAll(".taskColumn").forEach(col => {
        col.addEventListener("dragover", e => e.preventDefault());

        col.addEventListener("drop", async function () {
            this.appendChild(dragged);
            dragged.classList.remove("dragging");

            const newStatus = this.id;
            const taskId = dragged.dataset.taskId;

            // persist change
            await fetch("/api/tasks/update_status", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ task_id: taskId, status: newStatus }),
            });
        });
    });


    // ------------------------------------------------------
    // UTILITY
    // ------------------------------------------------------
    function clearAddForm() {
        document.getElementById("add_title").value = "";
        document.getElementById("add_description").value = "";
        document.getElementById("add_subject").value = "";
        document.getElementById("add_due_date").value = "";
    }

});
