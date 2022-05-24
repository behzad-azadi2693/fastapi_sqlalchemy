from enum import Enum
from config.models import BlogModel
from uuid import uuid4


class Status(str, Enum):
    importanr = 'importanr'
    necessary = 'necessary'
    usually   = 'usually'
    
  
def check_name(name, db):
    file_name = db.query(BlogModel).filter(BlogModel.image == name).first()

    if file_name:
        pre, post = name.split('.')
        new_name  = f"{pre}-{uuid4()}.{post}"
        return check_name(new_name, db)
    return name

