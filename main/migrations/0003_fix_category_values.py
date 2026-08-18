from django.db import migrations, models


CANONICAL_CATEGORIES = [
    "Milliy taomlar",
    "Fast Food",
    "Shirinliklar",
    "Salatlar",
    "Ichimliklar",
]

# Ma'lumotlar bazasida uchragan, canonical nomlardan farq qiladigan
# ("Milliy taomlar" o'rniga "Milliy taom" kabi) eski/xato yozilgan
# qiymatlar uchun moslik. Kalitlar kichik harfda va bo'sh joylarsiz
# solishtiriladi.
LEGACY_CATEGORY_FIXES = {
    "milliy taom": "Milliy taomlar",
}


def fix_category_values(apps, schema_editor):
    """Mavjud Recipe yozuvlaridagi category qiymatlarini canonical
    kategoriya nomlariga moslab to'g'rilaydi. Hech qanday yozuv
    o'chirilmaydi yoki reset qilinmaydi - faqat 'category' maydoni
    yangilanadi (agar kerak bo'lsa)."""
    Recipe = apps.get_model('main', 'Recipe')

    for recipe in Recipe.objects.all():
        raw_value = recipe.category or ""
        normalized = " ".join(raw_value.split())  # ortiqcha bo'sh joylarni yig'ish
        lowered = normalized.lower()

        canonical_match = None

        # 1) Katta-kichik harf/bo'sh joy farqi bilan canonical ro'yxatga mos kelsa
        for cat in CANONICAL_CATEGORIES:
            if lowered == cat.lower():
                canonical_match = cat
                break

        # 2) Ma'lum bo'lgan eski/xato yozilgan variantlar bilan mos kelsa
        if canonical_match is None and lowered in LEGACY_CATEGORY_FIXES:
            canonical_match = LEGACY_CATEGORY_FIXES[lowered]

        if canonical_match and recipe.category != canonical_match:
            recipe.category = canonical_match
            recipe.save(update_fields=['category'])


def reverse_noop(apps, schema_editor):
    # Orqaga qaytarishning hojati yo'q - bu faqat xato yozuvlarni
    # to'g'rilaydi, ma'lumotni yo'qotmaydi.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_recipe_instructions_recipe_servings_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_category_values, reverse_noop),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(
                max_length=100,
                choices=[
                    ('Milliy taomlar', 'Milliy taomlar'),
                    ('Fast Food', 'Fast Food'),
                    ('Shirinliklar', 'Shirinliklar'),
                    ('Salatlar', 'Salatlar'),
                    ('Ichimliklar', 'Ichimliklar'),
                ],
            ),
        ),
    ]
