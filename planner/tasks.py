from conductor import celeryapp


@celeryapp.task
def audit_school(school_id):
    """Audit a school if it has not been recently audited."""
