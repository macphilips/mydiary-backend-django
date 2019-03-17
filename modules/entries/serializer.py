from modules.account.serializer import OwnerSerializer
from modules.base_model import BaseModelSerializer
from modules.entries.models import Entry


class EntrySerializer(BaseModelSerializer):
    owner = OwnerSerializer(read_only=True)

    class Meta:
        partial = True
        fields = (
            'id',
            'title',
            'content',
            'createdDate',
            'lastModified',
            'owner'
        )
        model = Entry
