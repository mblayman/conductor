from typing import List, Optional

from django import template

from conductor.planner.models import Milestone

register = template.Library()


@register.simple_tag
def get_milestone_by_category(
    category: str, milestones: List[Milestone]
) -> Optional[Milestone]:
    for milestone in milestones:
        if milestone.category == category:
            return milestone
    return None
