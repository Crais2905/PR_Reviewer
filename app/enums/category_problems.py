from enum import Enum


class ProblemsCategory(Enum):
    BUG_RISK = "bug_risk"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    BEST_PRACTICE = "best_practice"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
