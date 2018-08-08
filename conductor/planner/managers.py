import functools
import operator

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db import models


class SchoolManager(models.Manager):
    """A manager for schools"""

    def search(self, name):
        """Search for a school by name."""
        queryset = self.get_queryset()
        terms = [SearchQuery(term) for term in name.split()]
        vector = SearchVector("name")
        query = functools.reduce(operator.or_, terms)
        queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by("-rank")
        # This is a magic value. By inspecting rank,
        # it appeared that anything below 0.04 was junk.
        queryset = queryset.filter(rank__gte=0.04)
        return queryset
