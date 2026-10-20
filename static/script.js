"use strict";

const $ = (selector) => document.querySelector(selector);

let analysisData = null;
let skillChart = null;
let matchChart = null;
let resumeChart = null;

Chart.defaults.font.family = "Inter, sans-serif";
Chart.defaults.color = "#9cacc5";

const chartColors = {
    mint: "#42e5bd",
    violet: "#aa8cff",
    blue: "#66b8ff",
    orange: "#ffbb76",
    muted: "#9cacc5"
};

function createCharts() {
    const gridColor = "rgba(147, 170, 210, 0.10)";

    skillChart = new Chart($("#skillChart"), {
        type: "radar",
        data: {
            labels: [
                "Programming",
                "Data Skills",
                "Web Development",
                "AI / ML",
                "Tools",
                "Soft Skills"
            ],
            datasets: [{
                label: "Detected skill coverage",
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: "rgba(66, 229, 189, 0.13)",
                borderColor: chartColors.mint,
                pointBackgroundColor: chartColors.mint,
                pointRadius: 4,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    min: 0,
                    max: 100,
                    ticks: {
                        display: false,
                        stepSize: 20
                    },
                    grid: {
                        color: gridColor
                    },
                    angleLines: {
                        color: gridColor
                    },
                    pointLabels: {
                        color: chartColors.muted,
                        font: { size: 10 }
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    matchChart = new Chart($("#matchChart"), {
        type: "bar",
        data: {
            labels: ["Matched skills", "Missing skills"],
            datasets: [{
                label: "Number of skills",
                data: [0, 0],
                backgroundColor: [
                    chartColors.mint,
                    chartColors.orange
                ],
                borderRadius: 8,
                barThickness: 32
            }]
        },
        options: {
            indexAxis: "y",
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0,
                        color: chartColors.muted
                    },
                    grid: { color: gridColor }
                },
                y: {
                    ticks: { color: chartColors.muted },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    resumeChart = new Chart($("#resumeChart"), {
        type: "doughnut",
        data: {
            labels: ["Sections found", "Sections not found"],
            datasets: [{
                data: [0, 5],
                backgroundColor: [
                    chartColors.violet,
                    "rgba(147, 170, 210, 0.14)"
                ],
                borderWidth: 0,
                hoverOffset: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "76%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: chartColors.muted,
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 10 }
                    }
                }
            }
        }
    });
}

function setMetric(id, value, barId, percentage = true) {
    const element = $(id);
    if (element) {
        element.textContent = percentage ? `${value}%` : value;
    }

    const bar = $(barId);
    if (bar) {
        bar.style.width = `${Math.max(0, Math.min(100, value))}%`;
    }
}

function countCategories(skills) {
    const categories = {
        "Programming": [
            "Python", "Java", "C", "C++", "C#", "JavaScript",
            "TypeScript", "OOP", "Data Structures", "Algorithms"
        ],
        "Data Skills": [
            "SQL", "MySQL", "PostgreSQL", "Excel", "Power BI",
            "Tableau", "Pandas", "NumPy", "Statistics",
            "Data Analysis", "Data Visualization", "Matplotlib"
        ],
        "Web Development": [
            "HTML", "CSS", "JavaScript", "React", "Angular",
            "Vue", "Node.js", "Express", "Flask", "Django",
            "Spring Boot", "REST API", "Responsive Design"
        ],
        "AI / ML": [
            "Machine Learning", "Deep Learning", "TensorFlow",
            "PyTorch", "NLP", "Generative AI", "LLM",
            "Scikit-learn"
        ],
        "Tools": [
            "Git", "GitHub", "Docker", "Kubernetes",
            "AWS", "Azure", "Linux", "Maven"
        ],
        "Soft Skills": [
            "Communication", "Leadership", "Problem Solving",
            "Teamwork", "Project Management"
        ]
    };

    const normalized = new Set(skills.map(s => s.toLowerCase()));

    return Object.values(categories).map(group => {
        const found = group.filter(s => normalized.has(s.toLowerCase()));
        return Math.round(found.length / group.length * 100);
    });
}

function renderSkillTags(elementId, skills, className) {
    const container = $(elementId);
    container.replaceChildren();

    if (!skills.length) {
        const message = document.createElement("p");
        message.className = "chart-note";
        message.textContent = "No skills detected in this category yet.";
        container.appendChild(message);
        return;
    }

    skills.forEach(skill => {
        const tag = document.createElement("span");
        tag.className = `skill-tag ${className}`;
        tag.textContent = skill;
        container.appendChild(tag);
    });
}

function renderRecommendations(recommendations) {
    const container = $("#recommendations");
    container.replaceChildren();

    recommendations.forEach(item => {
        const card = document.createElement("article");
        card.className = "recommendation-card";

        const title = document.createElement("h4");
        title.textContent = `✧ ${item.title}`;

        const description = document.createElement("p");
        description.textContent = item.description;

        card.append(title, description);
        container.appendChild(card);
    });

    if (!recommendations.length) {
        const message = document.createElement("p");
        message.className = "chart-note";
        message.textContent =
            "No additional recommendations were generated by this rule set.";
        container.appendChild(message);
    }
}

function renderResults(data) {
    analysisData = data;

    setMetric("#readinessValue", data.readiness, "#readinessBar");
    setMetric("#skillCount", data.skill_count, "#skillsBar", false);
    setMetric("#matchValue", data.match_score, "#matchBar");
    setMetric("#gapCount", data.missing_skills.length, "#gapBar", false);

    $("#readinessNote").textContent =
        `${data.resume_score}% resume section coverage`;

    $("#skillsBar").style.width =
        `${Math.min(100, data.skill_count * 5)}%`;

    $("#gapBar").style.width =
        `${data.required_skills.length
            ? data.missing_skills.length / data.required_skills.length * 100
            : 0}%`;

    $("#resumeScore").textContent = `${data.resume_score}%`;
    $("#resultRole").textContent = data.role;

    $("#emptyState").hidden = true;
    $("#resultsArea").hidden = false;

    renderSkillTags("#matchedSkills", data.matched_skills, "matched");
    renderSkillTags("#missingSkills", data.missing_skills, "missing");
    renderRecommendations(data.recommendations);

    skillChart.data.datasets[0].data = countCategories(data.skills);
    skillChart.update();

    matchChart.data.labels = [
        `Matched (${data.matched_skills.length})`,
        `Missing (${data.missing_skills.length})`
    ];

    matchChart.data.datasets[0].data = [
        data.matched_skills.length,
        data.missing_skills.length
    ];
    matchChart.update();

    const sectionsFound = Object.values(data.sections)
        .filter(Boolean).length;

    resumeChart.data.datasets[0].data = [
        sectionsFound,
        Object.keys(data.sections).length - sectionsFound
    ];
    resumeChart.update();

    $("#formMessage").textContent =
        "Analysis complete. Your results are displayed below.";
    $("#formMessage").className = "form-message success";
}

const form = $("#resumeForm");
const fileInput = $("#resumeFile");
const dropZone = $("#dropZone");

fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    $("#fileName").textContent = file
        ? file.name
        : "No file selected";

    $("#fileName").title = file ? file.name : "";
});

["dragenter", "dragover"].forEach(eventName => {
    dropZone.addEventListener(eventName, event => {
        event.preventDefault();
        dropZone.classList.add("drag-over");
    });
});

["dragleave", "drop"].forEach(eventName => {
    dropZone.addEventListener(eventName, event => {
        event.preventDefault();
        dropZone.classList.remove("drag-over");
    });
});

dropZone.addEventListener("drop", event => {
    const file = event.dataTransfer.files[0];
    if (!file) return;

    const allowed = /\.(pdf|docx|txt)$/i.test(file.name);

    if (!allowed) {
        showMessage("Please drop a PDF, DOCX, or TXT file.", true);
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showMessage("The maximum upload size is 10 MB.", true);
        return;
    }

    const transfer = new DataTransfer();
    transfer.items.add(file);
    fileInput.files = transfer.files;

    $("#fileName").textContent = file.name;
    showMessage("File ready for analysis.", false);
});

function showMessage(message, error) {
    $("#formMessage").textContent = message;
    $("#formMessage").className =
        `form-message ${error ? "error" : "success"}`;
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    const file = fileInput.files[0];

    if (!file) {
        showMessage("Please choose a resume first.", true);
        return;
    }

    if (!/\.(pdf|docx|txt)$/i.test(file.name)) {
        showMessage("Unsupported file format.", true);
        return;
    }

    if (file.size > 10 * 1024 * 1024) {
        showMessage("The maximum upload size is 10 MB.", true);
        return;
    }

    const button = $("#analyzeButton");
    button.disabled = true;
    button.textContent = "Analyzing resume...";

    showMessage("Extracting resume text and analyzing your skills...", false);

    const formData = new FormData(form);

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed.");
        }

        renderResults(data);
        $("#resultsArea").scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    } catch (error) {
        showMessage(error.message || "Unable to contact the server.", true);
    } finally {
        button.disabled = false;
        button.innerHTML = "✧ Analyze My Career <span>→</span>";
    }
});

$("#themeToggle").addEventListener("click", () => {
    document.body.classList.toggle("light-theme");

    const light = document.body.classList.contains("light-theme");
    $("#themeToggle").textContent = light ? "☾" : "☼";

    const muted = light ? "#64748b" : "#9cacc5";
    const grid = light
        ? "rgba(53, 76, 112, 0.12)"
        : "rgba(147, 170, 210, 0.10)";

    [skillChart, matchChart, resumeChart].forEach(chart => {
        chart.options.color = muted;

        if (chart.options.scales?.r) {
            chart.options.scales.r.pointLabels.color = muted;
            chart.options.scales.r.grid.color = grid;
            chart.options.scales.r.angleLines.color = grid;
        }

        if (chart.options.scales?.x) {
            chart.options.scales.x.ticks.color = muted;
            chart.options.scales.x.grid.color = grid;
        }

        if (chart.options.scales?.y) {
            chart.options.scales.y.ticks.color = muted;
            if (chart.options.scales.y.grid) {
                chart.options.scales.y.grid.color = grid;
            }
        }

        if (chart.options.plugins?.legend?.labels) {
            chart.options.plugins.legend.labels.color = muted;
        }

        chart.update();
    });
});

$("#menuToggle").addEventListener("click", () => {
    $("#sidebar").classList.toggle("open");
});

document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
        document.querySelectorAll(".nav-link").forEach(item => {
            item.classList.remove("active");
        });

        link.classList.add("active");
        $("#sidebar").classList.remove("open");
    });
});

