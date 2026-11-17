
const queryForm = document.getElementById("queryForm");
const questionInput = document.getElementById("questionInput");
const chatContainer = document.getElementById("chatContainer");
const welcomeSection = document.getElementById("welcomeSection");
const sendBtn = document.getElementById("sendBtn");
const sendText = document.getElementById("sendText");

const newChatBtn = document.getElementById("newChatBtn");
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");

const schemaNav = document.getElementById("schemaNav");
const schemaModal = document.getElementById("schemaModal");
const closeModal = document.getElementById("closeModal");
const schemaContent = document.getElementById("schemaContent");


// SEND QUESTION TO FASTAPI

async function sendQuestion(question) {

    if (!question.trim()) return;

    welcomeSection.style.display = "none";

    addUserMessage(question);

    const loadingElement = document.createElement("div");
    loadingElement.className = "loading-message";
    loadingElement.textContent = "✦ Inspecting schema and generating SQL...";
    chatContainer.appendChild(loadingElement);

    sendBtn.disabled = true;
    sendText.textContent = "Generating...";

    try {

        // const response = await fetch("/api/generate-sql", {
        const response = await fetch("http://127.0.0.1:8000/api/generate-sql", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        loadingElement.remove();

        addAIMessage(data);

    }

    catch (error) {

        loadingElement.remove();

        addErrorMessage(error.message);

        console.error("API Error:", error);

    }

    finally {

        sendBtn.disabled = false;
        sendText.textContent = "Generate SQL";

        questionInput.value = "";
        questionInput.focus();

        scrollToBottom();

    }
}


// USER MESSAGE

function addUserMessage(question) {

    const wrapper = document.createElement("div");
    wrapper.className = "chat-message";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = "YOU";

    const message = document.createElement("div");
    message.className = "user-message";
    message.textContent = question;

    wrapper.appendChild(label);
    wrapper.appendChild(message);

    chatContainer.appendChild(wrapper);

}


// AI RESPONSE

function addAIMessage(data) {

    const wrapper = document.createElement("div");
    wrapper.className = "chat-message";

    const label = document.createElement("div");
    label.className = "message-label";
    label.textContent = "QUERYMIND AI";

    const message = document.createElement("div");
    message.className = "ai-message";

    const heading = document.createElement("div");
    heading.className = "result-heading";

    const title = document.createElement("h3");
    title.textContent = "Generated SQL";

    const badge = document.createElement("span");
    badge.className = data.is_valid
        ? "result-badge"
        : "result-badge invalid";

    badge.textContent = data.is_valid
        ? "✓ SQL Validated"
        : "✕ Validation Failed";

    heading.appendChild(title);
    heading.appendChild(badge);

    const code = document.createElement("pre");
    code.className = "sql-code";
    code.textContent = data.sql || "No SQL was generated.";

    const copyButton = document.createElement("button");
    copyButton.className = "copy-btn";
    copyButton.textContent = "Copy SQL";

    copyButton.addEventListener("click", async () => {

        try {
            await navigator.clipboard.writeText(data.sql || "");
            copyButton.textContent = "Copied!";
        } catch (error) {
            copyButton.textContent = "Copy failed";
        }

        setTimeout(() => {
            copyButton.textContent = "Copy SQL";
        }, 2000);

    });

    heading.appendChild(copyButton);

    message.appendChild(heading);
    message.appendChild(code);

    if (!data.is_valid && data.validation_error) {

        const error = document.createElement("div");
        error.className = "error-message";
        error.textContent = "Validation error: " + data.validation_error;

        message.appendChild(error);

    }

    const note = document.createElement("p");
    note.className = "footer-note";
    note.textContent = "SQL generated and checked. Database execution is not enabled yet.";

    message.appendChild(note);

    wrapper.appendChild(label);
    wrapper.appendChild(message);

    chatContainer.appendChild(wrapper);

}


// ERROR MESSAGE

function addErrorMessage(errorText) {

    const wrapper = document.createElement("div");
    wrapper.className = "chat-message";

    const message = document.createElement("div");
    message.className = "error-message";
    message.textContent = "Error: " + errorText;

    wrapper.appendChild(message);

    chatContainer.appendChild(wrapper);

}


// FORM SUBMISSION

queryForm.addEventListener("submit", (event) => {

    event.preventDefault();

    const question = questionInput.value.trim();

    sendQuestion(question);

});


// ENTER TO SEND, SHIFT + ENTER FOR NEW LINE

questionInput.addEventListener("keydown", (event) => {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        queryForm.requestSubmit();

    }

});


// EXAMPLE QUESTIONS

document.querySelectorAll("[data-question]").forEach(button => {

    button.addEventListener("click", () => {

        const question = button.dataset.question;

        sendQuestion(question);

    });

});


// NEW CHAT

newChatBtn.addEventListener("click", () => {

    chatContainer.innerHTML = "";

    welcomeSection.style.display = "block";

    questionInput.value = "";

    questionInput.focus();

});


// MOBILE SIDEBAR

menuBtn.addEventListener("click", () => {

    sidebar.classList.toggle("open");

});


// CLOSE SIDEBAR AFTER NAVIGATION

document.querySelectorAll(".nav-item").forEach(item => {

    item.addEventListener("click", () => {

        sidebar.classList.remove("open");

    });

});


// DATABASE SCHEMA

schemaNav.addEventListener("click", async (event) => {

    event.preventDefault();

    schemaModal.classList.add("show");

    schemaContent.textContent = "Loading database schema...";

    try {

        // const response = await fetch("/api/schema");
        const response = await fetch("http://127.0.0.1:8000/api/schema");

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Could not load schema.");
        }

        displaySchema(data.schema);

    }

    catch (error) {

        schemaContent.textContent = error.message;

    }

});


// DISPLAY SCHEMA

function displaySchema(schema) {

    if (!schema || Object.keys(schema).length === 0) {

        schemaContent.textContent = "No tables found.";

        return;

    }

    schemaContent.innerHTML = "";

    Object.entries(schema).forEach(([tableName, columns]) => {

        const heading = document.createElement("h3");
        heading.textContent = "Table: " + tableName;
        heading.style.margin = "15px 0";

        const table = document.createElement("table");
        table.className = "schema-table";

        table.innerHTML = `
            <thead>
                <tr>
                    <th>Column</th>
                    <th>Data Type</th>
                    <th>Nullable</th>
                </tr>
            </thead>
        `;

        const tbody = document.createElement("tbody");

        columns.forEach(column => {

            const row = document.createElement("tr");

            const name = document.createElement("td");
            name.textContent = column.column_name;

            const type = document.createElement("td");
            type.textContent = column.data_type;

            const nullable = document.createElement("td");
            nullable.textContent = column.nullable ? "Yes" : "No";

            row.appendChild(name);
            row.appendChild(type);
            row.appendChild(nullable);

            tbody.appendChild(row);

        });

        table.appendChild(tbody);

        schemaContent.appendChild(heading);
        schemaContent.appendChild(table);

    });

}


// CLOSE MODAL

closeModal.addEventListener("click", () => {

    schemaModal.classList.remove("show");

});

schemaModal.addEventListener("click", (event) => {

    if (event.target === schemaModal) {

        schemaModal.classList.remove("show");

    }

});


// AUTO SCROLL

function scrollToBottom() {

    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: "smooth"
    });

}
