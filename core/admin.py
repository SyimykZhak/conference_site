from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Register, Speakers, Conference, Program, Partners, Work
# Register your models here.

class ProgramInline(admin.StackedInline):
    model = Program
    extra = 1

class RegisterInline(admin.StackedInline):
    model = Register
    extra = 1

class PartnersInline(admin.StackedInline):
    model = Partners
    extra = 1

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display =("name","email","created")
    list_filter = ("conference","created",)
    readonly_fields = ("conference",'name', 'lastname', 'age', 'email','telephone','addres',)
    fieldsets = (
        (None,{
            "fields": ("name", "lastname","age",)
        }),
        (None,{
            "fields": ("email","telephone","addres",)
        }),
    )

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "tagline", "draft")
    inlines = [ProgramInline,PartnersInline,RegisterInline]
    list_filter = ("date",)
    search_fields = ("title", "category__name")
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "about", "poster", "get_image",)
        }),
        (None, {
            "fields": ("date","address","tickets","ostatok_tickets","kol_speakers","telephone","email","place","street","map",)
        }),
        ("Speakers", {
            "fields": ("speakers",)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"







@admin.register(Speakers)
class SpeakerAdmin(admin.ModelAdmin):
    # Спикеры
    list_display = ("name", "age", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display =("conference","description")
    list_filter = ("conference",)
   
@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    list_display =("title","description","get_logo",)
    list_filter = ("conference",)
    readonly_fields = ("get_logo",)

    def get_logo(self, obj):
        return mark_safe(f'<img src={obj.logo.url} width="60" height="40"')

    get_logo.short_description = "Изображение"

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display =("conference","work","created")
    list_filter = ("conference","created")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.work.url} width="50" height="60"')

    get_image.short_description = "Изображение"