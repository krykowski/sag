from django.forms import Form, ModelForm, BaseForm
from django.forms.util import ErrorList
from django.forms.forms import BoundField
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class ErrorListExt(ErrorList):
    def __unicode__(self):
        return self.as_p()
    
    def as_p(self):
        if not self: 
            return u''
        
        return u'%s' % ''.join([u'<p class="help-block">%s</p>' % e for e in self])
      
class BaseFormExt(BaseForm):  
    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row, stacked=None):
        "Helper function for outputting HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors() # Errors that should be displayed above all fields.
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            html_class_attr = ''
            container_class = ''
            bf = BoundField(self, field, name)
            
            if stacked is not None:
                self.error_class = ErrorListExt
            
            bf_errors = self.error_class([conditional_escape(error) for error in bf.errors]) # Escape and cache in local variable.
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend([u'(Hidden field %s) %s' % (name, force_unicode(e)) for e in bf_errors])
                hidden_fields.append(unicode(bf))
            else:
                # Create a 'class="..."' atribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % force_unicode(bf_errors))

                if bf.label:
                    label = conditional_escape(force_unicode(bf.label))
                    # Only add the suffix if the label does not end in
                    # punctuation.
                    if self.label_suffix:
                        if label[-1] not in ':?.!':
                            label += self.label_suffix
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % force_unicode(field.help_text)
                else:
                    help_text = u''
                    
                if bf_errors:
                    container_class = 'error'
                    
                output.append(normal_row % {
                    'errors': force_unicode(bf_errors),
                    'label': force_unicode(label),
                    'field': unicode(bf),
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'container_class': container_class,
                })

        if top_errors:
            output.insert(0, error_row % force_unicode(top_errors))

        if hidden_fields: # Insert any hidden fields in the last row.
            str_hidden = u''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {'errors': '', 'label': '',
                                              'field': '', 'help_text':'',
                                              'html_class_attr': html_class_attr})
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
                
        return mark_safe(u'\n'.join(output))
        
    def as_bstrap(self):
        return self._as_bstrap(False)
        
    def as_bstrap_stacked(self):
        return self._as_bstrap()
        
    def _as_bstrap(self, stacked=True):
        if stacked:
            helpText = u'<p class="help-inline">%s</p>'
        else:
            helpText = u'<p class="help-block">%s</p>'
            
        return self._html_output(
            normal_row = u'<div class="control-group %(container_class)s">%(label)s <div class="controls">%(field)s%(help_text)s%(errors)s</div></div>',
            error_row = helpText,
            row_ender = '</div>',
            help_text_html = helpText,
            errors_on_separate_row = False,
            stacked = stacked)
        
class FormExt(BaseFormExt, Form):
    pass
        
class ModelFormExt(BaseFormExt, ModelForm):
    pass
    