document.addEventListener("DOMContentLoaded", function () {
    const daysGrid = document.getElementById("daysGrid");

    // Injected from Flask
    // monthTasks is available globally from monthly.html

    // -------------------------------------------------------
    // 🌸 DRAW CALENDAR (Full Month, No Events)
    // -------------------------------------------------------
    function drawCalendar() {
        const today = new Date();
        const year = today.getFullYear();
        const month = today.getMonth();

        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);

        const firstDayIndex = firstDay.getDay();
        const totalDays = lastDay.getDate();

        daysGrid.innerHTML = "";

        // ---- Leading empty cells (days before the 1st) ----
        for (let i = 0; i < firstDayIndex; i++) {
            const emptyCell = document.createElement("div");
            emptyCell.classList.add("day", "empty");
            daysGrid.appendChild(emptyCell);
        }

        // ---- Actual days of the month ----
        for (let day = 1; day <= totalDays; day++) {
            const cell = document.createElement("div");
            cell.classList.add("day");

            const number = document.createElement("div");
            number.classList.add("day-number");
            number.textContent = day;
            cell.appendChild(number);

            // Highlight today
            if (
                day === today.getDate() &&
                month === today.getMonth() &&
                year === today.getFullYear()
            ) {
                cell.classList.add("today");
            }

            // -------------------------------------------------------
            // 🌸 SHOW TASKS (SAFE DATE PARSE)
            // -------------------------------------------------------
            monthTasks.forEach(t => {
                if (!t.due_date) return;

                // Parse YYYY-MM-DD manually → FIXES timezone bug
                const [yStr, mStr, dStr] = t.due_date.split("-");
                const dueDay = parseInt(dStr);

                if (dueDay === day) {
                    const taskPill = document.createElement("div");
                    taskPill.classList.add("calendar-task-pill");
                    taskPill.textContent = t.title;

                    cell.appendChild(taskPill);
                }
            });

            daysGrid.appendChild(cell);
        }

        // ---- Trailing empty cells (finish last row) ----
        const remaining = daysGrid.children.length % 7;
        if (remaining !== 0) {
            for (let i = remaining; i < 7; i++) {
                const emptyCell = document.createElement("div");
                emptyCell.classList.add("day", "empty");
                daysGrid.appendChild(emptyCell);
            }
        }
    }

    drawCalendar();
});
