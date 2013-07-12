from django.db import models, backend

class SearchQuerySet(models.query.QuerySet):
    def __init__(self, model=None, field=None):
        super(SearchQuerySet, self).__init__(model)
        self._search_field = field
        
    def search(self, query):
        meta = self.model._meta
        
        # Get the table name and column names from the model
        # in `table_name`.`column_name` style
        
        print "*", self._search_field
        
        print self._search_field
        
        column = meta.get_field(self._search_field, many_to_many=False).column
                
        full_name = "%s.%s" % (backend.quote_name(meta.db_table), backend.quote_name(column))

        # Create the MATCH...AGAINST expressions        
        fulltext_column = full_name
        match_expr = ("MATCH(%s) AGAINST (%%s)" % fulltext_column)
        
        # Add the extra SELECT and WHERE options
        return self.extra(select={'relevance': match_expr},
                          where=[match_expr],
                          params=[query, query])

class SearchManager(models.Manager):
    def __init__(self, field):
        super(SearchManager, self).__init__()
        self._search_field = field

    def get_query_set(self):
        return SearchQuerySet(self.model, self._search_field)

    def search(self, query):
        return self.get_query_set().search(query)
