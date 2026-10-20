ROADMAP_LIBRARY = {
    "Python": [
        "Review syntax, functions, collections and comprehensions.",
        "Practice file handling, exceptions, modules and virtual environments.",
        "Build a Python automation tool and publish it with a README."
    ],
    "Machine Learning": [
        "Learn supervised learning, regression and classification.",
        "Practice data preprocessing, cross-validation and evaluation metrics.",
        "Build a prediction model and explain its results."
    ],
    "Deep Learning": [
        "Study neural networks, activation functions and backpropagation.",
        "Practice with PyTorch or TensorFlow using a small dataset.",
        "Build and evaluate an image or text classification model."
    ],
    "SQL": [
        "Practice SELECT, filtering, sorting and aggregate functions.",
        "Learn JOINs, subqueries, CTEs and window functions.",
        "Analyze a dataset and document insights using SQL."
    ],
    "Git": [
        "Practice status, add, commit, log and restore.",
        "Use branches, merges and pull requests.",
        "Publish a project repository with a clear README."
    ],
    "Statistics": [
        "Review probability, distributions, mean and variance.",
        "Learn sampling, confidence intervals and hypothesis testing.",
        "Apply statistical analysis to a real dataset."
    ],
    "HTML": [
        "Use semantic HTML and accessible form controls.",
        "Build structured layouts with forms and reusable sections.",
        "Create a responsive portfolio page."
    ],
    "CSS": [
        "Practice Flexbox, Grid, variables and responsive breakpoints.",
        "Build reusable cards, navigation and form components.",
        "Polish a complete responsive website."
    ],
    "JavaScript": [
        "Review variables, functions, arrays, objects and modules.",
        "Practice DOM manipulation, events, async/await and fetch.",
        "Build an interactive web application."
    ],
    "React": [
        "Learn components, props, state and rendering patterns.",
        "Practice hooks, forms and API integration.",
        "Build a dashboard with reusable components."
    ],
    "Power BI": [
        "Import, clean and model a dataset.",
        "Create measures, DAX calculations and charts.",
        "Publish an interactive report with a clear narrative."
    ],
    "Excel": [
        "Practice formulas, sorting, filtering and data cleaning.",
        "Learn pivot tables, lookups and charts.",
        "Create a data analysis report."
    ],
    "Spring Boot": [
        "Build REST controllers and service layers.",
        "Connect a database using Spring Data JPA.",
        "Create and test a CRUD application."
    ],
    "Docker": [
        "Learn images, containers, ports and volumes.",
        "Containerize a small application.",
        "Use Docker Compose for a multi-service project."
    ],
    "Linux": [
        "Learn shell commands, permissions and file operations.",
        "Practice processes, logs, package management and networking.",
        "Write a useful shell automation script."
    ],
    "Networking": [
        "Learn TCP/IP, DNS, HTTP and subnet fundamentals.",
        "Practice network diagnostics and packet analysis.",
        "Document a small networking lab."
    ]
}


def generate_roadmap(target_role, missing_skills):
    roadmap = []

    for week, skill in enumerate(missing_skills[:6], start=1):
        tasks = ROADMAP_LIBRARY.get(
            skill,
            [
                f"Learn the fundamentals of {skill}.",
                f"Practice {skill} with guided exercises.",
                f"Build a mini-project using {skill}."
            ]
        )
        roadmap.append({
            "week": week,
            "skill": skill,
            "tasks": tasks,
            "deliverable": f"Complete a practical {skill} exercise or mini-project."
        })

    if not roadmap:
        roadmap.append({
            "week": 1,
            "skill": "Portfolio project",
            "tasks": [
                f"Choose a project aligned with your {target_role} goal.",
                "Add tests, clear documentation and a README.",
                "Publish the project and prepare a short demo."
            ],
            "deliverable": "A portfolio-ready project"
        })

    return roadmap
