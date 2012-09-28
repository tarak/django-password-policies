import inspect
from django.utils.html import strip_tags
from django.utils.encoding import force_unicode


def process_docstring(app, what, name, obj, options, lines):
    # This causes import errors if left outside the function
    from django.db import models
    
    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        fields = obj._meta._fields()
    
        for field in fields:
            # Decode and strip any html out of the field's help text
            help_text = strip_tags(force_unicode(field.help_text))
            
            # Decode and capitalize the verbose name, for use if there isn't
            # any help text
            verbose_name = force_unicode(field.verbose_name).capitalize()
            
            if help_text:
                # Add the model field to the end of the docstring as a param
                # using the help text as the description
                lines.append(u':param %s: %s' % (field.attname, help_text))
            else:
                # Add the model field to the end of the docstring as a param
                # using the verbose name as the description
                lines.append(u':param %s: %s' % (field.attname, verbose_name))
                
            # Add the field's type to the docstring
            if isinstance(field, models.ForeignKey):
                to = field.rel.to
                lines.append(u':type %s: %s to :class:`~%s.%s`' % (field.attname, type(field).__name__, to.__module__, to.__name__))
            else:
                lines.append(u':type %s: %s' % (field.attname, type(field).__name__))
    
    # Return the extended docstring
    return lines 


def setup(app):
    app.add_crossref_type(
        directivename = "admin",
        rolename      = "admin",
        indextemplate = "pair: %s; admin",
    )
    app.add_crossref_type(
        directivename = "command",
        rolename      = "command",
        indextemplate = "pair: %s; command",
    )
    app.add_crossref_type(
        directivename = "context_processors",
        rolename      = "context_processors",
        indextemplate = "pair: %s; context_processors",
    )
    app.add_crossref_type(
        directivename = "form",
        rolename      = "form",
        indextemplate = "pair: %s; form",
    )
    app.add_crossref_type(
        directivename = "formfield",
        rolename      = "formfield",
        indextemplate = "pair: %s; formfield",
    )
    app.add_crossref_type(
        directivename = "manager",
        rolename      = "manager",
        indextemplate = "pair: %s; manager",
    )
    app.add_crossref_type(
        directivename = "middleware",
        rolename      = "middleware",
        indextemplate = "pair: %s; middleware",
    )
    app.add_crossref_type(
        directivename = "model",
        rolename      = "model",
        indextemplate = "pair: %s; model",
    )
    app.add_crossref_type(
        directivename = "setting",
        rolename      = "setting",
        indextemplate = "pair: %s; setting",
    )
    app.add_crossref_type(
        directivename = "settings",
        rolename      = "settings",
        indextemplate = "pair: %s; settings",
    )
    app.add_crossref_type(
        directivename = "signal",
        rolename      = "signal",
        indextemplate = "pair: %s; signal",
    )
    app.add_crossref_type(
        directivename = "token",
        rolename      = "token",
        indextemplate = "pair: %s; token",
    )
    app.add_crossref_type(
        directivename = "validator",
        rolename      = "validator",
        indextemplate = "pair: %s; validator",
    )
    app.add_crossref_type(
        directivename = "view",
        rolename      = "view",
        indextemplate = "pair: %s; view",
    )
    # Register the docstring processor with sphinx
    #app.connect('autodoc-process-docstring', process_docstring)
