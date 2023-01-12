from django.contrib import admin

from .models import Article, Scope, Tag
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count_is_main = 0
        for form in self.forms:
            is_main = form.cleaned_data.get('is_main')
            if is_main:
                count_is_main += 1

            if count_is_main > 1:
                raise ValidationError('Поле is_main должно быть указано только 1 раз')
        return super().clean()  # вызываем базовый код переопределяемого метода


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 6
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]