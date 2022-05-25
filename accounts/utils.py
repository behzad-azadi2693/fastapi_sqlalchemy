from config.models import ImageModel
from uuid import uuid4


def check_name(name, db):
    file_name = db.query(ImageModel).filter(ImageModel.image == name).first()

    if file_name:
        pre, post = name.split('.')
        new_name  = f"{pre}-{uuid4()}.{post}"
        return check_name(new_name, db)
    return name