$("#downloadReport").addEventListener("click", () => {
    if (!analysisData) {
        showMessage("Analyze a resume before exporting.", true);
        return;
    }

    const data = analysisData;

    const lines = [
        "CAREERIQ - CAREER INTELLIGENCE REPORT",
        "======================================",
        "",
        `Resume: ${data.filename}`,
        `Target role: ${data.role}`,
        `Career readiness estimate: ${data.readiness}%`,
        `Resume section coverage: ${data.resume_score}%`,
        `Target-role skill match: ${data.match_score}%`,
        `Skills identified: ${data.skill_count}`,
        `Resume word count: ${data.word_count}`,
        "",
        "MATCHED SKILLS",
        ...data.matched_skills.map(skill => `- ${skill}`),
        "",
        "SKILLS TO DEVELOP",
        ...data.missing_skills.map(skill => `- ${skill}`),
        "",
        "RECOMMENDATIONS",
        ...data.recommendations.map(item =>
            `- ${item.title}: ${item.description}`
        ),
        "",
        "Note: These are rule-based estimates, not a validated hiring prediction."
    ];

    const blob = new Blob(
        [lines.join("\n")],
        { type: "text/plain;charset=utf-8" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "CareerIQ-Report.txt";
    link.click();

    URL.revokeObjectURL(url);
});

createCharts();