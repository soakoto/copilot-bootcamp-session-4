"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import uuid4
import os
from pathlib import Path

app = FastAPI(title="Slalom Capabilities Management API",
              description="API for managing consulting capabilities and consultant expertise")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,  # hours per week available across team
        "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"]
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology", 
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Tableau Desktop Specialist", "Power BI Expert", "Google Analytics"],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"]
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"], 
        "certifications": ["Docker Certified Associate", "Kubernetes Admin", "Jenkins Certified"],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"]
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Digital Transformation Certificate", "Agile Certified Practitioner"],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"]
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"]
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Adobe Certified Expert", "Google UX Design Certificate"],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"]
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"]
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"]
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Certified Scrum Master", "SAFe Agilist", "ICAgile Certified"],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return capabilities


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if email in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability"
        )

    # Add consultant
    capability["consultants"].append(email)
    return {"message": f"Registered {email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability"""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    # Get the specific capability
    capability = capabilities[capability_name]

    # Validate consultant is registered
    if email not in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability"
        )

    # Remove consultant
    capability["consultants"].remove(email)
    return {"message": f"Unregistered {email} from {capability_name}"}


# ---------------------------------------------------------------------------
# Course / Module / Submodule — Data Models
# ---------------------------------------------------------------------------

SubmoduleType = Literal["learning", "quiz", "conclusion"]


class SubmoduleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    type: SubmoduleType


class SubmoduleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[SubmoduleType] = None


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[str] = None


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[str] = None


class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None
    category: Optional[str] = None
    level: Optional[Literal["Beginner", "Intermediate", "Advanced"]] = None
    language: Optional[str] = None
    duration: Optional[str] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructor: Optional[str] = None
    category: Optional[str] = None
    level: Optional[Literal["Beginner", "Intermediate", "Advanced"]] = None
    language: Optional[str] = None
    duration: Optional[str] = None


# ---------------------------------------------------------------------------
# In-memory course store
# ---------------------------------------------------------------------------
# Structure:
#   courses[course_id] = {
#       "id": str, "title": str, ...,
#       "modules": {
#           module_id: {
#               "id": str, "title": str, ...,
#               "submodules": { submodule_id: {...} }
#           }
#       }
#   }

courses: dict = {}


# ---------------------------------------------------------------------------
# Course endpoints
# ---------------------------------------------------------------------------

@app.get("/courses", summary="List all courses")
def list_courses():
    """Return all courses (without nested module/submodule detail)."""
    return [
        {k: v for k, v in course.items() if k != "modules"}
        for course in courses.values()
    ]


@app.post("/courses", status_code=201, summary="Create a course")
def create_course(payload: CourseCreate):
    """Create a new course."""
    course_id = str(uuid4())
    courses[course_id] = {
        "id": course_id,
        **payload.model_dump(),
        "modules": {}
    }
    return courses[course_id]


@app.get("/courses/{course_id}", summary="Get a course with all modules")
def get_course(course_id: str):
    """Return a single course including its modules and submodules."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


@app.put("/courses/{course_id}", summary="Update a course")
def update_course(course_id: str, payload: CourseUpdate):
    """Partially update a course's metadata."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    courses[course_id].update(updates)
    return courses[course_id]


@app.delete("/courses/{course_id}", summary="Delete a course")
def delete_course(course_id: str):
    """Delete a course and all its modules/submodules."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    del courses[course_id]
    return {"message": f"Course {course_id} deleted"}


# ---------------------------------------------------------------------------
# Module endpoints
# ---------------------------------------------------------------------------

@app.get("/courses/{course_id}/modules", summary="List modules in a course")
def list_modules(course_id: str):
    """Return all modules for a course (without submodule detail)."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return [
        {k: v for k, v in m.items() if k != "submodules"}
        for m in courses[course_id]["modules"].values()
    ]


@app.post("/courses/{course_id}/modules", status_code=201, summary="Add a module to a course")
def create_module(course_id: str, payload: ModuleCreate):
    """Add a new module to an existing course."""
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    module_id = str(uuid4())
    module = {"id": module_id, **payload.model_dump(), "submodules": {}}
    courses[course_id]["modules"][module_id] = module
    return module


@app.get("/courses/{course_id}/modules/{module_id}", summary="Get a module with submodules")
def get_module(course_id: str, module_id: str):
    """Return a single module including its submodules."""
    course = _get_course_or_404(course_id)
    return _get_module_or_404(course, module_id)


@app.put("/courses/{course_id}/modules/{module_id}", summary="Update a module")
def update_module(course_id: str, module_id: str, payload: ModuleUpdate):
    """Partially update a module's metadata."""
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    module.update(updates)
    return module


@app.delete("/courses/{course_id}/modules/{module_id}", summary="Delete a module")
def delete_module(course_id: str, module_id: str):
    """Delete a module and all its submodules."""
    course = _get_course_or_404(course_id)
    _get_module_or_404(course, module_id)
    del course["modules"][module_id]
    return {"message": f"Module {module_id} deleted"}


# ---------------------------------------------------------------------------
# Submodule endpoints
# ---------------------------------------------------------------------------

@app.get("/courses/{course_id}/modules/{module_id}/submodules",
         summary="List submodules in a module")
def list_submodules(course_id: str, module_id: str):
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    return list(module["submodules"].values())


@app.post("/courses/{course_id}/modules/{module_id}/submodules",
          status_code=201, summary="Add a submodule to a module")
def create_submodule(course_id: str, module_id: str, payload: SubmoduleCreate):
    """Add a new submodule (learning/quiz/conclusion) to a module."""
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    submodule_id = str(uuid4())
    submodule = {"id": submodule_id, **payload.model_dump()}
    module["submodules"][submodule_id] = submodule
    return submodule


@app.get("/courses/{course_id}/modules/{module_id}/submodules/{submodule_id}",
         summary="Get a submodule")
def get_submodule(course_id: str, module_id: str, submodule_id: str):
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    return _get_submodule_or_404(module, submodule_id)


@app.put("/courses/{course_id}/modules/{module_id}/submodules/{submodule_id}",
         summary="Update a submodule")
def update_submodule(course_id: str, module_id: str, submodule_id: str,
                     payload: SubmoduleUpdate):
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    submodule = _get_submodule_or_404(module, submodule_id)
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    submodule.update(updates)
    return submodule


@app.delete("/courses/{course_id}/modules/{module_id}/submodules/{submodule_id}",
            summary="Delete a submodule")
def delete_submodule(course_id: str, module_id: str, submodule_id: str):
    course = _get_course_or_404(course_id)
    module = _get_module_or_404(course, module_id)
    _get_submodule_or_404(module, submodule_id)
    del module["submodules"][submodule_id]
    return {"message": f"Submodule {submodule_id} deleted"}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_course_or_404(course_id: str) -> dict:
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]


def _get_module_or_404(course: dict, module_id: str) -> dict:
    if module_id not in course["modules"]:
        raise HTTPException(status_code=404, detail="Module not found")
    return course["modules"][module_id]


def _get_submodule_or_404(module: dict, submodule_id: str) -> dict:
    if submodule_id not in module["submodules"]:
        raise HTTPException(status_code=404, detail="Submodule not found")
    return module["submodules"][submodule_id]
