from sqlalchemy import event

from sqlalchemy.orm import Session


from .models.activities import Activity


@event.listens_for(Session, "before_flush")
def set_activity_depth(session: Session, *_):
    for obj in session.new:
        if isinstance(obj, Activity):
            if obj.parent_id is None:
                obj.depth = 1
            else:
                if obj.parent is None:
                    obj.parent = session.get(Activity, obj.parent_id)
                obj.depth = obj.parent.depth + 1
